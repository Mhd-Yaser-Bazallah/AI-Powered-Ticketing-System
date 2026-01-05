# Ticket Utilities Service

## Overview
Provides ticket analysis (category, priority, team assignment) and a Celery-based retraining pipeline once a threshold of analyses is reached.

## Tech Stack
- Python, Django, Django REST Framework
- MySQL
- Celery + Redis
- Hugging Face Transformers (BERT)
- spaCy + spacytextblob

## Base URL
http://127.0.0.1:8002

## Run This Service Only
```bash
cd ticket_utils_service
copy .env.example .env
python manage.py migrate
python manage.py runserver 127.0.0.1:8002
```

Dependency manifest (requirements.txt/pyproject) not found in repository (needs confirmation).

Start Celery worker for training:
```bash
celery -A ticket_utils_service worker -l info
```

Required services:
- MySQL
- Redis

## Configuration
Environment variables from `ticket_utils_service/.env.example` and settings:

| Variable | Purpose | Default |
| --- | --- | --- |
| `DB_NAME` | MySQL database name | Not found in repository (needs confirmation) |
| `DB_USER` | MySQL user | Not found in repository (needs confirmation) |
| `DB_PASSWORD` | MySQL password | Not found in repository (needs confirmation) |
| `DB_HOST` | MySQL host | `localhost` |
| `ANALYZE_TRAINING_THRESHOLD` | Count before retraining | `100` |
| `TRAINING_EXPORT_PATH` | XLSX export path | `exports/tickets_training.xlsx` |
| `TRAINING_EXPORT_SHEET_NAME` | Export sheet name | `Sheet1` |
| `TRAINING_DATA_DIR` | Training data directory | `ticket/utils/ml/training` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | Celery result backend | `redis://localhost:6379/0` |

## API Reference
All routes are rooted at `http://127.0.0.1:8002/api`.

### Analyze Ticket
- `POST /api/analyze`

Example:
```bash
curl -X POST http://127.0.0.1:8002/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"description":"Email delivery failing for multiple users","company_id":1}'
```

Response fields (from code):
- `category`
- `priority`
- `team_assignment`

## Integration Points
- Called by Ticketing service via `POST /api/analyze`.
- Internal async retraining task: `export_tickets_and_retrain` (Celery).

## Health Checks / Admin
- Admin interface: `GET /admin/`
- Health endpoint: Not found in repository (needs confirmation).

## Logging / Observability
- Uses Python logging in analysis and training pipeline.
- Retraining runs `ticket/utils/ml/training/Splitting.py` and `train_bert.py` via subprocess.
