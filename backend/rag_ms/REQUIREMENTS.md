# Operational Requirements

## Runtime Prerequisites
- Python 3.x
- Qdrant vector database
- Ollama LLM runtime
- Redis (required for Celery tasks)

## External Services
- Qdrant: set `QDRANT_URL` and ensure the collection can be created
- Ollama: set `OLLAMA_BASE_URL` and pull `OLLAMA_MODEL`
- Database: SQLite by default, MySQL when `DB_NAME` is set
- Redis: required if running Celery workers

## Ports
- rag_ms API: 8000
- Qdrant: 6333
- Ollama: 11434
- Redis: 6379

## Environment Variables
See the configuration table in `README.md`.

## Storage/Volumes
- SQLite uses `db.sqlite3` in the repo root by default
- Embedding and reranker models are cached by SentenceTransformers in the user cache directory
- File ingestion uses `RAG_FILES_BASE_PATH` as the base path