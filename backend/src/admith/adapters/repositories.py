from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from uuid import UUID, uuid4

from admith.domain.models import AuditEvent, Negotiation, Resource


def canonical_json(value: dict[str, object]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()


class InMemoryResourceRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, Resource] = {}

    async def add(self, resource: Resource) -> Resource:
        self.items[resource.resource_id] = resource
        return resource

    async def get(self, resource_id: UUID) -> Resource | None:
        return self.items.get(resource_id)

    async def lock_available(self, resource_id: UUID, negotiation_id: UUID) -> Resource | None:
        resource = self.items.get(resource_id)
        if resource is None or resource.state != "available":
            return None
        resource.state = "locked"
        resource.lock_token = uuid4()
        resource.locked_by_negotiation_id = negotiation_id
        resource.locked_until = datetime.now(timezone.utc)
        return resource


class InMemoryNegotiationRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, Negotiation] = {}

    async def add(self, negotiation: Negotiation) -> Negotiation:
        self.items[negotiation.negotiation_id] = negotiation
        return negotiation

    async def get(self, negotiation_id: UUID) -> Negotiation | None:
        return self.items.get(negotiation_id)

    async def by_state(self, state: str) -> list[Negotiation]:
        return [item for item in self.items.values() if item.state.value == state]

    async def expired(self) -> list[Negotiation]:
        now = datetime.now(timezone.utc)
        return [item for item in self.items.values() if item.matching_ttl_until < now or item.negotiation_ttl_until < now]


class InMemoryAuditEventRepository:
    def __init__(self) -> None:
        self.items: list[AuditEvent] = []

    async def append(self, event: AuditEvent) -> AuditEvent:
        previous = self.items[-1].event_hash if self.items else b""
        event.sequence_number = len(self.items) + 1
        event.previous_hash = previous
        event.event_hash = hashlib.sha256(canonical_json(event.event_data) + str(event.sequence_number).encode() + previous).digest()
        self.items.append(event)
        return event

    async def list(self, negotiation_id: UUID | None = None) -> list[AuditEvent]:
        if negotiation_id is None:
            return list(self.items)
        return [item for item in self.items if item.negotiation_id == negotiation_id]
