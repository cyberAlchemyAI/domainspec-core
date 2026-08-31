#!/usr/bin/env python3
"""Build the bounded reconciliation postimage and changed-byte inventory."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
RUN_DIR = Path(__file__).resolve().parent
BASELINE_PATH = RUN_DIR / "subagent-runtime-reconciliation-baseline.json"
OUTPUT_PATH = RUN_DIR / "subagent-runtime-reconciliation-postimage.json"

ROOT_PREFIXES = (
    ".agents/skills/dispatch-spec/",
    ".agents/skills/domainspec-subagents-strategy/",
    ".agents/skills/orchestrate/",
    ".agents/skills/other/",
    ".agents/skills/register-dispatch/",
    ".agents/skills/subagent-strategy/",
    ".claude/skills/dispatch-spec/",
    ".claude/skills/domainspec-subagents-strategy/",
    ".claude/skills/orchestrate/",
    ".claude/skills/other/",
    ".claude/skills/register-dispatch/",
    ".claude/skills/subagent-strategy/",
    "implementation/domainspec/internal_tools/subagents-dispatch-hooks/",
    "ops/development/2026-08-27-invoke-define-v2-documentation-tournament/",
)

ARCANUM_PREFIXES = (
    "arcana/subagent-strategy/",
    "formulae/dispatch-spec/",
    "runtime/orchestrate/",
)

IGNORED_EVIDENCE = (
    "arcanum/spells/invoke/development/example-runs/20260827T192423Z-invoke-define-live-pass",
    "arcanum/spells/invoke/development/example-outputs/invoke-define-live-pass.output.md",
    "arcanum/spells/invoke/development/runs/20260827T192921Z.md",
)


def digest(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"state": "missing"}
    body = path.read_bytes()
    return {
        "state": "present",
        "sha256": hashlib.sha256(body).hexdigest(),
        "size": len(body),
    }


def status_paths(repo: Path, prefix: str = "") -> set[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
    )
    entries = result.stdout.decode("utf-8", errors="surrogateescape").split("\0")
    paths: set[str] = set()
    index = 0
    while index < len(entries):
        entry = entries[index]
        if not entry:
            index += 1
            continue
        status = entry[:2]
        path = entry[3:]
        if status[0] in {"R", "C"}:
            index += 1
            if index < len(entries) and entries[index]:
                path = entries[index]
        paths.add(prefix + path)
        index += 1
    return paths


def in_scope(path: str) -> bool:
    if path.startswith("arcanum/"):
        inner = path.removeprefix("arcanum/")
        return any(inner.startswith(prefix) for prefix in ARCANUM_PREFIXES)
    return any(path.startswith(prefix) for prefix in ROOT_PREFIXES)


def ignored_files() -> set[str]:
    found: set[str] = set()
    for relative in IGNORED_EVIDENCE:
        target = ROOT / relative
        if target.is_file():
            found.add(relative)
        elif target.is_dir():
            for child in target.rglob("*"):
                if child.is_file():
                    found.add(child.relative_to(ROOT).as_posix())
    return found


def main() -> int:
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    preimages = {item["path"]: item for item in baseline["files"]}

    candidates = {path for path in preimages if in_scope(path)}
    candidates.update(
        path
        for path in status_paths(ROOT)
        if in_scope(path) and path != OUTPUT_PATH.relative_to(ROOT).as_posix()
    )
    candidates.update(
        path
        for path in status_paths(ROOT / "arcanum", "arcanum/")
        if in_scope(path)
    )
    candidates.update(ignored_files())

    changed = []
    for relative in sorted(candidates):
        current = digest(ROOT / relative)
        before = preimages.get(relative, {"state": "not_captured"})
        before_material = {key: before[key] for key in ("state", "sha256", "size") if key in before}
        if before_material == current:
            continue
        changed.append(
            {
                "path": relative,
                "preimage": before_material,
                "postimage": current,
                "baseline_bound": relative in preimages,
            }
        )

    receipt = {
        "schema_version": "domainspec.subagent-runtime-reconciliation-postimage.v1",
        "captured_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "baseline": BASELINE_PATH.relative_to(ROOT).as_posix(),
        "baseline_refs": {
            "arcanum": baseline["arcanum"],
            "domainspec": baseline["domainspec"],
        },
        "constraints_observed": baseline["constraints"],
        "validation": {
            "public_registrar": {"passed": 102, "failed": 0},
            "private_registrar": {"passed": 171, "failed": 0},
            "material_strategy": {"passed": 17, "failed": 0},
            "preconfirmation_closure": {"passed": 31, "failed": 0},
            "runtime_composition": {"passed": 58, "failed": 0},
            "dispatch_spec": "pass",
            "orchestrate_top_level": {"passed": 49, "failed": 0},
            "orchestrate_nested": {"passed": 63, "failed": 0},
            "orchestrate_registration_v03": {"passed": 12, "failed": 0},
            "bootstrap_generation": {"passed": 6, "failed": 0},
            "generated_parity": "pass",
            "public_private_leakage": "pass",
            "same_task_review": "pass",
            "native_invoke_define": "pass",
            "invoke_profile": "pass",
            "invoke_aggregate_harness": "block",
            "scoped_whitespace": {
                "status": "block",
                "raw_report_trailing_whitespace_lines": 18,
                "other_changed_and_create_targets": "pass",
            },
        },
        "continuation": {
            "canary_rematerialization": "not_authorized",
            "replacement_confirmation": "not_requested",
            "six_tournament_trials": "not_authorized",
        },
        "blockers": [
            "Design fixture expects obsolete deterministic-selection status prose",
            "preacceptance closure fixture omits required joined_driver_digest",
            "native Define attempt has no admitted generic Quality Bar pass",
            "generated raw Invoke report contains 18 whitespace-only lines with trailing spaces",
        ],
        "changed_file_count": len(changed),
        "files": changed,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=OUTPUT_PATH.parent, delete=False
    ) as handle:
        json.dump(receipt, handle, indent=2, sort_keys=False)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, OUTPUT_PATH)
    print(f"POSTIMAGE={OUTPUT_PATH.relative_to(ROOT)}")
    print(f"CHANGED_FILES={len(changed)}")
    print("CANARY_CONTINUATION=not_authorized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
