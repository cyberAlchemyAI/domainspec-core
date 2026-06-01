"""F-DEPRECATION-EXEMPTION-REUSE (F-AMDT-06) — PRE-gate on forced-replacement amendments.

When a provider deprecates a model or component mid-lifecycle, the
replacement amendment carries ``forced_replacement: true``. The deprecation
event triggers amendment filing but cannot pre-approve the REPLACEMENT
choice — "forced by deprecation" is not a bypass for the L-005 cross-family
review obligation. Without this gate, deprecation urgency could be used to
skip review entirely: the amendment ships; the replacement is never
audited.

This gate verifies that any forced-replacement amendment points to a
cross-family audit artifact whose Red Team verdict is either cleanly
``blocking: False`` OR every blocking finding has a matching ``cycle_fixes``
entry with non-empty ``fix_description`` and ``closure_evidence``.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-2 delta row for F-AMDT-06.

Semantics (spec card v1, 2026-04-20):
  * Strict ``is True`` trigger guard on ``forced_replacement``; any non-True
    value (missing key, ``"true"``, ``1``) → no-op PASS (gate does not fire).
  * Missing ``audit_artifact_path`` → FAIL.
  * ``file_exists`` returns False → FAIL.
  * Reader raises → FAIL fail-closed.
  * Artifact missing ``red_team_verdict`` → FAIL.
  * ``red_team_verdict.blocking is False`` → PASS.
  * ``red_team_verdict.blocking is True`` → every blocking finding's
    ``finding_id`` must appear in ``cycle_fixes`` with non-empty
    ``fix_description`` and ``closure_evidence``; multiple findings with
    the same ``finding_id`` each require their own fix entry (count-based
    match). Otherwise FAIL.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates._protocols import (
    AuditArtifactReaderCallable,
    FileExistsCallable,
)


F_AMDT_06: str = "F-AMDT-06"


_REASON_NOT_TRIGGERED: str = "forced_replacement_not_true"
_REASON_PATH_MISSING: str = "audit_artifact_path_missing"
_REASON_FILE_ABSENT: str = "audit_artifact_file_absent"
_REASON_READER_RAISED: str = "audit_reader_raised"
_REASON_ARTIFACT_NOT_DICT: str = "audit_artifact_not_dict"
_REASON_RED_TEAM_KEY_MISSING: str = "red_team_verdict_key_missing"
_REASON_RED_TEAM_NOT_DICT: str = "red_team_verdict_not_dict"
_REASON_BLOCKING_NOT_BOOL: str = "red_team_blocking_not_bool"
_REASON_FINDINGS_NOT_LIST: str = "red_team_findings_not_list"
_REASON_FIXES_NOT_LIST: str = "cycle_fixes_not_list"
_REASON_UNADDRESSED_FINDINGS: str = "blocking_findings_without_matching_fixes"


@dataclass(frozen=True, kw_only=True)
class DeprecationExemptionDetail:
    reason_tag: str
    unaddressed_finding_ids: tuple[str, ...]
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class DeprecationExemptionResult:
    success: bool
    failure_code: Optional[str]
    detail: Optional[DeprecationExemptionDetail]


def _fail(
    *,
    reason_tag: str,
    unaddressed_finding_ids: tuple[str, ...] = (),
    reader_error: Optional[str] = None,
) -> DeprecationExemptionResult:
    return DeprecationExemptionResult(
        success=False,
        failure_code=F_AMDT_06,
        detail=DeprecationExemptionDetail(
            reason_tag=reason_tag,
            unaddressed_finding_ids=unaddressed_finding_ids,
            reader_error=reader_error,
        ),
    )


def _ok() -> DeprecationExemptionResult:
    return DeprecationExemptionResult(success=True, failure_code=None, detail=None)


def _is_valid_fix(entry: object) -> bool:
    """A fix entry must be a dict with non-empty ``finding_id``,
    ``fix_description`` and ``closure_evidence`` string fields."""
    if not isinstance(entry, dict):
        return False
    for key in ("finding_id", "fix_description", "closure_evidence"):
        v = entry.get(key)
        if not isinstance(v, str) or v == "":
            return False
    return True


def check_deprecation_exemption_reuse(
    *,
    amendment_frontmatter: dict,
    file_exists: FileExistsCallable,
    audit_artifact_reader: AuditArtifactReaderCallable,
) -> DeprecationExemptionResult:
    """PRE-gate F-DEPRECATION-EXEMPTION-REUSE (F-AMDT-06).

    Returns PASS (no-op) if the amendment is not a forced-replacement.
    Otherwise validates the audit artifact referenced by
    ``amendment_frontmatter["audit_artifact_path"]`` per the spec.
    """
    if amendment_frontmatter.get("forced_replacement") is not True:
        return _ok()

    path_value = amendment_frontmatter.get("audit_artifact_path")
    if not isinstance(path_value, str) or path_value == "":
        return _fail(reason_tag=_REASON_PATH_MISSING)

    try:
        exists = file_exists(path_value)
    except Exception as exc:
        return _fail(
            reason_tag=_REASON_READER_RAISED,
            reader_error=f"file_exists: {type(exc).__name__}: {exc}"[:500],
        )

    if exists is not True:
        return _fail(reason_tag=_REASON_FILE_ABSENT)

    try:
        artifact = audit_artifact_reader(path_value)
    except Exception as exc:
        return _fail(
            reason_tag=_REASON_READER_RAISED,
            reader_error=f"audit_reader: {type(exc).__name__}: {exc}"[:500],
        )

    if not isinstance(artifact, dict):
        return _fail(reason_tag=_REASON_ARTIFACT_NOT_DICT)

    if "red_team_verdict" not in artifact:
        return _fail(reason_tag=_REASON_RED_TEAM_KEY_MISSING)

    red_team = artifact["red_team_verdict"]
    if not isinstance(red_team, dict):
        return _fail(reason_tag=_REASON_RED_TEAM_NOT_DICT)

    blocking = red_team.get("blocking")
    if not isinstance(blocking, bool):
        return _fail(reason_tag=_REASON_BLOCKING_NOT_BOOL)

    if blocking is False:
        return _ok()

    findings = red_team.get("findings", [])
    if not isinstance(findings, list):
        return _fail(reason_tag=_REASON_FINDINGS_NOT_LIST)

    fixes = artifact.get("cycle_fixes", [])
    if not isinstance(fixes, list):
        return _fail(reason_tag=_REASON_FIXES_NOT_LIST)

    finding_id_counts: Counter[str] = Counter()
    for f in findings:
        if isinstance(f, dict):
            fid = f.get("finding_id")
            if isinstance(fid, str) and fid != "":
                finding_id_counts[fid] += 1

    fix_id_counts: Counter[str] = Counter()
    for entry in fixes:
        if _is_valid_fix(entry):
            fix_id_counts[entry["finding_id"]] += 1

    unaddressed: list[str] = []
    for fid, needed in finding_id_counts.items():
        if fix_id_counts.get(fid, 0) < needed:
            unaddressed.append(fid)

    findings_without_id = sum(
        1
        for f in findings
        if not (isinstance(f, dict) and isinstance(f.get("finding_id"), str) and f["finding_id"] != "")
    )
    if findings_without_id > 0:
        unaddressed.append(f"<{findings_without_id}_findings_without_finding_id>")

    if unaddressed:
        return _fail(
            reason_tag=_REASON_UNADDRESSED_FINDINGS,
            unaddressed_finding_ids=tuple(sorted(unaddressed)),
        )

    return _ok()
