# repo-map.md -- pm-zero v9.4 Repository Map

## Read Policy
- Session start: read Summary only.
- Before editing: read the section for the target area when target files are unclear.
- When navigation is unclear: read Entry Points and Directory Map.
- After structural changes: update only the affected section.

## Summary
- App type: early-stage PoC repository for Admith multi-agent negotiation.
- Main runtime: Python/FastAPI backend; Node.js for verification scripts; future Operator Dashboard uses Next.js/TypeScript.
- Package manager: Python tooling not established yet; Node package manager not established yet.
- Primary source directory: none yet; future backend likely src/ or app/.
- Primary test directory: none yet.
- Project memory: docs/ and tasks.md.
- Context source: docs/context/.
- Current goal: Step 2 PoC, Gemini API four-party negotiation convergence test.
- Verification command: node scripts/verify.mjs.
- Secret template: .env.example.
- Runtime secret file: .env, ignored and read-denied for Claude.

## Directory Map
| Path | Purpose | Edit Frequency | Notes |
|---|---|---|---|
| docs/context/ | Source context imported before pm-zero initialization | low | Initial context documents, already committed |
| docs/vision.md | Product north star | medium | Product intent only |
| docs/state.md | Current pointer and lock | medium | No task facts beyond active pointer |
| docs/decisions.md | Permanent rationale | medium | Add durable decisions after T005 |
| docs/issues.md | Failure and escalation log | low | Empty until failures occur |
| scripts/ | Automation | medium | verify.mjs is the current entry point |
| future backend | FastAPI application and Gemini negotiation PoC | high | Python is the backend default |
| future dashboard | Operator Dashboard | medium | Next.js/TypeScript is the UI default |
| .claude/ | Claude project settings | low | Minimal .env read deny |

## Entry Points
| Area | File | Purpose |
|---|---|---|
| Agent rules | AGENTS.md | Shared execution rules and Admith safety rules |
| Claude adapter | CLAUDE.md | Imports AGENTS.md |
| Task ledger | tasks.md | Step 2 PoC work breakdown |
| Verification | scripts/verify.mjs | Minimal repository checks |

## Common Workflows
| Workflow | Read First | Edit Usually | Verify |
|---|---|---|---|
| Plan next PoC task | docs/vision.md, tasks.md | tasks.md, docs/state.md | node scripts/verify.mjs |
| Record decision | docs/decisions.md | docs/decisions.md | git diff --check |
| Add source code | docs/repo-map.md Summary | future src/ or experiments/ | targeted test plus node scripts/verify.mjs |

## Generated / External Files
| Path | Rule |
|---|---|
| node_modules/ | ignored dependency output |
| dist/ | ignored build output |
| build/ | ignored build output |
| __pycache__/ | ignored Python cache |
| *.pyc | ignored Python bytecode |
| .env, .env.* | ignored secrets; do not read |

## Update Rules
- Keep Summary under 20 lines.
- Keep each directory note concrete.
- Move rationale to docs/decisions.md.
