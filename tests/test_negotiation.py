from __future__ import annotations

import unittest
from dataclasses import replace

from poc.negotiation import (
    MandateScope,
    OntologyView,
    RuleEngine,
    compare_variants,
    default_food_waste_scenario,
    execute_action,
    execute_phase0_action_path,
    run_natural_language_baseline,
    run_structured_cnp,
)


class NegotiationPoCTest(unittest.TestCase):
    def test_structured_cnp_converges_with_rule_engine_agreement(self) -> None:
        result = run_structured_cnp()

        self.assertTrue(result.converged)
        self.assertIsNotNone(result.agreement)
        self.assertEqual(result.rounds, 2)
        self.assertTrue(result.agreement.requires_human_final_approval)
        self.assertIn("cfp", {message.message_type for message in result.audit_log})
        self.assertGreater(result.agreement.total_delta_yen, 0)

    def test_natural_language_baseline_converges_only_after_parsing_and_validation(self) -> None:
        result = run_natural_language_baseline()

        self.assertTrue(result.converged)
        self.assertIsNotNone(result.agreement)
        self.assertEqual(result.rounds, 3)
        self.assertEqual(result.agreement.transfer_price_yen_per_kg, -5)
        self.assertTrue(result.agreement.requires_human_final_approval)

    def test_rule_engine_rejects_missing_waste_carrier_permit(self) -> None:
        scenario = replace(default_food_waste_scenario(), carrier_has_waste_permit=False)
        engine = RuleEngine()

        agreement = engine.evaluate(scenario, transfer_price_yen_per_kg=engine.fair_price(scenario))

        self.assertIsNone(agreement)
        self.assertIn("missing_waste_carrier_permit", engine.rejection_reasons)

    def test_rule_engine_enforces_food_recycle_priority_and_contract_readiness(self) -> None:
        scenario = replace(
            default_food_waste_scenario(),
            required_use="fertilizer",
            consignment_contract_ready=False,
        )
        engine = RuleEngine()

        agreement = engine.evaluate(scenario, transfer_price_yen_per_kg=engine.fair_price(scenario))

        self.assertIsNone(agreement)
        self.assertIn("food_recycle_priority_requires_feed", engine.rejection_reasons)
        self.assertIn("missing_waste_consignment_contract", engine.rejection_reasons)

    def test_rule_engine_allows_fertilizer_when_feed_is_not_viable(self) -> None:
        scenario = replace(default_food_waste_scenario(), required_use="fertilizer", viable_uses=("fertilizer", "upcycle"))
        engine = RuleEngine()

        agreement = engine.evaluate(scenario, transfer_price_yen_per_kg=engine.fair_price(scenario))

        self.assertIsNotNone(agreement)

    def test_phase0_action_path_maps_cfp_to_settled(self) -> None:
        records = execute_phase0_action_path("mediator_agent")

        self.assertEqual(records[0].before_state, "resource_available")
        self.assertEqual(records[-1].after_state, "settled")
        self.assertEqual(
            [record.action_name for record in records],
            [
                "CreateCFP",
                "SubmitProposal",
                "FormAgreement",
                "RequestApproval",
                "ApproveAgreement",
                "SignAgreement",
                "SettleDeal",
            ],
        )

    def test_action_rejects_invalid_state_transition(self) -> None:
        with self.assertRaises(ValueError):
            execute_action("SettleDeal", "cfp_open", "mediator_agent")

    def test_ontology_view_is_mandate_checked_before_llm_use(self) -> None:
        scenario = default_food_waste_scenario()
        view = OntologyView.from_scenario(scenario)
        mandate = MandateScope(
            allowed_object_types=("FoodWasteResource",),
            allowed_actions=("CreateCFP", "SubmitProposal"),
            allowed_regions=("tokyo",),
            property_markings=("phase0_food_waste", "kyb_only"),
            max_amount_per_deal_yen=100_000,
            max_quantity_kg_per_deal=2_000,
            propagation_markings=("phase0_food_waste", "kyb_only"),
        )

        self.assertTrue(mandate.allows("CreateCFP", view, amount_yen=25_000))
        self.assertFalse(mandate.allows("SettleDeal", view, amount_yen=25_000))

    def test_comparison_records_success_delta_latency_and_cost(self) -> None:
        structured, baseline, comparison = compare_variants()

        self.assertTrue(structured.converged)
        self.assertTrue(baseline.converged)
        self.assertEqual(comparison.success_rate, 1.0)
        self.assertGreaterEqual(comparison.price_consistency_yen_per_kg, 0)
        self.assertGreater(comparison.structured_total_delta_yen, 0)
        self.assertGreater(comparison.baseline_total_delta_yen, 0)


if __name__ == "__main__":
    unittest.main()
