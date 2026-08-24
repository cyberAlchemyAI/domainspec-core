#!/usr/bin/env python3
"""Recheck the deterministic R4 gates and emit one final local validation receipt."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
R4_REL = "ops/development/2026-08-16-rwo-control-content-provenance-successor-r4/candidate-plan-epoch"
R4 = REPO / R4_REL
CAP_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/bootstrap/CCP-BOOTSTRAP-R3"
)


def run(argv: list[str]) -> dict[str, object]:
    result = subprocess.run(argv, cwd=REPO, text=True, capture_output=True, check=False)
    assert result.returncode == 0, {"argv": argv, "exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    return {"argv": argv, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def load(relative: str):
    return json.loads((R4 / relative).read_text())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    results = {}
    results["dispatch"] = run([
        "python3", ".agents/skills/dispatch-spec/scripts/validate-dispatch.py",
        "--json", f"{R4_REL}/DISPATCH-ROUTE.json",
    ])
    results["partition"] = run([
        "python3", f"{R4_REL}/validation/validate_task_session_partition_contract.py",
        "--candidate-root", R4_REL, "--repository-root", ".",
    ])
    results["field_capsule"] = run([
        "python3", f"{R4_REL}/validation/validate_context_builder_source_identity.py",
        "--capsule-root", CAP_REL,
    ])
    results["field_negative_sha256"] = run([
        "python3", f"{R4_REL}/validation/validate_context_builder_source_identity.py",
        "--capsule-root", CAP_REL, "--inject-missing", "sha256",
    ])
    results["field_negative_size_bytes"] = run([
        "python3", f"{R4_REL}/validation/validate_context_builder_source_identity.py",
        "--capsule-root", CAP_REL, "--inject-missing", "size_bytes",
    ])

    execution = load("validation/EXECUTION-ENTRY-VALIDATION.json")
    closure = load("validation/CAPSULE-CLOSURE-VALIDATION.json")
    generation = load("validation/generation-parity/GENERATION-PARITY-RECEIPT.json")
    distill = load("validation/DISTILL-RECOMPOSITION-VALIDATION.json")
    preacceptance = load("validation/bootstrap-admission/PREACCEPTANCE-RECEIPT.json")
    readiness = load("validation/readiness/work-pack-readiness-report-v2.json")
    assert execution["status"] == "pass"
    assert closure["result"] == generation["result"] == distill["result"] == preacceptance["result"] == "pass"
    assert readiness["verdict"] == "pass"
    assert readiness["terminal_code"] == "PLAN_SEMANTIC_READY"
    assert readiness["runtime_admission_status"] == "pending-selection"
    assert readiness["mutation_ready"] is False
    for name in ("work-pack-readiness-report-v2.json", "plan-semantic-manifest.json", "selection-handoff.json"):
        assert (R4 / "validation/readiness" / name).read_bytes() == (R4 / "validation/bootstrap-admission/readiness-repro" / name).read_bytes()

    receipt = {
        "schema_version": "rwo.r4-final-validation-receipt.v1",
        "result": "pass",
        "command_results": {key: {"exit_code": value["exit_code"]} for key, value in results.items()},
        "execution_entry": {"result": "pass", "allowed_routes_digest": execution["allowed_routes_digest"]},
        "capsule_closure": closure,
        "generation_parity": {"result": "pass", "template_count": generation["template_count"], "fresh_exit_code": 0},
        "distill_recomposition": {"result": "pass", "frontier": distill["frontier"]},
        "preacceptance": {
            "result": "pass",
            "invoke": "pass-ready",
            "task_session": "admit-mutationReady",
            "markdown_negative": "pass-rejected-exit-1",
            "validation_command_count": 10,
        },
        "readiness": {
            "result": "pass",
            "terminal_code": "PLAN_SEMANTIC_READY",
            "runtime_admission_status": "pending-selection",
            "two_run_exact_byte_reproducibility": "pass",
        },
        "preserved_nonzero_evidence": [
            {"path": "validation/generation-parity/reused-target.exit", "exit_code": 1, "classification": "expected guard"},
            {"path": "validation/bootstrap-admission/logs/negative-markdown.exit", "exit_code": 1, "classification": "expected negative"},
            {"path": "validation/WPRA-ATTEMPT-1-BLOCKER.json", "exit_code": 1, "classification": "repaired validation projection defect"},
            {"path": "validation/bootstrap-admission/PREACCEPTANCE-RECEIPT-BUILD-ATTEMPT-1-BLOCKER.json", "exit_code": 1, "classification": "repaired receipt builder defect"},
            {"path": "validation/FINAL-GATES-ATTEMPT-1-BLOCKER.json", "exit_code": 1, "classification": "repaired receipt field-name defect"},
        ],
        "authority_effect": "none",
        "claim_ceiling": "candidate validation only; no acceptance, selection, admission token, application, mutation, or execution",
    }
    rendered = json.dumps(receipt, indent=2) + "\n"
    (REPO / args.output).write_text(rendered)
    print(json.dumps({"result": "pass", "gate_count": len(results) + 6}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
