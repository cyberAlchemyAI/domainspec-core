#!/usr/bin/env python3
"""Exercise generated WPRA v2 input without running L0 product commands."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def repository_root(plan_root: Path) -> Path:
    for candidate in (plan_root, *plan_root.parents):
        if (candidate / ".git").exists():
            return candidate
    raise ValueError(f"repository root is not discoverable from {plan_root}")


def run_audit(audit_script: Path, config: Path, output_dir: Path) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(audit_script), "--config", str(config), "--output-dir", str(output_dir)],
        check=False,
        capture_output=True,
        text=True,
    )
    report = output_dir / "work-pack-readiness-report-v2.json"
    return completed.returncode, json.loads(report.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-root", required=True, type=Path)
    args = parser.parse_args()
    plan_root = args.plan_root.resolve()
    repo_root = repository_root(plan_root)
    validator = plan_root / "work-pack/admission/validate-admission.py"
    audit_script = repo_root / "arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py"
    with tempfile.TemporaryDirectory(prefix=".wp-cal-ten-l0-wpra-", dir=repo_root) as temp:
        temporary = Path(temp)
        config = temporary / "WPRA-CONFIG.json"
        subprocess.run(
            [
                sys.executable,
                str(validator),
                "--plan-root",
                str(plan_root),
                "--build-wpra-config",
                "--output",
                str(config),
            ],
            check=True,
        )
        positive_code, positive = run_audit(audit_script, config, temporary / "positive")
        assert positive_code == 0, positive
        assert positive["verdict"] == "pass", positive
        assert positive["runtime_admission_status"] == "pending-selection", positive
        assert positive["selected_unit"] is None, positive
        assert positive["mutation_ready"] is False, positive
        assert positive["configured_commands_executed"] is False, positive

        drifted = json.loads(config.read_text(encoding="utf-8"))
        binding = drifted["continuity_projection"]["projected_next_successor"]["continuation_router_verification_receipt_ref"]
        binding["selector"] = "/frontier/0"
        drifted_config = temporary / "WPRA-CONFIG-selector-drift.json"
        drifted_config.write_text(json.dumps(drifted, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        negative_code, negative = run_audit(audit_script, drifted_config, temporary / "negative")
        assert negative_code == 2, negative
        assert negative["verdict"] == "block", negative
        assert any(item["code"] == "BINDING_SELECTOR_UNRESOLVED" for item in negative["blockers"]), negative

    print(json.dumps({"status": "pass", "product_commands_run": 0, "authority_effect": "none"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
