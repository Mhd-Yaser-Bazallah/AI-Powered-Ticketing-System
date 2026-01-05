# Ticketing Microservices Backend

Table of Contents
- [Services](#services)
- [Architecture Overview](#architecture-overview)
- [Communication Styles](#communication-styles)
- [System Flow](#system-flow)
- [Ports & URLs](#ports--urls)
- [How to Run Everything](#how-to-run-everything)
- [Troubleshooting](#troubleshooting)

## Services
- Ticketing service (code directory: `ticketing_service/`)  
  README: `ticketing_service/README.md`
- RAG service (code directory: `rag_ms/`)  
  README: `rag_ms/README.md`
- Ticket utilities service (code directory: `ticket_utils_service/`)  
  README: `ticket_utils_service/README.md`

## Architecture Overview
### Services and responsibilities
- Ticketing service: authentication, users, companies, teams, tickets, workflows, comments, notifications, reporting, analysis, and file uploads. Publishes ticket/file events to the RAG queue and calls the analyze service for ticket enrichment.
- RAG service: retrieval-augmented chat, solution generation, retrieval API, ingestion of uploaded files into Qdrant, and processing of ticket/file events via Celery tasks.
- Ticket utilities service: ticket analysis (category, priority, team assignment) and asynchronous retraining workflow via Celery.

### Communication map
- HTTP
  - Client -> Ticketing service endpoints (auth, tickets, files, etc.).
  - Ticketing service -> Ticket utilities service `POST /api/analyze` for ticket enrichment.
  - Client -> RAG service endpoints (chat, solution, retrieve, health).
- Event-driven (Celery + Redis broker)
  - Ticketing service publishes Celery tasks to `rag_events` queue for file upload/delete and ticket.created.
  - RAG service consumes those tasks and updates Qdrant or ticket solution data.

## Communication Styles
### 1) Request/Response (HTTP)
- Ticketing service -> Ticket utilities service:
  - `POST http://127.0.0.1:8002/api/analyze` with ticket description and company ID.
- Client -> RAG service:
  - `POST http://127.0.0.1:8001/rag/chat`, `POST http://127.0.0.1:8001/rag/solution`, `POST http://127.0.0.1:8001/rag/retrieve`, `GET http://127.0.0.1:8001/rag/health`.
- Client -> Ticketing service:
  - Various endpoints under `http://127.0.0.1:8000/` (see `ticketing_service/README.md`).

### 2) Event-driven messaging (Celery + Redis broker)
- Broker: Redis (Celery broker URL via `RAG_BROKER_URL` or `CELERY_BROKER_URL`).
- Queue: `rag_events` (from `RAG_TASK_QUEUE`, default `rag_events`).

Producers and consumers
- Ticketing service (producer) sends Celery tasks:
  - `rag.process_file_uploaded`
  - `rag.process_file_deleted`
  - `rag.process_ticket_created`
- RAG service (consumer) handles tasks:
  - `rag.process_file_uploaded`: ingests file into Qdrant.
  - `rag.process_file_deleted`: deletes file chunks from Qdrant.
  - `rag.process_ticket_created`: generates solution steps and updates `Ticket` table.

Event payloads (derived from code)
- `file_uploaded`
  - `event`: "file_uploaded"
  - `event_id`: UUID
  - `file_id`: UUID
  - `company_id`: integer
  - `file_path`: string (absolute path) or empty if using `file_relative_path`
  - `file_relative_path`: string (relative path)
  - `original_name`: string
  - `kind`: "pdf" | "word" | "excel"
  - `size_bytes`: integer
  - `content_type`: string
  - `uploaded_at`: ISO timestamp or null
- `file_deleted`
  - `event`: "file_deleted"
  - `event_id`: UUID
  - `file_id`: UUID
  - `company_id`: integer
- `ticket.created`
  - `event`: "ticket.created"
  - `event_id`: UUID
  - `ticket_id`: integer
  - `company_id`: integer or null
  - `title`: string
  - `description`: string
  - `category`: string
  - `priority`: string
  - `created_at`: ISO timestamp or null
  - `need_admin`: boolean
  - `bert_category`: string or null
  - `bert_confidence`: float or null
  - `similarity_score`: float or null
  - `assigned_team_id`: integer or null

## System Flow
- Client creates a ticket via Ticketing service.
- Ticketing service calls Ticket utilities service to classify category/priority/team assignment.
- Ticketing service stores the ticket, logs the action, and publishes a `ticket.created` event to the RAG queue.
- RAG service consumes `ticket.created`, generates solution steps, and updates the shared `Ticket` table.
- Client uploads files via Ticketing service; file events are published to the RAG queue.
- RAG service ingests or deletes file chunks in Qdrant based on file events.

## Ports & URLs
- Ticketing service: http://127.0.0.1:8000  
- RAG service: http://127.0.0.1:8001  
- Ticket utilities service: http://127.0.0.1:8002  

## How to Run Everything
Docker Compose: Not found in repository (needs confirmation).

### Prerequisites (from repo requirements)
- Python 3.10+ (ticketing service), Python 3.x (rag service), Python 3.12 (ticket utils service).
- MySQL 8+ for ticketing and ticket utils.
- Redis 6+ for Celery brokers.
- Qdrant (RAG vector DB).
- Ollama (RAG LLM runtime).
- spaCy model `en_core_web_sm` (ticket utils).

### Environment setup
- Ticketing service: copy `ticketing_service/.env.example` to `ticketing_service/.env`.
- RAG service: copy `rag_ms/.env.example` to `rag_ms/.env`.
- Ticket utilities service: copy `ticket_utils_service/.env.example` to `ticket_utils_service/.env`.

### Start services (multi-terminal)
1) Start infrastructure
   - MySQL (port 3306)
   - Redis (port 6379)
   - Qdrant (port 6333)
   - Ollama (port 11434)

2) Ticket utilities service (analysis)
```bash
cd ticket_utils_service
python manage.py migrate
python manage.py runserver 127.0.0.1:8002
```
Optional Celery worker (for retraining):
```bash
celery -A ticket_utils_service worker -l info
```

3) RAG service
```bash
cd rag_ms
python manage.py migrate
python manage.py runserver 127.0.0.1:8001
```
Celery worker (required for file/ticket event processing):
```bash
celery -A rag_ms worker -l info
```

4) Ticketing service
```bash
cd ticketing_service
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

## Troubleshooting
- RAG events not processed: ensure `RAG_BROKER_URL` or `CELERY_BROKER_URL` is set and Redis is running; ticketing logs `RAG broker not configured; skipping task=...` when missing.
- File ingestion fails in RAG: `RAG_FILES_BASE_PATH` must be set if `file_path` is not provided; RAG raises `file_path not provided and RAG_FILES_BASE_PATH not set`.
- `ticket.created` processing fails in RAG: RAG uses an unmanaged `Ticket` model (`db_table = "Ticket"`); ensure the RAG service is pointed to the same MySQL database that contains the Ticket table.
- RAG query errors: verify Qdrant and Ollama are reachable at configured URLs.
- Analyze service unreachable: ticketing service falls back to defaults (`category=back`, `priority=low`) when `POST /api/analyze` fails.
- Ticket utilities training fails: retraining runs `Splitting.py` and `train_bert.py` via subprocess; errors are logged and saved on the `AnalyzeCounter` record.
