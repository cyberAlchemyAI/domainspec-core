"""F-AMENDMENT-SELF-REFERENCE-DETECT (F-AMDT-07) — PRE-gate on amendments.

Blocks two self-reference vectors that the Code Thesis Committee anti-
collision design would otherwise silently wave through:

v1 (Judge-family collision) — an amendment that adds a reviewer to the
Code Thesis Committee whose model family matches the active Judge's primary
family, authored by someone NOT of the Judge's family, creates a review in
which the Judge is grading a change that benefits its own family. Requires
an explicit ``judge_reassigned_to`` escape hatch to a third family.

v1.1 (author-family anti-collision, C4-NEW-04 extension) — an amendment
authored by a model family that already appears as a primary or fallback in
ANY of the five committee slots would create a two-same-family review pool.
Requires a ``committee_slot_reassigned_away_from_author_family`` escape
hatch to a family outside the current committee slot set.

The gate is PURE PYTHON, fail-closed, and reads family names exclusively
through the injected ``RouterConfigReaderCallable`` — no YAML parsing.

Semantics (spec card v1 + v1.1, 2026-04-20):
  * Strict ``is True`` trigger guard on ``modifies_committee``.
  * Any missing required field → FAIL.
  * Reader raising → FAIL fail-closed.
  * Non-dict router config → FAIL.
  * Missing ``judge_primary_family`` → FAIL.
  * Exact string equality on family names — no case-fold, no NFC/NFD
    normalisation.
  * v1 reassignment is valid iff present, non-empty, distinct from BOTH
    ``judge_primary_family`` AND ``added_reviewer_family``.
  * v1.1 reassignment is valid iff present, non-empty, and NOT in
    ``committee_families ∪ {author_family}``.
  * Both vectors are checked on every fire: v1 DENY and v1.1 DENY can
    co-occur; the gate reports the most specific failure code that triggered.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates._protocols import RouterConfigReaderCallable


F_AMDT_07: str = "F-AMDT-07"
F_AMDT_07_AUTHOR_COLLISION: str = "F-AMDT-07-AUTHOR-COLLISION"


_REASON_NOT_TRIGGERED: str = "modifies_committee_not_true"
_REASON_READER_RAISED: str = "router_config_reader_raised"
_REASON_ROUTER_NOT_DICT: str = "router_config_not_dict"
_REASON_JUDGE_FAMILY_MISSING: str = "judge_primary_family_missing"
_REASON_ADDED_FAMILY_MISSING: str = "added_reviewer_family_missing"
_REASON_AUTHOR_FAMILY_MISSING: str = "author_family_missing"
_REASON_JUDGE_COLLISION_UNRESOLVED: str = "judge_self_reference_unresolved"
_REASON_JUDGE_REASSIGN_INVALID: str = "judge_reassigned_to_invalid"
_REASON_AUTHOR_COLLISION_UNRESOLVED: str = "author_family_collision_unresolved"
_REASON_AUTHOR_REASSIGN_INVALID: str = "author_reassignment_invalid"


_SLOT_KEYS: tuple[str, ...] = (
    "code_reviewer_1",
    "code_reviewer_2",
    "code_reviewer_3",
    "code_reviewer_4",
    "code_reviewer_5",
)


@dataclass(frozen=True, kw_only=True)
class SelfReferenceDetail:
    reason_tag: str
    judge_primary_family: Optional[str]
    added_reviewer_family: Optional[str]
    author_family: Optional[str]
    judge_reassigned_to: Optional[str]
    committee_slot_reassigned_away_from_author_family: Optional[str]
    colliding_slots: tuple[str, ...]
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class SelfReferenceResult:
    success: bool
    failure_code: Optional[str]
    detail: Optional[SelfReferenceDetail]


def _fail(
    *,
    failure_code: str,
    reason_tag: str,
    judge_primary_family: Optional[str] = None,
    added_reviewer_family: Optional[str] = None,
    author_family: Optional[str] = None,
    judge_reassigned_to: Optional[str] = None,
    committee_slot_reassigned_away_from_author_family: Optional[str] = None,
    colliding_slots: tuple[str, ...] = (),
    reader_error: Optional[str] = None,
) -> SelfReferenceResult:
    return SelfReferenceResult(
        success=False,
        failure_code=failure_code,
        detail=SelfReferenceDetail(
            reason_tag=reason_tag,
            judge_primary_family=judge_primary_family,
            added_reviewer_family=added_reviewer_family,
            author_family=author_family,
            judge_reassigned_to=judge_reassigned_to,
            committee_slot_reassigned_away_from_author_family=(
                committee_slot_reassigned_away_from_author_family
            ),
            colliding_slots=colliding_slots,
            reader_error=reader_error,
        ),
    )


def _ok() -> SelfReferenceResult:
    return SelfReferenceResult(success=True, failure_code=None, detail=None)


def _get_nonempty_str(d: dict, key: str) -> Optional[str]:
    v = d.get(key)
    if isinstance(v, str) and v != "":
        return v
    return None


def _extract_committee_families(
    router: dict,
) -> tuple[set[str], dict[str, tuple[Optional[str], Optional[str]]]]:
    """Return (flat set of all committee slot families, slot→(primary,fallback) map).

    Unknown / malformed slot entries contribute whatever strings they carry
    (or nothing). The gate treats absent slots as not-in-the-set rather than
    fail-closing — the live router.yaml is always a complete 5-slot surface
    and the caller is responsible for shape; what the gate cares about is
    exact matches against the author family."""
    families: set[str] = set()
    slot_map: dict[str, tuple[Optional[str], Optional[str]]] = {}
    for key in _SLOT_KEYS:
        slot = router.get(key)
        if not isinstance(slot, dict):
            slot_map[key] = (None, None)
            continue
        primary = _get_nonempty_str(slot, "primary_family")
        fallback = _get_nonempty_str(slot, "fallback_family")
        if primary is not None:
            families.add(primary)
        if fallback is not None:
            families.add(fallback)
        slot_map[key] = (primary, fallback)
    return families, slot_map


def check_amendment_self_reference(
    *,
    amendment_frontmatter: dict,
    router_config_reader: RouterConfigReaderCallable,
) -> SelfReferenceResult:
    """PRE-gate F-AMENDMENT-SELF-REFERENCE-DETECT (F-AMDT-07 v1 + v1.1).

    Returns PASS (no-op) if the amendment does not modify the committee.
    Otherwise enforces the Judge-collision check (v1) AND the author-family
    anti-collision check (v1.1).
    """
    if amendment_frontmatter.get("modifies_committee") is not True:
        return _ok()

    try:
        router = router_config_reader()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_07,
            reason_tag=_REASON_READER_RAISED,
            reader_error=f"{type(exc).__name__}: {exc}"[:500],
        )

    if not isinstance(router, dict):
        return _fail(failure_code=F_AMDT_07, reason_tag=_REASON_ROUTER_NOT_DICT)

    judge_primary_family = _get_nonempty_str(router, "judge_primary_family")
    if judge_primary_family is None:
        return _fail(failure_code=F_AMDT_07, reason_tag=_REASON_JUDGE_FAMILY_MISSING)

    added_reviewer_family = _get_nonempty_str(amendment_frontmatter, "added_reviewer_family")
    if added_reviewer_family is None:
        return _fail(
            failure_code=F_AMDT_07,
            reason_tag=_REASON_ADDED_FAMILY_MISSING,
            judge_primary_family=judge_primary_family,
        )

    author_family = _get_nonempty_str(amendment_frontmatter, "author_family")
    if author_family is None:
        return _fail(
            failure_code=F_AMDT_07,
            reason_tag=_REASON_AUTHOR_FAMILY_MISSING,
            judge_primary_family=judge_primary_family,
            added_reviewer_family=added_reviewer_family,
        )

    judge_reassigned_to = _get_nonempty_str(amendment_frontmatter, "judge_reassigned_to")

    # v1 check — Judge self-reference
    judge_collision = (
        added_reviewer_family == judge_primary_family
        and author_family != judge_primary_family
    )
    if judge_collision:
        if judge_reassigned_to is None:
            return _fail(
                failure_code=F_AMDT_07,
                reason_tag=_REASON_JUDGE_COLLISION_UNRESOLVED,
                judge_primary_family=judge_primary_family,
                added_reviewer_family=added_reviewer_family,
                author_family=author_family,
            )
        if (
            judge_reassigned_to == judge_primary_family
            or judge_reassigned_to == added_reviewer_family
        ):
            return _fail(
                failure_code=F_AMDT_07,
                reason_tag=_REASON_JUDGE_REASSIGN_INVALID,
                judge_primary_family=judge_primary_family,
                added_reviewer_family=added_reviewer_family,
                author_family=author_family,
                judge_reassigned_to=judge_reassigned_to,
            )

    # v1.1 check — author-family anti-collision against full committee family set
    committee_families, slot_map = _extract_committee_families(router)
    if author_family in committee_families:
        colliding_slots = tuple(
            sorted(
                slot
                for slot, (primary, fallback) in slot_map.items()
                if author_family == primary or author_family == fallback
            )
        )
        reassignment = _get_nonempty_str(
            amendment_frontmatter, "committee_slot_reassigned_away_from_author_family"
        )
        if reassignment is None:
            return _fail(
                failure_code=F_AMDT_07_AUTHOR_COLLISION,
                reason_tag=_REASON_AUTHOR_COLLISION_UNRESOLVED,
                judge_primary_family=judge_primary_family,
                added_reviewer_family=added_reviewer_family,
                author_family=author_family,
                judge_reassigned_to=judge_reassigned_to,
                colliding_slots=colliding_slots,
            )
        # Reassignment must escape BOTH the committee family set AND the author's own family.
        if reassignment == author_family or reassignment in committee_families:
            return _fail(
                failure_code=F_AMDT_07_AUTHOR_COLLISION,
                reason_tag=_REASON_AUTHOR_REASSIGN_INVALID,
                judge_primary_family=judge_primary_family,
                added_reviewer_family=added_reviewer_family,
                author_family=author_family,
                judge_reassigned_to=judge_reassigned_to,
                committee_slot_reassigned_away_from_author_family=reassignment,
                colliding_slots=colliding_slots,
            )

    return _ok()
