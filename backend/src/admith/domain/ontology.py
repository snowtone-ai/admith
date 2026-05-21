from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import UUID

from admith.domain.models import ActionName, AgentMandate, NegotiationState, Resource


@dataclass(frozen=True)
class OntologyView:
    object_id: str
    object_type: str
    domain_id: str
    quantity_kg: Decimal
    permitted_fields: tuple[str, ...]
    security_markings: tuple[str, ...]
    facts: dict[str, Any]


@dataclass(frozen=True)
class MandateScope:
    allowed_object_types: tuple[str, ...]
    allowed_actions: tuple[ActionName, ...]
    allowed_regions: tuple[str, ...]
    property_markings: tuple[str, ...]
    max_amount_per_deal_yen: Decimal
    max_quantity_kg_per_deal: Decimal
    propagation_markings: tuple[str, ...]

    @classmethod
    def from_mandate(cls, mandate: AgentMandate) -> MandateScope:
        return cls(
            allowed_object_types=tuple(mandate.allowed_object_types),
            allowed_actions=tuple(mandate.allowed_actions),
            allowed_regions=tuple(mandate.allowed_regions),
            property_markings=tuple(mandate.property_markings),
            max_amount_per_deal_yen=mandate.max_amount_per_deal,
            max_quantity_kg_per_deal=mandate.max_quantity_per_deal or Decimal("0"),
            propagation_markings=tuple(mandate.propagation_markings),
        )

    def allows(self, action: ActionName, view: OntologyView, amount_yen: Decimal) -> bool:
        if action not in self.allowed_actions:
            return False
        if view.object_type not in self.allowed_object_types:
            return False
        if not set(view.security_markings).issubset(self.property_markings):
            return False
        if amount_yen > self.max_amount_per_deal_yen:
            return False
        return view.quantity_kg <= self.max_quantity_kg_per_deal


@dataclass(frozen=True)
class ActionType:
    action_name: ActionName
    before_state: NegotiationState | str
    after_state: NegotiationState
    preconditions: tuple[str, ...]
    mutations: tuple[str, ...]
    postconditions: tuple[str, ...]
    audit_event_type: str

    def execute(self, state: NegotiationState, mandate: MandateScope, view: OntologyView, amount_yen: Decimal) -> NegotiationState:
        if self.before_state != "any non-terminal" and state != self.before_state:
            raise ValueError(f"{self.action_name} requires {self.before_state}, got {state}")
        if state in {NegotiationState.SETTLED, NegotiationState.FAILED, NegotiationState.EXPIRED}:
            raise ValueError("terminal_state_cannot_transition")
        if not mandate.allows(self.action_name, view, amount_yen):
            raise PermissionError("mandate_does_not_allow_action")
        return self.after_state


ACTION_TRANSITIONS: dict[ActionName, ActionType] = {
    ActionName.CREATE_CFP: ActionType(
        ActionName.CREATE_CFP,
        NegotiationState.RESOURCE_AVAILABLE,
        NegotiationState.CFP_OPEN,
        ("state_is_resource_available", "mandate_allows_action"),
        ("lock_resource", "create_negotiation"),
        ("state_is_cfp_open", "audit_event_recorded"),
        "action.CreateCFP",
    ),
    ActionName.SUBMIT_PROPOSAL: ActionType(
        ActionName.SUBMIT_PROPOSAL,
        NegotiationState.CFP_OPEN,
        NegotiationState.NEGOTIATING,
        ("state_is_cfp_open",),
        ("save_proposal",),
        ("state_is_negotiating",),
        "action.SubmitProposal",
    ),
    ActionName.COUNTER_OFFER: ActionType(ActionName.COUNTER_OFFER, NegotiationState.NEGOTIATING, NegotiationState.NEGOTIATING, (), (), (), "action.CounterOffer"),
    ActionName.FORM_AGREEMENT: ActionType(ActionName.FORM_AGREEMENT, NegotiationState.NEGOTIATING, NegotiationState.DRAFT_AGREEMENT, (), (), (), "action.FormAgreement"),
    ActionName.REQUEST_APPROVAL: ActionType(ActionName.REQUEST_APPROVAL, NegotiationState.DRAFT_AGREEMENT, NegotiationState.PENDING_HUMAN_APPROVAL, (), (), (), "action.RequestApproval"),
    ActionName.APPROVE_AGREEMENT: ActionType(ActionName.APPROVE_AGREEMENT, NegotiationState.PENDING_HUMAN_APPROVAL, NegotiationState.SIGNING, (), (), (), "action.ApproveAgreement"),
    ActionName.REJECT_AGREEMENT: ActionType(ActionName.REJECT_AGREEMENT, NegotiationState.PENDING_HUMAN_APPROVAL, NegotiationState.FAILED, (), (), (), "action.RejectAgreement"),
    ActionName.SIGN_AGREEMENT: ActionType(ActionName.SIGN_AGREEMENT, NegotiationState.SIGNING, NegotiationState.SIGNING, (), (), (), "action.SignAgreement"),
    ActionName.SETTLE_DEAL: ActionType(ActionName.SETTLE_DEAL, NegotiationState.SIGNING, NegotiationState.SETTLED, (), (), (), "action.SettleDeal"),
    ActionName.FAIL_NEGOTIATION: ActionType(ActionName.FAIL_NEGOTIATION, "any non-terminal", NegotiationState.FAILED, (), (), (), "action.FailNegotiation"),
    ActionName.EXPIRE_NEGOTIATION: ActionType(ActionName.EXPIRE_NEGOTIATION, "any non-terminal", NegotiationState.EXPIRED, (), (), (), "action.ExpireNegotiation"),
}


class ResourceOntologyService:
    object_types = ("FoodWasteResource", "AgentEntity", "AgreementDoc")
    field_markings = {
        "material": "phase0_food_waste",
        "quantity_kg": "phase0_food_waste",
        "required_use": "phase0_food_waste",
        "contamination_risk": "kyb_only",
        "disposal_cost_yen": "commercial_sensitive",
    }

    def __init__(self, resources: dict[UUID, Resource] | None = None) -> None:
        self.resources = resources or {}

    def build_view(self, subject_id: UUID, mandate: AgentMandate) -> OntologyView:
        resource = self.resources[subject_id]
        markings = tuple(resource.security_markings)
        allowed_markings = set(mandate.property_markings)
        facts = {
            key: value
            for key, value in resource.attributes.items()
            if self.field_markings.get(key, "phase0_food_waste") in allowed_markings
        }
        return OntologyView(
            object_id=str(resource.resource_id),
            object_type="FoodWasteResource",
            domain_id=resource.domain_id,
            quantity_kg=Decimal(str(resource.attributes.get("quantity_kg", "0"))),
            permitted_fields=tuple(facts),
            security_markings=markings,
            facts=facts,
        )
