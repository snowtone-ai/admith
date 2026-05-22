# Quality Audit Plan (Step 4 provisional implementation)

## Scope
- DI introduction for API runtime selection (`memory` / `database`).
- Removal of demo-only runtime side effects from API import path.
- Preservation of Phase 0 API behavior in demo mode.

## Audit Items
1. Static checks:
   - `rtk ruff check backend/src tests`
2. Backend correctness:
   - `rtk pytest -q`
3. Dashboard integration safety:
   - `rtk pnpm --prefix dashboard build`
4. Repository structure integrity:
   - `node scripts/verify.mjs`

## Pass Criteria
- Static checks: zero errors.
- Backend tests: all existing tests pass.
- Dashboard build: success exit code.
- Verify script: success exit code.

## Known Constraints
- Docker CLI and live PostgreSQL integration are unavailable in this execution environment.
- Database-path runtime E2E remains limited to compile/import-level validation in this pass.
