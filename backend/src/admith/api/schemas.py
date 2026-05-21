from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from admith.domain.models import AgentType, ResourceUse


class ResourceCreate(BaseModel):
    material: str
    quantity_kg: int
    disposal_cost_yen: int
    required_use: ResourceUse = ResourceUse.FEED
    location: str = "POINT(139.767 35.681)"


class NegotiationCreate(BaseModel):
    resource_id: UUID
    buyer_max_price_yen_per_kg: int = 18


class AgentCreate(BaseModel):
    legal_name: str
    agent_type: AgentType = AgentType.AUTONOMOUS
    max_quantity_kg: int = 2000


class DecisionRequest(BaseModel):
    reason: str | None = None
    displayed_terms_hash: str | None = None
