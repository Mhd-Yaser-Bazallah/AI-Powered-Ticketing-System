from __future__ import annotations
from typing import List, Tuple
from django.conf import settings
from sentence_transformers import CrossEncoder

from rag.core.types import RetrievedChunk


class CrossEncoderReranker:
    def __init__(self) -> None:
        self.model = CrossEncoder(settings.RERANK_MODEL)

    def rerank(
        self,
        query: str,
        chunks: List[RetrievedChunk],
        top_k: int,
    ) -> List[RetrievedChunk]:
        if not chunks:
            return []

        pairs: List[Tuple[str, str]] = [(query, (c.text or "")) for c in chunks]
        scores = self.model.predict(pairs)

        scored = list(zip(chunks, scores))
        scored.sort(key=lambda x: float(x[1]), reverse=True)

        return [c for (c, _) in scored[:top_k]]
