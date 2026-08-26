# NimbusForge Frontend

This frontend uses React, TypeScript, and Vite. The repository root pins the Node.js version and installs repo-level tooling such as Nx, while the frontend package owns the app-specific dependencies and scripts.

## Prerequisites

- Node.js 22.12.0
- npm 10.9.2
- The repository root `.nvmrc` defines the supported runtime version

## Development

Install dependencies with the committed lockfile:

```bash
cd frontend
npm ci
npm run dev
```

The Vite dev server runs at the URL reported by the command, typically `http://localhost:5173`.

The frontend proxies `/api` to the FastAPI backend at `http://localhost:8000`.

## Repository Boundaries

- `frontend/package.json` and `frontend/package-lock.json` own the React, TypeScript, Vite, and linting setup.
- The root `package.json` owns Nx and other repo-level Node tooling only.
- Shared onboarding and root runtime pinning live in the repository root `README.md`, `.nvmrc`, and `.python-version`.
