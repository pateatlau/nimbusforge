# NimbusForge Frontend

This frontend uses React, TypeScript, Vite, Tailwind CSS v4, and source-owned shadcn/ui-style components. The repository root pins the Node.js version and installs repo-level tooling such as Nx, while the frontend package owns the app-specific dependencies and scripts.

## Prerequisites

- Node.js at the version pinned in the repository root `.nvmrc`
- npm 11.6.1

## Development

Install dependencies with the committed lockfile:

```bash
cd frontend
npm ci
npm run dev
```

The Vite dev server runs at the URL reported by the command, typically `http://localhost:5173`.

The frontend proxies `/api` to the FastAPI backend at `http://localhost:8000`.

## Build And Preview

```bash
npm run build
npm run preview
```

`npm run build` runs the TypeScript project build before creating the production Vite bundle. Frontend test and Phase 5 quality-tooling commands are not implemented yet; `npm run lint` continues to use the existing Oxlint configuration until that phase.

## Source Layout

```text
src/
├── api/                 # HTTP client modules
├── components/ui/       # Domain-neutral, source-owned UI primitives
├── components/          # Shared application components
├── features/items/      # Item-specific forms and tables
├── lib/                 # Shared utility functions
├── App.tsx              # Screen composition and item state ownership
├── index.css            # Tailwind import, semantic tokens, and base styles
└── types.ts             # Frontend API types
```

`App.tsx` owns item loading and mutation state. `api/items.ts` owns HTTP calls. Feature components compose shared primitives without moving domain assumptions into `components/ui/`.

## Design System

Tailwind utilities are the styling language. Semantic light and dark tokens live in `src/index.css`; reusable primitives consume those tokens rather than raw color and spacing values. `components.json` records the shadcn/ui source and alias conventions. CVA is the consistent variant mechanism, and `cn()` merges component classes.

The application currently provides Button, Input, Select, Checkbox, Dialog, Dropdown Menu, Toast, Card, Table, Form helpers, and shared loading, empty, error, and success states. Item-specific composition lives under `src/features/items/`.

Layouts are mobile-first and validated at representative mobile, tablet, and desktop widths. Controls require visible labels or accessible names, focus remains visible, Radix primitives own menu/dialog keyboard behavior, and dynamic states include text and live-region semantics rather than relying on color.

See the [frontend design-system documentation](../docs/frontend-design-system.md) for component contracts, token naming, ownership boundaries, responsive conventions, accessibility expectations, and contribution rules.

## Repository Boundaries

- `frontend/package.json` and `frontend/package-lock.json` own React, TypeScript, Vite, Tailwind, shadcn/Radix dependencies, and frontend linting.
- The root `package.json` owns Nx and other repo-level Node tooling only.
- Shared onboarding and root runtime pinning live in the repository root `README.md`, `.nvmrc`, and `.python-version`.
