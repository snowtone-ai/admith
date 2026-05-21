from __future__ import annotations

import pytest

from admith.config import ConfigError, Settings, ensure_demo_runtime_allowed, ensure_production_safe_settings, get_settings


def test_default_runtime_is_demo_memory(monkeypatch) -> None:
    for name in (
        "ADMITH_RUNTIME",
        "ADMITH_REPOSITORY_MODE",
        "ADMITH_ECONTRACT_ADAPTER_MODE",
        "ADMITH_MANIFEST_ADAPTER_MODE",
    ):
        monkeypatch.delenv(name, raising=False)

    settings = get_settings()

    assert settings.runtime == "demo"
    assert settings.repository_mode == "memory"
    assert settings.econtract_adapter_mode == "stub"
    assert settings.manifest_adapter_mode == "stub"


def test_demo_runtime_components_fail_closed_in_production() -> None:
    settings = Settings(
        runtime="production",
        repository_mode="database",
        econtract_adapter_mode="sandbox",
        manifest_adapter_mode="sandbox",
    )

    with pytest.raises(ConfigError, match="demo-only"):
        ensure_demo_runtime_allowed("admith.api.runtime", settings)


def test_production_rejects_memory_repository() -> None:
    settings = Settings(
        runtime="production",
        repository_mode="memory",
        econtract_adapter_mode="sandbox",
        manifest_adapter_mode="sandbox",
    )

    with pytest.raises(ConfigError, match="memory"):
        ensure_production_safe_settings(settings)


def test_production_rejects_stub_external_adapters() -> None:
    settings = Settings(
        runtime="production",
        repository_mode="database",
        econtract_adapter_mode="stub",
        manifest_adapter_mode="sandbox",
    )

    with pytest.raises(ConfigError, match="ECONTRACT"):
        ensure_production_safe_settings(settings)


@pytest.mark.asyncio
async def test_fastapi_lifespan_runs_production_safety_check(monkeypatch) -> None:
    from admith.api.main import app, lifespan

    monkeypatch.setenv("ADMITH_RUNTIME", "production")
    monkeypatch.setenv("ADMITH_REPOSITORY_MODE", "memory")
    monkeypatch.setenv("ADMITH_ECONTRACT_ADAPTER_MODE", "sandbox")
    monkeypatch.setenv("ADMITH_MANIFEST_ADAPTER_MODE", "sandbox")

    with pytest.raises(ConfigError, match="memory"):
        async with lifespan(app):
            pass
