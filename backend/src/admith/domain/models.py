from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class NegotiationState(StrEnum):
    RESOURCE_AVAILABLE = "resource_available"
    CFP_OPEN = "cfp_open"
    NEGOTIATING = "negotiating"
    DRAFT_AGREEMENT = "draft_agreement"
    PENDING_HUMAN_APPROVAL = "pending_human_approval"
    SIGNING = "signing"
    SETTLED = "settled"
    FAILED = "failed"
    EXPIRED = "expired"


class ActionName(StrEnum):
    CREATE_CFP = "CreateCFP"
    SUBMIT_PROPOSAL = "SubmitProposal"
    COUNTER_OFFER = "CounterOffer"
    FORM_AGREEMENT = "FormAgreement"
    REQUEST_APPROVAL = "RequestApproval"
    APPROVE_AGREEMENT = "ApproveAgreement"
    REJECT_AGREEMENT = "RejectAgreement"
    SIGN_AGREEMENT = "SignAgreement"
    SETTLE_DEAL = "SettleDeal"
    FAIL_NEGOTIATION = "FailNegotiation"
    EXPIRE_NEGOTIATION = "ExpireNegotiation"


class MessageType(StrEnum):
    CFP = "cfp"
    PROPOSAL = "proposal"
    COUNTER = "counter"
    ACCEPT = "accept"
    REJECT = "reject"
    INFORM = "inform"
    CANCEL = "cancel"


class ResourceUse(StrEnum):
    FEED = "feed"
    FERTILIZER = "fertilizer"
    UPCYCLE = "upcycle"


class KybStatus(StrEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class AgentType(StrEnum):
    AUTONOMOUS = "autonomous"
    HUMAN_IN_LOOP = "human_in_loop"
    MEDIATOR = "mediator"


class ApprovalDecisionValue(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    EDIT = "edit"
    ESCALATE = "escalate"


class AgentPolicy(BaseModel):
    objective: str = "maximize_total_delta_with_compliance"
    constraints: list[str] = Field(default_factory=list)
    strategy: str = "cooperative"
    human_approval_threshold: Decimal | None = None
    model_tier: int = 1


class OwnerEntity(BaseModel):
    owner_entity_id: UUID = Field(default_factory=uuid4)
    entity_type: str = "corporation"
    legal_name: str
    corporate_number: str | None = None
    kyb_status: KybStatus = KybStatus.PENDING
    kyb_verified_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Agent(BaseModel):
    agent_id: UUID = Field(default_factory=uuid4)
    owner_entity_id: UUID
    agent_type: AgentType = AgentType.AUTONOMOUS
    public_key: bytes = b"phase0-demo-key"
    domain_capabilities: dict[str, Any] = Field(default_factory=dict)
    policy: AgentPolicy = Field(default_factory=AgentPolicy)
    trust_score: Decimal = Decimal("0.3")
    status: str = "active"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AgentMandate(BaseModel):
    mandate_id: UUID = Field(default_factory=uuid4)
    agent_id: UUID
    owner_entity_id: UUID
    scope: dict[str, Any] = Field(default_factory=dict)
    allowed_object_types: list[str] = Field(default_factory=list)
    allowed_actions: list[ActionName] = Field(default_factory=list)
    allowed_regions: list[str] = Field(default_factory=list)
    property_markings: list[str] = Field(default_factory=list)
    propagation_markings: list[str] = Field(default_factory=list)
    max_amount_per_deal: Decimal = Decimal("0")
    max_amount_per_day: Decimal = Decimal("0")
    max_quantity_per_deal: Decimal | None = None
    currency: str = "JPY"
    allowed_counterparties: list[UUID] | None = None
    approval_mode: str = "approve_all"
    approval_threshold: Decimal | None = None
    valid_from: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=365))
    version: int = 1
    revoked_at: datetime | None = None
    revoked_reason: str | None = None
    mandate_signature: bytes = b"phase0-signature"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Resource(BaseModel):
    resource_id: UUID = Field(default_factory=uuid4)
    owner_agent_id: UUID
    domain_id: str = "food_waste"
    resource_type: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    ontology_version: str = "resource-envelope.v1"
    security_markings: list[str] = Field(default_factory=lambda: ["phase0_food_waste", "kyb_only"])
    state: str = "available"
    lock_token: UUID | None = None
    locked_by_negotiation_id: UUID | None = None
    locked_until: datetime | None = None
    ttl_until: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=24))
    reservation_price: Decimal = Decimal("0")
    location: str = "POINT(139.767 35.681)"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Negotiation(BaseModel):
    negotiation_id: UUID = Field(default_factory=uuid4)
    initiator_agent_id: UUID
    resource_id: UUID
    state: NegotiationState = NegotiationState.CFP_OPEN
    protocol_version: str = "cnp.phase0.v1"
    tier: int = 1
    matching_ttl_until: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(seconds=30))
    negotiation_ttl_until: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(minutes=5))
    approval_ttl_until: datetime | None = None
    pickup_deadline: datetime | None = None
    settlement_ttl_until: datetime | None = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
    domain_id: str = "food_waste"
    estimated_delta: Decimal = Decimal("0")
    final_delta: Decimal | None = None


class NegotiationParticipant(BaseModel):
    negotiation_id: UUID
    agent_id: UUID
    role: str
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    left_at: datetime | None = None
    final_status: str | None = None


class Message(BaseModel):
    message_id: UUID = Field(default_factory=uuid4)
    negotiation_id: UUID
    from_agent_id: UUID
    to_agent_id: UUID | None = None
    message_type: MessageType
    payload: dict[str, Any]
    signature: bytes = b"phase0-signature"
    nonce: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sequence_number: int = 1
    parent_message_id: UUID | None = None


class Agreement(BaseModel):
    agreement_id: UUID = Field(default_factory=uuid4)
    negotiation_id: UUID | None = None
    terms: dict[str, Any]
    parties: dict[str, Any] = Field(default_factory=dict)
    signatures: dict[str, Any] = Field(default_factory=dict)
    state: str = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    settled_at: datetime | None = None
    audit_hash: bytes = b""


class ApprovalRequest(BaseModel):
    approval_id: UUID = Field(default_factory=uuid4)
    negotiation_id: UUID
    agreement_id: UUID | None = None
    owner_entity_id: UUID
    required_role: str = "operator"
    status: str = "pending"
    displayed_terms_hash: bytes = b""
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ApprovalDecision(BaseModel):
    approval_id: UUID
    approver_user_id: UUID = Field(default_factory=uuid4)
    decision: ApprovalDecisionValue
    reason: str | None = None
    displayed_terms_hash: bytes
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    negotiation_id: UUID | None = None
    agent_id: UUID | None = None
    action_id: UUID | None = None
    event_type: str
    event_data: dict[str, Any]
    sequence_number: int
    previous_hash: bytes = b""
    hash_algorithm: str = "sha256-canonical-json-v1"
    event_hash: bytes = b""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TrustScoreHistory(BaseModel):
    agent_id: UUID
    score: Decimal
    calculation_method: str
    input_signals: dict[str, Any] = Field(default_factory=dict)
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PriceSignalHistory(BaseModel):
    price_signal_id: UUID = Field(default_factory=uuid4)
    domain_id: str
    resource_type: str
    region: str
    unit_price_yen: Decimal
    quantity_kg: Decimal
    agreement_id: UUID
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MandateAdjustmentRecommendation(BaseModel):
    recommendation_id: UUID = Field(default_factory=uuid4)
    agent_id: UUID
    owner_entity_id: UUID
    approval_rate: Decimal
    reject_reasons: list[str] = Field(default_factory=list)
    recommended_change: dict[str, Any] = Field(default_factory=dict)
    status: str = "proposed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MatchingOutcomeMetric(BaseModel):
    metric_id: UUID = Field(default_factory=uuid4)
    domain_id: str
    matching_policy: str
    candidate_count: int
    negotiation_id: UUID
    outcome: str
    elapsed_seconds: Decimal
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class FoodWasteScenario:
    lot_id: str
    material: str
    quantity_kg: int
    seller_disposal_cost_yen: int
    buyer_alternative_cost_yen_per_kg: int
    buyer_max_price_yen_per_kg: int
    logistics_base_fee_yen: int
    logistics_yen_per_kg: int
    required_use: ResourceUse
    contamination_risk: str
    carrier_has_waste_permit: bool
    manifest_supported: bool
    viable_uses: tuple[ResourceUse, ...] = (ResourceUse.FEED, ResourceUse.FERTILIZER, ResourceUse.UPCYCLE)
    carrier_permit_scope: tuple[str, ...] = ("food_waste",)
    consignment_contract_ready: bool = True
    producer_responsibility_ack: bool = True
    resource_envelope_version: str = "resource-envelope.v1"
    ontology_markings: tuple[str, ...] = ("phase0_food_waste", "kyb_only")
