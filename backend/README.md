# Backend

FastAPI backend for the item CRUD application.

## Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

## Development

Run all backend commands from this directory:

```bash
cd backend
uv sync
uv run fastapi dev main.py
```

The API runs at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

The Vite development server proxies frontend requests from `/api` to this service.

## Current Data Sources

- Item CRUD uses an in-memory store and resets when the process restarts.
- `GET /exchange-rates` reads from the public ExchangeRate-API service.

The planned PostgreSQL migration is documented in [../docs/db-implementation.md](../docs/db-implementation.md).
