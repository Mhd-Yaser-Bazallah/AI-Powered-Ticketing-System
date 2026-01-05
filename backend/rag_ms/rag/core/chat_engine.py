from __future__ import annotations

from typing import Optional, List
from django.conf import settings
from langchain_core.messages import SystemMessage, HumanMessage

from rag.models import Conversation, Message
from rag.core.retriever import QdrantRetriever
from rag.core.llm import get_llm
from rag.core.prompts import CHAT_SYSTEM, SUMMARY_SYSTEM
from rag.core.formatting import format_context, citations_from_chunks
from rag.core.rewriter import rewrite_query
from rag.core.validators import enforce_citations_if_needed
from rag.core.classifier import classify_chat_response
from rag.core.reranker import CrossEncoderReranker

def _last_messages(conv: Conversation, n: int) -> List[Message]:
    return list(conv.messages.order_by("-created_at")[:n])[::-1]


def _should_update_summary(conv: Conversation) -> bool:
                                  
    user_count = conv.messages.filter(role=Message.ROLE_USER).count()
    return user_count > 0 and (user_count % settings.SUMMARY_EVERY_N == 0)


def _update_summary(conv: Conversation, llm) -> None:
    last_msgs = _last_messages(conv, settings.CHAT_LAST_N)
    transcript = "\n".join([f"{m.role}: {m.content}" for m in last_msgs])

    prompt = [
        SystemMessage(content=SUMMARY_SYSTEM),
        HumanMessage(content=f"Existing summary:\n{conv.summary or ''}\n\nRecent transcript:\n{transcript}\n\nUpdate the summary."),
    ]
    summary = llm.invoke(prompt).content.strip()
    conv.summary = summary
    conv.save(update_fields=["summary"])

def chat_answer(
    *,
    conversation_id: Optional[str],
    user_message: str,
    ticket_description: Optional[str] = None,
    ticket_category: Optional[str] = None,
    ticket_priority: Optional[str] = None,
    company_id: Optional[int] = None,
):
    llm = get_llm()
    retriever = QdrantRetriever()

                                   
    if conversation_id:
        conv = Conversation.objects.get(id=conversation_id)
    else:
        conv = Conversation.objects.create(
            ticket_description=ticket_description,
            ticket_category=ticket_category,
            ticket_priority=ticket_priority,
        )

                             
    Message.objects.create(
        conversation=conv,
        role=Message.ROLE_USER,
        content=user_message,
    )

                                                   
    standalone = rewrite_query(
        user_message=user_message,
        summary=conv.summary or "",
        ticket_description=conv.ticket_description,
        ticket_category=conv.ticket_category,
        ticket_priority=conv.ticket_priority,
    )

                              
    query = standalone
    if conv.ticket_description:
        query = f"TICKET: {conv.ticket_description}\n\nQUERY: {standalone}"

                                 
    raw_chunks = retriever.retrieve(
        query=query,
        company_id=company_id,
        top_k=settings.RAG_RETRIEVE_K,
        filters={"category": conv.ticket_category} if conv.ticket_category else None,
        score_threshold=settings.RAG_MIN_SCORE,
    )

    chunks = raw_chunks
    if settings.RERANK_ENABLED and raw_chunks:
        chunks = CrossEncoderReranker().rerank(query=query, chunks=raw_chunks, top_k=settings.RAG_TOP_K)


    summary = conv.summary or ""
    context_text = format_context(chunks)

                                           
    if not chunks:
        answer = "I don’t have enough internal information to answer that based on our knowledge base."
        sources = []
        confidence = 0.0
    else:
        prompt = [
            SystemMessage(content=CHAT_SYSTEM),
            HumanMessage(
                content=(
                    f"Conversation summary:\n{summary}\n\n"
                    f"CONTEXT:\n{context_text}\n\n"
                    f"USER QUESTION:\n{user_message}"
                )
            ),
        ]

        answer = llm.invoke(prompt).content.strip()

                                                       
        sources = citations_from_chunks(chunks)
        confidence = (
            float(min(0.95, max(0.2, sources[0]["score"])))
            if sources
            else 0.0
        )

                                                        
        ok = enforce_citations_if_needed(
            user_message=user_message,
            answer=answer,
            retrieved=chunks,
        )
        if not ok:
            answer = (
                "I don’t have enough internal information to answer that "
                "with proper references from our knowledge base."
            )
            sources = []
            confidence = 0.0

                                  
    Message.objects.create(
        conversation=conv,
        role=Message.ROLE_ASSISTANT,
        content=answer,
    )

                                         
    if _should_update_summary(conv):
        _update_summary(conv, llm)

                               
    classification = classify_chat_response(
        user_message=user_message,
        answer=answer,
        retrieved=chunks,
    )

                                 
    return {
        "conversation_id": conv.id,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "refusal": None,
        "classification": classification.classification,
        "refusal_code": classification.refusal_code,
        "needs_human": classification.needs_human,
    }
 
