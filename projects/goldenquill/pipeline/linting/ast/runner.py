from __future__ import annotations

import ast
import fnmatch
import os
import sys
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation

def _glob_matches_path(target_glob: str, path: Path) -> bool:
    parts = target_glob.split("/")
    filename_pat = parts[-1]
    dir_parts = [p for p in parts[:-1] if p and p != "**"]
    parent_parts = path.parent.parts

    if not fnmatch.fnmatchcase(path.name, filename_pat):
        return False
    if not dir_parts:
        return True
    n, m = len(parent_parts), len(dir_parts)
    for i in range(n - m + 1):
        if all(
            fnmatch.fnmatchcase(parent_parts[i + j], dir_parts[j])
            for j in range(m)
        ):
            return True
    return False

# ---------------------------------------------------------------------------
# Tree walker
# ---------------------------------------------------------------------------


def _iter_python_files(root: Path) -> Iterator[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip virtualenv / build / cache trees.
        dirnames[:] = [
            d
            for d in dirnames
            if d
            not in {
                "__pycache__",
                ".venv",
                ".git",
                ".pytest_cache",
                "node_modules",
            }
        ]
        for fn in filenames:
            if fn.endswith(".py"):
                yield Path(dirpath) / fn


def lint_tree(root: Path, rules: list[Rule]) -> list[Violation]:
    """Walk `root`, apply each rule to matching files, return all violations.

    Unreadable or syntactically broken files are silently skipped — the
    harness is a guardrail, not a parser. Any broken file will already be
    failing the test suite.
    """
    root = Path(root)
    out: list[Violation] = []
    if not root.is_dir():
        return out
    for py in _iter_python_files(root):
        # Determine which rules apply to this file.
        applicable = [r for r in rules if _glob_matches_path(r.target_glob, py)]
        if not applicable:
            continue
        try:
            source = py.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(py))
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue
        for rule in applicable:
            out.extend(rule.check(tree, py))
    return out


# ---------------------------------------------------------------------------
# CLI entry (used by scripts/run_lint.sh)
# ---------------------------------------------------------------------------


def _format_violation(v: Violation) -> str:
    return (
        f"{v.file}:{v.line}:{v.col}: {v.rule_name} "
        f"[{v.reason_tag}] {v.message}"
    )


def main(argv: list[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    target = Path(args[0]) if args else Path("pipeline")
    violations = lint_tree(target, rules)
    if not violations:
        return 0
    for v in violations:
        print(_format_violation(v), file=sys.stderr)
    print(
        f"ast_lint: {len(violations)} violation(s) under {target}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":  # pragma: no cover - thin wrapper
    raise SystemExit(main())
