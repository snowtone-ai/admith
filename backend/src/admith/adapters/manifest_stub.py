from __future__ import annotations

from uuid import uuid4

from admith.config import ensure_demo_runtime_allowed


class ManifestAdapter:
    def __init__(self) -> None:
        ensure_demo_runtime_allowed("ManifestAdapter stub")

    async def create_manifest(self, payload: dict[str, object]) -> dict[str, str]:
        return {"manifest_id": str(uuid4())}
