# Operational Requirements

## Runtime Prerequisites
- Python 3.10+ with pip
- MySQL 8+ (or compatible)
- Redis 6+ (required only for RAG task dispatch)
- Analyze service reachable over HTTP (optional, used for ticket enrichment)

## Required Services
- MySQL database for all core data
- Redis broker for Celery RAG tasks (set `RAG_BROKER_URL` or `CELERY_BROKER_URL`)
- Analyze service at `ANALYZE_SERVICE_BASE_URL` (falls back to defaults if unavailable)

## Required Ports
- 8000: Django API server
- 3306: MySQL
- 6379: Redis (if enabled)
- 8002: Analyze service (default)

## Environment Variables
See the table in `README.md` for the full list and defaults. At minimum:
- DB_NAME, DB_USER, DB_PASSWORD
- JWT_SECRET
- DB_HOST (if not `localhost`)

## System-Level Notes
- Ensure the `media/` directory is writable for uploads and report exports.
- Plan disk space for uploaded files and generated reports under `media/`.
