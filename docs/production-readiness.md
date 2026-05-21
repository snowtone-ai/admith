# production-readiness.md

## Scope
Step 4の目的は、Step 3 MVPのdemo-only要素を本番運用可能な構成へ置き換えること。本書はREADMEに明記された本番前リスクをRelease Gateへ変換した実行基準である。

## Current Production Blockers
| ID | Risk | Current State | Release Gate | Owner |
|---|---|---|---|---|
| PR1 | in-memory runtime | `admith.api.runtime` がmodule global in-memory storeを持つ | G0: production profileでin-memory runtimeを起動不能にし、DB repositoryへ切替 | Codex CLI |
| PR2 | organization user auth | 単一`API_KEY`によるOperator認証 | G1: OIDC/JWT, organization, membership, invite, service accountを強制 | Codex CLI + Human IdP decision |
| PR3 | KYB operations | demo ownerは自動verified | G2: KYB verified前の取引操作を全拒否し、証跡を保存 | Codex CLI + Legal/Ops |
| PR4 | permissions | API keyが全権限 | G3: RBAC/ABAC, MandateScope, OntologyView, DB tenant guardを統合 | Codex CLI |
| PR5 | external contract/manifest | `econtract_stub.py` / `manifest_stub.py` がUUIDのみ返す | G4: sandbox/prod adapter, webhook署名検証, idempotency, DLQ, audit | Codex CLI + Legal/Ops |
| PR6 | secrets and operations | local Docker demo中心 | G6: secret rotation, observability, backup/restore, incident runbook, SLO | Platform + Codex CLI |
| PR7 | security review | local tests中心 | G7: SAST/DAST/dependency/container/IaC scan and cross-vendor review | Independent reviewer |

## Release Gates
| Gate | Required Evidence |
|---|---|
| G0 DB | production import graphにin-memory repositoryなし。DB migration, repository contract tests, concurrent lock testsが通過。 |
| G1 Auth | invalid token matrix, JWKS rotation, org membership, invite-only onboarding testsが通過。 |
| G2 KYB | pending/rejected ownerがresource/negotiation/approval/settlement/external actionで403になる。 |
| G3 Authorization | IDOR tests、role matrix tests、DB tenant guard testsが通過。 |
| G4 External | e-contract/manifest sandbox E2E、webhook signature tests、idempotency tests、DLQ testsが通過。 |
| G5 Compliance | Legal/Ops sign-off。未解決HIGHなし。accepted residual riskを明記。 |
| G6 Operations | backup/restore check、redacted structured logs、metrics、rate limit、rollback rehearsalの証跡。 |
| G7 Security | HIGH/CRITICAL findingsゼロ。修正差分と再検証ログ。 |
| G8 Evidence | `release-evidence/` に全Gateの検証結果、既知リスク、rollback手順を保存。 |

## Blocking Decisions
| ID | Required Decision | Blocks |
|---|---|---|
| BD1 | OIDC/IdP provider and tenant model | T220-T224 |
| BD2 | KYB provider or internal KYB SOP | T230-T234 |
| BD3 | 電子契約provider | T250/T252/T254/T255 |
| BD4 | 電子マニフェスト接続方式 | T250/T253/T254/T255 |
| BD5 | Production hosting and data residency | T260-T265 |

## Residual Risk Policy
- HIGH/Critical riskは、human owner、期限、暫定緩和策、Go/No-Go判断がない限りrelease不可。
- 法務・KYB・電子契約・電子マニフェスト・本番hostingは人間の運用/契約判断なしに完了扱いにしない。
- Demo profileの存在は許容するが、production profileから到達不能であることを検証する。
- 人間が完了すべき本番準備作業は `docs/production-human-actions.md` を正とする。
