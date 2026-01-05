from typing import List


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return []

    if chunk_size <= 0:
        return [cleaned]

    chunks: List[str] = []
    start = 0
    length = len(cleaned)
    overlap = max(0, min(overlap, chunk_size - 1))

    while start < length:
        end = min(start + chunk_size, length)
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= length:
            break
        start = end - overlap

    return chunks
