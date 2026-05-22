from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any
from uuid import UUID

from admith.adapters.db.session import session_scope
from admith.adapters.repositories import (
    InMemoryAuditEventRepository,
    InMemoryNegotiationRepository,
    InMemoryResourceRepository,
)
from admith.config import get_settings
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


@dataclass
class AppState:
    resources: Any
    negotiations: Any
    audits: Any
    agreements: dict[UUID, object] = field(default_factory=dict)
    approval_requests: dict[UUID, object] = field(default_factory=dict)
    approval_decisions: list[object] = field(default_factory=list)
    mandate_recommendations: list[object] = field(default_factory=list)
    feedback_records: list[dict[str, object]] = field(default_factory=list)
    orchestrator: NegotiationOrchestrator = field(default_factory=NegotiationOrchestrator)
    approval_workflow: ApprovalWorkflow = field(default_factory=ApprovalWorkflow)
    settlement_service: SettlementService = field(default_factory=SettlementService)
    agents: dict[UUID, Agent] = field(default_factory=dict)
    owners: dict[UUID, OwnerEntity] = field(default_factory=dict)

    def active_negotiations_count(self) -> int:
        terminal = {NegotiationState.SETTLED, NegotiationState.FAILED, NegotiationState.EXPIRED}
        return len([item for item in self.negotiations.items.values() if item.state not in terminal])

    def ensure_demo_agent(self) -> tuple[OwnerEntity, Agent]:
        if self.agents:
            agent = next(iter(self.agents.values()))
            return self.owners[agent.owner_entity_id], agent
        owner = OwnerEntity(legal_name="Admith Demo Owner", kyb_status=KybStatus.VERIFIED)
        agent = Agent(owner_entity_id=owner.owner_entity_id, domain_capabilities={"domains": ["food_waste"], "max_quantity_kg": 5000})
        self.owners[owner.owner_entity_id] = owner
        self.agents[agent.agent_id] = agent
        return owner, agent

    def default_mandate(self, agent: Agent, owner: OwnerEntity) -> AgentMandate:
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

    def scenario_from_resource(self, resource: Resource, buyer_max_price: int) -> FoodWasteScenario:
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


_memory_state = AppState(
    resources=InMemoryResourceRepository(),
    negotiations=InMemoryNegotiationRepository(),
    audits=InMemoryAuditEventRepository(),
)


def get_memory_state() -> AppState:
    return _memory_state


class DbRuntime:
    def __init__(self, session) -> None:
        from admith.adapters.db.repositories import (
            SqlAlchemyAuditEventRepository,
            SqlAlchemyNegotiationRepository,
            SqlAlchemyResourceRepository,
        )

        self.session = session
        self.resources = SqlAlchemyResourceRepository(session)
        self.negotiations = SqlAlchemyNegotiationRepository(session)
        self.audits = SqlAlchemyAuditEventRepository(session)

    async def ensure_demo_agent(self) -> tuple[OwnerEntity, Agent]:
        from sqlalchemy import select

        from admith.adapters.db.orm import AgentRow, OwnerEntityRow

        existing = await self.session.execute(select(AgentRow).limit(1))
        row = existing.scalar_one_or_none()
        if row is not None:
            owner_row = await self.session.get(OwnerEntityRow, row.owner_entity_id)
            if owner_row is None:
                raise RuntimeError("agent_owner_not_found")
            return (
                OwnerEntity.model_validate({column.name: getattr(owner_row, column.name) for column in OwnerEntityRow.__table__.columns}),
                Agent.model_validate({column.name: getattr(row, column.name) for column in AgentRow.__table__.columns}),
            )

        owner = OwnerEntity(legal_name="Admith Demo Owner", kyb_status=KybStatus.VERIFIED)
        agent = Agent(owner_entity_id=owner.owner_entity_id, domain_capabilities={"domains": ["food_waste"], "max_quantity_kg": 5000})
        self.session.add(OwnerEntityRow(**owner.model_dump(mode="python")))
        self.session.add(AgentRow(**agent.model_dump(mode="python")))
        await self.session.flush()
        return owner, agent

    async def create_owner_agent(self, owner: OwnerEntity, agent: Agent) -> None:
        from admith.adapters.db.orm import AgentRow, OwnerEntityRow

        self.session.add(OwnerEntityRow(**owner.model_dump(mode="python")))
        self.session.add(AgentRow(**agent.model_dump(mode="python")))
        await self.session.flush()


async def get_state() -> AppState | DbRuntime:
    if get_settings().repository_mode == "database":
        async with session_scope() as session:
            yield DbRuntime(session)
        return
    yield get_memory_state()
