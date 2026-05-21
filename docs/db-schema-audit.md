# db-schema-audit.md

## Scope
T210 audits the alignment between Pydantic domain models, SQLAlchemy ORM rows, and Alembic migrations for the Step 4 production database path.

## Findings Fixed
| Area | Gap | Fix |
|---|---|---|
| AgentMandate | Dynamic Security and approval delegation fields existed in Pydantic but were collapsed into `limits` or absent in ORM/migration. | Added explicit columns for amount/quantity limits, currency, counterparties, approval threshold, revocation metadata, and mandate signature. `limits` is now legacy compatibility-only and nullable; explicit columns are the source of truth. |
| AgentMandate signature | `mandate_signature` defaulted to empty bytea, which could hide unsigned Phase 0 rows as if signed. | Made `mandate_signature` nullable in the production alignment migration; real signature enforcement belongs to the external signing/KYB workflow. |
| Negotiation | `settlement_ttl_until` existed in Pydantic but not ORM/migration. | Added nullable `settlement_ttl_until` column. |
| Agreement | Design requires one Agreement per Negotiation, but ORM/migration lacked an explicit uniqueness constraint. | Added `uq_agreements_negotiation_id`. |
| Operational indexes | Lock/state/audit lookup paths lacked explicit production indexes. | Added state, locked_until, negotiation state, and audit negotiation/sequence indexes. |
| Audit sequence | `MAX(sequence_number)+1` could race under concurrent transactions. | Added DB uniqueness for global `sequence_number` and advisory transaction locking in the SQLAlchemy repository append path. |

## Remaining Verification
- `alembic upgrade head` still requires a running PostgreSQL/PostGIS database.
- Full DB repository contract tests are tracked by T211.
- Production import graph cutover from in-memory runtime is tracked by T212-T215.
