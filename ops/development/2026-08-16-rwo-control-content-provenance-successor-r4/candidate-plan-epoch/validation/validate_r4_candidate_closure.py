#!/usr/bin/env python3
"""Validate R4 capsule closure, six-target delta, live baselines, and hygiene."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import stat
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[5]
R4_REL = "ops/development/2026-08-16-rwo-control-content-provenance-successor-r4/candidate-plan-epoch"
R4 = REPO / R4_REL
CAP_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/bootstrap/CCP-BOOTSTRAP-R3"
)
CAP = REPO / CAP_REL
R2_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/bootstrap/CCP-BOOTSTRAP-R2"
)
R2 = REPO / R2_REL
R3_INVENTORY = REPO / (
    "ops/development/2026-08-16-rwo-control-content-provenance-successor-r3/"
    "candidate-plan-epoch/validation/CANDIDATE-INVENTORY.json"
)
BLOCKER_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/execution/CCP002-R3-1bdf98e1/blocker-receipt.json"
)
TERMINAL_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "SWU-RWO-CCP-001/terminal.json"
)
EXPECTED_CHANGED = {
    "staged/.agents/skills/context-builder/templates/codex-goal-handoff-index.json",
    "staged/.agents/skills/context-builder/templates/runtime-handoff-index.json",
    "staged/.claude/skills/context-builder/templates/codex-goal-handoff-index.json",
    "staged/.claude/skills/context-builder/templates/runtime-handoff-index.json",
    "staged/arcanum/transmutations/context-builder/templates/codex-goal-handoff-index.json",
    "staged/arcanum/transmutations/context-builder/templates/runtime-handoff-index.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


def exact_ref(path: Path, relative: str) -> dict[str, Any]:
    return {
        "path": relative,
        "sha256": digest(path),
        "size_bytes": path.stat().st_size,
        "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}",
    }


def check_ref(base: Path, item: dict[str, Any]) -> None:
    path = base / item["path"]
    assert path.is_file(), f"missing exact ref: {path}"
    assert digest(path) == item["sha256"], f"digest mismatch: {path}"
    assert path.stat().st_size == item["size_bytes"], f"size mismatch: {path}"
    if "mode" in item:
        assert f"{stat.S_IMODE(path.stat().st_mode):04o}" == item["mode"], f"mode mismatch: {path}"


def validate_r3_inventory() -> None:
    inventory = load(R3_INVENTORY)
    assert inventory["candidate_digest"] == "1bdf98e120a43c3dabe71d5d817b42411316bf0dffcdbaf3a1ec7b9fdae97bab"
    projection = []
    for item in inventory["files"]:
        path = REPO / item["path"]
        assert path.is_file(), f"missing immutable R3 file: {item['path']}"
        raw = path.read_bytes()
        assert len(raw) == item["size_bytes"], f"R3 size drift: {item['path']}"
        if item["normalization"] == "raw-bytes":
            actual = hashlib.sha256(raw).hexdigest()
        elif item["normalization"] == "candidate-inventory-projection":
            value = json.loads(raw)
            value.pop("candidate_digest", None)
            value["files"] = [
                {"path": entry["path"], "normalization": entry["normalization"]}
                for entry in value["files"]
            ]
            actual = hashlib.sha256(
                json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
            ).hexdigest()
        elif item["normalization"] == "final-acceptance-request-projection":
            value = json.loads(raw)
            value.pop("candidate_digest", None)
            value.pop("exact_acceptance_text", None)
            actual = hashlib.sha256(
                json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
            ).hexdigest()
        else:
            raise AssertionError(f"unknown R3 normalization: {item['normalization']}")
        assert actual == item["normalized_sha256"], f"R3 byte drift: {item['path']}"
        projection.append(
            {
                "path": item["path"],
                "normalized_sha256": actual,
                "size_bytes": len(raw),
            }
        )
    candidate_digest = hashlib.sha256(
        json.dumps(sorted(projection, key=lambda item: item["path"]), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert candidate_digest == inventory["candidate_digest"], "immutable R3 candidate digest drift"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()

    inventory = load(CAP / "TARGET-INVENTORY.json")
    assert inventory["target_count"] == 56
    assert len(inventory["targets"]) == 56
    staged_r2 = {p.relative_to(R2).as_posix(): p for p in R2.joinpath("staged").rglob("*") if p.is_file()}
    staged_r3 = {p.relative_to(CAP).as_posix(): p for p in CAP.joinpath("staged").rglob("*") if p.is_file()}
    assert set(staged_r2) == set(staged_r3)
    changed = {relative for relative in staged_r2 if staged_r2[relative].read_bytes() != staged_r3[relative].read_bytes()}
    assert changed == EXPECTED_CHANGED, f"unexpected staged delta: {sorted(changed ^ EXPECTED_CHANGED)}"
    for relative in staged_r2:
        assert stat.S_IMODE(staged_r2[relative].stat().st_mode) == stat.S_IMODE(staged_r3[relative].stat().st_mode)

    target_paths: set[str] = set()
    for item in inventory["targets"]:
        assert item["target_path"] not in target_paths
        target_paths.add(item["target_path"])
        staged = CAP / item["staged_path"]
        check_ref(CAP, {"path": item["staged_path"], **item["output"]})
        live = REPO / item["target_path"]
        baseline = item["baseline"]
        state = "present" if live.is_file() else "absent"
        assert state == baseline["state"], f"live baseline state drift: {item['target_path']}"
        if state == "present":
            check_ref(REPO, {"path": item["target_path"], **{k: baseline[k] for k in ("sha256", "size_bytes", "mode")}})

    manifest = load(CAP / "CAPSULE-MANIFEST.json")
    assert manifest["staged_target_count"] == 56
    assert manifest["exact_file_ref_count"] == 64
    assert len(manifest["exact_file_refs"]) == 64
    for item in manifest["exact_file_refs"]:
        check_ref(CAP, item)
    helper = load(CAP / "HELPER-RECEIPT.json")
    assert helper["output_inventory"]["exact_other_file_ref_count"] == 65
    assert len(helper["output_inventory"]["exact_other_file_refs"]) == 65
    for item in helper["output_inventory"]["exact_other_file_refs"]:
        check_ref(CAP, item)
    disclosure = load(CAP / "DISCLOSURE-REVIEW-RECEIPT.json")
    assert len(disclosure["review_inputs"]) == 10
    for item in disclosure["review_inputs"]:
        check_ref(CAP, item)

    validate_r3_inventory()
    assert digest(REPO / BLOCKER_REL) == "dc691a6e9449144cce554f646e553ef69484913cc73cec8084c5a9c8c8dfbf80"
    assert digest(REPO / TERMINAL_REL) == "ad79f1c55fb50b4a3fb78afcaa890611fa7832a1be4edeb699cd5fe9dc6b1223"

    json_count = 0
    text_count = 0
    for root in (R4, CAP):
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            raw = path.read_bytes()
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise AssertionError(f"non-UTF-8 candidate file: {path}") from exc
            text_count += 1
            if raw and not raw.endswith(b"\n"):
                raise AssertionError(f"missing final newline: {path}")
            for line_number, line in enumerate(text.splitlines(), 1):
                assert line == line.rstrip(" \t"), f"trailing whitespace: {path}:{line_number}"
            if path.suffix == ".json":
                json.loads(text)
                json_count += 1
            elif path.suffix == ".py":
                ast.parse(text, filename=str(path))

    result = {
        "schema_version": "rwo.r4-candidate-closure-validation.v1",
        "result": "pass",
        "capsule": CAP_REL,
        "staged_target_count": 56,
        "changed_staged_target_count": len(changed),
        "changed_staged_targets": sorted(changed),
        "unchanged_r2_staged_target_count": 50,
        "live_baseline_match_count": 56,
        "capsule_closure": {"manifest_refs": 64, "helper_refs": 65, "disclosure_refs": 10},
        "immutable_evidence": {
            "r3_candidate_digest": "1bdf98e120a43c3dabe71d5d817b42411316bf0dffcdbaf3a1ec7b9fdae97bab",
            "ccp001_terminal_sha256": "ad79f1c55fb50b4a3fb78afcaa890611fa7832a1be4edeb699cd5fe9dc6b1223",
            "r3_blocker_sha256": "dc691a6e9449144cce554f646e553ef69484913cc73cec8084c5a9c8c8dfbf80",
        },
        "hygiene": {"utf8_text_file_count": text_count, "json_parse_count": json_count, "python_ast_parse": "pass", "scoped_whitespace": "pass"},
        "authority_effect": "none",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        output = REPO / args.output
        output.write_text(rendered, "utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
