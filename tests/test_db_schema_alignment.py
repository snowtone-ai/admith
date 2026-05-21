from __future__ import annotations

import pytest

pytest.importorskip("geoalchemy2")

from admith.adapters.db.orm import AgentMandateRow, AgreementRow, NegotiationRow


def _columns(row_type: type) -> set[str]:
    return set(row_type.__table__.columns.keys())


def test_agent_mandate_orm_covers_dynamic_security_fields() -> None:
    expected = {
        "allowed_object_types",
        "allowed_actions",
        "allowed_regions",
        "property_markings",
        "propagation_markings",
        "max_amount_per_deal",
        "max_amount_per_day",
        "max_quantity_per_deal",
        "currency",
        "allowed_counterparties",
        "approval_mode",
        "approval_threshold",
        "revoked_at",
        "revoked_reason",
        "mandate_signature",
    }

    assert expected <= _columns(AgentMandateRow)


def test_negotiation_orm_covers_all_ttl_columns() -> None:
    assert {"matching_ttl_until", "negotiation_ttl_until", "approval_ttl_until", "pickup_deadline", "settlement_ttl_until"} <= _columns(NegotiationRow)


def test_agreement_is_unique_per_negotiation() -> None:
    constraints = {constraint.name for constraint in AgreementRow.__table__.constraints}
    assert "uq_agreements_negotiation_id" in constraints
