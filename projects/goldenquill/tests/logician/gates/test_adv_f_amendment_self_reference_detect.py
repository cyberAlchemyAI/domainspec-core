"""Adversarial tests for F-AMENDMENT-SELF-REFERENCE-DETECT (F-AMDT-07 v1 + v1.1).

Threat model:
  * Truthy-not-True ``modifies_committee`` values must NOT fire the gate.
  * Router config reader raising every common exception → fail-closed.
  * Unicode / case / homoglyph family-name near-matches must NOT be treated
    as matches (strict byte equality).
  * Live fallback resolution: gate reads BOTH primary and fallback families
    from every slot — fallback-only collisions must DENY even when primary
    is clean.
  * Reassignment hygiene: reassignment equal to added_reviewer_family or
    Judge's primary family (v1) or any committee family (v1.1) must DENY.
  * author_family == judge_primary_family (condition 3 fails) → v1 skipped,
    but v1.1 author-anti-collision must still fire if author ∈ committee set.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_07,
    F_AMDT_07_AUTHOR_COLLISION,
    check_amendment_self_reference,
)


def _router_live() -> dict:
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


class _FakeBool:
    def __bool__(self) -> bool:  # pragma: no cover - identity check bypasses
        return True


# ---------------------------------------------------------------------------
# ADV-1: strict `is True` on modifies_committee
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus",
    ["true", "True", "TRUE", 1, 1.0, [True], {"x": True}, _FakeBool()],
)
def test_adv_modifies_committee_truthy_not_True_is_noop(bogus: object) -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": bogus,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# ADV-2: router_config_reader raising every common exception
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "exc_factory",
    [
        lambda: FileNotFoundError("router.yaml missing"),
        lambda: PermissionError("denied"),
        lambda: OSError("io"),
        lambda: ValueError("bad YAML"),
        lambda: RuntimeError("unexpected"),
        lambda: KeyError("judge_primary_family"),
    ],
)
def test_adv_router_reader_raises_fail_closed(exc_factory) -> None:
    def _raising():
        raise exc_factory()

    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_raising,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07
    assert r.detail.reason_tag == "router_config_reader_raised"


# ---------------------------------------------------------------------------
# ADV-3: family-name case/homoglyph near-match — exact string equality only
# ---------------------------------------------------------------------------


def test_adv_family_name_capitalization_no_match() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "GOOGLE",  # all-caps
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is True


def test_adv_family_name_trailing_whitespace_no_match() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google ",  # trailing space
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is True


def test_adv_family_name_homoglyph_no_match() -> None:
    # Cyrillic 'o' (U+043E) vs Latin 'o' (U+006F)
    router = _router_live()
    router["judge_primary_family"] = "g\u043e\u043egle"
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",  # Latin o
            "author_family": "anthropic",
        },
        router_config_reader=_reader(router),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# ADV-4: reassignment self-reference — reassigning to family being added
# is still a self-reference conflict
# ---------------------------------------------------------------------------


def test_adv_judge_reassigned_to_same_as_added_family_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
            "judge_reassigned_to": "google",  # same as added
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "judge_reassigned_to_invalid"


# ---------------------------------------------------------------------------
# ADV-5: all three families identical — condition 3 fails → v1 PASS;
# v1.1 also PASS because a family not in committee family set.
# But if the shared family IS in committee set → v1.1 DENY.
# ---------------------------------------------------------------------------


def test_adv_all_three_families_identical_v1_skipped() -> None:
    """author=added=judge=google. v1 condition 3 fails → v1 skips.
    v1.1: google IS in committee set (slot 5 fallback) → v1.1 fires → DENY."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "google",
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07_AUTHOR_COLLISION


def test_adv_all_three_families_identical_author_not_in_committee() -> None:
    """author=added=judge=anthropic. Not in committee → v1 skips, v1.1 skips → PASS."""
    router = _router_live()
    router["judge_primary_family"] = "anthropic"
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "anthropic",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(router),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# ADV-6: author-collision-via-fallback — the motivating C4-NEW-04 scenario
# ---------------------------------------------------------------------------


def test_adv_author_collides_with_tertiary_not_primary() -> None:
    """Router where code_reviewer_1 serves openai primary AND openai fallback
    (both via same family). Author is openai — collides via ANY layer."""
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",  # not Judge's family
            "author_family": "openai",
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07_AUTHOR_COLLISION
    assert "code_reviewer_1" in r.detail.colliding_slots


def test_adv_author_collides_post_fallback_scenario() -> None:
    """Simulate live fallback scenario: a slot's primary has rotated into
    its fallback, and author was cleared against old primary but now
    collides with the new fallback. Gate checks BOTH layers at check time,
    so either way → DENY."""
    router = _router_live()
    # Slot 3 previously meta/meta; now primary shifted to anthropic, fallback retains meta.
    router["code_reviewer_3"] = {"primary_family": "anthropic", "fallback_family": "meta"}
    # Author was cleared against old primary (meta), now collides with fallback (meta).
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "meta",
        },
        router_config_reader=_reader(router),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07_AUTHOR_COLLISION
    assert "code_reviewer_3" in r.detail.colliding_slots


# ---------------------------------------------------------------------------
# ADV-7: reassignment-to-family-set escape must escape the ENTIRE set,
# not just the colliding slot
# ---------------------------------------------------------------------------


def test_adv_reassignment_to_different_slot_family_still_inside_set_denies() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "openai",
            "committee_slot_reassigned_away_from_author_family": "meta",  # still in set
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "author_reassignment_invalid"


# ---------------------------------------------------------------------------
# ADV-8: reader returning non-dict (list, string, None, int) → DENY
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus",
    [None, "not a dict", 42, [], ["yaml line"], (("judge_primary_family", "google"),)],
)
def test_adv_router_not_dict_denies_various(bogus: object) -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(bogus),
    )
    assert r.success is False
    assert r.detail.reason_tag == "router_config_not_dict"


# ---------------------------------------------------------------------------
# ADV-9: judge_primary_family is non-string — treated as missing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus_judge",
    [None, 42, [], {}, True],
)
def test_adv_judge_primary_family_non_string_denies(bogus_judge: object) -> None:
    router = _router_live()
    router["judge_primary_family"] = bogus_judge
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(router),
    )
    assert r.success is False
    assert r.detail.reason_tag == "judge_primary_family_missing"


# ---------------------------------------------------------------------------
# ADV-10: non-string author/added family → DENY as missing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus", [None, 42, True, [], {}, object()],
)
def test_adv_non_string_added_family_denies(bogus: object) -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": bogus,
            "author_family": "anthropic",
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "added_reviewer_family_missing"


@pytest.mark.parametrize(
    "bogus", [None, 42, True, [], {}, object()],
)
def test_adv_non_string_author_family_denies(bogus: object) -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": bogus,
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "author_family_missing"


# ---------------------------------------------------------------------------
# ADV-11: judge-collision resolved but author fills a silent v1.1 gap —
# MUST still DENY under v1.1 sub-code
# ---------------------------------------------------------------------------


def test_adv_v1_resolved_v11_must_still_deny() -> None:
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",  # judge collision
            "author_family": "openai_oss",      # collides with slot 4
            "judge_reassigned_to": "anthropic", # resolves v1
            # NO committee_slot_reassigned → v1.1 unresolved
        },
        router_config_reader=_reader(_router_live()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07_AUTHOR_COLLISION
    assert "code_reviewer_4" in r.detail.colliding_slots


# ---------------------------------------------------------------------------
# ADV-12: deeply nested non-dict slots — gate treats as missing, not error
# ---------------------------------------------------------------------------


def test_adv_slot_primary_not_string_treated_as_missing() -> None:
    router = _router_live()
    router["code_reviewer_2"] = {"primary_family": 42, "fallback_family": "alibaba"}
    # author=alibaba still collides via fallback; slot 2 still in colliding list.
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "google",
            "author_family": "alibaba",
            "judge_reassigned_to": "anthropic",  # resolve v1
        },
        router_config_reader=_reader(router),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_07_AUTHOR_COLLISION
    assert "code_reviewer_2" in r.detail.colliding_slots


def test_adv_all_slot_families_blank_author_clean_passes() -> None:
    router = {
        "judge_primary_family": "google",
        "code_reviewer_1": {"primary_family": None, "fallback_family": None},
        "code_reviewer_2": {"primary_family": "", "fallback_family": ""},
        "code_reviewer_3": None,
        "code_reviewer_4": "broken",
        "code_reviewer_5": {},
    }
    r = check_amendment_self_reference(
        amendment_frontmatter={
            "modifies_committee": True,
            "added_reviewer_family": "alibaba",
            "author_family": "anthropic",
        },
        router_config_reader=_reader(router),
    )
    # No judge-collision (alibaba != google), no slot collisions — PASS.
    assert r.success is True
