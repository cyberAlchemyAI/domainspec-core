from fastapi import HTTPException
from pipeline.nervous_system.models import IdentityContext, RouteMode

def require_identity_context(identity_context: IdentityContext | None) -> IdentityContext:
    if not identity_context:
        # missing identity_context = 400 malformed envelope
        raise HTTPException(status_code=400, detail="Missing identity_context")
    if not identity_context.token_validity:
        # expired/invalid identity = 403 security failure
        raise HTTPException(status_code=403, detail="Expired/invalid identity token")
    return identity_context

def enforce_applied_as(identity_context: IdentityContext, expected_applied_as: str):
    if identity_context.applied_as != expected_applied_as:
        # policy/export violation = fail closed
        raise HTTPException(status_code=403, detail=f"Unauthorized applied_as context. Expected {expected_applied_as}, got {identity_context.applied_as}")

def enforce_route_mode(requested_mode: str, allowed_modes: list[str]):
    valid_modes = [m.value for m in RouteMode]
    if not requested_mode or requested_mode not in valid_modes:
        raise HTTPException(status_code=400, detail=f"Malformed route mode: {requested_mode}")
    if requested_mode not in allowed_modes:
        raise HTTPException(status_code=403, detail=f"Unauthorized route mode: {requested_mode} not in {allowed_modes}")

def require_human_reauth(identity_context: IdentityContext):
    if not identity_context.is_human:
        raise HTTPException(status_code=403, detail="Final Packet Authorization requires human re-auth")
    if identity_context.origin != "human_direct":
        raise HTTPException(status_code=403, detail="Consequential actions require origin: human_direct")
