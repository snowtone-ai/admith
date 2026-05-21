# threat-model.md

## Scope
対象はStep 4 production profileのFastAPI backend、Operator Dashboard、PostgreSQL/PostGIS、Redis、KYB、電子契約、電子マニフェスト、監査ログ、運用者操作である。

## Assets
| Asset | Classification | Primary Risk |
|---|---|---|
| Organization/User/Membership | confidential | なりすまし、権限昇格、IDOR |
| OwnerEntity and KYB metadata | restricted | 書類情報漏えい、審査改ざん |
| Resource attributes | confidential | 営業秘密漏えい、品質偽装 |
| Negotiation terms and messages | confidential | 価格操作、改ざん、Replay |
| Approval decisions | restricted | 本人意思・代理権限の否認 |
| Contract and manifest records | restricted | 法定証跡欠落、外部webhook偽装 |
| AuditEvent hash chain | restricted | 改ざん、削除、順序破壊 |
| Runtime secrets | secret | 外部API不正利用、DB侵害 |

## STRIDE Summary
| Threat | Scenario | Required Control | Verification |
|---|---|---|---|
| Spoofing | stolen API key or forged JWT | OIDC/JWT validation, JWKS rotation, MFA-capable IdP, service account scoping | T222 invalid token matrix |
| Tampering | agreement terms altered before approval | displayed_terms_hash, immutable Agreement, AuditEvent hash chain | T130/T274 tests |
| Repudiation | approver denies decision | human approval record, approver identity, reason, timestamp, audit export | T224/T274 |
| Information disclosure | cross-org resource read | org context, RBAC/ABAC, DB tenant guard, OntologyView filtering | T241-T243 |
| Denial of service | lock contention or webhook burst | rate limit, idempotency, backoff, queue/DLQ | T264/T252/T253 |
| Elevation of privilege | operator performs compliance override | role matrix, dual control, audited break-glass | T240/T241/T270 |

## LINDDUN Summary
| Privacy Threat | Scenario | Required Control | Verification |
|---|---|---|---|
| Linkability | KYB documents linked to deal exports unnecessarily | export minimization, document metadata only | T231/T274 |
| Identifiability | personal approver data in general audit views | role-scoped views and redaction | T241/T244/T262 |
| Non-repudiation overreach | excessive retention of operator data | retention policy and legal review | T260/T270 |
| Detectability | tenant existence leaked by IDs | generic 404/403 policy and tenant guard | T241/T242 |
| Disclosure | secrets in logs | structured log redaction | T262 |
| Unawareness | AI/agent action not disclosed | audit timeline and operator UI | T244/T274 |
| Non-compliance | manifest or contract evidence incomplete | provider adapter evidence and legal sign-off | T250-T254/T270 |

## Release Blockers
- Production cannot use in-memory repositories or stub external adapters.
- Auth, DB schema/RLS, external APIs, security, deploy, and 300+ line diffs require independent review.
- BD1-BD5 must be resolved before related blocked phases can be completed.
