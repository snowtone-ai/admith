# data-classification.md

## Classification Levels
| Level | Meaning | Examples | Handling |
|---|---|---|---|
| public | 公開可能 | product name, public docs | 通常のGit管理可 |
| internal | 社内限定 | runbooks, architecture notes | repository内管理可 |
| confidential | 取引・営業秘密 | resource attributes, prices, negotiation messages | tenant isolation, least privilege, audit |
| restricted | 法務・KYB・本人意思証跡 | KYB metadata, approval records, contracts, manifests | role restriction, immutable audit, export minimization |
| secret | 認証情報 | API keys, JWT signing secrets, provider credentials | `.env`/secret manager only, logs禁止 |

## Domain Data
| Data | Level | Storage | Notes |
|---|---|---|---|
| OwnerEntity legal_name/corporate_number | restricted | PostgreSQL | KYB and tenant authorization only |
| KYB document body | restricted | external secure storage | DB stores metadata/hash/reference only |
| KYB decision and review event | restricted | PostgreSQL + AuditEvent | reason and reviewer required |
| Resource attributes | confidential | PostgreSQL JSONB | OntologyView filtering required |
| Resource location | confidential | PostGIS | org-scoped queries only |
| Negotiation messages | confidential | PostgreSQL | required for audit and Take-Teki evidence |
| Agreement terms | restricted | PostgreSQL | deterministic Rule Engine output only |
| Approval displayed_terms_hash | restricted | PostgreSQL | tamper detection |
| Contract provider response metadata | restricted | PostgreSQL | payload hash, provider ID, status |
| Manifest provider response metadata | restricted | PostgreSQL | legal evidence and retry state |
| AuditEvent hash chain | restricted | PostgreSQL append-only | no update/delete in production |
| Trust/price/matching feedback | confidential | PostgreSQL | no automatic application before human-approved policy |
| Runtime provider secrets | secret | secret manager / `.env` local only | never commit or log |

## Redaction Rules
- Logs may contain correlation IDs, event IDs, and status values.
- Logs must not contain API keys, JWTs, KYB document contents, full contract payloads, or manifest credential material.
- Audit exports must include enough metadata to prove the sequence without exposing unnecessary personal data.
