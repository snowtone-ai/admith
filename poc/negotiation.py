from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Literal


MessageType = Literal["cfp", "proposal", "counter", "accept", "reject", "summary"]
VariantName = Literal["variant_a_structured_cnp", "variant_b_natural_language"]
ResourceUse = Literal["feed", "fertilizer", "upcycle"]
NegotiationState = Literal[
    "resource_available",
    "cfp_open",
    "negotiating",
    "draft_agreement",
    "pending_human_approval",
    "signing",
    "settled",
    "failed",
    "expired",
]
ActionName = Literal[
    "CreateCFP",
    "SubmitProposal",
    "CounterOffer",
    "FormAgreement",
    "RequestApproval",
    "ApproveAgreement",
    "SignAgreement",
    "SettleDeal",
    "FailNegotiation",
    "ExpireNegotiation",
]


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
    contamination_risk: Literal["low", "medium", "high"]
    carrier_has_waste_permit: bool
    manifest_supported: bool
    viable_uses: tuple[ResourceUse, ...] = ("feed", "fertilizer", "upcycle")
    carrier_permit_scope: tuple[str, ...] = ("food_waste",)
    consignment_contract_ready: bool = True
    producer_responsibility_ack: bool = True
    resource_envelope_version: str = "resource-envelope.v1"
    ontology_markings: tuple[str, ...] = ("phase0_food_waste", "kyb_only")


@dataclass(frozen=True)
class Agreement:
    transfer_price_yen_per_kg: int
    logistics_fee_yen: int
    platform_fee_yen: int
    seller_delta_yen: int
    buyer_delta_yen: int
    total_delta_yen: int
    compliance_reasons: tuple[str, ...] = ()
    requires_human_final_approval: bool = True


@dataclass(frozen=True)
class AuditMessage:
    round_no: int
    sender: str
    message_type: MessageType
    content: str


@dataclass(frozen=True)
class RunResult:
    variant: VariantName
    converged: bool
    agreement: Agreement | None
    latency_seconds: float
    estimated_cost_usd: float
    rounds: int
    audit_log: tuple[AuditMessage, ...]
    failure_reason: str | None = None


@dataclass(frozen=True)
class MandateScope:
    allowed_object_types: tuple[str, ...]
    allowed_actions: tuple[ActionName, ...]
    allowed_regions: tuple[str, ...]
    property_markings: tuple[str, ...]
    max_amount_per_deal_yen: int
    max_quantity_kg_per_deal: int
    propagation_markings: tuple[str, ...]

    def allows(self, action: ActionName, view: "OntologyView", amount_yen: int) -> bool:
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
class OntologyView:
    object_id: str
    object_type: str
    domain_id: str
    quantity_kg: int
    permitted_fields: tuple[str, ...]
    security_markings: tuple[str, ...]
    facts: dict[str, str | int | bool]

    @classmethod
    def from_scenario(cls, scenario: FoodWasteScenario) -> "OntologyView":
        return cls(
            object_id=scenario.lot_id,
            object_type="FoodWasteResource",
            domain_id="food_waste",
            quantity_kg=scenario.quantity_kg,
            permitted_fields=("material", "quantity_kg", "required_use", "contamination_risk"),
            security_markings=scenario.ontology_markings,
            facts={
                "material": scenario.material,
                "quantity_kg": scenario.quantity_kg,
                "required_use": scenario.required_use,
                "contamination_risk": scenario.contamination_risk,
                "manifest_supported": scenario.manifest_supported,
            },
        )


@dataclass(frozen=True)
class ActionRecord:
    action_name: ActionName
    actor_agent_id: str
    before_state: NegotiationState
    after_state: NegotiationState
    preconditions: tuple[str, ...]
    mutations: tuple[str, ...]
    postconditions: tuple[str, ...]
    audit_event_type: str


@dataclass(frozen=True)
class Comparison:
    success_rate: float
    price_consistency_yen_per_kg: int
    latency_seconds: float
    estimated_cost_usd: float
    structured_total_delta_yen: int
    baseline_total_delta_yen: int


@dataclass
class RuleEngine:
    platform_take_rate: float = 0.20
    rejection_reasons: list[str] = field(default_factory=list)

    def evaluate(self, scenario: FoodWasteScenario, transfer_price_yen_per_kg: int) -> Agreement | None:
        self.rejection_reasons.clear()
        self.rejection_reasons.extend(self.validate_compliance(scenario))
        logistics_fee = self.logistics_fee(scenario)
        seller_min_price = -self._floor_div(scenario.seller_disposal_cost_yen, scenario.quantity_kg)

        if transfer_price_yen_per_kg < seller_min_price:
            self.rejection_reasons.append("seller_worse_than_disposal")
        if transfer_price_yen_per_kg > scenario.buyer_max_price_yen_per_kg:
            self.rejection_reasons.append("buyer_price_limit_exceeded")

        gross_delta = self.gross_delta(scenario, logistics_fee)
        platform_fee = round(gross_delta * self.platform_take_rate)
        seller_fee = platform_fee // 2
        buyer_fee = platform_fee - seller_fee
        seller_delta = scenario.seller_disposal_cost_yen + (transfer_price_yen_per_kg * scenario.quantity_kg) - seller_fee
        buyer_delta = (
            scenario.buyer_alternative_cost_yen_per_kg * scenario.quantity_kg
            - (transfer_price_yen_per_kg * scenario.quantity_kg)
            - logistics_fee
            - buyer_fee
        )
        total_delta = seller_delta + buyer_delta

        if gross_delta <= 0:
            self.rejection_reasons.append("non_positive_gross_delta")
        if seller_delta <= 0:
            self.rejection_reasons.append("seller_delta_not_positive")
        if buyer_delta <= 0:
            self.rejection_reasons.append("buyer_delta_not_positive")

        if self.rejection_reasons:
            return None

        return Agreement(
            transfer_price_yen_per_kg=transfer_price_yen_per_kg,
            logistics_fee_yen=logistics_fee,
            platform_fee_yen=platform_fee,
            seller_delta_yen=seller_delta,
            buyer_delta_yen=buyer_delta,
            total_delta_yen=total_delta,
            compliance_reasons=tuple(self.validate_compliance(scenario)),
        )

    def validate_compliance(self, scenario: FoodWasteScenario) -> list[str]:
        reasons: list[str] = []
        priority_use = self.highest_priority_viable_use(scenario)
        if scenario.required_use != priority_use:
            reasons.append(f"food_recycle_priority_requires_{priority_use}")
        if scenario.contamination_risk == "high":
            reasons.append("contamination_risk_high")
        if not scenario.carrier_has_waste_permit:
            reasons.append("missing_waste_carrier_permit")
        if "food_waste" not in scenario.carrier_permit_scope:
            reasons.append("carrier_permit_scope_excludes_food_waste")
        if not scenario.manifest_supported:
            reasons.append("manifest_not_supported")
        if not scenario.consignment_contract_ready:
            reasons.append("missing_waste_consignment_contract")
        if not scenario.producer_responsibility_ack:
            reasons.append("producer_responsibility_not_acknowledged")
        if scenario.resource_envelope_version != "resource-envelope.v1":
            reasons.append("unsupported_resource_envelope_version")
        return reasons

    @staticmethod
    def highest_priority_viable_use(scenario: FoodWasteScenario) -> ResourceUse:
        for use in ("feed", "fertilizer", "upcycle"):
            if use in scenario.viable_uses:
                return use
        raise ValueError("scenario.viable_uses must not be empty")

    def fair_price(self, scenario: FoodWasteScenario) -> int:
        seller_min_price = -self._floor_div(scenario.seller_disposal_cost_yen, scenario.quantity_kg)
        return round((seller_min_price + scenario.buyer_max_price_yen_per_kg) / 2)

    def logistics_fee(self, scenario: FoodWasteScenario) -> int:
        return scenario.logistics_base_fee_yen + scenario.logistics_yen_per_kg * scenario.quantity_kg

    def gross_delta(self, scenario: FoodWasteScenario, logistics_fee: int | None = None) -> int:
        fee = self.logistics_fee(scenario) if logistics_fee is None else logistics_fee
        return (
            scenario.seller_disposal_cost_yen
            + scenario.buyer_alternative_cost_yen_per_kg * scenario.quantity_kg
            - fee
        )

    @staticmethod
    def _floor_div(value: int, divisor: int) -> int:
        return value // divisor


def default_food_waste_scenario() -> FoodWasteScenario:
    return FoodWasteScenario(
        lot_id="okara-tokyo-001",
        material="okara",
        quantity_kg=1000,
        seller_disposal_cost_yen=25_000,
        buyer_alternative_cost_yen_per_kg=38,
        buyer_max_price_yen_per_kg=18,
        logistics_base_fee_yen=12_000,
        logistics_yen_per_kg=4,
        required_use="feed",
        contamination_risk="low",
        carrier_has_waste_permit=True,
        manifest_supported=True,
    )


def run_structured_cnp(scenario: FoodWasteScenario | None = None) -> RunResult:
    started = time.perf_counter()
    scenario = scenario or default_food_waste_scenario()
    engine = RuleEngine()
    fair_price = engine.fair_price(scenario)
    logistics_fee = engine.logistics_fee(scenario)
    actions = execute_phase0_action_path("mediator_agent")
    audit_log = [
        AuditMessage(1, "seller_agent", "cfp", f"{scenario.quantity_kg}kg {scenario.material}; disposal={scenario.seller_disposal_cost_yen}"),
        AuditMessage(1, "buyer_agent", "proposal", f"max_price_yen_per_kg={scenario.buyer_max_price_yen_per_kg}"),
        AuditMessage(1, "logistics_agent", "proposal", f"fee_yen={logistics_fee}; permit={scenario.carrier_has_waste_permit}"),
        AuditMessage(2, "mediator_agent", "counter", f"rule_engine_price_yen_per_kg={fair_price}"),
        AuditMessage(2, "mediator_agent", "summary", f"action_path={','.join(action.action_name for action in actions)}"),
    ]
    agreement = engine.evaluate(scenario, fair_price)
    if agreement is None:
        return RunResult(
            variant="variant_a_structured_cnp",
            converged=False,
            agreement=None,
            latency_seconds=time.perf_counter() - started,
            estimated_cost_usd=0.0,
            rounds=2,
            audit_log=tuple(audit_log),
            failure_reason=";".join(engine.rejection_reasons),
        )

    audit_log.extend(
        [
            AuditMessage(2, "seller_agent", "accept", "seller_delta_positive"),
            AuditMessage(2, "buyer_agent", "accept", "buyer_delta_positive"),
            AuditMessage(2, "mediator_agent", "summary", f"total_delta_yen={agreement.total_delta_yen}"),
        ]
    )
    return RunResult(
        variant="variant_a_structured_cnp",
        converged=True,
        agreement=agreement,
        latency_seconds=time.perf_counter() - started,
        estimated_cost_usd=0.0,
        rounds=2,
        audit_log=tuple(audit_log),
    )


def run_natural_language_baseline(scenario: FoodWasteScenario | None = None) -> RunResult:
    started = time.perf_counter()
    scenario = scenario or default_food_waste_scenario()
    engine = RuleEngine()
    logistics_fee = engine.logistics_fee(scenario)
    seller_anchor = -18
    buyer_anchor = 12
    transcript = [
        AuditMessage(1, "seller_agent", "proposal", f"We can release {scenario.quantity_kg}kg if the disposal contribution is not worse than -25 yen/kg."),
        AuditMessage(1, "buyer_agent", "counter", f"We can accept okara near {buyer_anchor} yen/kg if logistics stays predictable."),
        AuditMessage(1, "logistics_agent", "proposal", f"Pickup is possible for {logistics_fee} yen with manifest support."),
        AuditMessage(2, "seller_agent", "counter", f"Seller proposes {seller_anchor} yen/kg to move today."),
        AuditMessage(2, "buyer_agent", "counter", "Buyer counters at 8 yen/kg after transport risk."),
        AuditMessage(3, "mediator_agent", "summary", "Mediator suggests settling at -5 yen/kg so both sides keep positive delta."),
    ]
    parsed_price = _extract_last_price(transcript[-1].content)
    agreement = engine.evaluate(scenario, parsed_price)
    if agreement is None:
        return RunResult(
            variant="variant_b_natural_language",
            converged=False,
            agreement=None,
            latency_seconds=time.perf_counter() - started,
            estimated_cost_usd=_offline_llm_cost(transcript),
            rounds=3,
            audit_log=tuple(transcript),
            failure_reason=";".join(engine.rejection_reasons),
        )

    transcript.append(AuditMessage(3, "mediator_agent", "summary", f"Parsed non-binding draft; total_delta_yen={agreement.total_delta_yen}"))
    return RunResult(
        variant="variant_b_natural_language",
        converged=True,
        agreement=agreement,
        latency_seconds=time.perf_counter() - started,
        estimated_cost_usd=_offline_llm_cost(transcript),
        rounds=3,
        audit_log=tuple(transcript),
    )


def compare_variants() -> tuple[RunResult, RunResult, Comparison]:
    structured = run_structured_cnp()
    baseline = run_natural_language_baseline()
    if structured.agreement is None or baseline.agreement is None:
        success_count = int(structured.converged) + int(baseline.converged)
        return structured, baseline, Comparison(success_count / 2, 0, 0.0, 0.0, 0, 0)

    comparison = Comparison(
        success_rate=(int(structured.converged) + int(baseline.converged)) / 2,
        price_consistency_yen_per_kg=abs(
            structured.agreement.transfer_price_yen_per_kg - baseline.agreement.transfer_price_yen_per_kg
        ),
        latency_seconds=structured.latency_seconds + baseline.latency_seconds,
        estimated_cost_usd=structured.estimated_cost_usd + baseline.estimated_cost_usd,
        structured_total_delta_yen=structured.agreement.total_delta_yen,
        baseline_total_delta_yen=baseline.agreement.total_delta_yen,
    )
    return structured, baseline, comparison


ACTION_TRANSITIONS: dict[ActionName, tuple[NegotiationState, NegotiationState]] = {
    "CreateCFP": ("resource_available", "cfp_open"),
    "SubmitProposal": ("cfp_open", "negotiating"),
    "CounterOffer": ("negotiating", "negotiating"),
    "FormAgreement": ("negotiating", "draft_agreement"),
    "RequestApproval": ("draft_agreement", "pending_human_approval"),
    "ApproveAgreement": ("pending_human_approval", "signing"),
    "SignAgreement": ("signing", "signing"),
    "SettleDeal": ("signing", "settled"),
    "FailNegotiation": ("negotiating", "failed"),
    "ExpireNegotiation": ("negotiating", "expired"),
}


def execute_action(action_name: ActionName, state: NegotiationState, actor_agent_id: str) -> ActionRecord:
    expected_state, next_state = ACTION_TRANSITIONS[action_name]
    if state != expected_state:
        raise ValueError(f"{action_name} requires {expected_state}, got {state}")
    return ActionRecord(
        action_name=action_name,
        actor_agent_id=actor_agent_id,
        before_state=state,
        after_state=next_state,
        preconditions=(f"state_is_{expected_state}", "mandate_allows_action"),
        mutations=(f"set_state_{next_state}",),
        postconditions=(f"state_is_{next_state}", "audit_event_recorded"),
        audit_event_type=f"action.{action_name}",
    )


def execute_phase0_action_path(actor_agent_id: str) -> tuple[ActionRecord, ...]:
    state: NegotiationState = "resource_available"
    records: list[ActionRecord] = []
    for action_name in (
        "CreateCFP",
        "SubmitProposal",
        "FormAgreement",
        "RequestApproval",
        "ApproveAgreement",
        "SignAgreement",
        "SettleDeal",
    ):
        record = execute_action(action_name, state, actor_agent_id)
        records.append(record)
        state = record.after_state
    return tuple(records)


def _extract_last_price(text: str) -> int:
    matches = re.findall(r"-?\d+\s*yen/kg", text)
    if not matches:
        raise ValueError(f"no yen/kg price found in text: {text}")
    return int(matches[-1].split("yen/kg")[0].strip())


def _offline_llm_cost(messages: list[AuditMessage]) -> float:
    estimated_tokens = sum(max(1, len(message.content.split())) for message in messages)
    return round((estimated_tokens / 1_000_000) * 1.20, 8)
