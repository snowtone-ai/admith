from __future__ import annotations

from decimal import Decimal

from admith.domain.compliance import ComplianceResult, FoodWasteComplianceRules
from admith.domain.models import Agreement, FoodWasteScenario


class RuleEngine:
    def __init__(self, compliance: FoodWasteComplianceRules | None = None, platform_take_rate: Decimal = Decimal("0.20")) -> None:
        self.compliance = compliance or FoodWasteComplianceRules()
        self.platform_take_rate = platform_take_rate
        self.rejection_reasons: list[str] = []

    def evaluate(self, scenario: FoodWasteScenario, price: int | Decimal) -> Agreement | None:
        self.rejection_reasons.clear()
        compliance_result: ComplianceResult = self.compliance.evaluate(scenario)
        if compliance_result.violations:
            self.rejection_reasons.extend(compliance_result.violations)
            return None

        price_yen = Decimal(str(price))
        quantity = Decimal(scenario.quantity_kg)
        logistics_fee = Decimal(self.logistics_fee(scenario))
        seller_min_price = Decimal(-self._floor_div(scenario.seller_disposal_cost_yen, scenario.quantity_kg))
        gross_delta = Decimal(self.gross_delta(scenario, int(logistics_fee)))
        platform_fee = (gross_delta * self.platform_take_rate).quantize(Decimal("1"))
        seller_fee = platform_fee // 2
        buyer_fee = platform_fee - seller_fee
        seller_delta = Decimal(scenario.seller_disposal_cost_yen) + price_yen * quantity - seller_fee
        buyer_delta = Decimal(scenario.buyer_alternative_cost_yen_per_kg) * quantity - price_yen * quantity - logistics_fee - buyer_fee

        if price_yen < seller_min_price:
            self.rejection_reasons.append("seller_worse_than_disposal")
        if price_yen > scenario.buyer_max_price_yen_per_kg:
            self.rejection_reasons.append("buyer_price_limit_exceeded")
        if gross_delta <= 0:
            self.rejection_reasons.append("non_positive_gross_delta")
        if seller_delta <= 0:
            self.rejection_reasons.append("seller_delta_not_positive")
        if buyer_delta <= 0:
            self.rejection_reasons.append("buyer_delta_not_positive")
        if self.rejection_reasons:
            return None

        return Agreement(
            terms={
                "transfer_price_yen_per_kg": int(price_yen),
                "quantity_kg": scenario.quantity_kg,
                "logistics_fee_yen": int(logistics_fee),
                "platform_fee_yen": int(platform_fee),
                "seller_delta_yen": int(seller_delta),
                "buyer_delta_yen": int(buyer_delta),
                "total_delta_yen": int(seller_delta + buyer_delta),
                "compliance_reasons": [],
                "requires_human_final_approval": True,
            }
        )

    def fair_price(self, scenario: FoodWasteScenario) -> int:
        seller_min_price = -self._floor_div(scenario.seller_disposal_cost_yen, scenario.quantity_kg)
        return round((seller_min_price + scenario.buyer_max_price_yen_per_kg) / 2)

    @staticmethod
    def logistics_fee(scenario: FoodWasteScenario) -> int:
        return scenario.logistics_base_fee_yen + scenario.logistics_yen_per_kg * scenario.quantity_kg

    def gross_delta(self, scenario: FoodWasteScenario, logistics_fee: int | None = None) -> int:
        fee = self.logistics_fee(scenario) if logistics_fee is None else logistics_fee
        return scenario.seller_disposal_cost_yen + scenario.buyer_alternative_cost_yen_per_kg * scenario.quantity_kg - fee

    @staticmethod
    def _floor_div(value: int, divisor: int) -> int:
        return value // divisor
