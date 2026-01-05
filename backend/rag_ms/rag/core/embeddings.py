from __future__ import annotations
from typing import List
from django.conf import settings
from sentence_transformers import SentenceTransformer


class LocalEmbeddings:
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.EMBEDDINGS_MODEL)

    def embed_query(self, text: str) -> List[float]:
        vec = self.model.encode([text], normalize_embeddings=True)[0]
        return vec.astype("float32").tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        vecs = self.model.encode(texts, normalize_embeddings=True)
        return [v.astype("float32").tolist() for v in vecs]
