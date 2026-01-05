import logging

from celery import shared_task

from rag.api.solution_service import generate_solution_from_request
from rag.ingestion.processor import delete_file_chunks, ingest_file
from rag.models import ProcessedEvent, Ticket

logger = logging.getLogger(__name__)


@shared_task(name="rag.process_file_uploaded")
def process_file_uploaded(payload: dict) -> dict:
    try:
        chunk_count = ingest_file(payload)
        return {"ok": True, "chunks": chunk_count}
    except Exception as exc:
        logger.exception("Failed to ingest file event")
        return {"ok": False, "error": str(exc)}


@shared_task(name="rag.process_file_deleted")
def process_file_deleted(payload: dict) -> dict:
    logger.info("process_file_deleted: started")
    try:
        file_id = str(payload.get("file_id") or "")
        company_id = payload.get("company_id")
        logger.info("process_file_deleted: file_id=%s", file_id)
        if company_id is None:
            raise ValueError("company_id missing in payload")
        delete_file_chunks(file_id, company_id)
        logger.info("process_file_deleted: deleted chunks")
        return {"ok": True, "file_id": file_id}
    except Exception as exc:
        logger.exception("Failed to delete file chunks")
        return {"ok": False, "error": str(exc)}


@shared_task(name="rag.process_ticket_created")
def process_ticket_created(payload: dict) -> dict:
    logger.info("process_ticket_created: started")
    event_id = str(payload.get("event_id") or "")
    if not event_id:
        logger.error("ticket.created event missing event_id")
        return {"ok": False, "error": "event_id missing"}

    event_type = str(payload.get("event") or "ticket.created")
    logger.info(
        "Received ticket.created event_id=%s ticket_id=%s",
        event_id,
        payload.get("ticket_id"),
    )
    try:
        processed, created = ProcessedEvent.objects.get_or_create(
            event_id=event_id,
            defaults={"event_type": event_type, "status": ProcessedEvent.STATUS_PROCESSING},
        )
        if not created:
            if processed.status == ProcessedEvent.STATUS_COMPLETED:
                return {"ok": True, "skipped": True}
            if processed.status == ProcessedEvent.STATUS_PROCESSING:
                return {"ok": True, "skipped": True}
            processed.status = ProcessedEvent.STATUS_PROCESSING
            processed.error_message = None
            processed.save(update_fields=["status", "error_message", "updated_at"])
    except Exception as exc:
        logger.exception("Failed to create processed event record")
        return {"ok": False, "error": str(exc)}
    logger.info("process_ticket_created: entering main flow")
    try:
        ticket_id = payload.get("ticket_id")
        description = payload.get("description") or ""
        category = payload.get("category")or ""
        priority = payload.get("priority")or ""
        logger.info("payload keys: %s", list(payload.keys()))
        logger.info("desc_len=%s category=%s priority=%s", len(description), category, priority)
        logger.info("description_preview=%r", description[:120])
        company_id = payload.get("company_id")
        solution = generate_solution_from_request(
            {
                "ticket_description": description,
                "context": {"category": category, "priority": priority},
                "company_id": company_id,
            }
        )
        logger.info("process_ticket_created: solution generated")
        logger.info(solution)
        steps = solution.get("steps") or []
        normalized_steps = [{"order": idx + 1, "text": step} for idx, step in enumerate(steps)]
        confidence = solution.get("confidence")
        logger.info("process_ticket_created: steps=%s confidence=%s", len(steps), confidence)
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            raise ValueError(f"Ticket not found: {ticket_id}")

        ticket.solution_steps = normalized_steps
        ticket.solution_confidence = confidence
        ticket.save(update_fields=["solution_steps", "solution_confidence"])

        processed.status = ProcessedEvent.STATUS_COMPLETED
        processed.error_message = None
        processed.save(update_fields=["status", "error_message", "updated_at"])
        logger.info("process_ticket_created: completed ticket_id=%s", ticket_id)
        return {"ok": True, "ticket_id": ticket_id}
    except Exception as exc:
        logger.exception("Failed to process ticket.created event")
        try:
            processed.status = ProcessedEvent.STATUS_FAILED
            processed.error_message = str(exc)
            processed.save(update_fields=["status", "error_message", "updated_at"])
        except Exception:
            logger.exception("Failed to update processed event status")
        return {"ok": False, "error": str(exc)}
