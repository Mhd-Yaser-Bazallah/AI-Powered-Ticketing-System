from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from rag.core.types import RetrievedChunk
from rag.core.validators import extract_citations, is_policy_like_question


@dataclass
class ChatClassification:
    classification: str                                                      
    refusal_code: Optional[str]
    needs_human: bool


def classify_chat_response(
    user_message: str,
    answer: str,
    retrieved: List[RetrievedChunk],
    min_context_hits: int = 1,
) -> ChatClassification:
    a = (answer or "").strip().lower()
    cites = extract_citations(answer)
    policy_like = is_policy_like_question(user_message)

                                    
    if not retrieved or len(retrieved) < min_context_hits:
        return ChatClassification(
            classification="HARD_REFUSAL",
            refusal_code="NO_RETRIEVAL_CONTEXT",
            needs_human=True,
        )

                                                                             
    insufficient_markers = [
        "don't have enough internal information",
        "do not have enough internal information",
        "not enough information",
        "insufficient information",
        "cannot determine",
        "can't determine",
        "does not explicitly cover",
        "not explicitly cover",
        "cannot provide a definitive answer",
    ]
    if any(m in a for m in insufficient_markers):
                                                                             
                                                                            
        return ChatClassification(
            classification="SOFT_REFUSAL" if policy_like else "NEEDS_HUMAN",
            refusal_code="INSUFFICIENT_POLICY_COVERAGE" if policy_like else "INSUFFICIENT_CONTEXT",
            needs_human=True,
        )

                                                                              
    if policy_like and len(cites) == 0:
        return ChatClassification(
            classification="NEEDS_HUMAN",
            refusal_code="MISSING_CITATIONS",
            needs_human=True,
        )

                      
    return ChatClassification(
        classification="ANSWER",
        refusal_code=None,
        needs_human=False,
    )
