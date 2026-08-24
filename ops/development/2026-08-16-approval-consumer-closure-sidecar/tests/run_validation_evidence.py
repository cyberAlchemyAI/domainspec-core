#!/usr/bin/env python3
"""Run the staged sidecar validation matrix and preserve every exit status."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
SIDECAR = Path(__file__).resolve().parents[1]
EVIDENCE = SIDECAR / "evidence"
TMP = EVIDENCE / "tmp"
SCRIPT = SIDECAR / (
    "candidate/public-arcanum/arcanum/spells/work-pack-readiness-audit/"
    "scripts/consumer_closure.py"
)
PUBLIC_TEST = SIDECAR / (
    "candidate/public-arcanum/arcanum/spells/work-pack-readiness-audit/"
    "development/test_consumer_closure.py"
)
RUNNER = SIDECAR / (
    "candidate/public-arcanum/arcanum/spells/work-pack-readiness-audit/"
    "development/run-validation-fixtures.sh"
)
REPLAY_TEST = SIDECAR / "tests/test_exact_r1_r2_replay.py"
EXECUTION_ROOT = ROOT / (
    "research/2026-08-09-skillopt-arcanum-presentation/development/"
    "refinement-runs/20260816-three-next-steps-plan/execution-series/"
    "20260816-execute-everything"
)


def input_paths(refresh: str) -> dict[str, Path]:
    candidate = EXECUTION_ROOT / refresh / "candidate-plan-epoch"
    return {
        "execution-contracts": candidate / "SWU-MANIFEST.json",
        "audit-config": candidate / "readiness/AUDIT-CONFIG-v2.json",
        "audit-report": candidate
        / "validation/readiness/work-pack-readiness-report-v2.json",
        "semantic-manifest": candidate
        / "validation/readiness/plan-semantic-manifest.json",
        "selection-handoff": candidate
        / "validation/readiness/selection-handoff.json",
    }


def inputs(refresh: str) -> list[str]:
    values = input_paths(refresh)
    return [item for pair in values.items() for item in (f"--{pair[0]}", str(pair[1]))]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact(path: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def write_bound_synthetic_draft(
    refresh: str, receipt: Path, output: Path
) -> None:
    values = input_paths(refresh)
    config = json.loads(values["audit-config"].read_text(encoding="utf-8"))
    report = json.loads(values["audit-report"].read_text(encoding="utf-8"))
    manifest = json.loads(values["semantic-manifest"].read_text(encoding="utf-8"))
    if config["execution_policy"]["work_pack_id"] != manifest["work_pack_id"]:
        raise SystemExit("synthetic draft source work-pack tuple differs")
    draft = {
        "schema_version": "sidecar.synthetic-guard-probe/1.0.0",
        "kind": "not-an-acceptance-request",
        "authority_effect": "none",
        "work_pack_id": manifest["work_pack_id"],
        "plan_epoch_id": manifest["plan_epoch_id"],
        "manifest_id": manifest["manifest_id"],
        "audit_id": report["audit_id"],
        "audit_verdict": report["verdict"],
        "terminal_code": report["terminal_code"],
        "consumer_closure_receipt_ref": exact(receipt),
    }
    output.write_text(
        json.dumps(draft, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    results_path = EVIDENCE / "COMMAND-RESULTS.json"
    if results_path.exists():
        raise SystemExit(f"refusing to overwrite {results_path}")

    r1_receipt = EVIDENCE / "R1-CONSUMER-CLOSURE-RECEIPT.json"
    r2_receipt = EVIDENCE / "R2-CONSUMER-CLOSURE-RECEIPT.json"
    r1_draft = EVIDENCE / "R1-SYNTHETIC-GUARD-DRAFT.json"
    r2_draft = EVIDENCE / "R2-SYNTHETIC-GUARD-DRAFT.json"
    r1_guarded = EVIDENCE / "R1-GUARDED-SYNTHETIC-PROBE.json"
    r2_guarded = EVIDENCE / "R2-GUARDED-SYNTHETIC-PROBE.json"
    for path in (r1_receipt, r2_receipt, r1_draft, r2_draft, r1_guarded, r2_guarded):
        if path.exists():
            raise SystemExit(f"refusing to overwrite {path}")

    python = "python3"
    common = ["--repository-root", str(ROOT)]
    initial_commands: list[tuple[str, list[str], int]] = [
        (
            "staged-runner-shell-syntax",
            ["bash", "-n", str(RUNNER)],
            0,
        ),
        (
            "canonical-wpra-regression-suite",
            [
                "bash",
                str(
                    ROOT
                    / "arcanum/spells/work-pack-readiness-audit/development/run-validation-fixtures.sh"
                ),
            ],
            0,
        ),
        (
            "public-guard-regressions",
            [python, "-B", "-m", "unittest", "-v", str(PUBLIC_TEST)],
            0,
        ),
        (
            "exact-r1-r2-replays",
            [python, "-B", "-m", "unittest", "-v", str(REPLAY_TEST)],
            0,
        ),
        (
            "frozen-r1-consumer-closure",
            [python, "-B", str(SCRIPT), "validate", *common, *inputs("governed-refresh"), "--output", str(r1_receipt)],
            2,
        ),
        (
            "exact-r2-consumer-closure",
            [python, "-B", str(SCRIPT), "validate", *common, *inputs("governed-refresh-r2"), "--output", str(r2_receipt)],
            0,
        ),
    ]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["TMPDIR"] = str(TMP)
    results = []
    failed = False

    def run(command_id: str, argv: list[str], expected_exit: int) -> None:
        nonlocal failed
        completed = subprocess.run(
            argv,
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        passed = completed.returncode == expected_exit
        failed = failed or not passed
        results.append(
            {
                "command_id": command_id,
                "argv": argv,
                "cwd": str(ROOT),
                "expected_exit": expected_exit,
                "exit_code": completed.returncode,
                "status": "pass" if passed else "block",
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )

    for command_id, argv, expected_exit in initial_commands:
        run(command_id, argv, expected_exit)

    if r1_receipt.is_file() and r2_receipt.is_file():
        write_bound_synthetic_draft("governed-refresh", r1_receipt, r1_draft)
        write_bound_synthetic_draft("governed-refresh-r2", r2_receipt, r2_draft)
    else:
        failed = True

    guard_commands = [
        (
            "r1-acceptance-emission-blocked",
            [python, "-B", str(SCRIPT), "guard", *common, *inputs("governed-refresh"), "--receipt", str(r1_receipt), "--draft", str(r1_draft), "--output", str(r1_guarded)],
            3,
        ),
        (
            "r2-synthetic-guard-probe",
            [python, "-B", str(SCRIPT), "guard", *common, *inputs("governed-refresh-r2"), "--receipt", str(r2_receipt), "--draft", str(r2_draft), "--output", str(r2_guarded)],
            0,
        ),
    ]
    for command_id, argv, expected_exit in guard_commands:
        run(command_id, argv, expected_exit)

    artifact_checks = {
        "r1_receipt_exists": r1_receipt.is_file(),
        "r2_receipt_exists": r2_receipt.is_file(),
        "r1_guarded_output_absent": not r1_guarded.exists(),
        "r2_synthetic_guard_probe_exists": r2_guarded.is_file(),
        "r2_synthetic_guard_probe_matches_draft": (
            r2_guarded.is_file() and r2_guarded.read_bytes() == r2_draft.read_bytes()
        ),
    }
    failed = failed or not all(artifact_checks.values())
    artifacts = [
        exact(path)
        for path in (r1_receipt, r2_receipt, r1_draft, r2_draft, r2_guarded)
        if path.is_file()
    ]
    payload = {
        "schema_version": "arcanum.governance-sidecar-command-results/1.0.0",
        "status": "block" if failed else "pass",
        "commands": results,
        "artifact_checks": artifact_checks,
        "artifacts": artifacts,
        "authority_effect": "none",
        "selection_performed": False,
        "mutation_performed": False,
        "configured_unit_commands_executed": False,
        "synthetic_guard_probe_is_acceptance_request": False,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    results_path.write_text(rendered, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "command_count": len(results),
                "command_results": str(results_path),
                "command_results_sha256": sha256(results_path),
            },
            sort_keys=True,
        )
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
