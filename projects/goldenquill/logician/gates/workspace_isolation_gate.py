#!/usr/bin/env python3
"""
Golden Quill / Tilth — Workspace Isolation Gate (Law 3 enforcement)
-------------------------------------------------------------------
Deterministic fail-closed path confinement. No LLM. No heuristic.

Contract:
    check_path(path, active_op_id, workspace_root) -> (allowed: bool, reason: str)

ALLOWED paths (relative to workspace_root):
    orgs/<active_op_id>/**         active-org data
    orgs/_TEMPLATE/**              blank template (read-only data elsewhere)
    orgs/ORG_INDEX.md              shared index
    pipeline/**                    shared tooling
    logician/**                    shared tooling
    tools/**                       shared tooling
    skills/**                      shared skills
    Sovereign_Node_Handoff/**      shared product docs
    <file>.md|.yaml|.yml|.txt|.json (at workspace root)

BLOCKED:
    orgs/<any_other_op_id>/**      cross-org read (Law 3 violation)
    Anything outside workspace_root (symlinks resolved first)
    active_op_id missing or containing path separators

Exit codes (CLI):
    0 = all paths allowed
    1 = at least one path blocked (fail-closed)
    2 = config error
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Iterable

# --------------------------------------------------------------------- config

SHARED_TOP_DIRS = frozenset({
    "pipeline",
    "logician",
    "tools",
    "skills",
    "Sovereign_Node_Handoff",
})

ORGS_TOP_ALLOWLIST = frozenset({
    "_TEMPLATE",
    "ORG_INDEX.md",
})

SHARED_ROOT_SUFFIXES = frozenset({".md", ".yaml", ".yml", ".txt", ".json"})

INVALID_OP_CHARS = frozenset({"/", "\\", ":", ".."})


# --------------------------------------------------------------------- core

def _resolve(path: os.PathLike | str) -> Path:
    p = Path(path)
    try:
        return p.resolve(strict=False)
    except OSError:
        return p.absolute()


def _op_id_valid(op_id: str) -> tuple[bool, str]:
    if not op_id or not op_id.strip():
        return False, "empty active_op_id"
    if ".." in op_id:
        return False, f"active_op_id contains '..': {op_id!r}"
    if any(c in op_id for c in ("/", "\\")):
        return False, f"active_op_id contains path separator: {op_id!r}"
    return True, ""


def check_path(
    path: os.PathLike | str,
    active_op_id: str,
    workspace_root: os.PathLike | str,
) -> tuple[bool, str]:
    """Return (allowed, reason). Fail-closed on any ambiguity."""
    ok, why = _op_id_valid(active_op_id)
    if not ok:
        return False, f"invalid op_id ({why})"

    ws = _resolve(workspace_root)
    if not ws.exists():
        return False, f"workspace_root does not exist: {ws}"

    target = _resolve(path)

    try:
        rel = target.relative_to(ws)
    except ValueError:
        return False, f"path escapes workspace: {target} not under {ws}"

    parts = rel.parts
    if not parts:
        return True, "workspace root"

    first = parts[0]

    if first == "orgs":
        if len(parts) == 1:
            return False, "bare 'orgs/' access requires org scope"
        second = parts[1]
        if second == active_op_id:
            return True, f"orgs/{active_op_id} (active org)"
        if second in ORGS_TOP_ALLOWLIST:
            return True, f"orgs/{second} (shared)"
        return False, (
            f"cross-org read blocked: orgs/{second} "
            f"(active={active_op_id}) — Law 3 violation"
        )

    if first in SHARED_TOP_DIRS:
        return True, f"shared dir: {first}/"

    # Workspace-root file with a shared-doc suffix
    if len(parts) == 1 and target.suffix.lower() in SHARED_ROOT_SUFFIXES:
        return True, f"workspace root doc: {first}"

    return False, f"path not whitelisted under workspace: {rel}"


def check_paths(
    paths: Iterable[os.PathLike | str],
    active_op_id: str,
    workspace_root: os.PathLike | str,
) -> list[dict]:
    results: list[dict] = []
    for p in paths:
        allowed, reason = check_path(p, active_op_id, workspace_root)
        results.append({"path": str(p), "allowed": allowed, "reason": reason})
    return results


# --------------------------------------------------------------------- decorator

def enforce(active_op_id_getter, workspace_root_getter):
    """Decorator factory for wrapping I/O callables in the gate.

    Usage:
        @enforce(lambda: active_op_id, lambda: WORKSPACE_ROOT)
        def open_file(path, mode): ...

    The wrapped callable receives its first positional arg (the path) gated.
    If the gate blocks, raises PermissionError.
    """
    def _wrap(fn):
        def _gated(path, *args, **kwargs):
            ok, reason = check_path(path, active_op_id_getter(), workspace_root_getter())
            if not ok:
                raise PermissionError(f"workspace_isolation_gate blocked: {reason}")
            return fn(path, *args, **kwargs)
        _gated.__name__ = fn.__name__
        _gated.__doc__ = fn.__doc__
        return _gated
    return _wrap


# --------------------------------------------------------------------- CLI

def _cli_main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Workspace Isolation Gate (Law 3)")
    ap.add_argument("--op", required=True, help="Active operator/org id")
    ap.add_argument("--workspace", required=True, help="Workspace root path")
    ap.add_argument("--json", action="store_true", help="Emit JSON")
    ap.add_argument("paths", nargs="+", help="One or more paths to check")
    args = ap.parse_args(argv)

    results = check_paths(args.paths, args.op, args.workspace)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            tag = "ALLOW" if r["allowed"] else "BLOCK"
            print(f"{tag:5s} {r['path']}  — {r['reason']}")

    return 1 if any(not r["allowed"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(_cli_main())
