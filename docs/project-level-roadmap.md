# NimbusForge Project-Level Roadmap

This roadmap tracks repository-wide work in priority order. Detailed feature plans should remain in separate documents and be linked from the relevant section here.

## Project Overview

**Project name:** NimbusForge

**Current level:** See the Status Snapshot below for implementation status.

**Implemented today:**

- The backend is a FastAPI application in `backend/main.py`.
- Item CRUD is persisted in PostgreSQL through SQLAlchemy's async ORM.
- Docker Compose provides PostgreSQL 16 with health checks, a named volume, and a dedicated test database.
- Alembic owns schema migrations, and committed fixtures load through a transactional, idempotent seed command.
- PostgreSQL-backed Phase 1 integration tests cover migrations, CRUD compatibility, transactions, constraints, seeding, and outages.
- The frontend is a React, TypeScript, and Vite application in `frontend/`.
- Vite proxies frontend `/api` requests to the backend at `http://localhost:8000`.
- Backend and frontend dependencies are separated into their own project directories.
- The backend uses uv with `backend/pyproject.toml`, `backend/uv.lock`, `backend/.venv`, and a pinned Python version in `backend/.python-version`.
- The frontend uses npm with `frontend/package.json` and `frontend/package-lock.json`.
- The repository root pins Python and Node.js versions, includes root Node tooling, and documents the repo-level setup and ownership boundaries.
- Shared project documentation lives in `docs/`.

**Not implemented yet:**

- Backend modularization beyond the persistence modules required by Phase 1
- Backend tests outside Phase 1 database integration coverage, and frontend automated tests
- Tailwind CSS, shadcn/ui, design tokens, and reusable frontend components
- ESLint and Prettier for frontend quality checks
- Ruff and Pyright for backend quality checks
- Frontend environment examples and environment-specific configuration beyond the implemented backend local defaults
- Pre-commit hooks, CI/CD, and deployment configuration
- Nx monorepo orchestration
- AWS CDK infrastructure and production deployment

The checkboxes below describe the target project state. A command shown in a future-state workflow is a planned interface until the corresponding implementation task is complete.

### Status Snapshot

| Area                                 | Status                      |
| ------------------------------------ | --------------------------- |
| Backend/frontend separation          | Implemented                 |
| FastAPI item CRUD                    | Implemented with PostgreSQL |
| React/Vite frontend                  | Implemented                 |
| PostgreSQL persistence               | Implemented                 |
| Backend modularity                   | Planned                     |
| Automated tests                      | Phase 1 integration tests   |
| Frontend design system               | Planned                     |
| Root tooling and runtime pinning     | Implemented                 |
| Frontend and backend quality tooling | Planned                     |
| Pre-commit and CI/CD                 | Planned                     |
| Deployment and operations            | Planned                     |
| AWS cloud infrastructure             | Planned                     |
| Nx orchestration                     | Planned                     |
| API contract governance              | Planned                     |
| Security and dependency maintenance  | Planned                     |
| Accessibility                        | Planned                     |
| Architecture decision records        | Planned                     |
| Failure and recovery exercises       | Planned                     |

### Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Node.js with npm
- Git
- Repository-root Python and Node.js runtimes are pinned in `.python-version` and `.nvmrc`, and the backend also pins its own Python version in `backend/.python-version`
- Docker Desktop or Docker Engine and Docker Compose
- An AWS account and AWS CLI access once section 10 is implemented
- A pre-commit installation once section 9 is implemented

### Tool Responsibilities

| Tool           | Responsibility                                                 |
| -------------- | -------------------------------------------------------------- |
| uv             | Backend Python dependencies, lockfile, and virtual environment |
| root npm       | Nx and repository-level Node tooling                           |
| frontend npm   | Frontend dependencies, scripts, and lockfile                   |
| Docker Compose | Local PostgreSQL runtime and persistent volume                 |
| Alembic        | Database schema migrations                                     |
| Ruff           | Python linting, import sorting, and formatting                 |
| Pyright        | Python static type checking                                    |
| ESLint         | Frontend JavaScript and TypeScript linting                     |
| Prettier       | Frontend formatting                                            |
| pre-commit     | Repository Git hooks                                           |
| Nx             | Cross-project task orchestration and affected-task practice    |
| AWS CDK        | Version-controlled AWS infrastructure definitions              |
| CI             | Authoritative validation and release checks                    |

Nx must not become the owner of backend or frontend dependencies. Its targets should delegate to the native commands documented by each application.

### Repository Ownership Boundaries

- The root `package.json` owns Nx and repository-level Node tooling only.
- `frontend/package.json` and `frontend/package-lock.json` own React, Vite, Tailwind, shadcn/ui, tests, and frontend quality tooling.
- `backend/pyproject.toml` and `backend/uv.lock` own Python dependencies and backend tooling.
- `infra/package.json` and its lockfile own the TypeScript AWS CDK application and infrastructure dependencies.
- Nx orchestrates native uv and npm commands across backend, frontend, and infrastructure projects; it does not install or duplicate project dependencies.

### Current and Future Workflows

The commands currently available are:

```bash
# Terminal 1: database, schema, seed, and backend
cd backend
docker compose up -d --wait db
uv run alembic upgrade head
uv run python -m app.seed
uv run fastapi dev main.py

# Terminal 2
cd frontend
npm install
npm run dev
```

The implemented local workflow starts PostgreSQL, migrations, and seeding before the backend:

```text
PostgreSQL container -> migrations -> seed data -> backend -> frontend
```

The planned Nx workflow is an additional orchestration layer, not a replacement for the commands above:

```bash
npx nx run-many -t lint,typecheck,test,build
npx nx graph
npx nx affected -t lint,test,build
```

## Phase 0. Repository and Runtime Foundation

- [x] Add a root `package.json` and lockfile for pinned Nx and repository-level Node tooling.
- [x] Keep frontend and backend dependency ownership in their existing manifests and document the boundary.
- [x] Pin the Python version in `.python-version` and the Node.js version in `.nvmrc` or an equivalent declaration.
- [x] Use the same pinned runtime versions locally and in GitHub Actions.
- [x] Use `uv sync --locked` and `npm ci` in CI so dependency installation cannot rewrite lockfiles.
- [x] Keep all lockfiles committed and fail CI when a manifest and lockfile disagree.
- [x] Add a root `.editorconfig` defining UTF-8, LF line endings, indentation, trailing whitespace, and final-newline conventions.
- [x] Make the root README the complete onboarding entry point, including prerequisites, installation, configuration, local topology, native commands, and Nx commands.
- [x] Verify that a new developer can reach a working environment from a clean clone without undocumented steps.

**Done when:** runtime and dependency installation are reproducible, ownership of each tooling layer is unambiguous, and the root README is sufficient to begin development.

**Status:** Completed for Phase 0.

### Assumptions and Risks

- Data entered before Phase 1 was not recoverable after the in-memory backend process stopped; current item data is durable in PostgreSQL.
- Seed fixtures should be deterministic, committed, offline-capable, transactional, and idempotent.
- PostgreSQL should be used for both development and integration testing so database-specific behavior is exercised.
- The existing frontend API contract is preserved while persistence is changed behind it.
- Nx will wrap native `uv` and `npm` commands; it will not replace either dependency manager.
- Nx Cloud is optional and should be evaluated only after local caching and CI behavior are understood.
- Real credentials must never be committed, placed in frontend bundles, or written to logs.
- Local development initially runs Vite and FastAPI natively with PostgreSQL in Docker Compose for fast feedback.
- AWS is the only production deployment target for this project and initially uses one region and one environment.
- Production serves the React build from private S3 through CloudFront, runs FastAPI on ECS/Fargate behind an ALB, and stores data in private RDS PostgreSQL.
- AWS CDK in `infra/` is the authoritative infrastructure definition; console changes are limited to inspection and troubleshooting.
- The application remains a simple CRUD domain; complexity belongs in the engineering workflow rather than additional business features or infrastructure.

### Milestones

1. **Repository foundation:** root tooling ownership, pinned runtimes, conventions, onboarding, and architecture decision records.
2. **Database foundation:** PostgreSQL, migrations, persistence, transactions, and seed data.
3. **Backend architecture:** routers, schemas, services/repositories, dependency injection, and settings.
4. **Frontend architecture:** Tailwind v4, shadcn/ui, design tokens, reusable components, responsiveness, and accessibility.
5. **API integration:** OpenAPI-derived contracts, frontend client/types, and compatibility checks.
6. **Testing:** backend unit/integration, frontend component/design-system, and Playwright E2E tests.
7. **Quality tooling:** Ruff, Pyright, ESLint, Prettier, TypeScript, and pre-commit.
8. **Repository automation:** CI, locked dependencies, updates, and security scanning.
9. **Nx orchestration:** project graph, targets, dependencies, caching, affected tasks, and CI integration.
10. **AWS infrastructure and deployment:** CDK, networking, S3/CloudFront, ALB/ECS/Fargate, ECR, RDS, IAM, and immutable releases.
11. **Operational readiness:** CloudWatch, health checks, secrets, backups, cost awareness, and recovery exercises.
12. **Greenfield validation:** clean-checkout development, test, build, deployment, and rollback.

Milestones group related numbered sections rather than mapping to them one-to-one; consult the section list below for the full checklist behind each milestone.

## Phase 1. Containers and Database

Detailed plan: [Database implementation plan](db-implementation.md)

- [x] Add a Docker Compose service for PostgreSQL with a named volume and health check.
- [x] Add SQLAlchemy 2.x async database models and session management.
- [x] Add Alembic and create the initial schema migration.
- [x] Model item data with database constraints and indexes.
- [x] Add version-controlled item seed fixtures.
- [x] Implement a transactional, idempotent seed command.
- [x] Define and document transaction boundaries in the service/repository architecture.
- [x] Practice explicit commit and rollback behavior, including multiple operations in one transaction.
- [x] Test successful transactions, constraint failures, and rollback without partially persisted state.
- [x] Replace the in-memory item store with PostgreSQL persistence.
- [x] Preserve all existing endpoint paths, payloads, status codes, and error responses.
- [x] Document database startup, migration, seeding, inspection, shutdown, and reset commands.
- [x] Verify migrations can upgrade a blank database, downgrade to base, and upgrade again.
- [x] Verify item data survives API and database container restarts.
- [x] Verify backend behavior when PostgreSQL is unavailable at startup or becomes temporarily unavailable.

**Done when:** local development is repeatable from an empty machine and persisted data survives restarts.

**Status:** Completed for Phase 1.

### Local Run Workflow

The complete local workflow is:

```bash
# Terminal 1: start PostgreSQL
cd backend
docker compose up -d db
until [ "$(docker inspect --format='{{.State.Health.Status}}' "$(docker compose ps -q db)")" = "healthy" ]; do sleep 1; done
docker compose ps

# Terminal 1: apply the schema and load deterministic seed data
uv run alembic upgrade head
uv run python -m app.seed

# Terminal 1: start the backend
uv run fastapi dev main.py

# Terminal 2: start the frontend
cd frontend
npm install
npm run dev
```

The frontend should then be opened at the Vite URL, normally `http://localhost:5173`. The backend should be available at `http://localhost:8000`, with interactive API documentation at `/docs`.

For a clean database reset, the planned workflow is:

```bash
cd backend
docker compose down -v
docker compose up -d db
until [ "$(docker inspect --format='{{.State.Health.Status}}' "$(docker compose ps -q db)")" = "healthy" ]; do sleep 1; done
uv run alembic upgrade head
uv run python -m app.seed
```

These commands keep schema migration, deterministic seeding, and application startup as separate observable steps.

## Phase 2. Backend Modularity

- [ ] Create a backend application package such as `backend/app/`.
- [ ] Keep `backend/main.py` as a small FastAPI entry point or app import shim.
- [ ] Move Pydantic request and response schemas into a schema module.
- [ ] Move SQLAlchemy models and database configuration into dedicated modules.
- [ ] Group item endpoints into `APIRouter` modules.
- [ ] Add repository or service modules where they separate persistence from HTTP concerns.
- [ ] Use FastAPI dependencies for database sessions and other request-scoped resources.
- [ ] Add an application factory or lifespan handler for startup and shutdown resources.
- [ ] Keep module boundaries proportional to the project; avoid one-file-per-function abstractions.
- [ ] Update backend documentation with the resulting architecture and entry points.
- [ ] Keep pure business logic independent from FastAPI and PostgreSQL where practical so it can be unit tested.
- [ ] Return safe, actionable failures without leaking connection strings, SQL, stack traces, or other sensitive implementation details.

**Done when:** route handlers coordinate HTTP behavior, persistence code is independently testable, and `main.py` no longer owns schemas, storage, and business logic.

## Phase 3. Automated Tests

Explicitly separate fast unit tests, PostgreSQL-backed integration tests, and browser-level end-to-end tests. Test names, directories, documentation, and CI jobs should make the level clear.

### Unit Tests

- [ ] Test pure backend business logic independently from FastAPI and PostgreSQL.
- [ ] Test frontend utilities and isolated component behavior with Vitest and React Testing Library.
- [ ] Keep unit tests deterministic, fast, and focused on observable behavior rather than implementation details.

### Integration Tests

- [ ] Add backend test dependencies and configuration for pytest and async tests.
- [ ] Run database integration tests against PostgreSQL rather than SQLite.
- [ ] Add fixtures that create an isolated test database and apply Alembic migrations.
- [ ] Test item list, create, retrieve, update, delete, validation, and not-found behavior.
- [ ] Test migration upgrade/downgrade behavior.
- [ ] Test seeding success, idempotency, sequence alignment, validation, and transaction rollback.
- [ ] Test service/repository behavior, database constraints, successful transactions, and rollback against PostgreSQL.
- [ ] Keep integration tests independent of public network services.

### Frontend Component and Design-System Tests

- [ ] Test reusable components, variants, and important interaction states independently.
- [ ] Test keyboard interaction and loading, disabled, empty, success, and error states where applicable.
- [ ] Add automated accessibility assertions for representative shared components.
- [ ] Consider Storybook interaction tests and visual regression for important shared components as stretch goals.

### End-to-End Tests

- [ ] Add a browser-level CRUD smoke test with Playwright after the database flow is stable.
- [ ] Exercise the real React frontend, FastAPI backend, and PostgreSQL database.
- [ ] Use real design-system components through a representative create, read, update, and delete workflow.
- [ ] Include responsive behavior, an API failure, and frontend retry/recovery in at least one representative scenario.
- [ ] Make tests deterministic and independent of public network services.
- [ ] Define practical coverage reporting and thresholds after the initial suite exists.

**Done when:** backend contracts, persistence, core frontend behavior, and one full-stack user flow are checked automatically.

## Phase 4. Frontend Architecture and Design System

### Styling Foundation and Tokens

- [ ] Add Tailwind CSS v4 as the primary utility-first styling system.
- [ ] Add shadcn/ui as the source-owned foundation for reusable UI primitives.
- [ ] Document the distinction between Tailwind utilities, shadcn-generated components, shared application components, and feature-specific components.
- [ ] Define centralized semantic design tokens for color, typography, spacing, radius, shadows, dimensions, breakpoints, and transitions.
- [ ] Define light and dark theme tokens even if only one theme is initially exposed.
- [ ] Require shared components to consume semantic tokens instead of scattering raw values or repeated one-off utility combinations.
- [ ] Document where tokens live, how they are named, and how new tokens are introduced.

### Component Hierarchy

- [ ] Separate reusable design-system components from feature-specific components.
- [ ] Establish conventions for naming, props, composition, and variants using one consistent variant mechanism.
- [ ] Build components in response to real application needs, beginning with Button, Input, Select, Checkbox, Dialog, Menu, Toast, Card, Table, Form, and loading/empty/error states.
- [ ] Prefer existing or customized shadcn components where they fit; use application-specific components for domain composition and plain Tailwind for genuinely local styling.
- [ ] Keep the design system inside the frontend application until a genuine reason exists to publish a separate package.
- [ ] Treat shared component APIs as contracts and avoid feature-specific assumptions leaking into reusable components.

### Documentation, Responsiveness, and Accessibility

- [ ] Document component purpose, variants, states, accessibility expectations, and intended/unintended usage.
- [ ] Define responsive-layout conventions and test representative desktop, tablet, and mobile viewports.
- [ ] Define keyboard behavior, visible focus treatment, labels, accessible names, and assistive-technology expectations for dialogs, menus, notifications, and dynamic content.
- [ ] Ensure loading, empty, success, and error states do not rely on color alone.
- [ ] Consider Storybook as an Nx-integrated stretch goal for component development and documentation.

**Done when:** the application has a small, documented, token-driven component layer that is consistent, responsive, accessible, and independently testable.

## Phase 5. Frontend Quality Tooling

- [ ] Use **ESLint** as the frontend linter; remove Oxlint rather than maintaining overlapping lint rules.
- [ ] Configure ESLint with `typescript-eslint`, `eslint-plugin-react-hooks`, and `eslint-plugin-react-refresh` for TypeScript and React code.
- [ ] Use **Prettier** as the frontend formatter, with checked-in `.prettierrc` and `.prettierignore` files.
- [ ] Add `lint`, `lint:fix`, `format`, `format:check`, and `typecheck` scripts.
- [ ] Ensure ESLint and Prettier do not disagree by using a compatible configuration.
- [ ] Apply formatting once in a dedicated mechanical change.
- [ ] Document editor integration and the canonical frontend quality commands.

Canonical commands:

```bash
npm run lint          # eslint .
npm run lint:fix      # eslint . --fix
npm run format        # prettier . --write
npm run format:check  # prettier . --check
npm run typecheck     # tsc -b
```

**Done when:** linting, formatting, and TypeScript checking run non-interactively and produce the same results locally and in CI.

## Phase 6. Backend Quality Tooling

- [ ] Use **Ruff** for Python linting, import sorting, and formatting.
- [ ] Configure Ruff in `backend/pyproject.toml` with an explicit target Python version and selected rules.
- [ ] Use **Pyright** as the backend static type checker, configured in `backend/pyrightconfig.json` or `backend/pyproject.toml`.
- [ ] Enable strictness incrementally and document any intentional exceptions.
- [ ] Add commands for lint checking, automatic fixes, formatting, format checking, and type checking.
- [ ] Replace placeholder package metadata in `backend/pyproject.toml`.
- [ ] Apply formatting once in a dedicated mechanical change.
- [ ] Document editor integration and the canonical backend quality commands.

Ruff replaces separate Black and isort tooling. Canonical commands:

```bash
uv run ruff check .          # lint
uv run ruff check . --fix    # lint and apply safe fixes
uv run ruff format .         # format
uv run ruff format --check . # verify formatting
uv run pyright               # static type checking
```

**Done when:** Python linting, formatting, imports, and type checking are reproducible locally and in CI.

## Phase 7. Environment Configuration

- [ ] Define backend settings with `pydantic-settings` and typed defaults where appropriate.
- [ ] Add `backend/.env.example` containing safe local-development values.
- [ ] Add a frontend environment example for supported `VITE_*` variables.
- [ ] Ignore real `.env` files while ensuring example files remain tracked.
- [ ] Separate development, test, CI, and production configuration.
- [ ] Validate required settings at startup and fail with actionable messages.
- [ ] Keep secrets out of source control, images, logs, and frontend bundles.
- [ ] Document environment-variable precedence and database host differences between host and container execution.
- [ ] Review CORS origins and debug/development flags by environment.
- [ ] Document the local topology: native Vite and FastAPI processes with PostgreSQL in Docker Compose and Vite proxying `/api`.
- [ ] Document the production topology: CloudFront/S3 frontend, public ALB, private ECS/Fargate tasks, and private RDS PostgreSQL.
- [ ] Configure CloudFront to route frontend assets to S3 and `/api` requests to the ALB; configure FastAPI CORS only for any intentionally supported cross-origin access.
- [ ] Store production application/database secrets in AWS Secrets Manager and inject them into ECS tasks at runtime.
- [ ] Document AWS account, region, environment, and resource naming conventions plus CDK configuration differences between environments.
- [ ] Keep local development independent from AWS and add another AWS environment only if environment-promotion practice requires it.

**Done when:** a new developer can configure both applications from examples and production secrets are supplied only at runtime.

## Phase 8. Frontend Documentation Cleanup

- [ ] Replace the generated Vite README with project-specific documentation.
- [ ] Document prerequisites, installation, development, build, lint, test, and preview commands.
- [ ] Document supported environment variables and the Vite API proxy.
- [ ] Explain the main source layout, API client, state ownership, and type definitions.
- [ ] Document Tailwind, shadcn/ui customization, design-token ownership, shared/feature component conventions, responsive design, and accessibility expectations.
- [ ] Document how to add reusable and feature-specific components and how frontend targets participate in Nx.
- [ ] Document frontend unit, component, design-system, and E2E testing responsibilities.
- [ ] Describe expected backend availability and common troubleshooting steps.
- [ ] Keep shared full-stack information in the root README rather than duplicating it.
- [ ] Link back to shared plans in `docs/` where relevant.

**Done when:** the frontend README describes this application rather than the starter template.

## Phase 9. Pre-Commit Hooks, CI, and CD

- [ ] Use **pre-commit** as the single repository-wide Git hook manager; do not combine it with Lefthook or Husky.
- [ ] Add `.pre-commit-config.yaml` at the repository root with pinned hook revisions.
- [ ] Configure standard repository checks for trailing whitespace, end-of-file fixes, YAML/JSON validation, and large files.
- [ ] Configure the official Ruff pre-commit hooks for backend linting and formatting.
- [ ] Configure local pre-commit hooks that run the versions installed in `frontend/node_modules` for ESLint and Prettier.
- [ ] Scope hooks to relevant paths under `backend/` and `frontend/` and operate on staged files where practical.
- [ ] Keep pre-commit checks fast: repository hygiene, Ruff, ESLint, and Prettier.
- [ ] Run slower checks from a pre-push hook or CI: Pyright, TypeScript, tests, migrations, and builds.
- [ ] Keep slower integration and browser tests in CI rather than blocking every commit.
- [ ] Add a GitHub Actions workflow triggered for pull requests and protected branches.
- [ ] Cache uv, npm, and Docker dependencies where useful without hiding lockfile problems.
- [ ] Install Python dependencies with uv's locked synchronization and Node dependencies with `npm ci`.
- [ ] Fail CI when dependency manifests and lockfiles are inconsistent.
- [ ] Run backend lint, format check, type check, migrations, and tests in CI.
- [ ] Run frontend lint, format check, type check, tests, and production build in CI.
- [ ] Start PostgreSQL as a CI service and wait for health before database checks.
- [ ] Add a Playwright smoke-test job once the full-stack test exists.
- [ ] Add branch protection requiring the relevant checks before merge.
- [ ] Build the frontend artifact and production backend image during CI to validate packaging.
- [ ] Run `cdk synth` on every relevant CI change.
- [ ] Run `cdk diff` when infrastructure changes are detected and make the resulting infrastructure changes visible during review.
- [ ] Keep CI responsible for pull-request validation and define AWS CD separately.
- [ ] Trigger CD from an appropriate protected branch, release, or tag.
- [ ] Authenticate GitHub Actions to AWS with short-lived federated credentials rather than permanent access keys where practical.
- [ ] Build and scan the backend image, tag it with an immutable Git SHA, push it to ECR, and update ECS to that exact version.
- [ ] Deploy the frontend build to S3 and invalidate or update CloudFront content when required.
- [ ] Run production database migrations through the explicit deployment process rather than every ECS task startup.
- [ ] Wait for ECS/ALB health checks, run post-deployment smoke tests, and fail deployment when health or smoke checks fail.
- [ ] Support and document rollback to the previous frontend artifact, backend image, and compatible database state.
- [ ] Document and practice the chosen migration/deployment ordering, including why it is safe for the application's schema changes.

**Done when:** local hooks catch quick issues and every pull request receives reproducible quality, test, migration, and build checks.

## Phase 10. AWS Deployment and Cloud Infrastructure

Use the simplest production-grade AWS architecture that provides meaningful cloud-engineering practice. AWS is the only production target for this repository.

```text
                         Internet
                            |
                        Route 53
                            |
                       CloudFront
                      /          \
                     /            \
                    v              v
             S3 / React SPA      ALB
                                  |
                                  v
                            ECS / Fargate
                                  |
                               FastAPI
                                  |
                                  v
                            RDS PostgreSQL
```

```text
CloudFront
  ├── /*      → S3
  └── /api/* → ALB
```

### Infrastructure as Code and Networking

- [ ] Create an `infra/` TypeScript project for AWS CDK and keep all authoritative infrastructure definitions in source control.
- [ ] Define a single-region VPC with appropriate public/private subnet boundaries and keep ECS application tasks and RDS private where practical.
- [ ] Keep the frontend S3 bucket private and use CloudFront Origin Access Control (OAC) for bucket access.
- [ ] Define S3/CloudFront frontend hosting, SPA routing, `/api` behavior routing to the ALB, HTTPS, and optional Route 53 custom-domain integration through CDK.
- [ ] Define the public ALB, ECS/Fargate service, ECR repository, private RDS PostgreSQL, and required security groups through CDK.
- [ ] Permit only required traffic between the public entry points and backend tiers using appropriate CloudFront/ALB configuration and security groups; keep RDS inaccessible from the public internet.
- [ ] Define IAM roles/policies, Secrets Manager integration, and CloudWatch resources through CDK where appropriate.
- [ ] Practice `cdk synth`, `cdk diff`, and `cdk deploy`; inspect the synthesized CloudFormation rather than treating CDK as opaque.
- [ ] Document CDK bootstrap/deployment and ensure infrastructure can be recreated without undocumented console configuration.
- [ ] Use AWS Certificate Manager for TLS certificates and configure HTTPS for CloudFront and the ALB as appropriate.
- [ ] Use CDK context/configuration rather than hard-coding environment-specific values into infrastructure definitions.
- [ ] Keep application configuration and infrastructure configuration conceptually separate.

### IAM, Secrets, and Containers

- [ ] Avoid the AWS root account for normal development/deployment and use least-privilege IAM policies where practical.
- [ ] Distinguish ECS task execution roles from application task roles and grant FastAPI only the AWS permissions it requires.
- [ ] Use IAM roles and GitHub Actions federation instead of embedding long-lived AWS credentials.
- [ ] Keep secrets out of Git, images, CI output, and application logs; obtain production database credentials through Secrets Manager.
- [ ] Build a minimal production FastAPI image, use multi-stage construction where beneficial, run as non-root, and keep the `.dockerignore`/build context minimal.
- [ ] Tag images with immutable Git SHAs, push them to ECR, and configure ECS to deploy exact versions rather than relying on `latest`.
- [ ] Configure an ECR lifecycle policy to remove obsolete/unreferenced images and prevent unbounded registry storage growth.
- [ ] Verify production builds and deployments do not depend on uncommitted local state.

### Database, Reliability, and Operations

- [ ] Understand and document the ECS deployment strategy used for application releases, including how old and new task versions coexist during deployment and how failed deployments are detected.
- [ ] Define an explicit Alembic migration job/process; do not run migrations automatically in every application container startup unless proven safe.
- [ ] Document safe migration and rollback procedures, including compatibility with concurrently running application versions.
- [ ] Configure appropriate RDS backup/retention settings and practice or verify database restoration.
- [ ] Add liveness/readiness behavior and useful ECS/ALB health checks.
- [ ] Send structured backend/container logs to CloudWatch and monitor basic CPU, memory, request/error, and database health indicators.
- [ ] Add basic CloudWatch alarms for meaningful failure conditions and document how to locate logs and diagnose failed deployments.
- [ ] Configure sensible ECS CPU/memory allocations and graceful shutdown; understand ALB distribution and ECS task scaling.
- [ ] Keep application state out of process memory/container filesystems so multiple FastAPI tasks can share PostgreSQL safely.
- [ ] Understand basic RDS scaling/availability options and document how the architecture could evolve with substantially higher traffic.

### Architecture Learning and Scope

- [ ] Draw the complete architecture and trace frontend and API requests through Route 53, CloudFront/S3, ALB, ECS/Fargate, and RDS.
- [ ] Explain public/private boundaries, security groups, IAM roles, secret delivery, ECR-to-ECS image flow, HTTPS, logs, metrics, scaling, task crashes, database outages, and rollback.
- [ ] Use one AWS region and initially one environment; add environments only for a specific promotion-learning objective.
- [ ] Do not add API Gateway, Lambda, EKS, EC2-managed application servers, service mesh, Redis, queues/event buses, multi-region infrastructure, or enterprise networking/security layers without a later explicit learning need.
- [ ] Avoid NAT Gateway infrastructure unless the selected private-task design genuinely requires outbound access and the cost is justified.

### Cost Awareness

- [ ] Estimate monthly architecture cost and distinguish fixed costs from usage-scaled costs.
- [ ] Configure AWS Budgets/cost alerts and periodically review the major bill contributors.
- [ ] Understand the cost implications of NAT Gateways, ALB, Fargate, RDS, CloudWatch, and data transfer.
- [ ] Avoid unnecessary always-on resources and tear down non-essential environments when not in use.
- [ ] Be able to explain the approximate monthly cost of the architecture and identify the first infrastructure components that would become material cost drivers as traffic grows.

**Done when:** CDK can recreate the AWS environment; React is served by S3/CloudFront; FastAPI runs on ECS/Fargate behind an ALB using immutable ECR images; private RDS stores application data; IAM, secrets, network boundaries, logs, metrics, migrations, deployment, rollback, recovery, and costs are understood and documented.

## Phase 11. API Contract and Integration Governance

- [ ] Treat FastAPI's generated OpenAPI document as the canonical HTTP contract.
- [ ] Add contract assertions for existing paths, schemas, status codes, and error bodies.
- [ ] Evaluate OpenAPI-driven TypeScript type/client generation before retaining handwritten request and response types.
- [ ] Decide where generated client code lives and whether it is committed or generated during development and CI.
- [ ] Ensure backend schema changes propagate predictably to the frontend without relying on undocumented error shapes.
- [ ] Test representative validation and error responses across the frontend/backend boundary.
- [ ] Add a CI check that detects accidental breaking API changes.
- [ ] Establish an API versioning and deprecation policy before external consumers exist.

**Why this was missing:** tests cover examples, but explicit contract governance prevents backend refactors from silently breaking frontend assumptions.

## Phase 12. Security and Dependency Maintenance

- [ ] Add Dependabot or Renovate for uv, npm, GitHub Actions, and container base images.
- [ ] Add dependency vulnerability scanning for Python, npm, and container images.
- [ ] Enable secret scanning and review repository history before adding real credentials.
- [ ] Review request validation, error disclosure, CORS, rate limiting, and security headers.
- [ ] Pin CI actions to trusted versions and keep lockfiles required and current.
- [ ] Configure automated updates for npm, uv/Python, GitHub Actions, and Docker base images where supported.
- [ ] Add a security policy describing supported versions and private vulnerability reporting.

**Why this was missing:** secure defaults and dependency updates are ongoing repository responsibilities, not only deployment tasks.

## Phase 13. Accessibility and User-Facing Quality

- [ ] Verify form labels, focus order, keyboard operation, and visible focus states.
- [ ] Announce loading, success, and error states appropriately to assistive technology.
- [ ] Check color contrast, zoom behavior, responsive layouts, and reduced-motion preferences.
- [ ] Add automated accessibility checks and one manual keyboard/screen-reader review.
- [ ] Define user-facing error and empty-state behavior for backend outages and slow requests.

**Why this was missing:** functional frontend tests do not guarantee that the application is usable or accessible.

## Phase 14. Architecture Decision Records

- [ ] Add a lightweight `docs/adr/` convention for decisions with lasting consequences.
- [ ] Record the PostgreSQL selection and persistence model as the first decision.
- [ ] Record choices for frontend linting, Python type checking, testing strategy, and the AWS deployment architecture when made.
- [ ] Record the design-system/component ownership and API-client generation decisions when made.
- [ ] Keep ADRs concise and mark superseded decisions rather than rewriting history.

**Why this was missing:** the repository already contains implementation plans, but decision records preserve why major tools and boundaries were chosen after plans evolve.

## Phase 15. Nx Monorepo Tooling

Nx is an intentional learning and orchestration layer for this repository. It should complement the backend and frontend toolchains rather than replace them. `uv`, `npm`, Ruff, Pyright, pytest, ESLint, Prettier, TypeScript, and Vite remain the owners of their native configuration and commands.

- [ ] Add Nx at the repository root with a pinned package version and a checked-in `nx.json`.
- [ ] Define `backend`, `frontend`, and `infra` as Nx projects without moving their dependency manifests or the backend virtual environment.
- [ ] Keep `backend/pyproject.toml` and `backend/uv.lock` authoritative for Python dependencies.
- [ ] Keep `frontend/package.json` and `frontend/package-lock.json` authoritative for frontend dependencies.
- [ ] Keep `infra/package.json` and its lockfile authoritative for AWS CDK dependencies.
- [ ] Add explicit Nx targets that delegate to native commands through `nx:run-commands`.
- [ ] Add backend targets for development, linting, formatting, type checking, tests, migrations, and seeding.
- [ ] Add frontend targets for development, linting, formatting, type checking, tests, and production builds.
- [ ] Add infrastructure targets for CDK linting, type checking, tests, synthesis, diff, and deployment; never cache deployments.
- [ ] Use clear target names such as `lint`, `format:check`, `typecheck`, `test`, `build`, and `dev` consistently across projects.
- [ ] Keep native commands documented in `backend/README.md`, `frontend/README.md`, and the root README.
- [ ] Add root-level Nx targets for common workflows such as `lint`, `typecheck`, `test`, and `build`.
- [ ] Practice `nx run`, `nx run-many`, and `nx graph` while keeping the equivalent direct commands available.
- [ ] Make a backend API/schema change and verify which frontend/backend projects Nx reports as affected.
- [ ] Add project dependencies and task dependencies explicitly where they exist, such as frontend integration tests depending on the backend and database.
- [ ] Configure task inputs and outputs so Nx cache results are correct and do not cache development servers or database state.
- [ ] Classify lint, format checks, type checks, unit tests, and builds as cacheable when their inputs/outputs are correct.
- [ ] Do not cache migrations, seeds, development servers, database resets, or database state; evaluate E2E caching before enabling it.
- [ ] Verify cache invalidation after relevant source/configuration changes and practice resetting the local cache.
- [ ] Configure `nx affected` with correct CI base/head references and verify unrelated changes do not trigger every project.
- [ ] Use `nx affected` in PR CI while retaining a scheduled full validation workflow.
- [ ] Add local caching first and document cache behavior, invalidation, and reset commands.
- [ ] Evaluate Nx Cloud only after local task caching and CI workflows are understood; it is optional for this repository.
- [ ] Add Nx commands to CI without making CI dependent on opaque generated behavior.
- [ ] Add a short architecture note explaining which responsibilities belong to Nx and which remain with uv, npm, and native tools.
- [ ] Model the dependency between application code and generated API-contract artifacts if OpenAPI-derived frontend types/client code is introduced.

Recommended initial command mapping:

```text
nx run backend:lint        -> cd backend && uv run ruff check .
nx run backend:typecheck   -> cd backend && uv run pyright
nx run backend:test        -> cd backend && uv run pytest
nx run frontend:lint       -> cd frontend && npm run lint
nx run frontend:typecheck  -> cd frontend && npm run typecheck
nx run frontend:build      -> cd frontend && npm run build
```

**Learning boundary:** Nx should provide project discovery, target naming, dependency graphs, parallel execution, and affected-task practice. It should not hide the commands, configuration, dependency managers, or failure output of the underlying tools.

**Done when:** `nx run-many -t lint,typecheck,test,build` can coordinate the repository, `nx affected` can select changed projects in CI, native commands still work independently, and the Nx graph accurately reflects project relationships.

## Phase 16. Failure and Recovery Exercises

Deliberately introduce failures in a disposable local, test, or non-production environment, then diagnose, recover, and document the result.

- [ ] **Database:** start without PostgreSQL, introduce and recover from an invalid migration, trigger a constraint rollback, downgrade/re-upgrade, restore a backup, and verify behavior after restart.
- [ ] **Backend:** test missing/invalid configuration and database or upstream dependency failures; verify useful responses without sensitive detail leakage.
- [ ] **Frontend:** simulate slow, unavailable, 4xx, and 5xx APIs; verify loading, empty, error, retry, and recovery states.
- [ ] **CI:** introduce lint, type-check, test, migration, and frontend-build failures; verify required checks prevent merge.
- [ ] **Nx:** introduce an incorrect task dependency or cache input/output declaration; diagnose it and verify affected selection and invalidation after correction.
- [ ] **AWS:** deploy a broken backend image, introduce configuration/secret and security-group errors, inspect ECS/ALB health and CloudWatch logs, and roll back to the known-good image.
- [ ] **AWS database:** make RDS temporarily unavailable and introduce a failed migration; verify safe API failure and practice recovery.
- [ ] **AWS frontend:** verify CloudFront/S3 remains available while the API is unavailable and the UI communicates the failure safely.

**Done when:** each layer has at least one documented failure exercise with observable detection, a repeatable recovery procedure, and evidence that partial or broken state is not silently accepted.

## Phase 17. Repository Quality Gate and Greenfield Validation

- [ ] Define one root command, initially `npx nx run-many -t lint,typecheck,test,build`, as the recommended local pre-push quality gate.
- [ ] Ensure the command works from a clean checkout, requires no unintended public network services, and clearly reports the failing project and native command.
- [ ] Keep native backend/frontend commands independently usable and make CI the authoritative equivalent of the local gate.
- [ ] From a clean machine or disposable environment, clone the repository and install the pinned Python and Node.js runtimes.
- [ ] Install locked dependencies and configure environment variables from committed examples.
- [ ] Start PostgreSQL, run migrations and seeds, then start the backend and frontend using only documented commands.
- [ ] Run unit, integration, E2E, lint, format, type-check, Nx quality-gate, and production-build workflows.
- [ ] Follow the documented deployment procedure, verify the deployed application, and perform the documented rollback procedure.
- [ ] Have a developer unfamiliar with the repository repeat the exercise without undocumented assistance.

**Done when:** a new developer can develop, test, build, deploy, verify, and roll back the application from a clean environment using only repository documentation.

## Guiding Principle

Keep the business domain intentionally simple. The project is a greenfield engineering laboratory for repeatedly practicing design, implementation, testing, quality checks, CI, build, deployment, observation, failure, recovery, and improvement. Add technologies such as authentication, microservices, event systems, Kubernetes, Redis, or Terraform only when they serve a specific learning objective.
