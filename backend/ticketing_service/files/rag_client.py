import logging
import os
import uuid

from celery import Celery

logger = logging.getLogger(__name__)


def _get_broker_url() -> str:
    return os.getenv("RAG_BROKER_URL") or os.getenv("CELERY_BROKER_URL") or ""


def _get_queue_name() -> str:
    return os.getenv("RAG_TASK_QUEUE") or "rag_events"


def _get_celery_app():
    broker_url = _get_broker_url()
    if not broker_url:
        return None
    return Celery("ticketing_rag_events", broker=broker_url)


def build_file_payload(record) -> dict:
    file_path = getattr(record.file, "path", "") if getattr(record, "file", None) else ""
    file_name = getattr(record.file, "name", "") if getattr(record, "file", None) else ""
    uploaded_at = record.uploaded_at.isoformat() if record.uploaded_at else None
    return {
        "event": "file_uploaded",
        "event_id": str(uuid.uuid4()),
        "file_id": str(record.id),
        "company_id": record.company_id,
        "file_path": file_path,
        "file_relative_path": file_name,
        "original_name": record.original_name,
        "kind": record.kind,
        "size_bytes": record.size_bytes,
        "content_type": record.content_type,
        "uploaded_at": uploaded_at,
    }


def send_rag_task(task_name: str, payload: dict) -> None:
    app = _get_celery_app()
    if not app:
        logger.warning("RAG broker not configured; skipping task=%s", task_name)
        return
    try:
        app.send_task(task_name, args=[payload], queue=_get_queue_name())
    except Exception:
        logger.exception("Failed to send RAG task=%s", task_name)
