from __future__ import annotations

from decimal import Decimal
from uuid import UUID


def json_model(model):
    return to_jsonable(model.model_dump(mode="python"))


def to_jsonable(value):
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return str(value)
    return value
