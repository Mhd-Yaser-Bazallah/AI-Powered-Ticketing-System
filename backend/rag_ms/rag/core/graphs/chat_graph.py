from __future__ import annotations

import re
from typing import Dict, Any, List, Tuple

from django.conf import settings
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

from rag.models import Conversation, Message
from rag.core.classifier import classify_chat_response
from rag.core.formatting import format_context, citations_from_chunks
from rag.core.llm import get_llm
from rag.core.prompts import CHAT_SYSTEM, SUMMARY_SYSTEM
from rag.core.retriever import QdrantRetriever
from rag.core.rewriter import rewrite_query
from rag.core.reranker import CrossEncoderReranker
from rag.core.validators import enforce_citations_if_needed, is_policy_like_question
from rag.core.graphs.state import ChatState
from rag.core.graphs.tracing import add_event, now_ms, summarize_chunks, summarize_context, summarize_answer

_CHAT_GRAPH = None

_SMALLTALK_RESPONSES = {
    "greeting": "Hi! How can I help with your ticket today?",
    "thanks": "You're welcome! Anything else you need help with?",
    "goodbye": "Glad I could help. If you need anything else, just ask.",
    "identity": "I'm your support assistant. Ask me about tickets, policies, or troubleshooting steps.",
    "ack": "Got it. Let me know if you have any other questions.",
}

_SMALLTALK_EXACT = {
    "hi",
    "hello",
    "hey",
    "yo",
    "thanks",
    "thank you",
    "thx",
    "ty",
    "bye",
    "goodbye",
    "ok",
    "okay",
    "kk",
    "k",
    "cool",
    "got it",
    "\u0645\u0631\u062d\u0628\u0627",         
    "\u0627\u0647\u0644\u0627",        
    "\u0623\u0647\u0644\u0627",        
    "\u0634\u0643\u0631\u0627",        
    "\u0645\u0639 \u0627\u0644\u0633\u0644\u0627\u0645\u0629",              
    "\u0627\u0644\u0633\u0644\u0627\u0645 \u0639\u0644\u064a\u0643\u0645",                
}

_SMALLTALK_TOKENS = {
    "hi": "greeting",
    "hello": "greeting",
    "hey": "greeting",
    "yo": "greeting",
    "thanks": "thanks",
    "thank": "thanks",
    "thx": "thanks",
    "ty": "thanks",
    "bye": "goodbye",
    "goodbye": "goodbye",
    "ok": "ack",
    "okay": "ack",
    "kk": "ack",
    "k": "ack",
    "cool": "ack",
    "got": "ack",
    "\u0645\u0631\u062d\u0628\u0627": "greeting",         
    "\u0627\u0647\u0644\u0627": "greeting",        
    "\u0623\u0647\u0644\u0627": "greeting",        
    "\u0634\u0643\u0631\u0627": "thanks",        
    "\u0645\u0639": "goodbye",              
    "\u0627\u0644\u0633\u0644\u0627\u0645": "greeting",                
}

_SMALLTALK_PATTERNS = [
    (r"^(hi|hello|hey|yo|good (morning|afternoon|evening))\b", "greeting"),
    (r"^(thanks|thank you|thx|ty)\b", "thanks"),
    (r"^(bye|goodbye|see you|later|cya)\b", "goodbye"),
    (r"^(who are you|what can you do|what do you do)\b", "identity"),
    (r"^(ok|okay|kk|k|cool|got it)\b", "ack"),
    (r"^\u0645\u0631\u062d\u0628\u0627\b", "greeting"),         
    (r"^\u0627\u0647\u0644\u0627\b", "greeting"),        
    (r"^\u0623\u0647\u0644\u0627\b", "greeting"),        
    (r"^\u0627\u0644\u0633\u0644\u0627\u0645 \u0639\u0644\u064a\u0643\u0645\b", "greeting"),                
    (r"^\u0634\u0643\u0631\u0627\b", "thanks"),        
    (r"^\u0645\u0639 \u0627\u0644\u0633\u0644\u0627\u0645\u0629\b", "goodbye"),              
    (r"^\u0645\u0646 \u0627\u0646\u062a|\u0645\u0627\u0630\u0627 \u062a\u0641\u0639\u0644\b", "identity"),                      
]

_PRONOUN_PATTERNS = [
    r"\b(this|that|it|these|those|above|previous|earlier|before|same|the other|other one)\b",
    r"\b(that issue|that one|the other)\b",
    r"\u0647\u0630\u0627|\u0647\u0630\u0647|\u0647\u0630\u064a|\u0630\u0627\u0643|\u0630\u0644\u0643",                       
    r"\u0627\u0644\u0644\u064a \u0642\u0628\u0644|\u0627\u0644\u0633\u0627\u0628\u0642",                   
]

_FOLLOWUP_PATTERNS = [
    r"^(why|how|what about|how about)\b",
    r"\b(why|how)\?$",
    r"\b(what about the other|the other one|another one)\b",
    r"\b(also|and also)\b",
    r"\u0644\u064a\u0634|\u0643\u064a\u0641|\u0648 \u0643\u0645\u0627\u0646|\u0637\u064a\u0628 \u0648\u0627\u0644\u062b\u0627\u0646\u064a",                              
]

_STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "is",
    "are",
    "was",
    "were",
    "to",
    "for",
    "of",
    "in",
    "on",
    "at",
    "with",
    "this",
    "that",
    "it",
    "its",
    "my",
    "your",
    "our",
    "their",
    "we",
    "you",
    "i",
    "me",
    "what",
    "why",
    "how",
    "when",
    "where",
    "who",
    "which",
    "about",
    "other",
    "one",
    "ones",
    "also",
    "please",
    "pls",
    "\u0645\u0627",      
    "\u0645\u0627\u0630\u0627",        
    "\u0643\u064a\u0641",       
    "\u0644\u064a\u0634",       
    "\u0647\u0644",      
    "\u0647\u0648",      
    "\u0647\u064a",      
    "\u0647\u0630\u0627",       
    "\u0647\u0630\u0647",       
    "\u0630\u0644\u0643",       
    "\u0648",     
    "\u0641\u064a",      
    "\u0639\u0644\u0649",       
    "\u0645\u0646",      
    "\u0627\u0644\u0649",       
}


def _should_update_summary(conv: Conversation) -> bool:
    user_count = conv.messages.filter(role=Message.ROLE_USER).count()
    return user_count > 0 and (user_count % settings.SUMMARY_EVERY_N == 0)


def _update_summary(conv: Conversation) -> None:
    last_msgs = list(conv.messages.order_by("-created_at")[: settings.CHAT_LAST_N])[::-1]
    transcript = "\n".join([f"{m.role}: {m.content}" for m in last_msgs])

    llm = get_llm()
    prompt = [
        SystemMessage(content=SUMMARY_SYSTEM),
        HumanMessage(
            content=f"Existing summary:\n{conv.summary or ''}\n\nRecent transcript:\n{transcript}\n\nUpdate the summary."
        ),
    ]
    summary = llm.invoke(prompt).content.strip()
    conv.summary = summary
    conv.save(update_fields=["summary"])


def _build_query(standalone: str, ticket_description: str | None) -> str:
    if ticket_description:
        return f"TICKET: {ticket_description}\n\nQUERY: {standalone}"
    return standalone


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9]+|[\u0600-\u06FF]+", text or "")


def _has_concrete_terms(tokens: List[str]) -> bool:
    for token in tokens:
        if token.lower() not in _STOPWORDS and len(token) > 2:
            return True
    return False


def _has_reference_terms(text: str) -> bool:
    lowered = _normalize_text(text)
    return any(re.search(pattern, lowered) for pattern in _PRONOUN_PATTERNS)


def _is_follow_up(text: str) -> bool:
    lowered = _normalize_text(text)
    return any(re.search(pattern, lowered) for pattern in _FOLLOWUP_PATTERNS)


def _detect_smalltalk(text: str) -> Tuple[bool, str]:
    lowered = _normalize_text(text)
    if lowered in _SMALLTALK_EXACT:
        for pattern, kind in _SMALLTALK_PATTERNS:
            if re.search(pattern, lowered):
                return True, _SMALLTALK_RESPONSES.get(kind, _SMALLTALK_RESPONSES["ack"])
        return True, _SMALLTALK_RESPONSES["greeting"]
    tokens = _tokenize(lowered)
    if 0 < len(tokens) <= 3:
        for token in tokens:
            kind = _SMALLTALK_TOKENS.get(token.lower())
            if kind:
                return True, _SMALLTALK_RESPONSES.get(kind, _SMALLTALK_RESPONSES["ack"])
    for pattern, kind in _SMALLTALK_PATTERNS:
        if re.search(pattern, lowered):
            if kind in {"greeting", "thanks", "goodbye", "ack"} and len(tokens) > 6:
                return False, ""
            return True, _SMALLTALK_RESPONSES.get(kind, _SMALLTALK_RESPONSES["ack"])
    return False, ""


def _should_rewrite(state: ChatState) -> bool:
    message = state.get("user_message") or ""
    if not message:
        return False

    has_context = bool(state.get("summary") or state.get("ticket_description"))
    if not has_context:
        return False

    if _detect_smalltalk(message)[0]:
        return False

    tokens = _tokenize(message)
    if not tokens:
        return False

    has_pronoun = _has_reference_terms(message)
    follow_up = _is_follow_up(message)
    short = len(tokens) <= 4
    lacks_keywords = not _has_concrete_terms(tokens)

    return bool(has_pronoun or follow_up or (short and lacks_keywords))


def _split_multi_questions(text: str) -> List[str]:
    cleaned = (text or "").strip()
    if not cleaned:
        return []

    q_marks = re.findall(r"[?\u061f]", cleaned)
    if len(q_marks) >= 2:
        parts = re.split(r"[?\u061f]+", cleaned)
        return [p.strip() for p in parts if p.strip()]

    if re.search(r"\b\d+[.)]\s+", cleaned):
        parts = re.split(r"\b\d+[.)]\s+", cleaned)
        return [p.strip() for p in parts if p.strip()]

    if "\n" in cleaned:
        parts = [p.strip() for p in cleaned.splitlines() if p.strip()]
        if len(parts) >= 2:
            return parts

    return []


def persist_user_message(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    conversation_id = state.get("conversation_id")
    if conversation_id:
        conv = Conversation.objects.get(id=conversation_id)
    else:
        conv = Conversation.objects.create(
            ticket_description=state.get("ticket_description"),
            ticket_category=state.get("ticket_category"),
            ticket_priority=state.get("ticket_priority"),
        )

    msg = Message.objects.create(
        conversation=conv,
        role=Message.ROLE_USER,
        content=state["user_message"],
    )

    trace_update = add_event(
        state,
        "persist_user_message",
        {
            "conversation_id_provided": bool(conversation_id),
            "message_chars": len(state["user_message"] or ""),
        },
        {
            "conversation_id": str(conv.id),
            "message_id": str(msg.id),
        },
        duration_ms=now_ms() - start,
    )

    return {
        "conversation": conv,
        "conversation_id": str(conv.id),
        "summary": conv.summary or "",
        **trace_update,
    }


def _route_rewrite(state: ChatState) -> str:
    return "rewrite" if _should_rewrite(state) else "skip_rewrite"


def smalltalk_router(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    message = state.get("user_message") or ""
    normalized = _normalize_text(message)
    tokens = _tokenize(normalized)
    matched, response = _detect_smalltalk(message)
    trace_update = add_event(
        state,
        "smalltalk_router",
        {"message_chars": len(message or "")},
        {"matched": bool(matched), "normalized": normalized, "tokens": tokens},
        duration_ms=now_ms() - start,
    )
    if not matched:
        return {"smalltalk_match": False, **trace_update}

    return {
        "smalltalk_match": True,
        "answer": response,
        "sources": [],
        "confidence": 0.0,
        **trace_update,
    }


def _route_after_smalltalk(state: ChatState) -> str:
    if state.get("smalltalk_match") or state.get("answer"):
        return "smalltalk_done"
    return _route_rewrite(state)


def rewrite(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    try:
        standalone = rewrite_query(
            user_message=state["user_message"],
            summary=state.get("summary", ""),
            ticket_description=state.get("ticket_description"),
            ticket_category=state.get("ticket_category"),
            ticket_priority=state.get("ticket_priority"),
        )
        error = False
    except Exception:
        standalone = state["user_message"]
        error = True
    trace_update = add_event(
        state,
        "rewrite",
        {"user_message_chars": len(state["user_message"] or "")},
        {"standalone_chars": len(standalone or "")},
        skipped=False,
        error=error,
        duration_ms=now_ms() - start,
    )
    return {"standalone_query": standalone, **trace_update}


def skip_rewrite(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    trace_update = add_event(
        state,
        "rewrite",
        {"user_message_chars": len(state["user_message"] or "")},
        {"standalone_chars": len(state["user_message"] or "")},
        skipped=True,
        duration_ms=now_ms() - start,
    )
    return {"standalone_query": state["user_message"], **trace_update}


def multi_question_router(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    standalone = state.get("standalone_query") or state.get("user_message") or ""
    sub_questions = _split_multi_questions(standalone)
    multi = len(sub_questions) >= 2

    trace_update = add_event(
        state,
        "multi_question_router",
        {"standalone_chars": len(standalone)},
        {"multi": bool(multi), "sub_questions_count": len(sub_questions)},
        duration_ms=now_ms() - start,
    )

    if not multi:
        return {**trace_update}

    combined = "\n".join([f"{idx + 1}) {q}" for idx, q in enumerate(sub_questions)])
    return {
        "sub_questions": sub_questions,
        "standalone_query": combined,
        **trace_update,
    }


def retrieve(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    standalone = state.get("standalone_query") or state["user_message"]
    query = _build_query(standalone, state.get("ticket_description"))

    retriever = QdrantRetriever()
    filters = {"category": state.get("ticket_category")} if state.get("ticket_category") else None
    raw_chunks = retriever.retrieve(
        query=query,
        company_id=state.get("company_id"),
        top_k=settings.RAG_RETRIEVE_K,
        filters=filters,
        score_threshold=settings.RAG_MIN_SCORE,
    )
    attempt1_count = len(raw_chunks or [])
    attempt2_count = 0
    fallback_used = False
    if filters and not raw_chunks:
        fallback_used = True
        raw_chunks = retriever.retrieve(
            query=query,
            company_id=state.get("company_id"),
            top_k=settings.RAG_RETRIEVE_K,
            filters=None,
            score_threshold=settings.RAG_MIN_SCORE,
        )
        attempt2_count = len(raw_chunks or [])
    scores = [float(getattr(c, "score", 0.0)) for c in (raw_chunks or [])]
    rerank_decision, _rerank_debug = should_rerank(
        query=standalone,
        retrieved_count=len(raw_chunks or []),
        scores=scores if scores else None,
    )

    trace_update = add_event(
        state,
        "retrieve",
        {
            "query_chars": len(query or ""),
            "top_k": settings.RAG_RETRIEVE_K,
            "filters": filters,
            "attempt1_count": attempt1_count,
            "attempt2_count": attempt2_count,
            "fallback_used": fallback_used,
            "score_threshold": settings.RAG_MIN_SCORE,
        },
        summarize_chunks(raw_chunks),
        duration_ms=now_ms() - start,
    )
    return {
        "query": query,
        "raw_chunks": raw_chunks,
        "rerank_should": rerank_decision,
        **trace_update,
    }


def _route_rerank(state: ChatState) -> str:
    if settings.RERANK_ENABLED and state.get("rerank_should") and (state.get("raw_chunks") or []):
        return "rerank"
    return "skip_rerank"


def should_rerank(
    query: str,
    retrieved_count: int,
    scores: List[float] | None,
) -> Tuple[bool, Dict[str, Any]]:
                                                                                   
    delta_top1_top2 = None
    if scores and len(scores) >= 2:
        try:
            delta_top1_top2 = float(scores[0]) - float(scores[1])
        except (TypeError, ValueError):
            delta_top1_top2 = None

    if retrieved_count >= 6:
        return True, {
            "reason": "count",
            "retrieved_count": retrieved_count,
            "delta_top1_top2": delta_top1_top2,
        }

    if delta_top1_top2 is not None and delta_top1_top2 < 0.03:
        return True, {
            "reason": "close_scores",
            "retrieved_count": retrieved_count,
            "delta_top1_top2": delta_top1_top2,
        }

    if is_policy_like_question(query):
        return True, {
            "reason": "policy_like",
            "retrieved_count": retrieved_count,
            "delta_top1_top2": delta_top1_top2,
        }

    return False, {
        "reason": "none",
        "retrieved_count": retrieved_count,
        "delta_top1_top2": delta_top1_top2,
    }


def rerank(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    raw_chunks = state.get("raw_chunks") or []
    reranker = CrossEncoderReranker()
    reranked = reranker.rerank(query=state.get("query") or "", chunks=raw_chunks, top_k=settings.RAG_TOP_K)

    trace_update = add_event(
        state,
        "rerank",
        {"raw_count": len(raw_chunks), "top_k": settings.RAG_TOP_K},
        summarize_chunks(reranked),
        duration_ms=now_ms() - start,
    )
    return {"chunks": reranked, **trace_update}


def skip_rerank(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    raw_chunks = state.get("raw_chunks") or []
    trimmed = raw_chunks[: settings.RAG_TOP_K]
    trace_update = add_event(
        state,
        "rerank",
        {"raw_count": len(raw_chunks)},
        summarize_chunks(trimmed),
        skipped=True,
        duration_ms=now_ms() - start,
    )
    return {"chunks": trimmed, **trace_update}


def _route_no_docs(state: ChatState) -> str:
    return "fallback_no_docs" if not (state.get("chunks") or []) else "build_context"


def fallback_no_docs(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    trace_update = add_event(
        state,
        "fallback_no_docs",
        {"retrieved_count": len(state.get("chunks") or [])},
        {"answer_type": "no_docs"},
        duration_ms=now_ms() - start,
    )
    return {
        "answer": "I don't have enough internal information to answer that based on our knowledge base.",
        "sources": [],
        "confidence": 0.0,
        **trace_update,
    }


def build_context(state: ChatState) -> Dict[str, Any]:
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


def llm_answer(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    chunks = state.get("chunks") or []
    if not chunks:
        trace_update = add_event(
            state,
            "llm_answer",
            {"retrieved_count": 0},
            {"answer_chars": len(state.get("answer") or "")},
            skipped=True,
            duration_ms=now_ms() - start,
        )
        return {**trace_update}

    llm = get_llm()
    sub_questions = state.get("sub_questions") or []
    if sub_questions:
        questions_block = "\n".join([f"{idx + 1}) {q}" for idx, q in enumerate(sub_questions)])
        question_section = (
            "USER QUESTIONS (answer each in order with numbered sections and include citations "
            "for each section):\n"
            f"{questions_block}"
        )
    else:
        question_section = (
            "USER QUESTION (include citations when using context):\n"
            f"{state.get('user_message', '')}"
        )
    prompt = [
        SystemMessage(content=CHAT_SYSTEM),
        HumanMessage(
            content=(
                f"Conversation summary:\n{state.get('summary', '')}\n\n"
                f"CONTEXT:\n{state.get('context_text', '')}\n\n"
                f"{question_section}"
            )
        ),
    ]
    answer = llm.invoke(prompt).content.strip()
    sources = citations_from_chunks(chunks)
    confidence = float(min(0.95, max(0.2, sources[0]["score"]))) if sources else 0.0

    trace_update = add_event(
        state,
        "llm_answer",
        {"context_chars": len(state.get("context_text", ""))},
        summarize_answer(answer),
        duration_ms=now_ms() - start,
    )
    return {"answer": answer, "sources": sources, "confidence": confidence, **trace_update}


def validate_citations(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    chunks = state.get("chunks") or []
    if not chunks:
        trace_update = add_event(
            state,
            "validate_citations",
            {},
            {"skipped_reason": "no_chunks"},
            skipped=True,
            duration_ms=now_ms() - start,
        )
        return {**trace_update}

    answer = state.get("answer") or ""
    ok = enforce_citations_if_needed(
        user_message=state.get("user_message") or "",
        answer=answer,
        retrieved=chunks,
    )

    output = {
        "ok": bool(ok),
        "policy_like": is_policy_like_question(state.get("user_message") or ""),
    }

    if not ok:
        output["action"] = "refuse_missing_citations"
        trace_update = add_event(
            state,
            "validate_citations",
            {"citations_count": summarize_answer(answer)["citations_count"]},
            output,
            duration_ms=now_ms() - start,
        )
        return {
            "answer": (
                "I don't have enough internal information to answer that "
                "with proper references from our knowledge base."
            ),
            "sources": [],
            "confidence": 0.0,
            **trace_update,
        }

    trace_update = add_event(
        state,
        "validate_citations",
        {"citations_count": summarize_answer(answer)["citations_count"]},
        output,
        duration_ms=now_ms() - start,
    )
    return {**trace_update}


def persist_assistant_message(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    conv = state.get("conversation")
    if conv is None:
        return {}

    msg = Message.objects.create(
        conversation=conv,
        role=Message.ROLE_ASSISTANT,
        content=state.get("answer") or "",
    )

    trace_update = add_event(
        state,
        "persist_assistant_message",
        {"answer_chars": len(state.get("answer") or "")},
        {"message_id": str(msg.id)},
        duration_ms=now_ms() - start,
    )
    return {**trace_update}


def _route_update_summary(state: ChatState) -> str:
    conv = state.get("conversation")
    if conv and _should_update_summary(conv):
        return "update_summary"
    return "classify_response"


def update_summary(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    conv = state.get("conversation")
    if not conv:
        trace_update = add_event(
            state,
            "update_summary",
            {},
            {"updated": False},
            skipped=True,
            duration_ms=now_ms() - start,
        )
        return {**trace_update}

    _update_summary(conv)
    trace_update = add_event(
        state,
        "update_summary",
        {},
        {"updated": True},
        duration_ms=now_ms() - start,
    )
    return {"summary": conv.summary or "", **trace_update}


def classify_response(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    classification = classify_chat_response(
        user_message=state.get("user_message") or "",
        answer=state.get("answer") or "",
        retrieved=state.get("chunks") or [],
    )

    trace_update = add_event(
        state,
        "classify_response",
        {"answer_chars": len(state.get("answer") or "")},
        {
            "classification": classification.classification,
            "refusal_code": classification.refusal_code,
            "needs_human": classification.needs_human,
        },
        duration_ms=now_ms() - start,
    )
    return {
        "classification": classification.classification,
        "refusal_code": classification.refusal_code,
        "needs_human": classification.needs_human,
        **trace_update,
    }


def finalize(state: ChatState) -> Dict[str, Any]:
    start = now_ms()
    payload = {
        "mode": "chat",
        "conversation_id": state.get("conversation_id"),
        "answer": state.get("answer") or "",
        "confidence": float(state.get("confidence") or 0.0),
        "sources": state.get("sources") or [],
        "refusal": None,
        "classification": state.get("classification"),
        "refusal_code": state.get("refusal_code"),
        "needs_human": state.get("needs_human"),
    }

    trace_update = add_event(
        state,
        "final",
        {},
        {
            "answer_chars": len(payload.get("answer") or ""),
            "sources_count": len(payload.get("sources") or []),
        },
        duration_ms=now_ms() - start,
    )
    return {"final_payload": payload, **trace_update}


def build_chat_graph():
    global _CHAT_GRAPH
    if _CHAT_GRAPH is not None:
        return _CHAT_GRAPH

    graph = StateGraph(ChatState)

    graph.add_node("persist_user_message", persist_user_message)
    graph.add_node("smalltalk_router", smalltalk_router)
    graph.add_node("rewrite", rewrite)
    graph.add_node("skip_rewrite", skip_rewrite)
    graph.add_node("multi_question_router", multi_question_router)
    graph.add_node("retrieve", retrieve)
    graph.add_node("rerank", rerank)
    graph.add_node("skip_rerank", skip_rerank)
    graph.add_node("fallback_no_docs", fallback_no_docs)
    graph.add_node("build_context", build_context)
    graph.add_node("llm_answer", llm_answer)
    graph.add_node("validate_citations", validate_citations)
    graph.add_node("persist_assistant_message", persist_assistant_message)
    graph.add_node("update_summary", update_summary)
    graph.add_node("classify_response", classify_response)
    graph.add_node("finalize", finalize)

    graph.set_entry_point("persist_user_message")

    graph.add_edge("persist_user_message", "smalltalk_router")
    graph.add_conditional_edges(
        "smalltalk_router",
        _route_after_smalltalk,
        {"smalltalk_done": "validate_citations", "rewrite": "rewrite", "skip_rewrite": "skip_rewrite"},
    )
    graph.add_edge("rewrite", "multi_question_router")
    graph.add_edge("skip_rewrite", "multi_question_router")
    graph.add_edge("multi_question_router", "retrieve")

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

    graph.add_edge("fallback_no_docs", "validate_citations")
    graph.add_edge("build_context", "llm_answer")
    graph.add_edge("llm_answer", "validate_citations")
    graph.add_edge("validate_citations", "persist_assistant_message")

    graph.add_conditional_edges(
        "persist_assistant_message",
        _route_update_summary,
        {"update_summary": "update_summary", "classify_response": "classify_response"},
    )
    graph.add_edge("update_summary", "classify_response")
    graph.add_edge("classify_response", "finalize")
    graph.add_edge("finalize", END)

    _CHAT_GRAPH = graph.compile()
    return _CHAT_GRAPH
