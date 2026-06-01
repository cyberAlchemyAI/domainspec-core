"""F-VECTOR-NS-MISMATCH — PRE-gate (Law 3 isolation, P0).

Per architecture v7.0.5 §5.2 + companion `section_04_v7_0_5_companion.md`.
The Pydantic AI vector-store tool wrapping FAISS or Chroma declares
`org_slug: str` as REQUIRED with no default; this gate validates that
the slug arg matches the session-bound slug for per-org namespaces.

Workspace-scoped namespaces (`funder_intel/`) skip the slug check (no
per-org content). Per-org namespaces (`kfr_facts/<slug>/` and forward-
design `match_db/<slug>/`) enforce strict match.

v0.1 protection note: Match DB is structured YAML only in v0.1 (per
v7.0.5 §1); F-VECTOR-NS-MISMATCH is forward-design protection that
activates if any future component vectorizes match reasoning. Today the
gate fires only against `kfr_facts/<slug>/` queries.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_VECTOR_NS_MISMATCH: Final[str] = "F-VECTOR-NS-MISMATCH"

# Workspace-scoped namespaces have no per-org segregation; slug check skipped.
WORKSPACE_SCOPED_NAMESPACES: Final[frozenset[str]] = frozenset({
    "funder_intel/",
    "benchmarks/",
})

# Per-org namespaces require strict slug match. Listed by prefix; the gate
# inspects whatever follows the prefix as the per-org slug segment.
PER_ORG_NAMESPACE_PREFIXES: Final[tuple[str, ...]] = (
    "kfr_facts/",
    "match_db/",
)


@dataclass(frozen=True, kw_only=True)
class VectorNsMismatchResult:
    """Result of F-VECTOR-NS-MISMATCH check."""

    success: bool
    failure_code: Optional[str]
    detail: str


def check_vector_ns_mismatch(
    *,
    namespace: str,
    requested_org_slug: Optional[str],
    session_slug: str,
) -> VectorNsMismatchResult:
    """PRE-gate: vector-tool slug arg must match session slug for per-org NS.

    Parameters
    ----------
    namespace
        Vector store namespace string the tool is about to query (e.g.
        ``kfr_facts/mycosymbiotics_cooperative/``).
    requested_org_slug
        The `org_slug` arg the tool received (may be None — fail-closed).
    session_slug
        Org slug parsed from active PROJECT_CONTEXT.md at session start.

    Returns
    -------
    VectorNsMismatchResult. Workspace-scoped namespaces always pass
    (no per-org content); per-org namespaces require strict slug match.
    """
    if not session_slug:
        return VectorNsMismatchResult(
            success=False,
            failure_code=F_VECTOR_NS_MISMATCH,
            detail="empty session_slug — cannot enforce Law 3",
        )
    if namespace in WORKSPACE_SCOPED_NAMESPACES:
        return VectorNsMismatchResult(
            success=True,
            failure_code=None,
            detail=f"workspace-scoped namespace {namespace!r}, slug check skipped",
        )
    for prefix in PER_ORG_NAMESPACE_PREFIXES:
        if namespace.startswith(prefix):
            if requested_org_slug is None:
                return VectorNsMismatchResult(
                    success=False,
                    failure_code=F_VECTOR_NS_MISMATCH,
                    detail=(
                        f"per-org namespace {namespace!r} but tool received "
                        "no org_slug arg — fail-closed"
                    ),
                )
            if requested_org_slug != session_slug:
                return VectorNsMismatchResult(
                    success=False,
                    failure_code=F_VECTOR_NS_MISMATCH,
                    detail=(
                        f"requested_org_slug {requested_org_slug!r} does not "
                        f"match session_slug {session_slug!r} for namespace "
                        f"{namespace!r} — Law 3 violation"
                    ),
                )
            # Slug matches; verify the namespace's slug segment also matches
            tail = namespace[len(prefix):]
            ns_slug = tail.split("/", 1)[0] if "/" in tail else tail.rstrip("/")
            if ns_slug and ns_slug != session_slug:
                return VectorNsMismatchResult(
                    success=False,
                    failure_code=F_VECTOR_NS_MISMATCH,
                    detail=(
                        f"namespace path slug {ns_slug!r} does not match "
                        f"session_slug {session_slug!r} — Law 3 violation"
                    ),
                )
            return VectorNsMismatchResult(
                success=True,
                failure_code=None,
                detail=(
                    f"per-org namespace {namespace!r} matches session "
                    f"slug {session_slug!r}"
                ),
            )
    # Unrecognized namespace — fail-closed (could be a typo or new namespace
    # not yet registered as workspace-scoped or per-org).
    return VectorNsMismatchResult(
        success=False,
        failure_code=F_VECTOR_NS_MISMATCH,
        detail=(
            f"namespace {namespace!r} is neither workspace-scoped nor "
            f"per-org-prefixed; cannot validate Law 3 posture"
        ),
    )
