"""F-UPLOADER-INPUT-INCONSISTENT — PRE-gate.

Per Blueprint §12.9.5 + §4 v2.7 amendment. ``UploaderInput.claim_evidence_map``
MUST equal the union of ``section_drafts[*].claim_evidence_map``. Any
inconsistency (extra entries, missing entries, divergent content) blocks
assembly — the bundle would be ambiguous about which claims have evidence.

ClaimEvidence equality is keyed by ``(section_name, claim_id)``. Two
ClaimEvidence instances with the same key but divergent payload (evidence
text, source ref) are treated as inconsistent. The caller flattens both
sides to comparable tuples; this gate performs the set comparison.

Fail-closed. Bypass: M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


F_UPLOADER_INPUT_INCONSISTENT: str = "F-UPLOADER-INPUT-INCONSISTENT"


@dataclass(frozen=True, kw_only=True)
class InputInconsistentResult:
    """Result of F-UPLOADER-INPUT-INCONSISTENT check."""

    success: bool
    failure_code: Optional[str]
    only_in_top_level: tuple[tuple, ...]
    only_in_sections: tuple[tuple, ...]
    detail: str


def _to_set(items: Iterable[tuple]) -> set[tuple]:
    return set(items)


def check_uploader_input_inconsistent(
    *,
    top_level_claim_evidence: Iterable[tuple],
    section_drafts_claim_evidence: Iterable[tuple],
) -> InputInconsistentResult:
    """PRE-gate: top-level claim_evidence_map == union of per-section maps.

    Both args are flat iterables of comparable tuples (typically
    ``(section_name, claim_id, evidence_hash)``). The caller is responsible
    for flattening section_drafts and computing the comparable tuple form.
    """
    top = _to_set(top_level_claim_evidence)
    sec = _to_set(section_drafts_claim_evidence)
    only_top = top - sec
    only_sec = sec - top
    if only_top or only_sec:
        return InputInconsistentResult(
            success=False,
            failure_code=F_UPLOADER_INPUT_INCONSISTENT,
            only_in_top_level=tuple(sorted(only_top)),
            only_in_sections=tuple(sorted(only_sec)),
            detail=(
                f"claim_evidence_map mismatch: "
                f"{len(only_top)} entries only in top-level, "
                f"{len(only_sec)} entries only in section_drafts union"
            ),
        )
    return InputInconsistentResult(
        success=True,
        failure_code=None,
        only_in_top_level=(),
        only_in_sections=(),
        detail="claim_evidence_map equals union of section_drafts maps",
    )
