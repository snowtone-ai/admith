from __future__ import annotations

from uuid import uuid4

from admith.config import ensure_demo_runtime_allowed


class EContractAdapter:
    def __init__(self) -> None:
        ensure_demo_runtime_allowed("EContractAdapter stub")

    async def create_contract(self, payload: dict[str, object]) -> dict[str, str]:
        return {"contract_id": str(uuid4())}
