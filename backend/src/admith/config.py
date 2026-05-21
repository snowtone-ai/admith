from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

RuntimeMode = Literal["demo", "production"]
RepositoryMode = Literal["memory", "database"]
AdapterMode = Literal["stub", "sandbox", "production"]


class ConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    runtime: RuntimeMode
    repository_mode: RepositoryMode
    econtract_adapter_mode: AdapterMode
    manifest_adapter_mode: AdapterMode


def _read_choice(name: str, default: str, allowed: set[str]) -> str:
    value = os.getenv(name, default).strip().lower()
    if value not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        raise ConfigError(f"{name} must be one of: {allowed_values}")
    return value


def get_settings() -> Settings:
    runtime = _read_choice("ADMITH_RUNTIME", "demo", {"demo", "production"})
    repository_default = "memory" if runtime == "demo" else "database"
    return Settings(
        runtime=runtime,  # type: ignore[arg-type]
        repository_mode=_read_choice("ADMITH_REPOSITORY_MODE", repository_default, {"memory", "database"}),  # type: ignore[arg-type]
        econtract_adapter_mode=_read_choice(
            "ADMITH_ECONTRACT_ADAPTER_MODE",
            "stub",
            {"stub", "sandbox", "production"},
        ),  # type: ignore[arg-type]
        manifest_adapter_mode=_read_choice(
            "ADMITH_MANIFEST_ADAPTER_MODE",
            "stub",
            {"stub", "sandbox", "production"},
        ),  # type: ignore[arg-type]
    )


def ensure_demo_runtime_allowed(component: str, settings: Settings | None = None) -> None:
    effective = settings or get_settings()
    if effective.runtime == "production":
        raise ConfigError(f"{component} is demo-only and cannot be loaded when ADMITH_RUNTIME=production")


def ensure_production_safe_settings(settings: Settings | None = None) -> None:
    effective = settings or get_settings()
    if effective.runtime != "production":
        return
    if effective.repository_mode == "memory":
        raise ConfigError("ADMITH_REPOSITORY_MODE=memory is not allowed when ADMITH_RUNTIME=production")
    if effective.econtract_adapter_mode == "stub":
        raise ConfigError("ADMITH_ECONTRACT_ADAPTER_MODE=stub is not allowed when ADMITH_RUNTIME=production")
    if effective.manifest_adapter_mode == "stub":
        raise ConfigError("ADMITH_MANIFEST_ADAPTER_MODE=stub is not allowed when ADMITH_RUNTIME=production")
