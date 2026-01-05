import time
from typing import Any, Dict, List

from rag.core.types import RetrievedChunk
from rag.core.validators import extract_citations


def now_ms() -> int:
    return int(time.time() * 1000)


def add_event(
    state: Dict[str, Any],
    stage: str,
    input_summary: Dict[str, Any],
    output_summary: Dict[str, Any],
    skipped: bool = False,
    error: bool = False,
    duration_ms: int = 0,
) -> Dict[str, Any]:
    event_id = int(state.get("event_id_counter", 0)) + 1

    event = {
        "event_id": event_id,
        "stage": stage,
        "ts_ms": now_ms(),
        "duration_ms": int(duration_ms),
        "input": input_summary,
        "output": output_summary,
        "skipped": bool(skipped),
        "error": bool(error),
    }

    events = list(state.get("trace_events") or [])
    events.append(event)
    return {"event_id_counter": event_id, "trace_events": events}


def summarize_chunks(chunks: List[RetrievedChunk], max_items: int = 3) -> Dict[str, Any]:
    top = chunks[:max_items]
    return {
        "count": len(chunks),
        "top_doc_ids": [f"{c.source_type}:{c.source_id}#{c.chunk_id}" for c in top],
        "top_scores": [float(c.score) for c in top],
    }


def summarize_context(context_text: str) -> Dict[str, Any]:
    return {
        "context_chars": len(context_text or ""),
    }


def summarize_answer(answer: str) -> Dict[str, Any]:
    cites = extract_citations(answer or "")
    return {
        "answer_chars": len(answer or ""),
        "citations_count": len(cites),
    }
