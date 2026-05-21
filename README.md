# Admith

Admith is a Phase 0 MVP for B2B food-waste matching and negotiation.

The product lets verified business operators register food-waste resources, start a deterministic negotiation flow, require human final approval, settle the approved deal, and keep an append-only audit trail.

## What This MVP Proves

- Food-waste resources can be registered and locked before negotiation.
- Price, compliance, and agreement decisions are made by deterministic rule engines, not by an LLM.
- Human final approval is required before signing or settlement.
- Settlement emits feedback records for trust, price, mandate, and matching quality.
- Operators can use a local dashboard to register resources, start negotiations, approve or reject agreements, and inspect audit events.

## Architecture

- `backend/`: FastAPI backend with domain services, ports, adapters, in-memory demo runtime, SQLAlchemy ORM, and Alembic migrations.
- `dashboard/`: Next.js operator dashboard.
- `db/`: PostgreSQL/PostGIS initialization.
- `scripts/`: smoke test, verification, PoC, and demo utilities.
- `tests/`: Python tests for the domain and API flow.

The backend follows a hexagonal architecture. The current demo runtime uses in-memory stores for a simple Docker demo, while database schema and migrations are present for the PostgreSQL path.

## Safety Boundaries

- LLMs must not make contract decisions.
- Human final approval is required before signing, settlement, or any irreversible business action.
- Phase 0 is food-waste only.
- Phase 0 assumes KYB-verified and invited counterparties.
- API keys and runtime secrets must be kept in `.env`; do not commit `.env`.
- Build artifacts such as `.next/` and `*.tsbuildinfo` are ignored and should not be committed.

## Requirements

- Docker Desktop with Docker Compose v2
- Node.js and pnpm for local dashboard checks
- Python 3.12 tooling for backend checks

## Local Setup

Create a local `.env` from `.env.example` and set a random operator API key.

```bash
cp .env.example .env
```

Required local value:

```text
API_KEY=replace-with-a-random-operator-api-key
```

Start the stack:

```bash
docker compose up -d --build
```

Open the dashboard:

```text
http://localhost:3000
```

Log in with the same `API_KEY` value from `.env`.

## Smoke Test

```bash
bash scripts/smoke_test.sh
```

On Windows, if `bash` is not on `PATH`:

```powershell
C:\Program Files\Git\bin\bash.exe scripts/smoke_test.sh
```

Stop the stack:

```bash
docker compose down
```

## Verification

Backend:

```bash
rtk ruff check backend/src tests
rtk pytest -q
```

Dashboard:

```bash
rtk pnpm --prefix dashboard lint
rtk pnpm --prefix dashboard typecheck
rtk pnpm --prefix dashboard test
rtk pnpm --prefix dashboard build
```

Repository structure:

```bash
node scripts/verify.mjs
```

## Current Scope

This is not production-ready SaaS. Before production use, replace the in-memory runtime with the database-backed repository path, add organization/user auth, enforce full KYB workflows, harden deployment secrets, and run cross-vendor security review.
