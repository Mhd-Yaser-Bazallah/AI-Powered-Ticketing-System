from __future__ import annotations

from typing import Optional
from django.conf import settings
from langchain_core.messages import SystemMessage, HumanMessage
from rag.core.reranker import CrossEncoderReranker

from rag.core.retriever import QdrantRetriever
from rag.core.llm import get_llm
from rag.core.prompts import SOLUTION_SYSTEM
from rag.core.formatting import format_context, citations_from_chunks
from rag.core.validators import validate_solution_steps

def generate_solution_steps(
    *,
    ticket_description: str,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    company_id: Optional[int] = None,
):
    llm = get_llm()
    retriever = QdrantRetriever()

    query = f"TICKET: {ticket_description}\nCATEGORY: {category or ''}\nPRIORITY: {priority or ''}\nGenerate troubleshooting steps."

    raw_chunks = retriever.retrieve(
        query=query,
        company_id=company_id,
        top_k=settings.RAG_RETRIEVE_K,
        filters={"category": category} if category else None,
        score_threshold=settings.RAG_MIN_SCORE,
    )

    chunks = raw_chunks
    if settings.RERANK_ENABLED and raw_chunks:
        chunks = CrossEncoderReranker().rerank(query=query, chunks=raw_chunks, top_k=settings.RAG_TOP_K)

    if not chunks:
        return {
            "steps": [],
            "sources": [],
            "confidence": 0.0,
            "needs_human": True,
        }

    context_text = format_context(chunks)

    prompt = [
        SystemMessage(content=SOLUTION_SYSTEM),
        HumanMessage(content=f"CONTEXT:\n{context_text}\n\nTICKET DESCRIPTION:\n{ticket_description}\n\nReturn steps now."),
    ]

    raw = llm.invoke(prompt).content.strip()

    if raw.strip() == "NEEDS_HUMAN":
        return {
            "steps": [],
            "sources": citations_from_chunks(chunks),
            "confidence": 0.0,
            "needs_human": True,
        }

                                    
    steps = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
                                     
        if line[0].isdigit():
            steps.append(line)
        else:
                                     
            steps.append(line)

                                          
    if not validate_solution_steps(steps):
        return {
            "steps": [],
            "sources": citations_from_chunks(chunks),
            "confidence": 0.0,
            "needs_human": True,
        }
    confidence = float(min(0.95, max(0.2, citations_from_chunks(chunks)[0]["score"])))
    return {
        "steps": steps,
        "sources": citations_from_chunks(chunks),
        "confidence": confidence,
        "needs_human": False,
    }
