# Lista API

Backend for the Lista app (FastAPI + PostgreSQL).

## Setup

```bash
# Install dependencies
poetry install

# Copy env template and fill in your local DB URL
cp .env.example .env

# Run the dev server
poetry run uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs` once running.

## Running tests

```bash
poetry run pytest -v
```

## Project structure

```
app/
  routers/    # API endpoints
  models/     # SQLAlchemy database models
  schemas/    # Pydantic request/response schemas
  core/       # config, database session
tests/
```

## Branching & PRs

- `main` is always deployable — no direct commits.
- One short-lived `feature/*` branch per Trello card.
- Every PR needs: a passing CI run, a linked Trello card, and a linked Figma frame (see PR template).
- Squash-merge into `main` once approved.

## Sprint tracking

Progress is tracked on the [Lista Trello board](https://trello.com/b/fBPv0hcY/lista-app-development).
