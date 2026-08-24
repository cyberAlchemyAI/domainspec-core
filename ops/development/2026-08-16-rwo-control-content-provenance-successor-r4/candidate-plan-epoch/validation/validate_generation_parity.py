#!/usr/bin/env python3
"""Bind the isolated official Context Builder generation and six-file parity result."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
R4_REL = "ops/development/2026-08-16-rwo-control-content-provenance-successor-r4/candidate-plan-epoch"
EVIDENCE = REPO / R4_REL / "validation/generation-parity"
CAP_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/bootstrap/CCP-BOOTSTRAP-R3"
)
CAP = REPO / CAP_REL / "staged"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    assert (EVIDENCE / "reused-target.exit").read_text().strip() == "1"
    guard = (EVIDENCE / "reused-target.stderr").read_text()
    assert "Refusing a partial --force repo-codex install into an existing skill surface" in guard
    assert (EVIDENCE / "fresh-target.exit").read_text().strip() == "0"
    fresh = (EVIDENCE / "fresh-target.stdout").read_text()
    assert "Claude skill validation: pass" in fresh
    assert "Arcanum bootstrap complete." in fresh

    families = {
        "runtime-handoff-index.json": "e00cfef8d9e9205f2c2853077d6a4241073e47134981ef5afc1067547256549f",
        "codex-goal-handoff-index.json": "0ac1bad3fe33aaefbff7e16e5ab35a5f7b521561dd235824fc5fc98886b8d5a0",
    }
    surfaces = [
        "arcanum/transmutations/context-builder/templates",
        ".agents/skills/context-builder/templates",
        ".claude/skills/context-builder/templates",
    ]
    refs = []
    for name, expected in families.items():
        family_bytes = []
        for surface in surfaces:
            path = CAP / surface / name
            assert sha(path) == expected
            family_bytes.append(path.read_bytes())
            refs.append(
                {
                    "path": f"staged/{surface}/{name}",
                    "sha256": expected,
                    "size_bytes": path.stat().st_size,
                }
            )
        assert family_bytes[0] == family_bytes[1] == family_bytes[2]

    result = {
        "schema_version": "rwo.context-builder-generation-parity.v1",
        "result": "pass",
        "official_generation_path": "arcanum/tools/bootstrap_arcanum.sh",
        "profiles": ["repo-codex", "claude"],
        "selected_sigil": "context-builder",
        "fresh_isolated_generation_exit_code": 0,
        "claude_validation": "pass",
        "preserved_reused_target_guard": {
            "exit_code": 1,
            "result": "pass-rejected",
            "later_success_does_not_mask": True,
        },
        "parity_family_count": 2,
        "template_count": 6,
        "template_refs": sorted(refs, key=lambda item: item["path"]),
        "broader_delta_required": False,
        "authority_effect": "none",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    (REPO / args.output).write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
