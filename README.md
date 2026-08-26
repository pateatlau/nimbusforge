# NimbusForge

NimbusForge is a full-stack item CRUD application for learning and iterating on Python/FastAPI, React/TypeScript, and repo-level engineering workflow practices.

This repository keeps the backend and frontend in separate project trees while pinning shared runtime and tooling conventions at the repository root.

## Stack

- **Backend:** Python 3.12, FastAPI, Pydantic, uv, and HTTPX
- **Frontend:** React 19, TypeScript, Vite, and Oxlint
- **Repository tooling:** Node.js 22.23.0, npm 10.9.2, and Nx for repo-level orchestration
- **Planned database layer:** PostgreSQL, SQLAlchemy, and Alembic

## Repository Structure

```text
.
├── .editorconfig            # Repository formatting and newline rules
├── .nvmrc                  # Root Node.js version pin
├── .python-version         # Root Python version pin
├── .github/workflows/      # CI automation
├── backend/                # FastAPI application and Python environment
├── frontend/               # React and TypeScript application
├── docs/                   # Shared architecture and implementation plans
├── package.json            # Root npm tooling and Nx installation entry point
├── package-lock.json       # Root lockfile for repo-level Node dependencies
├── README.md               # Repository onboarding entry point
└── .gitignore              # Repo-level exclusions
```

Application-specific guidance:

- [Backend documentation](backend/README.md)
- [Frontend documentation](frontend/README.md)
- [Project roadmap](docs/project-level-roadmap.md)
- [Database implementation plan](docs/db-implementation.md)

## Prerequisites

- Git
- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Node.js 22.23.0 and npm 10.9.2
- Docker Desktop or Docker Engine for future database work

## Runtime and Dependency Ownership

- The repository root owns the pinned runtime versions and repo-level Node tooling.
- `backend/pyproject.toml` and `backend/uv.lock` own backend Python dependencies and backend tooling.
- `frontend/package.json` and `frontend/package-lock.json` own frontend dependencies and scripts.
- Root `package.json` owns Nx and other repository-level Node tooling only.

## Initial Setup

From the repository root, select the pinned runtime and match the expected npm version before installing dependencies:

```bash
nvm install
nvm use
npm install -g npm@10.9.2
npm --version
```

Install the repo-level Node tooling with the committed lockfile:

```bash
npm ci
```

Install backend dependencies with the locked lockfile:

```bash
cd backend
uv sync --locked
```

Install frontend dependencies with the committed lockfile:

```bash
cd frontend
npm ci
```

## Local Development

Run the backend from one terminal:

```bash
cd backend
uv run fastapi dev main.py
```

Run the frontend from another terminal:

```bash
cd frontend
npm run dev
```

Open the Vite URL shown in the frontend terminal, normally `http://localhost:5173`.

The frontend sends requests to `/api`, which Vite proxies to the FastAPI server at `http://localhost:8000`. FastAPI's interactive API documentation is available at `http://localhost:8000/docs`.

## Native Commands

Backend:

```bash
cd backend
uv sync --locked
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

## Nx Commands

The root `package.json` installs Nx for future repository orchestration, but the backend and frontend still run through their native commands above. You can confirm the tool is available with:

```bash
npx nx --help
```

## Current Data Behavior

Item data is currently stored in backend memory and is lost when the FastAPI process restarts.

The next project milestone replaces the in-memory store with a containerized PostgreSQL database, versioned migrations, and repeatable seed data. See the [database implementation plan](docs/db-implementation.md) for the proposed architecture and delivery steps.
