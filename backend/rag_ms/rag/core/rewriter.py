from __future__ import annotations
from langchain_core.messages import SystemMessage, HumanMessage

from rag.core.llm import get_llm

REWRITE_SYSTEM = """Rewrite the user's message into a standalone search query.
Rules:
- Preserve all constraints and entities (order ids, invoice, refund, etc.).
- If the question refers to prior context ("that", "it", "them"), resolve it using the provided conversation summary and ticket context.
- Output ONLY the rewritten query text. No quotes, no extra formatting.
"""

def rewrite_query(
    user_message: str,
    summary: str = "",
    ticket_description: str | None = None,
    ticket_category: str | None = None,
    ticket_priority: str | None = None,
) -> str:
    llm = get_llm()
    ticket_ctx = ""
    if ticket_description:
        ticket_ctx = f"TICKET: {ticket_description}\nCATEGORY: {ticket_category or ''}\nPRIORITY: {ticket_priority or ''}\n"

    prompt = [
        SystemMessage(content=REWRITE_SYSTEM),
        HumanMessage(content=f"Conversation summary:\n{summary}\n\n{ticket_ctx}\nUser message:\n{user_message}\n\nRewrite:"),
    ]
    out = llm.invoke(prompt).content.strip()
    return out or user_message
