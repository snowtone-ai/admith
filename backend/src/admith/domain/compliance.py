from __future__ import annotations

from dataclasses import dataclass

from admith.domain.models import FoodWasteScenario, ResourceUse


@dataclass(frozen=True)
class ComplianceResult:
    violations: list[str]

    @property
    def is_compliant(self) -> bool:
        return not self.violations


class FoodWasteComplianceRules:
    def evaluate(self, scenario: FoodWasteScenario) -> ComplianceResult:
        violations: list[str] = []
        priority_use = self.highest_priority_viable_use(scenario)
        if scenario.required_use != priority_use:
            violations.append(f"food_recycle_priority_requires_{priority_use.value}")
        if scenario.contamination_risk == "high":
            violations.append("contamination_risk_high")
        if not scenario.carrier_has_waste_permit:
            violations.append("missing_waste_carrier_permit")
        if "food_waste" not in scenario.carrier_permit_scope:
            violations.append("carrier_permit_scope_excludes_food_waste")
        if not scenario.manifest_supported:
            violations.append("manifest_not_supported")
        if not scenario.consignment_contract_ready:
            violations.append("missing_waste_consignment_contract")
        if not scenario.producer_responsibility_ack:
            violations.append("producer_responsibility_not_acknowledged")
        return ComplianceResult(violations)

    @staticmethod
    def highest_priority_viable_use(scenario: FoodWasteScenario) -> ResourceUse:
        for use in (ResourceUse.FEED, ResourceUse.FERTILIZER, ResourceUse.UPCYCLE):
            if use in scenario.viable_uses:
                return use
        raise ValueError("scenario.viable_uses must not be empty")
