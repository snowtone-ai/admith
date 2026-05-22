from __future__ import annotations

import hmac
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from decimal import Decimal
from uuid import UUID

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from admith.api.runtime import (
    active_negotiations_count,
    agents,
    agreements,
    approval_decisions,
    approval_requests,
    approval_workflow,
    audits,
    default_mandate,
    ensure_demo_agent,
    feedback_records,
    json_model,
    mandate_recommendations,
    negotiations,
    orchestrator,
    owners,
    resources,
    scenario_from_resource,
    settlement_service,
)
from admith.api.schemas import AgentCreate, DecisionRequest, NegotiationCreate, ResourceCreate
from admith.config import ensure_production_safe_settings
from admith.domain.approval import canonical_hash
from admith.domain.models import (
    Agent,
    AgentPolicy,
    ApprovalDecisionValue,
    AuditEvent,
    KybStatus,
    Negotiation,
    NegotiationState,
    OwnerEntity,
    Resource,
)
from admith.domain.rule_engine import RuleEngine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    ensure_production_safe_settings()
    yield


app = FastAPI(title="Admith MVP", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_api_key(authorization: str | None = Header(default=None)) -> None:
    expected = os.getenv("API_KEY")
    if not expected:
        raise HTTPException(status_code=503, detail="api_key_not_configured")
    if not hmac.compare_digest(authorization or "", f"Bearer {expected}"):
        raise HTTPException(status_code=401, detail="invalid_api_key")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/resources", dependencies=[Depends(require_api_key)])
async def list_resources(state: str | None = Query(default=None)):
    rows = list(resources.items.values())
    if state:
        rows = [item for item in rows if item.state == state]
    return [json_model(item) for item in rows]


@app.post("/resources", status_code=201, dependencies=[Depends(require_api_key)])
async def create_resource(payload: ResourceCreate):
    owner, agent = ensure_demo_agent()
    resource = Resource(
        owner_agent_id=agent.agent_id,
        resource_type=payload.material,
        attributes={
            "material": payload.material,
            "quantity_kg": payload.quantity_kg,
            "disposal_cost_yen": payload.disposal_cost_yen,
            "required_use": payload.required_use.value,
            "contamination_risk": "low",
        },
        reservation_price=Decimal("-25"),
        location=payload.location,
    )
    await resources.add(resource)
    return json_model(resource)


@app.get("/negotiations", dependencies=[Depends(require_api_key)])
async def list_negotiations(state: str | None = None, pending_approval: bool = False):
    rows = list(negotiations.items.values())
    if state:
        rows = [item for item in rows if item.state.value == state]
    if pending_approval:
        rows = [item for item in rows if item.state == NegotiationState.PENDING_HUMAN_APPROVAL]
    return [json_model(item) for item in rows]


@app.post("/negotiations", status_code=201, dependencies=[Depends(require_api_key)])
async def create_negotiation(payload: NegotiationCreate):
    owner, agent = ensure_demo_agent()
    resource = await resources.get(payload.resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="resource_not_found")
    negotiation = Negotiation(initiator_agent_id=agent.agent_id, resource_id=resource.resource_id)
    locked = await resources.lock_available(resource.resource_id, negotiation.negotiation_id)
    if locked is None:
        raise HTTPException(status_code=409, detail="resource_unavailable")
    scenario = scenario_from_resource(resource, payload.buyer_max_price_yen_per_kg)
    engine = RuleEngine()
    agreement = engine.evaluate(scenario, engine.fair_price(scenario))
    if agreement is None:
        negotiation.state = NegotiationState.FAILED
        await negotiations.add(negotiation)
        return json_model(negotiation)
    agreement.parties = {"seller_agent_id": str(agent.agent_id), "owner_entity_id": str(owner.owner_entity_id)}
    result = orchestrator.advance_to_approval(negotiation, agreement)
    await negotiations.add(result.negotiation)
    agreements[negotiation.negotiation_id] = result.agreement
    for event in result.audit_events:
        await audits.append(event)
    request = approval_workflow.request_approval(result.agreement, result.negotiation, owner.owner_entity_id)
    approval_requests[negotiation.negotiation_id] = request
    await audits.append(AuditEvent(negotiation_id=negotiation.negotiation_id, event_type="approval.requested", event_data={"approval_id": str(request.approval_id)}, sequence_number=0))
    return json_model(result.negotiation)


@app.get("/negotiations/{negotiation_id}", dependencies=[Depends(require_api_key)])
async def get_negotiation(negotiation_id: UUID):
    negotiation = await negotiations.get(negotiation_id)
    if negotiation is None:
        raise HTTPException(status_code=404, detail="negotiation_not_found")
    agreement = agreements.get(negotiation_id)
    events = await audits.list(negotiation_id)
    return {
        **json_model(negotiation),
        "agreement": agreement.model_dump(mode="json") if agreement else None,
        "displayed_terms_hash": canonical_hash(agreement.terms).hex() if agreement else None,
        "approval_request": json_model(approval_requests[negotiation_id]) if negotiation_id in approval_requests else None,
        "audit_events": [json_model(event) for event in events],
    }


@app.post("/negotiations/{negotiation_id}/approve", dependencies=[Depends(require_api_key)])
async def approve_negotiation(negotiation_id: UUID, payload: DecisionRequest):
    if not payload.reason:
        raise HTTPException(status_code=400, detail="reason_required")
    negotiation = await negotiations.get(negotiation_id)
    if negotiation is None:
        raise HTTPException(status_code=404, detail="negotiation_not_found")
    if negotiation.state != NegotiationState.PENDING_HUMAN_APPROVAL:
        raise HTTPException(status_code=400, detail="approval_not_pending")
    agreement = agreements.get(negotiation_id)
    request = approval_requests.get(negotiation_id)
    if agreement is None or request is None:
        raise HTTPException(status_code=404, detail="approval_request_not_found")
    terms_hash = bytes.fromhex(payload.displayed_terms_hash) if payload.displayed_terms_hash else canonical_hash(agreement.terms)
    try:
        decision, recommendation = approval_workflow.decide(
            request,
            agreement,
            terms_hash,
            ApprovalDecisionValue.APPROVE,
            payload.reason,
            negotiation.initiator_agent_id,
        )
    except (TimeoutError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    approval_decisions.append(decision)
    if recommendation is not None:
        mandate_recommendations.append(recommendation)
    for event in orchestrator.settle_after_approval(negotiation):
        await audits.append(event)
    invoice = settlement_service.settle(agreement)
    for name, record in settlement_service.feedback_records(agreement).items():
        feedback_records.append({"type": name, "record": record})
    await audits.append(AuditEvent(negotiation_id=negotiation_id, event_type="settlement.invoice_issued", event_data=invoice, sequence_number=0))
    return json_model(negotiation)


@app.post("/negotiations/{negotiation_id}/reject", dependencies=[Depends(require_api_key)])
async def reject_negotiation(negotiation_id: UUID, payload: DecisionRequest):
    if not payload.reason:
        raise HTTPException(status_code=400, detail="reason_required")
    negotiation = await negotiations.get(negotiation_id)
    if negotiation is None:
        raise HTTPException(status_code=404, detail="negotiation_not_found")
    if negotiation.state != NegotiationState.PENDING_HUMAN_APPROVAL:
        raise HTTPException(status_code=400, detail="approval_not_pending")
    agreement = agreements.get(negotiation_id)
    request = approval_requests.get(negotiation_id)
    if agreement is None or request is None:
        raise HTTPException(status_code=404, detail="approval_request_not_found")
    terms_hash = bytes.fromhex(payload.displayed_terms_hash) if payload.displayed_terms_hash else canonical_hash(agreement.terms)
    try:
        decision, recommendation = approval_workflow.decide(
            request,
            agreement,
            terms_hash,
            ApprovalDecisionValue.REJECT,
            payload.reason,
            negotiation.initiator_agent_id,
        )
    except (TimeoutError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    approval_decisions.append(decision)
    if recommendation is not None:
        mandate_recommendations.append(recommendation)
    negotiation.state = NegotiationState.FAILED
    await audits.append(AuditEvent(negotiation_id=negotiation_id, event_type="action.RejectAgreement", event_data={"reason": payload.reason, "decision_id": str(decision.approval_id)}, sequence_number=0))
    return json_model(negotiation)


@app.get("/agents", dependencies=[Depends(require_api_key)])
async def list_agents():
    return [json_model(item) for item in agents.values()]


@app.post("/agents", status_code=201, dependencies=[Depends(require_api_key)])
async def create_agent(payload: AgentCreate):
    owner = OwnerEntity(legal_name=payload.legal_name, kyb_status=KybStatus.VERIFIED)
    agent = Agent(
        owner_entity_id=owner.owner_entity_id,
        agent_type=payload.agent_type,
        domain_capabilities={"domains": ["food_waste"], "max_quantity_kg": payload.max_quantity_kg},
        policy=AgentPolicy(model_tier=1),
    )
    owners[owner.owner_entity_id] = owner
    agents[agent.agent_id] = agent
    return {"owner": json_model(owner), "agent": json_model(agent), "mandate": json_model(default_mandate(agent, owner))}


@app.get("/audit-events", dependencies=[Depends(require_api_key)])
async def list_audit_events(negotiation_id: UUID | None = None):
    return [json_model(item) for item in await audits.list(negotiation_id)]


@app.get("/dashboard/metrics", dependencies=[Depends(require_api_key)])
async def dashboard_metrics():
    pending = [item for item in negotiations.items.values() if item.state == NegotiationState.PENDING_HUMAN_APPROVAL]
    delta = sum(int(getattr(agreements.get(item.negotiation_id), "terms", {}).get("total_delta_yen", 0)) for item in negotiations.items.values())
    return {"active_negotiations": active_negotiations_count(), "pending_approvals": len(pending), "today_delta_yen": delta}
