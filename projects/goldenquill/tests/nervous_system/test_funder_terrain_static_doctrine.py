import os
from pathlib import Path

FORBIDDEN_TERMS = [
    "draft_support",
    "draft-support",
    "proposal narrative",
    "submission-ready",
    "grant drafter",
    "final packet ready",
    "approved for export",
    "autonomous grant writer",
    "automatic submission",
    "web_scanner",
    "search_agent",
    "mini_scout"
]

def test_forbidden_language_static_production():
    project_root = Path(__file__).resolve().parent.parent.parent
    paths_to_check = [
        project_root / "pipeline" / "nervous_system" / "funder_terrain",
        project_root / "pipeline" / "nervous_system" / "scout_adapters",
        project_root / "pipeline" / "nervous_system" / "scout_source_roster.py"
    ]

    for check_path in paths_to_check:
        if not check_path.exists():
            continue

        if check_path.is_file():
            files_to_scan = [check_path]
        else:
            files_to_scan = [Path(root) / f for root, _, files in os.walk(check_path) for f in files]

        for filepath in files_to_scan:
            if filepath.suffix != '.py' and filepath.suffix != '.yaml':
                continue

            if filepath.name == "test_funder_terrain_static_doctrine.py":
                continue

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()

            for term in FORBIDDEN_TERMS:
                assert term.lower() not in content, f"Forbidden term '{term}' found in {filepath}"
