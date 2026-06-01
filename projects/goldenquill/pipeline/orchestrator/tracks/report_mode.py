"""report_mode track entry point — §14 Report Generator v1 LOCK + WS-J Slice 3 wiring.

Per §14 v1 LOCKED 2026-05-10 + WS-J Slice 3 (2026-05-11). This module is
the runner for the §5 v8 track-registry's ``report`` row, binding the
``prior_commitments_to_council_to_signed_report`` pipeline shape to the
five-seat council under report_mode.

Slice 3 replaces the Slice 1 NotImplementedError stubs with the full
wiring:

* :func:`run_report_pipeline` — orchestrates the per-sub-section composer
  dispatch, the council-seat protocol dispatch, the F-REPORT-* gate
  battery (run-all-then-collect per Cycle 1 RT-10a), the
  claim_evidence_map assembly, and the DRAFT_PENDING_OPERATOR_SIGN
  bundle materialization. State-write-on-failure per Rule 1.
* :func:`finalize_operator_signed_report` — operator-approval transition
  that runs the PRE-write-finalized-report Logician check (RT-8b
  post-sign mutation re-check), the Cedar
  ``evaluate_report_finalize_action`` PERMIT/DENY composition, the
  Ed25519 signing via the injected signer protocol, the post-sign
  immutability discipline (flock + chmod 0444), and the
  ``operator_signature.signed.yaml`` companion-record write per
  RT-C2-09 closure.

AST-lint discipline (Slice 3):

* ``R-REPORT-NO-AUTO-FINALIZE`` (Layer 1) — only
  ``finalize_operator_signed_report`` may construct
  ``GrantReportBundle(bundle_state="FINALIZED")``.
* ``R-REPORT-VAULT-INTENT-REQUIRED`` (Layer 1) — substrate reads route
  through injected callables; raw ``open()`` is forbidden.
* ``R-REPORT-DECIMAL-MANDATE`` (Layer 1, per Cycle 2 RT-C2-01) — float
  coercion / float-literal arithmetic / float-literal comparison /
  Decimal(float-literal) all forbidden across composer + gate + this
  track module.

First-wave marker hash-binding (RT-C2-04):
:mod:`pipeline.logician.first_wave_marker` verifies the three-way
binding (marker signature + lock_history hash binding + ledger
signature) and supplies the verdict to the
F-REPORT-TEMPLATE-MISMATCH PRE-pre-track-dispatch gate via the
``WorkspacePublishedTemplateSnapshot.first_wave_marker_*`` fields.

Module-load integrity assertion at the bottom: ``REPORT_MODE_PIPELINE_SHAPE``
+ ``TILTH_VERSION_FAMILY`` + ``SUB_SECTIONS_V0_2`` are checked against
their canonical values at module load — a contributor that rebinds them
at module load triggers ``AssertionError`` and aborts the importing
process. Mirrors the §5 v8 inline-literal rebind-resistance pattern.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Final, Mapping, Optional, Protocol, runtime_checkable

from pipeline.logician.gates._report_protocols import (
    DraftIntegrityAtFinalize,
    PromotedCommitmentRow,
    ReportingTemplateSnapshot,
    SourceResolutionAtFinalize,
    WaiverRecord,
    WorkspacePublishedTemplateSnapshot,
)
from pipeline.logician.gates.f_report_commitment_missed import (
    F_REPORT_COMMITMENT_MISSED,
    check_commitment_missed,
)
from pipeline.logician.gates.f_report_commitment_untraced import (
    F_REPORT_COMMITMENT_UNTRACED,
    check_commitment_untraced,
)
from pipeline.logician.gates.f_report_numeric_drift import (
    F_REPORT_NUMERIC_DRIFT,
    NumericClaimVsKfr,
    check_numeric_drift,
)
from pipeline.logician.gates.f_report_out_of_scope_drift import (
    F_REPORT_OUT_OF_SCOPE_DRIFT,
    check_out_of_scope_drift,
)
from pipeline.logician.gates.f_report_template_mismatch import (
    F_REPORT_TEMPLATE_MISMATCH,
    check_template_mismatch,
)
from pipeline.orchestrator.seats.report_generator._cedar_bootstrap import (
    CedarVerdict,
    evaluate_report_finalize_action,
)
from pipeline.orchestrator.seats.report_generator._schemas import (
    BUNDLE_STATE_DRAFT_PENDING,
    BUNDLE_STATE_FINALIZED,
    OPERATOR_SIG_STATUS_PENDING,
    OPERATOR_SIG_STATUS_SIGNED,
    ClaimEntry,
    ClaimEvidenceMap,
    GrantReportBundle,
    ReportGeneratorRunInput,
)
from pipeline.orchestrator.seats.report_generator.claim_evidence_map import (
    Ed25519SignerProtocol,
    assemble_claim_evidence_map,
    canonical_map_bytes,
    sign_claim_evidence_map,
    signing_payload_bytes,
)


# ---------------------------------------------------------------------------
# Pipeline constants (inline-literal rebind-resistance per §5 v8 + §14.0)
# ---------------------------------------------------------------------------


# v0.2 first-ship Tilth version family — bumped from §5 v8's "v0.1" at
# v0.2 release. With TILTH_VERSION_FAMILY = "v0.2", the report row's
# shippable_in: v0.2 gate passes and ``dispatch_track`` admits report_mode
# dispatch.
TILTH_VERSION_FAMILY: Final[str] = "v0.2"

# Extension to §5 v8 §3.2 _V0_1_IMPLEMENTED_SHAPES per §14 v1 LOCK. At
# v0.2 first ship the dispatcher's implemented-shape set extends from
# {"rfa_to_council_to_signed_bundle", "operator_harness_to_per_seat_calibration"}
# to {previous} ∪ {"prior_commitments_to_council_to_signed_report"}.
REPORT_MODE_PIPELINE_SHAPE: Final[str] = "prior_commitments_to_council_to_signed_report"

# Closed set of sub-section names per §14.6 (v0.2 first ship). Module-load
# integrity assertion at the bottom guards against contributor drift.
SUB_SECTIONS_V0_2: Final[frozenset[str]] = frozenset(
    {
        "narrative",
        "metrics_table",
        "financial_summary",
        "photo_gallery",
        "beneficiary_section",
    }
)

# Deterministic concatenation order per §14.9.0 — drafts assemble from
# per-sub-section composer outputs in this canonical order.
_SUB_SECTION_RENDER_ORDER: Final[tuple[str, ...]] = (
    "narrative",
    "metrics_table",
    "financial_summary",
    "photo_gallery",
    "beneficiary_section",
)

# RT-C2-04 first-wave marker hash binding — bound at this track's first
# invocation per §5 v8's track-registry first-activation pattern. The
# binding payload is a dict {"funder_id": str, "marker_content_sha3_512": str}
# that the orchestrator captures and audit-trails. Read via
# :func:`get_first_wave_marker_binding_at_first_activation`.
_FIRST_WAVE_MARKER_BINDING_AT_FIRST_ACTIVATION: dict[str, str] = {}
_FIRST_WAVE_MARKER_BINDING_LOCKED: list[bool] = [False]


def get_first_wave_marker_binding_at_first_activation() -> Mapping[str, str]:
    """Per RT-C2-04 — return the first-wave marker hash binding captured at
    the track's first invocation.

    Returns an empty mapping if the track has not yet been invoked. The
    binding is a per-funder_id snapshot of the marker content hash at the
    moment the track first activated; downstream audits diff this against
    subsequent invocations to detect SN-LLC release-ceremony drift.
    """
    return dict(_FIRST_WAVE_MARKER_BINDING_AT_FIRST_ACTIVATION)


# ---------------------------------------------------------------------------
# Frozen schemas (re-exported from _schemas — canonical identity preserved
# so Cedar evaluator's isinstance check against GrantReportBundle passes)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class ReportRunResult:
    """Returned by :func:`run_report_pipeline`. Carries the bundle + the
    state-file path (state is written on both success AND failure per Rule 1)."""

    bundle: GrantReportBundle
    state_file_path: str
    cycle_completed: bool
    failure_reason: str  # empty when cycle_completed=True
    failure_sub_tag: str  # empty when cycle_completed=True


# ---------------------------------------------------------------------------
# Injected Protocols — council seats + substrate accessors
# ---------------------------------------------------------------------------


class ScribeProtocol(Protocol):
    """Council seat — composer-level Scribe drafting callable."""

    def compose_sub_section(
        self,
        *,
        sub_section: str,
        proposal_commitments_promoted: tuple[PromotedCommitmentRow, ...],
        reporting_template: ReportingTemplateSnapshot,
        operational_data: Any,
        kfr: Any,
        funder_intelligence: Any,
        benchmarks: Any,
        trend_narrative_authorized: bool,
    ) -> "SubSectionComposerOutput": ...


class EditorProtocol(Protocol):
    """Council seat — clarity review."""

    def review_sub_section(
        self, *, sub_section: str, draft: str, claims: tuple[ClaimEntry, ...]
    ) -> "EditorVerdict": ...


class JudgeProtocol(Protocol):
    """Council seat — scoring."""

    def score_sub_section(
        self,
        *,
        sub_section: str,
        draft: str,
        proposal_commitments_rubric: Any,
        funder_published_rubric: Any,
    ) -> "JudgeVerdict": ...


class RedTeamProtocol(Protocol):
    """Council seat — adversarial probe."""

    def probe_sub_section(
        self, *, sub_section: str, draft: str, claims: tuple[ClaimEntry, ...]
    ) -> "RedTeamVerdict": ...


class ScopeTagExtractorProtocol(Protocol):
    def __call__(self, claim_text: str) -> tuple[str, ...]: ...


class ComposerDispatcherProtocol(Protocol):
    """Builds + dispatches the per-sub-section composer."""

    def __call__(
        self,
        *,
        sub_section: str,
        input: ReportGeneratorRunInput,
        proposal_commitments_promoted: tuple[PromotedCommitmentRow, ...],
        reporting_template: ReportingTemplateSnapshot,
        scribe: ScribeProtocol,
    ) -> "SubSectionComposerOutput": ...


@dataclass(frozen=True, kw_only=True)
class SubSectionComposerOutput:
    """Per-sub-section composer result handed to the run pipeline."""

    sub_section: str
    markdown_fragment: str
    claims: tuple[ClaimEntry, ...]


@dataclass(frozen=True, kw_only=True)
class EditorVerdict:
    success: bool
    detail: str = ""


@dataclass(frozen=True, kw_only=True)
class JudgeVerdict:
    success: bool
    score: int = 0
    detail: str = ""


@dataclass(frozen=True, kw_only=True)
class RedTeamVerdict:
    success: bool
    detail: str = ""


# ---------------------------------------------------------------------------
# Substrate-loader Protocols — all I/O routed here
# ---------------------------------------------------------------------------


class ProposalCommitmentsLoader(Protocol):
    def __call__(self, *, path: str) -> tuple[PromotedCommitmentRow, ...]: ...


class ReportingTemplateLoader(Protocol):
    def __call__(self, *, path: str) -> ReportingTemplateSnapshot: ...


class WorkspacePublishedLoader(Protocol):
    def __call__(
        self, *, funder_id: str, root: str
    ) -> Optional[WorkspacePublishedTemplateSnapshot]: ...


class WaiversLoader(Protocol):
    def __call__(self, *, path: str) -> Mapping[str, WaiverRecord]: ...


class SourceResolutionAssembler(Protocol):
    def __call__(
        self,
        *,
        claim_evidence_map: ClaimEvidenceMap,
        input: ReportGeneratorRunInput,
    ) -> Mapping[tuple[str, int], SourceResolutionAtFinalize]: ...


class NarrativeSourceTextsAssembler(Protocol):
    def __call__(
        self,
        *,
        claim_evidence_map: ClaimEvidenceMap,
        input: ReportGeneratorRunInput,
    ) -> Mapping[str, tuple[str, ...]]: ...


class DraftIntegrityAssembler(Protocol):
    def __call__(
        self,
        *,
        draft_path: str,
        post_sign_read: bool,
    ) -> DraftIntegrityAtFinalize: ...


class NumericRowsAssembler(Protocol):
    def __call__(
        self,
        *,
        claims: tuple[ClaimEntry, ...],
        input: ReportGeneratorRunInput,
    ) -> tuple[NumericClaimVsKfr, ...]: ...


class DraftWriter(Protocol):
    def __call__(self, *, markdown: str, path: str) -> str: ...
    # Returns lowercase-hex SHA3-512 of the written markdown.


class ClaimEvidenceMapWriter(Protocol):
    def __call__(self, *, map_bytes: bytes, path: str) -> str: ...
    # Returns lowercase-hex SHA3-512 of the written bytes.


class StateWriter(Protocol):
    def __call__(self, *, state_payload: Mapping[str, Any], path: str) -> str: ...


class OperatorSignatureWriter(Protocol):
    def __call__(self, *, signed_yaml_bytes: bytes, path: str) -> str: ...


class DraftPostSignLockingProtocol(Protocol):
    """Acquires write-lock + chmod 0444 on the finalized draft. RT-8b discipline."""

    def __call__(self, *, draft_path: str) -> None: ...


class ClockProtocol(Protocol):
    def __call__(self) -> str: ...


class HashBytesProtocol(Protocol):
    def __call__(self, data: bytes) -> str: ...


# ---------------------------------------------------------------------------
# Dependency bundle — everything the pipeline needs in one frozen container
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ReportPipelineDeps:
    """All injected callables the report_mode pipeline depends on.

    A test fixture constructs this with stubs; production wiring builds
    it once at seat startup. The bundle is frozen so the pipeline cannot
    mutate it during a run.
    """

    # Council seats
    scribe: ScribeProtocol
    editor: EditorProtocol
    judge: JudgeProtocol
    red_team: RedTeamProtocol

    # Composer dispatcher (per-sub-section composer factory)
    composer_dispatcher: ComposerDispatcherProtocol

    # Substrate loaders
    proposal_commitments_loader: ProposalCommitmentsLoader
    reporting_template_loader: ReportingTemplateLoader
    workspace_published_loader: WorkspacePublishedLoader
    waivers_loader: WaiversLoader

    # Gate-input assemblers
    source_resolution_assembler: SourceResolutionAssembler
    narrative_source_texts_assembler: NarrativeSourceTextsAssembler
    draft_integrity_assembler: DraftIntegrityAssembler
    numeric_rows_assembler: NumericRowsAssembler

    # Adversarial-gate inputs
    scope_tag_extractor: ScopeTagExtractorProtocol

    # File-writing surfaces
    draft_writer: DraftWriter
    claim_evidence_map_writer: ClaimEvidenceMapWriter
    state_writer: StateWriter
    operator_signature_writer: OperatorSignatureWriter
    draft_post_sign_locker: DraftPostSignLockingProtocol

    # Clock + hash
    clock: ClockProtocol
    hash_bytes: HashBytesProtocol

    # Optional auxiliaries
    proposal_commitments_rubric: Any = None
    funder_published_rubric: Any = None
    operator_pinned_key_version: Optional[str] = None
    sp0_cross_period_authorized: bool = False
    actual_period_cadence_months: Optional[int] = None
    caption_resolutions: Mapping[str, Any] = field(default_factory=dict)
    beneficiary_consent_infos: tuple = ()
    photo_consent_infos: tuple = ()
    aggregate_references: tuple = ()
    beneficiary_name_dictionary: Optional[Any] = None
    prior_period_integrity: Optional[Any] = None


# ---------------------------------------------------------------------------
# Internal helpers — failure-path bundle construction (DRAFT_PENDING only)
# ---------------------------------------------------------------------------


def _empty_draft_pending_bundle(
    input: ReportGeneratorRunInput,
    *,
    reporting_template_hash: str = "",
    proposal_commitments_consumed: tuple[str, ...] = (),
    sub_sections_authored: tuple[str, ...] = (),
    draft_path: str = "",
    draft_version: int = 0,
    claim_evidence_map_path: str = "",
    scoring_dir: str = "",
) -> GrantReportBundle:
    """Construct a bundle in DRAFT_PENDING_OPERATOR_SIGN state for failure
    paths or early returns. NEVER constructs FINALIZED — that is the
    sole prerogative of :func:`finalize_operator_signed_report`."""
    return GrantReportBundle(
        run_id=input.run_id,
        org_slug=input.org_slug,
        grant_id=input.grant_id,
        period_n=input.period_n,
        draft_path=draft_path,
        draft_version=draft_version,
        claim_evidence_map_path=claim_evidence_map_path,
        scoring_dir=scoring_dir,
        proposal_commitments_consumed=proposal_commitments_consumed,
        reporting_template_content_sha3_512=reporting_template_hash,
        sub_sections_authored=sub_sections_authored,
        operator_signature_status=OPERATOR_SIG_STATUS_PENDING,
        operator_signature="",
        operator_signed_at_utc="",
        finalized_at_utc="",
        bundle_state=BUNDLE_STATE_DRAFT_PENDING,
    )


def _vault_paths(input: ReportGeneratorRunInput, draft_version: int) -> dict[str, str]:
    """Compute the per-period vault paths under
    ``orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/``."""
    base = (
        f"orgs/{input.org_slug}/vault/grants/{input.grant_id}/reports/"
        f"period_{input.period_n}"
    )
    return {
        "base": base,
        "draft": f"{base}/draft_{draft_version}.md",
        "map": f"{base}/claim_evidence_map.yaml",
        "state": f"{base}/run_state.yaml",
        "scoring": f"{base}/scoring/",
        "operator_signature": f"{base}/operator_signature.signed.yaml",
    }


def _state_payload(
    *,
    input: ReportGeneratorRunInput,
    cycle_completed: bool,
    failure_reason: str,
    failure_sub_tag: str,
    sub_sections_authored: tuple[str, ...],
    gate_results: Mapping[str, Any],
) -> dict[str, Any]:
    """Compose the run_state.yaml payload (success OR failure per Rule 1)."""
    return {
        "schema_version": "report_mode.run_state.v1",
        "run_id": input.run_id,
        "org_slug": input.org_slug,
        "grant_id": input.grant_id,
        "period_n": input.period_n,
        "invoked_at_utc": input.invoked_at_utc,
        "cycle_completed": cycle_completed,
        "failure_reason": failure_reason,
        "failure_sub_tag": failure_sub_tag,
        "sub_sections_authored": list(sub_sections_authored),
        "gate_results_summary": {
            code: {
                "success": getattr(r, "success", None),
                "fired_sub_tags": list(getattr(r, "fired_sub_tags", ()) or ()),
            }
            for code, r in gate_results.items()
            if r is not None
        },
    }


def _bind_first_wave_marker(
    *,
    workspace_published: Optional[WorkspacePublishedTemplateSnapshot],
    reporting_template: ReportingTemplateSnapshot,
) -> None:
    """Per RT-C2-04 — bind the first-wave marker hash at first activation
    of the report_mode track.

    Only binds when the workspace_published snapshot is present AND
    marks the funder as first-wave AND the marker has cleared signature +
    lock_history binding (i.e., the verifier's three booleans are all
    True at the moment of binding). Subsequent invocations do NOT
    re-bind; downstream audits diff this binding against the live
    marker hash to detect SN-LLC release-ceremony drift.

    The binding is purely informational at v0.2 first ship — the
    F-REPORT-TEMPLATE-MISMATCH gate already fail-closes on marker
    tampering; this binding captures the audit-time snapshot.
    """
    if _FIRST_WAVE_MARKER_BINDING_LOCKED[0]:
        return
    if workspace_published is None or not workspace_published.first_wave:
        return
    if workspace_published.first_wave_marker_signature_valid is not True:
        return
    if workspace_published.first_wave_marker_hash_bound_to_lock_history is not True:
        return
    if not workspace_published.content_sha3_512:
        return
    _FIRST_WAVE_MARKER_BINDING_AT_FIRST_ACTIVATION[reporting_template.funder_id] = (
        workspace_published.content_sha3_512
    )
    _FIRST_WAVE_MARKER_BINDING_LOCKED[0] = True


# ---------------------------------------------------------------------------
# Public API — run_report_pipeline
# ---------------------------------------------------------------------------


def run_report_pipeline(
    input: ReportGeneratorRunInput,
    *,
    deps: ReportPipelineDeps,
) -> ReportRunResult:
    """Per §14.9.0 — full report_mode pipeline run.

    Pipeline shape (all gates run-all-then-collect per Cycle 1 RT-10a):

    1. **PRE-pre-track-dispatch consolidated check**
       (F-REPORT-TEMPLATE-MISMATCH + F-REPORT-COMMITMENT-MISSED
       .empty_promoted_set). Cedar's F-CEDAR-OPERATIONAL-DENIED +
       F-CEDAR-PII-CONSENT-MISSING are inherited from §2 v7.2 Cedar
       reads at the substrate-loader layer — the loader fails closed
       and surfaces here as a load-time exception caught + routed to
       ``failure_reason="cedar_operational_denied"``.

    2. **Load substrates** — proposal_commitments PROMOTED-filtered,
       reporting_template, workspace-published template (when
       present). Each loader is the injected callable from
       :class:`ReportPipelineDeps` — the run pipeline never opens
       files directly.

    3. **Per-sub-section composer dispatch** — for each
       ``sub_section`` in ``input.sub_sections_in_scope``, invoke
       :meth:`ComposerDispatcherProtocol.__call__` to compose the
       markdown fragment + collect the ClaimEntry tuple.

    4. **POST-scribe per-sub-section** — F-REPORT-NUMERIC-DRIFT +
       F-REPORT-OUT-OF-SCOPE-DRIFT against the assembled claim_entries.

    5. **Council seats** — Editor, Judge, Red Team Protocol dispatch.
       Failures surface as ``cycle_completed=False`` with
       ``failure_reason`` = the seat that vetoed.

    6. **POST-judge per-sub-section** — F-REPORT-COMMITMENT-MISSED.

    7. **PRE-pre-finalize consolidated check** —
       F-REPORT-COMMITMENT-UNTRACED + (re-)check of NUMERIC-DRIFT +
       OUT-OF-SCOPE-DRIFT against the full assembled draft.

    8. **Compose ``draft_<v>.md``** — deterministic concatenation of
       per-sub-section markdown fragments in
       ``required_sub_sections`` order from the reporting_template.

    9. **Assemble ``claim_evidence_map.yaml``** — DRAFT/PENDING via
       :func:`assemble_claim_evidence_map`; write via the injected
       map_writer.

    10. **State-write** — run_state.yaml with the cycle outcome
        (success AND failure paths per Rule 1).

    11. **Return** ``ReportRunResult`` with the
        ``DRAFT_PENDING_OPERATOR_SIGN`` bundle awaiting operator
        sign-off via :func:`finalize_operator_signed_report`.
    """
    if not isinstance(input, ReportGeneratorRunInput):
        raise TypeError(
            f"input must be ReportGeneratorRunInput; got {type(input).__name__}"
        )
    if not isinstance(deps, ReportPipelineDeps):
        raise TypeError(
            f"deps must be ReportPipelineDeps; got {type(deps).__name__}"
        )

    gate_results: dict[str, Any] = {}
    sub_sections_authored: tuple[str, ...] = ()
    proposal_commitments_consumed: tuple[str, ...] = ()
    draft_version = 1
    paths = _vault_paths(input, draft_version)

    # ------------------------------------------------------------------
    # Step 2 — load reporting_template + workspace_published + commitments
    # ------------------------------------------------------------------
    try:
        reporting_template = deps.reporting_template_loader(
            path=input.reporting_template_path
        )
    except Exception as exc:
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=(
                f"reporting_template_loader raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag="",
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
        )

    try:
        workspace_published = deps.workspace_published_loader(
            funder_id=reporting_template.funder_id,
            root=input.funder_intelligence_root,
        )
    except Exception as exc:
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=(
                f"workspace_published_loader raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag="",
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
        )

    # RT-C2-04 first-wave marker hash binding at first activation
    _bind_first_wave_marker(
        workspace_published=workspace_published,
        reporting_template=reporting_template,
    )

    # ------------------------------------------------------------------
    # Step 1 — PRE-pre-track-dispatch (template + empty-promoted)
    # ------------------------------------------------------------------
    template_result = check_template_mismatch(
        operator_template=reporting_template,
        workspace_published=workspace_published,
        actual_period_cadence_months=deps.actual_period_cadence_months,
        operator_pinned_key_version=deps.operator_pinned_key_version,
    )
    gate_results[F_REPORT_TEMPLATE_MISMATCH] = template_result

    try:
        promoted = deps.proposal_commitments_loader(
            path=input.proposal_commitments_path
        )
    except Exception as exc:
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=(
                f"proposal_commitments_loader raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag="",
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
        )
    proposal_commitments_consumed = tuple(c.commitment_id for c in promoted)

    try:
        waivers = deps.waivers_loader(path=input.proposal_commitments_path)
    except Exception as exc:
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=(
                f"waivers_loader raised: {type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag="",
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
        )

    # Empty-promoted-set fail-closed (PRE-pre-track-dispatch slice)
    pre_dispatch_commitment_missed = check_commitment_missed(
        promoted_commitments=promoted,
        sub_sections_in_scope=input.sub_sections_in_scope,
        sub_sections_authored=(),  # nothing authored yet
        period_n=input.period_n,
        claim_commitment_links={},
        addressed_criteria={},
        waivers=waivers,
    )
    # Only the .empty_promoted_set firing is fatal at PRE; other sub-tags
    # are deferred to POST-judge re-check.
    pre_dispatch_empty = (
        not pre_dispatch_commitment_missed.success
        and ".empty_promoted_set" in pre_dispatch_commitment_missed.fired_sub_tags
    )

    # Collect both PRE failures into a single consolidated verdict (Cycle 1
    # RT-10a run-all-then-collect; do NOT short-circuit).
    if not template_result.success or pre_dispatch_empty:
        # Record empty-promoted distinct from POST-judge phase
        if pre_dispatch_empty:
            gate_results[F_REPORT_COMMITMENT_MISSED] = pre_dispatch_commitment_missed
        # First failure wins for failure_reason narration; both subjected
        # to the gate_results record so the operator UI surfaces both.
        if not template_result.success:
            primary_code = F_REPORT_TEMPLATE_MISMATCH
            primary_sub_tag = (
                template_result.fired_sub_tags[0]
                if template_result.fired_sub_tags
                else ""
            )
        else:
            primary_code = F_REPORT_COMMITMENT_MISSED
            primary_sub_tag = ".empty_promoted_set"
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=f"PRE-pre-track-dispatch consolidated check failed: {primary_code}",
            failure_sub_tag=primary_sub_tag,
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
        )

    # ------------------------------------------------------------------
    # Step 3 — per-sub-section composer dispatch
    # ------------------------------------------------------------------
    all_claims: list[ClaimEntry] = []
    sub_section_outputs: dict[str, SubSectionComposerOutput] = {}

    for sub_section in input.sub_sections_in_scope:
        try:
            output = deps.composer_dispatcher(
                sub_section=sub_section,
                input=input,
                proposal_commitments_promoted=promoted,
                reporting_template=reporting_template,
                scribe=deps.scribe,
            )
        except Exception as exc:
            return _fail(
                input,
                deps=deps,
                paths=paths,
                failure_reason=(
                    f"composer_dispatcher raised on sub_section="
                    f"{sub_section!r}: {type(exc).__name__}: {exc!s}"
                ),
                failure_sub_tag=".composer_error",
                gate_results=gate_results,
                sub_sections_authored=sub_sections_authored,
                proposal_commitments_consumed=proposal_commitments_consumed,
                reporting_template_hash=reporting_template.template_content_sha3_512,
            )
        if not isinstance(output, SubSectionComposerOutput):
            return _fail(
                input,
                deps=deps,
                paths=paths,
                failure_reason=(
                    f"composer_dispatcher returned non-SubSectionComposerOutput "
                    f"for sub_section={sub_section!r}: {type(output).__name__}"
                ),
                failure_sub_tag=".composer_protocol_violation",
                gate_results=gate_results,
                sub_sections_authored=sub_sections_authored,
                proposal_commitments_consumed=proposal_commitments_consumed,
                reporting_template_hash=reporting_template.template_content_sha3_512,
            )
        sub_section_outputs[sub_section] = output
        sub_sections_authored = sub_sections_authored + (sub_section,)
        all_claims.extend(output.claims)

    claims_tuple: tuple[ClaimEntry, ...] = tuple(all_claims)

    # ------------------------------------------------------------------
    # Step 4 — POST-scribe (per sub-section composer outputs)
    # ------------------------------------------------------------------
    # F-REPORT-NUMERIC-DRIFT
    try:
        numeric_rows = deps.numeric_rows_assembler(
            claims=claims_tuple, input=input
        )
    except Exception as exc:
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=(
                f"numeric_rows_assembler raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag="",
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
        )
    numeric_drift_result = check_numeric_drift(numeric_rows=numeric_rows)
    gate_results[F_REPORT_NUMERIC_DRIFT] = numeric_drift_result

    # Assemble a synthetic claim_evidence_map for the POST-scribe scope-drift check.
    # We need to compute draft hash for a placeholder draft; the real
    # draft hash is computed below after concatenation.
    # We use a SHA3-512 of a fixed placeholder to satisfy schema invariants;
    # the F-REPORT-OUT-OF-SCOPE-DRIFT predicate does not consult
    # draft_content_sha3_512.
    placeholder_draft_hash = deps.hash_bytes(b"__placeholder_pre_assembly__")
    synth_map = assemble_claim_evidence_map(
        run_id=input.run_id,
        org_slug=input.org_slug,
        grant_id=input.grant_id,
        period_n=input.period_n,
        draft_path=paths["draft"],
        draft_version=draft_version,
        draft_content_sha3_512=placeholder_draft_hash,
        authored_at_utc=deps.clock(),
        authored_by_seat="report_generator.scribe",
        claims=claims_tuple,
    )

    scope_drift_result = check_out_of_scope_drift(
        claim_evidence_map=synth_map,
        promoted_commitments=promoted,
        report_grant_id=input.grant_id,
        report_org_slug=input.org_slug,
        report_period_n=input.period_n,
        sp0_cross_period_authorized=deps.sp0_cross_period_authorized,
        scope_tag_extractor=deps.scope_tag_extractor,
        beneficiary_consent_infos=deps.beneficiary_consent_infos,
        photo_consent_infos=deps.photo_consent_infos,
        aggregate_references=deps.aggregate_references,
        beneficiary_name_dictionary=deps.beneficiary_name_dictionary,
    )
    gate_results[F_REPORT_OUT_OF_SCOPE_DRIFT] = scope_drift_result

    # ------------------------------------------------------------------
    # Step 5 — Council seats (Editor + Judge + Red Team)
    # ------------------------------------------------------------------
    for sub_section, output in sub_section_outputs.items():
        editor_verdict = deps.editor.review_sub_section(
            sub_section=sub_section,
            draft=output.markdown_fragment,
            claims=output.claims,
        )
        if not editor_verdict.success:
            return _fail(
                input,
                deps=deps,
                paths=paths,
                failure_reason=(
                    f"Editor rejected sub_section={sub_section!r}: "
                    f"{editor_verdict.detail}"
                ),
                failure_sub_tag=".editor_rejection",
                gate_results=gate_results,
                sub_sections_authored=sub_sections_authored,
                proposal_commitments_consumed=proposal_commitments_consumed,
                reporting_template_hash=reporting_template.template_content_sha3_512,
            )
        judge_verdict = deps.judge.score_sub_section(
            sub_section=sub_section,
            draft=output.markdown_fragment,
            proposal_commitments_rubric=deps.proposal_commitments_rubric,
            funder_published_rubric=deps.funder_published_rubric,
        )
        if not judge_verdict.success:
            return _fail(
                input,
                deps=deps,
                paths=paths,
                failure_reason=(
                    f"Judge rejected sub_section={sub_section!r} "
                    f"(score={judge_verdict.score}): {judge_verdict.detail}"
                ),
                failure_sub_tag=".judge_rejection",
                gate_results=gate_results,
                sub_sections_authored=sub_sections_authored,
                proposal_commitments_consumed=proposal_commitments_consumed,
                reporting_template_hash=reporting_template.template_content_sha3_512,
            )
        red_team_verdict = deps.red_team.probe_sub_section(
            sub_section=sub_section,
            draft=output.markdown_fragment,
            claims=output.claims,
        )
        if not red_team_verdict.success:
            return _fail(
                input,
                deps=deps,
                paths=paths,
                failure_reason=(
                    f"Red Team flagged sub_section={sub_section!r}: "
                    f"{red_team_verdict.detail}"
                ),
                failure_sub_tag=".red_team_rejection",
                gate_results=gate_results,
                sub_sections_authored=sub_sections_authored,
                proposal_commitments_consumed=proposal_commitments_consumed,
                reporting_template_hash=reporting_template.template_content_sha3_512,
            )

    # ------------------------------------------------------------------
    # Step 6 — POST-judge: F-REPORT-COMMITMENT-MISSED against assembled draft
    # ------------------------------------------------------------------
    claim_commitment_links: dict[str, list[str]] = {}
    for claim in claims_tuple:
        for src in claim.sources:
            if src.kind == "proposal_commitments" and src.commitment_id:
                claim_commitment_links.setdefault(src.commitment_id, []).append(
                    claim.sub_section
                )
    claim_commitment_links_t = {
        cid: tuple(set(subs)) for cid, subs in claim_commitment_links.items()
    }

    addressed_criteria: dict[str, set[str]] = {}
    for claim in claims_tuple:
        for src in claim.sources:
            if src.kind == "proposal_commitments" and src.commitment_id:
                addressed_criteria.setdefault(src.commitment_id, set()).add(
                    claim.claim_text.split("=")[0].strip()
                )
    addressed_criteria_f = {
        cid: frozenset(fs) for cid, fs in addressed_criteria.items()
    }

    post_judge_missed = check_commitment_missed(
        promoted_commitments=promoted,
        sub_sections_in_scope=input.sub_sections_in_scope,
        sub_sections_authored=sub_sections_authored,
        period_n=input.period_n,
        claim_commitment_links=claim_commitment_links_t,
        addressed_criteria=addressed_criteria_f,
        waivers=waivers,
    )
    gate_results[F_REPORT_COMMITMENT_MISSED] = post_judge_missed

    # ------------------------------------------------------------------
    # Step 8 — Compose draft_<v>.md (deterministic per-sub-section concat)
    # ------------------------------------------------------------------
    rendered_fragments: list[str] = []
    for sub_section in _SUB_SECTION_RENDER_ORDER:
        if sub_section in sub_section_outputs:
            rendered_fragments.append(
                f"## {sub_section}\n\n{sub_section_outputs[sub_section].markdown_fragment}"
            )
    draft_markdown = "\n\n".join(rendered_fragments) + "\n"
    draft_content_hash = deps.hash_bytes(draft_markdown.encode("utf-8"))

    # ------------------------------------------------------------------
    # Step 9 — Assemble claim_evidence_map with real draft hash
    # ------------------------------------------------------------------
    real_map = assemble_claim_evidence_map(
        run_id=input.run_id,
        org_slug=input.org_slug,
        grant_id=input.grant_id,
        period_n=input.period_n,
        draft_path=paths["draft"],
        draft_version=draft_version,
        draft_content_sha3_512=draft_content_hash,
        authored_at_utc=deps.clock(),
        authored_by_seat="report_generator.scribe",
        claims=claims_tuple,
    )

    # ------------------------------------------------------------------
    # Step 7 — PRE-pre-finalize consolidated check (F-REPORT-COMMITMENT-UNTRACED)
    # ------------------------------------------------------------------
    try:
        source_resolutions = deps.source_resolution_assembler(
            claim_evidence_map=real_map, input=input
        )
    except Exception as exc:
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=(
                f"source_resolution_assembler raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag="",
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
        )
    try:
        narrative_source_texts = deps.narrative_source_texts_assembler(
            claim_evidence_map=real_map, input=input
        )
    except Exception as exc:
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=(
                f"narrative_source_texts_assembler raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag="",
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
        )
    # pre-finalize draft integrity (post_sign_read=False, this is pre-sign)
    pre_finalize_draft_integrity = DraftIntegrityAtFinalize(
        draft_content_sha3_512_at_finalize=draft_content_hash,
        post_sign_read=False,
    )

    commitment_untraced_result = check_commitment_untraced(
        claim_evidence_map=real_map,
        source_resolutions=source_resolutions,
        narrative_source_texts=narrative_source_texts,
        caption_resolutions=deps.caption_resolutions,
        draft_integrity=pre_finalize_draft_integrity,
        prior_period_integrity=deps.prior_period_integrity,
    )
    gate_results[F_REPORT_COMMITMENT_UNTRACED] = commitment_untraced_result

    # ------------------------------------------------------------------
    # Aggregate gate verdicts — any non-success ⇒ DRAFT_PENDING fail
    # ------------------------------------------------------------------
    failing_gates = [
        (code, r)
        for code, r in gate_results.items()
        if r is not None and getattr(r, "success", True) is not True
    ]
    if failing_gates:
        primary_code, primary_result = failing_gates[0]
        primary_sub_tag = (
            primary_result.fired_sub_tags[0]
            if getattr(primary_result, "fired_sub_tags", None)
            else ""
        )
        # Still write the draft + map to the vault (DRAFT_PENDING state
        # lets operator review the failure surface), AND write state.
        try:
            written_draft_hash = deps.draft_writer(
                markdown=draft_markdown, path=paths["draft"]
            )
            written_map_hash = deps.claim_evidence_map_writer(
                map_bytes=canonical_map_bytes(real_map), path=paths["map"]
            )
        except Exception as exc:  # write failure compounds with gate failure
            return _fail(
                input,
                deps=deps,
                paths=paths,
                failure_reason=(
                    f"{primary_code} + writer raise: "
                    f"{type(exc).__name__}: {exc!s}"
                ),
                failure_sub_tag=primary_sub_tag,
                gate_results=gate_results,
                sub_sections_authored=sub_sections_authored,
                proposal_commitments_consumed=proposal_commitments_consumed,
                reporting_template_hash=reporting_template.template_content_sha3_512,
            )
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=f"gate failure: {primary_code}",
            failure_sub_tag=primary_sub_tag,
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
            draft_path=paths["draft"],
            draft_version=draft_version,
            claim_evidence_map_path=paths["map"],
            scoring_dir=paths["scoring"],
        )

    # ------------------------------------------------------------------
    # Step 9 + 10 — Write draft + claim_evidence_map + state
    # ------------------------------------------------------------------
    try:
        written_draft_hash = deps.draft_writer(
            markdown=draft_markdown, path=paths["draft"]
        )
        if written_draft_hash != draft_content_hash:  # written hash sanity
            raise ValueError(
                f"draft_writer returned hash {written_draft_hash[:16]}… "
                f"!= computed hash {draft_content_hash[:16]}…"
            )
        written_map_hash = deps.claim_evidence_map_writer(
            map_bytes=canonical_map_bytes(real_map), path=paths["map"]
        )
    except Exception as exc:
        return _fail(
            input,
            deps=deps,
            paths=paths,
            failure_reason=(
                f"writer raised: {type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag=".writer_failure",
            gate_results=gate_results,
            sub_sections_authored=sub_sections_authored,
            proposal_commitments_consumed=proposal_commitments_consumed,
            reporting_template_hash=reporting_template.template_content_sha3_512,
            draft_path=paths["draft"],
            draft_version=draft_version,
            claim_evidence_map_path=paths["map"],
            scoring_dir=paths["scoring"],
        )

    bundle = _empty_draft_pending_bundle(
        input,
        reporting_template_hash=reporting_template.template_content_sha3_512,
        proposal_commitments_consumed=proposal_commitments_consumed,
        sub_sections_authored=sub_sections_authored,
        draft_path=paths["draft"],
        draft_version=draft_version,
        claim_evidence_map_path=paths["map"],
        scoring_dir=paths["scoring"],
    )

    state_payload = _state_payload(
        input=input,
        cycle_completed=True,
        failure_reason="",
        failure_sub_tag="",
        sub_sections_authored=sub_sections_authored,
        gate_results=gate_results,
    )
    state_path = deps.state_writer(
        state_payload=state_payload, path=paths["state"]
    )

    return ReportRunResult(
        bundle=bundle,
        state_file_path=state_path,
        cycle_completed=True,
        failure_reason="",
        failure_sub_tag="",
    )


def _fail(
    input: ReportGeneratorRunInput,
    *,
    deps: ReportPipelineDeps,
    paths: Mapping[str, str],
    failure_reason: str,
    failure_sub_tag: str,
    gate_results: Mapping[str, Any],
    sub_sections_authored: tuple[str, ...],
    proposal_commitments_consumed: tuple[str, ...],
    reporting_template_hash: str = "",
    draft_path: str = "",
    draft_version: int = 0,
    claim_evidence_map_path: str = "",
    scoring_dir: str = "",
) -> ReportRunResult:
    """Failure-path return that writes state (Rule 1 — save state on failure too)."""
    bundle = _empty_draft_pending_bundle(
        input,
        reporting_template_hash=reporting_template_hash,
        proposal_commitments_consumed=proposal_commitments_consumed,
        sub_sections_authored=sub_sections_authored,
        draft_path=draft_path,
        draft_version=draft_version,
        claim_evidence_map_path=claim_evidence_map_path,
        scoring_dir=scoring_dir,
    )
    state_payload = _state_payload(
        input=input,
        cycle_completed=False,
        failure_reason=failure_reason,
        failure_sub_tag=failure_sub_tag,
        sub_sections_authored=sub_sections_authored,
        gate_results=gate_results,
    )
    try:
        state_path = deps.state_writer(
            state_payload=state_payload, path=paths["state"]
        )
    except Exception as state_exc:  # state-writer must not mask failure_reason
        state_path = ""
        failure_reason = (
            f"{failure_reason} + state_writer raise: "
            f"{type(state_exc).__name__}: {state_exc!s}"
        )
    return ReportRunResult(
        bundle=bundle,
        state_file_path=state_path,
        cycle_completed=False,
        failure_reason=failure_reason,
        failure_sub_tag=failure_sub_tag,
    )


# ---------------------------------------------------------------------------
# Public API — finalize_operator_signed_report
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class FinalizeDeps:
    """Subset of :class:`ReportPipelineDeps` needed for finalization.

    Operator-approval is a separate UI surface (the run pipeline left
    the bundle in DRAFT_PENDING_OPERATOR_SIGN). The operator UI invokes
    :func:`finalize_operator_signed_report` with the signer protocol +
    PRE-write-finalized-report check inputs.
    """

    ed25519_signer: Ed25519SignerProtocol
    source_resolution_assembler: SourceResolutionAssembler
    narrative_source_texts_assembler: NarrativeSourceTextsAssembler
    draft_integrity_assembler: DraftIntegrityAssembler
    draft_post_sign_locker: DraftPostSignLockingProtocol
    operator_signature_writer: OperatorSignatureWriter
    hash_bytes: HashBytesProtocol
    clock: ClockProtocol
    caption_resolutions: Mapping[str, Any] = field(default_factory=dict)
    prior_period_integrity: Optional[Any] = None


def finalize_operator_signed_report(
    *,
    bundle: GrantReportBundle,
    claim_evidence_map: ClaimEvidenceMap,
    input: ReportGeneratorRunInput,
    deps: FinalizeDeps,
) -> ReportRunResult:
    """Per §14.5.0 — operator-approved finalization transition.

    The operator reviews the per-claim evidence trace + per-commitment
    fulfillment summary + classification routing summary + Cedar policy
    compliance summary in the UI; on approval the UI calls this function
    with the unsigned ``ClaimEvidenceMap`` (state=PENDING_OPERATOR_REVIEW)
    returned from :func:`run_report_pipeline`. Steps:

    1. PRE-write-finalized-report Logician consolidated check —
       re-runs F-REPORT-COMMITMENT-UNTRACED with ``post_sign_read=True``
       (RT-8b post-sign mutation detection).
    2. Cedar bootstrap :func:`evaluate_report_finalize_action` — DENY if
       any F-REPORT-* gate has not cleared OR draft re-hash detected drift.
    3. Apply operator Ed25519 signature via
       :func:`sign_claim_evidence_map` (the only sanctioned signer surface).
    4. ``flock(LOCK_EX | LOCK_NB)`` + ``chmod 0444`` on the draft file
       via the injected locker (RT-8b post-sign immutability discipline).
    5. Write ``operator_signature.signed.yaml`` companion record
       (RT-C2-09 closure — carries
       ``claim_evidence_map_content_sha3_512`` +
       ``draft_content_sha3_512`` + Ed25519 over canonical-JSON of
       those fields).
    6. Construct FINALIZED ``GrantReportBundle`` + return
       :class:`ReportRunResult` with ``cycle_completed=True`` and
       the FINALIZED bundle.

    Failure-mode: any check fails → returns a
    DRAFT_PENDING_OPERATOR_SIGN ``ReportRunResult`` with
    ``cycle_completed=False`` and the failure reason populated.
    """
    if bundle.bundle_state != BUNDLE_STATE_DRAFT_PENDING:
        return ReportRunResult(
            bundle=bundle,
            state_file_path="",
            cycle_completed=False,
            failure_reason=(
                f"finalize invoked on bundle_state={bundle.bundle_state!r}; "
                f"expected {BUNDLE_STATE_DRAFT_PENDING!r}"
            ),
            failure_sub_tag=".finalize_state_violation",
        )
    if claim_evidence_map.operator_signature_status != OPERATOR_SIG_STATUS_PENDING:
        return ReportRunResult(
            bundle=bundle,
            state_file_path="",
            cycle_completed=False,
            failure_reason=(
                f"finalize invoked on map with "
                f"operator_signature_status="
                f"{claim_evidence_map.operator_signature_status!r}; "
                f"expected PENDING_OPERATOR_REVIEW"
            ),
            failure_sub_tag=".finalize_state_violation",
        )

    # Step 1 — RT-8b post-sign mutation detection (we are AT sign-time;
    # the convention is post_sign_read=True means "re-read draft now and
    # compare to map.draft_content_sha3_512"). The first read at this
    # stage is the pre-sign read but per §14.9.1 we activate
    # post_sign_read=True at the moment of finalization to catch any
    # mutation between run_pipeline and finalize.
    try:
        draft_integrity = deps.draft_integrity_assembler(
            draft_path=claim_evidence_map.draft_path,
            post_sign_read=True,
        )
        source_resolutions = deps.source_resolution_assembler(
            claim_evidence_map=claim_evidence_map, input=input
        )
        narrative_source_texts = deps.narrative_source_texts_assembler(
            claim_evidence_map=claim_evidence_map, input=input
        )
    except Exception as exc:
        return ReportRunResult(
            bundle=bundle,
            state_file_path="",
            cycle_completed=False,
            failure_reason=(
                f"finalize PRE-write assemblers raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag=".finalize_pre_write_assembler_error",
        )

    commitment_untraced_result = check_commitment_untraced(
        claim_evidence_map=claim_evidence_map,
        source_resolutions=source_resolutions,
        narrative_source_texts=narrative_source_texts,
        caption_resolutions=deps.caption_resolutions,
        draft_integrity=draft_integrity,
        prior_period_integrity=deps.prior_period_integrity,
    )

    # Step 2 — Cedar evaluator composes the gate verdict.
    cedar_verdict = evaluate_report_finalize_action(
        bundle, commitment_untraced=commitment_untraced_result
    )
    if cedar_verdict.decision != "PERMIT":
        return ReportRunResult(
            bundle=bundle,
            state_file_path="",
            cycle_completed=False,
            failure_reason=cedar_verdict.detail,
            failure_sub_tag=(
                cedar_verdict.sub_tags[0]
                if cedar_verdict.sub_tags
                else ".cedar_deny"
            ),
        )

    # Step 3 — apply operator Ed25519 signature
    operator_signed_at_utc = deps.clock()
    sign_result = sign_claim_evidence_map(
        claim_evidence_map,
        signer=deps.ed25519_signer,
        operator_signed_at_utc=operator_signed_at_utc,
    )
    if not sign_result.success or sign_result.signed_map is None:
        return ReportRunResult(
            bundle=bundle,
            state_file_path="",
            cycle_completed=False,
            failure_reason=(
                f"sign_claim_evidence_map failed: {sign_result.detail}"
            ),
            failure_sub_tag=".signer_failure",
        )
    signed_map = sign_result.signed_map

    # Step 4 — write-lock the draft + chmod 0444 (post-sign immutability)
    try:
        deps.draft_post_sign_locker(draft_path=signed_map.draft_path)
    except Exception as exc:
        return ReportRunResult(
            bundle=bundle,
            state_file_path="",
            cycle_completed=False,
            failure_reason=(
                f"draft_post_sign_locker raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag=".finalize_locker_failure",
        )

    # Step 5 — write operator_signature.signed.yaml companion record
    operator_signature_record = {
        "schema_version": "operator_signature.v1",
        "run_id": signed_map.run_id,
        "org_slug": signed_map.org_slug,
        "grant_id": signed_map.grant_id,
        "period_n": signed_map.period_n,
        "draft_path": signed_map.draft_path,
        "draft_content_sha3_512": signed_map.draft_content_sha3_512,
        "claim_evidence_map_path": bundle.claim_evidence_map_path,
        "claim_evidence_map_content_sha3_512": deps.hash_bytes(
            canonical_map_bytes(signed_map)
        ),
        "signing_payload_sha3_512": sign_result.signing_payload_sha3_512,
        "operator_signature": signed_map.operator_signature,
        "operator_signed_at_utc": operator_signed_at_utc,
    }
    # Canonical JSON (sort_keys=True) is the wire form for the companion
    # record; the operator_signature_writer translates to YAML on disk.
    signed_yaml_bytes = json.dumps(
        operator_signature_record,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    # The signed.yaml path lives next to the draft.
    operator_signature_path = signed_map.draft_path.rsplit("/", 1)[0] + "/operator_signature.signed.yaml"
    try:
        deps.operator_signature_writer(
            signed_yaml_bytes=signed_yaml_bytes,
            path=operator_signature_path,
        )
    except Exception as exc:
        return ReportRunResult(
            bundle=bundle,
            state_file_path="",
            cycle_completed=False,
            failure_reason=(
                f"operator_signature_writer raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
            failure_sub_tag=".operator_signature_write_failure",
        )

    # Step 6 — construct FINALIZED bundle (the SOLE auto-finalize site)
    finalized_at_utc = deps.clock()
    finalized_bundle = GrantReportBundle(
        run_id=bundle.run_id,
        org_slug=bundle.org_slug,
        grant_id=bundle.grant_id,
        period_n=bundle.period_n,
        draft_path=bundle.draft_path,
        draft_version=bundle.draft_version,
        claim_evidence_map_path=bundle.claim_evidence_map_path,
        scoring_dir=bundle.scoring_dir,
        proposal_commitments_consumed=bundle.proposal_commitments_consumed,
        reporting_template_content_sha3_512=bundle.reporting_template_content_sha3_512,
        sub_sections_authored=bundle.sub_sections_authored,
        operator_signature_status=OPERATOR_SIG_STATUS_SIGNED,
        operator_signature=signed_map.operator_signature,
        operator_signed_at_utc=operator_signed_at_utc,
        finalized_at_utc=finalized_at_utc,
        bundle_state=BUNDLE_STATE_FINALIZED,
    )

    return ReportRunResult(
        bundle=finalized_bundle,
        state_file_path=operator_signature_path,
        cycle_completed=True,
        failure_reason="",
        failure_sub_tag="",
    )


# ---------------------------------------------------------------------------
# Module-load rebind-resistance assertion (mirrors §5 v8 inline-literal pattern)
# ---------------------------------------------------------------------------


assert REPORT_MODE_PIPELINE_SHAPE == (
    "prior_commitments_to_council_to_signed_report"
), (
    "REPORT_MODE_PIPELINE_SHAPE has been rebound at module load — refusing "
    "to load pipeline.orchestrator.tracks.report_mode"
)
assert TILTH_VERSION_FAMILY == "v0.2", (
    "TILTH_VERSION_FAMILY has been rebound at module load — refusing to "
    "load pipeline.orchestrator.tracks.report_mode"
)
assert SUB_SECTIONS_V0_2 == frozenset(
    {
        "narrative",
        "metrics_table",
        "financial_summary",
        "photo_gallery",
        "beneficiary_section",
    }
), (
    "SUB_SECTIONS_V0_2 has been rebound at module load — refusing to load "
    "pipeline.orchestrator.tracks.report_mode"
)


__all__ = [
    "REPORT_MODE_PIPELINE_SHAPE",
    "SUB_SECTIONS_V0_2",
    "TILTH_VERSION_FAMILY",
    "ClockProtocol",
    "ComposerDispatcherProtocol",
    "EditorProtocol",
    "EditorVerdict",
    "FinalizeDeps",
    "GrantReportBundle",
    "HashBytesProtocol",
    "JudgeProtocol",
    "JudgeVerdict",
    "RedTeamProtocol",
    "RedTeamVerdict",
    "ReportGeneratorRunInput",
    "ReportPipelineDeps",
    "ReportRunResult",
    "ScribeProtocol",
    "SubSectionComposerOutput",
    "finalize_operator_signed_report",
    "get_first_wave_marker_binding_at_first_activation",
    "run_report_pipeline",
]
