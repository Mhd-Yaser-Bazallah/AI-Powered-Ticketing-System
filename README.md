# AI-Powered Ticketing System

## Project Overview
This repository contains a multi-service ticketing platform with a core ticketing API, an AI-powered RAG service, and a ticket utilities service for analysis and retraining workflows.

## Repository Layout
- `backend/`
  - `ticketing_service/` (core ticketing API)
  - `rag_ms/` (RAG service)
  - `ticket_utils_service/` (ticket analysis + retraining)
  - `scripts/` (model download helpers)
- `frontend/` (client UI)

## Ports & URLs
- Ticketing service: http://127.0.0.1:8000
- RAG service: http://127.0.0.1:8001
- Ticket utilities service: http://127.0.0.1:8002

## Communication Overview
### HTTP request/response
- Client -> Ticketing service endpoints (auth, tickets, files, etc.).
- Ticketing service -> Ticket utilities service `POST /api/analyze` for ticket enrichment.
- Client -> RAG service endpoints (chat, solution, retrieve, health).

### Event-driven messaging
- Ticketing service publishes Celery tasks to Redis queue `rag_events`:
  - `rag.process_file_uploaded`
  - `rag.process_file_deleted`
  - `rag.process_ticket_created`
- RAG service consumes those tasks to ingest files into Qdrant and to generate ticket solutions.

## Large Files / Pretrained Models
Pretrained models and large ML artifacts are intentionally excluded from git via `.gitignore` to keep the repository lightweight.

Expected local model locations:
- Ticket utilities models: `backend/ticket_utils_service/ticket/utils/ml/models/`
- Team classifier models: `backend/ticket_utils_service/ticket/utils/TeamClassifier/models/`
- RAG embeddings/reranker cache: HuggingFace cache (e.g., `~/.cache/huggingface/hub` or `C:\Users\<USER>\.cache\huggingface\hub`)
- Optional local RAG assets: `backend/rag_ms/models/` (set `EMBEDDINGS_MODEL` / `RERANK_MODEL` to local paths)
- Ollama models are stored by Ollama (see `OLLAMA_MODEL` in `backend/rag_ms/.env.example`).

Download helpers (generic):
- `backend/scripts/download_models.sh`
- `backend/scripts/download_models.ps1`

Usage (set these env vars before running the script):
- `MODEL_URL` (direct URL to the model file)
- `MODEL_DIR` (target folder to store the model)

## How to Run the Whole System
1) Start infrastructure: MySQL, Redis, Qdrant, and Ollama.
2) Copy service env files from their `.env.example` templates and install dependencies per service README.
3) Start the services in separate terminals (ticket utilities, RAG, ticketing) and then start the frontend.

For details and per-service commands, see:
- `backend/ticketing_service/README.md`
- `backend/rag_ms/README.md`
- `backend/ticket_utils_service/README.md`
