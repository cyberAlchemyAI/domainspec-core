from pipeline.nervous_system.models import ScoutRescanRequest
from pipeline.nervous_system.route_policy import RoutePolicy
from pipeline.nervous_system.provider_adapter import DevProviderAdapter, DisabledProviderAdapter
from fastapi import HTTPException

class ModelAccessBoundary:
    @staticmethod
    def execute_scout_rescan(request: ScoutRescanRequest, request_id: str = "none"):
        """
        Seam for the Model Access Boundary.
        Ensures provider access is governed by RoutePolicy.
        """
        # Posture must be derived from backend authority (e.g., IdentityContext/Operator Manifest)
        # Until Channels A-G are fully wired, we use an unresolved sentinel for audit.
        backend_derived_posture = "backend_posture_unresolved"
        decision = RoutePolicy.evaluate(backend_derived_posture, request.operation_intent or "none")
        decision.request_id = request_id

        if not decision.allowed:
            raise HTTPException(status_code=403, detail=f"Execution denied: {decision.reason}")

        if decision.execution_mode == "deterministic_fixture":
            # Load the fixture internally to own the data handoff
            from pipeline.nervous_system.fixtures import load_scout_demo_data
            data = load_scout_demo_data()
        elif decision.execution_mode == "dev_provider_adapter":
            # Use the dev provider adapter
            from pipeline.nervous_system.transport import ProviderTransportError
            try:
                data = DevProviderAdapter.execute_live(request, decision=decision)
            except ProviderTransportError as e:
                raise HTTPException(status_code=502, detail=f"Provider transport error: {str(e)}")
        elif decision.execution_mode == "dev_real_provider_transport":
            # Use the real provider transport
            from pipeline.nervous_system.transport import ProviderTransportError
            try:
                data = DevProviderAdapter.execute_live(request, use_real_transport=True, decision=decision)
            except ProviderTransportError as e:
                raise HTTPException(status_code=502, detail=f"Provider transport error: {str(e)}")
        else:
            raise HTTPException(status_code=501, detail=f"Unsupported execution mode: {decision.execution_mode}. Live execution not yet wired.")

        # We enforce the expected payload here
        response_payload = {
            "ok": True,
            "scout_pipeline": data.get("scout_pipeline", []),
            "scout_totals": data.get("scout_totals", {}),
            "meta": decision.model_dump()
        }

        return response_payload, decision
