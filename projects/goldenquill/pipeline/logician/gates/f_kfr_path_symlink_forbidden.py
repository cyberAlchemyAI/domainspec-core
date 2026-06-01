"""F-KFR-PATH-SYMLINK-FORBIDDEN — KFR PRE-load gate (M1 §4.2.2).

Atomic-read discipline (RT-05 Cycle-2 closure): the KFR + ledger
pair MUST be read under a shared advisory lock + symlink rejection.
This gate is the symlink-rejection leg — refuses any path that
resolves to a symlink at read time.

The fcntl.flock + O_NOFOLLOW open machinery is implementation detail
of the disk-state read helper; the gate itself only owns the
symlink predicate.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Optional


F_KFR_PATH_SYMLINK_FORBIDDEN: Final[str] = "F-KFR-PATH-SYMLINK-FORBIDDEN"


@dataclass(frozen=True, kw_only=True)
class PathSymlinkForbiddenResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    offending_path: Optional[str] = None


def check_kfr_path_symlink_forbidden(
    *,
    kfr_path: Path | str,
    ledger_path: Path | str,
) -> PathSymlinkForbiddenResult:
    """PRE-load gate: refuse symlinked KFR or ledger paths.

    Both paths are checked.  First match (in order: KFR, then ledger)
    is reported; the gate is fail-closed so a single symlinked path
    fails the entire read.
    """
    for label, path in (("kfr_path", kfr_path), ("ledger_path", ledger_path)):
        if path is None:
            continue
        path_str = os.fspath(path)
        if os.path.islink(path_str):
            return PathSymlinkForbiddenResult(
                success=False,
                failure_code=F_KFR_PATH_SYMLINK_FORBIDDEN,
                detail=(
                    f"{label}={path_str!r} is a symbolic link — KFR "
                    "atomic-read discipline forbids symlinks per M1 §4.2.2"
                ),
                offending_path=path_str,
            )
    return PathSymlinkForbiddenResult(
        success=True,
        failure_code=None,
        detail=(
            "neither KFR nor ledger path is a symlink (atomic-read "
            "symlink discipline holds)"
        ),
    )


__all__ = [
    "F_KFR_PATH_SYMLINK_FORBIDDEN",
    "PathSymlinkForbiddenResult",
    "check_kfr_path_symlink_forbidden",
]
