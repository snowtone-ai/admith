from __future__ import annotations

import json
import urllib.request

BASE = "http://localhost:8000"
HEADERS = {"Authorization": "Bearer test-key", "Content-Type": "application/json"}


def post(path: str, payload: dict[str, object]) -> dict[str, object]:
    request = urllib.request.Request(
        f"{BASE}{path}",
        data=json.dumps(payload).encode(),
        headers=HEADERS,
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


def main() -> None:
    for legal_name in ("東京食品工業株式会社", "関東飼料株式会社", "東日本物流株式会社", "Admith運営株式会社"):
        post("/agents", {"legal_name": legal_name, "max_quantity_kg": 5000})
    for resource in (
        {"material": "okara", "quantity_kg": 1000, "disposal_cost_yen": 25000, "required_use": "feed"},
        {"material": "surplus_bread", "quantity_kg": 500, "disposal_cost_yen": 12000, "required_use": "feed"},
    ):
        post("/resources", resource)
    print("seed_demo completed")


if __name__ == "__main__":
    main()
