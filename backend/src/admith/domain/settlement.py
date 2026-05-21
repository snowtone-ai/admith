from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from admith.domain.models import (
    Agreement,
    MandateAdjustmentRecommendation,
    MatchingOutcomeMetric,
    PriceSignalHistory,
    TrustScoreHistory,
)


class SettlementService:
    def settle(self, agreement: Agreement) -> dict[str, object]:
        agreement.state = "settled"
        agreement.settled_at = datetime.now(timezone.utc)
        return {
            "agreement_id": str(agreement.agreement_id),
            "parties": agreement.parties,
            "amounts": {
                "platform_fee_yen": agreement.terms.get("platform_fee_yen", 0),
                "total_delta_yen": agreement.terms.get("total_delta_yen", 0),
            },
            "items": agreement.terms,
            "issued_at": agreement.settled_at.isoformat(),
        }

    def feedback_records(self, agreement: Agreement) -> dict[str, object]:
        quantity = Decimal(str(agreement.terms.get("quantity_kg", "0")))
        price = Decimal(str(agreement.terms.get("transfer_price_yen_per_kg", "0")))
        agent_id = next(iter(agreement.parties.values()), None)
        return {
            "trust": TrustScoreHistory(agent_id=agent_id, score=Decimal("0.8"), calculation_method="settlement_success"),
            "price": PriceSignalHistory(
                domain_id="food_waste",
                resource_type=str(agreement.terms.get("material", "food_waste")),
                region=str(agreement.terms.get("region", "tokyo")),
                unit_price_yen=price,
                quantity_kg=quantity,
                agreement_id=agreement.agreement_id,
            ),
            "mandate": MandateAdjustmentRecommendation(
                agent_id=agent_id,
                owner_entity_id=agent_id,
                approval_rate=Decimal("1.0"),
                recommended_change={"approval_mode": "auto_within_mandate"},
            ),
            "matching": MatchingOutcomeMetric(
                domain_id="food_waste",
                matching_policy="phase0_rule_based",
                candidate_count=1,
                negotiation_id=agreement.negotiation_id,
                outcome="settled",
                elapsed_seconds=Decimal("0"),
            ),
        }
