"""F-MATCH-DB-CROSS-ORG — PRE-gate (Law 3 isolation, P0).

Per architecture v7.0.5 §5.1 + companion `section_04_v7_0_5_companion.md`.
Every Match Database read at any seat is intercepted by an I/O wrapper that
calls this gate BEFORE opening the file. The gate validates that the
on-disk path resolves to the session-bound org slug only — any cross-org
read attempt fail-closes.

The gate is a pure string predicate. The session-bound `org_slug` is parsed
from PROJECT_CONTEXT.md by the I/O wrapper (Law 3 canonical source) and
passed as a positional argument; the gate does not perform any filesystem
or PROJECT_CONTEXT I/O itself.

Cedar companion policy: ``pipeline/vault/policies/match_db_session_scoped.cedar``
(authored at v7.0.5 LOCK; loaded by Logician at PRE-check init). The Python
predicate here is the structural floor; the Cedar policy is defense in depth.

Failure semantics: fail-closed. Mismatch RAISES at the I/O wrapper (the
wrapper translates the result's `failure_code` into an exception); does
not log-and-continue.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final, Optional


F_MATCH_DB_CROSS_ORG: Final[str] = "F-MATCH-DB-CROSS-ORG"

# Match DB files live under orgs/<slug>/match_database/<file>.{yaml,yml,json}.
# No `..` traversal allowed; the regex uses [^/]+ to forbid path separators
# inside the filename. Symlink-follow protection lives at the I/O wrapper
# (gate is pure-string; cannot inspect FS state).
_MATCH_DB_PATH_PATTERN: Final[str] = (
    r"^orgs/{slug}/match_database/[^/]+\.(yaml|yml|json)$"
)


@dataclass(frozen=True, kw_only=True)
class MatchDbCrossOrgResult:
    """Result of F-MATCH-DB-CROSS-ORG check."""

    success: bool
    failure_code: Optional[str]
    detail: str


def check_match_db_cross_org(
    *,
    path: str,
    session_slug: str,
) -> MatchDbCrossOrgResult:
    """PRE-gate: path must resolve to the session-bound org's match_database/.

    Parameters
    ----------
    path
        On-disk path the I/O wrapper is about to open.
    session_slug
        Org slug parsed from the active PROJECT_CONTEXT.md at session start.

    Returns
    -------
    MatchDbCrossOrgResult with success=True iff `path` matches
    `^orgs/<session_slug>/match_database/[^/]+\\.(yaml|yml|json)$`. Any
    cross-org path, traversal attempt, or wrong file extension fails.
    """
    if not session_slug:
        return MatchDbCrossOrgResult(
            success=False,
            failure_code=F_MATCH_DB_CROSS_ORG,
            detail="empty session_slug — cannot enforce Law 3",
        )
    if ".." in path:
        return MatchDbCrossOrgResult(
            success=False,
            failure_code=F_MATCH_DB_CROSS_ORG,
            detail=f"path contains traversal segment: {path!r}",
        )
    pattern = _MATCH_DB_PATH_PATTERN.format(slug=re.escape(session_slug))
    if re.match(pattern, path):
        return MatchDbCrossOrgResult(
            success=True,
            failure_code=None,
            detail=f"path scoped to session org {session_slug!r}",
        )
    return MatchDbCrossOrgResult(
        success=False,
        failure_code=F_MATCH_DB_CROSS_ORG,
        detail=(
            f"path {path!r} does not resolve to "
            f"orgs/{session_slug}/match_database/ — Law 3 violation"
        ),
    )
