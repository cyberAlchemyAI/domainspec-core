"""§14 Report Generator — Cedar engine bootstrap + Python evaluator.

Per §14 v1 LOCK 2026-05-10 + Slice 2 handoff (2026-05-11). Mirrors the
``pipeline.orchestrator.seats.data_collector.__init__`` Cedar bootstrap
pattern and the ``pipeline.vault.sub_kinds.policy_eval`` Python evaluator
shape, scoped to the five ``report_*.cedar`` skeleton policies shipped
alongside the workspace's shared policy vault at
``pipeline/vault/policies/``.

Lifecycle posture (mirrors ``operational_subkinds.cedar``)
-------------------------------------------------------

* The five ``report_*.cedar`` files are SKELETONs at §14 v1 LOCK — human-
  auditable surfaces that pair with the authoritative Python predicate
  bodies under ``pipeline.logician.gates.f_report_*.py``.
* This module's ``evaluate_report_finalize_action`` is authoritative at
  v0.2: it composes the 5 gate result types into a Cedar-flavoured
  PERMIT / DENY decision shape. The .cedar text load + grammar floor
  + ``is_ready() is True`` identity check is the audit surface that
  proves the human-auditable skeletons are present and well-formed.

Bootstrap discipline (per WS-I §13 v1 RT-06 + RT-C2-04 closures)
-------------------------------------------------------------

* ``CriticalPolicyError`` subclasses :class:`BaseException` so upstream
  ``try/except Exception`` blocks cannot silently swallow Cedar engine
  load failures. Mirrors :class:`pipeline.orchestrator.seats.data_collector.CriticalPolicyError`.
* The readiness check is identity-strict (``engine.is_ready() is True``).
* Module-load bootstrap fail-closes the module import on any failure.
* Lazy import of ``CedarEngine`` so this seat package remains importable
  for type-checking without eager-loading the Cedar substrate.

The Cedar policy directory is the workspace-shared
``pipeline/vault/policies/`` — Report Generator does NOT ship its own
seat-scoped ``cedar_policies/`` subtree (the policy authority is the
shared vault; Report Generator's bootstrap filters by ``report_*.cedar``
filename prefix so other policies in the same dir don't bleed into the
report_mode evaluator).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Mapping, Optional, Protocol, runtime_checkable

from ._schemas import (
    BUNDLE_STATE_DRAFT_PENDING,
    BUNDLE_STATE_FINALIZED,
    GrantReportBundle,
)


# ---------------------------------------------------------------------------
# Failure code references — these are the F-REPORT-* codes the gate
# modules emit. We do not import the gate modules at module load (avoids
# a circular import + keeps this module decoupled from gate signatures);
# instead we treat any gate-result type with a ``failure_code`` attribute
# as the authoritative source of the per-gate verdict.
# ---------------------------------------------------------------------------

F_REPORT_COMMITMENT_UNTRACED: Final[str] = "F-REPORT-COMMITMENT-UNTRACED"
F_REPORT_COMMITMENT_MISSED: Final[str] = "F-REPORT-COMMITMENT-MISSED"
F_REPORT_OUT_OF_SCOPE_DRIFT: Final[str] = "F-REPORT-OUT-OF-SCOPE-DRIFT"
F_REPORT_NUMERIC_DRIFT: Final[str] = "F-REPORT-NUMERIC-DRIFT"
F_REPORT_TEMPLATE_MISMATCH: Final[str] = "F-REPORT-TEMPLATE-MISMATCH"

REPORT_FAILURE_CODES: Final[frozenset[str]] = frozenset(
    {
        F_REPORT_COMMITMENT_UNTRACED,
        F_REPORT_COMMITMENT_MISSED,
        F_REPORT_OUT_OF_SCOPE_DRIFT,
        F_REPORT_NUMERIC_DRIFT,
        F_REPORT_TEMPLATE_MISMATCH,
    }
)

# Canonical filename → failure code mapping. The five report_*.cedar
# skeleton files pair 1:1 with the five F-REPORT-* failure codes.
_POLICY_NAME_TO_FAILURE_CODE: Final[Mapping[str, str]] = {
    "report_commitment_untraced": F_REPORT_COMMITMENT_UNTRACED,
    "report_commitment_missed": F_REPORT_COMMITMENT_MISSED,
    "report_out_of_scope_drift": F_REPORT_OUT_OF_SCOPE_DRIFT,
    "report_numeric_drift": F_REPORT_NUMERIC_DRIFT,
    "report_template_mismatch": F_REPORT_TEMPLATE_MISMATCH,
}

REQUIRED_REPORT_POLICY_NAMES: Final[frozenset[str]] = frozenset(
    _POLICY_NAME_TO_FAILURE_CODE
)


# ---------------------------------------------------------------------------
# Policy dir resolution
# ---------------------------------------------------------------------------


# pipeline/orchestrator/seats/report_generator/_cedar_bootstrap.py
#   → parents[3] == pipeline/
# Pipeline-shared vault: pipeline/vault/policies/
_REPORT_CEDAR_POLICY_DIR: Final[Path] = (
    Path(__file__).resolve().parents[3] / "vault" / "policies"
)


def report_cedar_policy_dir() -> Path:
    """Return the canonical directory the bootstrap reads ``report_*.cedar`` from.

    Test fixtures use the canonical path; tests that want to override the
    dir construct their own loader call (``load_report_cedar_policies`` /
    ``_bootstrap_cedar_engine_at``) with an explicit ``policy_dir`` arg.
    """
    return _REPORT_CEDAR_POLICY_DIR


# ---------------------------------------------------------------------------
# Critical policy error (mirrors data_collector pattern)
# ---------------------------------------------------------------------------


class CriticalPolicyError(BaseException):
    """Raised on Cedar engine load failure for the Report Generator seat.

    Subclasses :class:`BaseException` so upstream ``try/except Exception``
    blocks cannot silently swallow Cedar load failures (mirrors
    :class:`pipeline.orchestrator.seats.data_collector.CriticalPolicyError`
    per WS-I §13 v1 RT-C2-04 closure).
    """


# ---------------------------------------------------------------------------
# Engine handle (Protocol alias) — see data_collector for the same pattern
# ---------------------------------------------------------------------------


class CedarEngineRef(Protocol):
    """Structural alias for :class:`pipeline.logician.cedar_eval.CedarEngine`."""

    def load_all(self) -> None: ...

    def is_ready(self) -> bool: ...

    def loaded_policy_names(self) -> tuple[str, ...]: ...

    def policy_text(self, name: str) -> str: ...


_cedar_engine: Optional[CedarEngineRef] = None
_report_policy_texts: Optional[Mapping[str, str]] = None


# ---------------------------------------------------------------------------
# Policy text loader
# ---------------------------------------------------------------------------


def load_report_cedar_policies(
    policy_dir: Optional[Path] = None,
) -> dict[str, str]:
    """Read the 5 ``report_*.cedar`` skeleton policies into a dict.

    Returns ``{policy_name: text}`` where ``policy_name`` is the file
    stem (e.g. ``"report_commitment_untraced"``).

    Failure modes:

    * ``policy_dir`` missing / not a directory → :class:`CriticalPolicyError`.
    * Any of the five required policies missing → :class:`CriticalPolicyError`
      (mirrors data_collector's "load_all then verify the closed set" pattern).
    * Read IOError → :class:`CriticalPolicyError`.

    The loaded text is NOT compiled here — Cedar compilation is the
    :class:`pipeline.logician.cedar_eval.CedarEngine` responsibility (see
    :func:`_bootstrap_cedar_engine_at`). This loader is the audit-surface
    helper Tilth's audit trail consumes (the orchestrator can diff the
    loaded text against the on-disk artefact at audit time).
    """
    target = policy_dir if policy_dir is not None else _REPORT_CEDAR_POLICY_DIR
    target = Path(target)
    if not target.is_dir():
        raise CriticalPolicyError(
            f"report_cedar policy_dir is not a directory: {target!r}"
        )

    found: dict[str, str] = {}
    for stem in sorted(REQUIRED_REPORT_POLICY_NAMES):
        path = target / f"{stem}.cedar"
        if not path.is_file():
            raise CriticalPolicyError(
                f"required report Cedar policy missing: {path!r}"
            )
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise CriticalPolicyError(
                f"failed to read report Cedar policy {path!r}: {exc}"
            ) from exc
        if not text.strip():
            raise CriticalPolicyError(
                f"report Cedar policy is empty: {path!r}"
            )
        found[stem] = text

    missing = REQUIRED_REPORT_POLICY_NAMES - frozenset(found)
    if missing:
        raise CriticalPolicyError(
            f"required report Cedar policies missing: {sorted(missing)!r}"
        )
    return found


# ---------------------------------------------------------------------------
# Engine bootstrap — mirrors data_collector pattern
# ---------------------------------------------------------------------------


# Comment-stripping pattern for the grammar floor check below — mirrors
# the one used by ``cedar_eval._bundled_grammar_floor`` so this module's
# verification matches the engine's.
_CEDAR_COMMENT_RE: Final[re.Pattern[str]] = re.compile(r"//[^\n]*")


def _verify_text_grammar_floor(text: str) -> tuple[bool, str]:
    """Local grammar-floor mirror of ``cedar_eval._bundled_grammar_floor``.

    Kept here so :func:`load_report_cedar_policies` can fail-closed at
    load time WITHOUT eager-importing the engine module.
    """
    stripped = text.strip()
    if not stripped:
        return False, "policy text is empty"
    no_comments = _CEDAR_COMMENT_RE.sub("", stripped)
    if "permit" not in no_comments and "forbid" not in no_comments:
        return False, "policy text contains neither 'permit' nor 'forbid'"
    return True, ""


def _bootstrap_cedar_engine_at(policy_dir: Optional[Path] = None) -> CedarEngineRef:
    """Construct + load a CedarEngine pinned to ``policy_dir``.

    Used by :func:`_bootstrap_cedar_engine` for module-load wiring and by
    tests that need a fresh engine against a fixture policy dir.

    Failure raises :class:`CriticalPolicyError`. The readiness check is
    identity-strict (``engine.is_ready() is True``) per WS-I §13 RT-C2-04.
    """
    target = policy_dir if policy_dir is not None else _REPORT_CEDAR_POLICY_DIR
    target = Path(target)

    # First — verify the 5 required report policies are present + well-
    # formed at the grammar floor BEFORE we hand the directory to
    # CedarEngine. CedarEngine walks every *.cedar in the dir; the shared
    # vault may carry other unrelated policies. This loader gates entry by
    # explicit policy-name verification.
    texts = load_report_cedar_policies(policy_dir=target)
    for name, text in texts.items():
        ok, detail = _verify_text_grammar_floor(text)
        if not ok:
            raise CriticalPolicyError(
                f"report Cedar policy {name!r} failed grammar floor: {detail}"
            )

    # Lazy import per data_collector pattern.
    from pipeline.logician.cedar_eval import CedarEngine

    engine = CedarEngine(policy_dir=target)
    try:
        engine.load_all()
    except BaseException as exc:
        raise CriticalPolicyError(
            f"Cedar engine load failure at module load: {exc}"
        ) from exc
    if engine.is_ready() is not True:
        # Identity-strict per v7.0.7 §4.3.4 + WS-I RT-C2-04.
        raise CriticalPolicyError(
            "CedarEngine.is_ready() returned non-True; fail-closed"
        )
    # Verify the engine actually loaded all 5 report policies (the dir may
    # contain additional non-report cedar files; we only require the 5).
    loaded_names = frozenset(engine.loaded_policy_names())
    missing = REQUIRED_REPORT_POLICY_NAMES - loaded_names
    if missing:
        raise CriticalPolicyError(
            f"Cedar engine loaded {sorted(loaded_names)!r} but is missing required "
            f"report policies: {sorted(missing)!r}"
        )
    return engine


def _bootstrap_cedar_engine() -> None:
    """Module-level Cedar engine bootstrap, called at import time.

    Populates module-level ``_cedar_engine`` + ``_report_policy_texts``.
    Mirrors the data_collector pattern: failure → :class:`CriticalPolicyError`
    propagation aborts the importing process.
    """
    engine = _bootstrap_cedar_engine_at()
    # Cache the policy-text dict alongside the engine handle so callers
    # that want raw text without re-touching disk can pull from
    # ``get_report_policy_texts``.
    texts = load_report_cedar_policies()
    globals()["_cedar_engine"] = engine
    globals()["_report_policy_texts"] = texts


def get_cedar_engine() -> CedarEngineRef:
    """Return the module-load Cedar engine handle.

    Raises :class:`CriticalPolicyError` if the engine is not available —
    in practice unreachable because ``_bootstrap_cedar_engine`` runs at
    import and any failure aborts the import.
    """
    engine = globals().get("_cedar_engine")
    if engine is None:
        raise CriticalPolicyError(
            "Cedar engine not initialised; _bootstrap_cedar_engine() did not "
            "run or aborted before assignment"
        )
    return engine


def get_report_policy_texts() -> Mapping[str, str]:
    """Return the loaded ``report_*.cedar`` text dict (frozen view)."""
    texts = globals().get("_report_policy_texts")
    if texts is None:
        raise CriticalPolicyError(
            "report policy texts not loaded; _bootstrap_cedar_engine() did not "
            "run or aborted before assignment"
        )
    return texts


# ---------------------------------------------------------------------------
# Python-side evaluator (mirrors pipeline.vault.sub_kinds.policy_eval shape)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CedarVerdict:
    """Python-side Cedar verdict for the report_finalize_action decision.

    Mirrors ``CedarDecision`` shape from
    :mod:`pipeline.logician.cedar_eval` but scoped to the
    Report Generator finalize_action principal/action.

    * ``decision`` — "PERMIT" iff every supplied gate result is success;
      "DENY" iff any non-success gate result fired.
    * ``rule`` — Cedar rule that fired the DENY (matches a ``Rule N``
      comment in the .cedar skeleton); ``None`` on PERMIT.
    * ``failure_code`` — the F-REPORT-* code of the firing gate; ``None``
      on PERMIT.
    * ``sub_tags`` — the firing sub-tags collected from the gate's
      ``fired_sub_tags`` property (empty on PERMIT or on gates that don't
      expose sub-tags).
    * ``detail`` — human-readable explanation.
    """

    decision: str
    rule: Optional[str] = None
    failure_code: Optional[str] = None
    sub_tags: tuple[str, ...] = field(default_factory=tuple)
    detail: str = ""

    def __post_init__(self) -> None:
        if self.decision not in ("PERMIT", "DENY"):
            raise ValueError(
                f"CedarVerdict.decision must be PERMIT|DENY, got {self.decision!r}"
            )


# Per-failure-code Cedar rule identifier — names the rule comment in the
# corresponding .cedar skeleton that the Python evaluator mirrors.
_RULE_FOR_FAILURE_CODE: Final[Mapping[str, str]] = {
    F_REPORT_COMMITMENT_UNTRACED: "refuse_finalize_with_untraced_claims",
    F_REPORT_COMMITMENT_MISSED: "refuse_judge_score_with_missed_required_subsection",
    F_REPORT_OUT_OF_SCOPE_DRIFT: "refuse_write_finalized_with_scope_drift",
    F_REPORT_NUMERIC_DRIFT: "refuse_write_finalized_with_value_drift",
    F_REPORT_TEMPLATE_MISMATCH: "refuse_dispatch_with_workspace_template_drift",
}


def _gate_is_pass(gate_result: object) -> bool:
    """Return True iff the gate result indicates PASS.

    Each F-REPORT-* gate exposes a ``success: bool`` attribute (per
    Slice 1 schema). ``None`` (gate not run) is treated as PASS — the
    evaluator's contract is "DENY when any gate that ran failed"; a gate
    that wasn't supplied is out of scope for this evaluation.
    """
    if gate_result is None:
        return True
    success = getattr(gate_result, "success", None)
    if success is None:
        raise TypeError(
            f"gate result of type {type(gate_result).__name__} has no .success "
            f"attribute; cannot evaluate"
        )
    return bool(success)


def _gate_sub_tags(gate_result: object) -> tuple[str, ...]:
    """Extract ``fired_sub_tags`` from a gate result if present."""
    if gate_result is None:
        return ()
    sub_tags = getattr(gate_result, "fired_sub_tags", None)
    if sub_tags is None:
        return ()
    return tuple(sub_tags)


def _gate_findings_detail(gate_result: object) -> str:
    """Extract a compact detail string from a gate result's findings."""
    if gate_result is None:
        return ""
    findings = getattr(gate_result, "findings", None)
    if not findings:
        return ""
    parts: list[str] = []
    for f in findings[:3]:  # cap for log readability
        sub_tag = getattr(f, "sub_tag", "<sub_tag?>")
        detail = getattr(f, "detail", "<detail?>")
        parts.append(f"{sub_tag}: {detail}")
    if len(findings) > 3:
        parts.append(f"... (+{len(findings) - 3} more)")
    return " | ".join(parts)


def evaluate_report_finalize_action(
    bundle: GrantReportBundle,
    *,
    commitment_untraced: Optional[object] = None,
    numeric_drift: Optional[object] = None,
    template_mismatch: Optional[object] = None,
    out_of_scope_drift: Optional[object] = None,
    commitment_missed: Optional[object] = None,
) -> CedarVerdict:
    """Compose the 5 F-REPORT-* gate results into a Cedar PERMIT/DENY verdict.

    Mirrors :func:`pipeline.vault.sub_kinds.policy_eval.evaluate_operational_write`
    but for the ``ReportGenerator::finalize_action`` principal +
    ``Vault::write_finalized_report`` action.

    Decision protocol:

    1. ``bundle`` MUST be a :class:`GrantReportBundle` in
       ``DRAFT_PENDING_OPERATOR_SIGN`` state. Calling this evaluator on a
       FINALIZED bundle is a contract violation (operator-sign is a
       precondition for finalization; the evaluator runs at the moment
       of operator-sign, not after).
    2. Each supplied gate result is checked: any non-success fail-closes
       to DENY with the gate's ``failure_code`` + Cedar rule pointer.
    3. The first firing gate wins (deterministic per
       ``REPORT_FAILURE_CODES`` iteration order); the verdict carries the
       sub-tag list from THAT gate. Operator triages further failures
       from the per-gate results returned alongside the verdict.
    4. PERMIT iff every supplied gate is success.

    Identity discipline: every ``success`` attribute is read as a bool;
    falsy non-bool values fail-closed.
    """
    if not isinstance(bundle, GrantReportBundle):
        raise TypeError(
            f"bundle must be GrantReportBundle, got {type(bundle).__name__}"
        )
    if bundle.bundle_state == BUNDLE_STATE_FINALIZED:
        raise ValueError(
            "evaluate_report_finalize_action invoked on FINALIZED bundle; "
            "the finalize_action evaluator runs at sign time, not post-sign"
        )
    if bundle.bundle_state != BUNDLE_STATE_DRAFT_PENDING:
        raise ValueError(
            f"bundle.bundle_state must be {BUNDLE_STATE_DRAFT_PENDING!r}; "
            f"got {bundle.bundle_state!r}"
        )

    # Iterate the gates in deterministic failure-code order.
    gate_results_by_code: Mapping[str, object] = {
        F_REPORT_TEMPLATE_MISMATCH: template_mismatch,
        F_REPORT_COMMITMENT_MISSED: commitment_missed,
        F_REPORT_COMMITMENT_UNTRACED: commitment_untraced,
        F_REPORT_OUT_OF_SCOPE_DRIFT: out_of_scope_drift,
        F_REPORT_NUMERIC_DRIFT: numeric_drift,
    }

    for failure_code, result in gate_results_by_code.items():
        if _gate_is_pass(result):
            continue
        rule = _RULE_FOR_FAILURE_CODE[failure_code]
        sub_tags = _gate_sub_tags(result)
        detail_findings = _gate_findings_detail(result)
        detail = (
            f"DENY {rule}: {failure_code}"
            + (f" sub_tags={list(sub_tags)!r}" if sub_tags else "")
            + (f"; findings: {detail_findings}" if detail_findings else "")
        )
        return CedarVerdict(
            decision="DENY",
            rule=rule,
            failure_code=failure_code,
            sub_tags=sub_tags,
            detail=detail,
        )

    return CedarVerdict(
        decision="PERMIT",
        rule=None,
        failure_code=None,
        sub_tags=(),
        detail=(
            f"PERMIT finalize_action: bundle run_id={bundle.run_id!r} "
            f"period_n={bundle.period_n}"
        ),
    )


# ---------------------------------------------------------------------------
# Module-level Cedar bootstrap — fires at import time
# ---------------------------------------------------------------------------


_bootstrap_cedar_engine()


__all__ = [
    "CedarEngineRef",
    "CedarVerdict",
    "CriticalPolicyError",
    "F_REPORT_COMMITMENT_MISSED",
    "F_REPORT_COMMITMENT_UNTRACED",
    "F_REPORT_NUMERIC_DRIFT",
    "F_REPORT_OUT_OF_SCOPE_DRIFT",
    "F_REPORT_TEMPLATE_MISMATCH",
    "REPORT_FAILURE_CODES",
    "REQUIRED_REPORT_POLICY_NAMES",
    "_bootstrap_cedar_engine_at",
    "evaluate_report_finalize_action",
    "get_cedar_engine",
    "get_report_policy_texts",
    "load_report_cedar_policies",
    "report_cedar_policy_dir",
]
