from __future__ import annotations

from typing import Any, Dict, List, Optional
from qdrant_client.http import models as qmodels
from django.conf import settings

from .types import RetrievedChunk
from .embeddings import LocalEmbeddings
from .qdrant_store import get_qdrant, ensure_collection


def _build_filter(company_id: int, filters: Optional[Dict[str, Any]]) -> qmodels.Filter:
    must: List[qmodels.FieldCondition] = [
        qmodels.FieldCondition(key="company_id", match=qmodels.MatchValue(value=company_id))
    ]

    if filters:
        for key, value in filters.items():
            if value is None:
                continue
            must.append(qmodels.FieldCondition(key=key, match=qmodels.MatchValue(value=value)))

    return qmodels.Filter(must=must)


class QdrantRetriever:
    VECTOR_SIZE = 384                    

    def __init__(self) -> None:
        self.client = get_qdrant()
        self.collection = settings.QDRANT_COLLECTION
        self.emb = LocalEmbeddings()
        ensure_collection(self.client, self.collection, vector_size=self.VECTOR_SIZE)

    def _query_qdrant(
        self,
        vector: List[float],
        top_k: int,
        q_filter: Optional[qmodels.Filter],
        score_threshold: Optional[float],
    ):
                                 
        if hasattr(self.client, "query_points"):
            return self.client.query_points(
                collection_name=self.collection,
                query=vector,
                limit=top_k,
                query_filter=q_filter,
                with_payload=True,
                with_vectors=False,
                score_threshold=score_threshold,
            ).points

                                                 
        if hasattr(self.client, "points_api") and hasattr(self.client.points_api, "search_points"):
            res = self.client.points_api.search_points(
                collection_name=self.collection,
                search_request=qmodels.SearchRequest(
                    vector=vector,
                    limit=top_k,
                    filter=q_filter,
                    with_payload=True,
                    with_vector=False,
                    score_threshold=score_threshold,
                ),
            )
            return res.result

        raise RuntimeError("Unsupported qdrant-client version: no query_points/search_points found.")

    def retrieve(
        self,
        query: str,
        company_id: int,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None,
    ) -> List[RetrievedChunk]:
        if company_id is None:
            raise ValueError("company_id is required")
        vector = self.emb.embed_query(query)
        q_filter = _build_filter(company_id, filters)

        hits = self._query_qdrant(
            vector=vector,
            top_k=top_k,
            q_filter=q_filter,
            score_threshold=score_threshold,
        )

        out: List[RetrievedChunk] = []
        for h in hits:
            payload = getattr(h, "payload", None) or {}
            score = float(getattr(h, "score", 0.0) or 0.0)

            text = payload.get("text") or payload.get("content") or ""
            out.append(
                RetrievedChunk(
                    text=text,
                    score=score,
                    source_type=str(payload.get("source_type", "unknown")),
                    source_id=str(payload.get("source_id", "")),
                    chunk_id=str(payload.get("chunk_id", "")),
                    metadata={k: v for k, v in payload.items() if k not in {"text", "content"}},
                )
            )
        return out
