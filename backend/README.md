# Backend

FastAPI backend for NimbusForge, backed by PostgreSQL 16 through SQLAlchemy's
async ORM and versioned with Alembic migrations.

## Prerequisites

- Python 3.12, pinned in the root and backend `.python-version` files
- [uv](https://docs.astral.sh/uv/)
- Docker Desktop or Docker Engine with Docker Compose

## First Run

Run backend commands from `backend/`:

```bash
uv sync --locked
docker compose up -d --wait db
uv run alembic upgrade head
uv run python -m app.seed
uv run fastapi dev main.py
```

The API runs at `http://localhost:8000`, with interactive documentation at
`http://localhost:8000/docs`. The Vite server proxies frontend `/api` requests
to this service.

Local defaults work without an environment file. Copy `.env.example` to `.env`
to override them. The backend runs on the host and reaches PostgreSQL through
`localhost`; a future containerized backend would use the Compose service name
`db` instead.

## Database Operations

```bash
# Start PostgreSQL and wait for health
docker compose up -d --wait db

# Apply, inspect, or reverse migrations
uv run alembic upgrade head
uv run alembic current
uv run alembic downgrade base

# Load the committed fixture; safe to run repeatedly
uv run python -m app.seed

# Inspect container state and database logs
docker compose ps
docker compose logs db

# Stop PostgreSQL without deleting item data
docker compose down

# Delete local data and rebuild from the migration and fixture
docker compose down -v
docker compose up -d --wait db
uv run alembic upgrade head
uv run python -m app.seed
```

PostgreSQL publishes host port `55432` by default to avoid conflicts with local
PostgreSQL installations and binds it to `127.0.0.1` by default. The container
continues to listen on port `5432`. To use another host port, set the same value
in `POSTGRES_PORT`, `DATABASE_URL`, and `TEST_DATABASE_URL` in `.env`. Set
`POSTGRES_BIND_ADDRESS` only when remote host access is intentional.

## Transactions

Route handlers and the seed command own transaction boundaries with
`session.begin()`. Repository functions issue queries and `flush()` writes but
never commit, so one caller can group multiple repository operations into one
atomic transaction. Leaving the transaction block commits successful work;
any exception rolls back the entire block without partial persistence.

Schema creation and seeding are separate explicit operations. The application
checks database connectivity during startup and fails startup when PostgreSQL is
unavailable. A database driver failure after startup returns
`503 {"detail":"Database unavailable"}`.

## Tests

Compose creates a dedicated `nimbusforge_test` database with a fresh volume.
With PostgreSQL healthy, run:

```bash
uv run pytest
```

The suite cycles migrations from blank to head, down to base, and back to head.
It also verifies CRUD compatibility, constraints, multi-operation commit and
rollback, seed idempotency and rollback, and database outage behavior. Override
`TEST_DATABASE_URL` when Compose uses a non-default published port.

## Source Layout

- `main.py` defines the FastAPI lifecycle, middleware, error handling, and item routes.
- `app/config.py` and `app/database.py` own settings, the engine, and sessions.
- `app/models.py`, `app/schemas.py`, and `app/repositories.py` own item persistence.
- `alembic/` contains the versioned schema history.
- `seeds/items.json` and `app/seed.py` own deterministic local seed data.
- `tests/` contains PostgreSQL-backed Phase 1 integration tests.

Backend Python dependencies and tooling remain owned by `pyproject.toml` and
`uv.lock`. Repository-level runtime pinning and Nx tooling remain at the root.
