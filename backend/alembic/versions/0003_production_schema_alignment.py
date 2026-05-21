from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0003_production_schema_alignment"
down_revision = "0002_remaining_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("negotiations", sa.Column("settlement_ttl_until", sa.DateTime(timezone=True)))
    op.add_column("agent_mandates", sa.Column("max_amount_per_deal", sa.Numeric(), nullable=False, server_default="0"))
    op.add_column("agent_mandates", sa.Column("max_amount_per_day", sa.Numeric(), nullable=False, server_default="0"))
    op.add_column("agent_mandates", sa.Column("max_quantity_per_deal", sa.Numeric()))
    op.add_column("agent_mandates", sa.Column("currency", sa.String(8), nullable=False, server_default="JPY"))
    op.add_column("agent_mandates", sa.Column("allowed_counterparties", postgresql.JSONB()))
    op.add_column("agent_mandates", sa.Column("approval_threshold", sa.Numeric()))
    op.add_column("agent_mandates", sa.Column("revoked_at", sa.DateTime(timezone=True)))
    op.add_column("agent_mandates", sa.Column("revoked_reason", sa.String(1024)))
    op.add_column("agent_mandates", sa.Column("mandate_signature", sa.LargeBinary()))
    op.alter_column("agent_mandates", "limits", nullable=True)
    op.create_unique_constraint("uq_agreements_negotiation_id", "agreements", ["negotiation_id"])
    op.create_unique_constraint("uq_audit_events_sequence_number", "audit_events", ["sequence_number"])
    op.create_index("ix_resources_state", "resources", ["state"])
    op.create_index("ix_resources_locked_until", "resources", ["locked_until"])
    op.create_index("ix_negotiations_state", "negotiations", ["state"])
    op.create_index("ix_audit_events_negotiation_sequence", "audit_events", ["negotiation_id", "sequence_number"])


def downgrade() -> None:
    op.drop_index("ix_audit_events_negotiation_sequence", table_name="audit_events")
    op.drop_index("ix_negotiations_state", table_name="negotiations")
    op.drop_index("ix_resources_locked_until", table_name="resources")
    op.drop_index("ix_resources_state", table_name="resources")
    op.drop_constraint("uq_audit_events_sequence_number", "audit_events", type_="unique")
    op.drop_constraint("uq_agreements_negotiation_id", "agreements", type_="unique")
    op.execute("UPDATE agent_mandates SET limits = '{}'::jsonb WHERE limits IS NULL")
    op.alter_column("agent_mandates", "limits", nullable=False)
    for column in (
        "mandate_signature",
        "revoked_reason",
        "revoked_at",
        "approval_threshold",
        "allowed_counterparties",
        "currency",
        "max_quantity_per_deal",
        "max_amount_per_day",
        "max_amount_per_deal",
    ):
        op.drop_column("agent_mandates", column)
    op.drop_column("negotiations", "settlement_ttl_until")
