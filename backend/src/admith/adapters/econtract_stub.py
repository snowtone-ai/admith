from __future__ import annotations

from uuid import uuid4


class EContractAdapter:
    async def create_contract(self, payload: dict[str, object]) -> dict[str, str]:
        return {"contract_id": str(uuid4())}
