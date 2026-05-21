from __future__ import annotations

from decimal import Decimal

from admith.domain.models import KybStatus, OwnerEntity, TrustScoreHistory


class TrustScoreService:
    scores = {KybStatus.VERIFIED: Decimal("0.8"), KybStatus.PENDING: Decimal("0.3"), KybStatus.REJECTED: Decimal("0.0")}

    def calculate(self, owner: OwnerEntity):
        return self.scores[owner.kyb_status]

    def record(self, owner: OwnerEntity, agent_id) -> TrustScoreHistory:
        return TrustScoreHistory(
            agent_id=agent_id,
            score=self.calculate(owner),
            calculation_method="kyb_based",
            input_signals={"kyb_status": owner.kyb_status.value},
        )
