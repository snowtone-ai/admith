from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from admith.domain.models import AgentType, ResourceUse


class ResourceCreate(BaseModel):
    material: str = Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9 _-]+$")
    quantity_kg: int = Field(gt=0, le=100_000)
    disposal_cost_yen: int = Field(ge=0, le=100_000_000)
    required_use: ResourceUse = ResourceUse.FEED
    location: str = Field(default="POINT(139.767 35.681)", max_length=128, pattern=r"^POINT\(-?\d+(\.\d+)? -?\d+(\.\d+)?\)$")


class NegotiationCreate(BaseModel):
    resource_id: UUID
    buyer_max_price_yen_per_kg: int = Field(default=18, ge=0, le=100_000)


class AgentCreate(BaseModel):
    legal_name: str = Field(min_length=1, max_length=120)
    agent_type: AgentType = AgentType.AUTONOMOUS
    max_quantity_kg: int = Field(default=2000, gt=0, le=100_000)


class DecisionRequest(BaseModel):
    reason: str | None = Field(default=None, max_length=1000)
    displayed_terms_hash: str | None = Field(default=None, pattern=r"^[0-9a-fA-F]{64}$")
