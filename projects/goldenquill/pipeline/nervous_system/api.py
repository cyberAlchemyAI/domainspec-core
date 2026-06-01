import os
import re
import json
import uuid
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from pipeline.nervous_system.models import CommandRequest, ActionRequest, RouteMode, ScoutRescanRequest, ScoutRescanResponse, CurrentProjectionResponse, IdentityContext
from pipeline.nervous_system.governance import (
    require_identity_context,
    enforce_applied_as,
    enforce_route_mode,
    require_human_reauth
)

app = FastAPI(title="Golden Quill Nervous System", version="0.3.0")

SCOUT_DEMO_DATA_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "scout_demo_data.json")

from pipeline.nervous_system.fixtures import load_scout_demo_data

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "Golden Quill Nervous System"}

@app.get("/api/scout/demo")
async def get_scout_demo():
    data = load_scout_demo_data()
    return JSONResponse(content=data)

from pipeline.nervous_system.model_access_boundary import ModelAccessBoundary

@app.post("/api/scout/rescan", response_model=ScoutRescanResponse)
async def scout_rescan(request: ScoutRescanRequest):
    if not request.identity_context:
        raise HTTPException(status_code=400, detail="missing identity_context")
    if not request.applied_as_entity_id:
        raise HTTPException(status_code=400, detail="missing applied_as_entity_id")

    identity = require_identity_context(request.identity_context)
    enforce_applied_as(identity, request.applied_as_entity_id)

    from pipeline.nervous_system.audit import audit_recorder, global_audit_sink
    from pipeline.nervous_system.audit_proof import proof_recorder
    from pipeline.nervous_system.scout_service import ScoutService

    # Use the correlation_id from the envelope as the chain ID, or generate one if missing
    chain_id = request.correlation_id or str(uuid.uuid4())
    request_id = chain_id

    # 4. Handoff to the governed Scout service interface
    return ScoutService.rescan(
        request=request,
        identity=identity,
        audit_recorder=audit_recorder,
        global_audit_sink=global_audit_sink,
        proof_recorder=proof_recorder,
        chain_id=chain_id,
        request_id=request_id,
        model_access_boundary=ModelAccessBoundary
    )

@app.get("/api/projections/current", response_model=CurrentProjectionResponse)
async def get_current_projection(x_identity_context: str = Header(default=None), cycle_id: str = "cyc_default"):
    import json
    if not x_identity_context:
        raise HTTPException(status_code=400, detail="Missing X-Identity-Context header")
    try:
        identity_dict = json.loads(x_identity_context)
        identity = IdentityContext(**identity_dict)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid X-Identity-Context header")

    identity = require_identity_context(identity)
    org_slug = identity.applied_as

    if os.environ.get("TILTH_DEV_FIXTURE_MODE") == "1":
        data = load_scout_demo_data()
        return CurrentProjectionResponse(**data)

    from pipeline.nervous_system.vault_projection_adapter import load_current_projection
    data = load_current_projection(org_slug, cycle_id)
    return CurrentProjectionResponse(**data)

@app.post("/api/commands")
async def run_command(request: CommandRequest):
    # Logician Gate: identity context must be present and valid
    identity = require_identity_context(request.identity_context)

    # Applied As boundary enforcement unconditionally
    enforce_applied_as(identity, request.applied_as_entity_id)

    expected_applied_as = request.payload.get("context", {}).get("org_slug")
    if expected_applied_as and expected_applied_as != request.applied_as_entity_id:
        raise HTTPException(status_code=400, detail="payload.context.org_slug conflicts with envelope applied_as_entity_id")

    if request.command_type == "FINAL_PACKET_AUTHORIZATION":
        require_human_reauth(identity)

    return {"status": "accepted", "command_result": "PROCESSED"}

@app.post("/api/actions/run")
async def run_action(request: ActionRequest):
    identity = require_identity_context(request.identity_context)

    if request.action == "MUTATE_MEMORY":
        raise HTTPException(status_code=403, detail="Actions cannot mutate memory directly. Must go through ledger.")

    from pipeline.nervous_system.action_registry import ActionRegistry
    policy = ActionRegistry.get_policy(request.action)
    if not policy:
        raise HTTPException(status_code=400, detail=f"Unknown or unregistered action: {request.action}")

    if policy.requires_human:
        require_human_reauth(identity)

    # Route mode enforcement based on action policy
    enforce_route_mode(request.route_mode, policy.allowed_route_modes)

    if policy.requires_applied_as:
        if not request.applied_as_entity_id:
            raise HTTPException(status_code=400, detail="Action requires applied_as_entity_id")
        enforce_applied_as(identity, request.applied_as_entity_id)

    # Action execution returns accepted/rejected only
    return {"status": "accepted", "action": request.action}

# We'll serve the React SPA built output if present
REACT_DIST_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "tilth_ui_react", "dist")

if os.path.exists(REACT_DIST_DIR):
    app.mount("/", StaticFiles(directory=REACT_DIST_DIR, html=True), name="react_ui")


