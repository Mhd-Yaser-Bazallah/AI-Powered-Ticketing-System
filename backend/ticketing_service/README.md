# Ticketing Service

## Overview
Core ticketing API handling authentication, user/company/team management, ticket lifecycle, workflows, comments, notifications, reporting, analysis endpoints, and file uploads. It calls the ticket utilities service for enrichment and publishes ticket/file events to the RAG queue.

Repository directory: `ticketing_service/`.

## Tech Stack
- Python, Django 5.1, Django REST Framework
- MySQL (primary database)
- SimpleJWT authentication
- Celery client (Redis broker) for RAG task dispatch
- `requests` for analyze service HTTP calls
- `sentence-transformers` for team embeddings

## Base URL
http://127.0.0.1:8000

## Run This Service Only
```bash
cd ticketing_service
copy .env.example .env
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Dependencies required at runtime:
- MySQL 8+ (for application data)
- Redis 6+ (only if dispatching RAG tasks)

## Configuration
Environment variables from `ticketing_service/.env.example` and settings:

| Variable | Purpose | Default |
| --- | --- | --- |
| `DB_NAME` | MySQL database name | Not found in repository (needs confirmation) |
| `DB_USER` | MySQL user | Not found in repository (needs confirmation) |
| `DB_PASSWORD` | MySQL password | Not found in repository (needs confirmation) |
| `DB_HOST` | MySQL host | `localhost` |
| `JWT_SECRET` | JWT signing secret | Not found in repository (needs confirmation) |
| `RAG_BROKER_URL` | Redis broker URL for RAG tasks | Not found in repository (needs confirmation) |
| `RAG_TASK_QUEUE` | Celery queue name | `rag_events` |
| `RAG_API_KEY` | RAG API key (used by permissions) | empty string |
| `ANALYZE_SERVICE_BASE_URL` | Ticket utils service base URL | `http://127.0.0.1:8002` |
| `TEAM_EMBEDDING_MODEL_PATH` | SentenceTransformer model path/name | `all-MiniLM-L6-v2` |

## API Reference
All routes are rooted at `http://127.0.0.1:8000/`.

### Authentication
- `POST /authentication/register`
- `POST /authentication/login`
- `POST /authentication/logout`

Example (register):
```bash
curl -X POST http://127.0.0.1:8000/authentication/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user1","company_id":1,"phone_number":"1234567890","password":"secret"}'
```

### Users
- `GET /users/List`
- `POST /users/create`
- `PUT /users/update/<user_id>`
- `DELETE /users/delete/<user_id>`
- `GET /users/search/<user_id>`
- `GET /users/getme/<user_id>`
- `PUT /users/account/update`
- `DELETE /users/account/delete`

Example (list users):
```bash
curl http://127.0.0.1:8000/users/List
```

### Companies
- `GET /company/List`
- `GET /company/company`
- `POST /company/create`
- `PUT /company/update/<company_id>`
- `DELETE /company/delete/<company_id>`
- `GET /company/search/<company_id>`
- `GET /company/company_email`
- `POST /company/toggle_auto_prioritize/<company_id>/`
- `POST /company/toggle_auto_categorize/<company_id>/`
- `POST /company/toggle_auto_assign/<company_id>/`

Example (create company):
```bash
curl -X POST http://127.0.0.1:8000/company/create \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme","address":"123 Main St","email":"ops@acme.com"}'
```

### Teams
- `GET /team/List`
- `GET /team/List-members/<company_id>`
- `GET /team/team/<company_id>`
- `POST /team/create`
- `POST /team/createMember`
- `PUT /team/update/<team_id>`
- `DELETE /team/delete/<team_id>`
- `GET /team/search/<team_id>`
- `POST /team/add-user/<user_id>`
- `POST /team/activate/<user_id>`
- `POST /team/deactivate/<user_id>`

Example (create team):
```bash
curl -X POST http://127.0.0.1:8000/team/create \
  -H "Content-Type: application/json" \
  -d '{"description":"Billing team","category":"billing","company":1}'
```

### Tickets
- `GET /ticket/List`
- `POST /ticket/create`
- `GET /ticket/client-Tickets/<client_id>`
- `GET /ticket/assign-user-Tickets/<user_id>`
- `GET /ticket/assign-team-Tickets/<team_id>`
- `GET /ticket/company-Tickets/<company_id>`
- `POST /ticket/Assign-Ticket-team/<ticket_id>`
- `POST /ticket/Ticket-In-Progress/<ticket_id>`
- `POST /ticket/Ticket-To-Done/<ticket_id>`
- `POST /ticket/Assign-Ticket-user/<ticket_id>`
- `PUT /ticket/update/<ticket_id>`
- `DELETE /ticket/delete/<ticket_id>`
- `POST /ticket/<ticket_id>/advance-status`
- `POST /ticket/<ticket_id>/solve`

Example (create ticket):
```bash
curl -X POST http://127.0.0.1:8000/ticket/create \
  -H "Content-Type: application/json" \
  -d '{"description":"Customer cannot login","title":"Login issue","client":1,"company":1}'
```

### Ticket Logs
- `GET /ticket-log/List`
- `POST /ticket-log/create`
- `GET /ticket-log/cmopany_log/<company_id>`
- `GET /ticket-log/search/<log_id>`

Example (list logs):
```bash
curl http://127.0.0.1:8000/ticket-log/List
```

### Comments
- `GET /comments/List`
- `POST /comments/create`
- `PUT /comments/update/<comment_id>`
- `DELETE /comments/delete/<comment_id>`
- `GET /comments/search/<comment_id>`
- `GET /comments/commentsUser/<user_id>`
- `GET /comments/commentsTicket/<ticket_id>`

Example (create comment):
```bash
curl -X POST http://127.0.0.1:8000/comments/create \
  -H "Content-Type: application/json" \
  -d '{"ticket":123,"user":1,"description":"Investigating this now"}'
```

### Workflows
- `GET /workflow/list`
- `POST /workflow/create`
- `POST /workflow/create-default-company`
- `GET /workflow/by-company`

Example (create custom workflow):
```bash
curl -X POST http://127.0.0.1:8000/workflow/create \
  -H "Content-Type: application/json" \
  -d '{"name":"Default Workflow","company":1,"created_by":1,"steps":[{"name":"Open"},{"name":"In Progress"},{"name":"Done"}]}'
```

### Reporting
- `GET /reporting/tickets/status`
- `GET /reporting/tickets/priority`
- `GET /reporting/teams/performance`
- `GET /reporting/companies/tickets`

Example (ticket status report):
```bash
curl -L http://127.0.0.1:8000/reporting/tickets/status
```

### Analysis
- `GET /analysis/analysis/<company_id>/`

Example:
```bash
curl http://127.0.0.1:8000/analysis/analysis/1/
```

### Files
- `GET /api/files/?company_id=<company_id>`
- `POST /api/files/`
- `DELETE /api/files/<file_id>/`

Example (upload file):
```bash
curl -X POST http://127.0.0.1:8000/api/files/ \
  -F "file=@C:\\path\\to\\doc.pdf" \
  -F "kind=pdf" \
  -F "company=1"
```

### Notifications
- `GET /notification/<user_id>/`
- `POST /notification/<notification_id>/read/`
- `POST /notification/read/all/`

Example (mark notification read):
```bash
curl -X POST http://127.0.0.1:8000/notification/42/read/ \
  -H "Content-Type: application/json" \
  -d '{"user":1}'
```

## Integration Points
- HTTP call to Ticket utilities service:
  - `POST {ANALYZE_SERVICE_BASE_URL}/api/analyze`
- Event-driven (Celery tasks):
  - Publishes `rag.process_ticket_created`, `rag.process_file_uploaded`, `rag.process_file_deleted` to Redis queue `rag_events`.

## Health Checks / Admin
- Admin interface: `GET /admin/`
- Health endpoint: Not found in repository (needs confirmation).

## Logging / Observability
- Uses Python logging in ticket creation flow and RAG dispatch. No structured logging format specified in the repo.
