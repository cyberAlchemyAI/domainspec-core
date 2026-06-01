"""Unit tests for F-CHANNEL-G-CROSS-ORG-LEAK (POST-extract, Law 3, P0).

Per architecture v7.0.5 §3 + §5.3.
"""

from __future__ import annotations

import base64
from urllib.parse import quote

from pipeline.logician.gates.f_channel_g_cross_org_leak import (
    F_CHANNEL_G_CROSS_ORG_LEAK,
    check_channel_g_cross_org_leak,
)


def test_failure_code_constant() -> None:
    assert F_CHANNEL_G_CROSS_ORG_LEAK == "F-CHANNEL-G-CROSS-ORG-LEAK"


def test_clean_extract_passes() -> None:
    r = check_channel_g_cross_org_leak(
        extracted_text="The funder seeks specialty crop value-added projects.",
        session_slug="fit_farms",
    )
    assert r.success is True


def test_raw_match_id_fails() -> None:
    r = check_channel_g_cross_org_leak(
        extracted_text="See match_a1b2c3d4e5f6789012345678901234ab for prior context.",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_CROSS_ORG_LEAK
    assert len(r.leaked_match_ids) == 1


def test_cross_org_reference_fails() -> None:
    r = check_channel_g_cross_org_leak(
        extracted_text="Prior award per orgs/other_org/match_database/cycle_a.yaml row 4.",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_CROSS_ORG_LEAK
    assert "other_org" in r.leaked_org_slugs


def test_same_org_reference_passes() -> None:
    # Reference to session org's OWN match_database is not a leak (same-org)
    r = check_channel_g_cross_org_leak(
        extracted_text="Linked: orgs/fit_farms/match_database/cycle_a.yaml",
        session_slug="fit_farms",
    )
    assert r.success is True


def test_base64_encoded_match_id_caught() -> None:
    # Sanitization-evasion: base64-encoded match_id should still be caught
    payload = "match_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    encoded = base64.b64encode(payload.encode()).decode()
    text = f"Reference token: {encoded}"
    r = check_channel_g_cross_org_leak(
        extracted_text=text,
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_CROSS_ORG_LEAK


def test_hex_encoded_match_id_caught() -> None:
    payload = "match_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    encoded = payload.encode().hex()
    text = f"Hex token: {encoded}"
    r = check_channel_g_cross_org_leak(
        extracted_text=text,
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_CROSS_ORG_LEAK


def test_url_encoded_org_ref_caught() -> None:
    text = f"Linked: {quote('orgs/other_org/match_database/cycle_a.yaml')}"
    r = check_channel_g_cross_org_leak(
        extracted_text=text,
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_CROSS_ORG_LEAK


def test_multiple_leaks_aggregated_in_detail() -> None:
    text = (
        "match_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, "
        "match_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb, "
        "orgs/other_org/match_database/x.yaml"
    )
    r = check_channel_g_cross_org_leak(
        extracted_text=text,
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_CROSS_ORG_LEAK
    assert len(r.leaked_match_ids) == 2
    assert len(r.leaked_org_slugs) == 1


def test_empty_session_slug_fails_closed() -> None:
    r = check_channel_g_cross_org_leak(
        extracted_text="anything goes",
        session_slug="",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_CROSS_ORG_LEAK


def test_case_insensitive_match_id() -> None:
    # match_id pattern is case-insensitive per the regex flag
    r = check_channel_g_cross_org_leak(
        extracted_text="Token MATCH_ABCDEFABCDEFABCDEFABCDEFABCDEFAB embedded.",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_CROSS_ORG_LEAK
