"""F-REPORT-TEMPLATE-MISMATCH — PRE pre-track-dispatch.

Per §14 Report Generator v1 LOCKED 2026-05-10 §14.9.5 (Cycle 1 RT-5a/5b/5c
+ Cycle 2 RT-C2-04/05 closures).

Trigger: ``reporting_template.yaml`` schema does not match the funder's
actual reporting template at dispatch time.

Fail-closed/advisory matrix per RT-5a:

* SN-LLC first-wave funder + workspace-published template missing →
  FAIL-CLOSED (``.workspace_published_template_absent_first_wave``).
* Non-first-wave funder + workspace-published template missing →
  ADVISORY (``.workspace_published_template_absent``).
* Workspace-published template present + content-hash mismatch →
  FAIL-CLOSED (``.workspace_published_template_drift``).
* First-wave marker file missing / tampered →
  FAIL-CLOSED (``.workspace_published_template_marker_tampered``;
  RT-C2-04 closure).

Schema-level fail-closed sub-tags:

* ``.schema_required_sub_sections_unrecognized``
* ``.schema_required_fields_unspecified``
* ``.period_cadence_invalid``
* ``.template_signature_invalid``
* ``.operator_key_version_mismatch`` — RT-5b TOFU rotation
* ``.workspace_published_template_marker_tampered`` — RT-C2-04
* ``.period_cadence_actual_drift`` — RT-5c (advisory)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Mapping, Optional, Sequence

from pipeline.logician.gates._report_protocols import (
    PERMITTED_PERIOD_CADENCES,
    ReportingTemplateSnapshot,
    WorkspacePublishedTemplateSnapshot,
)
from pipeline.orchestrator.seats.report_generator._schemas import (
    SUB_SECTIONS_V0_2,
)

F_REPORT_TEMPLATE_MISMATCH: Final[str] = "F-REPORT-TEMPLATE-MISMATCH"

SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_DRIFT: Final[str] = (
    ".workspace_published_template_drift"
)
SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT: Final[str] = (
    ".workspace_published_template_absent"
)
SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT_FIRST_WAVE: Final[str] = (
    ".workspace_published_template_absent_first_wave"
)
SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_MARKER_TAMPERED: Final[str] = (
    ".workspace_published_template_marker_tampered"
)
SUB_TAG_SCHEMA_REQUIRED_SUB_SECTIONS_UNRECOGNIZED: Final[str] = (
    ".schema_required_sub_sections_unrecognized"
)
SUB_TAG_SCHEMA_REQUIRED_FIELDS_UNSPECIFIED: Final[str] = (
    ".schema_required_fields_unspecified"
)
SUB_TAG_PERIOD_CADENCE_INVALID: Final[str] = ".period_cadence_invalid"
SUB_TAG_TEMPLATE_SIGNATURE_INVALID: Final[str] = ".template_signature_invalid"
SUB_TAG_OPERATOR_KEY_VERSION_MISMATCH: Final[str] = ".operator_key_version_mismatch"
SUB_TAG_PERIOD_CADENCE_ACTUAL_DRIFT: Final[str] = ".period_cadence_actual_drift"


# Severity classification per RT-5a / RT-10a closures.
_FAIL_CLOSED_SUB_TAGS: Final[frozenset[str]] = frozenset({
    SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_DRIFT,
    SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT_FIRST_WAVE,
    SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_MARKER_TAMPERED,
    SUB_TAG_SCHEMA_REQUIRED_SUB_SECTIONS_UNRECOGNIZED,
    SUB_TAG_SCHEMA_REQUIRED_FIELDS_UNSPECIFIED,
    SUB_TAG_PERIOD_CADENCE_INVALID,
    SUB_TAG_TEMPLATE_SIGNATURE_INVALID,
    SUB_TAG_OPERATOR_KEY_VERSION_MISMATCH,
})


@dataclass(frozen=True, kw_only=True)
class TemplateMismatchFinding:
    sub_tag: str
    detail: str


@dataclass(frozen=True, kw_only=True)
class TemplateMismatchResult:
    success: bool
    failure_code: Optional[str]
    findings: tuple[TemplateMismatchFinding, ...] = field(default_factory=tuple)
    advisory_findings: tuple[TemplateMismatchFinding, ...] = field(default_factory=tuple)

    @property
    def fired_sub_tags(self) -> tuple[str, ...]:
        seen: list[str] = []
        for f in self.findings + self.advisory_findings:
            if f.sub_tag not in seen:
                seen.append(f.sub_tag)
        return tuple(seen)


def check_template_mismatch(
    *,
    operator_template: ReportingTemplateSnapshot,
    workspace_published: Optional[WorkspacePublishedTemplateSnapshot],
    actual_period_cadence_months: Optional[int] = None,
    operator_pinned_key_version: Optional[str] = None,
) -> TemplateMismatchResult:
    """Walk template invariants; collect fail-closed + advisory findings.

    Inputs:

    * ``operator_template`` — pre-parsed view of ``reporting_template.yaml``.
    * ``workspace_published`` — pre-parsed view of
      ``vault_shared/funder_intelligence/<funder_id>/published_reporting_template.yaml``
      and the SN-LLC first-wave marker (when present).
    * ``actual_period_cadence_months`` — months between
      ``award_signed_at_utc`` and the current period boundary; used for
      RT-5c advisory.
    * ``operator_pinned_key_version`` — currently pinned operator key
      version per RT-5b; ``None`` means TOFU bootstrap (first signature).
    """
    fail_findings: list[TemplateMismatchFinding] = []
    advisory_findings: list[TemplateMismatchFinding] = []

    # Schema shape checks
    unrecognized = [
        s for s in operator_template.required_sub_sections
        if s not in SUB_SECTIONS_V0_2
    ]
    if unrecognized:
        fail_findings.append(
            TemplateMismatchFinding(
                sub_tag=SUB_TAG_SCHEMA_REQUIRED_SUB_SECTIONS_UNRECOGNIZED,
                detail=(
                    f"unrecognized required_sub_sections={unrecognized!r}; "
                    f"closed set={sorted(SUB_SECTIONS_V0_2)}"
                ),
            )
        )
    for required_subsec in operator_template.required_sub_sections:
        fields_for_subsec = operator_template.required_fields_per_sub_section.get(
            required_subsec
        )
        if not fields_for_subsec:
            fail_findings.append(
                TemplateMismatchFinding(
                    sub_tag=SUB_TAG_SCHEMA_REQUIRED_FIELDS_UNSPECIFIED,
                    detail=(
                        f"required_sub_section={required_subsec!r} has empty/missing "
                        f"required_fields_per_sub_section entry"
                    ),
                )
            )

    # Period cadence enum check
    if operator_template.required_period_cadence not in PERMITTED_PERIOD_CADENCES:
        fail_findings.append(
            TemplateMismatchFinding(
                sub_tag=SUB_TAG_PERIOD_CADENCE_INVALID,
                detail=(
                    f"required_period_cadence="
                    f"{operator_template.required_period_cadence!r} not in "
                    f"{sorted(PERMITTED_PERIOD_CADENCES)}"
                ),
            )
        )

    # Template signature (when operator signed the captured template)
    if operator_template.template_signature_present and not operator_template.template_signature_valid:
        fail_findings.append(
            TemplateMismatchFinding(
                sub_tag=SUB_TAG_TEMPLATE_SIGNATURE_INVALID,
                detail="operator-signed template signature did not verify",
            )
        )

    # Operator key version (RT-5b TOFU rotation)
    if operator_pinned_key_version is not None and operator_template.operator_key_version is not None:
        if operator_template.operator_key_version != operator_pinned_key_version:
            fail_findings.append(
                TemplateMismatchFinding(
                    sub_tag=SUB_TAG_OPERATOR_KEY_VERSION_MISMATCH,
                    detail=(
                        f"template operator_key_version="
                        f"{operator_template.operator_key_version!r} != "
                        f"pinned={operator_pinned_key_version!r}"
                    ),
                )
            )

    # Workspace-published template drift / absent / marker tamper
    if workspace_published is None or not workspace_published.present:
        # Funder has no workspace-shared published template.
        is_first_wave = workspace_published is not None and workspace_published.first_wave
        if is_first_wave:
            fail_findings.append(
                TemplateMismatchFinding(
                    sub_tag=SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT_FIRST_WAVE,
                    detail=(
                        f"funder is SN-LLC first-wave but published_reporting_template "
                        f"absent or sn_llc_first_wave marker missing/tampered"
                    ),
                )
            )
        else:
            advisory_findings.append(
                TemplateMismatchFinding(
                    sub_tag=SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT,
                    detail=(
                        f"funder={operator_template.funder_id!r} has no workspace-"
                        f"published template; operator capture is sole source of truth"
                    ),
                )
            )
    else:
        # Workspace-published present — check marker integrity (RT-C2-04)
        if workspace_published.first_wave:
            marker_sig_ok = workspace_published.first_wave_marker_signature_valid
            marker_hash_ok = workspace_published.first_wave_marker_hash_bound_to_lock_history
            if marker_sig_ok is not True or marker_hash_ok is not True:
                fail_findings.append(
                    TemplateMismatchFinding(
                        sub_tag=SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_MARKER_TAMPERED,
                        detail=(
                            f"first-wave marker integrity check failed: "
                            f"sig_valid={marker_sig_ok!r} "
                            f"hash_bound={marker_hash_ok!r}"
                        ),
                    )
                )
        if (
            workspace_published.content_sha3_512 is not None
            and workspace_published.content_sha3_512
            != operator_template.template_content_sha3_512
        ):
            fail_findings.append(
                TemplateMismatchFinding(
                    sub_tag=SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_DRIFT,
                    detail=(
                        f"operator captured template hash="
                        f"{operator_template.template_content_sha3_512[:16]}… vs "
                        f"workspace published hash="
                        f"{workspace_published.content_sha3_512[:16]}…"
                    ),
                )
            )

    # Period cadence vs actual (RT-5c advisory)
    if actual_period_cadence_months is not None:
        expected_months = {
            "monthly": 1, "quarterly": 3, "semi_annual": 6, "annual": 12,
        }.get(operator_template.required_period_cadence)
        if expected_months is not None and expected_months != actual_period_cadence_months:
            advisory_findings.append(
                TemplateMismatchFinding(
                    sub_tag=SUB_TAG_PERIOD_CADENCE_ACTUAL_DRIFT,
                    detail=(
                        f"required_period_cadence="
                        f"{operator_template.required_period_cadence!r} expects "
                        f"{expected_months} months; actual span="
                        f"{actual_period_cadence_months} months"
                    ),
                )
            )

    if fail_findings:
        return TemplateMismatchResult(
            success=False,
            failure_code=F_REPORT_TEMPLATE_MISMATCH,
            findings=tuple(fail_findings),
            advisory_findings=tuple(advisory_findings),
        )
    return TemplateMismatchResult(
        success=True,
        failure_code=None,
        findings=(),
        advisory_findings=tuple(advisory_findings),
    )


__all__ = [
    "F_REPORT_TEMPLATE_MISMATCH",
    "SUB_TAG_OPERATOR_KEY_VERSION_MISMATCH",
    "SUB_TAG_PERIOD_CADENCE_ACTUAL_DRIFT",
    "SUB_TAG_PERIOD_CADENCE_INVALID",
    "SUB_TAG_SCHEMA_REQUIRED_FIELDS_UNSPECIFIED",
    "SUB_TAG_SCHEMA_REQUIRED_SUB_SECTIONS_UNRECOGNIZED",
    "SUB_TAG_TEMPLATE_SIGNATURE_INVALID",
    "SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT",
    "SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT_FIRST_WAVE",
    "SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_DRIFT",
    "SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_MARKER_TAMPERED",
    "TemplateMismatchFinding",
    "TemplateMismatchResult",
    "check_template_mismatch",
]
