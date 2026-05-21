from __future__ import annotations

from admith.domain.models import (
    Agent,
    AgentMandate,
    Agreement,
    ApprovalDecision,
    ApprovalDecisionValue,
    ApprovalRequest,
    AuditEvent,
    MatchingOutcomeMetric,
    Message,
    MessageType,
    Negotiation,
    NegotiationParticipant,
    OwnerEntity,
    PriceSignalHistory,
    Resource,
    TrustScoreHistory,
)


def test_all_core_entities_validate() -> None:
    owner = OwnerEntity.model_validate({"legal_name": "東京食品工業株式会社", "kyb_status": "verified"})
    agent = Agent.model_validate({"owner_entity_id": owner.owner_entity_id, "domain_capabilities": {"domains": ["food_waste"]}})
    mandate = AgentMandate.model_validate(
        {
            "agent_id": agent.agent_id,
            "owner_entity_id": owner.owner_entity_id,
            "allowed_object_types": ["FoodWasteResource"],
            "allowed_actions": ["CreateCFP"],
            "allowed_regions": ["tokyo"],
            "property_markings": ["phase0_food_waste"],
            "propagation_markings": ["phase0_food_waste"],
            "max_amount_per_deal": "100000",
            "max_amount_per_day": "500000",
        }
    )
    resource = Resource.model_validate({"owner_agent_id": agent.agent_id, "resource_type": "okara", "reservation_price": "-25"})
    negotiation = Negotiation.model_validate({"initiator_agent_id": agent.agent_id, "resource_id": resource.resource_id})
    participant = NegotiationParticipant.model_validate({"negotiation_id": negotiation.negotiation_id, "agent_id": agent.agent_id, "role": "seller"})
    message = Message.model_validate({"negotiation_id": negotiation.negotiation_id, "from_agent_id": agent.agent_id, "message_type": MessageType.CFP, "payload": {}})
    agreement = Agreement.model_validate({"negotiation_id": negotiation.negotiation_id, "terms": {"total_delta_yen": 1}})
    request = ApprovalRequest.model_validate({"negotiation_id": negotiation.negotiation_id, "agreement_id": agreement.agreement_id, "owner_entity_id": owner.owner_entity_id, "expires_at": negotiation.negotiation_ttl_until})
    decision = ApprovalDecision.model_validate({"approval_id": request.approval_id, "decision": ApprovalDecisionValue.APPROVE, "displayed_terms_hash": b"x"})
    audit = AuditEvent.model_validate({"event_type": "x", "event_data": {}, "sequence_number": 1})
    trust = TrustScoreHistory.model_validate({"agent_id": agent.agent_id, "score": "0.8", "calculation_method": "kyb_based"})
    price = PriceSignalHistory.model_validate({"domain_id": "food_waste", "resource_type": "okara", "region": "tokyo", "unit_price_yen": "-3", "quantity_kg": "1000", "agreement_id": agreement.agreement_id})
    metric = MatchingOutcomeMetric.model_validate({"domain_id": "food_waste", "matching_policy": "phase0", "candidate_count": 1, "negotiation_id": negotiation.negotiation_id, "outcome": "settled", "elapsed_seconds": "1"})
    assert mandate.agent_id == agent.agent_id
    assert all([participant, message, decision, audit, trust, price, metric])
