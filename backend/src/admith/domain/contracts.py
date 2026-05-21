from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class Terms:
    resource_type: str
    quantity_kg: Decimal
    transfer_price_yen_per_kg: Decimal
    total_delta_yen: Decimal
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ResourceEnvelope:
    resource_id: UUID
    domain_id: str
    resource_type: str
    attributes: dict[str, Any]
    security_markings: tuple[str, ...]
    ontology_version: str
