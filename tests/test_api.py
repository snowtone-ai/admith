from __future__ import annotations

from fastapi.testclient import TestClient

from admith.api.main import app, approval_decisions, feedback_records


def test_api_smoke_path_and_auth() -> None:
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    assert client.get("/resources").status_code == 401
    headers = {"Authorization": "Bearer test-key"}
    resource = client.post(
        "/resources",
        headers=headers,
        json={"material": "okara", "quantity_kg": 1000, "disposal_cost_yen": 25000, "required_use": "feed"},
    )
    assert resource.status_code == 201
    negotiation = client.post(
        "/negotiations",
        headers=headers,
        json={"resource_id": resource.json()["resource_id"], "buyer_max_price_yen_per_kg": 18},
    )
    assert negotiation.status_code == 201
    negotiation_id = negotiation.json()["negotiation_id"]
    detail = client.get(f"/negotiations/{negotiation_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["state"] == "pending_human_approval"
    tampered = client.post(
        f"/negotiations/{negotiation_id}/approve",
        headers=headers,
        json={"reason": "bad hash", "displayed_terms_hash": "00"},
    )
    assert tampered.status_code == 400
    approved = client.post(f"/negotiations/{negotiation_id}/approve", headers=headers, json={"reason": "ok"})
    assert approved.status_code == 200
    assert approved.json()["state"] == "settled"
    assert approval_decisions
    assert {item["type"] for item in feedback_records} >= {"trust", "price", "mandate", "matching"}
    assert client.get("/negotiations/00000000-0000-0000-0000-000000000000", headers=headers).status_code == 404
