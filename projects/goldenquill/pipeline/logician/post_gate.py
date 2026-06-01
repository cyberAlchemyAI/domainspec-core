"""POST-gate skeleton — F-POST-10 (hard-block) + F-POST-11 (unsourced). [§4.4]

Round 2 floor: a deterministic skeleton that consumes pre-classified claim
tuples (Round 3's BT10 classifier will populate them) and the M8 admin-risk
hard-block count (Round 1's verifier surfaces it), assembles the
ClaimEvidenceMap (Round 2's `claim_evidence.assemble_claim_evidence_map`),
and applies the two POST-gate hard-floor predicates:

* `F-POST-10.hard_block_unresolved` — admin_risk_hard_block_count > 0
* `F-POST-11.unsourced_unresolved`  — any claim tagged UNSOURCED

The full POST-gate (§4.4.1 thirteen-step sequence including PRE-invariant
re-verify, claim extraction invocation, BT10/S11c verification, structural
checks, rails-report assembly, vault-write atomic commit) is the Round 6
capstone. Round 2 deliberately exposes only the artifact-and-predicate floor
so Rounds 3-5 can wire their checks without circular-dependency risk.

Per §4.4.4, POST-gate produces artifacts even on failure: the operator sees
the map to decide which §4.4.2 UNSOURCED resolution path to take. Therefore
`PostGateResult.claim_evidence_map` is populated regardless of `success`.

v0.2 additions
--------------
Three v0.2 gates wired in via optional kwargs. Each fires only when its
full input set is supplied; missing inputs preserve Round-2-floor
backward-compat for callers not yet sector-aware.

* ``F-LOGICIAN-FABRICATED-ORG`` — fires when ``draft_text`` +
  ``project_context`` provided. Spec card:
  ``pipeline/engineering/spec_cards/logician_fabricated_org_ner_gate.md``.
* ``F-LOGICIAN-SPINE-DRIFT`` — fires when ``draft_text`` + ``spine_path``
  + ``section_id`` + ``section_dialect`` provided. Spec card:
  ``pipeline/engineering/spec_cards/logician_spine_drift_gate.md``.
* ``F-LOGICIAN-FACT-DRIFT`` — fires when ``draft_text`` + ``kfr_path``
  + ``grant_funding_period`` provided. Spec card:
  ``pipeline/engineering/spec_cards/logician_fact_drift_kfr_gate.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Optional

from pipeline.logician.claim_evidence import (
    ClaimEntry,
    ClaimEvidenceMap,
    assemble_claim_evidence_map,
)
from pipeline.logician.gates.f_logician_fabricated_org import (
    F_LOGICIAN_FABRICATED_ORG,
    FabricatedOrgGateResult,
    check_fabricated_orgs,
)
from pipeline.logician.gates.f_logician_fact_drift import (
    F_LOGICIAN_FACT_DRIFT,
    FactDriftGateResult,
    check_fact_drift,
)
from pipeline.logician.gates.f_logician_spine_drift import (
    F_LOGICIAN_SPINE_DRIFT,
    SpineDriftGateResult,
    check_spine_drift,
)


# ---------------------------------------------------------------------------
# Failure-code constants (blueprint §6.2)
# ---------------------------------------------------------------------------


F_POST_10: str = "F-POST-10"
F_POST_11: str = "F-POST-11"


# ---------------------------------------------------------------------------
# Result + exception
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PostGateResult:
    success: bool
    claim_evidence_map: Optional[ClaimEvidenceMap]
    unsourced_count: int
    hard_block_count: int
    failure_codes: tuple[str, ...]
    # v0.2 — gate-specific results (None when the gate was not invoked
    # because its full input set was not supplied — see kwargs on
    # `run_post_gate_skeleton`).
    fabricated_org_result: Optional[FabricatedOrgGateResult] = None
    spine_drift_result: Optional[SpineDriftGateResult] = None
    fact_drift_result: Optional[FactDriftGateResult] = None


class PostGateSkeletonFailed(RuntimeError):
    """Raised by callers that prefer fail-closed propagation over result-shape."""

    def __init__(self, failure_codes: tuple[str, ...]) -> None:
        super().__init__(f"POST-gate skeleton failed: {failure_codes}")
        self.failure_codes = failure_codes


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run_post_gate_skeleton(
    *,
    draft_hash: str,
    rfa_hash: str,
    session_id: str,
    org_slug: str,
    rfa_url_hash: str,
    claims: tuple[ClaimEntry, ...],
    rigor_breach_active: bool,
    admin_risk_hard_block_count: int,
    generated_at_utc: str,
    # v0.2 — fabricated-org gate inputs. Optional for backward compat:
    # callers that don't supply both `draft_text` and `project_context`
    # get the original Round-2-floor behaviour. When supplied, the gate
    # runs and may append F-LOGICIAN-FABRICATED-ORG to failure_codes.
    draft_text: Optional[str] = None,
    project_context: Optional[Mapping[str, Any]] = None,
    rfa_issuer: Optional[str] = None,
    # v0.2 — spine-drift gate inputs. All three required to invoke
    # alongside draft_text. May append F-LOGICIAN-SPINE-DRIFT.
    spine_path: Optional[Path] = None,
    section_id: Optional[str] = None,
    section_dialect: Optional[str] = None,
    # v0.2 — fact-drift gate inputs. Both required to invoke alongside
    # draft_text. May append F-LOGICIAN-FACT-DRIFT.
    kfr_path: Optional[Path] = None,
    grant_funding_period: Optional[tuple[date, date]] = None,
) -> PostGateResult:
    if not isinstance(claims, tuple):
        raise TypeError(
            f"claims must be a tuple of ClaimEntry, got {type(claims).__name__}"
        )
    for c in claims:
        if not isinstance(c, ClaimEntry):
            raise TypeError(f"claim must be ClaimEntry, got {type(c).__name__}")
    if not isinstance(admin_risk_hard_block_count, int) or admin_risk_hard_block_count < 0:
        raise ValueError("admin_risk_hard_block_count must be non-negative int")

    cmap = assemble_claim_evidence_map(
        draft_hash=draft_hash,
        rfa_hash=rfa_hash,
        session_id=session_id,
        org_slug=org_slug,
        rfa_url_hash=rfa_url_hash,
        claims=claims,
        rigor_breach_active=rigor_breach_active,
        generated_at_utc=generated_at_utc,
        hard_block_count=admin_risk_hard_block_count,
    )

    failure_codes: list[str] = []
    if admin_risk_hard_block_count > 0:
        failure_codes.append(F_POST_10)
    if cmap.unsourced_count > 0:
        failure_codes.append(F_POST_11)

    # v0.2 — F-LOGICIAN-FABRICATED-ORG runtime registration.
    # Both inputs must be supplied to invoke the gate. Skipping when
    # either is None preserves Round-2-floor backward compatibility for
    # existing callers that don't yet thread draft_text / project_context.
    fabricated_org_result: Optional[FabricatedOrgGateResult] = None
    if draft_text is not None and project_context is not None:
        fabricated_org_result = check_fabricated_orgs(
            draft_text=draft_text,
            project_context=project_context,
            rfa_issuer=rfa_issuer,
        )
        if fabricated_org_result.verdict == "FAIL":
            failure_codes.append(F_LOGICIAN_FABRICATED_ORG)

    # v0.2 — F-LOGICIAN-SPINE-DRIFT runtime registration.
    # All three spine-side inputs required alongside draft_text.
    spine_drift_result: Optional[SpineDriftGateResult] = None
    if (
        draft_text is not None
        and spine_path is not None
        and section_id is not None
        and section_dialect is not None
    ):
        spine_drift_result = check_spine_drift(
            section_text=draft_text,
            section_id=section_id,
            section_dialect=section_dialect,
            spine_path=spine_path,
        )
        if spine_drift_result.verdict == "FAIL":
            failure_codes.append(F_LOGICIAN_SPINE_DRIFT)

    # v0.2 — F-LOGICIAN-FACT-DRIFT runtime registration.
    # Both KFR-side inputs required alongside draft_text.
    fact_drift_result: Optional[FactDriftGateResult] = None
    if (
        draft_text is not None
        and kfr_path is not None
        and grant_funding_period is not None
    ):
        fact_drift_result = check_fact_drift(
            draft_text=draft_text,
            kfr_path=kfr_path,
            grant_funding_period=grant_funding_period,
        )
        if fact_drift_result.verdict == "FAIL":
            failure_codes.append(F_LOGICIAN_FACT_DRIFT)

    return PostGateResult(
        success=len(failure_codes) == 0,
        claim_evidence_map=cmap,
        unsourced_count=cmap.unsourced_count,
        hard_block_count=cmap.hard_block_count,
        failure_codes=tuple(failure_codes),
        fabricated_org_result=fabricated_org_result,
        spine_drift_result=spine_drift_result,
        fact_drift_result=fact_drift_result,
    )
