"""Adversarial tests for F-DEPRECATION-EXEMPTION-REUSE (F-AMDT-06).

Threat model — what this file enumerates:
  * Truthy-not-True ``forced_replacement`` values that must NOT trigger the
    gate (strict ``is True`` identity guard).
  * ``file_exists`` and ``audit_artifact_reader`` raising every common
    real-world exception (FileNotFoundError / PermissionError / OSError /
    ValueError / RuntimeError / KeyError).
  * Non-bool truthy ``blocking`` values (``1``, ``"true"``) that must NOT
    be treated as blocking.
  * Duplicate ``finding_id`` collisions: N findings with the same ID require
    N distinct valid fix entries; N-1 is FAIL.
  * Extra unused ``cycle_fixes`` entries are harmless (do not mask reuse).
  * Homoglyph / Unicode-normalization mismatches between finding_id and fix
    finding_id stay unmatched (strict byte-identity match).
  * Findings without any ``finding_id`` are counted as unaddressable.
  * Valid-fix shape strictness: empty strings, wrong types, missing keys.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_06,
    check_deprecation_exemption_reuse,
)


def _exists_true(_: str) -> bool:
    return True


def _make_reader(artifact):
    def _r(_: str):
        return artifact
    return _r


def _make_raising_reader(exc_factory):
    def _r(_: str):
        raise exc_factory()
    return _r


class _FakeBool:
    """Truthy object whose __bool__ returns True — must NOT pass the strict
    ``is True`` trigger guard nor the strict ``isinstance(bool)`` blocking
    guard."""

    def __bool__(self) -> bool:  # pragma: no cover - identity check bypasses
        return True


# ---------------------------------------------------------------------------
# ADV-1: strict is-True on forced_replacement rejects all truthy look-alikes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus",
    [
        "true",
        "True",
        "TRUE",
        1,
        1.0,
        [True],
        {"x": True},
        _FakeBool(),
    ],
)
def test_adv_forced_replacement_truthy_not_True_is_noop(bogus: object) -> None:
    """A provider-deprecation amendment with ``forced_replacement: "true"``
    (string) must NOT trigger the gate — strict identity only. Otherwise a
    YAML-coerced string could bypass the L-005 review obligation by
    accident."""
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": bogus,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is True
    assert r.detail is None


# ---------------------------------------------------------------------------
# ADV-2: file_exists raising every common real-world exception
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "exc_factory",
    [
        lambda: FileNotFoundError("no such audit"),
        lambda: PermissionError("denied"),
        lambda: OSError("io error"),
        lambda: RuntimeError("unexpected"),
        lambda: ValueError("bad path"),
    ],
)
def test_adv_file_exists_raises_fail_closed(exc_factory) -> None:
    def _raising(_: str) -> bool:
        raise exc_factory()

    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_raising,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_06
    assert r.detail.reason_tag == "audit_reader_raised"
    assert "file_exists:" in r.detail.reader_error


# ---------------------------------------------------------------------------
# ADV-3: audit_artifact_reader raising after file_exists returned True
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "exc_factory",
    [
        lambda: FileNotFoundError("race"),
        lambda: PermissionError("locked"),
        lambda: ValueError("malformed YAML"),
        lambda: KeyError("red_team_verdict"),
        lambda: RuntimeError("io"),
    ],
)
def test_adv_reader_raises_after_exists_true(exc_factory) -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_raising_reader(exc_factory),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_06
    assert r.detail.reason_tag == "audit_reader_raised"
    assert "audit_reader:" in r.detail.reader_error


# ---------------------------------------------------------------------------
# ADV-4: non-bool truthy blocking (1, "true", list) must FAIL structural
# guard — never interpreted as blocking=True
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus_blocking",
    [1, 0, "true", "false", [], [True], {"b": True}, None],
)
def test_adv_blocking_not_bool_fails_structural(bogus_blocking: object) -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({"red_team_verdict": {"blocking": bogus_blocking}}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "red_team_blocking_not_bool"


# ---------------------------------------------------------------------------
# ADV-5: duplicate finding_id collision — N findings with same ID require N
# distinct fix entries. N-1 must FAIL. This is the Counter-based match.
# ---------------------------------------------------------------------------


def test_adv_two_findings_same_id_require_two_fixes() -> None:
    artifact = {
        "red_team_verdict": {
            "blocking": True,
            "findings": [
                {"finding_id": "FND-DUP", "severity": "HIGH"},
                {"finding_id": "FND-DUP", "severity": "HIGH"},
            ],
        },
        "cycle_fixes": [
            {
                "finding_id": "FND-DUP",
                "fix_description": "first patch",
                "closure_evidence": "diff-1",
            },
        ],
    }
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(artifact),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"
    assert "FND-DUP" in r.detail.unaddressed_finding_ids


def test_adv_two_findings_same_id_pass_with_two_fixes() -> None:
    artifact = {
        "red_team_verdict": {
            "blocking": True,
            "findings": [
                {"finding_id": "FND-DUP", "severity": "HIGH"},
                {"finding_id": "FND-DUP", "severity": "HIGH"},
            ],
        },
        "cycle_fixes": [
            {
                "finding_id": "FND-DUP",
                "fix_description": "first patch",
                "closure_evidence": "diff-1",
            },
            {
                "finding_id": "FND-DUP",
                "fix_description": "second patch",
                "closure_evidence": "diff-2",
            },
        ],
    }
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(artifact),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# ADV-6: extra unused cycle_fixes entries must NOT mask missing matches
# (fixes for unrelated IDs don't count as closure for the blocking findings).
# ---------------------------------------------------------------------------


def test_adv_extra_unused_fixes_do_not_mask_missing() -> None:
    artifact = {
        "red_team_verdict": {
            "blocking": True,
            "findings": [{"finding_id": "FND-REAL", "severity": "HIGH"}],
        },
        "cycle_fixes": [
            {
                "finding_id": "FND-OTHER-1",
                "fix_description": "unrelated",
                "closure_evidence": "e1",
            },
            {
                "finding_id": "FND-OTHER-2",
                "fix_description": "unrelated",
                "closure_evidence": "e2",
            },
            {
                "finding_id": "FND-OTHER-3",
                "fix_description": "unrelated",
                "closure_evidence": "e3",
            },
        ],
    }
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(artifact),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"
    assert "FND-REAL" in r.detail.unaddressed_finding_ids


# ---------------------------------------------------------------------------
# ADV-7: Unicode/homoglyph near-match IDs stay unmatched (strict byte equality)
# ---------------------------------------------------------------------------


def test_adv_homoglyph_finding_ids_do_not_match() -> None:
    # Cyrillic A (U+0410) vs Latin A (U+0041) — look identical, different bytes
    finding_id_latin = "FND-A"
    fix_id_cyrillic = "FND-\u0410"
    assert finding_id_latin != fix_id_cyrillic  # sanity
    artifact = {
        "red_team_verdict": {
            "blocking": True,
            "findings": [{"finding_id": finding_id_latin, "severity": "HIGH"}],
        },
        "cycle_fixes": [
            {
                "finding_id": fix_id_cyrillic,
                "fix_description": "looks like it matches but doesn't",
                "closure_evidence": "e",
            },
        ],
    }
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(artifact),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"
    assert finding_id_latin in r.detail.unaddressed_finding_ids


# ---------------------------------------------------------------------------
# ADV-8: findings without a finding_id are unaddressable — rolled up under
# a synthetic marker so the FAIL is visible in telemetry.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_finding",
    [
        {"severity": "HIGH"},          # key missing
        {"finding_id": None},          # None
        {"finding_id": ""},            # empty string
        {"finding_id": 123},           # non-string
        "not a dict",                  # non-dict finding
        None,                          # None finding
    ],
)
def test_adv_findings_without_valid_id_are_unaddressable(bad_finding: object) -> None:
    artifact = {
        "red_team_verdict": {
            "blocking": True,
            "findings": [bad_finding],
        },
        "cycle_fixes": [
            {
                "finding_id": "FND-ANY",
                "fix_description": "irrelevant",
                "closure_evidence": "e",
            },
        ],
    }
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(artifact),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"
    # findings-without-id must surface via the synthetic marker
    assert any(
        "findings_without_finding_id" in u for u in r.detail.unaddressed_finding_ids
    )


# ---------------------------------------------------------------------------
# ADV-9: fix entry shape strictness — empty strings, wrong types, missing keys
# must all be rejected as invalid fixes.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_fix",
    [
        {"finding_id": "FND-X", "fix_description": "", "closure_evidence": "e"},
        {"finding_id": "FND-X", "fix_description": "d", "closure_evidence": ""},
        {"finding_id": "", "fix_description": "d", "closure_evidence": "e"},
        {"finding_id": "FND-X", "fix_description": "d"},  # missing closure
        {"finding_id": "FND-X", "closure_evidence": "e"},  # missing description
        {"fix_description": "d", "closure_evidence": "e"},  # missing id
        {"finding_id": 123, "fix_description": "d", "closure_evidence": "e"},
        {"finding_id": "FND-X", "fix_description": None, "closure_evidence": "e"},
        {"finding_id": "FND-X", "fix_description": "d", "closure_evidence": None},
        "not a dict",
        None,
        [],
    ],
)
def test_adv_invalid_fix_shape_rejected(bad_fix: object) -> None:
    artifact = {
        "red_team_verdict": {
            "blocking": True,
            "findings": [{"finding_id": "FND-X", "severity": "HIGH"}],
        },
        "cycle_fixes": [bad_fix],
    }
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(artifact),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"
    assert "FND-X" in r.detail.unaddressed_finding_ids


# ---------------------------------------------------------------------------
# ADV-10: file_exists returning truthy-not-True (e.g., "yes", 1) must FAIL
# — strict identity, not truthiness.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus_exists",
    ["yes", 1, "true", [True], _FakeBool()],
)
def test_adv_file_exists_truthy_not_True_fails(bogus_exists: object) -> None:
    def _weird(_: str):
        return bogus_exists

    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_weird,  # type: ignore[arg-type]
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "audit_artifact_file_absent"


# ---------------------------------------------------------------------------
# ADV-11: large-scale mixed findings — many blocking findings, partial fixes —
# every unaddressed ID surfaces; sort-order is stable (for deterministic
# telemetry comparisons across reruns).
# ---------------------------------------------------------------------------


def test_adv_large_scale_partial_closure_deterministic_output() -> None:
    findings = [{"finding_id": f"FND-{i:03d}", "severity": "HIGH"} for i in range(50)]
    # Close only even-indexed findings
    fixes = [
        {
            "finding_id": f"FND-{i:03d}",
            "fix_description": f"fix-{i}",
            "closure_evidence": f"ev-{i}",
        }
        for i in range(0, 50, 2)
    ]
    artifact = {
        "red_team_verdict": {"blocking": True, "findings": findings},
        "cycle_fixes": fixes,
    }
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(artifact),
    )
    assert r.success is False
    # 25 odd-indexed findings unaddressed
    unaddressed = r.detail.unaddressed_finding_ids
    assert len(unaddressed) == 25
    # Deterministic sort
    assert list(unaddressed) == sorted(unaddressed)
    for i in range(1, 50, 2):
        assert f"FND-{i:03d}" in unaddressed
