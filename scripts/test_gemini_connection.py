from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from poc.gemini_client import (
    DEFAULT_MODEL,
    GeminiError,
    discover_preferred_models,
    generate_with_available_model,
)


def main() -> int:
    print(f"Gemini connection test started: model={DEFAULT_MODEL}")
    try:
        preferred_models = discover_preferred_models()
        print(f"models_list_ok=true count={len(preferred_models)}")
    except GeminiError as exc:
        print(f"models_list_ok=false reason={exc}")
        preferred_models = None

    try:
        model, result, failures = generate_with_available_model(
            "Reply with exactly: admith-ok",
            temperature=0.0,
            max_output_tokens=64,
            preferred_models=preferred_models,
        )
    except GeminiError as exc:
        print(f"Gemini connection test failed: {exc}")
        return 1

    print("Gemini connection test succeeded")
    if failures:
        print("primary_model_unavailable=true")
        print(f"fallback_reason={DEFAULT_MODEL} was attempted first but was unavailable")
    print(f"model_used={model}")
    print(f"response={result.text.strip()}")
    print(f"tokens={result.total_tokens}")
    print(f"estimated_cost_usd={result.cost_usd:.8f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
