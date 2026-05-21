from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from admith.adapters.repositories import (
    InMemoryAuditEventRepository,
    InMemoryNegotiationRepository,
    InMemoryResourceRepository,
)
from admith.config import ensure_demo_runtime_allowed
from admith.domain.approval import ApprovalWorkflow
from admith.domain.models import (
    Agent,
    AgentMandate,
    FoodWasteScenario,
    KybStatus,
    NegotiationState,
    OwnerEntity,
    Resource,
    ResourceUse,
)
from admith.domain.orchestrator import NegotiationOrchestrator
from admith.domain.settlement import SettlementService

ensure_demo_runtime_allowed("admith.api.runtime")

resources = InMemoryResourceRepository()
negotiations = InMemoryNegotiationRepository()
audits = InMemoryAuditEventRepository()
agents: dict[UUID, Agent] = {}
owners: dict[UUID, OwnerEntity] = {}
agreements: dict[UUID, object] = {}
approval_requests: dict[UUID, object] = {}
approval_decisions: list[object] = []
mandate_recommendations: list[object] = []
feedback_records: list[dict[str, object]] = []
orchestrator = NegotiationOrchestrator()
approval_workflow = ApprovalWorkflow()
settlement_service = SettlementService()


def json_model(model):
    return to_jsonable(model.model_dump(mode="python"))


def to_jsonable(value):
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return str(value)
    return value


def ensure_demo_agent() -> tuple[OwnerEntity, Agent]:
    if agents:
        agent = next(iter(agents.values()))
        return owners[agent.owner_entity_id], agent
    owner = OwnerEntity(legal_name="Admith Demo Owner", kyb_status=KybStatus.VERIFIED)
    agent = Agent(owner_entity_id=owner.owner_entity_id, domain_capabilities={"domains": ["food_waste"], "max_quantity_kg": 5000})
    owners[owner.owner_entity_id] = owner
    agents[agent.agent_id] = agent
    return owner, agent


def default_mandate(agent: Agent, owner: OwnerEntity) -> AgentMandate:
    return AgentMandate(
        agent_id=agent.agent_id,
        owner_entity_id=owner.owner_entity_id,
        allowed_object_types=["FoodWasteResource", "AgreementDoc"],
        allowed_actions=["CreateCFP", "SubmitProposal", "FormAgreement", "RequestApproval", "ApproveAgreement", "SignAgreement", "SettleDeal"],
        allowed_regions=["tokyo"],
        property_markings=["phase0_food_waste", "kyb_only", "commercial_sensitive"],
        propagation_markings=["phase0_food_waste", "kyb_only"],
        max_amount_per_deal=Decimal("1000000"),
        max_amount_per_day=Decimal("5000000"),
        max_quantity_per_deal=Decimal("5000"),
    )


def scenario_from_resource(resource: Resource, buyer_max_price: int) -> FoodWasteScenario:
    return FoodWasteScenario(
        lot_id=str(resource.resource_id),
        material=resource.resource_type,
        quantity_kg=int(resource.attributes["quantity_kg"]),
        seller_disposal_cost_yen=int(resource.attributes["disposal_cost_yen"]),
        buyer_alternative_cost_yen_per_kg=38,
        buyer_max_price_yen_per_kg=buyer_max_price,
        logistics_base_fee_yen=12000,
        logistics_yen_per_kg=4,
        required_use=ResourceUse(resource.attributes.get("required_use", "feed")),
        contamination_risk=str(resource.attributes.get("contamination_risk", "low")),
        carrier_has_waste_permit=True,
        manifest_supported=True,
    )


def active_negotiations_count() -> int:
    terminal = {NegotiationState.SETTLED, NegotiationState.FAILED, NegotiationState.EXPIRED}
    return len([item for item in negotiations.items.values() if item.state not in terminal])
