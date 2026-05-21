from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Protocol
from uuid import UUID

from admith.domain.compliance import ComplianceResult
from admith.domain.contracts import ResourceEnvelope, Terms
from admith.domain.models import Agreement, ApprovalDecision, AuditEvent, Negotiation, Resource
from admith.domain.ontology import ActionType, OntologyView


@dataclass(frozen=True)
class LLMTask:
    task_type: str
    instructions: str
    output_schema: dict[str, Any] | None = None


@dataclass(frozen=True)
class CompletionResult:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    cost_yen: Decimal = Decimal("0")


@dataclass(frozen=True)
class ActionContext:
    negotiation: Negotiation
    view: OntologyView
    amount_yen: Decimal


@dataclass(frozen=True)
class ActionResult:
    state: str
    audit_event_type: str


@dataclass(frozen=True)
class SettlementOutcome:
    success: bool
    invoice: dict[str, Any]


class OntologyViewPort(Protocol):
    def build_view(self, subject_id: UUID, mandate: Any) -> OntologyView: ...


class ComplianceRulePort(Protocol):
    def check(self, terms: Terms, envelope: ResourceEnvelope) -> ComplianceResult: ...


class ActionExecutorPort(Protocol):
    def execute(self, action: ActionType, context: ActionContext) -> ActionResult: ...


class ApprovalPort(Protocol):
    def request_approval(self, agreement: Agreement, negotiation: Negotiation, owner_entity_id: UUID) -> Any: ...
    def decide(self, request: Any, agreement: Agreement, displayed_terms_hash: bytes, decision: Any, reason: str | None, agent_id: UUID) -> tuple[ApprovalDecision, Any]: ...


class FeedbackSinkPort(Protocol):
    def record_settlement_feedback(self, agreement: Agreement, outcome: SettlementOutcome) -> None: ...
    def record(self, record_type: str, record: Any) -> None: ...


class LLMProvider(Protocol):
    async def complete_view(
        self, view: OntologyView, task: LLMTask, max_tokens: int, temperature: float
    ) -> CompletionResult: ...


class ResourceRepositoryPort(Protocol):
    async def add(self, resource: Resource) -> Resource: ...
    async def get(self, resource_id: UUID) -> Resource | None: ...
    async def lock_available(self, resource_id: UUID, negotiation_id: UUID) -> Resource | None: ...


class NegotiationRepositoryPort(Protocol):
    async def add(self, negotiation: Negotiation) -> Negotiation: ...
    async def get(self, negotiation_id: UUID) -> Negotiation | None: ...
    async def by_state(self, state: str) -> list[Negotiation]: ...
    async def expired(self) -> list[Negotiation]: ...


class AuditRepositoryPort(Protocol):
    async def append(self, event: AuditEvent) -> AuditEvent: ...
    async def list(self, negotiation_id: UUID | None = None) -> list[AuditEvent]: ...
