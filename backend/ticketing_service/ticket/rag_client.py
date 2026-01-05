import logging
import os
import uuid

from files.rag_client import send_rag_task

logger = logging.getLogger(__name__)


def _get_broker_url() -> str:
    return os.getenv("RAG_BROKER_URL") or os.getenv("CELERY_BROKER_URL") or ""


def _get_queue_name() -> str:
    return os.getenv("RAG_TASK_QUEUE") or "rag_events"


def build_ticket_payload(ticket, assigned_team_id=None) -> dict:
    created_at = ticket.created_at.isoformat() if ticket.created_at else None
    payload = {
        "event": "ticket.created",
        "event_id": str(uuid.uuid4()),
        "ticket_id": int(ticket.id),
        "company_id": int(ticket.company_id) if ticket.company_id is not None else None,
        "title": ticket.title,
        "description": ticket.description,
        "category": ticket.category,
        "priority": ticket.priority,
        "created_at": created_at,
        "need_admin": bool(getattr(ticket, "need_admin", False)),
        "bert_category": getattr(ticket, "bert_category", None),
        "bert_confidence": getattr(ticket, "bert_confidence", None),
        "similarity_score": getattr(ticket, "similarity_score", None),
        "assigned_team_id": assigned_team_id,
    }
    return payload


def publish_ticket_created(payload: dict) -> None:
    logger.info(
        "Publishing ticket.created event_id=%s ticket_id=%s broker=%s queue=%s",
        payload.get("event_id"),
        payload.get("ticket_id"),
        _get_broker_url() or "missing",
        _get_queue_name(),
    )
    send_rag_task("rag.process_ticket_created", payload)


__all__ = ["build_ticket_payload", "publish_ticket_created"]
