from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from admith.domain.models import ActionName, Agreement, AuditEvent, Negotiation, NegotiationState


@dataclass(frozen=True)
class OrchestratorResult:
    negotiation: Negotiation
    agreement: Agreement | None
    audit_events: list[AuditEvent]


class NegotiationOrchestrator:
    normal_path = (
        ActionName.SUBMIT_PROPOSAL,
        ActionName.FORM_AGREEMENT,
        ActionName.REQUEST_APPROVAL,
    )

    def advance_to_approval(self, negotiation: Negotiation, agreement: Agreement, median_price: Decimal | None = None) -> OrchestratorResult:
        events: list[AuditEvent] = []
        price = Decimal(str(agreement.terms.get("transfer_price_yen_per_kg", "0")))
        if median_price is not None and (price > median_price * Decimal("1.5") or price < median_price * Decimal("0.5")):
            negotiation.state = NegotiationState.FAILED
            events.append(self._event(negotiation, "circuit_breaker.price_anomaly"))
            return OrchestratorResult(negotiation, None, events)
        if negotiation.matching_ttl_until < datetime.now(timezone.utc):
            negotiation.state = NegotiationState.EXPIRED
            events.append(self._event(negotiation, "action.ExpireNegotiation"))
            return OrchestratorResult(negotiation, None, events)

        for action, state in (
            (ActionName.SUBMIT_PROPOSAL, NegotiationState.NEGOTIATING),
            (ActionName.FORM_AGREEMENT, NegotiationState.DRAFT_AGREEMENT),
            (ActionName.REQUEST_APPROVAL, NegotiationState.PENDING_HUMAN_APPROVAL),
        ):
            negotiation.state = state
            events.append(self._event(negotiation, f"action.{action.value}"))
        agreement.negotiation_id = negotiation.negotiation_id
        agreement.state = "pending_approval"
        return OrchestratorResult(negotiation, agreement, events)

    def settle_after_approval(self, negotiation: Negotiation) -> list[AuditEvent]:
        if negotiation.state != NegotiationState.PENDING_HUMAN_APPROVAL:
            raise ValueError("approval_required_before_signing")
        events: list[AuditEvent] = []
        negotiation.state = NegotiationState.SIGNING
        events.append(self._event(negotiation, "action.ApproveAgreement"))
        events.append(self._event(negotiation, "action.SignAgreement"))
        negotiation.state = NegotiationState.SETTLED
        negotiation.ended_at = datetime.now(timezone.utc)
        events.append(self._event(negotiation, "action.SettleDeal"))
        return events

    @staticmethod
    def _event(negotiation: Negotiation, event_type: str) -> AuditEvent:
        return AuditEvent(
            negotiation_id=negotiation.negotiation_id,
            event_type=event_type,
            event_data={"state": negotiation.state.value},
            sequence_number=0,
        )
