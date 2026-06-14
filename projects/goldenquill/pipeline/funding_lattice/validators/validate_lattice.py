import sys
import yaml
from pipeline.funding_lattice.models import Entity, OpportunityTarget, RouteLock, PacketState, ContextBundleManifest

def validate_target(target, known_entities):
    errors = []
    if not hasattr(target, 'route_lock') or target.route_lock is None:
        errors.append("Target missing route_lock")

    if not hasattr(target, 'packet_state') or target.packet_state is None:
        errors.append("Target missing packet_state")

    if getattr(target, 'route_lock', None):
        if target.route_lock.route_status == "MISSING":
            if target.lifecycle_stage == "DRAFTING_ELIGIBLE":
                errors.append("MISSING route_status cannot have DRAFTING_ELIGIBLE lifecycle_stage")
            if "route_lock_missing" not in getattr(target, 'fatal_gates', []):
                errors.append("MISSING route_status must have route_lock_missing in fatal_gates")

        if target.route_lock.authorization_record_required and not target.route_lock.authorization_record_present:
            if target.route_lock.route_status == "VALID":
                errors.append("Route status cannot be VALID if authorization is required but missing")

        if target.route_lock.applied_as_entity_id:
            if target.route_lock.applied_as_entity_id not in [e.entity_id for e in known_entities]:
                if target.route_lock.route_status not in ["INVALID", "BLOCKED"]:
                    errors.append("Unknown applied_as_entity_id requires INVALID or BLOCKED route_status")

    if getattr(target, 'packet_state', None):
        if target.packet_state.export_staged and not target.packet_state.operator_authorization_required:
            errors.append("If export_staged, operator_authorization_required must be true")

        if not target.packet_state.operator_authorization_present and not target.packet_state.export_blocked:
            errors.append("If operator_authorization_present is false, export_blocked must be true")

    return errors

def validate_entity_data(data):
    errors = []
    required = ["entity_id", "display_name", "entity_type", "legal_status"]
    for req in required:
        if req not in data or not data[req]:
            errors.append(f"Entity missing required field: {req}")
    return errors

def parse_target(data):
    route_lock_data = data.get("route_lock", {})
    packet_state_data = data.get("packet_state", {})
    manifest_data = data.get("context_bundle_manifest")

    rl = RouteLock(**route_lock_data) if route_lock_data else None
    ps = PacketState(**packet_state_data) if packet_state_data else None
    cbm = ContextBundleManifest(**manifest_data) if manifest_data else None

    kwargs = {k: v for k, v in data.items() if k not in ["route_lock", "packet_state", "context_bundle_manifest"]}

    # Very basic validation of required fields for target
    required = ["opportunity_id", "title", "verification_status", "lifecycle_stage"]
    for req in required:
        if req not in kwargs or not kwargs[req]:
            raise ValueError(f"Target missing required field: {req}")

    return OpportunityTarget(
        route_lock=rl,
        packet_state=ps,
        context_bundle_manifest=cbm,
        **kwargs
    )

def validate_file(path, known_entities=None):
    if known_entities is None:
        known_entities = []

    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        return ["File does not contain a valid YAML dictionary"]

    # Infer type
    if "entity_id" in data:
        # Entity
        errs = validate_entity_data(data)
        if errs:
            return errs
        # Build Entity object to ensure it works
        try:
            Entity(**data)
        except Exception as e:
            return [f"Entity structure error: {e}"]
        return []
    elif "opportunity_id" in data:
        # Target
        try:
            target = parse_target(data)
        except Exception as e:
            return [f"Target structure error: {e}"]

        return validate_target(target, known_entities)
    else:
        return ["Unknown document type: missing both entity_id and opportunity_id"]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        has_errors = False
        for path in sys.argv[1:]:
            try:
                errors = validate_file(path)
                if errors:
                    has_errors = True
                    sys.stderr.write(f"Validation failed for {path}:\n")
                    for err in errors:
                        sys.stderr.write(f"  - {err}\n")
                else:
                    print(f"Validation passed for {path}")
            except Exception as e:
                has_errors = True
                sys.stderr.write(f"Fatal error reading {path}: {e}\n")

        if has_errors:
            sys.exit(1)
        sys.exit(0)
