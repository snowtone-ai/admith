# Project AGENTS.md -- pm-zero v9.4

## Language
- Completion reports, error reports, and manual confirmation requests: Japanese.
- Code identifiers: English.
- When 3+ HIGH assumptions accumulate, ask immediately.

## Engineering Role
- Act as a principal-level full-stack engineer with distributed systems, AI agent infrastructure, and production-grade Python backend experience.
- Write readable, testable, minimal, correct code that can pass senior engineering review.
- Do not write placeholder code or TODOs. Every committed function must work.

## Thinking Protocol
- Before code changes, decompose the task into atomic subtasks.
- Challenge assumptions from first principles and prefer the simplest correct solution.
- Compare three conceptual implementation skeletons for correctness, simplicity, testability, and cost; choose one explicitly in working notes or reports.
- Use Chain-of-Verification: draft internally, plan failure-revealing checks, verify independently, then revise using only verified facts.
- Do not output long reasoning in one shot. Provide short progress checks.
- Before using an external API or library function, verify the actual call shape or run a minimal test when uncertain.

## Source of Truth
- Product intent: docs/vision.md
- Execution tasks: tasks.md
- Current state: docs/state.md
- Decisions: docs/decisions.md
- Failures: docs/issues.md
- Repository map: docs/repo-map.md
- Report: HANDOFF-JA.md

## Startup Read
- Read this file.
- Read docs/state.md.
- Read docs/decisions.md.
- Read docs/repo-map.md Summary.

## Repository Navigation
- Read detailed repo-map sections only when target files are unclear.
- Update docs/repo-map.md after structural changes.
- Use rg before broad manual browsing.

## Task Ledger Rule
- Planning output goes to tasks.md.
- Implementation starts from tasks marked ready.
- Each ready task includes owner, dependencies, write scope, acceptance, verification, and evidence.
- Coordinator updates tasks.md.
- Worker agents report results to the coordinator.

## Scope Lock Rule
- One coordinator owns tasks.md and docs/state.md.
- Workers edit only their assigned write scope.
- Parallel work requires disjoint write scopes or isolated worktrees.
- Tasks touching the same file are serialized.

## Admith-Specific Safety Rules
- LLMは契約判断に使わない。価格・制約・合意条件は決定論的Rule Engineで確定する。
- Human Final Approvalが完了するまで、署名・資金移動・契約確定処理を実行しない。
- 廃棄物処理法・食品リサイクル法の優先順位ルールはCompliance Rule Engineに従う。
- Phase 0はFood Waste専用。汎用Admith Accord公開API、CVE、Trust Score有料API、マイクロ決済はスコープ外。
- KYB済み・招待制の相手のみを前提にし、Sybil価格操作を構造的に排除する。
- 交渉ログ、見積根拠、条件変更理由は監査可能な形で保存する。

## Quality Standards
- Refer to Quality Gates in pm-zero-knowledge-v9.4 Section 10.
- Keep files and functions small enough to review: target 300 lines per file and 50 lines per function.
- After 3 consecutive identical errors, record in docs/issues.md and pause.
- 300+ line diffs: split or explain in docs/decisions.md.
- Auth, billing, DB schema, RLS/permissions, deploy, security, 300+ line diff, and new external API require cross-vendor review.

## Commands
- install: pnpm install
- lint: pnpm lint
- typecheck: pnpm typecheck
- test: pnpm test
- build: pnpm build
- verify: node scripts/verify.mjs

Use only commands that exist in this repository.

## Execution Boundaries
- Use PowerShell.
- Use standard push with branch tracking.
- Handle every error explicitly.
- Keep safe values only in output.
- Use .env.example as template; runtime reads actual env values.
- Authentication, billing, production deploy final approval, and personal data handling are human tasks.
- All other safe operations are AI-executed.

## Agent Routing
- 計画・設計・レビューはClaude Codeを既定とする。
- 実装はCodex CLIを既定とする。
- Either agent can perform the full workflow when needed.
- Critical changes: review by a model or vendor different from the implementer.
- Auth, billing, DB schema, RLS/permissions, deploy, security, 300+ line diff, and new external API: cross-vendor review required.
