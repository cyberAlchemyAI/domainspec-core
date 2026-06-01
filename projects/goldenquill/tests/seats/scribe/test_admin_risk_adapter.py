"""Tests for pipeline.seats.scribe.admin_risk_adapter.

Covers register parse / load (stale + malformed paths), shape invariants,
flag-routing across federal × progressive × identity-overlay axes, and the
POST-gate verifier (verify_draft_flags_or_raise).
"""

from __future__ import annotations

import pytest

from pipeline.seats.scribe.admin_risk_adapter import (
    F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED,
    F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED,
    F_SCRIBE_ADMIN_RISK_REGISTER_STALE,
    F_SCRIBE_ADMIN_RISK_UNFLAGGED,
    SNAPSHOT_AGE_HOURS_CEILING,
    AdminRiskEntry,
    AdminRiskHighUnapproved,
    AdminRiskRegister,
    AdminRiskRegisterMalformed,
    AdminRiskRegisterStale,
    acceptable_under_clc,
    load_admin_risk_register,
    parse_admin_risk_register,
    route_flag_for_match,
    scan_draft_for_admin_risk,
    scan_draft_for_admin_risk_clc,
    term_acceptable_under_clc,
    verify_draft_flags_or_raise,
)
from pipeline.seats.scribe.section_draft import AdminRiskFlag


def _ok_raw_register() -> dict:
    return {
        "version": "2.2",
        "entries": [
            {
                "term": "DEI",
                "severity": "RED",
                "progressive_register": "EXPECTED",
                "alternatives": ["workforce development", "broad participation"],
                "variants": ["diversity equity inclusion"],
                "context": "EO 14151",
            },
            {
                "term": "stakeholder",
                "severity": "YELLOW",
                "alternatives": ["partner", "participant"],
                "context": "centrist softening",
            },
            {
                "term": "synergize",
                "severity": "GREEN",
                "alternatives": ["align", "coordinate"],
                "context": "low-tier jargon",
            },
            {
                "term": "BIPOC",
                "severity": "RED",
                "progressive_register": "PREFERRED",
                "alternatives": ["communities of color"],
                "context": "racial-justice funder language",
            },
        ],
    }


def _parse_ok() -> AdminRiskRegister:
    return parse_admin_risk_register(
        raw_mapping=_ok_raw_register(),
        snapshot_sha3_512="a" * 128,
        snapshot_age_hours=1.0,
    )


# ---------- Constants ----------


def test_snapshot_age_ceiling_is_24h() -> None:
    assert SNAPSHOT_AGE_HOURS_CEILING == 24.0


# ---------- AdminRiskEntry shape ----------


def test_entry_constructs_ok() -> None:
    e = AdminRiskEntry(
        term="x",
        severity="high",
        progressive_register="OK",
        suggested_substitutions=("y",),
        context="",
        variants=(),
    )
    assert e.severity == "high"


def test_entry_rejects_empty_term() -> None:
    with pytest.raises(ValueError, match="term"):
        AdminRiskEntry(
            term="",
            severity="high",
            progressive_register="OK",
            suggested_substitutions=(),
            context="",
            variants=(),
        )


def test_entry_rejects_invalid_progressive_register() -> None:
    with pytest.raises(ValueError, match="progressive_register"):
        AdminRiskEntry(
            term="x",
            severity="high",
            progressive_register="WHATEVER",
            suggested_substitutions=(),
            context="",
            variants=(),
        )


# ---------- parse_admin_risk_register ----------


def test_parse_register_happy() -> None:
    reg = _parse_ok()
    assert reg.version == "2.2"
    assert len(reg.entries) == 4
    by_term = {e.term: e for e in reg.entries}
    assert by_term["DEI"].severity == "high"
    assert by_term["stakeholder"].severity == "medium"
    assert by_term["synergize"].severity == "low"
    assert by_term["BIPOC"].progressive_register == "PREFERRED"
    # Default progressive_register applies to the YELLOW/GREEN entries.
    assert by_term["stakeholder"].progressive_register == "OK"
    assert by_term["synergize"].progressive_register == "OK"


def test_parse_register_rejects_missing_version() -> None:
    with pytest.raises(AdminRiskRegisterMalformed, match="version"):
        parse_admin_risk_register(
            raw_mapping={"entries": [{"term": "x", "severity": "RED"}]},
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_parse_register_rejects_empty_entries() -> None:
    with pytest.raises(AdminRiskRegisterMalformed, match="entries"):
        parse_admin_risk_register(
            raw_mapping={"version": "2.2", "entries": []},
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_parse_register_rejects_unknown_severity() -> None:
    raw = _ok_raw_register()
    raw["entries"][0]["severity"] = "PURPLE"
    with pytest.raises(AdminRiskRegisterMalformed, match="severity"):
        parse_admin_risk_register(
            raw_mapping=raw,
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_parse_register_rejects_invalid_progressive_register() -> None:
    raw = _ok_raw_register()
    raw["entries"][0]["progressive_register"] = "BAD"
    with pytest.raises(AdminRiskRegisterMalformed, match="progressive_register"):
        parse_admin_risk_register(
            raw_mapping=raw,
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_parse_register_rejects_alternatives_not_list() -> None:
    raw = _ok_raw_register()
    raw["entries"][0]["alternatives"] = "not a list"
    with pytest.raises(AdminRiskRegisterMalformed, match="alternatives"):
        parse_admin_risk_register(
            raw_mapping=raw,
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_parse_register_rejects_entry_not_mapping() -> None:
    with pytest.raises(AdminRiskRegisterMalformed, match="not a mapping"):
        parse_admin_risk_register(
            raw_mapping={"version": "2.2", "entries": ["just a string"]},
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_parse_register_rejects_missing_term() -> None:
    raw = {"version": "2.2", "entries": [{"severity": "RED"}]}
    with pytest.raises(AdminRiskRegisterMalformed, match="term"):
        parse_admin_risk_register(
            raw_mapping=raw,
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_parse_register_legacy_entry_without_progressive_register_defaults_ok() -> None:
    raw = {
        "version": "2.2",
        "entries": [
            {
                "term": "legacy",
                "severity": "YELLOW",
                "alternatives": ["other"],
            }
        ],
    }
    reg = parse_admin_risk_register(
        raw_mapping=raw, snapshot_sha3_512="a" * 128, snapshot_age_hours=0.0
    )
    assert reg.entries[0].progressive_register == "OK"


# ---------- load_admin_risk_register (with vault primitive seam) ----------


def test_load_register_stale_fails_closed() -> None:
    def loader(*, register_path: str):  # type: ignore[no-untyped-def]
        raise AssertionError("loader must not be called when stale")

    with pytest.raises(AdminRiskRegisterStale, match="exceeds 24h"):
        load_admin_risk_register(
            register_loader=loader,
            register_path="/x.yaml",
            snapshot_age_hours=25.0,
        )


def test_load_register_stale_bypass_when_disabled() -> None:
    raw = _ok_raw_register()

    def loader(*, register_path: str):  # type: ignore[no-untyped-def]
        return raw

    reg = load_admin_risk_register(
        register_loader=loader,
        register_path="/x.yaml",
        snapshot_age_hours=99.0,
        fail_closed_on_stale=False,
    )
    assert reg.version == "2.2"


def test_load_register_canonical_sha_is_deterministic() -> None:
    raw = _ok_raw_register()

    def loader(*, register_path: str):  # type: ignore[no-untyped-def]
        return raw

    r1 = load_admin_risk_register(
        register_loader=loader, register_path="/x", snapshot_age_hours=0.0
    )
    r2 = load_admin_risk_register(
        register_loader=loader, register_path="/x", snapshot_age_hours=0.0
    )
    assert r1.snapshot_sha3_512 == r2.snapshot_sha3_512
    assert len(r1.snapshot_sha3_512) == 128


# ---------- route_flag_for_match ----------


def _entry(
    term: str,
    severity: str = "high",
    progressive: str = "OK",
    subs: tuple[str, ...] = ("alt",),
) -> AdminRiskEntry:
    return AdminRiskEntry(
        term=term,
        severity=severity,  # type: ignore[arg-type]
        progressive_register=progressive,
        suggested_substitutions=subs,
        context="",
        variants=(),
    )


def test_route_high_federal_funder_flags() -> None:
    f = route_flag_for_match(
        entry=_entry("DEI", severity="high"),
        funder_dialect="conservative",
        identity_claim_terms=(),
        auto_substitute_low_enabled=False,
    )
    assert isinstance(f, AdminRiskFlag)
    assert f.severity == "high"
    assert f.applicant_approved is False
    assert f.proposed_substitution == "alt"


def test_route_progressive_funder_expected_drops_flag() -> None:
    f = route_flag_for_match(
        entry=_entry("DEI", severity="high", progressive="EXPECTED"),
        funder_dialect="progressive",
        identity_claim_terms=(),
        auto_substitute_low_enabled=False,
    )
    assert f is None


def test_route_progressive_funder_preferred_drops_flag() -> None:
    f = route_flag_for_match(
        entry=_entry("BIPOC", severity="high", progressive="PREFERRED"),
        funder_dialect="soul_fire",
        identity_claim_terms=(),
        auto_substitute_low_enabled=False,
    )
    assert f is None


def test_route_progressive_avoid_always_flags() -> None:
    f = route_flag_for_match(
        entry=_entry("slur", severity="medium", progressive="AVOID"),
        funder_dialect="progressive",
        identity_claim_terms=(),
        auto_substitute_low_enabled=False,
    )
    assert f is not None
    assert f.severity == "medium"


def test_route_identity_overlay_drops_flag() -> None:
    # Black-led applicant + identity-tied register entry → no flag.
    f = route_flag_for_match(
        entry=_entry("Black", severity="high"),
        funder_dialect="conservative",
        identity_claim_terms=("Black-led organization",),
        auto_substitute_low_enabled=False,
    )
    assert f is None


def test_route_low_auto_substitute_drops_flag_when_subs_present() -> None:
    f = route_flag_for_match(
        entry=_entry("synergize", severity="low", subs=("align",)),
        funder_dialect="conservative",
        identity_claim_terms=(),
        auto_substitute_low_enabled=True,
    )
    assert f is None


def test_route_low_auto_substitute_disabled_still_flags() -> None:
    f = route_flag_for_match(
        entry=_entry("synergize", severity="low"),
        funder_dialect="conservative",
        identity_claim_terms=(),
        auto_substitute_low_enabled=False,
    )
    assert f is not None
    assert f.severity == "low"


def test_route_low_no_subs_still_flags_even_with_auto_substitute() -> None:
    f = route_flag_for_match(
        entry=_entry("synergize", severity="low", subs=()),
        funder_dialect="conservative",
        identity_claim_terms=(),
        auto_substitute_low_enabled=True,
    )
    # No substitution available → must still flag.
    assert f is not None
    assert f.proposed_substitution is None


def test_route_medium_federal_flags() -> None:
    f = route_flag_for_match(
        entry=_entry("stakeholder", severity="medium"),
        funder_dialect="centrist",
        identity_claim_terms=(),
        auto_substitute_low_enabled=False,
    )
    assert f is not None
    assert f.severity == "medium"


# ---------- scan_draft_for_admin_risk ----------


def test_scan_finds_term_in_body() -> None:
    reg = _parse_ok()
    flags = scan_draft_for_admin_risk(
        draft_body="Our DEI initiative serves underrepresented communities.",
        register=reg,
        funder_dialect="conservative",
    )
    terms = {f.term for f in flags}
    assert "DEI" in terms


def test_scan_case_insensitive() -> None:
    reg = _parse_ok()
    flags = scan_draft_for_admin_risk(
        draft_body="our dei work matters",
        register=reg,
        funder_dialect="conservative",
    )
    assert "DEI" in {f.term for f in flags}


def test_scan_finds_variant_form() -> None:
    reg = _parse_ok()
    flags = scan_draft_for_admin_risk(
        draft_body="Our diversity equity inclusion plan is robust.",
        register=reg,
        funder_dialect="conservative",
    )
    assert "DEI" in {f.term for f in flags}


def test_scan_skips_progressive_expected_under_progressive_funder() -> None:
    reg = _parse_ok()
    flags = scan_draft_for_admin_risk(
        draft_body="Our DEI plan...",
        register=reg,
        funder_dialect="progressive",
    )
    assert "DEI" not in {f.term for f in flags}


def test_scan_no_double_flag_on_same_term() -> None:
    reg = _parse_ok()
    flags = scan_draft_for_admin_risk(
        draft_body="DEI DEI DEI synergize synergize",
        register=reg,
        funder_dialect="conservative",
    )
    assert len([f for f in flags if f.term == "DEI"]) == 1
    assert len([f for f in flags if f.term == "synergize"]) == 1


def test_scan_empty_body_returns_no_flags() -> None:
    reg = _parse_ok()
    flags = scan_draft_for_admin_risk(
        draft_body="",
        register=reg,
        funder_dialect="conservative",
    )
    assert flags == ()


# ---------- verify_draft_flags_or_raise ----------


def test_verify_passes_when_high_terms_declared_and_approved() -> None:
    reg = _parse_ok()
    declared = (
        AdminRiskFlag(
            term="DEI",
            severity="high",
            proposed_substitution="workforce development",
            applicant_approved=True,
        ),
    )
    # Should not raise.
    verify_draft_flags_or_raise(
        draft_body="DEI program description",
        declared_flags=declared,
        register=reg,
        funder_dialect="conservative",
    )


def test_verify_raises_unflagged_when_medium_term_undeclared() -> None:
    reg = _parse_ok()
    with pytest.raises(RuntimeError, match=F_SCRIBE_ADMIN_RISK_UNFLAGGED):
        verify_draft_flags_or_raise(
            draft_body="our stakeholder engagement",
            declared_flags=(),
            register=reg,
            funder_dialect="centrist",
        )


def test_verify_raises_high_unapproved() -> None:
    reg = _parse_ok()
    declared = (
        AdminRiskFlag(
            term="DEI",
            severity="high",
            proposed_substitution="x",
            applicant_approved=False,
        ),
    )
    with pytest.raises(AdminRiskHighUnapproved, match=F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED):
        verify_draft_flags_or_raise(
            draft_body="DEI work",
            declared_flags=declared,
            register=reg,
            funder_dialect="conservative",
        )


def test_verify_low_undeclared_does_not_raise() -> None:
    reg = _parse_ok()
    # synergize is GREEN/low — undeclared is fine for verifier.
    verify_draft_flags_or_raise(
        draft_body="we will synergize across teams",
        declared_flags=(),
        register=reg,
        funder_dialect="conservative",
    )


# ---------- Failure-code constant exports ----------


def test_failure_code_constants_match_spec_strings() -> None:
    assert F_SCRIBE_ADMIN_RISK_REGISTER_STALE == "F-SCRIBE-ADMIN-RISK-REGISTER-STALE"
    assert F_SCRIBE_ADMIN_RISK_UNFLAGGED == "F-SCRIBE-ADMIN-RISK-UNFLAGGED"
    assert F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED == "F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED"
    assert F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED == "F-SCRIBE-ADMIN-RISK-REGISTER-MALFORMED"


# ---------- CLC-axis dialect routing (architecture v7.0.12 §1.2) ----------


def _entry_clc(
    term: str,
    severity: str = "low",
    per_clc: tuple[tuple[str, str], ...] = (),
    subs: tuple[str, ...] = ("alt",),
) -> AdminRiskEntry:
    return AdminRiskEntry(
        term=term,
        severity=severity,  # type: ignore[arg-type]
        progressive_register="OK",
        suggested_substitutions=subs,
        context="",
        variants=(),
        per_clc_register=per_clc,
    )


def test_entry_per_clc_register_rejects_unknown_slug() -> None:
    with pytest.raises(ValueError, match="per_clc_register slug"):
        AdminRiskEntry(
            term="x",
            severity="low",
            progressive_register="OK",
            suggested_substitutions=(),
            context="",
            variants=(),
            per_clc_register=(("not_a_clc", "OK"),),
        )


def test_entry_per_clc_register_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="per_clc_register value"):
        AdminRiskEntry(
            term="x",
            severity="low",
            progressive_register="OK",
            suggested_substitutions=(),
            context="",
            variants=(),
            per_clc_register=(("catalytic_change", "MAYBE"),),
        )


def test_acceptable_under_clc_returns_listed_value() -> None:
    e = _entry_clc(
        "systems change",
        per_clc=(("catalytic_change", "EXPECTED"),),
    )
    assert acceptable_under_clc(entry=e, clc="catalytic_change") == "EXPECTED"


def test_acceptable_under_clc_defaults_to_AVOID_for_unlisted() -> None:
    e = _entry_clc(
        "systems change",
        per_clc=(("catalytic_change", "EXPECTED"),),
    )
    # v7.0.12 §1.2 safest default
    assert acceptable_under_clc(entry=e, clc="market_access") == "AVOID"


def test_acceptable_under_clc_unknown_clc_raises() -> None:
    e = _entry_clc("x", per_clc=())
    with pytest.raises(ValueError, match="clc must be one of"):
        acceptable_under_clc(entry=e, clc="not_a_clc")


def test_parse_per_clc_register_from_yaml_shape() -> None:
    raw = {
        "version": "2.4",
        "entries": [
            {
                "term": "systems change",
                "severity": "GREEN",
                "per_clc_register": {"catalytic_change": "EXPECTED"},
                "alternatives": [],
                "variants": [],
            },
        ],
    }
    reg = parse_admin_risk_register(
        raw_mapping=raw,
        snapshot_sha3_512="a" * 128,
        snapshot_age_hours=0.0,
    )
    e = reg.entries[0]
    assert e.per_clc_register == (("catalytic_change", "EXPECTED"),)


def test_parse_per_clc_register_rejects_unknown_slug() -> None:
    raw = {
        "version": "2.4",
        "entries": [
            {
                "term": "x",
                "severity": "GREEN",
                "per_clc_register": {"not_a_clc": "OK"},
            },
        ],
    }
    with pytest.raises(AdminRiskRegisterMalformed, match="unknown CLC slug"):
        parse_admin_risk_register(
            raw_mapping=raw,
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_term_acceptable_under_clc_term_found() -> None:
    raw = {
        "version": "2.4",
        "entries": [
            {
                "term": "systems change",
                "severity": "GREEN",
                "per_clc_register": {"catalytic_change": "EXPECTED"},
            },
        ],
    }
    reg = parse_admin_risk_register(
        raw_mapping=raw,
        snapshot_sha3_512="a" * 128,
        snapshot_age_hours=0.0,
    )
    assert (
        term_acceptable_under_clc(
            register=reg, term="systems change", clc="catalytic_change"
        )
        == "EXPECTED"
    )
    assert (
        term_acceptable_under_clc(
            register=reg, term="systems change", clc="credit_underwriting"
        )
        == "AVOID"
    )


def test_term_acceptable_under_clc_not_in_register() -> None:
    raw = {
        "version": "2.4",
        "entries": [
            {"term": "DEI", "severity": "RED"},
        ],
    }
    reg = parse_admin_risk_register(
        raw_mapping=raw,
        snapshot_sha3_512="a" * 128,
        snapshot_age_hours=0.0,
    )
    assert (
        term_acceptable_under_clc(
            register=reg, term="unrelated phrase", clc="catalytic_change"
        )
        == "NOT_FLAGGED"
    )


def test_term_acceptable_under_clc_case_insensitive() -> None:
    raw = {
        "version": "2.4",
        "entries": [
            {
                "term": "Systems Change",
                "severity": "GREEN",
                "per_clc_register": {"catalytic_change": "EXPECTED"},
            },
        ],
    }
    reg = parse_admin_risk_register(
        raw_mapping=raw,
        snapshot_sha3_512="a" * 128,
        snapshot_age_hours=0.0,
    )
    assert (
        term_acceptable_under_clc(
            register=reg, term="systems change", clc="catalytic_change"
        )
        == "EXPECTED"
    )


def test_scan_clc_drops_flag_when_active_clc_expected() -> None:
    raw = {
        "version": "2.4",
        "entries": [
            {
                "term": "systems change",
                "severity": "GREEN",
                "per_clc_register": {"catalytic_change": "EXPECTED"},
                "alternatives": ["alt"],
            },
        ],
    }
    reg = parse_admin_risk_register(
        raw_mapping=raw, snapshot_sha3_512="a" * 128, snapshot_age_hours=0.0
    )
    flags = scan_draft_for_admin_risk_clc(
        draft_body="our systems change approach",
        register=reg,
        active_clc="catalytic_change",
    )
    assert flags == ()


def test_scan_clc_flags_when_active_clc_avoid_default() -> None:
    raw = {
        "version": "2.4",
        "entries": [
            {
                "term": "systems change",
                "severity": "GREEN",
                "per_clc_register": {"catalytic_change": "EXPECTED"},
                "alternatives": ["alt"],
            },
        ],
    }
    reg = parse_admin_risk_register(
        raw_mapping=raw, snapshot_sha3_512="a" * 128, snapshot_age_hours=0.0
    )
    # market_access not listed → defaults AVOID → flag fires
    flags = scan_draft_for_admin_risk_clc(
        draft_body="our systems change approach",
        register=reg,
        active_clc="market_access",
    )
    assert len(flags) == 1
    assert flags[0].term == "systems change"


def test_scan_clc_rejects_unknown_active_clc() -> None:
    raw = {"version": "2.4", "entries": [{"term": "x", "severity": "GREEN"}]}
    reg = parse_admin_risk_register(
        raw_mapping=raw, snapshot_sha3_512="a" * 128, snapshot_age_hours=0.0
    )
    with pytest.raises(ValueError, match="active_clc must be one of"):
        scan_draft_for_admin_risk_clc(
            draft_body="anything",
            register=reg,
            active_clc="not_a_clc",
        )


def test_scan_clc_identity_overlay_drops_flag() -> None:
    raw = {
        "version": "2.4",
        "entries": [
            {
                "term": "Black",
                "severity": "RED",
                "per_clc_register": {"catalytic_change": "AVOID"},
            },
        ],
    }
    reg = parse_admin_risk_register(
        raw_mapping=raw, snapshot_sha3_512="a" * 128, snapshot_age_hours=0.0
    )
    flags = scan_draft_for_admin_risk_clc(
        draft_body="our Black-led organization",
        register=reg,
        active_clc="catalytic_change",
        identity_claim_terms=("Black-led organization",),
    )
    assert flags == ()
