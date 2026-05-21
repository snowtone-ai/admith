from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from uuid import UUID, uuid4

from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from admith.adapters.db.orm import AuditEventRow, NegotiationRow, ResourceRow
from admith.adapters.repositories import RESOURCE_LOCK_LEASE, canonical_json
from admith.domain.models import AuditEvent, Negotiation, NegotiationState, Resource

AUDIT_CHAIN_ADVISORY_LOCK_ID = 4_120_030


def _resource_location_to_db(location: str) -> WKTElement:
    return WKTElement(location, srid=4326)


def _resource_location_from_db(location: object) -> str:
    if isinstance(location, str):
        return location
    data = getattr(location, "data", None)
    return data if isinstance(data, str) else str(location)


def _resource_row(resource: Resource) -> ResourceRow:
    values = resource.model_dump(mode="python")
    values["location"] = _resource_location_to_db(resource.location)
    return ResourceRow(**values)


def _resource_model(row: ResourceRow) -> Resource:
    values = {column.name: getattr(row, column.name) for column in ResourceRow.__table__.columns}
    values["location"] = _resource_location_from_db(values["location"])
    return Resource.model_validate(values)


def _negotiation_row(negotiation: Negotiation) -> NegotiationRow:
    return NegotiationRow(**negotiation.model_dump(mode="python"))


def _negotiation_model(row: NegotiationRow) -> Negotiation:
    return Negotiation.model_validate({column.name: getattr(row, column.name) for column in NegotiationRow.__table__.columns})


def _audit_row(event: AuditEvent) -> AuditEventRow:
    return AuditEventRow(**event.model_dump(mode="python"))


def _audit_model(row: AuditEventRow) -> AuditEvent:
    return AuditEvent.model_validate({column.name: getattr(row, column.name) for column in AuditEventRow.__table__.columns})


class SqlAlchemyResourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, resource: Resource) -> Resource:
        self.session.add(_resource_row(resource))
        await self.session.flush()
        return resource

    async def get(self, resource_id: UUID) -> Resource | None:
        row = await self.session.get(ResourceRow, resource_id)
        return _resource_model(row) if row is not None else None

    async def lock_available(self, resource_id: UUID, negotiation_id: UUID) -> Resource | None:
        result = await self.session.execute(
            select(ResourceRow)
            .where(ResourceRow.resource_id == resource_id, ResourceRow.state == "available")
            .with_for_update(skip_locked=True)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        row.state = "locked"
        row.lock_token = uuid4()
        row.locked_by_negotiation_id = negotiation_id
        row.locked_until = datetime.now(timezone.utc) + RESOURCE_LOCK_LEASE
        await self.session.flush()
        return _resource_model(row)


class SqlAlchemyNegotiationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, negotiation: Negotiation) -> Negotiation:
        await self.session.merge(_negotiation_row(negotiation))
        await self.session.flush()
        return negotiation

    async def get(self, negotiation_id: UUID) -> Negotiation | None:
        row = await self.session.get(NegotiationRow, negotiation_id)
        return _negotiation_model(row) if row is not None else None

    async def by_state(self, state: str) -> list[Negotiation]:
        result = await self.session.execute(select(NegotiationRow).where(NegotiationRow.state == state))
        return [_negotiation_model(row) for row in result.scalars()]

    async def expired(self) -> list[Negotiation]:
        now = datetime.now(timezone.utc)
        terminal = {NegotiationState.SETTLED.value, NegotiationState.FAILED.value, NegotiationState.EXPIRED.value}
        result = await self.session.execute(
            select(NegotiationRow).where(
                NegotiationRow.state.not_in(terminal),
                (NegotiationRow.matching_ttl_until < now) | (NegotiationRow.negotiation_ttl_until < now),
            )
        )
        return [_negotiation_model(row) for row in result.scalars()]


class SqlAlchemyAuditEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def append(self, event: AuditEvent) -> AuditEvent:
        await self.session.execute(select(func.pg_advisory_xact_lock(AUDIT_CHAIN_ADVISORY_LOCK_ID)))
        previous_result = await self.session.execute(
            select(AuditEventRow).order_by(AuditEventRow.sequence_number.desc()).limit(1)
        )
        previous = previous_result.scalar_one_or_none()
        event.sequence_number = 1 if previous is None else previous.sequence_number + 1
        event.previous_hash = b"" if previous is None else previous.event_hash
        event.event_hash = hashlib.sha256(
            canonical_json(event.event_data) + str(event.sequence_number).encode() + event.previous_hash
        ).digest()
        self.session.add(_audit_row(event))
        await self.session.flush()
        return event

    async def list(self, negotiation_id: UUID | None = None) -> list[AuditEvent]:
        statement = select(AuditEventRow).order_by(AuditEventRow.sequence_number)
        if negotiation_id is not None:
            statement = statement.where(AuditEventRow.negotiation_id == negotiation_id)
        result = await self.session.execute(statement)
        return [_audit_model(row) for row in result.scalars()]
