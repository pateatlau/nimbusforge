# NimbusForge

NimbusForge is a full-stack item CRUD application for learning and iterating on
Python/FastAPI, React/TypeScript, and repository-level engineering workflows.

## Stack

- **Backend:** Python 3.12, FastAPI, Pydantic, SQLAlchemy, Alembic, asyncpg, and uv
- **Frontend:** React 19, TypeScript, Vite, and Oxlint
- **Database:** PostgreSQL 16 in Docker Compose
- **Repository tooling:** Node.js 24.11.0, npm 11.6.1, and Nx

## Repository Structure

```text
.
├── .editorconfig
├── .nvmrc
├── .python-version
├── backend/                # Modular FastAPI application, PostgreSQL, and tests
├── frontend/               # React and TypeScript application
├── docs/                   # Shared plans and architecture documentation
├── package.json            # Repository-level Node and Nx tooling
├── package-lock.json
└── README.md
```

- [Backend documentation](backend/README.md)
- [Frontend documentation](frontend/README.md)
- [Project roadmap](docs/project-level-roadmap.md)
- [Database implementation plan](docs/db-implementation.md)

## Prerequisites

- Git
- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Node.js 24.11.0 and npm 11.6.1
- Docker Desktop or Docker Engine with Docker Compose

## Runtime and Dependency Ownership

- The repository root owns pinned runtimes, Nx, and repository-level Node tooling.
- `backend/pyproject.toml` and `backend/uv.lock` own backend dependencies and tooling.
- `frontend/package.json` and its lockfile own frontend dependencies and scripts.

## Initial Setup

From the repository root:

```bash
nvm install
nvm use
npm install -g npm@11.6.1
npm ci

cd backend
uv sync --locked

cd ../frontend
npm ci
```

The backend publishes PostgreSQL on host port `55432` by default to avoid local
PostgreSQL conflicts. Copy `backend/.env.example` to `backend/.env` only when you
need to override the defaults. Real `.env` files are ignored by Git.

## Local Development

Start the database, apply its schema, load deterministic seed data, and run the
backend in one terminal:

```bash
cd backend
docker compose up -d --wait db
uv run alembic upgrade head
uv run python -m app.seed
uv run fastapi dev main.py
```

Run the frontend in a second terminal:

```bash
cd frontend
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`. Vite proxies `/api` to the
backend at `http://localhost:8000`; FastAPI documentation is available at
`http://localhost:8000/docs`.

Item CRUD is persisted in PostgreSQL and survives backend and database container
restarts. Alembic migrations and seed loading remain explicit commands; the
application does not create or seed the schema during startup.

The backend keeps `main.py` as a small import shim. Application assembly and
lifecycle behavior live in `backend/app/application.py`, item HTTP routes live
in `backend/app/routers/`, and persistence remains isolated in the database,
model, and repository modules.

## Native Commands

Backend:

```bash
cd backend
uv sync --locked
docker compose up -d --wait db
uv run alembic upgrade head
uv run python -m app.seed
uv run pytest
uv run fastapi dev main.py
```

Frontend:

```bash
cd frontend
npm ci
npm run dev
npm run build
npm run lint
npm run preview
```

See the [backend documentation](backend/README.md) for database inspection,
shutdown, reset, migration, testing, and troubleshooting commands.

## Nx Commands

Nx is installed for future repository orchestration. Backend and frontend tasks
still run through their native commands. Confirm Nx is available with:

```bash
npx nx --help
```
