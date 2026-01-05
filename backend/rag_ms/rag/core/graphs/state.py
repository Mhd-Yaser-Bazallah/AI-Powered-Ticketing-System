from typing import Any, Dict, List, Optional, TypedDict

from rag.core.types import RetrievedChunk


class TraceEvent(TypedDict):
    event_id: int
    stage: str
    ts_ms: int
    duration_ms: int
    input: Dict[str, Any]
    output: Dict[str, Any]
    skipped: bool
    error: bool


class ChatState(TypedDict, total=False):
    event_id_counter: int
    trace_events: List[TraceEvent]

    conversation_id: Optional[str]
    user_message: str
    ticket_description: Optional[str]
    ticket_category: Optional[str]
    ticket_priority: Optional[str]
    company_id: Optional[int]

    conversation: Any
    summary: str

    standalone_query: str
    query: str
    raw_chunks: List[RetrievedChunk]
    rerank_should: bool
    chunks: List[RetrievedChunk]
    context_text: str

    smalltalk_match: bool
    sub_questions: List[str]

    answer: str
    sources: List[Dict[str, Any]]
    confidence: float

    classification: str
    refusal_code: Optional[str]
    needs_human: bool

    final_payload: Dict[str, Any]


class SolutionState(TypedDict, total=False):
    event_id_counter: int
    trace_events: List[TraceEvent]

    ticket_description: str
    ticket_category: Optional[str]
    ticket_priority: Optional[str]
    company_id: Optional[int]

    query: str
    raw_chunks: List[RetrievedChunk]
    chunks: List[RetrievedChunk]
    context_text: str

    raw_steps: str
    steps: List[str]
    needs_human: bool

    sources: List[Dict[str, Any]]
    confidence: float

    final_payload: Dict[str, Any]
