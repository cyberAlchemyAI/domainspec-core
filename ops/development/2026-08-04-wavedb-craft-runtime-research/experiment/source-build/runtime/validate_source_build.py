#!/usr/bin/env python3
"""Fail-closed validator for one reviewed-source WaveDB build receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_VERSION = "wavedb-reviewed-source-build.v1"
CLAIM_CEILING = "one-local-linux-x86_64-reviewed-source-build-observation"
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
INSTALL_COMMAND = ["npm", "ci", "--ignore-scripts", "--no-audit", "--fund=false"]


class ValidationFailure(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def fail(code: str, detail: str) -> None:
    raise ValidationFailure(code, detail)


def digest_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_object(path: Path, code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        fail(code, f"cannot read JSON object {path}: {error}")
    if not isinstance(value, dict):
        fail(code, f"JSON object required: {path}")
    return value


def object_field(value: Any, code: str, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(code, f"object required: {label}")
    return value


def safe_path(root: Path, raw: str, code: str) -> Path:
    if not isinstance(raw, str) or not raw:
        fail(code, "empty evidence path")
    normalized = PurePosixPath(raw.replace("\\", "/"))
    if normalized.is_absolute() or ".." in normalized.parts or str(normalized) in ("", "."):
        fail(code, f"unsafe evidence path: {raw}")
    candidate = (root / normalized).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError:
        fail(code, f"evidence path escapes source-build root: {raw}")
    return candidate


def verify_ref(
    root: Path,
    reference: Any,
    missing_code: str = "LIVE_EVIDENCE_MISSING",
    mismatch_code: str = "LIVE_EVIDENCE_MISMATCH",
) -> Path:
    ref = object_field(reference, mismatch_code, "artifact reference")
    path = safe_path(root, ref.get("path"), mismatch_code)
    if not path.is_file() or path.is_symlink():
        fail(missing_code, f"missing regular evidence file: {ref.get('path')}")
    content = path.read_bytes()
    if len(content) != ref.get("size_bytes") or digest_bytes(content) != ref.get("sha256"):
        fail(mismatch_code, f"live evidence mismatch: {ref.get('path')}")
    return path


def validate(
    receipt_path: Path,
    root: Path,
    schema_path: Path,
    expected_source_commit: str | None,
    expected_lockfile_sha256: str | None,
) -> dict[str, Any]:
    schema = load_object(schema_path, "SCHEMA_INVALID")
    if schema.get("$id") != "https://arcanum.dev/schemas/wavedb-reviewed-source-build/v1":
        fail("SCHEMA_INVALID", "unsupported source-build schema identity")
    receipt = load_object(receipt_path, "RECEIPT_INVALID")
    required = schema.get("required")
    if not isinstance(required, list) or any(key not in receipt for key in required):
        fail("RECEIPT_INVALID", "receipt omits a required top-level field")
    if receipt.get("schema_version") != SCHEMA_VERSION:
        fail("SCHEMA_VERSION_UNSUPPORTED", "unsupported receipt schema version")
    if receipt.get("verdict") != "pass" or receipt.get("failure_code") is not None:
        fail("RECEIPT_NOT_PASS", "terminal receipt is not a clean pass")
    if receipt.get("claim_ceiling") != CLAIM_CEILING:
        fail("CLAIM_CEILING_EXCEEDED", "claim ceiling is not the local source-build ceiling")
    claims = receipt.get("claims")
    if claims != [CLAIM_CEILING]:
        fail("CLAIM_CEILING_EXCEEDED", "receipt contains an inflated or extra claim")

    source = object_field(receipt.get("source"), "SOURCE_RECORD_MISSING", "source")
    if expected_source_commit and source.get("root_commit") != expected_source_commit:
        fail("SOURCE_COMMIT_MISMATCH", "root source commit differs from the admitted commit")
    if source.get("clean_tracked_baseline") is not True:
        fail("SOURCE_TREE_DIRTY", "tracked source baseline was not clean")
    submodules = source.get("recursive_submodules")
    if not isinstance(submodules, dict) or submodules.get("recursive_checked") is not True:
        fail("SUBMODULE_RECORD_MISSING", "recursive submodule check is absent")
    entries = submodules.get("entries")
    if not isinstance(entries, list):
        fail("SUBMODULE_RECORD_MISSING", "recursive submodule entries are absent")
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("status") != "clean" or not entry.get("path") or not entry.get("commit"):
            fail("SUBMODULE_IDENTITY_MISMATCH", "recursive submodule identity is incomplete or dirty")
    root_files = source.get("root_build_files")
    if not isinstance(root_files, dict) or sorted(root_files) != [
        "binding.gyp",
        "package-lock.json",
        "package.json",
        "scripts/build.js",
        "scripts/copy-sources.js",
    ]:
        fail("SOURCE_BUILD_FILE_MISMATCH", "source build-file identity set is incomplete")

    dependency = object_field(receipt.get("dependency"), "DEPENDENCY_RECORD_MISSING", "dependency")
    lock_digest = dependency.get("lockfile_sha256")
    if expected_lockfile_sha256 and lock_digest != expected_lockfile_sha256:
        fail("LOCKFILE_DRIFT", "package-lock digest differs from the admitted lock")
    if dependency.get("lockfile_unchanged") is not True:
        fail("LOCKFILE_DRIFT", "package-lock changed during dependency materialization")
    if dependency.get("install_command") != INSTALL_COMMAND:
        fail("INSTALL_COMMAND_MISMATCH", "dependency install command is not the admitted argv")
    if dependency.get("lifecycle_scripts_disabled") is not True:
        fail("LIFECYCLE_SCRIPTS_ENABLED", "dependency lifecycle scripts were not disabled")

    stages = receipt.get("stages")
    if not isinstance(stages, list) or [item.get("id") for item in stages if isinstance(item, dict)] != STAGES:
        fail("STAGE_SET_MISMATCH", "acceptance stage set or order differs")
    if any(item.get("status") != "pass" for item in stages if isinstance(item, dict)):
        fail("STAGE_FAILED", "one or more acceptance stages did not pass")

    tests = object_field(receipt.get("tests"), "TEST_RECORD_MISSING", "tests")
    if tests.get("addon_load") != "pass":
        fail("ADDON_LOAD_FAILED", "native addon did not load")
    if tests.get("upstream") != "pass":
        fail("UPSTREAM_TEST_FAILED", "upstream test suite did not pass")
    if tests.get("empty_value_canary") != "pass":
        fail("EMPTY_VALUE_CANARY_FAILED", "empty-value canary did not pass")

    effects = object_field(receipt.get("effects"), "EFFECT_RECORD_MISSING", "effects")
    if effects.get("craft_access") is not False:
        fail("FORBIDDEN_CRAFT_EFFECT", "Craft access or mutation was observed")
    for key in ("git_mutation", "publication", "deployment"):
        if effects.get(key) is not False:
            fail("FORBIDDEN_EFFECT", f"forbidden effect observed: {key}")
    if effects.get("unclassified") != []:
        fail("UNCLASSIFIED_RESIDUE", "unclassified side-effect residue exists")

    evidence = object_field(receipt.get("evidence"), "EVIDENCE_RECORD_MISSING", "evidence")
    for key in (
        "source_manifest",
        "dependency_manifest",
        "generated_source_manifest",
        "build_manifest",
        "test_manifest",
    ):
        verify_ref(root, evidence.get(key))
    logs = evidence.get("logs")
    if not isinstance(logs, list) or not logs:
        fail("LOG_RECORD_MISSING", "command log references are absent")
    for log_ref in logs:
        verify_ref(root, log_ref)

    addon_ref = evidence.get("addon")
    verify_ref(root, addon_ref, "ADDON_MISSING", "ADDON_HASH_MISMATCH")
    addon = object_field(addon_ref, "ADDON_HASH_MISMATCH", "addon")
    if not addon.get("path", "").endswith("/build/Release/wavedb.node"):
        fail("ADDON_PATH_MISMATCH", "unexpected addon path")
    return {
        "verdict": "pass",
        "code": "SOURCE_BUILD_RECEIPT_VALID",
        "attempt_id": receipt.get("attempt_id"),
        "source_commit": source.get("root_commit"),
        "addon_sha256": addon.get("sha256"),
        "claim_ceiling": CLAIM_CEILING,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--source-build-root", required=True, type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--expected-source-commit")
    parser.add_argument("--expected-lockfile-sha256")
    args = parser.parse_args()
    root = args.source_build_root.resolve()
    schema = args.schema or Path(__file__).with_name("source-build-receipt.schema.json")
    try:
        result = validate(
            args.receipt.resolve(),
            root,
            schema.resolve(),
            args.expected_source_commit,
            args.expected_lockfile_sha256,
        )
    except ValidationFailure as error:
        print(json.dumps({"verdict": "block", "code": error.code, "detail": error.detail}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

