# Backend

FastAPI backend for NimbusForge.

## Prerequisites

- Python 3.12 (pinned in both the repository-root `.python-version` and `backend/.python-version`; keep them in sync)
- [uv](https://docs.astral.sh/uv/)
- Root runtime pinning is defined in the top-level `.python-version`, and the backend runtime pin is defined in `backend/.python-version`

## Development

Run backend commands from the repository root:

```bash
cd backend
uv sync --locked
uv run fastapi dev main.py
```

The API runs at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

The Vite development server proxies frontend requests from `/api` to this service.

## Current Data Sources

- Item CRUD uses an in-memory store and resets when the process restarts.

The planned PostgreSQL migration is documented in [../docs/db-implementation.md](../docs/db-implementation.md).

## Repository Boundaries

- Backend Python dependencies live in `backend/pyproject.toml` and `backend/uv.lock`.
- Repository-level runtime pinning and root tooling live in the root `README.md`, `.python-version`, `.nvmrc`, and `package.json`.
