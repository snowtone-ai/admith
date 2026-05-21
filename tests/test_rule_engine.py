from __future__ import annotations

from dataclasses import replace

from admith.domain.models import FoodWasteScenario, ResourceUse
from admith.domain.rule_engine import RuleEngine


def scenario() -> FoodWasteScenario:
    return FoodWasteScenario("okara", "okara", 1000, 25000, 38, 18, 12000, 4, ResourceUse.FEED, "low", True, True)


def test_rule_engine_accepts_normal_case() -> None:
    engine = RuleEngine()
    agreement = engine.evaluate(scenario(), engine.fair_price(scenario()))
    assert agreement is not None
    assert agreement.terms["seller_delta_yen"] > 0
    assert agreement.terms["buyer_delta_yen"] > 0


def test_rule_engine_rejects_five_compliance_cases() -> None:
    cases = [
        replace(scenario(), carrier_has_waste_permit=False),
        replace(scenario(), manifest_supported=False),
        replace(scenario(), consignment_contract_ready=False),
        replace(scenario(), producer_responsibility_ack=False),
        replace(scenario(), required_use=ResourceUse.FERTILIZER),
    ]
    for case in cases:
        engine = RuleEngine()
        assert engine.evaluate(case, engine.fair_price(case)) is None
        assert engine.rejection_reasons
