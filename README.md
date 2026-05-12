# AccordIQ

AccordIQ turns Slack conversations into durable team agreements: tasks,
decisions, open questions, and cited recall answers backed by Notion and
Postgres/pgvector.

## Backend V1

This repository contains the backend-only phase:

- FastAPI Slack edge.
- Redis/arq-style worker boundaries.
- LangGraph-style extraction and query workflows.
- Postgres + pgvector data model.
- Notion system-of-record sync.
- Admin panel API endpoints for the later frontend phase.
- Docker Compose with API, worker, Postgres/pgvector, and Redis.

## Runtime Rule

Runtime values belong in YAML and environment variables. Provider names,
model names, API versions, thresholds, scopes, prompts, Docker image names,
and emoji mappings must not be hardcoded in business logic.

## Local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
docker compose config --quiet
```
