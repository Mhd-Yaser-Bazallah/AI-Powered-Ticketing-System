from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class RetrievedChunk:
    text: str
    score: float
    source_type: str
    source_id: str
    chunk_id: str
    metadata: Dict[str, Any]
