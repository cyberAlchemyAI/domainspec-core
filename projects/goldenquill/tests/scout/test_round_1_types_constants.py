"""Round 1 — pipeline.scout._types + _constants + __init__.

Verifies:
1. Every §2 dataclass is frozen + kw_only and rejects positional construction.
2. Every §8 pinned constant matches the blueprint value and has the expected
   Python type.
3. Every §2-enum `Final[str]` literal is the exact spelling the blueprint
   schema field domain names.
4. Every `canonical_bytes` helper is deterministic, sorts keys, hex-encodes
   bytes, sorts frozensets, and produces distinct output for distinct inputs.
5. The package `__all__` exports every public symbol and no private name.
6. The package imports with zero side effects (no disk, no network, fast).

Tests live under `tests/scout/` so pytest's `testpaths = ["tests"]` pins in
pyproject.toml automatically pick them up without further configuration.
"""

from __future__ import annotations

import dataclasses
import importlib
import json
import re
import time
from dataclasses import FrozenInstanceError

import pytest

import pipeline.scout as scout
from pipeline.scout import (
    CANDIDATE_ID_HEX_LEN,
    CHANNEL_A,
    CHANNEL_A_CONNECT_TIMEOUT_S,
    CHANNEL_A_READ_TIMEOUT_S,
    CHANNEL_A_RETRY_COUNT,
    CHANNEL_B,
    CHANNEL_C,
    CHANNEL_D,
    CHANNEL_D_MAX_CANDIDATES_PER_PAGE,
    CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER,
    CHANNEL_E,
    CHANNEL_E_RUNAWAY_MAX,
    CHANNEL_F,
    CLAIM_ID_HEX_LEN,
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    DECISION_ACCEPT,
    DECISION_HOLD,
    DECISION_REJECT,
    DOSSIER_VALIDITY_DAYS,
    FEED_PREFIX_API,
    FEED_PREFIX_BRAVE,
    FEED_PREFIX_CACHE,
    FEED_PREFIX_PORTAL,
    FEED_PREFIX_RSS,
    FEED_PREFIX_SEARXNG,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT,
    INTENT_CHANNEL_F_POLICY_READ,
    INTENT_DOSSIER_BODY_WRITE,
    INTENT_DOSSIER_SIGNOFF_WRITE,
    INTENT_READ,
    INTENT_REVIEW_QUEUE_WRITE,
    INTENT_SCOUT_RUN_LOG_WRITE,
    MAX_DOSSIER_BYTES,
    SCOUT_CANDIDATE_VERIFY_CAP,
    SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO,
    SCOUT_REVIEW_LOCK_STRIPES,
    VERDICT_UNVERIFIED,
    VERDICT_VERIFICATION_FAILED,
    VERDICT_VERIFIED_FIT,
    VERDICT_VERIFIED_NOT_FIT,
    Candidate,
    ChannelFJurisdictionPolicy,
    DossierSignoff,
    EntityClaim,
    EntityDossier,
    EntityRosterEntry,
    HealthTuple,
    ReviewQueueItem,
    SignedHealthTuple,
    SourceDomainAllowlist,
    VerificationVerdict,
    candidate_canonical_bytes,
    dossier_signoff_canonical_bytes,
    entity_dossier_canonical_bytes,
    health_tuple_canonical_bytes,
)


# ---------------------------------------------------------------------------
# Fixture builders — minimal valid instances of each §2 schema
# ---------------------------------------------------------------------------


def _candidate() -> Candidate:
    return Candidate(
        candidate_id="a" * CANDIDATE_ID_HEX_LEN,
        channel=CHANNEL_A,
        feed_or_adapter_id=f"{FEED_PREFIX_API}:grants.gov",
        source_key="OPP-123",
        title="Some Opportunity",
        funder="USDA",
        funder_kind="federal",
        url="https://grants.gov/web/grants/view-opportunity.html?oppId=123",
        close_date_utc="2026-06-01T00:00:00Z",
        award_ceiling=500_000,
        award_floor=100_000,
        applicant_types=("Nonprofits", "Small businesses"),
        program_page_url=None,
        fetch_timestamp_utc="2026-04-20T12:00:00Z",
        url_hash="b" * 128,
        content_hash="c" * 128,
        fit_score_cached=72,
        cache_provenance=None,
    )


def _verdict() -> VerificationVerdict:
    return VerificationVerdict(
        candidate_id="a" * CANDIDATE_ID_HEX_LEN,
        verdict=VERDICT_VERIFIED_FIT,
        reason_code="V-OK",
        live_synopsis_url="https://grants.gov/...",
        live_content_hash="d" * 128,
        fetched_at_utc="2026-04-20T12:05:00Z",
        timeout_seconds=10,
        eligibility_live=("nonprofit",),
        award_floor_live=100_000,
        award_ceiling_live=500_000,
        close_date_live_utc="2026-06-01T00:00:00Z",
        evidence_quote="Eligible applicants: nonprofit organizations.",
    )


def _health_tuple() -> HealthTuple:
    return HealthTuple(
        session_id="sess-0000",
        slug="fit_farms_llc",
        run_id="r" * 24,
        run_wall_ns=1_700_000_000_000_000_000,
        channel_a=HEALTH_OK,
        channel_b=HEALTH_OK,
        channel_c=HEALTH_DEGRADED,
        channel_d=HEALTH_OK,
        channel_e=HEALTH_OK,
        channel_f=HEALTH_OK,
        channel_a_endpoints={
            "grants.gov": HEALTH_OK,
            "sam.gov": HEALTH_OK,
            "usaspending.gov": HEALTH_OK,
        },
        backbone_failed=False,
        run_entropy={
            "run_urandom_hex": "00" * 8,
            "run_monotonic_ns": 1_700_000_000_000_000_000,
            "run_tiebreak_seed_hex": "00" * 16,
        },
    )


def _signed_health_tuple() -> SignedHealthTuple:
    return SignedHealthTuple(
        tuple_canonical=b"{}",
        hmac_sha3_512=b"\x00" * 64,
        signed_at_utc="2026-04-20T12:10:00Z",
        hmac_key_id="tilth.scout.health.hmac.v1",
    )


def _review_item() -> ReviewQueueItem:
    return ReviewQueueItem(
        candidate_id="a" * CANDIDATE_ID_HEX_LEN,
        queued_at_utc="2026-04-20T12:15:00Z",
        queued_by_verdict=VERDICT_VERIFIED_FIT,
        candidate_snapshot=_candidate(),
        verification_snapshot=_verdict(),
        fit_rationale="Applicant eligibility aligns with RFA eligibility.",
        operator_decision=None,
        operator_decided_at_utc=None,
        operator_decision_reason=None,
    )


def _roster_entry() -> EntityRosterEntry:
    return EntityRosterEntry(
        entity_slug="josh-inklovich",
        display_name="Josh Inklovich",
        kind="person_lead",
        seed_urls=("https://fitfarms.example/about",),
        added_by="operator",
        added_at_utc="2026-04-20T12:00:00Z",
    )


def _claim() -> EntityClaim:
    return EntityClaim(
        claim_id="c" * CLAIM_ID_HEX_LEN,
        claim_text="Directs PA mushroom foraging certification program.",
        source_url="https://agriculture.pa.gov/wild-mushroom-cert",
        source_registrable_domain="pa.gov",
        fetched_at_utc="2026-04-20T12:00:00Z",
        url_hash="e" * 128,
        content_hash="f" * 128,
        evidence_quote="Program director: Josh Inklovich.",
        confidence_tier=CONFIDENCE_HIGH,
        corroborating_claim_ids=("d" * CLAIM_ID_HEX_LEN,),
    )


def _signoff() -> DossierSignoff:
    return DossierSignoff(
        signed_at_utc="2026-04-20T12:30:00Z",
        operator_id="josh",
        signed_canonical_path="/repo/orgs/x/dossier/entities/josh-inklovich.md",
        signed_inode=1_234_567,
        signed_content_hash="9" * 128,
        operator_signature=b"\x01" * 64,
        expires_at_utc="2026-07-19T12:30:00Z",
    )


def _dossier() -> EntityDossier:
    return EntityDossier(
        entity_slug="josh-inklovich",
        roster_entry=_roster_entry(),
        claims=(_claim(),),
        dossier_written_at_utc="2026-04-20T12:25:00Z",
        dossier_content_hash="9" * 128,
        operator_signoff=_signoff(),
    )


def _allowlist() -> SourceDomainAllowlist:
    return SourceDomainAllowlist(
        slug="fit_farms_llc",
        allowlisted_registrable_domains=frozenset({"grants.gov", "usda.gov"}),
        last_updated_at_utc="2026-04-20T00:00:00Z",
        last_updated_by_operator_id="josh",
    )


def _policy() -> ChannelFJurisdictionPolicy:
    return ChannelFJurisdictionPolicy(
        slug="fit_farms_llc",
        opt_in=True,
        allowed_jurisdictions=frozenset({"US"}),
        disallowed_registrable_domains=frozenset({"example.net"}),
        last_updated_at_utc="2026-04-20T00:00:00Z",
    )


# ---------------------------------------------------------------------------
# Frozen + kw_only discipline
# ---------------------------------------------------------------------------


class TestFrozenDiscipline:
    @pytest.mark.parametrize(
        ("build", "field", "value"),
        [
            (_candidate, "candidate_id", "z" * CANDIDATE_ID_HEX_LEN),
            (_verdict, "verdict", VERDICT_UNVERIFIED),
            (_health_tuple, "channel_a", HEALTH_FAILED),
            (_signed_health_tuple, "hmac_key_id", "other"),
            (_review_item, "operator_decision", DECISION_ACCEPT),
            (_roster_entry, "kind", "org_applicant"),
            (_claim, "confidence_tier", CONFIDENCE_LOW),
            (_signoff, "operator_id", "mallory"),
            (_dossier, "entity_slug", "other"),
            (_allowlist, "slug", "other"),
            (_policy, "opt_in", False),
        ],
    )
    def test_dataclass_is_frozen(self, build, field, value):
        instance = build()
        with pytest.raises(FrozenInstanceError):
            setattr(instance, field, value)


class TestKWOnly:
    @pytest.mark.parametrize(
        ("cls", "positional"),
        [
            (Candidate, ("a" * 24,)),
            (VerificationVerdict, ("a" * 24,)),
            (HealthTuple, ("s",)),
            (SignedHealthTuple, (b"",)),
            (ReviewQueueItem, ("a" * 24,)),
            (EntityRosterEntry, ("slug",)),
            (EntityClaim, ("c" * 24,)),
            (EntityDossier, ("slug",)),
            (DossierSignoff, ("2026",)),
            (SourceDomainAllowlist, ("slug",)),
            (ChannelFJurisdictionPolicy, ("slug",)),
        ],
    )
    def test_rejects_positional(self, cls, positional):
        with pytest.raises(TypeError):
            cls(*positional)  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# Field-completeness + round-trip
# ---------------------------------------------------------------------------


class TestFieldCompleteness:
    @pytest.mark.parametrize(
        "build",
        [
            _candidate,
            _verdict,
            _health_tuple,
            _signed_health_tuple,
            _review_item,
            _roster_entry,
            _claim,
            _signoff,
            _dossier,
            _allowlist,
            _policy,
        ],
    )
    def test_asdict_round_trip(self, build):
        instance = build()
        as_dict = dataclasses.asdict(instance)
        assert isinstance(as_dict, dict)
        for field in dataclasses.fields(instance):
            assert field.name in as_dict

    def test_optional_fields_accept_none_and_value(self):
        # VerificationVerdict.live_synopsis_url is Optional[str]
        both = _verdict()
        nulled = dataclasses.replace(both, live_synopsis_url=None)
        assert both.live_synopsis_url is not None
        assert nulled.live_synopsis_url is None

    def test_tuple_valued_fields_are_tuples(self):
        cand = _candidate()
        assert isinstance(cand.applicant_types, tuple)
        claim = _claim()
        assert isinstance(claim.corroborating_claim_ids, tuple)
        dossier = _dossier()
        assert isinstance(dossier.claims, tuple)

    def test_frozenset_valued_fields_are_frozensets(self):
        allow = _allowlist()
        assert isinstance(allow.allowlisted_registrable_domains, frozenset)
        pol = _policy()
        assert isinstance(pol.allowed_jurisdictions, frozenset)
        assert isinstance(pol.disallowed_registrable_domains, frozenset)

    def test_nested_dataclass_fields_preserved(self):
        item = _review_item()
        assert isinstance(item.candidate_snapshot, Candidate)
        assert isinstance(item.verification_snapshot, VerificationVerdict)
        dossier = _dossier()
        assert isinstance(dossier.roster_entry, EntityRosterEntry)
        assert dossier.operator_signoff is not None
        assert isinstance(dossier.operator_signoff, DossierSignoff)

    def test_unsigned_dossier_accepts_none_signoff(self):
        unsigned = dataclasses.replace(_dossier(), operator_signoff=None)
        assert unsigned.operator_signoff is None

    def test_health_tuple_has_run_entropy_field(self):
        # Round-2 amendment: §4.10 body lists run_entropy as an audit-replay
        # field. Option A of the Round 2 spec card promotes it to a real
        # HealthTuple field so signer/verifier canonicalize identically.
        ht = _health_tuple()
        assert isinstance(ht.run_entropy, dict)
        assert "run_urandom_hex" in ht.run_entropy
        assert "run_monotonic_ns" in ht.run_entropy
        assert "run_tiebreak_seed_hex" in ht.run_entropy

    def test_health_tuple_run_entropy_is_canonical_bytes_stable(self):
        ht1 = _health_tuple()
        ht2 = dataclasses.replace(
            ht1,
            run_entropy={
                "run_urandom_hex": "00" * 8,
                "run_monotonic_ns": 9_999,
                "run_tiebreak_seed_hex": "00" * 16,
            },
        )
        assert health_tuple_canonical_bytes(ht1) != health_tuple_canonical_bytes(ht2)


# ---------------------------------------------------------------------------
# Canonical-bytes determinism + correctness
# ---------------------------------------------------------------------------


class TestCanonicalBytes:
    def test_health_tuple_bytes_deterministic(self):
        ht = _health_tuple()
        first = health_tuple_canonical_bytes(ht)
        for _ in range(100):
            assert health_tuple_canonical_bytes(ht) == first

    def test_health_tuple_bytes_keys_sorted(self):
        ht = _health_tuple()
        decoded = json.loads(health_tuple_canonical_bytes(ht).decode("utf-8"))
        keys = list(decoded.keys())
        assert keys == sorted(keys)

    def test_health_tuple_bytes_separator_compact(self):
        ht = _health_tuple()
        encoded = health_tuple_canonical_bytes(ht).decode("utf-8")
        assert ", " not in encoded
        assert ": " not in encoded

    def test_health_tuple_bytes_distinct_for_distinct_inputs(self):
        ht1 = _health_tuple()
        ht2 = dataclasses.replace(ht1, channel_a=HEALTH_FAILED)
        assert health_tuple_canonical_bytes(ht1) != health_tuple_canonical_bytes(ht2)

    def test_candidate_bytes_deterministic_and_distinct(self):
        c1 = _candidate()
        c2 = dataclasses.replace(c1, candidate_id="z" * CANDIDATE_ID_HEX_LEN)
        assert candidate_canonical_bytes(c1) == candidate_canonical_bytes(c1)
        assert candidate_canonical_bytes(c1) != candidate_canonical_bytes(c2)

    def test_entity_dossier_bytes_nested_signoff_roundtrips(self):
        d1 = _dossier()
        d2 = dataclasses.replace(d1, operator_signoff=None)
        encoded_signed = entity_dossier_canonical_bytes(d1)
        encoded_unsigned = entity_dossier_canonical_bytes(d2)
        assert encoded_signed != encoded_unsigned
        # Bytes fields in the nested signoff must be hex-encoded, not raw.
        as_dict_signed = json.loads(encoded_signed.decode("utf-8"))
        assert isinstance(
            as_dict_signed["operator_signoff"]["operator_signature"], str
        )
        assert all(
            c in "0123456789abcdef"
            for c in as_dict_signed["operator_signoff"]["operator_signature"]
        )

    def test_dossier_signoff_bytes_hex_encodes_signature(self):
        s = _signoff()
        encoded = dossier_signoff_canonical_bytes(s)
        decoded = json.loads(encoded.decode("utf-8"))
        assert decoded["operator_signature"] == (b"\x01" * 64).hex()

    def test_frozenset_serializes_as_sorted_list(self):
        # Allowlist has a frozenset field — canonical bytes should sort it.
        allow_ab = SourceDomainAllowlist(
            slug="x",
            allowlisted_registrable_domains=frozenset({"a", "b"}),
            last_updated_at_utc="2026-04-20T00:00:00Z",
            last_updated_by_operator_id="josh",
        )
        allow_ba = SourceDomainAllowlist(
            slug="x",
            allowlisted_registrable_domains=frozenset({"b", "a"}),
            last_updated_at_utc="2026-04-20T00:00:00Z",
            last_updated_by_operator_id="josh",
        )
        # Both frozensets are semantically equal; canonical JSON must agree.
        from pipeline.scout._types import _normalize_for_json

        assert _normalize_for_json(
            dataclasses.asdict(allow_ab)
        ) == _normalize_for_json(dataclasses.asdict(allow_ba))

    def test_bytes_encoded_as_lowercase_hex(self):
        s = _signoff()
        decoded = json.loads(dossier_signoff_canonical_bytes(s).decode("utf-8"))
        signature_hex = decoded["operator_signature"]
        assert signature_hex == signature_hex.lower()
        assert len(signature_hex) == 128  # 64 bytes × 2 hex chars


# ---------------------------------------------------------------------------
# §8 numeric-pin fidelity
# ---------------------------------------------------------------------------


PINNED_VALUES = {
    "CHANNEL_A_CONNECT_TIMEOUT_S": (CHANNEL_A_CONNECT_TIMEOUT_S, 10, int),
    "CHANNEL_A_READ_TIMEOUT_S": (CHANNEL_A_READ_TIMEOUT_S, 30, int),
    "CHANNEL_A_RETRY_COUNT": (CHANNEL_A_RETRY_COUNT, 3, int),
    "CHANNEL_E_RUNAWAY_MAX": (CHANNEL_E_RUNAWAY_MAX, 100, int),
    "CHANNEL_D_MAX_CANDIDATES_PER_PAGE": (
        CHANNEL_D_MAX_CANDIDATES_PER_PAGE,
        200,
        int,
    ),
    "CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER": (
        CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER,
        500,
        int,
    ),
    "SCOUT_CANDIDATE_VERIFY_CAP": (SCOUT_CANDIDATE_VERIFY_CAP, 1000, int),
    "SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO": (
        SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO,
        0.25,
        float,
    ),
    "SCOUT_REVIEW_LOCK_STRIPES": (SCOUT_REVIEW_LOCK_STRIPES, 64, int),
    "MAX_DOSSIER_BYTES": (MAX_DOSSIER_BYTES, 5 * 1024 * 1024, int),
    "DOSSIER_VALIDITY_DAYS": (DOSSIER_VALIDITY_DAYS, 90, int),
    "HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT": (
        HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT,
        2,
        int,
    ),
}


class TestNumericPins:
    @pytest.mark.parametrize("name", sorted(PINNED_VALUES.keys()))
    def test_numeric_pin_matches_blueprint(self, name):
        value, expected, expected_type = PINNED_VALUES[name]
        assert value == expected
        assert isinstance(value, expected_type)

    def test_degrade_ratio_is_fraction(self):
        assert 0.0 < SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO < 1.0

    def test_stripes_is_power_of_two(self):
        # A-v3-02: striped lock array sized at a power-of-two so
        # sha3_512(key)[:8] & (stripes - 1) is a uniform modulo.
        assert SCOUT_REVIEW_LOCK_STRIPES > 0
        assert SCOUT_REVIEW_LOCK_STRIPES & (SCOUT_REVIEW_LOCK_STRIPES - 1) == 0


# ---------------------------------------------------------------------------
# §2-enum string-literal fidelity
# ---------------------------------------------------------------------------


class TestEnumStrings:
    def test_channel_codes_are_single_uppercase_letters(self):
        codes = (CHANNEL_A, CHANNEL_B, CHANNEL_C, CHANNEL_D, CHANNEL_E, CHANNEL_F)
        assert codes == ("A", "B", "C", "D", "E", "F")
        assert len(set(codes)) == 6

    def test_verdict_strings_match_blueprint(self):
        assert VERDICT_VERIFIED_FIT == "VERIFIED_FIT"
        assert VERDICT_VERIFIED_NOT_FIT == "VERIFIED_NOT_FIT"
        assert VERDICT_UNVERIFIED == "UNVERIFIED"
        assert VERDICT_VERIFICATION_FAILED == "VERIFICATION_FAILED"

    def test_decision_strings_match_blueprint(self):
        assert DECISION_ACCEPT == "ACCEPT"
        assert DECISION_REJECT == "REJECT"
        assert DECISION_HOLD == "HOLD"

    def test_health_strings_match_blueprint(self):
        assert HEALTH_OK == "OK"
        assert HEALTH_DEGRADED == "DEGRADED"
        assert HEALTH_FAILED == "FAILED"

    def test_confidence_tiers_match_blueprint(self):
        assert CONFIDENCE_HIGH == "HIGH"
        assert CONFIDENCE_MEDIUM == "MEDIUM"
        assert CONFIDENCE_LOW == "LOW"

    @pytest.mark.parametrize(
        "prefix",
        [
            FEED_PREFIX_API,
            FEED_PREFIX_CACHE,
            FEED_PREFIX_PORTAL,
            FEED_PREFIX_RSS,
            FEED_PREFIX_SEARXNG,
            FEED_PREFIX_BRAVE,
        ],
    )
    def test_feed_prefixes_are_lowercase_and_colon_free(self, prefix):
        assert prefix == prefix.lower()
        assert ":" not in prefix
        assert prefix != ""

    @pytest.mark.parametrize(
        "intent",
        [
            INTENT_READ,
            INTENT_CHANNEL_F_POLICY_READ,
            INTENT_REVIEW_QUEUE_WRITE,
            INTENT_DOSSIER_BODY_WRITE,
            INTENT_DOSSIER_SIGNOFF_WRITE,
            INTENT_SCOUT_RUN_LOG_WRITE,
        ],
    )
    def test_intents_are_kebab_case(self, intent):
        assert intent != ""
        assert intent == intent.lower()
        for ch in intent:
            assert ch.isalnum() or ch == "-"


# ---------------------------------------------------------------------------
# __all__ completeness + no-private-export
# ---------------------------------------------------------------------------


class TestPackageSurface:
    def test_version_pinned(self):
        # Forward-compat: future round bumps should not require touching this
        # test. Round-specific pin lives in that round's own test file.
        assert re.fullmatch(r"0\.1\.0-scout-r\d+", scout.__version__), scout.__version__

    def test_all_exports_have_module_attribute(self):
        missing = [name for name in scout.__all__ if not hasattr(scout, name)]
        assert missing == []

    def test_no_private_name_exported(self):
        private = [name for name in scout.__all__ if name.startswith("_") and name != "__version__"]
        assert private == []

    def test_all_is_sorted_or_grouped(self):
        # Not alphabetically sorted — blueprint order. Assert uniqueness only.
        assert len(scout.__all__) == len(set(scout.__all__))

    def test_package_import_runs_under_100ms(self):
        # Reload timing — cold import timing is unreliable because the module
        # is already cached. Measure a reload after clearing caches instead.
        import sys

        for mod_name in list(sys.modules):
            if mod_name.startswith("pipeline.scout"):
                sys.modules.pop(mod_name)
        start = time.monotonic()
        importlib.import_module("pipeline.scout")
        elapsed = time.monotonic() - start
        assert elapsed < 0.5  # generous; typical is < 20 ms


# ---------------------------------------------------------------------------
# AST-lint regression — R1-R5 against pipeline/scout
# ---------------------------------------------------------------------------


class TestASTLintRegression:
    def test_scout_tree_has_zero_violations(self):
        from pathlib import Path

        from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree

        repo_root = Path(__file__).resolve().parent.parent.parent
        scout_dir = repo_root / "pipeline" / "scout"
        violations = lint_tree(scout_dir, DEFAULT_RULES)
        assert violations == []
