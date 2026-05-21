from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from admith.domain.models import AgentPolicy, Agreement, FoodWasteScenario, MessageType
from admith.domain.rule_engine import RuleEngine


@dataclass(frozen=True)
class AgentResponse:
    message_type: MessageType
    payload: dict[str, object]


class AgentProtocol(Protocol):
    async def on_cfp_received(self, cfp: FoodWasteScenario) -> AgentResponse | None: ...
    async def on_counter_received(self, counter: dict[str, object]) -> AgentResponse: ...
    async def evaluate(self, terms: dict[str, object]) -> bool: ...
    async def sign_agreement(self, agreement: Agreement) -> bytes: ...


class Phase0FoodWasteAgent:
    def __init__(self, policy: AgentPolicy | None = None, rule_engine: RuleEngine | None = None) -> None:
        self.policy = policy or AgentPolicy(model_tier=1)
        self.rule_engine = rule_engine or RuleEngine()

    async def on_cfp_received(self, cfp: FoodWasteScenario) -> AgentResponse | None:
        price = self.rule_engine.fair_price(cfp)
        agreement = self.rule_engine.evaluate(cfp, price)
        if agreement is None:
            return None
        return AgentResponse(MessageType.PROPOSAL, {"price_yen_per_kg": price, "terms": agreement.terms})

    async def on_counter_received(self, counter: dict[str, object]) -> AgentResponse:
        return AgentResponse(MessageType.ACCEPT, {"accepted": True, "counter": counter})

    async def evaluate(self, terms: dict[str, object]) -> bool:
        return Decimal(str(terms.get("total_delta_yen", "0"))) > 0

    async def sign_agreement(self, agreement: Agreement) -> bytes:
        if not await self.evaluate(agreement.terms):
            raise ValueError("agreement_not_acceptable")
        return b"phase0-agent-signature"
