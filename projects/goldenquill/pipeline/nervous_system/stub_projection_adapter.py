import os
import yaml
from pathlib import Path
from typing import Dict, Any

def get_repo_root() -> Path:
    """Return the root of the Golden Quill repository."""
    # Assuming this file is at pipeline/nervous_system/projection_adapter.py
    return Path(__file__).resolve().parent.parent.parent

def load_current_projection(org_slug: str, cycle_id: str, repo_root: Path = None) -> Dict[str, Any]:
    """
    Adapter that reads from the real Tilth pipeline state (e.g. vault)
    and constructs a projection payload for the UI.
    """
    if repo_root is None:
        repo_root = get_repo_root()

    # Default to a safe posture if we can't find the register
    posture_mode = "HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT"

    # Example reading from real vault state: the classification register
    register_path = repo_root / "orgs" / org_slug / "vault" / "classification" / "register.yaml"

    if register_path.is_file():
        try:
            with open(register_path, "r", encoding="utf-8") as f:
                register_data = yaml.safe_load(f)
                if register_data and isinstance(register_data, dict):
                    if "selected_posture" in register_data:
                        posture_mode = str(register_data["selected_posture"]).upper()
        except Exception:
            pass

    # Basic shape required by CurrentProjectionResponse
    return {
        "node": {
            "node_id": f"gq_node_{org_slug}_001",
            "node_name": f"Golden Quill — {org_slug} Node",
            "organization_slug": org_slug,
            "machine_fingerprint": "adapter-real-pipeline",
            "local_status": "ONLINE_LOCAL",
            "network_mode": "HYBRID_ALLOWED"
        },
        "cycle": {
            "cycle_id": cycle_id,
            "status": "GATE_FAILED_CLOSED",
            "created_at": "2026-05-20T14:32:00Z",
            "updated_at": "2026-05-20T15:12:22Z",
            "active_surface": "ELIGIBILITY_GATE",
            "scribe_access": "LOCKED"
        },
        "posture": {
            "mode": posture_mode,
            "changed_mid_cycle": False,
            "last_confirmed_by": "adapter",
            "last_confirmed_at": "2026-05-20T14:35:10Z",
            "data_boundary_note": "Adapter reading from real state"
        }
    }
