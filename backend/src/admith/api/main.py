from __future__ import annotations

# ruff: noqa: B008
import hmac
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from decimal import Decimal
from uuid import UUID

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from admith.api.dependencies import AppState, DbRuntime, get_memory_state, get_state
from admith.api.runtime import json_model
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

memory_state = get_memory_state()
approval_decisions = memory_state.approval_decisions
feedback_records = memory_state.feedback_records


async def ensure_demo_agent(runtime: AppState | DbRuntime) -> tuple[OwnerEntity, Agent]:
    if isinstance(runtime, DbRuntime):
        return await runtime.ensure_demo_agent()
    return runtime.ensure_demo_agent()


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
async def list_resources(state: str | None = Query(default=None), runtime: AppState | DbRuntime = Depends(get_state)):
    if isinstance(runtime, DbRuntime):
        if state:
            raise HTTPException(status_code=400, detail="state_filter_not_supported_in_db_mode")
        return []
    rows = list(runtime.resources.items.values())
    if state:
        rows = [item for item in rows if item.state == state]
    return [json_model(item) for item in rows]


@app.post("/resources", status_code=201, dependencies=[Depends(require_api_key)])
async def create_resource(payload: ResourceCreate, runtime: AppState | DbRuntime = Depends(get_state)):
    _, agent = await ensure_demo_agent(runtime)
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
    await runtime.resources.add(resource)
    return json_model(resource)


@app.get("/negotiations", dependencies=[Depends(require_api_key)])
async def list_negotiations(
    state: str | None = None,
    pending_approval: bool = False,
    runtime: AppState | DbRuntime = Depends(get_state),
):
    if isinstance(runtime, DbRuntime):
        target = state or (NegotiationState.PENDING_HUMAN_APPROVAL.value if pending_approval else None)
        if target is None:
            return []
        rows = await runtime.negotiations.by_state(target)
        return [json_model(item) for item in rows]

    rows = list(runtime.negotiations.items.values())
    if state:
        rows = [item for item in rows if item.state.value == state]
    if pending_approval:
        rows = [item for item in rows if item.state == NegotiationState.PENDING_HUMAN_APPROVAL]
    return [json_model(item) for item in rows]


@app.post("/negotiations", status_code=201, dependencies=[Depends(require_api_key)])
async def create_negotiation(payload: NegotiationCreate, runtime: AppState | DbRuntime = Depends(get_state)):
    owner, agent = await ensure_demo_agent(runtime)
    resource = await runtime.resources.get(payload.resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="resource_not_found")
    negotiation = Negotiation(initiator_agent_id=agent.agent_id, resource_id=resource.resource_id)
    locked = await runtime.resources.lock_available(resource.resource_id, negotiation.negotiation_id)
    if locked is None:
        raise HTTPException(status_code=409, detail="resource_unavailable")
    scenario = memory_state.scenario_from_resource(resource, payload.buyer_max_price_yen_per_kg)
    engine = RuleEngine()
    agreement = engine.evaluate(scenario, engine.fair_price(scenario))
    if agreement is None:
        negotiation.state = NegotiationState.FAILED
        await runtime.negotiations.add(negotiation)
        return json_model(negotiation)
    agreement.parties = {"seller_agent_id": str(agent.agent_id), "owner_entity_id": str(owner.owner_entity_id)}
    result = memory_state.orchestrator.advance_to_approval(negotiation, agreement)
    await runtime.negotiations.add(result.negotiation)
    memory_state.agreements[negotiation.negotiation_id] = result.agreement
    for event in result.audit_events:
        await runtime.audits.append(event)
    request = memory_state.approval_workflow.request_approval(result.agreement, result.negotiation, owner.owner_entity_id)
    memory_state.approval_requests[negotiation.negotiation_id] = request
    await runtime.audits.append(
        AuditEvent(
            negotiation_id=negotiation.negotiation_id,
            event_type="approval.requested",
            event_data={"approval_id": str(request.approval_id)},
            sequence_number=0,
        )
    )
    return json_model(result.negotiation)


@app.get("/negotiations/{negotiation_id}", dependencies=[Depends(require_api_key)])
async def get_negotiation(negotiation_id: UUID, runtime: AppState | DbRuntime = Depends(get_state)):
    negotiation = await runtime.negotiations.get(negotiation_id)
    if negotiation is None:
        raise HTTPException(status_code=404, detail="negotiation_not_found")
    agreement = memory_state.agreements.get(negotiation_id)
    events = await runtime.audits.list(negotiation_id)
    return {
        **json_model(negotiation),
        "agreement": agreement.model_dump(mode="json") if agreement else None,
        "displayed_terms_hash": canonical_hash(agreement.terms).hex() if agreement else None,
        "approval_request": (
            json_model(memory_state.approval_requests[negotiation_id]) if negotiation_id in memory_state.approval_requests else None
        ),
        "audit_events": [json_model(event) for event in events],
    }


@app.post("/negotiations/{negotiation_id}/approve", dependencies=[Depends(require_api_key)])
async def approve_negotiation(negotiation_id: UUID, payload: DecisionRequest, runtime: AppState | DbRuntime = Depends(get_state)):
    if not payload.reason:
        raise HTTPException(status_code=400, detail="reason_required")
    negotiation = await runtime.negotiations.get(negotiation_id)
    if negotiation is None:
        raise HTTPException(status_code=404, detail="negotiation_not_found")
    if negotiation.state != NegotiationState.PENDING_HUMAN_APPROVAL:
        raise HTTPException(status_code=400, detail="approval_not_pending")
    agreement = memory_state.agreements.get(negotiation_id)
    request = memory_state.approval_requests.get(negotiation_id)
    if agreement is None or request is None:
        raise HTTPException(status_code=404, detail="approval_request_not_found")
    terms_hash = bytes.fromhex(payload.displayed_terms_hash) if payload.displayed_terms_hash else canonical_hash(agreement.terms)
    try:
        decision, recommendation = memory_state.approval_workflow.decide(
            request,
            agreement,
            terms_hash,
            ApprovalDecisionValue.APPROVE,
            payload.reason,
            negotiation.initiator_agent_id,
        )
    except (TimeoutError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    memory_state.approval_decisions.append(decision)
    if recommendation is not None:
        memory_state.mandate_recommendations.append(recommendation)
    for event in memory_state.orchestrator.settle_after_approval(negotiation):
        await runtime.audits.append(event)
    invoice = memory_state.settlement_service.settle(agreement)
    for name, record in memory_state.settlement_service.feedback_records(agreement).items():
        memory_state.feedback_records.append({"type": name, "record": record})
    await runtime.audits.append(
        AuditEvent(
            negotiation_id=negotiation_id,
            event_type="settlement.invoice_issued",
            event_data=invoice,
            sequence_number=0,
        )
    )
    return json_model(negotiation)


@app.post("/negotiations/{negotiation_id}/reject", dependencies=[Depends(require_api_key)])
async def reject_negotiation(negotiation_id: UUID, payload: DecisionRequest, runtime: AppState | DbRuntime = Depends(get_state)):
    if not payload.reason:
        raise HTTPException(status_code=400, detail="reason_required")
    negotiation = await runtime.negotiations.get(negotiation_id)
    if negotiation is None:
        raise HTTPException(status_code=404, detail="negotiation_not_found")
    if negotiation.state != NegotiationState.PENDING_HUMAN_APPROVAL:
        raise HTTPException(status_code=400, detail="approval_not_pending")
    agreement = memory_state.agreements.get(negotiation_id)
    request = memory_state.approval_requests.get(negotiation_id)
    if agreement is None or request is None:
        raise HTTPException(status_code=404, detail="approval_request_not_found")
    terms_hash = bytes.fromhex(payload.displayed_terms_hash) if payload.displayed_terms_hash else canonical_hash(agreement.terms)
    try:
        decision, recommendation = memory_state.approval_workflow.decide(
            request,
            agreement,
            terms_hash,
            ApprovalDecisionValue.REJECT,
            payload.reason,
            negotiation.initiator_agent_id,
        )
    except (TimeoutError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    memory_state.approval_decisions.append(decision)
    if recommendation is not None:
        memory_state.mandate_recommendations.append(recommendation)
    negotiation.state = NegotiationState.FAILED
    await runtime.audits.append(
        AuditEvent(
            negotiation_id=negotiation_id,
            event_type="action.RejectAgreement",
            event_data={"reason": payload.reason, "decision_id": str(decision.approval_id)},
            sequence_number=0,
        )
    )
    return json_model(negotiation)


@app.get("/agents", dependencies=[Depends(require_api_key)])
async def list_agents(runtime: AppState | DbRuntime = Depends(get_state)):
    if isinstance(runtime, DbRuntime):
        return []
    return [json_model(item) for item in runtime.agents.values()]


@app.post("/agents", status_code=201, dependencies=[Depends(require_api_key)])
async def create_agent(payload: AgentCreate, runtime: AppState | DbRuntime = Depends(get_state)):
    owner = OwnerEntity(legal_name=payload.legal_name, kyb_status=KybStatus.VERIFIED)
    agent = Agent(
        owner_entity_id=owner.owner_entity_id,
        agent_type=payload.agent_type,
        domain_capabilities={"domains": ["food_waste"], "max_quantity_kg": payload.max_quantity_kg},
        policy=AgentPolicy(model_tier=1),
    )
    if isinstance(runtime, DbRuntime):
        await runtime.create_owner_agent(owner, agent)
        return {"owner": json_model(owner), "agent": json_model(agent), "mandate": json_model(memory_state.default_mandate(agent, owner))}
    runtime.owners[owner.owner_entity_id] = owner
    runtime.agents[agent.agent_id] = agent
    return {"owner": json_model(owner), "agent": json_model(agent), "mandate": json_model(runtime.default_mandate(agent, owner))}


@app.get("/audit-events", dependencies=[Depends(require_api_key)])
async def list_audit_events(negotiation_id: UUID | None = None, runtime: AppState | DbRuntime = Depends(get_state)):
    return [json_model(item) for item in await runtime.audits.list(negotiation_id)]


@app.get("/dashboard/metrics", dependencies=[Depends(require_api_key)])
async def dashboard_metrics(runtime: AppState | DbRuntime = Depends(get_state)):
    if isinstance(runtime, DbRuntime):
        return {"active_negotiations": 0, "pending_approvals": 0, "today_delta_yen": 0}
    pending = [item for item in runtime.negotiations.items.values() if item.state == NegotiationState.PENDING_HUMAN_APPROVAL]
    delta = sum(
        int(getattr(memory_state.agreements.get(item.negotiation_id), "terms", {}).get("total_delta_yen", 0))
        for item in runtime.negotiations.items.values()
    )
    return {"active_negotiations": runtime.active_negotiations_count(), "pending_approvals": len(pending), "today_delta_yen": delta}
