from __future__ import annotations

from rag.core.graphs.solution_graph import build_solution_graph
from rag.api.serializers import SolutionRequestSerializer, SolutionResponseSerializer


def generate_solution_from_request(data: dict) -> dict:
    req = SolutionRequestSerializer(data=data)
    req.is_valid(raise_exception=True)
    validated = req.validated_data

    ctx = validated.get("context") or {}
    graph = build_solution_graph()
    state = graph.invoke(
        {
            "ticket_description": validated["ticket_description"],
            "ticket_category": ctx.get("category"),
            "ticket_priority": ctx.get("priority"),
            "company_id": validated.get("company_id"),
            "trace_events": [],
            "event_id_counter": 0,
        }
    )
    payload = state.get("final_payload") or {
        "mode": "solution",
        "steps": [],
        "confidence": 0.0,
        "sources": [],
        "needs_human": True,
    }

    res = SolutionResponseSerializer(data=payload)
    res.is_valid(raise_exception=True)
    return res.data
