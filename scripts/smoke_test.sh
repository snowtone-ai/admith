#!/bin/bash
set -e

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

BASE=${BASE:-http://localhost:8000}
: "${API_KEY:?API_KEY must be set in .env or the shell environment}"
AUTH="Authorization: Bearer ${API_KEY}"

curl -sf "$BASE/health" >/dev/null
RES=$(curl -sf -X POST "$BASE/resources" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"material":"okara","quantity_kg":1000,"disposal_cost_yen":25000,"required_use":"feed"}')
RES_ID=$(echo "$RES" | jq -r .resource_id)
NEG=$(curl -sf -X POST "$BASE/negotiations" -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"resource_id\":\"$RES_ID\",\"buyer_max_price_yen_per_kg\":18}")
NEG_ID=$(echo "$NEG" | jq -r .negotiation_id)
for _ in $(seq 1 "${SMOKE_MAX_ATTEMPTS:-20}"); do
  STATE=$(curl -sf "$BASE/negotiations/$NEG_ID" -H "$AUTH" | jq -r .state)
  [ "$STATE" = "pending_human_approval" ] && break
  sleep "${SMOKE_POLL_SECONDS:-2}"
done
curl -sf -X POST "$BASE/negotiations/$NEG_ID/approve" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"reason":"smoke test approval"}' >/dev/null
for _ in $(seq 1 "${SMOKE_MAX_ATTEMPTS:-20}"); do
  STATE=$(curl -sf "$BASE/negotiations/$NEG_ID" -H "$AUTH" | jq -r .state)
  [ "$STATE" = "settled" ] && break
  sleep "${SMOKE_POLL_SECONDS:-2}"
done
[ "$STATE" = "settled" ] || exit 1
AUDIT_COUNT=$(curl -sf "$BASE/audit-events?negotiation_id=$NEG_ID" -H "$AUTH" | jq length)
[ "$AUDIT_COUNT" -gt 0 ] || exit 1
echo "Smoke test PASSED"
