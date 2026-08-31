#!/usr/bin/env python3
"""Validate the machine proposal and deterministically derive its human artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_ROOT.parents[2]
SOURCE_PATH = PACKAGE_ROOT / "GOVERNANCE-FLOW-REVISION.yml"
SCHEMA_PATH = PACKAGE_ROOT / "governance-flow-revision.schema.yml"
HUMAN_PATH = PACKAGE_ROOT / "GOVERNANCE-FLOW-REVISION.md"
PATCH_PATH = PACKAGE_ROOT / "AGENTS-PATCH-PROPOSAL.diff"
RECEIPT_PATH = PACKAGE_ROOT / "VALIDATION-RECEIPT.yml"
DECISION_GATE_ROOT = REPOSITORY_ROOT / ".agents/skills/decision-gate"
DECISION_REQUEST_SCHEMA = DECISION_GATE_ROOT / "schemas/option-admissibility-request.schema.json"
DECISION_RECEIPT_SCHEMA = DECISION_GATE_ROOT / "schemas/option-admissibility-receipt.schema.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256_bytes(payload)


def exact_ref(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "path": path.relative_to(REPOSITORY_ROOT).as_posix(),
        "sha256": sha256_bytes(payload),
        "size_bytes": len(payload),
    }


def load_source() -> tuple[dict[str, Any], dict[str, Any]]:
    source = yaml.safe_load(SOURCE_PATH.read_text(encoding="utf-8"))
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(source),
        key=lambda error: [str(item) for item in error.absolute_path],
    )
    if errors:
        first = errors[0]
        location = "/".join(str(item) for item in first.absolute_path) or "<root>"
        raise ValueError(f"proposal schema invalid at {location}: {first.message}")
    return source, schema


def validate_evidence(source: dict[str, Any]) -> None:
    for record in source["evidence_scope"]["sources"]:
        target = (REPOSITORY_ROOT / record["path"]).resolve()
        if not target.is_file():
            raise ValueError(f"evidence source missing: {record['path']}")
        if sha256_bytes(target.read_bytes()) != record["sha256"]:
            raise ValueError(f"evidence source digest drift: {record['path']}")


def validate_contract(source: dict[str, Any]) -> None:
    modes = {record["mode"] for record in source["mode_contracts"]}
    required_modes = {
        "preacceptance_no_effect",
        "human_decision",
        "effectful_execution",
    }
    if modes != required_modes:
        raise ValueError("mode contract must contain exactly the three required modes")

    retries = {record["classification"] for record in source["retry_policy"]}
    required_retries = {
        "environmental",
        "mechanical_evidence_only",
        "semantic_or_authority",
    }
    if retries != required_retries:
        raise ValueError("retry policy must contain exactly the three required classes")

    metrics = {record["metric_id"]: record["target"] for record in source["metrics"]}
    expected_metrics = {
        "postacceptance_consumer_defects": "0",
        "prompts_per_immutable_graph": "1",
        "unchanged_byte_approval_retries": "0",
        "blockers_discovered_after_request": "0",
        "manual_receipt_transfers": "0",
    }
    if metrics != expected_metrics:
        raise ValueError("metric identifiers or targets differ from the required contract")

    matrix_ids = {record["case_id"] for record in source["regression_matrix"]}
    if "P01-TERMINAL-VERTICAL" not in matrix_ids:
        raise ValueError("positive terminal-boundary fixture is absent from regression matrix")

    if not source["positive_terminal_fixture"]["required_assertions"]:
        raise ValueError("positive terminal-boundary fixture lacks assertions")

    public_paths = source["changed_path_proposal"]["later_public_canonical"]["paths"]
    private_markers = (
        "domainspec-core",
        "cyberAlchemy-v2",
        "projects/domainspec",
        "ops/development",
        ".arcanum/",
    )
    for path in public_paths:
        if not path.startswith("arcanum/"):
            raise ValueError(f"public canonical target is outside Arcanum: {path}")
        if any(marker.lower() in path.lower() for marker in private_markers):
            raise ValueError(f"public canonical target contains private marker: {path}")

    stage_paths = source["changed_path_proposal"]["stage_now"]["paths"]
    if set(stage_paths) != {
        "ops/development/2026-08-25-governance-flow-revision/governance-flow-revision.schema.yml",
        "ops/development/2026-08-25-governance-flow-revision/GOVERNANCE-FLOW-REVISION.yml",
        "ops/development/2026-08-25-governance-flow-revision/materialize_revision.py",
        "ops/development/2026-08-25-governance-flow-revision/GOVERNANCE-FLOW-REVISION.md",
        "ops/development/2026-08-25-governance-flow-revision/AGENTS-PATCH-PROPOSAL.diff",
        "ops/development/2026-08-25-governance-flow-revision/VALIDATION-RECEIPT.yml",
    }:
        raise ValueError("stage-now inventory is not the exact six-path package")

    decision = source["owner_decision_surface"]
    request_schema = json.loads(DECISION_REQUEST_SCHEMA.read_text(encoding="utf-8"))
    receipt_schema = json.loads(DECISION_RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    request_errors = sorted(
        Draft202012Validator(request_schema).iter_errors(decision["admissibility_request"]),
        key=lambda error: [str(item) for item in error.absolute_path],
    )
    receipt_errors = sorted(
        Draft202012Validator(receipt_schema).iter_errors(decision["admissibility_receipt"]),
        key=lambda error: [str(item) for item in error.absolute_path],
    )
    if request_errors:
        raise ValueError(f"decision admissibility request invalid: {request_errors[0].message}")
    if receipt_errors:
        raise ValueError(f"decision admissibility receipt invalid: {receipt_errors[0].message}")
    if decision["admissibility_receipt"]["requestDigest"] != canonical_digest(
        decision["admissibility_request"]
    ):
        raise ValueError("decision admissibility request digest mismatch")
    if decision["admissibility_receipt"]["routeOutcome"] != "gate":
        raise ValueError("decision did not traverse the required owner gate")
    if decision["selected_option_id"] not in decision["admissibility_receipt"][
        "admissibleOptionIds"
    ]:
        raise ValueError("selected decision option was not structurally admissible")
    if decision["remains"] or decision["decision_gate_blockers_remaining"] != 0:
        raise ValueError("resolved decision still reports a Decision Gate blocker")


def table(headers: list[str], rows: list[list[str]]) -> list[str]:
    result = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        result.append("| " + " | ".join(value.replace("|", "\\|") for value in row) + " |")
    return result


def render_human(source: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Governance Flow Revision",
        "",
        "> Deterministically derived from `GOVERNANCE-FLOW-REVISION.yml`. The machine",
        "> proposal is authoritative for this design package. This human view grants no",
        "> mutation, acceptance, execution, publication, or deployment authority.",
        "",
        "## Outcome",
        "",
        source["problem_statement"],
        "",
        f"- Status: `{source['completion_claim']['status']}`",
        f"- Authority effect: `{source['authority_effect']}`",
        f"- Terminal fixture in plan: `{str(source['completion_claim']['terminal_fixture_in_plan']).lower()}`",
        f"- Claim ceiling: {source['claim_ceiling']}",
        "",
        "## Evidence boundary",
        "",
        (
            f"The formal Workflow Reflect threshold is not met: "
            f"{source['evidence_scope']['formal_signal_count']} directly matched signal. "
            f"The proposal is justified as a severe-incident correction by "
            f"{source['evidence_scope']['incident_count']} durable incidents and at least "
            f"{source['evidence_scope']['renewed_acceptance_cycles_minimum']} renewed-acceptance cycles."
        ),
        "",
    ]
    lines.extend(
        table(
            ["Source", "Use", "Strength"],
            [
                [record["path"], record["use"], record["strength"]]
                for record in source["evidence_scope"]["sources"]
            ],
        )
    )

    lines.extend(["", "## Practical before / after", "", "### Before", ""])
    lines.extend(
        table(
            ["Step", "Behavior", "Authority"],
            [
                [f"{step['ordinal']}. {step['name']}", step["behavior"], step["authority"]]
                for step in source["before_workflow"]
            ],
        )
    )
    lines.extend(["", "### After", ""])
    lines.extend(
        table(
            ["Step", "Behavior", "Authority"],
            [
                [f"{step['ordinal']}. {step['name']}", step["behavior"], step["authority"]]
                for step in source["after_workflow"]
            ],
        )
    )

    lines.extend(["", "## Required invariants", ""])
    for invariant in source["required_invariants"]:
        lines.extend(
            [
                f"### {invariant['id']}",
                "",
                invariant["statement"],
                "",
                f"Enforcement: {invariant['enforcement']}",
                "",
            ]
        )

    lines.extend(["## Three-mode contract", ""])
    lines.extend(
        table(
            ["Mode", "Effect ceiling", "Stop", "Continuation", "Completion"],
            [
                [
                    mode["mode"],
                    mode["effect_ceiling"],
                    mode["stop_policy"],
                    mode["continuation_policy"],
                    mode["completion_rule"],
                ]
                for mode in source["mode_contracts"]
            ],
        )
    )

    graph = source["decision_graph_contract"]
    lines.extend(
        [
            "",
            "## Immutable decision graph",
            "",
            graph["definition"],
            "",
            "Included fields:",
            "",
            *[f"- {item}" for item in graph["includes"]],
            "",
            "Excluded non-authoritative descendants:",
            "",
            *[f"- {item}" for item in graph["excludes"]],
            "",
            f"- Freeze rule: {graph['freeze_rule']}",
            f"- Request rule: {graph['request_rule']}",
            f"- Descendant rule: {graph['descendant_rule']}",
        ]
    )

    terminal = source["terminal_outcome_contract"]
    lines.extend(
        [
            "",
            "## Terminal outcome contract",
            "",
            terminal["dominance_rule"],
            "",
            *[f"- `{field}`" for field in terminal["required_fields"]],
            "",
            f"- Local PASS: {terminal['local_pass_rule']}",
            f"- Bounded: {terminal['bounded_definition']}",
        ]
    )

    lines.extend(["", "## Retry and sidecar resumption", ""])
    lines.extend(
        table(
            ["Class", "Predicate", "Action", "Graph", "Prompt"],
            [
                [
                    retry["classification"],
                    retry["predicate"],
                    retry["action"],
                    retry["graph_effect"],
                    retry["owner_prompt"],
                ]
                for retry in source["retry_policy"]
            ],
        )
    )
    sidecar = source["sidecar_resume_contract"]
    lines.extend(
        [
            "",
            f"- Suspend: {sidecar['suspend_rule']}",
            f"- Repair ceiling: {sidecar['repair_ceiling']}",
            f"- Resume predicate: `{sidecar['resume_predicate']}`",
            "- Do not resume when:",
            "",
            *[f"  - {item}" for item in sidecar["non_resume_cases"]],
        ]
    )

    lines.extend(["", "## Success metrics", ""])
    lines.extend(
        table(
            ["Metric", "Definition", "Target", "Event"],
            [
                [metric["metric_id"], metric["definition"], metric["target"], metric["evidence_event"]]
                for metric in source["metrics"]
            ],
        )
    )

    lines.extend(["", "## Exact changed-path proposal", ""])
    group_labels = {
        "stage_now": "Current non-overlapping package",
        "later_root_policy": "Later root policy",
        "later_public_canonical": "Later canonical public contract and tests",
        "later_adapters_after_concurrency": "Later adapters after the MVLR concurrency edge closes",
    }
    for key, label in group_labels.items():
        group = source["changed_path_proposal"][key]
        lines.extend(
            [
                f"### {label}",
                "",
                f"Apply now: `{str(group['apply_now']).lower()}`",
                "",
                *[f"- `{path}`" for path in group["paths"]],
                "",
                group["purpose"],
                "",
            ]
        )
    lines.extend(
        [
            f"Generated surface policy: {source['changed_path_proposal']['generated_surface_policy']}",
            "",
            "The exact proposed root-policy diff is in `AGENTS-PATCH-PROPOSAL.diff`; it is not applied.",
        ]
    )

    lines.extend(["", "## Compatibility impact", ""])
    lines.extend(
        table(
            ["Surface", "Impact"],
            [[impact["surface"], impact["impact"]] for impact in source["compatibility_impact"]],
        )
    )

    lines.extend(["", "## Migration plan", ""])
    lines.extend(
        table(
            ["Phase", "Action", "Gate", "Authority effect"],
            [
                [phase["phase"], phase["action"], phase["gate"], phase["authority_effect"]]
                for phase in source["migration_plan"]
            ],
        )
    )

    lines.extend(["", "## Regression matrix", ""])
    lines.extend(
        table(
            ["Case", "Polarity", "Assertion"],
            [
                [case["case_id"], case["polarity"], case["assertion"]]
                for case in source["regression_matrix"]
            ],
        )
    )

    fixture = source["positive_terminal_fixture"]
    lines.extend(
        [
            "",
            "## Positive terminal-boundary fixture",
            "",
            f"- Source: `{fixture['fixture_path']}`",
            f"- Executor: `{fixture['executor_path']}`",
            f"- Promised boundary: {fixture['promised_boundary']}",
            "",
            "Steps:",
            "",
            *[f"1. {step}" for step in fixture["steps"]],
            "",
            "Required assertions:",
            "",
            *[f"- {assertion}" for assertion in fixture["required_assertions"]],
        ]
    )

    decision = source["owner_decision_surface"]
    lines.extend(
        [
            "",
            "## Owner decision surface",
            "",
            f"- Decision: `{decision['decision_id']}`",
            f"- Remains: `{str(decision['remains']).lower()}`",
            f"- Status: `{decision['decision_status']}`",
            f"- Selected: `{decision['selected_option_id']}` — {decision['selected_option_label']}",
            f"- Selected at: `{decision['selected_at']}`",
            f"- Selection source: `{decision['selection_source']['kind']}` response `{decision['selection_source']['response']}`",
            f"- Decision effect: `{decision['decision_effect']}`",
            f"- Selection rationale: {decision['selection_rationale']}",
            f"- Question: {decision['question']}",
            f"- Recommendation: {decision['recommendation']}",
            "",
            *[
                f"- {alternative['surface']}: {alternative['impact']}"
                for alternative in decision["alternatives"]
            ],
            "",
            f"- Admissibility request digest: `{decision['admissibility_receipt']['requestDigest']}`",
            f"- Admissible options: `{', '.join(decision['admissibility_receipt']['admissibleOptionIds'])}`",
            f"- Decision Gate blockers remaining: `{decision['decision_gate_blockers_remaining']}`",
            "- Downstream gates:",
            "",
            *[f"  - {gate}" for gate in decision["downstream_gates"]],
            "",
            f"Apply boundary: {decision['apply_authorization']}",
        ]
    )

    helper = source["helper_receipt"]
    lines.extend(
        [
            "",
            "## Background helper receipt",
            "",
            f"- Helper: `{helper['helper_id']}`",
            f"- Status: `{helper['status']}`",
            f"- Writes: `{helper['writes']}`",
            f"- Material challenge adopted into this proposal: {helper['material_challenge']}",
            f"- Claim ceiling: {helper['claim_ceiling']}",
            "",
            "## Governance sidecar receipts",
            "",
            *[
                f"- `{sidecar['issue_id']}` via `{sidecar['helper_id']}`: "
                f"{sidecar['root_cause']} Permanent fix: {sidecar['permanent_fix']}"
                for sidecar in source["governance_sidecar_receipts"]
            ],
            "",
            "## Current lifecycle status",
            "",
            source["completion_claim"]["reason"],
            "",
            "This package is proposal-ready, not implementation-complete.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def patch_apply_check(patch_bytes: bytes) -> None:
    result = subprocess.run(
        ["git", "apply", "--check", "--recount", "-"],
        cwd=REPOSITORY_ROOT,
        input=patch_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"AGENTS patch does not apply to live bytes: {detail}")


def expected_receipt(source: dict[str, Any], human_bytes: bytes, patch_bytes: bytes) -> dict[str, Any]:
    return {
        "schema_version": "domainspec.governance-flow-revision-validation.v1",
        "package_id": source["package_id"],
        "status": "pass",
        "authority_effect": "none",
        "artifact_role": "durable-proposal-package-validation-artifact",
        "run_local_telemetry": False,
        "source_ref": exact_ref(SOURCE_PATH),
        "schema_ref": exact_ref(SCHEMA_PATH),
        "derived_outputs": [
            {
                "path": HUMAN_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
                "sha256": sha256_bytes(human_bytes),
                "size_bytes": len(human_bytes),
                "role": "deterministic-human-view",
            },
            {
                "path": PATCH_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
                "sha256": sha256_bytes(patch_bytes),
                "size_bytes": len(patch_bytes),
                "role": "unapplied-root-policy-patch",
            },
        ],
        "checks": {
            "proposal_schema": "pass",
            "evidence_exact_digests": "pass",
            "required_three_modes": "pass",
            "required_retry_classes": "pass",
            "required_metrics": "pass",
            "positive_terminal_fixture_in_plan": "pass",
            "stage_now_exact_six_path_inventory": "pass",
            "public_target_path_boundary": "pass",
            "agents_patch_apply_check": "pass",
            "helper_joined": "pass",
            "decision_admissibility_request": "pass",
            "decision_admissibility_receipt": "pass",
            "decision_request_digest": "pass",
            "decision_selected_option_admissible": "pass",
        },
        "counts": {
            "evidence_sources": len(source["evidence_scope"]["sources"]),
            "invariants": len(source["required_invariants"]),
            "modes": len(source["mode_contracts"]),
            "metrics": len(source["metrics"]),
            "regression_cases": len(source["regression_matrix"]),
            "positive_terminal_cases": sum(
                case["polarity"] == "positive" for case in source["regression_matrix"]
            ),
            "public_canonical_paths_proposed": len(
                source["changed_path_proposal"]["later_public_canonical"]["paths"]
            ),
            "adapter_paths_proposed": len(
                source["changed_path_proposal"]["later_adapters_after_concurrency"]["paths"]
            ),
        },
        "write_scope": source["changed_path_proposal"]["stage_now"]["paths"],
        "forbidden_path_writes": [],
        "helper": {
            "helper_id": source["helper_receipt"]["helper_id"],
            "status": source["helper_receipt"]["status"],
            "writes": source["helper_receipt"]["writes"],
        },
        "decision_gate": {
            "result": "PASS",
            "decision_id": source["owner_decision_surface"]["decision_id"],
            "decisions_resolved": 1,
            "decision_gate_blockers_remaining": source["owner_decision_surface"][
                "decision_gate_blockers_remaining"
            ],
            "admissibility_request_digest": source["owner_decision_surface"][
                "admissibility_receipt"
            ]["requestDigest"],
            "admissible_routing": source["owner_decision_surface"][
                "admissibility_receipt"
            ]["routeOutcome"],
            "selected_option_id": source["owner_decision_surface"][
                "selected_option_id"
            ],
            "override_verdict": "not-requested",
            "downstream_gates": source["owner_decision_surface"]["downstream_gates"],
        },
        "governance_sidecars": [
            {
                "helper_id": sidecar["helper_id"],
                "issue_id": sidecar["issue_id"],
                "status": sidecar["status"],
                "writes": sidecar["writes"],
                "renewed_owner_acceptance_required": sidecar[
                    "renewed_owner_acceptance_required"
                ],
            }
            for sidecar in source["governance_sidecar_receipts"]
        ],
        "completion_status": source["completion_claim"]["status"],
        "completion_claim": "proposal package validated; canonical implementation and terminal fixture remain unapplied and unexecuted",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    source, _ = load_source()
    validate_evidence(source)
    validate_contract(source)

    human_bytes = render_human(source).encode("utf-8")
    patch_bytes = source["agents_patch"].encode("utf-8")
    patch_apply_check(patch_bytes)
    receipt = expected_receipt(source, human_bytes, patch_bytes)
    receipt_bytes = yaml.safe_dump(
        receipt,
        sort_keys=True,
        allow_unicode=True,
        width=1_000_000,
    ).encode("utf-8")

    outputs = {
        HUMAN_PATH: human_bytes,
        PATCH_PATH: patch_bytes,
        RECEIPT_PATH: receipt_bytes,
    }
    if arguments.check:
        for path, expected in outputs.items():
            if not path.is_file():
                raise ValueError(f"derived output missing: {path.relative_to(REPOSITORY_ROOT)}")
            if path.read_bytes() != expected:
                raise ValueError(f"derived output drift: {path.relative_to(REPOSITORY_ROOT)}")
    else:
        for path, payload in outputs.items():
            path.write_bytes(payload)

    print(
        json.dumps(
            {
                "status": "pass",
                "mode": "check" if arguments.check else "materialize",
                "source": SOURCE_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
                "outputs": [path.relative_to(REPOSITORY_ROOT).as_posix() for path in outputs],
                "authority_effect": "none",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
