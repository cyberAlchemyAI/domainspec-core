#!/usr/bin/env python3
"""Build isolated receipt fixtures and exercise only the independent validator."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


COMMIT = "01c77e8b70f71de9b72480e73a3a179f6e93a009"
LOCK = "26fbf0839106a0521f1ad6785764cefa3d39aedd9ff8412c982689c09b109f95"
CLAIM = "one-local-linux-x86_64-reviewed-source-build-observation"
STAGES = [
    "source",
    "dependencies",
    "generated-source",
    "build",
    "addon-load",
    "upstream-tests",
    "empty-value-canary",
    "scope-audit",
]


def write(path: Path, content: bytes) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {
        "path": path.as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def relative_ref(root: Path, relative: str, content: bytes) -> dict[str, Any]:
    ref = write(root / relative, content)
    ref["path"] = relative
    return ref


def base_receipt(root: Path) -> dict[str, Any]:
    manifests = {
        name: relative_ref(root, f"evidence/{name}.json", b"{}\n")
        for name in ("source-manifest", "dependency-manifest", "generated-source-manifest", "build-manifest", "test-manifest")
    }
    log = relative_ref(root, "evidence/logs/01.log", b"fixture command log\n")
    addon = relative_ref(root, "attempt/source/bindings/nodejs/build/Release/wavedb.node", b"fixture-addon")
    return {
        "schema_version": "wavedb-reviewed-source-build.v1",
        "attempt_id": "fixture-attempt",
        "verdict": "pass",
        "failure_code": None,
        "claim_ceiling": CLAIM,
        "claims": [CLAIM],
        "source": {
            "url": "fixture-source",
            "root_commit": COMMIT,
            "clean_tracked_baseline": True,
            "recursive_submodules": {"recursive_checked": True, "entries": []},
            "root_build_files": {
                "binding.gyp": "a" * 64,
                "package-lock.json": LOCK,
                "package.json": "b" * 64,
                "scripts/build.js": "c" * 64,
                "scripts/copy-sources.js": "d" * 64
            }
        },
        "dependency": {
            "lockfile_sha256": LOCK,
            "lockfile_unchanged": True,
            "install_command": ["npm", "ci", "--ignore-scripts", "--no-audit", "--fund=false"],
            "lifecycle_scripts_disabled": True
        },
        "toolchain": {"node": "fixture"},
        "openssl": {"enabled": True, "root": "/usr"},
        "stages": [{"id": stage, "status": "pass"} for stage in STAGES],
        "tests": {"addon_load": "pass", "upstream": "pass", "empty_value_canary": "pass"},
        "effects": {"craft_access": False, "git_mutation": False, "publication": False, "deployment": False, "unclassified": []},
        "evidence": {
            "source_manifest": manifests["source-manifest"],
            "dependency_manifest": manifests["dependency-manifest"],
            "generated_source_manifest": manifests["generated-source-manifest"],
            "build_manifest": manifests["build-manifest"],
            "test_manifest": manifests["test-manifest"],
            "addon": addon,
            "logs": [log]
        }
    }


def mutate(receipt: dict[str, Any], mutation: str, root: Path) -> None:
    if mutation == "none":
        return
    if mutation == "source-commit":
        receipt["source"]["root_commit"] = "0" * 40
    elif mutation == "submodule-record":
        del receipt["source"]["recursive_submodules"]
    elif mutation == "lockfile":
        receipt["dependency"]["lockfile_sha256"] = "0" * 64
    elif mutation == "lifecycle-scripts":
        receipt["dependency"]["lifecycle_scripts_disabled"] = False
    elif mutation == "missing-addon":
        (root / receipt["evidence"]["addon"]["path"]).unlink()
    elif mutation == "addon-hash":
        receipt["evidence"]["addon"]["sha256"] = "0" * 64
    elif mutation == "upstream-test":
        receipt["tests"]["upstream"] = "block"
    elif mutation == "craft-effect":
        receipt["effects"]["craft_access"] = True
    elif mutation == "claim":
        receipt["claims"].append("npm-package-ready")
    else:
        raise ValueError(f"unknown fixture mutation: {mutation}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validator", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--cases", required=True, type=Path)
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text(encoding="utf-8"))["cases"]
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="wcsb-fixtures-") as temporary:
        parent = Path(temporary)
        for case in cases:
            root = parent / case["id"]
            receipt = base_receipt(root)
            mutate(receipt, case["mutation"], root)
            receipt_path = root / "receipt.json"
            receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(args.validator),
                    str(receipt_path),
                    "--source-build-root",
                    str(root),
                    "--schema",
                    str(args.schema),
                    "--expected-source-commit",
                    COMMIT,
                    "--expected-lockfile-sha256",
                    LOCK,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            try:
                observed = json.loads(result.stdout)
            except json.JSONDecodeError:
                failures.append(f"{case['id']}: non-JSON validator output: {result.stdout!r}")
                continue
            if result.returncode != case["expected_exit"] or observed.get("code") != case["expected_code"]:
                failures.append(
                    f"{case['id']}: expected exit/code {case['expected_exit']}/{case['expected_code']}, "
                    f"observed {result.returncode}/{observed.get('code')}"
                )
            else:
                print(f"FIXTURE={case['id']} RESULT=pass CODE={observed.get('code')}")
    if failures:
        for failure in failures:
            print(f"FIXTURE_FAILURE={failure}", file=sys.stderr)
        return 1
    print(f"FIXTURE_MATRIX=pass CASES={len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

