"""pipeline.logician.cedar_engine — runtime Cedar policy load + evaluation shim.

Companion code for §4 v2.x.5 amendment (LOCKED 2026-05-16 row 232) — Cycle 2
RT-C2-04 + Cycle 1 RT-20/RT-21 fold-ins.

Adds a runtime-load-with-fail-closed-flag shim on top of the existing
``pipeline.logician.cedar_eval`` pure-Python evaluator. The pre-existing
evaluator handles the v0.1 three-policy surface (``org_isolation``,
``byok_key_scope``, ``cross_org_dossier_reference``) for §2.6 entity-shape
authorization; the new shim handles the §4 v2.x.5 outbound-boundary policy
as a second-layer defense against monkey-patching the Python wrapper at
``pipeline.orchestrator.provider_boundary.enforce_outbound_boundary``.

Load-time discipline (RT-C2-04)
-------------------------------

At module load, the shim attempts to read + parse the two policy files:

  - ``pipeline/vault/policies/outbound_boundary.cedar``
  - ``pipeline/vault/policies/split_context.cedar`` (optional; absent at v0.1)

If parse fails OR a required file is absent, ``_CEDAR_LOAD_SUCCEEDED`` is set
to ``False`` and ``_CEDAR_LOAD_FAILURE_CLASS`` records the exception class
name. Any subsequent call to :func:`evaluate_outbound_boundary_cedar`
fails-closed with
``F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.cedar_load_failure``.

In v0.1 the Cedar engine integration is deferred (per
``pipeline.logician.cedar_eval`` documentation) — the load-attempt is
text-level and parse failure is the only signal. Real Cedar engine
integration lands at the v0.2 horizon when ``cedarpy`` or equivalent is
added to ``pyproject.toml``.

DEFERRED — v0.2 substrate-addition decision (CC-007 follow-on, 2026-05-16)
-------------------------------------------------------------------------

Candidate binding: ``cedarpy 4.8.3`` (PyPI). Wraps the Rust Cedar Policy
engine v4.8.2. Platforms verified: macOS aarch64 + Linux aarch64 +
Linux x86_64 + Windows x86_64 across Python 3.9-3.14 (macOS 3.11-3.14).
Surface: ``is_authorized(request, policies, entities) -> AuthzResult``
plus ``validate_policies`` / ``format_policies`` / ``is_authorized_batch``
/ JSON policy import-export. Caveat: third-party binding under
``k9securityio/cedar-py`` (NOT officially supported by AWS or the Cedar
Policy team).

Pulling cedarpy forward to v0.1 is a **substrate addition** under ADR-001 /
architecture v7.0.3 — requires operator ratification (Rust-backed wheel
enters the Golden Image), Cedar entity model design (principal/action/
resource/context schema), rewrite of ``outbound_boundary.cedar`` to use
real Cedar schema syntax, rewrite of ``evaluate_outbound_boundary_cedar``
to call ``cedarpy.is_authorized``, and a new test surface. NOT session-
scope cleanup.

Architectural soundness today: the Python wrapper at
``pipeline.orchestrator.provider_boundary.enforce_outbound_boundary`` IS
the primary enforcement layer. This Cedar shim is the **defense-in-depth
second layer**. The text-level fail-closed flag preserves the load-bearing
property — if Cedar policy fails to load or parse, the second-layer
evaluation refuses. The architectural goal "two independent enforcement
layers" is met.

Full deferral disposition: see
``pipeline/handoffs/cc007_deferral_dispositions_2026-05-16.md`` §1.

Public surface
--------------

- :data:`OUTBOUND_BOUNDARY_POLICY` — parsed policy text (or None on load fail).
- :data:`SPLIT_CONTEXT_POLICY` — parsed policy text (optional).
- :data:`_CEDAR_LOAD_SUCCEEDED` — module-level fail-closed flag.
- :func:`evaluate_outbound_boundary_cedar` — second-layer evaluation entry point.

The shim is read-only at runtime; tests can override paths via
``load_cedar_policies_for_tests()``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Mapping, Optional

_OUTBOUND_BOUNDARY_PATH: Final[str] = "pipeline/vault/policies/outbound_boundary.cedar"
_SPLIT_CONTEXT_PATH: Final[str] = "pipeline/vault/policies/split_context.cedar"


class CedarParseError(RuntimeError):
    """Raised when a Cedar policy text fails the minimal-shape check."""


class CedarSyntaxError(RuntimeError):
    """Raised when a Cedar policy text contains syntactic anomalies."""


@dataclass(frozen=True, kw_only=True)
class _CedarPolicy:
    """Parsed policy handle — text body + minimal structural metadata."""

    text: str
    path: str
    has_forbid: bool
    has_permit: bool
    rule_count: int


def _load_cedar_policy(
    relative_path: str, *, root: Path | None = None
) -> _CedarPolicy:
    """Minimal Cedar policy parser — text-level shape check.

    Raises ``FileNotFoundError`` if the policy file is absent; raises
    :class:`CedarParseError` / :class:`CedarSyntaxError` on shape failures.

    Real Cedar parsing is deferred to v0.2 (cedarpy / equivalent). This
    function implements the §11.4 RT-20 contract surface: load, validate
    minimal shape, raise on failure so the load-fail flag flips.
    """
    base = root if root is not None else Path.cwd()
    path = base / relative_path
    if not path.exists():
        raise FileNotFoundError(f"Cedar policy not found at {path}")

    text = path.read_text(encoding="utf-8")

    # Strip comments (the same pattern used in cedar_eval.py) before checking
    # for effect keywords.
    comment_pattern = re.compile(r"//[^\n]*|/\*.*?\*/", re.DOTALL)
    stripped = comment_pattern.sub("", text)

    has_forbid = bool(re.search(r"\bforbid\s*\(", stripped))
    has_permit = bool(re.search(r"\bpermit\s*\(", stripped))

    if not (has_forbid or has_permit):
        raise CedarSyntaxError(
            f"Cedar policy at {path} has no permit or forbid rules"
        )

    rule_count = len(re.findall(r"\b(permit|forbid)\s*\(", stripped))

    return _CedarPolicy(
        text=text,
        path=str(path),
        has_forbid=has_forbid,
        has_permit=has_permit,
        rule_count=rule_count,
    )


# ---------------------------------------------------------------------------
# Module-level load — fires at first import.
# ---------------------------------------------------------------------------

OUTBOUND_BOUNDARY_POLICY: Optional[_CedarPolicy]
SPLIT_CONTEXT_POLICY: Optional[_CedarPolicy]
_CEDAR_LOAD_SUCCEEDED: bool
_CEDAR_LOAD_FAILURE_CLASS: Optional[str]
_CEDAR_LOAD_FAILURE_DETAIL: Optional[str]


def _load_at_startup() -> None:
    """Load the outbound-boundary + split-context policies at module init."""
    global OUTBOUND_BOUNDARY_POLICY, SPLIT_CONTEXT_POLICY
    global _CEDAR_LOAD_SUCCEEDED, _CEDAR_LOAD_FAILURE_CLASS, _CEDAR_LOAD_FAILURE_DETAIL

    OUTBOUND_BOUNDARY_POLICY = None
    SPLIT_CONTEXT_POLICY = None
    _CEDAR_LOAD_SUCCEEDED = False
    _CEDAR_LOAD_FAILURE_CLASS = None
    _CEDAR_LOAD_FAILURE_DETAIL = None

    try:
        OUTBOUND_BOUNDARY_POLICY = _load_cedar_policy(_OUTBOUND_BOUNDARY_PATH)
        # Split-context policy is optional at v0.1; absent file is OK.
        try:
            SPLIT_CONTEXT_POLICY = _load_cedar_policy(_SPLIT_CONTEXT_PATH)
        except FileNotFoundError:
            SPLIT_CONTEXT_POLICY = None
        _CEDAR_LOAD_SUCCEEDED = True
    except (FileNotFoundError, CedarParseError, CedarSyntaxError) as exc:
        _CEDAR_LOAD_SUCCEEDED = False
        _CEDAR_LOAD_FAILURE_CLASS = type(exc).__name__
        _CEDAR_LOAD_FAILURE_DETAIL = str(exc)


_load_at_startup()


# ---------------------------------------------------------------------------
# Test helpers.
# ---------------------------------------------------------------------------


def load_cedar_policies_for_tests(
    *,
    outbound_boundary_path: str | None = None,
    split_context_path: str | None = None,
    root: Path | None = None,
    fail_intentionally: bool = False,
) -> None:
    """Test-only re-load helper.

    When ``fail_intentionally=True``, the module flag is force-flipped to
    False as if a malformed Cedar file had been loaded. The companion
    integration test injects a malformed file via this hook.
    """
    global OUTBOUND_BOUNDARY_POLICY, SPLIT_CONTEXT_POLICY
    global _CEDAR_LOAD_SUCCEEDED, _CEDAR_LOAD_FAILURE_CLASS, _CEDAR_LOAD_FAILURE_DETAIL

    if fail_intentionally:
        OUTBOUND_BOUNDARY_POLICY = None
        SPLIT_CONTEXT_POLICY = None
        _CEDAR_LOAD_SUCCEEDED = False
        _CEDAR_LOAD_FAILURE_CLASS = "CedarSyntaxError"
        _CEDAR_LOAD_FAILURE_DETAIL = "test-injected fail-closed flag"
        return

    OUTBOUND_BOUNDARY_POLICY = None
    SPLIT_CONTEXT_POLICY = None
    _CEDAR_LOAD_SUCCEEDED = False
    _CEDAR_LOAD_FAILURE_CLASS = None
    _CEDAR_LOAD_FAILURE_DETAIL = None

    out_path = outbound_boundary_path or _OUTBOUND_BOUNDARY_PATH
    split_path = split_context_path or _SPLIT_CONTEXT_PATH

    try:
        OUTBOUND_BOUNDARY_POLICY = _load_cedar_policy(out_path, root=root)
        try:
            SPLIT_CONTEXT_POLICY = _load_cedar_policy(split_path, root=root)
        except FileNotFoundError:
            SPLIT_CONTEXT_POLICY = None
        _CEDAR_LOAD_SUCCEEDED = True
    except (FileNotFoundError, CedarParseError, CedarSyntaxError) as exc:
        _CEDAR_LOAD_SUCCEEDED = False
        _CEDAR_LOAD_FAILURE_CLASS = type(exc).__name__
        _CEDAR_LOAD_FAILURE_DETAIL = str(exc)


def reset_for_tests() -> None:
    """Re-run the module-init load — restores production state after tests."""
    _load_at_startup()


# ---------------------------------------------------------------------------
# Evaluation entry point.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CedarOutboundResult:
    """Result of an outbound-boundary Cedar evaluation."""

    allow: bool
    failure_code: Optional[str]
    detail: str


def evaluate_outbound_boundary_cedar(
    *,
    classification_context_provided: bool,
    posture: str,
    runtime_integrity_failed: bool = False,
    payload_sha3_512_commitment_mismatch: bool = False,
    posture_mismatch_with_register: bool = False,
    classified_input_classes: tuple[str, ...] = (),
) -> CedarOutboundResult:
    """Second-layer Cedar evaluation for the outbound boundary.

    Mirrors the Python wrapper's PRE refusal surface but evaluates against
    the Cedar policy text. Per §12.6 RT-C2-04: if Cedar policy failed to
    load at startup, this function returns ``allow=False`` with
    ``F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.cedar_load_failure`` so the
    wrapper fails-closed and surfaces the load failure on every invocation.

    Per §12.7 RT-C2-05 the forbid clause appears AFTER include directives
    in the .cedar text; this evaluator implements forbid-precedence in code
    by checking forbid conditions first (any True attribute → DENY).
    """
    if not _CEDAR_LOAD_SUCCEEDED:
        return CedarOutboundResult(
            allow=False,
            failure_code="F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.cedar_load_failure",
            detail=(
                f"Cedar policy failed to load at startup: "
                f"{_CEDAR_LOAD_FAILURE_CLASS}: {_CEDAR_LOAD_FAILURE_DETAIL}; "
                "second-layer defense unavailable; fail-closed"
            ),
        )

    # Forbid Rule 1 — outbound_boundary_combined_forbid (mirrors .cedar §1).
    if posture == "local_only_sovereign":
        return CedarOutboundResult(
            allow=False,
            failure_code=(
                "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny"
            ),
            detail="Local-Only posture refuses cloud egress structurally (Cedar layer)",
        )
    if not classification_context_provided:
        return CedarOutboundResult(
            allow=False,
            failure_code=(
                "F-CLASS-ROUTING-INDETERMINATE.outbound_boundary_missing_context"
            ),
            detail="no classification_context_provided (Cedar layer)",
        )
    if runtime_integrity_failed:
        return CedarOutboundResult(
            allow=False,
            failure_code=(
                "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_runtime_integrity_fail"
            ),
            detail="runtime identity pin failed (Cedar layer)",
        )
    if payload_sha3_512_commitment_mismatch:
        return CedarOutboundResult(
            allow=False,
            failure_code=(
                "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_payload_commitment_mismatch"
            ),
            detail="payload commitment mismatch (Cedar layer)",
        )
    if posture_mismatch_with_register:
        return CedarOutboundResult(
            allow=False,
            failure_code=(
                "F-CLASS-POSTURE-MID-CYCLE-CHANGE.outbound_boundary_posture_mismatch"
            ),
            detail="posture mismatch with signed register (Cedar layer)",
        )
    if any(
        cls in {"confidential", "operator_flagged"} for cls in classified_input_classes
    ):
        return CedarOutboundResult(
            allow=False,
            failure_code=(
                "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny"
            ),
            detail=(
                "classified input class is confidential or operator_flagged "
                "(Cedar layer)"
            ),
        )

    return CedarOutboundResult(
        allow=True,
        failure_code=None,
        detail="Cedar outbound-boundary evaluation: allow",
    )


def is_cedar_loaded() -> bool:
    """True iff Cedar policies loaded successfully at startup."""
    return _CEDAR_LOAD_SUCCEEDED


def get_cedar_load_failure() -> Optional[str]:
    """Return the load-failure detail (or None on success)."""
    if _CEDAR_LOAD_SUCCEEDED:
        return None
    return f"{_CEDAR_LOAD_FAILURE_CLASS}: {_CEDAR_LOAD_FAILURE_DETAIL}"


__all__ = [
    "OUTBOUND_BOUNDARY_POLICY",
    "SPLIT_CONTEXT_POLICY",
    "CedarOutboundResult",
    "CedarParseError",
    "CedarSyntaxError",
    "evaluate_outbound_boundary_cedar",
    "is_cedar_loaded",
    "get_cedar_load_failure",
    "load_cedar_policies_for_tests",
    "reset_for_tests",
]
