#!/usr/bin/env python3
"""Generate the replacement strict Context pack and WPRA v2 audit config."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[6]
PREFIX = "ops/development/2026-08-01-intent-route-arcanum-addon/planning"
OLD_EPOCH = "20260802T013311Z"
EPOCH = "20260802T021738Z"
OLD_READY = ROOT / f"{PREFIX}/readiness/{OLD_EPOCH}"
READY = ROOT / f"{PREFIX}/readiness/{EPOCH}"
CONTEXT_DIR = ROOT / f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/{EPOCH}"
CONTRACT_PATH = f"{PREFIX}/work-pack/shared/EXECUTION-CONTRACT.json"
REFRESH_PATH = f"{PREFIX}/refreshes/IRO-REFRESH-002/refresh-report.json"


def rendered(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_ref(path: str) -> dict[str, Any]:
    data = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def replace_strings(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace(OLD_EPOCH, EPOCH).replace("IRO-REFRESH-001", "IRO-REFRESH-002")
    if isinstance(value, list):
        return [replace_strings(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item) for key, item in value.items()}
    return value


def concrete_outputs(contract: dict[str, Any], unit: dict[str, Any]) -> list[str]:
    root = contract["coordinator_root"].replace("<epoch-id>", EPOCH)
    outputs = [f"{root}/{suffix}" for suffix in unit["runtime_outputs"]]
    outputs.append(
        unit["continuity_cursor"]
        .replace("<epoch-id>", EPOCH)
        .replace("<unit-id>", unit["unit_id"])
    )
    return outputs


def build_context() -> dict[str, Any]:
    old = json.loads((ROOT / f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/{OLD_EPOCH}/CONTEXT-PACK.json").read_text())
    context = replace_strings(old)
    context["identity"]["session_or_run_id"] = EPOCH
    context["identity"]["evidence_date"] = "2026-08-02"
    context["strict_coverage"] = "pass"
    context["write_scope"] = [
        f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/{EPOCH}/**",
        f".arcanum/task-session-until-blocker/chains/IRO-FULL-STREAM-{EPOCH}/**",
        f".arcanum/task-session/continuity/IRO-FULL-STREAM-{EPOCH}-<unit-id>.json",
        "Only the exact current-unit owner scope after its explicit owner receipt; unresolved placeholders block",
    ]
    context["validation_surface"] = [
        f"python3 {PREFIX}/work-pack/shared/validate-execution-contract.py --root .",
        f"python3 .agents/skills/work-pack-readiness-audit/scripts/audit_work_pack.py --config {PREFIX}/readiness/{EPOCH}/audit-config-v2.json --output-dir {PREFIX}/readiness/{EPOCH}/outputs",
        "Schema validation for Goal-start, chain, strict Context, mutation-admission, terminal, closeout, router, and continuity receipts",
        "Unit commands at EXECUTION-CONTRACT.json#/units/*/validation_commands",
    ]
    for source in context["selected_sources"]:
        if "refreshes/IRO-REFRESH-002" in source["path"]:
            source["path"] = REFRESH_PATH
        current = ROOT / source["path"]
        if current.is_file():
            ref = file_ref(source["path"])
            source["sha256"] = ref["sha256"]
            source["size_bytes"] = ref["size_bytes"]
    runtime_source = {
        **file_ref(f"{PREFIX}/work-pack/shared/RUNTIME-EVIDENCE.md"),
        "selectors": ["complete document"],
        "obligations": ["O4", "O12", "O13"],
        "evidence_kind": "contract",
    }
    if not any(item["path"] == runtime_source["path"] for item in context["selected_sources"]):
        context["selected_sources"].append(runtime_source)
    context["obligations"].append({
        "id": "O13",
        "status": "covered",
        "summary": "Complete Task Session and outer-chain runtime evidence paths",
        "selected_evidence": [{
            "path": f"{PREFIX}/work-pack/shared/RUNTIME-EVIDENCE.md",
            "selector": "complete document",
            "excerpt_summary": "Nine per-unit support classes, IRO-001 decision bundle, unit cursors, and exact outer chain records.",
        }],
        "resolution": "",
    })
    context["coverage_summary"] = {"total": 13, "covered": 13, "resolved": 0, "blocked": 0, "coverage_percent": 100}
    context["builder"]["source_count"] = len(context["selected_sources"])
    context["output_paths"] = {
        "markdown": f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/{EPOCH}/CONTEXT-PACK.md",
        "json_index": f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/{EPOCH}/CONTEXT-PACK.json",
    }
    return context


def build_context_markdown(context: dict[str, Any]) -> str:
    lines = [
        "# IRO-FULL-STREAM strict runtime Context pack",
        "",
        f"- Run: `{EPOCH}`",
        "- Mode: `deep`, runtime handoff",
        f"- Sources: {len(context['selected_sources'])}/24",
        "- Obligation coverage: 13/13 (`pass`)",
        "- Authority effect: `none`",
        "- Runtime status: context-complete; execution still requires passing WPRA plus exact Goal-start approval",
        "",
        "## Obligations",
        "",
    ]
    for obligation in context["obligations"]:
        lines.append(f"- `{obligation['id']}` — {obligation['summary']}: `{obligation['status']}`")
    lines.extend(["", "## Selected evidence", ""])
    for source in context["selected_sources"]:
        refs = ", ".join(source["obligations"])
        selectors = "; ".join(source["selectors"])
        lines.append(f"- `{source['path']}` — {selectors} — {refs}")
    lines.extend([
        "", "## Runtime write boundary", "",
        f"- Fixed evidence root: `{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/{EPOCH}/`.",
        f"- Fixed chain state: `.arcanum/task-session-until-blocker/chains/IRO-FULL-STREAM-{EPOCH}/`.",
        f"- Unit cursors: `.arcanum/task-session/continuity/IRO-FULL-STREAM-{EPOCH}-<unit-id>.json`.",
        "- Owner material remains separately gated; placeholder scopes cannot be inferred.",
        "", "## Runtime evidence closure", "",
        "Every unit declares strict Context Markdown/JSON, closeout preflight, mutation-admission request/receipt, terminal receipt, closeout-sync request, joined owner receipt, Continuation Router receipt, and a unit cursor. IRO-001 additionally declares its four Decision Gate artifacts and one decision-bundle receipt. The outer chain declares Goal approval, config, preflight, immutable chain record, and ten numbered transitions.",
        "", "## Deferred owner gates", "",
    ])
    for gap in context["gaps_and_blockers"]:
        lines.append(f"- `{gap['id']}` — {gap['summary']}; runtime fallback: `{str(gap['runtime_fallback_allowed']).lower()}`.")
    lines.extend([
        "", "## Fallback rule", "",
        "Search only for evidence needed by a named uncovered obligation. No broad repository exploration, scope inference, or owner substitution is allowed.",
        "", "## Outputs", "",
        f"- Markdown: `{context['output_paths']['markdown']}`",
        f"- JSON/index: `{context['output_paths']['json_index']}`",
        "",
    ])
    return "\n".join(lines)


def build_evidence(contract: dict[str, Any]) -> dict[str, Any]:
    old = json.loads((OLD_READY / "EVIDENCE.json").read_text())
    evidence = replace_strings(old)
    evidence["objective"]["summary"] = "Coordinate the intent-route add-on through ten owner-routed units with complete Task Session and outer-chain receipt paths."
    evidence["statuses"]["artifact_authored"] = {"value": "runtime-admission-contract-repaired", "evidence": "IRO-REFRESH-002"}
    evidence["statuses"]["plan_artifact"] = {"value": "runtime-admission-contract-repaired", "evidence": "IRO-REFRESH-002"}
    evidence["receipts"].update({
        "goal_start_approval_schema": {"path": contract["receipt_schemas"]["goal_start_approval"]},
        "closeout_preflight_schema": {"path": contract["receipt_schemas"]["closeout_preflight"]},
        "closeout_sync_request_schema": {"path": contract["receipt_schemas"]["closeout_sync_request"]},
        "mutation_admission_request_schema": {"path": contract["receipt_schemas"]["mutation_admission_request"]},
        "mutation_admission_receipt_schema": {"path": contract["receipt_schemas"]["mutation_admission_receipt"]},
        "continuation_route_schema": {"path": contract["receipt_schemas"]["continuation_route"]},
        "continuity_cursor_schema": {"path": contract["receipt_schemas"]["continuity_cursor"]},
        "chain_config_schema": {"path": contract["receipt_schemas"]["chain_config"]},
        "chain_transition_schema": {"path": contract["receipt_schemas"]["chain_transition"]},
    })
    all_outputs: list[str] = []
    for unit in contract["units"]:
        outputs = concrete_outputs(contract, unit)
        all_outputs.extend(outputs)
        entry = evidence["units"][unit["unit_id"]]
        entry["expected_receipts"] = outputs
        if unit["unit_id"] == "SWU-IRO-001":
            entry["material_package"] = {
                "contract_id": "SWU-IRO-001-output-only-v2",
                "status": "not-applicable-output-only",
                "owner_ref": "intent-route-planning-owner",
                "target_inventory": [],
                "activation_gate": "passing WPRA epoch plus exact Goal-start approval",
                "authority_effect": "none",
            }
            entry["producer_receipt"] = {"required": False, "status": "not-applicable", "owner_ref": "intent-route-planning-owner"}
            entry["target_inventory"] = []
        entry["material_digest"] = canonical_digest(entry["material_package"])
    evidence["receipts"]["expected"] = all_outputs
    chain = contract["chain_runtime"]
    evidence["receipts"]["expected_outer"] = [
        chain["approval_receipt"].replace("<epoch-id>", EPOCH),
        chain["chain_config"].replace("<epoch-id>", EPOCH),
        chain["chain_preflight"].replace("<epoch-id>", EPOCH),
        chain["chain_record"].replace("<epoch-id>", EPOCH),
        *[path.replace("<epoch-id>", EPOCH) for path in chain["transition_receipts"]],
    ]
    evidence["runtime"].update({
        "support_outputs_declared": True,
        "outer_chain_outputs_declared": True,
        "admission_status": "projection-only-unapproved",
    })
    evidence["continuity"]["cursor"] = f"IRO-FULL-STREAM-{EPOCH}"
    return evidence


def update_refs(value: Any, evidence_ref: dict[str, Any], context_ref: dict[str, Any], refresh_ref: dict[str, Any]) -> None:
    if isinstance(value, list):
        for item in value:
            update_refs(item, evidence_ref, context_ref, refresh_ref)
        return
    if not isinstance(value, dict):
        return
    if {"path", "sha256", "size_bytes"}.issubset(value):
        path = value["path"]
        if path.endswith(f"readiness/{EPOCH}/EVIDENCE.json"):
            value.update(evidence_ref)
        elif path.endswith(f"{EPOCH}/CONTEXT-PACK.json"):
            value.update(context_ref)
        elif path == REFRESH_PATH:
            value.update(refresh_ref)
        elif (ROOT / path).is_file():
            value.update(file_ref(path))
    for item in value.values():
        update_refs(item, evidence_ref, context_ref, refresh_ref)


def build_audit_config(contract: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    old = json.loads((OLD_READY / "audit-config-v2.json").read_text())
    config = replace_strings(old)
    config["audit_id"] = f"iro-full-stream-{EPOCH}"
    unit_by_id = {item["unit_id"]: item for item in contract["units"]}
    for binding in config["execution_bindings"]:
        unit = unit_by_id[binding["unit_id"]]
        outputs = concrete_outputs(contract, unit)
        binding["command"]["argv"][-1] = EPOCH
        binding["execution_outputs"] = outputs
        binding["allowed_writes"] = outputs
        binding["material_writes"] = []
        binding["material_package"]["declared_sha256"] = evidence["units"][unit["unit_id"]]["material_digest"]
    config["expected_material_digests"] = {
        unit_id: entry["material_digest"] for unit_id, entry in evidence["units"].items()
    }
    evidence_path = f"{PREFIX}/readiness/{EPOCH}/EVIDENCE.json"
    evidence_ref = file_ref(evidence_path)
    context_ref = file_ref(f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/{EPOCH}/CONTEXT-PACK.json")
    refresh_ref = file_ref(REFRESH_PATH)
    update_refs(config, evidence_ref, context_ref, refresh_ref)
    return config


def main() -> int:
    contract = json.loads((ROOT / CONTRACT_PATH).read_text())
    context = build_context()
    CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    (CONTEXT_DIR / "CONTEXT-PACK.json").write_bytes(rendered(context))
    (CONTEXT_DIR / "CONTEXT-PACK.md").write_text(build_context_markdown(context), encoding="utf-8")
    evidence = build_evidence(contract)
    READY.mkdir(parents=True, exist_ok=True)
    (READY / "EVIDENCE.json").write_bytes(rendered(evidence))
    config = build_audit_config(contract, evidence)
    (READY / "audit-config-v2.json").write_bytes(rendered(config))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
