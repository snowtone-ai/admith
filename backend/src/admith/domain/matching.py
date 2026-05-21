from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from admith.domain.models import Agent, MatchingOutcomeMetric, Negotiation, Resource
from admith.ports.interfaces import FeedbackSinkPort


@dataclass(frozen=True)
class MatchResult:
    negotiation: Negotiation | None
    candidates: list[Agent]
    metric: MatchingOutcomeMetric | None


class MatchingEngine:
    def __init__(self, feedback: FeedbackSinkPort | None = None) -> None:
        self.feedback = feedback

    def match(self, resource: Resource, agents: list[Agent], initiator_agent_id: UUID) -> MatchResult:
        now = datetime.now(timezone.utc)
        if resource.ttl_until < now:
            return MatchResult(None, [], None)
        quantity = Decimal(str(resource.attributes.get("quantity_kg", "0")))
        candidates = [
            agent
            for agent in agents
            if agent.status == "active"
            and resource.domain_id in agent.domain_capabilities.get("domains", [resource.domain_id])
            and quantity <= Decimal(str(agent.domain_capabilities.get("max_quantity_kg", quantity)))
        ]
        if not candidates:
            return MatchResult(None, [], None)
        negotiation = Negotiation(initiator_agent_id=initiator_agent_id, resource_id=resource.resource_id)
        metric = MatchingOutcomeMetric(
            domain_id=resource.domain_id,
            matching_policy="phase0_rule_based",
            candidate_count=len(candidates),
            negotiation_id=negotiation.negotiation_id,
            outcome="started",
            elapsed_seconds=Decimal("0"),
        )
        return MatchResult(negotiation, candidates, metric)
