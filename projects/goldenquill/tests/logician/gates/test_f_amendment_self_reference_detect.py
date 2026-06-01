"""Unit tests for F-AMENDMENT-SELF-REFERENCE-DETECT (F-AMDT-07 v1 + v1.1)."""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_07,
    F_AMDT_07_AUTHOR_COLLISION,
    SelfReferenceDetail,
    SelfReferenceResult,
    check_amendment_self_reference,
)


# Representative router config mirroring the live router.yaml surface at
# 2026-04-20. Judge primary = google; five committee slots with one dual-
# family slot (code_reviewer_5: moonshot primary / google fallback).
def _router_config_live() -> dict:
    return {
        "judge_primary_family": "google",
        "code_reviewer_1": {"primary_family": "openai", "fallback_family": "openai"},
        "code_reviewer_2": {"primary_family": "alibaba", "fallback_family": "alibaba"},
        "code_reviewer_3": {"primary_family": "meta", "fallback_family": "meta"},
        "code_reviewer_4": {"primary_family": "openai_oss", "fallback_family": "openai_oss"},
        "code_reviewer_5": {"primary_family": "moonshot", "fallback_family": "google"},
    }


def _reader(config):
    def _r():
        return config
    return _r


# ---------------------------------------------------------------------------
# Trigger discipline — no-op PASS when gate doesn't fire
# ---------------------------------------------------------------------------


def test_modifies_committee_absent_no_op() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={},
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True
    assert r.detail is None


def test_modifies_committee_false_no_op() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={"modifies_committee": False},
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True


@pytest.mark.parametrize("bogus", ["true", "True", 1, 0, [], None])
def test_modifies_committee_truthy_not_True_no_op(bogus: object) -> None:
    """Strict `is True` — YAML-string 'true' or int 1 must NOT fire the gate."""
    r = check_amendment_self_reference(
        amendment_frontmatter={"modifies_committee": bogus},
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# v1 Judge-collision happy paths and DENY paths
# ---------------------------------------------------------------------------


def test_all_three_conditions_met_no_reassignment_denies() -> None:
    """Amendment adds google reviewer (Judge's family); author is anthropic;
    no reassignment → DENY F-AMDT-07."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07
    assert r.detail.reason_tag == "judge_self_reference_unresolved"


def test_all_three_conditions_met_valid_reassignment_passes() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
            "judge_reassigned_to": "alibaba",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True


def test_reassignment_to_judge_primary_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
            "judge_reassigned_to": "google",  # Judge's own primary
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07
    assert r.detail.reason_tag == "judge_reassigned_to_invalid"


def test_reassignment_to_added_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
            "judge_reassigned_to": "google",  # added family itself
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "judge_reassigned_to_invalid"


def test_condition2_fails_added_not_judge_family_passes() -> None:
    """Added family is alibaba, Judge is google → condition 2 fails → PASS."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True


def test_condition3_fails_author_equals_judge_family_passes_v1() -> None:
    """Author IS Judge's family, adding a reviewer of same family — v1 skips
    (different conflict vector). v1.1 may still DENY if author-family
    collides with committee slots. In this config author=google collides
    with code_reviewer_5.fallback_family=google → author-collision DENY.

    This test uses a router where no slot fallback is google to isolate v1
    behavior: mutate the live fixture to drop the google fallback."""
    router = _router_config_live()
    router["code_reviewer_5"] = {"primary_family": "moonshot", "fallback_family": "moonshot"}
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "google",  # author IS Judge's family
        },
        router_config_reader=_reader(router),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Missing-field DENY paths
# ---------------------------------------------------------------------------


def test_missing_added_reviewer_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "added_reviewer_family_missing"


def test_missing_author_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "author_family_missing"


def test_empty_string_added_reviewer_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "added_reviewer_family_missing"


def test_non_string_added_reviewer_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": 123,
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "added_reviewer_family_missing"


def test_empty_author_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "author_family_missing"


def test_empty_judge_reassigned_to_treated_as_missing() -> None:
    """Empty-string reassignment is rejected by _get_nonempty_str — fires the
    unresolved-collision branch, not the invalid-reassignment branch."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
            "judge_reassigned_to": "",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "judge_self_reference_unresolved"


# ---------------------------------------------------------------------------
# Router config structural failures
# ---------------------------------------------------------------------------


def test_router_reader_raises_denies() -> None:
    def _raising():
        raise FileNotFoundError("router.yaml missing")

    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_raising,
    )
    assert r.success is False
    assert r.detail.reason_tag == "router_config_reader_raised"
    assert "FileNotFoundError" in r.detail.reader_error


def test_router_not_dict_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader("not a dict"),
    )
    assert r.success is False
    assert r.detail.reason_tag == "router_config_not_dict"


def test_router_missing_judge_primary_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader({"other_field": "x"}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "judge_primary_family_missing"


def test_router_empty_judge_primary_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader({"judge_primary_family": ""}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "judge_primary_family_missing"


# ---------------------------------------------------------------------------
# v1.1 — author-family anti-collision across committee slot set
# ---------------------------------------------------------------------------


def test_author_family_not_in_any_slot_passes() -> None:
    """Author is anthropic, not in any slot of live router → PASS."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True


def test_author_matches_slot_1_primary_denies() -> None:
    """Author = openai, code_reviewer_1.primary = openai → author-collision DENY."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",  # not Judge's family → v1 skipped
            "author_family": "openai",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07_AUTHOR_COLLISION
    assert r.detail.reason_tag == "author_family_collision_unresolved"
    assert "code_reviewer_1" in r.detail.colliding_slots


def test_author_matches_slot_5_fallback_denies() -> None:
    """Author = google (code_reviewer_5.fallback_family) — gate DENIES on
    fallback-layer collision even when no primary matches."""
    # Use a config where google is ONLY a fallback (not judge primary, and
    # not any slot primary) — but we need modifies_committee to fire and
    # Judge's family to differ. Mutate the fixture to isolate.
    router = _router_config_live()
    router["judge_primary_family"] = "anthropic"
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "google",
        },
        router_config_reader=_reader(router),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07_AUTHOR_COLLISION
    assert "code_reviewer_5" in r.detail.colliding_slots


def test_author_collision_valid_reassignment_passes() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai",
            "committee_slot_reassigned_away_from_author_family": "anthropic",  # not in slot set
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True


def test_author_collision_reassignment_to_same_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai",
            "committee_slot_reassigned_away_from_author_family": "openai",  # self
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "author_reassignment_invalid"


def test_author_collision_reassignment_to_other_slot_family_denies() -> None:
    """Reassigning author's conflicting slot to ANOTHER committee family is
    still inside the committee family set → DENY."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai",
            "committee_slot_reassigned_away_from_author_family": "meta",  # meta ∈ committee_families
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "author_reassignment_invalid"


def test_author_collision_with_openai_oss_fallback_slot() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai_oss",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "author_family_collision_unresolved"
    assert "code_reviewer_4" in r.detail.colliding_slots


def test_author_collision_reports_multiple_slots_when_family_appears_twice() -> None:
    """If author_family appears in two slots, colliding_slots includes both."""
    router = _router_config_live()
    # Make anthropic appear in two slots
    router["code_reviewer_1"] = {"primary_family": "anthropic", "fallback_family": "anthropic"}
    router["code_reviewer_3"] = {"primary_family": "anthropic", "fallback_family": "meta"}
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(router),
    )
    assert r.success is False
    assert "code_reviewer_1" in r.detail.colliding_slots
    assert "code_reviewer_3" in r.detail.colliding_slots


# ---------------------------------------------------------------------------
# Malformed slot entries — gate treats as not-present rather than fail-closing
# ---------------------------------------------------------------------------


def test_malformed_slot_not_dict_is_not_in_committee_set() -> None:
    router = _router_config_live()
    router["code_reviewer_2"] = "not a dict"
    # author_family=openai still collides via slot 1; gate still DENIES but
    # colliding_slots only reports slot 1.
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai",
        },
        router_config_reader=_reader(router),
    )
    assert r.success is False
    assert "code_reviewer_1" in r.detail.colliding_slots
    # slot 2 never contributed alibaba to the family set because it was
    # malformed — so "alibaba" author would be OK. Verify the inverse:
    r2 = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",  # will fire judge-collision
            "author_family": "alibaba",         # no longer collides via slot 2
            "judge_reassigned_to": "anthropic",
        },
        router_config_reader=_reader(router),
    )
    assert r2.success is True


def test_missing_slot_in_router_config() -> None:
    router = _router_config_live()
    del router["code_reviewer_4"]
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai_oss",  # used to collide via deleted slot
        },
        router_config_reader=_reader(router),
    )
    # openai_oss no longer present → PASS
    assert r.success is True


# ---------------------------------------------------------------------------
# Result-shape discipline
# ---------------------------------------------------------------------------


def test_result_is_frozen() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={},
        router_config_reader=_reader(_router_config_live()),
    )
    with pytest.raises((AttributeError, TypeError)):
        r.success = False  # type: ignore[misc]


def test_failure_detail_is_frozen() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.detail is not None
    with pytest.raises((AttributeError, TypeError)):
        r.detail.reason_tag = "other"  # type: ignore[misc]


def test_success_result_detail_is_none() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={},
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.detail is None
    assert r.failure_code is None


def test_failure_code_uses_v1_parent_for_judge_failures() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.failure_code == "F-AMDT-07"


def test_failure_code_uses_sub_code_for_author_failures() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.failure_code == "F-AMDT-07-AUTHOR-COLLISION"


# ---------------------------------------------------------------------------
# Family-name parametrization coverage
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "judge_family",
    ["anthropic", "google", "openai", "groq", "meta"],
)
def test_judge_collision_parametrized_over_families(judge_family: str) -> None:
    router = _router_config_live()
    router["judge_primary_family"] = judge_family
    # Ensure no slot family equals an otherwise-uncorrelated author
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": judge_family,
            "author_family": "anthropic" if judge_family != "anthropic" else "google",
        },
        router_config_reader=_reader(router),
    )
    # The combo triggers v1 judge-collision; no reassignment → DENY
    # Except if author's substitute family collides with slot set, in which
    # case v1.1 fires first after v1 DENIES — but v1 check precedes v1.1.
    assert r.success is False


def test_family_name_case_sensitive_no_match() -> None:
    """Router judge is 'google' lowercase; added reviewer 'Google' capitalised
    → canonical strings do NOT match; condition 2 fails → PASS."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "Google",  # capital
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True


def test_detail_carries_context_on_judge_collision_fail() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.detail.judge_primary_family == "google"
    assert r.detail.added_reviewer_family == "google"
    assert r.detail.author_family == "anthropic"
    assert r.detail.judge_reassigned_to is None


def test_detail_carries_context_on_author_collision_fail() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.detail.author_family == "openai"
    assert "code_reviewer_1" in r.detail.colliding_slots


def test_reader_called_exactly_once_when_triggered() -> None:
    calls: list[int] = []

    def _r():
        calls.append(1)
        return _router_config_live()

    check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_r,
    )
    assert len(calls) == 1


def test_reader_not_called_when_not_triggered() -> None:
    calls: list[int] = []

    def _r():
        calls.append(1)
        return _router_config_live()

    check_amendment_self_reference(
        amendment_frontmatter={"modifies_committee": False},
        router_config_reader=_r,
    )
    assert calls == []


def test_reassignment_valid_when_equals_author_family_but_author_not_in_committee() -> None:
    """If author_family is NOT in committee_families, v1.1 never fires —
    committee_slot_reassigned_away_from_author_family is irrelevant and not
    checked. Verify this doesn't spuriously fail."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "anthropic",  # not in any slot
            "committee_slot_reassigned_away_from_author_family": "anthropic",
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is True


def test_both_v1_and_v11_fire_v1_wins() -> None:
    """Author = openai (collides with slot 1) AND adds Judge's family.
    v1 check runs first; no judge_reassigned_to → DENY with F-AMDT-07 parent
    code (v1 precedes v1.1)."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "openai",  # ≠ google → v1 condition 3 holds
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.failure_code == "F-AMDT-07"  # v1 parent code
    assert r.detail.reason_tag == "judge_self_reference_unresolved"


def test_v1_resolved_v11_still_fires() -> None:
    """v1 resolved via judge_reassigned_to, but v1.1 author-collision is
    still unresolved → DENY with F-AMDT-07-AUTHOR-COLLISION."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "openai",
            "judge_reassigned_to": "anthropic",  # resolves v1
            # no committee_slot_reassigned_away_from_author_family → v1.1 fires
        },
        router_config_reader=_reader(_router_config_live()),
    )
    assert r.success is False
    assert r.failure_code == "F-AMDT-07-AUTHOR-COLLISION"
