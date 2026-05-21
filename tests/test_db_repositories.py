from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

pytest.importorskip("geoalchemy2")

from admith.adapters.db.repositories import (  # noqa: E402
    AUDIT_CHAIN_ADVISORY_LOCK_ID,
    SqlAlchemyAuditEventRepository,
    SqlAlchemyNegotiationRepository,
    SqlAlchemyResourceRepository,
    _resource_row,
)
from admith.adapters.repositories import InMemoryNegotiationRepository, InMemoryResourceRepository  # noqa: E402
from admith.domain.models import Negotiation, NegotiationState, Resource  # noqa: E402


def test_sqlalchemy_repositories_expose_port_methods() -> None:
    session = object()
    resource_repo = SqlAlchemyResourceRepository(session)  # type: ignore[arg-type]
    negotiation_repo = SqlAlchemyNegotiationRepository(session)  # type: ignore[arg-type]
    audit_repo = SqlAlchemyAuditEventRepository(session)  # type: ignore[arg-type]

    assert all(hasattr(resource_repo, name) for name in ("add", "get", "lock_available"))
    assert all(hasattr(negotiation_repo, name) for name in ("add", "get", "by_state", "expired"))
    assert all(hasattr(audit_repo, name) for name in ("append", "list"))


def test_resource_row_converts_wkt_to_geoalchemy_element() -> None:
    resource = Resource(owner_agent_id=uuid4(), resource_type="okara", location="POINT(139.767 35.681)")

    row = _resource_row(resource)

    assert row.location.desc == "POINT(139.767 35.681)"
    assert row.location.srid == 4326


@pytest.mark.asyncio
async def test_in_memory_lock_available_sets_future_lease() -> None:
    repository = InMemoryResourceRepository()
    resource = Resource(owner_agent_id=uuid4(), resource_type="okara")
    await repository.add(resource)

    locked = await repository.lock_available(resource.resource_id, uuid4())

    assert locked is not None
    assert locked.locked_until is not None
    assert locked.locked_until > datetime.now(timezone.utc) + timedelta(minutes=4)


@pytest.mark.asyncio
async def test_in_memory_expired_excludes_terminal_states() -> None:
    repository = InMemoryNegotiationRepository()
    expired_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    active = Negotiation(initiator_agent_id=uuid4(), resource_id=uuid4(), matching_ttl_until=expired_at)
    settled = Negotiation(
        initiator_agent_id=uuid4(),
        resource_id=uuid4(),
        state=NegotiationState.SETTLED,
        matching_ttl_until=expired_at,
    )
    await repository.add(active)
    await repository.add(settled)

    expired = await repository.expired()

    assert [item.negotiation_id for item in expired] == [active.negotiation_id]


def test_audit_repository_uses_advisory_lock_constant() -> None:
    assert isinstance(AUDIT_CHAIN_ADVISORY_LOCK_ID, int)
    assert AUDIT_CHAIN_ADVISORY_LOCK_ID > 0
