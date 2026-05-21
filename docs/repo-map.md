# repo-map.md -- pm-zero v9.4 Repository Map

## Read Policy
- Session start: read Summary only.
- Before editing: read the section for the target area when target files are unclear.
- When navigation is unclear: read Entry Points and Directory Map.
- After structural changes: update only the affected section.

## Summary
- App type: Admith MVP repository for B2B food waste matching and negotiation.
- Main runtime: Python/FastAPI backend; Next.js/TypeScript Operator Dashboard; Node.js verification scripts.
- Package manager: uv for backend; pnpm for dashboard.
- Primary source directories: backend/src/admith/, dashboard/src/, poc/.
- Primary test directory: tests/.
- Project memory: docs/ and tasks.md.
- Context source: docs/context/.
- Current goal: Step 3 MVP implemented; Docker smoke remains pending because Docker CLI is unavailable in this environment.
- Verification command: node scripts/verify.mjs.
- Secret template: .env.example.
- Runtime secret file: .env, ignored and read-denied for Claude.

## Directory Map
| Path | Purpose | Edit Frequency | Notes |
|---|---|---|---|
| docs/context/ | Source context imported before pm-zero initialization | low | Initial context documents + Palantir統合分析（Admith_Palantir_Integration.md） |
| docs/vision.md | Product north star | medium | Product intent only |
| docs/state.md | Current pointer and lock | medium | No task facts beyond active pointer |
| docs/decisions.md | Permanent rationale | medium | Add durable decisions after T005 |
| docs/issues.md | Failure and escalation log | low | Empty until failures occur |
| scripts/ | Automation | medium | verify.mjs is the structure check; run_poc.py executes the PoC comparison |
| poc/ | Step 2 negotiation PoC source | high | Rule Engine, Compliance reasons, Action state path, OntologyView/Mandate boundary, structured CNP, natural-language baseline, comparison metrics |
| backend/ | FastAPI backend | high | Hexagonal structure, domain models, Ports, adapters, API, Alembic |
| dashboard/ | Operator Dashboard | high | Next.js 15 App Router, Tailwind UI, API wrapper, login shell, resource/negotiation/audit flows |
| db/ | Database initialization | low | PostGIS and uuid-ossp init SQL |
| tests/ | Python PoC tests | high | unittest coverage for convergence, Compliance rejection, Action state path, and OntologyView mandate checks |
| .claude/ | Claude project settings | low | Minimal .env read deny |

## Entry Points
| Area | File | Purpose |
|---|---|---|
| Agent rules | AGENTS.md | Shared execution rules and Admith safety rules |
| Claude adapter | CLAUDE.md | Imports AGENTS.md |
| Task ledger | tasks.md | Step 2 PoC work breakdown |
| Verification | scripts/verify.mjs | Minimal repository checks |
| PoC comparison | scripts/run_poc.py | Runs Variant A, Variant B, and comparison summary |
| Palantir統合 | docs/context/Admith_Palantir_Integration.md | Ontology-as-Backbone設計根拠と具体的変更 |

## Common Workflows
| Workflow | Read First | Edit Usually | Verify |
|---|---|---|---|
| Plan next PoC task | docs/vision.md, tasks.md | tasks.md, docs/state.md | node scripts/verify.mjs |
| Record decision | docs/decisions.md | docs/decisions.md | git diff --check |
| Add source code | docs/repo-map.md Summary | poc/ or future backend | targeted test plus node scripts/verify.mjs |

## Generated / External Files
| Path | Rule |
|---|---|
| node_modules/ | ignored dependency output |
| dist/ | ignored build output |
| build/ | ignored build output |
| dashboard/.next/ | ignored Next.js build output; must not be tracked |
| *.tsbuildinfo | ignored TypeScript incremental cache |
| __pycache__/ | ignored Python cache |
| *.pyc | ignored Python bytecode |
| .env, .env.* | ignored secrets; do not read |

## Update Rules
- Keep Summary under 20 lines.
- Keep each directory note concrete.
- Move rationale to docs/decisions.md.
