#!/usr/bin/env python3
"""Freeze the isolated Invoke governance-repair candidate without applying it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


EXPECTED_ARCANUM_HEAD = "b07a03d95e4c8bd4d98c05a8eb2916ad7f8341d9"
EXPECTED_CANONICAL_TARGETS = 32
EXPECTED_GENERATED_TARGETS = 36
TASK_SESSION_TEST_TARGETS = {
    "arcana/task-session/development/run-validation-fixtures.sh",
    "arcana/task-session/development/test_live_execution_entry.py",
}
IGNORED_PREFIXES = (
    "arcana/task-session/development/runs/",
    "spells/invoke/development/runs/",
)
VALIDATION_REPORT = (
    "arcanum/spells/invoke/development/runs/20260826T210218Z.md"
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def byte_digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def file_digest(path: Path) -> str:
    return byte_digest(path.read_bytes())


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def relative_ref(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def exact_ref(path: Path, root: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": relative_ref(path, root),
        "sha256": byte_digest(content),
        "size_bytes": len(content),
    }


def mode_string(path: Path) -> str:
    return f"{stat.S_IMODE(path.stat().st_mode):04o}"


def is_ignored(relative_path: str) -> bool:
    path = PurePosixPath(relative_path)
    return (
        any(part == "__pycache__" for part in path.parts)
        or path.suffix == ".pyc"
        or path.name == ".DS_Store"
        or any(relative_path.startswith(prefix) for prefix in IGNORED_PREFIXES)
    )


def git_output(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def dirty_paths(repo: Path) -> set[str]:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "ls-files",
            "-m",
            "-o",
            "-d",
            "--exclude-standard",
            "-z",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item and not is_ignored(item.decode("utf-8"))
    }


def files_equal(left: Path, right: Path) -> bool:
    if left.exists() != right.exists():
        return False
    if not left.exists():
        return True
    if not left.is_file() or not right.is_file():
        raise ValueError(f"non-file candidate target: {left} or {right}")
    return left.read_bytes() == right.read_bytes() and mode_string(left) == mode_string(right)


def collect_canonical_differences(
    live_arcanum: Path, candidate_arcanum: Path
) -> list[tuple[str, Path, Path]]:
    paths = dirty_paths(live_arcanum) | dirty_paths(candidate_arcanum)
    differences: list[tuple[str, Path, Path]] = []
    forbidden: list[str] = []
    for relative_path in sorted(paths):
        live_path = live_arcanum / relative_path
        candidate_path = candidate_arcanum / relative_path
        if files_equal(live_path, candidate_path):
            continue
        allowed = relative_path.startswith("spells/invoke/") or relative_path in TASK_SESSION_TEST_TARGETS
        if not allowed:
            forbidden.append(relative_path)
            continue
        if not candidate_path.is_file():
            raise ValueError(f"delete targets are forbidden: arcanum/{relative_path}")
        differences.append((f"arcanum/{relative_path}", candidate_path, live_path))
    if forbidden:
        raise ValueError(
            "candidate differs from live outside the accepted canonical scope: "
            + ", ".join(forbidden)
        )
    if len(differences) != EXPECTED_CANONICAL_TARGETS:
        raise ValueError(
            f"expected {EXPECTED_CANONICAL_TARGETS} canonical targets, "
            f"found {len(differences)}"
        )
    return differences


def tree_files(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        raise ValueError(f"missing generated Invoke package: {root}")
    result: dict[str, Path] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root).as_posix()
        if is_ignored(relative_path):
            continue
        result[relative_path] = path
    return result


def collect_generated_differences(
    live_root: Path, candidate_root: Path
) -> list[tuple[str, Path, Path]]:
    differences: list[tuple[str, Path, Path]] = []
    for package_prefix in (".agents/skills/invoke", ".claude/skills/invoke"):
        live_package = live_root / package_prefix
        candidate_package = candidate_root / package_prefix
        live_files = tree_files(live_package)
        candidate_files = tree_files(candidate_package)
        for relative_path in sorted(set(live_files) | set(candidate_files)):
            live_path = live_files.get(relative_path, live_package / relative_path)
            candidate_path = candidate_files.get(
                relative_path, candidate_package / relative_path
            )
            if files_equal(live_path, candidate_path):
                continue
            if not candidate_path.is_file():
                raise ValueError(
                    f"delete targets are forbidden: {package_prefix}/{relative_path}"
                )
            differences.append(
                (f"{package_prefix}/{relative_path}", candidate_path, live_path)
            )
    if len(differences) != EXPECTED_GENERATED_TARGETS:
        raise ValueError(
            f"expected {EXPECTED_GENERATED_TARGETS} generated targets, "
            f"found {len(differences)}"
        )
    return differences


def baseline_record(target_path: str, live_path: Path) -> dict[str, Any]:
    if not live_path.exists():
        return {
            "path": target_path,
            "state": "absent",
            "sha256": None,
            "size_bytes": None,
        }
    if not live_path.is_file():
        raise ValueError(f"live baseline is not a regular file: {target_path}")
    content = live_path.read_bytes()
    return {
        "path": target_path,
        "state": "present",
        "sha256": byte_digest(content),
        "size_bytes": len(content),
    }


def copy_postimage(
    target_path: str,
    candidate_path: Path,
    live_path: Path,
    run_dir: Path,
    root: Path,
) -> dict[str, Any]:
    content = candidate_path.read_bytes()
    candidate_mode = mode_string(candidate_path)
    baseline = baseline_record(target_path, live_path)
    postimage_path = run_dir / "postimages" / target_path
    postimage_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(candidate_path, postimage_path)
    os.chmod(postimage_path, int(candidate_mode, 8))
    if postimage_path.read_bytes() != content or mode_string(postimage_path) != candidate_mode:
        raise ValueError(f"postimage copy mismatch: {target_path}")
    return {
        "target_path": target_path,
        "operation": "update" if baseline["state"] == "present" else "create",
        "baseline": {
            "state": baseline["state"],
            "sha256": baseline["sha256"],
            "size_bytes": baseline["size_bytes"],
            "mode": mode_string(live_path) if live_path.is_file() else None,
        },
        "postimage_ref": exact_ref(postimage_path, root),
        "postimage_mode": candidate_mode,
        "candidate_source": str(candidate_path),
    }


def assert_sources_and_baselines_stable(
    targets: list[dict[str, Any]], candidate_by_target: dict[str, Path], root: Path
) -> None:
    for target in targets:
        target_path = target["target_path"]
        candidate_path = candidate_by_target[target_path]
        postimage_ref = target["postimage_ref"]
        candidate_content = candidate_path.read_bytes()
        if byte_digest(candidate_content) != postimage_ref["sha256"]:
            raise ValueError(f"candidate drift after freeze copy: {target_path}")
        if len(candidate_content) != postimage_ref["size_bytes"]:
            raise ValueError(f"candidate size drift after freeze copy: {target_path}")
        if mode_string(candidate_path) != target["postimage_mode"]:
            raise ValueError(f"candidate mode drift after freeze copy: {target_path}")

        live_path = root / target_path
        current = baseline_record(target_path, live_path)
        baseline = target["baseline"]
        if any(
            current[key] != baseline[key]
            for key in ("state", "sha256", "size_bytes")
        ):
            raise ValueError(f"live baseline drift during freeze: {target_path}")
        current_mode = mode_string(live_path) if live_path.is_file() else None
        if current_mode != baseline["mode"]:
            raise ValueError(f"live baseline mode drift during freeze: {target_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--validation-report", default=VALIDATION_REPORT)
    parser.add_argument("--supersedes-run-id")
    args = parser.parse_args()

    root = args.root.resolve()
    candidate_root = args.candidate.resolve()
    live_arcanum = root / "arcanum"
    candidate_arcanum = candidate_root / "arcanum"
    run_id = args.run_id or (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "-spellcraft-candidate-freeze-001"
    )
    evidence_root = (
        root
        / "ops/development/2026-08-26-invoke-preacceptance-governance-defect/runs"
    )
    run_dir = evidence_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    live_head = git_output(live_arcanum, "rev-parse", "HEAD")
    candidate_head = git_output(candidate_arcanum, "rev-parse", "HEAD")
    if live_head != EXPECTED_ARCANUM_HEAD or candidate_head != EXPECTED_ARCANUM_HEAD:
        raise ValueError(
            "Arcanum HEAD mismatch: "
            f"live={live_head}, candidate={candidate_head}, expected={EXPECTED_ARCANUM_HEAD}"
        )

    canonical = collect_canonical_differences(live_arcanum, candidate_arcanum)
    generated = collect_generated_differences(root, candidate_root)
    discovered = sorted(canonical + generated, key=lambda item: item[0])
    if len(discovered) != EXPECTED_CANONICAL_TARGETS + EXPECTED_GENERATED_TARGETS:
        raise ValueError("unexpected total target count")
    if len({item[0] for item in discovered}) != len(discovered):
        raise ValueError("duplicate frozen target path")

    targets: list[dict[str, Any]] = []
    candidate_by_target: dict[str, Path] = {}
    for target_path, candidate_path, live_path in discovered:
        candidate_by_target[target_path] = candidate_path
        targets.append(
            copy_postimage(
                target_path, candidate_path, live_path, run_dir, root
            )
        )

    assert_sources_and_baselines_stable(targets, candidate_by_target, root)
    baseline_digest = canonical_digest(
        [
            {"target_path": item["target_path"], **item["baseline"]}
            for item in targets
        ]
    )
    postimage_digest = canonical_digest(
        [
            {
                "target_path": item["target_path"],
                "operation": item["operation"],
                "postimage_ref": item["postimage_ref"],
                "postimage_mode": item["postimage_mode"],
            }
            for item in targets
        ]
    )

    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    candidate_report = candidate_root / args.validation_report
    if not candidate_report.is_file():
        raise ValueError(f"missing candidate validation report: {candidate_report}")
    copied_report = evidence_dir / "invoke-validation-report.md"
    shutil.copyfile(candidate_report, copied_report)

    work_pack = (
        root
        / "ops/development/2026-08-26-invoke-preacceptance-governance-defect/WORK-PACK.md"
    )
    work_pack_digest = file_digest(work_pack)
    plan_epoch_id = f"epoch-{work_pack_digest[:24]}"

    unit_contract_path = run_dir / "UNIT-CONTRACT.json"
    unit_contract = {
        "schema_version": "invoke-governance-repair-unit-contract/1.0.0",
        "contract_id": f"UC-{run_id}",
        "task_id": "TASK-IGD-REPAIR",
        "swu_id": "SWU-IGD-CLOSEOUT",
        "plan_epoch_id": plan_epoch_id,
        "work_pack_ref": exact_ref(work_pack, root),
        "candidate_root": str(candidate_root),
        "supersedes_run_id": args.supersedes_run_id,
        "arcanum_head": EXPECTED_ARCANUM_HEAD,
        "target_count": len(targets),
        "canonical_target_count": EXPECTED_CANONICAL_TARGETS,
        "generated_target_count": EXPECTED_GENERATED_TARGETS,
        "target_paths": [item["target_path"] for item in targets],
        "required_outcome": (
            "Install the accepted Invoke preacceptance governance repair, preserve "
            "historical readers plus the concurrent accepted-stream v1 producer and "
            "v3 request schema without adopting their runtime-readiness claims, install "
            "a uniquely identified historical-v1 compatibility schema, a separate "
            "preacceptance v2 producer, and the noncolliding v4 wrapper, "
            "enforce exact governance projection and producer/source/WPRA/route "
            "bindings, and then "
            "produce a fresh governed Body War continuation route."
        ),
        "authority": "candidate-preparation-only",
    }
    write_json(unit_contract_path, unit_contract)

    selection_path = run_dir / "CANDIDATE-SELECTION-RECEIPT.json"
    selection_receipt = {
        "schema_version": "invoke-governance-repair-candidate-selection/1.0.0",
        "receipt_id": f"CSR-{run_id}",
        "run_id": run_id,
        "selected_candidate_root": str(candidate_root),
        "supersedes_run_id": args.supersedes_run_id,
        "arcanum_head": EXPECTED_ARCANUM_HEAD,
        "baseline_digest": baseline_digest,
        "postimage_digest": postimage_digest,
        "target_count": len(targets),
        "selection_result": "selected-for-independent-review",
        "authority": "candidate-preparation-only",
        "grants_live_selection": False,
        "grants_admission": False,
        "grants_apply": False,
        "grants_publication": False,
        "grants_deployment": False,
    }
    write_json(selection_path, selection_receipt)

    validation_contracts = [
        {
            "command_id": "invoke-canonical-validation",
            "argv": [
                "env",
                "INVOKE_VALIDATION_SCOPE=canonical-only",
                "PYTHONDONTWRITEBYTECODE=1",
                "bash",
                "arcanum/spells/invoke/development/run-validation-fixtures.sh",
            ],
            "cwd": str(candidate_root),
            "timeout_seconds": 1200,
            "max_output_bytes": 16777216,
        },
        {
            "command_id": "invoke-generated-parity",
            "argv": [
                "bash",
                "arcanum/spells/invoke/development/run-generated-runtime-parity.sh",
            ],
            "cwd": str(candidate_root),
            "timeout_seconds": 300,
            "max_output_bytes": 4194304,
        },
        {
            "command_id": "invoke-generated-behavior",
            "argv": [
                "bash",
                "arcanum/spells/invoke/development/run-generated-runtime-behavior.sh",
            ],
            "cwd": str(candidate_root),
            "timeout_seconds": 600,
            "max_output_bytes": 8388608,
        },
        {
            "command_id": "accepted-stream-driver-bridge",
            "argv": [
                "env",
                "PYTHONDONTWRITEBYTECODE=1",
                "python3",
                "arcanum/spells/invoke/development/accepted-stream-runtime/test_driver_bridge.py",
            ],
            "cwd": str(candidate_root),
            "timeout_seconds": 300,
            "max_output_bytes": 4194304,
        },
        {
            "command_id": "task-session-full-wrapper",
            "argv": [
                "bash",
                "arcanum/arcana/task-session/development/run-validation-fixtures.sh",
            ],
            "cwd": str(candidate_root),
            "timeout_seconds": 1200,
            "max_output_bytes": 16777216,
        },
    ]
    validation_receipt_path = run_dir / "VALIDATION-RECEIPT.json"
    validation_receipt = {
        "schema_version": "invoke-governance-repair-validation/1.0.0",
        "receipt_id": f"VR-{run_id}",
        "run_id": run_id,
        "validated_postimage_digest": postimage_digest,
        "overall_result": "pass",
        "results": [
            {
                "command_id": "invoke-canonical-validation",
                "result": "pass",
                "detail": "the complete Invoke aggregate passed, including separated preacceptance-producer, schema-identity, and compatibility coverage",
                "evidence_ref": exact_ref(copied_report, root),
            },
            {
                "command_id": "invoke-generated-parity",
                "result": "pass",
                "detail": "repo-codex and claude Invoke packages matched canonical inventory, bytes, and modes",
            },
            {
                "command_id": "invoke-generated-behavior",
                "result": "pass",
                "detail": "material and preacceptance behavior passed through both generated runtimes",
            },
            {
                "command_id": "accepted-stream-driver-bridge",
                "result": "pass",
                "detail": "accepted-stream request compilation, exact driver identity, single receipt join, no-effect determinism, and negative drift cases passed as compatibility evidence only; this does not admit the stream tail or prove accepted-stream runtime readiness",
            },
            {
                "command_id": "task-session-full-wrapper",
                "result": "pass",
                "detail": "disposable correct-topology Task Session wrapper passed, including 9 live-entry cases",
            },
            {
                "command_id": "scoped-postimage-hygiene",
                "result": "pass",
                "detail": (
                    f"all {EXPECTED_CANONICAL_TARGETS} canonical postimages passed "
                    "diff, whitespace, newline, and conflict-marker checks"
                ),
            },
        ],
        "validation_contracts": validation_contracts,
        "validation_contract_digest": canonical_digest(validation_contracts),
        "authority": "evidence-only",
        "grants_apply": False,
    }
    write_json(validation_receipt_path, validation_receipt)

    source_plan = live_arcanum / "spells/invoke/plan.md"
    if not source_plan.is_file():
        raise ValueError(f"missing public source plan: {source_plan}")
    material_path = run_dir / "MATERIAL-PACKAGE.json"
    target_baselines = [
        {
            "path": item["target_path"],
            "state": item["baseline"]["state"],
            "sha256": item["baseline"]["sha256"],
            "size_bytes": item["baseline"]["size_bytes"],
        }
        for item in targets
    ]
    material_package = {
        "schema_version": "2.0.0",
        "package_id": f"invoke-governance-repair-{run_id}",
        "mutation_mode": "proposal-only",
        "mutation_state": "staged",
        "lifecycle_owner": "spellcraft",
        "authority_class": "public",
        "publication_class": "public",
        "source_artifacts": [
            {
                **exact_ref(source_plan, root),
                "authority_class": "public",
            }
        ],
        "changes": [
            {
                "target_path": item["target_path"],
                "operation": item["operation"],
                "output_ref": item["postimage_ref"],
            }
            for item in targets
        ],
        "target_inventory": [
            {
                "target_path": item["target_path"],
                "lifecycle_owner": "spellcraft",
                "authority_class": "public",
                "publication_class": "public",
                "dependency_ids": [],
            }
            for item in targets
        ],
        "dependencies": [],
        "mirror_groups": [],
        "approval": {
            "class": "none",
            "owner": None,
            "scope_paths": [],
            "authority_classes": [],
            "publication_classes": [],
        },
        "validation_commands": [
            " ".join(contract["argv"]) for contract in validation_contracts
        ],
        "plan_binding": {
            "task_id": "TASK-IGD-REPAIR",
            "swu_id": "SWU-IGD-CLOSEOUT",
            "plan_epoch_id": plan_epoch_id,
            "unit_contract_digest": file_digest(unit_contract_path),
            "selection_receipt_digest": file_digest(selection_path),
            "attempt_id": run_id,
            "validation_contract_digest": canonical_digest(validation_contracts),
            "validation_contracts": validation_contracts,
            "target_baselines": target_baselines,
        },
    }
    write_json(material_path, material_package)

    freeze_path = run_dir / "CANDIDATE-FREEZE.json"
    freeze_document: dict[str, Any] = {
        "schema_version": "invoke-governance-repair-freeze/1.0.0",
        "run_id": run_id,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "live_root": str(root),
        "candidate_root": str(candidate_root),
        "supersedes_run_id": args.supersedes_run_id,
        "arcanum_head": EXPECTED_ARCANUM_HEAD,
        "baseline_digest": baseline_digest,
        "postimage_digest": postimage_digest,
        "target_count": len(targets),
        "canonical_target_count": EXPECTED_CANONICAL_TARGETS,
        "generated_target_count": EXPECTED_GENERATED_TARGETS,
        "delete_target_count": 0,
        "targets": targets,
        "unit_contract_ref": exact_ref(unit_contract_path, root),
        "selection_receipt_ref": exact_ref(selection_path, root),
        "validation_receipt_ref": exact_ref(validation_receipt_path, root),
        "material_package_ref": exact_ref(material_path, root),
        "authority": "frozen-candidate-only",
        "grants_apply": False,
    }
    freeze_document["freeze_digest"] = canonical_digest(freeze_document)
    write_json(freeze_path, freeze_document)

    assert_sources_and_baselines_stable(targets, candidate_by_target, root)
    print(
        json.dumps(
            {
                "run_dir": str(run_dir),
                "freeze_digest": freeze_document["freeze_digest"],
                "baseline_digest": baseline_digest,
                "postimage_digest": postimage_digest,
                "target_count": len(targets),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
