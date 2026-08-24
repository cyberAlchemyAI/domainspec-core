#!/usr/bin/env python3
"""Validate Context Builder selected-source identity fields and generated parity."""

from __future__ import annotations

import argparse
import copy
import json
import re
import stat
from pathlib import Path, PurePosixPath
from typing import Any


INDEX_NAMES = (
    "runtime-handoff-index.json",
    "codex-goal-handoff-index.json",
)
SURFACE_PREFIXES = (
    "arcanum/transmutations/context-builder/templates",
    ".agents/skills/context-builder/templates",
    ".claude/skills/context-builder/templates",
)
REQUIRED_FIELDS = (
    "path",
    "sha256",
    "size_bytes",
    "selectors",
    "authority_class",
    "obligation_bindings",
    "evidence_kind",
)
SHA256 = re.compile(r"^[a-f0-9]{64}$")


def contained(root: Path, relative: str) -> Path:
    portable = relative.replace("\\", "/")
    path = PurePosixPath(portable)
    if path.is_absolute() or ".." in path.parts or portable != path.as_posix():
        raise ValueError(f"unsafe or non-canonical path: {relative}")
    candidate = root.joinpath(*path.parts)
    candidate.resolve().relative_to(root.resolve())
    return candidate


def validate_entry(entry: Any, label: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(entry, dict):
        return [f"{label}: selected source must be an object"]
    missing = [field for field in REQUIRED_FIELDS if field not in entry]
    if missing:
        errors.append(f"{label}: missing required fields: {', '.join(missing)}")
    path = entry.get("path")
    if not isinstance(path, str) or not path:
        errors.append(f"{label}: path must be a nonempty string")
    digest = entry.get("sha256")
    if not isinstance(digest, str) or not (
        digest == "<sha256>" or SHA256.fullmatch(digest)
    ):
        errors.append(
            f"{label}: sha256 must be '<sha256>' or 64 lowercase hex characters"
        )
    size_bytes = entry.get("size_bytes")
    if isinstance(size_bytes, bool) or not isinstance(size_bytes, int) or size_bytes < 0:
        errors.append(f"{label}: size_bytes must be a non-negative integer")
    for field in ("selectors", "obligation_bindings"):
        value = entry.get(field)
        if (
            not isinstance(value, list)
            or not value
            or any(not isinstance(item, str) or not item for item in value)
        ):
            errors.append(f"{label}: {field} must be a nonempty string array")
    authority = entry.get("authority_class")
    if authority not in ("public", "private", "<public|private>"):
        errors.append(f"{label}: authority_class has invalid value")
    evidence_kind = entry.get("evidence_kind")
    if not isinstance(evidence_kind, str) or not evidence_kind:
        errors.append(f"{label}: evidence_kind must be a nonempty string")
    if "obligations" in entry:
        errors.append(f"{label}: legacy obligations field is not allowed")
    return errors


def validate_document(document: Any, label: str) -> list[str]:
    if not isinstance(document, dict):
        return [f"{label}: template root must be an object"]
    sources = document.get("selected_sources")
    if not isinstance(sources, list) or not sources:
        return [f"{label}: selected_sources must be a nonempty array"]
    errors: list[str] = []
    for index, entry in enumerate(sources):
        errors.extend(validate_entry(entry, f"{label}/selected_sources/{index}"))
    return errors


def load_templates(root: Path, capsule_mode: bool) -> tuple[dict[str, bytes], list[str]]:
    blobs: dict[str, bytes] = {}
    errors: list[str] = []
    for prefix in SURFACE_PREFIXES:
        for name in INDEX_NAMES:
            relative = f"{prefix}/{name}"
            if capsule_mode:
                relative = f"staged/{relative}"
            path = contained(root, relative)
            if not path.is_file():
                errors.append(f"missing template: {path}")
                continue
            if stat.S_IMODE(path.stat().st_mode) != 0o644:
                errors.append(f"template mode is not 0644: {path}")
            blobs[relative] = path.read_bytes()
    return blobs, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capsule-root")
    parser.add_argument("--repository-root")
    parser.add_argument(
        "--inject-missing",
        choices=("sha256", "size_bytes"),
        help="prove that an in-memory missing-field mutation is rejected",
    )
    args = parser.parse_args()
    if bool(args.capsule_root) == bool(args.repository_root):
        parser.error("select exactly one of --capsule-root or --repository-root")
    root = Path(args.capsule_root or args.repository_root).resolve()
    blobs, errors = load_templates(root, bool(args.capsule_root))

    for relative, content in sorted(blobs.items()):
        try:
            document = json.loads(content)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        errors.extend(validate_document(document, relative))

    for name in INDEX_NAMES:
        suffix = f"/{name}"
        family = [content for path, content in blobs.items() if path.endswith(suffix)]
        if len(family) == 3 and len(set(family)) != 1:
            errors.append(f"canonical/generated parity mismatch: {name}")

    if args.inject_missing:
        if errors:
            print(json.dumps({"status": "block", "errors": errors}, indent=2))
            return 1
        relative = sorted(blobs)[0]
        document = json.loads(blobs[relative])
        injected = copy.deepcopy(document)
        del injected["selected_sources"][0][args.inject_missing]
        injected_errors = validate_document(injected, f"injected:{relative}")
        expected = f"missing required fields: {args.inject_missing}"
        if not any(expected in item for item in injected_errors):
            print(
                json.dumps(
                    {
                        "status": "fail",
                        "injected_field": args.inject_missing,
                        "errors": injected_errors,
                    },
                    indent=2,
                )
            )
            return 1
        print(
            json.dumps(
                {
                    "status": "pass",
                    "negative_case": f"missing-{args.inject_missing}-blocked",
                    "observed_errors": injected_errors,
                },
                indent=2,
            )
        )
        return 0

    status = "pass" if not errors else "block"
    print(
        json.dumps(
            {
                "status": status,
                "template_count": len(blobs),
                "required_fields": list(REQUIRED_FIELDS),
                "parity_families": len(INDEX_NAMES),
                "errors": errors,
            },
            indent=2,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
