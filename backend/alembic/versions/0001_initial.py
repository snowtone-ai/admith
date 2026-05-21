from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table(
        "owner_entities",
        sa.Column("owner_entity_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("entity_type", sa.String(32), nullable=False),
        sa.Column("legal_name", sa.String(255), nullable=False),
        sa.Column("corporate_number", sa.String(32)),
        sa.Column("kyb_status", sa.String(32), nullable=False),
        sa.Column("kyb_verified_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "agents",
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("owner_entity_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("owner_entities.owner_entity_id")),
        sa.Column("agent_type", sa.String(32), nullable=False),
        sa.Column("public_key", sa.LargeBinary, nullable=False),
        sa.Column("domain_capabilities", postgresql.JSONB, nullable=False),
        sa.Column("policy", postgresql.JSONB, nullable=False),
        sa.Column("trust_score", sa.Numeric(5, 4), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "resources",
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("owner_agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("agents.agent_id")),
        sa.Column("domain_id", sa.String(64), nullable=False),
        sa.Column("resource_type", sa.String(128), nullable=False),
        sa.Column("attributes", postgresql.JSONB, nullable=False),
        sa.Column("ontology_version", sa.String(64), nullable=False),
        sa.Column("security_markings", postgresql.JSONB, nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("lock_token", postgresql.UUID(as_uuid=True)),
        sa.Column("locked_by_negotiation_id", postgresql.UUID(as_uuid=True)),
        sa.Column("locked_until", sa.DateTime(timezone=True)),
        sa.Column("ttl_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reservation_price", sa.Numeric, nullable=False),
        sa.Column("location", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "negotiations",
        sa.Column("negotiation_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("initiator_agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("agents.agent_id")),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("resources.resource_id")),
        sa.Column("state", sa.String(64), nullable=False),
        sa.Column("protocol_version", sa.String(64), nullable=False),
        sa.Column("tier", sa.Integer, nullable=False),
        sa.Column("matching_ttl_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("negotiation_ttl_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("approval_ttl_until", sa.DateTime(timezone=True)),
        sa.Column("pickup_deadline", sa.DateTime(timezone=True)),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
        sa.Column("domain_id", sa.String(64), nullable=False),
        sa.Column("estimated_delta", sa.Numeric, nullable=False),
        sa.Column("final_delta", sa.Numeric),
    )
    op.create_table(
        "audit_events",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("negotiation_id", postgresql.UUID(as_uuid=True)),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True)),
        sa.Column("action_id", postgresql.UUID(as_uuid=True)),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("event_data", postgresql.JSONB, nullable=False),
        sa.Column("sequence_number", sa.Integer, nullable=False),
        sa.Column("previous_hash", sa.LargeBinary, nullable=False),
        sa.Column("hash_algorithm", sa.String(64), nullable=False),
        sa.Column("event_hash", sa.LargeBinary, nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )
    op.execute(
        """
        CREATE OR REPLACE FUNCTION prevent_audit_event_mutation() RETURNS trigger AS $$
        BEGIN RAISE EXCEPTION 'audit_events is append-only'; END;
        $$ LANGUAGE plpgsql
        """
    )
    op.execute(
        """
        CREATE TRIGGER audit_events_no_update BEFORE UPDATE OR DELETE ON audit_events
        FOR EACH ROW EXECUTE FUNCTION prevent_audit_event_mutation()
        """
    )


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("negotiations")
    op.drop_table("resources")
    op.drop_table("agents")
    op.drop_table("owner_entities")
