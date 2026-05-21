# state.md

## Current
- Branch: main
- Active task: Step 4 Production Hardening: T200-T203 done; T210 done; T211 doing; BD1-BD5 blocked
- Current executor: Codex CLI
- Write lock: none
- Coordinator: Codex CLI
- Latest verification pointer: rtk pytest -q -> 22 passed; rtk ruff check backend/src tests -> passed; node scripts/verify.mjs -> passed
- Verification mode: quick

## Current Blocker
- BD1-BD5 require human/vendor decisions before Auth, KYB, external contract, manifest, and hosting tasks can be completed.

## Next
- Resolve BD1-BD5 and complete `docs/production-human-actions.md`; run PostgreSQL/PostGIS-backed Alembic and repository contract tests when Docker/DB is available.
