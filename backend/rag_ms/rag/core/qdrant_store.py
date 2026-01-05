from __future__ import annotations
from typing import Any, Dict, List, Optional
from django.conf import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels


def get_qdrant() -> QdrantClient:
    return QdrantClient(url=settings.QDRANT_URL, api_key=(settings.QDRANT_API_KEY or None))


def ensure_collection(client: QdrantClient, name: str, vector_size: int) -> None:
    existing = [c.name for c in client.get_collections().collections]
    if name in existing:
        return
    client.create_collection(
        collection_name=name,
        vectors_config=qmodels.VectorParams(
            size=vector_size,
            distance=qmodels.Distance.COSINE,
        ),
    )


def upsert_points(
    client: QdrantClient,
    collection: str,
    points: List[qmodels.PointStruct],
) -> None:
    client.upsert(collection_name=collection, points=points)


def delete_by_filter(
    client: QdrantClient,
    collection: str,
    q_filter: qmodels.Filter,
) -> None:
    try:
        client.delete(
            collection_name=collection,
            points_selector=qmodels.FilterSelector(filter=q_filter),
        )
        return
    except Exception:
        pass

    if hasattr(client, "points_api") and hasattr(client.points_api, "delete_points"):
        client.points_api.delete_points(
            collection_name=collection,
            points_selector=qmodels.FilterSelector(filter=q_filter),
        )
        return

    raise RuntimeError("Unsupported qdrant-client version: delete not available.")
