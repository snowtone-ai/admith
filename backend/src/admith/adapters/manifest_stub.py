from __future__ import annotations

from uuid import uuid4


class ManifestAdapter:
    async def create_manifest(self, payload: dict[str, object]) -> dict[str, str]:
        return {"manifest_id": str(uuid4())}
