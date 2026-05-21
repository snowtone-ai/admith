from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-3.5-flash"
FALLBACK_MODELS = ("gemini-2.5-flash", "gemini-2.0-flash")
GENERATE_CONTENT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
LIST_MODELS_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
INPUT_USD_PER_MILLION_TOKENS = 0.40
OUTPUT_USD_PER_MILLION_TOKENS = 1.20


class GeminiError(RuntimeError):
    pass


@dataclass(frozen=True)
class GeminiResult:
    text: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    latency_seconds: float


def load_env_file(path: Path = ROOT_DIR / ".env.local") -> None:
    if not path.exists():
        raise GeminiError(f"Environment file not found: {path}")

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def require_api_key() -> str:
    load_env_file()
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise GeminiError("GEMINI_API_KEY is missing in .env.local")
    return api_key


class GeminiClient:
    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.model = model
        self.api_key = require_api_key()

    def generate_text(self, prompt: str, *, temperature: float = 0.2, max_output_tokens: int = 256) -> GeminiResult:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        request_body = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens,
            },
        }
        payload = json.dumps(request_body).encode("utf-8")
        request = urllib.request.Request(
            GENERATE_CONTENT_ENDPOINT.format(model=self.model),
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            },
            method="POST",
        )

        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise GeminiError(f"Gemini API HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise GeminiError(f"Gemini API request failed: {exc.reason}") from exc

        latency_seconds = time.perf_counter() - started
        data = json.loads(response_body)
        text = _extract_text(data)
        usage = data.get("usageMetadata", {})
        input_tokens = int(usage.get("promptTokenCount", 0))
        output_tokens = int(usage.get("candidatesTokenCount", 0))
        total_tokens = int(usage.get("totalTokenCount", input_tokens + output_tokens))
        cost_usd = _estimate_cost_usd(input_tokens, output_tokens)

        return GeminiResult(
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_usd=cost_usd,
            latency_seconds=latency_seconds,
        )


def list_available_models() -> list[str]:
    api_key = require_api_key()
    request = urllib.request.Request(
        LIST_MODELS_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise GeminiError(f"Gemini models.list HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise GeminiError(f"Gemini models.list request failed: {exc.reason}") from exc

    data = json.loads(response_body)
    models = data.get("models", [])
    names: list[str] = []
    for model in models:
        if not isinstance(model, dict):
            continue
        methods = model.get("supportedGenerationMethods", [])
        if "generateContent" not in methods:
            continue
        raw_name = str(model.get("name", "")).strip()
        if not raw_name.startswith("models/"):
            continue
        names.append(raw_name.split("/", 1)[1])
    return names


def discover_preferred_models() -> tuple[str, ...]:
    discovered = list_available_models()
    discovered_set = set(discovered)
    ordered: list[str] = []

    # Preserve explicit preference first, then add discovered flash models.
    for candidate in (DEFAULT_MODEL, *FALLBACK_MODELS):
        if candidate in discovered_set:
            ordered.append(candidate)

    flash_models = sorted(
        model for model in discovered if model.startswith("gemini-") and "flash" in model
    )
    for model in flash_models:
        if model not in ordered:
            ordered.append(model)

    if ordered:
        return tuple(ordered)
    return (DEFAULT_MODEL, *FALLBACK_MODELS)


def generate_with_available_model(
    prompt: str,
    *,
    temperature: float = 0.2,
    max_output_tokens: int = 256,
    preferred_models: tuple[str, ...] | None = None,
) -> tuple[str, GeminiResult, list[str]]:
    if preferred_models is None:
        preferred_models = discover_preferred_models()

    failures: list[str] = []
    for model in preferred_models:
        client = GeminiClient(model=model)
        try:
            return model, client.generate_text(
                prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ), failures
        except GeminiError as exc:
            failures.append(f"{model}: {exc}")
    raise GeminiError("All Gemini model attempts failed:\n" + "\n".join(failures))


def _extract_text(data: dict[str, Any]) -> str:
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise GeminiError(f"Gemini response has no candidates: {json.dumps(data, ensure_ascii=False)[:500]}")

    parts = candidates[0].get("content", {}).get("parts", [])
    texts = [part.get("text", "") for part in parts if isinstance(part, dict)]
    text = "\n".join(value for value in texts if value).strip()
    if not text:
        raise GeminiError(f"Gemini response candidate has no text: {json.dumps(candidates[0], ensure_ascii=False)[:500]}")
    return text


def _estimate_cost_usd(input_tokens: int, output_tokens: int) -> float:
    input_cost = (input_tokens / 1_000_000) * INPUT_USD_PER_MILLION_TOKENS
    output_cost = (output_tokens / 1_000_000) * OUTPUT_USD_PER_MILLION_TOKENS
    return round(input_cost + output_cost, 8)
