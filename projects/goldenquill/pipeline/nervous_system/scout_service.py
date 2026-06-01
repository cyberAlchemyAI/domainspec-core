import uuid
from typing import Dict, Any

from pipeline.nervous_system.models import ScoutRescanRequest, ScoutRescanResponse, IdentityContext
from pipeline.nervous_system.audit import AuditEvent
from pipeline.nervous_system.audit_proof import global_proof_sink

class ScoutService:
    @staticmethod
    def rescan(request: ScoutRescanRequest, identity: IdentityContext, audit_recorder, global_audit_sink, proof_recorder, chain_id, request_id, model_access_boundary) -> ScoutRescanResponse:
        """
        Orchestrates the Scout rescan workflow.
        This is the governed seam where real execution will eventually live.
        It is wrapped in audit events and delegates to the Model Access Boundary.
        """
        actor_snapshot = {
            "user_id": identity.user_id,
            "is_human": identity.is_human,
            "applied_as": identity.applied_as,
        }

        # 1. Emit start event (audit layer + proof chain)
        audit_recorder.record_event(AuditEvent(
            event_type="scout_rescan_requested",
            request_id=request_id,
            session_id=None,
            active_user_id=identity.user_id,
            licensed_node_id=None,
            licensed_customer_entity_id=None,
            applied_as_entity_id=request.applied_as_entity_id,
            route_mode="backend_posture_unresolved",
            operation_intent="scout_rescan",
            boundary="api_route",
            outcome="validated"
        ))
        proof_recorder.record(
            chain_id=request_id,
            event_type="scout_rescan_requested",
            request_id=request_id,
            actor_snapshot=actor_snapshot,
            applied_as_entity_id=request.applied_as_entity_id,
            route_mode="backend_posture_unresolved",
            operation_intent="scout_rescan",
            boundary="api_route",
            outcome="validated",
        )

        # 2. Invoke boundary; request_id propagates into the ModelAccessDecision
        #    so any downstream transport keeps writing to the same proof chain.
        boundary_response, decision = model_access_boundary.execute_scout_rescan(
            request, request_id=request_id
        )

        # 3. Emit end event (audit layer + proof chain)
        audit_recorder.record_event(AuditEvent(
            event_type="model_access_boundary_invoked",
            request_id=request_id,
            session_id=None,
            active_user_id=identity.user_id,
            licensed_node_id=None,
            licensed_customer_entity_id=None,
            applied_as_entity_id=request.applied_as_entity_id,
            route_mode="backend_posture_unresolved",
            operation_intent="scout_rescan",
            boundary="model_access_boundary_stub",
            outcome="fixture_returned"
        ))
        proof_recorder.record(
            chain_id=request_id,
            event_type="model_access_boundary_invoked",
            request_id=request_id,
            actor_snapshot=actor_snapshot,
            applied_as_entity_id=request.applied_as_entity_id,
            route_mode="backend_posture_unresolved",
            operation_intent="scout_rescan",
            boundary=decision.boundary,
            outcome=decision.execution_mode,
        )

        # 4. Surface reality report from source coverage
        from pipeline.nervous_system.scout_source_roster import summarize_source_coverage
        import datetime

        coverage = summarize_source_coverage()
        fixture_mode = coverage.get("fixture_mode", True)
        status = "source_not_configured" if fixture_mode else "verified"
        notes = "No real source channels configured" if fixture_mode else "Source channels checked."

        channels = coverage.get("channels", []) if isinstance(coverage, dict) else []
        channel_coverage = {}

        for c in channels:
            if not isinstance(c, dict):
                continue
            channel_key = c.get("channel_id") or c.get("source_id")
            if not channel_key:
                continue
            normalized_channel = dict(c)
            normalized_channel.setdefault("channel_id", channel_key)
            normalized_channel.setdefault("source_id", channel_key)
            channel_coverage[channel_key] = normalized_channel

        report = {
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "fixture_mode": fixture_mode,
            "source_status": status,
            "channel_coverage": channel_coverage,
            "available_now": [],
            "impending": [],
            "stale_or_needs_recheck": [],
            "blocked": [],
            "relationship_sourced": [],
            "coalition_required": [],
            "evidence_gaps": [],
            "dormant_or_not_implemented": [],
            "notes": notes
        }
        boundary_response["scout_reality_report"] = report

        # 5. Attach metadata for parity/tests.
        boundary_response["meta"]["audit_event_count"] = len(global_audit_sink.events)
        boundary_response["meta"]["audit_event_types"] = [e.event_type for e in global_audit_sink.events[-2:]]

        # 6. Surface proof-chain pointer (NOT the proof payload) into the response meta.
        proof_chain = global_proof_sink.get_chain(request_id)
        boundary_response["meta"]["proof_chain_id"] = request_id
        boundary_response["meta"]["proof_event_count"] = len(proof_chain.events)
        boundary_response["meta"]["last_event_hash"] = proof_chain.last_hash

        return ScoutRescanResponse(**boundary_response)
