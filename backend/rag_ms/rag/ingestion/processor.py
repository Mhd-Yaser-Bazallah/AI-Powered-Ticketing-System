import os
import uuid
import logging
from typing import Dict, List, Optional

from django.conf import settings
from qdrant_client.http import models as qmodels

from rag.core.embeddings import LocalEmbeddings
from rag.core.qdrant_store import get_qdrant, ensure_collection, delete_by_filter, upsert_points
from .chunking import chunk_text
from .extractors import extract_text

logger = logging.getLogger(__name__)


def resolve_file_path(payload: Dict[str, str]) -> str:
    direct_path = payload.get("file_path") or ""
    if direct_path:
        return direct_path

    rel_path = payload.get("file_relative_path") or ""
    base_path = settings.RAG_FILES_BASE_PATH or ""
    if rel_path and base_path:
        return os.path.join(base_path, rel_path)

    return ""


def ingest_file(payload: Dict[str, str]) -> int:
    file_path = resolve_file_path(payload)
    if not file_path:
        raise ValueError("file_path not provided and RAG_FILES_BASE_PATH not set")
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    file_id = str(payload.get("file_id") or "")
    company_id = payload.get("company_id")
    if company_id is None:
        raise ValueError("company_id missing in payload")
    kind = payload.get("kind") or ""
    original_name = payload.get("original_name") or ""
    content_type = payload.get("content_type") or ""

    text = extract_text(file_path, kind=kind)
    chunks = chunk_text(text)
    if not chunks:
        return 0

    client = get_qdrant()
    ensure_collection(client, settings.QDRANT_COLLECTION, vector_size=384)
    emb = LocalEmbeddings()
    vectors = emb.embed_documents(chunks)

    points: List[qmodels.PointStruct] = []
    total_chunks = len(chunks)
    for idx, (chunk, vector) in enumerate(zip(chunks, vectors)):
        payload_doc = {
            "text": chunk,
            "source_type": "file",
            "source_id": file_id,
            "company_id": company_id,
            "chunk_id": f"{file_id}-{idx}",
            "file_name": original_name,
            "file_path": file_path,
            "kind": kind,
            "content_type": content_type,
            "chunk_index": idx,
            "total_chunks": total_chunks,
        }
        points.append(
            qmodels.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payload_doc,
            )
        )

    upsert_points(client, settings.QDRANT_COLLECTION, points)
    logger.info("Ingested %s chunks for file_id=%s", total_chunks, file_id)
    return total_chunks


def delete_file_chunks(file_id: str, company_id: int | None) -> None:
    if not file_id or company_id is None:
        return
    client = get_qdrant()
    ensure_collection(client, settings.QDRANT_COLLECTION, vector_size=384)
    q_filter = qmodels.Filter(
        must=[
            qmodels.FieldCondition(
                key="source_type",
                match=qmodels.MatchValue(value="file"),
            ),
            qmodels.FieldCondition(
                key="source_id",
                match=qmodels.MatchValue(value=file_id),
            ),
            qmodels.FieldCondition(
                key="company_id",
                match=qmodels.MatchValue(value=company_id),
            ),
        ]
    )
    delete_by_filter(client, settings.QDRANT_COLLECTION, q_filter)
    logger.info("Deleted chunks for file_id=%s", file_id)
