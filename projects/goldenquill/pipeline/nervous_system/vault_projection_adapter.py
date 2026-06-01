import yaml
import copy
from pathlib import Path
from typing import Dict, Any

def get_repo_root() -> Path:
    """Return the root of the Golden Quill repository."""
    return Path(__file__).resolve().parent.parent.parent

def load_current_projection(org_slug: str, cycle_id: str, repo_root: Path = None) -> Dict[str, Any]:
    """
    Projection adapter reading vault classification register state.
    """
    if repo_root is None:
        repo_root = get_repo_root()

    posture_mode = "HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT"

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

    from pipeline.nervous_system.fixtures import load_scout_demo_data
    base_data = copy.deepcopy(load_scout_demo_data())

    if "node" not in base_data:
        base_data["node"] = {}
    base_data["node"]["node_id"] = f"gq_node_{org_slug}_001"
    base_data["node"]["node_name"] = f"Golden Quill — {org_slug} Node"
    base_data["node"]["organization_slug"] = org_slug

    if "cycle" not in base_data:
        base_data["cycle"] = {}
    base_data["cycle"]["cycle_id"] = cycle_id

    if "posture" not in base_data:
        base_data["posture"] = {}
    base_data["posture"]["mode"] = posture_mode
    base_data["posture"]["data_boundary_note"] = "Projection adapter reading vault classification register scaffolded on demo data"

    return base_data
