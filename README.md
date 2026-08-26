# FastAPI + React Learning Project

A small full-stack item CRUD application for practicing FastAPI, React, TypeScript, uv, API integration, and database-backed development.

The repository keeps the backend and frontend as separate projects while sharing project-level documentation from `docs/`.

## Stack

- **Backend:** Python 3.12, FastAPI, Pydantic, uv, and HTTPX
- **Frontend:** React 19, TypeScript, Vite, and Oxlint
- **Planned database:** PostgreSQL, SQLAlchemy, and Alembic

## Repository Structure

```text
.
├── backend/    # FastAPI application and Python environment
├── frontend/   # React and TypeScript application
├── docs/       # Shared architecture and implementation plans
└── README.md   # Repository overview
```

Each application manages its own dependencies and development commands:

- [Backend documentation](backend/README.md)
- [Frontend documentation](frontend/README.md)
- [Database implementation plan](docs/db-implementation.md)

## Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- Node.js with npm

## Run Locally

Install and start the backend from one terminal:

```bash
cd backend
uv sync
uv run fastapi dev main.py
```

Install and start the frontend from another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the frontend terminal, normally `http://localhost:5173`.

The frontend sends requests to `/api`, which Vite proxies to the FastAPI server at `http://localhost:8000`. FastAPI's interactive API documentation is available at `http://localhost:8000/docs`.

## Available Features

- List items
- Create items with an optional description
- Edit existing items
- Delete items

## Current Data Behavior

Item data is currently stored in backend memory and is lost when the FastAPI process restarts.

The next project milestone replaces the in-memory store with a containerized PostgreSQL database, versioned migrations, and repeatable seed data. See the [database implementation plan](docs/db-implementation.md) for the proposed architecture and delivery steps.

## Useful Commands

Run backend commands from `backend/`:

```bash
uv sync
uv run fastapi dev main.py
```

Run frontend commands from `frontend/`:

```bash
npm run dev
npm run build
npm run lint
npm run preview
```
