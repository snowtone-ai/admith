from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from uuid import UUID

from admith.domain.models import (
    Agreement,
    ApprovalDecision,
    ApprovalDecisionValue,
    ApprovalRequest,
    MandateAdjustmentRecommendation,
    Negotiation,
    NegotiationState,
)


def canonical_hash(value: dict[str, object]) -> bytes:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(payload).digest()


class ApprovalWorkflow:
    def request_approval(self, agreement: Agreement, negotiation: Negotiation, owner_entity_id: UUID) -> ApprovalRequest:
        negotiation.state = NegotiationState.PENDING_HUMAN_APPROVAL
        negotiation.approval_ttl_until = datetime.now(timezone.utc) + timedelta(hours=1)
        return ApprovalRequest(
            negotiation_id=negotiation.negotiation_id,
            agreement_id=agreement.agreement_id,
            owner_entity_id=owner_entity_id,
            displayed_terms_hash=canonical_hash(agreement.terms),
            expires_at=negotiation.approval_ttl_until,
        )

    def decide(
        self,
        request: ApprovalRequest,
        agreement: Agreement,
        displayed_terms_hash: bytes,
        decision: ApprovalDecisionValue,
        reason: str | None,
        agent_id: UUID,
    ) -> tuple[ApprovalDecision, MandateAdjustmentRecommendation | None]:
        if request.expires_at < datetime.now(timezone.utc):
            request.status = "expired"
            raise TimeoutError("approval_request_expired")
        if displayed_terms_hash != canonical_hash(agreement.terms):
            raise ValueError("displayed_terms_hash_mismatch")
        if request.displayed_terms_hash and displayed_terms_hash != request.displayed_terms_hash:
            raise ValueError("approval_request_hash_mismatch")
        request.status = "approved" if decision == ApprovalDecisionValue.APPROVE else "rejected"
        approval = ApprovalDecision(
            approval_id=request.approval_id,
            decision=decision,
            reason=reason,
            displayed_terms_hash=displayed_terms_hash,
        )
        recommendation = None
        if decision == ApprovalDecisionValue.REJECT:
            recommendation = MandateAdjustmentRecommendation(
                agent_id=agent_id,
                owner_entity_id=request.owner_entity_id,
                approval_rate=0,
                reject_reasons=[reason or "rejected"],
                recommended_change={"approval_mode": "approve_all"},
            )
        return approval, recommendation
