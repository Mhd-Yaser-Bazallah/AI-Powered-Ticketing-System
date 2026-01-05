# RAG Service

## Overview
Retrieval-augmented generation service that supports chat, solution generation, retrieval, and event-driven ingestion of uploaded files into Qdrant. It also processes `ticket.created` events to populate solution steps on tickets.

## Tech Stack
- Python, Django, Django REST Framework
- Celery + Redis (async task processing)
- Qdrant (vector store)
- Ollama (LLM runtime)
- SentenceTransformers (embeddings), optional reranker

## Base URL
http://127.0.0.1:8001

## Run This Service Only
```bash
cd backend/rag_ms
copy .env.example .env
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8001
```

Start Celery worker for ingestion/event tasks:
```bash
celery -A rag_ms worker -l info
```

Required services:
- Qdrant
- Ollama
- Redis

## Configuration
Environment variables from `rag_ms/.env.example` and settings:

| Variable | Purpose | Default |
| --- | --- | --- |
| `RAG_API_KEY` | Required API key for protected endpoints | empty string |
| `QDRANT_URL` | Qdrant base URL | `http://127.0.0.1:6333` |
| `QDRANT_API_KEY` | Qdrant API key | empty string |
| `QDRANT_COLLECTION` | Qdrant collection name | `kb_main` |
| `EMBEDDINGS_PROVIDER` | Embeddings provider | `local` |
| `EMBEDDINGS_MODEL` | Embeddings model name | `all-MiniLM-L6-v2` |
| `OLLAMA_BASE_URL` | Ollama base URL | `http://127.0.0.1:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.1:8b` |
| `RERANK_ENABLED` | Enable reranker | `true` |
| `RERANK_MODEL` | Reranker model | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| `RAG_RETRIEVE_K` | Retrieve candidates | `12` |
| `RAG_TOP_K` | Top results | `6` |
| `RAG_MIN_SCORE` | Minimum score threshold | `0.25` |
| `CHAT_LAST_N` | Chat history limit | `12` |
| `SUMMARY_EVERY_N` | Summary interval | `8` |
| `RAG_MIN_CHUNKS_BEFORE_FALLBACK` | Minimum chunks | `3` |
| `RAG_FILES_BASE_PATH` | Base path for ingested files | empty string |
| `RAG_BROKER_URL` | Celery broker URL | empty string |
| `CELERY_BROKER_URL` | Celery broker URL fallback | `redis://127.0.0.1:6379/0` |
| `RAG_TASK_QUEUE` | Celery queue name | `rag_events` |
| `DB_NAME` | MySQL database name (optional) | empty string |
| `DB_USER` | MySQL user | empty string |
| `DB_PASSWORD` | MySQL password | empty string |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |

## Models & Assets
Models are intentionally NOT tracked by git. They are cached or stored locally on each machine.

Expected local model paths:
- HuggingFace cache (SentenceTransformers and CrossEncoder): `~/.cache/huggingface/hub` or `C:\Users\<USER>\.cache\huggingface\hub`
- Optional local model storage: `backend/rag_ms/models/` (set `EMBEDDINGS_MODEL` / `RERANK_MODEL` to local paths)
- Ollama models are managed by Ollama (pull the configured `OLLAMA_MODEL`).

Download instructions (generic):
- Use `backend/scripts/download_models.sh` or `backend/scripts/download_models.ps1`.
- Set `MODEL_URL` and `MODEL_DIR` before running the script.

## API Reference
All routes are rooted at `http://127.0.0.1:8001/rag`.

### Health
- `GET /rag/health` (requires `X-RAG-API-KEY`)

Example:
```bash
curl http://127.0.0.1:8001/rag/health \
  -H "X-RAG-API-KEY: $RAG_API_KEY"
```

### Chat (SSE)
- `POST /rag/chat` (requires `X-RAG-API-KEY`, streams SSE)

Example:
```bash
curl -N http://127.0.0.1:8001/rag/chat \
  -H "X-RAG-API-KEY: $RAG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message":"How do we handle duplicate charges?","company_id":1,"ticket":{"description":"Duplicate charge issue","category":"billing","priority":"high"}}'
```

### Solution
- `POST /rag/solution`

Example:
```bash
curl -X POST http://127.0.0.1:8001/rag/solution \
  -H "Content-Type: application/json" \
  -d '{"ticket_description":"Customer charged twice","context":{"category":"billing","priority":"high"},"company_id":1}'
```

### Retrieve
- `POST /rag/retrieve` (requires `X-RAG-API-KEY`)

Example:
```bash
curl -X POST http://127.0.0.1:8001/rag/retrieve \
  -H "X-RAG-API-KEY: $RAG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"refund duplicate charge","company_id":1,"top_k":6}'
```

### Events (HTTP)
- `POST /rag/events` (requires `X-RAG-API-KEY`)

Example:
```bash
curl -X POST http://127.0.0.1:8001/rag/events \
  -H "X-RAG-API-KEY: $RAG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"event":"ticket.created","event_id":"uuid","ticket_id":123,"description":"Login failure","category":"access","priority":"high","company_id":1}'
```

### Dev Seed
- `POST /rag/dev/seed`

Example:
```bash
curl -X POST http://127.0.0.1:8001/rag/dev/seed \
  -H "Content-Type: application/json" \
  -d '{"wipe":true,"company_id":1}'
```

## Integration Points
- Consumes Celery tasks from Redis queue `rag_events`:
  - `rag.process_file_uploaded`, `rag.process_file_deleted`, `rag.process_ticket_created`.
- External dependencies:
  - Qdrant vector store (`QDRANT_URL`)
  - Ollama model server (`OLLAMA_BASE_URL`)

## Health Checks / Admin
- Health endpoint: `GET /rag/health` (API key required)
- Admin interface: `GET /admin/`

## Logging / Observability
- Uses Python logging.
- `/rag/chat` streams Server-Sent Events with `event: stage` and `event: final` payloads.
