from __future__ import annotations

from decimal import Decimal

import pytest

from admith.domain.models import ActionName, AgentMandate, NegotiationState, Resource
from admith.domain.ontology import ACTION_TRANSITIONS, MandateScope, ResourceOntologyService


def test_mandate_filters_out_disallowed_fields() -> None:
    resource = Resource(owner_agent_id="00000000-0000-0000-0000-000000000001", resource_type="okara", attributes={"material": "okara", "disposal_cost_yen": 25000, "quantity_kg": 1000})
    mandate = AgentMandate(
        agent_id="00000000-0000-0000-0000-000000000001",
        owner_entity_id="00000000-0000-0000-0000-000000000002",
        allowed_object_types=["FoodWasteResource"],
        allowed_actions=["CreateCFP"],
        allowed_regions=["tokyo"],
        property_markings=["phase0_food_waste", "kyb_only"],
        propagation_markings=["phase0_food_waste"],
        max_amount_per_deal=Decimal("100000"),
        max_amount_per_day=Decimal("500000"),
        max_quantity_per_deal=Decimal("2000"),
    )
    view = ResourceOntologyService({resource.resource_id: resource}).build_view(resource.resource_id, mandate)
    assert "material" in view.facts
    assert "disposal_cost_yen" not in view.facts


def test_action_rejects_precondition_violation() -> None:
    resource = Resource(owner_agent_id="00000000-0000-0000-0000-000000000001", resource_type="okara", attributes={"quantity_kg": 1000})
    mandate = AgentMandate(agent_id=resource.owner_agent_id, owner_entity_id="00000000-0000-0000-0000-000000000002", allowed_object_types=["FoodWasteResource"], allowed_actions=["SettleDeal"], allowed_regions=["tokyo"], property_markings=["phase0_food_waste", "kyb_only"], propagation_markings=["phase0_food_waste"], max_amount_per_deal=Decimal("100000"), max_amount_per_day=Decimal("500000"), max_quantity_per_deal=Decimal("2000"))
    view = ResourceOntologyService({resource.resource_id: resource}).build_view(resource.resource_id, mandate)
    with pytest.raises(ValueError):
        ACTION_TRANSITIONS[ActionName.SETTLE_DEAL].execute(NegotiationState.CFP_OPEN, MandateScope.from_mandate(mandate), view, Decimal("1"))
