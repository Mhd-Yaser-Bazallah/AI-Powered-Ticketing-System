from __future__ import annotations

import logging
from typing import Dict, Any

from django.conf import settings
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

from rag.core.formatting import format_context, citations_from_chunks
from rag.core.llm import get_llm
from rag.core.prompts import SOLUTION_SYSTEM
from rag.core.retriever import QdrantRetriever
from rag.core.reranker import CrossEncoderReranker
from rag.core.validators import validate_solution_steps
from rag.core.graphs.state import SolutionState
from rag.core.graphs.tracing import add_event, now_ms, summarize_chunks, summarize_context

_SOLUTION_GRAPH = None
logger = logging.getLogger(__name__)


def retrieve(state: SolutionState) -> Dict[str, Any]:
    start = now_ms()
    query = (
        f"TICKET: {state.get('ticket_description')}\n"
        f"CATEGORY: {state.get('ticket_category') or ''}\n"
        f"PRIORITY: {state.get('ticket_priority') or ''}\n"
        f"Generate troubleshooting steps."
    )

    retriever = QdrantRetriever()
    category = state.get("ticket_category")
    priority = state.get("ticket_priority")
    filters = {"category": category} if category else None
    min_chunks = getattr(settings, "RAG_MIN_CHUNKS_BEFORE_FALLBACK", 3)

    logger.info(
        "retrieve: category=%s priority=%s min_chunks=%s",
        category,
        priority,
        min_chunks,
    )

    attempt1 = retriever.retrieve(
        query=query,
        company_id=state.get("company_id"),
        top_k=settings.RAG_RETRIEVE_K,
        filters=filters,
        score_threshold=settings.RAG_MIN_SCORE,
    )
    attempt1_count = len(attempt1 or [])

    fallback_used = False
    attempt2_count = 0
    raw_chunks = attempt1
    if filters and attempt1_count < min_chunks:
        fallback_used = True
        attempt2 = retriever.retrieve(
            query=query,
            company_id=state.get("company_id"),
            top_k=settings.RAG_RETRIEVE_K,
            filters=None,
            score_threshold=settings.RAG_MIN_SCORE,
        )
        attempt2_count = len(attempt2 or [])
        if attempt2_count:
            raw_chunks = attempt2

    logger.info(
        "retrieve: attempt1_count=%s attempt2_count=%s filters=%s fallback_used=%s",
        attempt1_count,
        attempt2_count,
        filters,
        fallback_used,
    )

    trace_update = add_event(
        state,
        "retrieve",
        {
            "query_chars": len(query or ""),
            "top_k": settings.RAG_RETRIEVE_K,
            "filters": filters,
            "priority": priority,
            "attempt1_count": attempt1_count,
            "attempt2_count": attempt2_count,
            "fallback_used": fallback_used,
            "min_chunks_before_fallback": min_chunks,
            "score_threshold": settings.RAG_MIN_SCORE,
        },
        summarize_chunks(raw_chunks),
        duration_ms=now_ms() - start,
    )
    return {"query": query, "raw_chunks": raw_chunks, **trace_update}


def _route_rerank(state: SolutionState) -> str:
    if settings.RERANK_ENABLED and (state.get("raw_chunks") or []):
        return "rerank"
    return "skip_rerank"


def rerank(state: SolutionState) -> Dict[str, Any]:
    start = now_ms()
    raw_chunks = state.get("raw_chunks") or []
    reranked = CrossEncoderReranker().rerank(query=state.get("query") or "", chunks=raw_chunks, top_k=settings.RAG_TOP_K)

    trace_update = add_event(
        state,
        "rerank",
        {"raw_count": len(raw_chunks), "top_k": settings.RAG_TOP_K},
        summarize_chunks(reranked),
        duration_ms=now_ms() - start,
    )
    return {"chunks": reranked, **trace_update}


def skip_rerank(state: SolutionState) -> Dict[str, Any]:
    start = now_ms()
    raw_chunks = state.get("raw_chunks") or []
    trace_update = add_event(
        state,
        "rerank",
        {"raw_count": len(raw_chunks)},
        summarize_chunks(raw_chunks),
        skipped=True,
        duration_ms=now_ms() - start,
    )
    return {"chunks": raw_chunks, **trace_update}


def _route_no_docs(state: SolutionState) -> str:
    return "fallback_no_docs" if not (state.get("chunks") or []) else "build_context"


def fallback_no_docs(state: SolutionState) -> Dict[str, Any]:
    start = now_ms()
    trace_update = add_event(
        state,
        "fallback_no_docs",
        {"retrieved_count": len(state.get("chunks") or [])},
        {"needs_human": True},
        duration_ms=now_ms() - start,
    )
    return {
        "steps": [],
        "sources": [],
        "confidence": 0.0,
        "needs_human": True,
        **trace_update,
    }


def build_context(state: SolutionState) -> Dict[str, Any]:
    start = now_ms()
    chunks = state.get("chunks") or []
    if not chunks:
        trace_update = add_event(
            state,
            "build_context",
            {"retrieved_count": 0},
            {"context_chars": 0},
            skipped=True,
            duration_ms=now_ms() - start,
        )
        return {"context_text": "", **trace_update}

    context_text = format_context(chunks)
    trace_update = add_event(
        state,
        "build_context",
        {"retrieved_count": len(chunks)},
        summarize_context(context_text),
        duration_ms=now_ms() - start,
    )
    return {"context_text": context_text, **trace_update}


def llm_solution(state: SolutionState) -> Dict[str, Any]:
    start = now_ms()
    chunks = state.get("chunks") or []
    if not chunks:
        trace_update = add_event(
            state,
            "llm_solution",
            {"retrieved_count": 0},
            {"raw_steps_chars": 0},
            skipped=True,
            duration_ms=now_ms() - start,
        )
        return {**trace_update}

    llm = get_llm()
    prompt = [
        SystemMessage(content=SOLUTION_SYSTEM),
        HumanMessage(
            content=(
                f"CONTEXT:\n{state.get('context_text', '')}\n\n"
                f"TICKET DESCRIPTION:\n{state.get('ticket_description', '')}\n\n"
                f"Return steps now."
            )
        ),
    ]
    raw = llm.invoke(prompt).content.strip()

    trace_update = add_event(
        state,
        "llm_solution",
        {"context_chars": len(state.get("context_text") or "")},
        {"raw_steps_chars": len(raw or "")},
        duration_ms=now_ms() - start,
    )
    return {"raw_steps": raw, **trace_update}


def validate_steps(state: SolutionState) -> Dict[str, Any]:
    start = now_ms()
    chunks = state.get("chunks") or []
    if not chunks:
        trace_update = add_event(
            state,
            "validate_steps",
            {"raw_steps_chars": 0},
            {"needs_human": True},
            skipped=True,
            duration_ms=now_ms() - start,
        )
        return {**trace_update}

    raw = (state.get("raw_steps") or "").strip()
    if raw == "NEEDS_HUMAN":
        trace_update = add_event(
            state,
            "validate_steps",
            {"raw_steps_chars": len(raw)},
            {"needs_human": True},
            duration_ms=now_ms() - start,
        )
        return {"steps": [], "needs_human": True, **trace_update}

    steps = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit():
            steps.append(line)
        else:
            steps.append(line)

    ok = validate_solution_steps(steps)
    trace_update = add_event(
        state,
        "validate_steps",
        {"raw_steps_chars": len(raw)},
        {"valid": bool(ok), "steps_count": len(steps)},
        duration_ms=now_ms() - start,
    )
    if not ok:
        return {"steps": [], "needs_human": True, **trace_update}

    return {"steps": steps, "needs_human": False, **trace_update}


def finalize(state: SolutionState) -> Dict[str, Any]:
    start = now_ms()
    chunks = state.get("chunks") or []
    sources = citations_from_chunks(chunks) if chunks else []
    needs_human = bool(state.get("needs_human"))
    confidence = 0.0
    if sources and not needs_human:
        confidence = float(min(0.95, max(0.2, sources[0]["score"])))

    payload = {
        "mode": "solution",
        "steps": state.get("steps") or [],
        "confidence": confidence,
        "sources": sources,
        "needs_human": needs_human if chunks else True,
    }

    trace_update = add_event(
        state,
        "final",
        {},
        {"steps_count": len(payload.get("steps") or []), "sources_count": len(sources)},
        duration_ms=now_ms() - start,
    )
    return {"final_payload": payload, **trace_update}


def build_solution_graph():
    global _SOLUTION_GRAPH
    if _SOLUTION_GRAPH is not None:
        return _SOLUTION_GRAPH

    graph = StateGraph(SolutionState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("rerank", rerank)
    graph.add_node("skip_rerank", skip_rerank)
    graph.add_node("fallback_no_docs", fallback_no_docs)
    graph.add_node("build_context", build_context)
    graph.add_node("llm_solution", llm_solution)
    graph.add_node("validate_steps", validate_steps)
    graph.add_node("finalize", finalize)

    graph.set_entry_point("retrieve")

    graph.add_conditional_edges(
        "retrieve",
        _route_rerank,
        {"rerank": "rerank", "skip_rerank": "skip_rerank"},
    )
    graph.add_conditional_edges(
        "rerank",
        _route_no_docs,
        {"fallback_no_docs": "fallback_no_docs", "build_context": "build_context"},
    )
    graph.add_conditional_edges(
        "skip_rerank",
        _route_no_docs,
        {"fallback_no_docs": "fallback_no_docs", "build_context": "build_context"},
    )

    graph.add_edge("fallback_no_docs", "finalize")
    graph.add_edge("build_context", "llm_solution")
    graph.add_edge("llm_solution", "validate_steps")
    graph.add_edge("validate_steps", "finalize")
    graph.add_edge("finalize", END)

    _SOLUTION_GRAPH = graph.compile()
    return _SOLUTION_GRAPH
