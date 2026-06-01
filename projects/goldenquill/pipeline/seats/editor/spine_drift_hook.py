"""pipeline.seats.editor.spine_drift_hook — Editor-side F-LOGICIAN-SPINE-DRIFT
hook with pre/post delta semantics.

Why a separate hook (not a pure ``check_spine_drift`` reuse)
-------------------------------------------------------------
The Logician POST-gate (``pipeline.logician.post_gate.run_post_gate_skeleton``)
already wires :func:`pipeline.logician.gates.f_logician_spine_drift.check_spine_drift`
for Scribe-output drift detection. That same function would technically
work on Editor outputs too — but flat reuse loses signal:

- A section may already drift the spine *before* Editor touches it
  (Scribe authored a weak framing). That's a Scribe failure surfaced at
  the SP2 stop point, not an Editor failure.
- A section may drift *after* Editor's edits are applied (Editor
  silently weakened a framing while polishing prose). That's the
  failure mode Editor-side enforcement exists to catch.

Conflating the two — flagging Editor for drift Scribe introduced —
floods the operator with false positives at SP4 and dilutes the signal
that Editor-applied edits can introduce framing damage.

This hook computes a **delta**: spine adherence BEFORE Editor edits vs.
AFTER. New findings in the post-Editor result that weren't in the
pre-Editor result are attributed to Editor. Pre-existing findings are
preserved in the result so the operator sees the full picture, but
``delta_findings`` is the actionable Editor-specific signal.

Stop-point integration
----------------------
SP4 — Post-Editor / Pre-Judge (per
``pipeline/roadmap/explorations/narrative_spine_design.md``):

  Operator sees Editor's clarity changes alongside spine adherence
  delta. Anything Editor moved that drifted the spine surfaces
  explicitly. Operator approves, reverts, or sends back to Editor.

The orchestrator calls this hook between Editor's edit-application and
Judge's rubric scoring. Pass:

- ``pre_editor_section_text``: the Scribe-drafted section body that fed
  Editor's review. Same string Logician's Scribe-side POST-gate already
  evaluated.
- ``post_editor_section_text``: the section body that emerges after
  Editor's R2-validated feedback has been applied (orchestrator
  responsibility — this hook does not apply edits, only evaluates the
  resulting text).

Verdict
-------
- ``PASS`` when ``delta_findings`` is empty (Editor preserved spine
  adherence).
- ``FAIL`` (failure code ``F-LOGICIAN-SPINE-DRIFT``) when Editor
  introduced new findings.

Pre-existing findings are not a verdict failure here — they're Scribe's
problem and would have been caught at SP2. This hook fires only on
Editor-introduced drift.

Sovereignty / dependency posture
--------------------------------
Pure-stdlib + the existing pyyaml-driven spine loader. No new substrate
deps. Imports the spine-drift gate's public API only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from pipeline.logician.gates.f_logician_spine_drift import (
    F_LOGICIAN_SPINE_DRIFT,
    SpineDriftFinding,
    SpineDriftGateResult,
    check_spine_drift,
)


# --------------------------------------------------------------------------
# Result
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True, slots=True)
class EditorSpineDeltaResult:
    """Outcome of pre/post spine-drift comparison around Editor edits.

    Attributes:
        verdict: "PASS" iff ``delta_findings`` is empty.
        failure_code: ``F-LOGICIAN-SPINE-DRIFT`` when verdict is FAIL,
            otherwise None. Mirrors the underlying gate's failure code so
            the orchestrator's failure-codes tuple stays uniform.
        pre_editor_findings: Findings on the Scribe-authored section
            text. Operator sees these for context but they are NOT
            treated as Editor-side failures here.
        post_editor_findings: Findings on the post-Editor section text.
            Superset of ``delta_findings``.
        delta_findings: Findings present post-Editor that were NOT
            present pre-Editor — the Editor-introduced drift signal.
            Identity computed by (framing_id, reason_tag) tuple; a
            finding with the same identity but different ``detail``
            string is treated as the same finding (e.g. dialect drift
            with the same mismatch reason).
        pre_editor_verdict: Convenience copy of the pre-Editor
            underlying gate's verdict — useful for SP4 review surface.
        post_editor_verdict: Same for post-Editor.
    """

    verdict: Literal["PASS", "FAIL"]
    failure_code: Optional[str] = None
    pre_editor_findings: tuple[SpineDriftFinding, ...] = ()
    post_editor_findings: tuple[SpineDriftFinding, ...] = ()
    delta_findings: tuple[SpineDriftFinding, ...] = ()
    pre_editor_verdict: Literal["PASS", "FAIL"] = "PASS"
    post_editor_verdict: Literal["PASS", "FAIL"] = "PASS"


# --------------------------------------------------------------------------
# Internal — finding identity
# --------------------------------------------------------------------------

def _finding_identity(f: SpineDriftFinding) -> tuple[str | None, str]:
    """Stable identity for delta comparison.

    Two findings with the same (framing_id, reason_tag) are treated as
    the same drift incident — so an Editor edit that doesn't introduce
    a NEW kind of drift (just preserves a pre-existing one) is not
    counted against Editor.
    """
    return (f.framing_id, f.reason_tag)


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------

def check_editor_spine_delta(
    *,
    pre_editor_section_text: str,
    post_editor_section_text: str,
    section_id: str,
    section_dialect: str,
    spine_path: Path,
) -> EditorSpineDeltaResult:
    """Editor-side spine-drift hook with pre/post delta semantics.

    Args:
        pre_editor_section_text: Section body Scribe drafted (what
            Editor reviewed and produced feedback on).
        post_editor_section_text: Section body after Editor's
            R2-validated feedback has been applied. Caller is
            responsible for the application; this hook only evaluates.
        section_id: Canonical section identifier (e.g. "1.A.2").
        section_dialect: Caller's classified dialect for the post-Editor
            text. (Pre-Editor dialect is assumed identical — Editor edits
            should not change funder-dialect register; if they did,
            that's also Editor drift.)
        spine_path: Path to ``orgs/<org>/grants/<grant_id>/spine.locked.yaml``.

    Returns:
        :class:`EditorSpineDeltaResult` with PASS when Editor introduced
        no new drift, FAIL when at least one new finding emerged.
        Structural failures in the underlying gate (missing spine,
        schema error) propagate as FAIL with the same finding shape so
        the orchestrator's failure surface stays uniform.
    """
    pre_result: SpineDriftGateResult = check_spine_drift(
        section_text=pre_editor_section_text,
        section_id=section_id,
        section_dialect=section_dialect,
        spine_path=spine_path,
    )
    post_result: SpineDriftGateResult = check_spine_drift(
        section_text=post_editor_section_text,
        section_id=section_id,
        section_dialect=section_dialect,
        spine_path=spine_path,
    )

    # If the spine itself can't be loaded (missing file, schema error),
    # both pre/post results carry the same structural finding. Surface
    # that as FAIL so SP4 doesn't silently swallow it.
    if any(f.reason_tag in ("spine_missing", "spine_schema_error")
           for f in post_result.findings):
        return EditorSpineDeltaResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_SPINE_DRIFT,
            pre_editor_findings=pre_result.findings,
            post_editor_findings=post_result.findings,
            delta_findings=post_result.findings,
            pre_editor_verdict=pre_result.verdict,
            post_editor_verdict=post_result.verdict,
        )

    # Compute delta — findings present post but not pre
    pre_identities = {_finding_identity(f) for f in pre_result.findings}
    delta = tuple(
        f for f in post_result.findings
        if _finding_identity(f) not in pre_identities
    )

    if delta:
        return EditorSpineDeltaResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_SPINE_DRIFT,
            pre_editor_findings=pre_result.findings,
            post_editor_findings=post_result.findings,
            delta_findings=delta,
            pre_editor_verdict=pre_result.verdict,
            post_editor_verdict=post_result.verdict,
        )

    return EditorSpineDeltaResult(
        verdict="PASS",
        pre_editor_findings=pre_result.findings,
        post_editor_findings=post_result.findings,
        delta_findings=(),
        pre_editor_verdict=pre_result.verdict,
        post_editor_verdict=post_result.verdict,
    )


__all__ = [
    "EditorSpineDeltaResult",
    "check_editor_spine_delta",
]
