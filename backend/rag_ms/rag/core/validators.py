from __future__ import annotations
import re
from typing import List
from rag.core.types import RetrievedChunk

CITATION_PATTERN = re.compile(r"\[(?P<type>[^:\]]+):(?P<id>[^#\]]+)#(?P<chunk>[^\]]+)\]")

def extract_citations(text: str) -> List[dict]:
    cites = []
    for m in CITATION_PATTERN.finditer(text or ""):
        cites.append(
            {
                "source_type": m.group("type").strip(),
                "source_id": m.group("id").strip(),
                "chunk_id": m.group("chunk").strip(),
            }
        )
    return cites

def is_policy_like_question(user_message: str) -> bool:
    """
    Rule-based intent detection (fast & sufficient initially).
    We treat these as requiring citations when we have context.
    """
    s = (user_message or "").lower()
    keywords = [
        "policy", "refund", "eligible", "procedure", "process", "sla", "guideline",
        "according to", "what is the rule", "is it allowed", "compliance"
    ]
    return any(k in s for k in keywords)

def enforce_citations_if_needed(
    user_message: str,
    answer: str,
    retrieved: List[RetrievedChunk],
) -> bool:
    """
    If retrieved context exists AND the question is policy-like,
    the answer must contain at least one valid citation.
    """
    if not retrieved:
        return True                                             
    if not is_policy_like_question(user_message):
        return True                                             
    return len(extract_citations(answer)) > 0

def validate_solution_steps(steps: List[str]) -> bool:
    """
    Every step must contain at least one citation.
    """
    if not steps:
        return False
    for s in steps:
        if len(extract_citations(s)) == 0:
            return False
    return True
