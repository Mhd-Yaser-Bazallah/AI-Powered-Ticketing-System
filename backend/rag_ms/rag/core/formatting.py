from typing import List
from rag.core.types import RetrievedChunk

def format_context(chunks, max_chars_per_chunk: int = 900) -> str:
    lines = []
    for c in chunks:
        cite = f"[{c.source_type}:{c.source_id}#{c.chunk_id}]"
        txt = (c.text or "").strip()
        if len(txt) > max_chars_per_chunk:
            txt = txt[:max_chars_per_chunk].rsplit(" ", 1)[0] + "..."
        lines.append(f"{cite}\n{txt}")
    return "\n\n".join(lines)



def citations_from_chunks(chunks: List[RetrievedChunk]):
    return [
        {
            "source_type": c.source_type,
            "source_id": c.source_id,
            "chunk_id": c.chunk_id,
            "score": c.score,
        }
        for c in chunks
    ]
