import json
import logging

from django.conf import settings
from django.utils import timezone
from django.http import StreamingHttpResponse
from qdrant_client.http import models as qmodels
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rag.core.embeddings import LocalEmbeddings
from rag.core.qdrant_store import get_qdrant, ensure_collection
from rag.core.retriever import QdrantRetriever
from rag.core.graphs.chat_graph import build_chat_graph
from rag.api.solution_service import generate_solution_from_request

from .auth import HasRagApiKey
from .serializers import (
    ChatRequestSerializer,
    ChatResponseSerializer,
    RetrieveRequestSerializer,
    RetrieveResponseSerializer,
    SeedRequestSerializer,
)
from rag.tasks import process_ticket_created

logger = logging.getLogger(__name__)


def _sse(event_name: str, data: dict) -> str:
    return f"event: {event_name}\ndata: {json.dumps(data, ensure_ascii=True)}\n\n"


class HealthView(APIView):
    permission_classes = [HasRagApiKey]

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "service": "rag-ms",
                "timestamp": timezone.now().isoformat(),
            },
            status=status.HTTP_200_OK,
        )


class RagSolutionView(APIView):
                                         

    def post(self, request):
        payload = generate_solution_from_request(request.data)
        return Response(payload, status=status.HTTP_200_OK)


class RagChatView(APIView):
    permission_classes = [HasRagApiKey]

    def post(self, request):
        req = ChatRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        data = req.validated_data

        ticket = data.get("ticket") or {}
        company_id = data.get("company_id")

        graph = build_chat_graph()
        initial_state = {
            "conversation_id": str(data.get("conversation_id")) if data.get("conversation_id") else None,
            "user_message": data["message"],
            "ticket_description": ticket.get("description"),
            "ticket_category": ticket.get("category"),
            "ticket_priority": ticket.get("priority"),
            "company_id": company_id,
            "trace_events": [],
            "event_id_counter": 0,
        }

        def event_stream():
            yield ":\n\n"
            last_event_id = 0
            try:
                for state in graph.stream(initial_state, stream_mode="values"):
                    events = state.get("trace_events") or []
                    for ev in events:
                        if ev["event_id"] <= last_event_id:
                            continue
                        last_event_id = ev["event_id"]
                        if ev["stage"] == "final":
                            payload = state.get("final_payload") or {}
                            data = {"event_id": ev["event_id"], "stage": "final", "payload": payload}
                            yield _sse("final", data)
                            return
                        yield _sse("stage", ev)
            except Exception as exc:
                err = {
                    "event_id": last_event_id + 1,
                    "stage": "error",
                    "message": str(exc),
                }
                yield _sse("error", err)

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream; charset=utf-8")
        response["Cache-Control"] = "no-cache, no-transform"
                                               
        response["X-Accel-Buffering"] = "no"
        return response


class RagRetrieveView(APIView):
    permission_classes = [HasRagApiKey]

    def post(self, request):
        req = RetrieveRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        data = req.validated_data

        retriever = QdrantRetriever()
        chunks = retriever.retrieve(
            query=data["query"],
            company_id=data["company_id"],
            top_k=data["top_k"],
            filters=data.get("filters"),
            score_threshold=data.get("score_threshold"),
        )

        payload = {
            "items": [
                {
                    "score": c.score,
                    "text": c.text,
                    "source_type": c.source_type,
                    "source_id": c.source_id,
                    "chunk_id": c.chunk_id,
                    "metadata": c.metadata,
                }
                for c in chunks
            ]
        }

        res = RetrieveResponseSerializer(data=payload)
        res.is_valid(raise_exception=True)
        return Response(res.data, status=status.HTTP_200_OK)


class DevSeedView(APIView):
                                         

    def post(self, request):
        req = SeedRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)

        client = get_qdrant()
        collection = settings.QDRANT_COLLECTION
        company_id = req.validated_data.get("company_id", 0)

        if req.validated_data.get("wipe"):
            try:
                client.delete_collection(collection_name=collection)
            except Exception:
                pass

        ensure_collection(client, collection, vector_size=384)

        emb = LocalEmbeddings()
        docs = [
            {
                "text": "Refund Policy: Duplicate charges are refundable if confirmed by billing logs. Process within 5 business days.",
                "source_type": "policy",
                "source_id": "refund_policy_v1",
                "chunk_id": "p1-c1",
                "category": "billing",
                "company_id": company_id,
            },
            {
                "text": "Billing Procedure: If a customer retries payment and gets double charged, verify transaction IDs and refund the duplicate charge.",
                "source_type": "policy",
                "source_id": "billing_procedure_v2",
                "chunk_id": "p2-c3",
                "category": "billing",
                "company_id": company_id,
            },
            {
                "text": "Catalog: Payment retry may create a second transaction. Use reconciliation to merge records and avoid double capture.",
                "source_type": "catalog",
                "source_id": "payments_catalog",
                "chunk_id": "c1",
                "category": "billing",
                "company_id": company_id,
            },
            {
                "text": "Solved Ticket T-8831: Double charge after retry. Steps: verify two transaction IDs, refund the duplicate, notify customer with confirmation.",
                "source_type": "solved_ticket",
                "source_id": "T-8831",
                "chunk_id": "t-c7",
                "category": "billing",
                "company_id": company_id,
            },
            {
                "text": "Solved Ticket T-9012: Customer charged twice due to timeout. Steps: check gateway logs, refund second charge, add note to account.",
                "source_type": "solved_ticket",
                "source_id": "T-9012",
                "chunk_id": "t-c2",
                "category": "billing",
                "company_id": company_id,
            },
        ]

        vectors = emb.embed_documents([d["text"] for d in docs])

        points = []
        for d, v in zip(docs, vectors):
            points.append(
                qmodels.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=v,
                    payload=d,
                )
            )

        client.upsert(collection_name=collection, points=points)

        return Response({"seeded": len(points), "collection": collection}, status=status.HTTP_200_OK)


class RagEventView(APIView):
    permission_classes = [HasRagApiKey]

    def post(self, request):
        payload = request.data or {}
        event_type = payload.get("event")
        logger.info(
            "Received RAG event=%s event_id=%s",
            event_type,
            payload.get("event_id"),
        )
        if event_type != "ticket.created":
            return Response({"error": "Unsupported event type"}, status=status.HTTP_400_BAD_REQUEST)

        required = ["event_id", "ticket_id", "description", "category", "priority"]
        missing = [k for k in required if k not in payload]
        if missing:
            return Response(
                {"error": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queue_name = getattr(settings, "CELERY_TASK_DEFAULT_QUEUE", "rag_events")
        try:
            process_ticket_created.apply_async(args=[payload], queue=queue_name)
            logger.info(
                "Enqueued process_ticket_created event_id=%s queue=%s",
                payload.get("event_id"),
                queue_name,
            )
            return Response({"accepted": True}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            logger.exception("Failed to enqueue ticket.created event")
            return Response({"accepted": False}, status=status.HTTP_202_ACCEPTED)
