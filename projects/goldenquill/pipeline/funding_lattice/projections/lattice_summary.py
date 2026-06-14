import yaml
import os

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def summarize_lattice(entities_dir, targets_dir):
    summary = []
    for filename in os.listdir(targets_dir):
        if not filename.endswith('.yaml'):
            continue
        data = load_yaml(os.path.join(targets_dir, filename))

        opportunity_id = data.get('opportunity_id')
        title = data.get('title')
        verification_status = data.get('verification_status')
        lifecycle_stage = data.get('lifecycle_stage')
        route_lock = data.get('route_lock', {})
        applied_as_entity_id = route_lock.get('applied_as_entity_id')
        beneficiary_entity_id = route_lock.get('beneficiary_entity_id')
        sponsor_entity_id = route_lock.get('sponsor_entity_id')
        route_status = route_lock.get('route_status')
        fatal_gates_count = len(data.get('fatal_gates', []))
        advisory_warnings_count = len(data.get('advisory_warnings', []))
        packet_state = data.get('packet_state', {})
        export_blocked = packet_state.get('export_blocked', True)

        next_action = "None"
        if route_status == "MISSING":
            next_action = "Set or review route lock before drafting."

        summary.append({
            "opportunity_id": opportunity_id,
            "title": title,
            "verification_status": verification_status,
            "lifecycle_stage": lifecycle_stage,
            "applied_as_entity_id": applied_as_entity_id,
            "beneficiary_entity_id": beneficiary_entity_id,
            "sponsor_entity_id": sponsor_entity_id,
            "route_status": route_status,
            "fatal_gates_count": fatal_gates_count,
            "advisory_warnings_count": advisory_warnings_count,
            "export_blocked": export_blocked,
            "next_valid_operator_action": next_action
        })

    return summary

if __name__ == "__main__":
    entities_dir = "pipeline/funding_lattice/examples/entities"
    targets_dir = "pipeline/funding_lattice/examples/targets"
    for r in summarize_lattice(entities_dir, targets_dir):
        print(r)
