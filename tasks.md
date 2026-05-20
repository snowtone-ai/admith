# tasks.md -- pm-zero v9.4 Execution Ledger

## Goal Binding
- Vision source: docs/vision.md
- Active goal: Step 2 PoC（Gemini APIで4者間交渉の収束テスト）
- Planning owner: Claude Code
- Implementation owner: Codex CLI
- Review owner: Claude Code

## Status Vocabulary
- proposed: idea exists, not ready
- ready: owner, dependencies, write scope, acceptance, verification, and expected evidence are clear
- doing: one owner is actively working
- blocked: needs decision, dependency, credential, environment, or human action
- review: implementation complete, review pending
- done: accepted by reviewer
- verified: evidence recorded

## Parallelization Rules
- Coordinator owns tasks.md.
- Worker agents own only their assigned Write Scope.
- Parallel implementation requires disjoint Write Scopes or isolated worktrees.
- If two tasks need the same file, serialize them.
- Subagents return reports; coordinator updates tasks.md.

## Tasks
| ID | Status | Owner | Depends On | Write Scope | Acceptance | Verification | Evidence |
|---|---|---|---|---|---|---|---|
| T001 | ready | Codex CLI | none | .env.example, scripts/**, future Python PoC config docs | Gemini API key loading path is documented; authentication can be smoke-tested without exposing secrets | node scripts/verify.mjs plus a safe auth smoke command once implementation exists | pending |
| T002 | ready | Codex CLI | T001 | future Python PoC source for Variant A, related tests/docs | Variant A implements Rule Engine + structured CNP negotiation; LLM never determines price, constraints, or agreement validity | run Variant A sample scenario and record convergence, delta, and cost | pending |
| T003 | ready | Codex CLI | T001 | future Python PoC source for Variant B, related tests/docs | Variant B implements pure LLM natural-language negotiation baseline with identical scenario inputs | run Variant B sample scenario and record convergence, consistency, and cost | pending |
| T004 | ready | Codex CLI | T002, T003 | future benchmark scripts/results docs | Both variants are executed on comparable scenarios; success rate, price consistency, latency, and API cost are compared | run comparison command and save summarized results | pending |
| T005 | ready | Claude Code | T004 | docs/decisions.md, tasks.md, docs/state.md | Results and Go/No-Go implications are recorded as durable decisions; task evidence is updated | git diff --check and node scripts/verify.mjs | pending |

## Blockers
| ID | Task | Blocker | Needed decision | Owner |
|---|---|---|---|---|

## Review Notes
| Task | Reviewer | Result | Follow-up |
|---|---|---|---|
