from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from poc.negotiation import compare_variants


def main() -> int:
    structured, baseline, comparison = compare_variants()
    payload = {
        "structured": _result_summary(structured),
        "baseline": _result_summary(baseline),
        "comparison": asdict(comparison),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if structured.converged and baseline.converged else 1


def _result_summary(result):
    agreement = asdict(result.agreement) if result.agreement else None
    return {
        "variant": result.variant,
        "converged": result.converged,
        "rounds": result.rounds,
        "latency_seconds": round(result.latency_seconds, 6),
        "estimated_cost_usd": result.estimated_cost_usd,
        "agreement": agreement,
        "failure_reason": result.failure_reason,
        "audit_messages": len(result.audit_log),
    }


if __name__ == "__main__":
    raise SystemExit(main())
