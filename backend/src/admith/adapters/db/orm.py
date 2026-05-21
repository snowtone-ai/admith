from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from geoalchemy2 import Geography
from sqlalchemy import DateTime, ForeignKey, Integer, LargeBinary, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class OwnerEntityRow(Base):
    __tablename__ = "owner_entities"
    owner_entity_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(32))
    legal_name: Mapped[str] = mapped_column(String(255))
    corporate_number: Mapped[str | None] = mapped_column(String(32))
    kyb_status: Mapped[str] = mapped_column(String(32))
    kyb_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AgentRow(Base):
    __tablename__ = "agents"
    agent_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    owner_entity_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("owner_entities.owner_entity_id"))
    agent_type: Mapped[str] = mapped_column(String(32))
    public_key: Mapped[bytes] = mapped_column(LargeBinary)
    domain_capabilities: Mapped[dict] = mapped_column(JSONB)
    policy: Mapped[dict] = mapped_column(JSONB)
    trust_score: Mapped[Decimal] = mapped_column(Numeric(5, 4))
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ResourceRow(Base):
    __tablename__ = "resources"
    resource_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    owner_agent_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agents.agent_id"))
    domain_id: Mapped[str] = mapped_column(String(64))
    resource_type: Mapped[str] = mapped_column(String(128))
    attributes: Mapped[dict] = mapped_column(JSONB)
    ontology_version: Mapped[str] = mapped_column(String(64))
    security_markings: Mapped[list] = mapped_column(JSONB)
    state: Mapped[str] = mapped_column(String(32))
    lock_token: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    locked_by_negotiation_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ttl_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reservation_price: Mapped[Decimal] = mapped_column(Numeric)
    location: Mapped[str] = mapped_column(Geography(geometry_type="POINT", srid=4326))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class NegotiationRow(Base):
    __tablename__ = "negotiations"
    negotiation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    initiator_agent_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agents.agent_id"))
    resource_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("resources.resource_id"))
    state: Mapped[str] = mapped_column(String(64))
    protocol_version: Mapped[str] = mapped_column(String(64))
    tier: Mapped[int] = mapped_column(Integer)
    matching_ttl_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    negotiation_ttl_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    approval_ttl_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    pickup_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    settlement_ttl_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    domain_id: Mapped[str] = mapped_column(String(64))
    estimated_delta: Mapped[Decimal] = mapped_column(Numeric)
    final_delta: Mapped[Decimal | None] = mapped_column(Numeric)


class AgentMandateRow(Base):
    __tablename__ = "agent_mandates"
    mandate_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    agent_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agents.agent_id"))
    owner_entity_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("owner_entities.owner_entity_id"))
    scope: Mapped[dict] = mapped_column(JSONB)
    allowed_object_types: Mapped[list] = mapped_column(JSONB)
    allowed_actions: Mapped[list] = mapped_column(JSONB)
    allowed_regions: Mapped[list] = mapped_column(JSONB)
    property_markings: Mapped[list] = mapped_column(JSONB)
    propagation_markings: Mapped[list] = mapped_column(JSONB)
    max_amount_per_deal: Mapped[Decimal] = mapped_column(Numeric)
    max_amount_per_day: Mapped[Decimal] = mapped_column(Numeric)
    max_quantity_per_deal: Mapped[Decimal | None] = mapped_column(Numeric)
    currency: Mapped[str] = mapped_column(String(8))
    allowed_counterparties: Mapped[list | None] = mapped_column(JSONB)
    approval_mode: Mapped[str] = mapped_column(String(32))
    approval_threshold: Mapped[Decimal | None] = mapped_column(Numeric)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    version: Mapped[int] = mapped_column(Integer)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_reason: Mapped[str | None] = mapped_column(String(1024))
    mandate_signature: Mapped[bytes | None] = mapped_column(LargeBinary)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class NegotiationParticipantRow(Base):
    __tablename__ = "negotiation_participants"
    negotiation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("negotiations.negotiation_id"), primary_key=True)
    agent_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agents.agent_id"), primary_key=True)
    role: Mapped[str] = mapped_column(String(32))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    final_status: Mapped[str | None] = mapped_column(String(32))


class MessageRow(Base):
    __tablename__ = "messages"
    message_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    negotiation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("negotiations.negotiation_id"))
    from_agent_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agents.agent_id"))
    to_agent_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    message_type: Mapped[str] = mapped_column(String(32))
    payload: Mapped[dict] = mapped_column(JSONB)
    signature: Mapped[bytes] = mapped_column(LargeBinary)
    nonce: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sequence_number: Mapped[int] = mapped_column(Integer)
    parent_message_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))


class AgreementRow(Base):
    __tablename__ = "agreements"
    __table_args__ = (UniqueConstraint("negotiation_id", name="uq_agreements_negotiation_id"),)
    agreement_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    negotiation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("negotiations.negotiation_id"))
    terms: Mapped[dict] = mapped_column(JSONB)
    parties: Mapped[dict] = mapped_column(JSONB)
    signatures: Mapped[dict] = mapped_column(JSONB)
    state: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    settled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    audit_hash: Mapped[bytes] = mapped_column(LargeBinary)


class ApprovalRequestRow(Base):
    __tablename__ = "approval_requests"
    approval_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    negotiation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("negotiations.negotiation_id"))
    agreement_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agreements.agreement_id"))
    owner_entity_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("owner_entities.owner_entity_id"))
    required_role: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32))
    displayed_terms_hash: Mapped[bytes] = mapped_column(LargeBinary)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ApprovalDecisionRow(Base):
    __tablename__ = "approval_decisions"
    approval_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("approval_requests.approval_id"), primary_key=True)
    approver_user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True))
    decision: Mapped[str] = mapped_column(String(32))
    reason: Mapped[str | None] = mapped_column(String(1024))
    displayed_terms_hash: Mapped[bytes] = mapped_column(LargeBinary)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AuditEventRow(Base):
    __tablename__ = "audit_events"
    event_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    negotiation_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    agent_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    action_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    event_type: Mapped[str] = mapped_column(String(128))
    event_data: Mapped[dict] = mapped_column(JSONB)
    sequence_number: Mapped[int] = mapped_column(Integer)
    previous_hash: Mapped[bytes] = mapped_column(LargeBinary)
    hash_algorithm: Mapped[str] = mapped_column(String(64))
    event_hash: Mapped[bytes] = mapped_column(LargeBinary)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TrustScoreHistoryRow(Base):
    __tablename__ = "trust_score_history"
    agent_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agents.agent_id"), primary_key=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    score: Mapped[Decimal] = mapped_column(Numeric(5, 4))
    calculation_method: Mapped[str] = mapped_column(String(64))
    input_signals: Mapped[dict] = mapped_column(JSONB)


class PriceSignalHistoryRow(Base):
    __tablename__ = "price_signal_history"
    price_signal_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    domain_id: Mapped[str] = mapped_column(String(64))
    resource_type: Mapped[str] = mapped_column(String(128))
    region: Mapped[str] = mapped_column(String(64))
    unit_price_yen: Mapped[Decimal] = mapped_column(Numeric)
    quantity_kg: Mapped[Decimal] = mapped_column(Numeric)
    agreement_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agreements.agreement_id"))
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class MandateAdjustmentRecommendationRow(Base):
    __tablename__ = "mandate_adjustment_recommendations"
    recommendation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    agent_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("agents.agent_id"))
    owner_entity_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("owner_entities.owner_entity_id"))
    approval_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4))
    reject_reasons: Mapped[list] = mapped_column(JSONB)
    recommended_change: Mapped[dict] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class MatchingOutcomeMetricRow(Base):
    __tablename__ = "matching_outcome_metrics"
    metric_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    domain_id: Mapped[str] = mapped_column(String(64))
    matching_policy: Mapped[str] = mapped_column(String(64))
    candidate_count: Mapped[int] = mapped_column(Integer)
    negotiation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("negotiations.negotiation_id"))
    outcome: Mapped[str] = mapped_column(String(32))
    elapsed_seconds: Mapped[Decimal] = mapped_column(Numeric)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
