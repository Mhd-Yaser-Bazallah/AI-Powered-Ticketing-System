# Requirements (Operational)

## Runtime prerequisites
- Python 3.12 (pycache indicates cpython-312)
- MySQL 8.x (or compatible)
- Redis 6.x+
- spaCy model `en_core_web_sm`

## External services
- MySQL: create the database defined by `DB_NAME` and ensure credentials match `DB_USER`/`DB_PASSWORD`.
- Redis: required for Celery broker and result backend.

## Ports
- Service HTTP: `8000` (default Django runserver)
- MySQL: `3306`
- Redis: `6379`

## Environment variables
See the environment variable table in `README.md`.

## Storage and volumes
- `exports/` is created for XLSX training exports.
- `ticket/utils/ml/training/` stores training CSVs and outputs.
- `ticket/utils/ml/models/` holds ML model artifacts required at runtime.
