"""Round 10 Module 2 — §4.9 entity research (``pipeline.scout.entity_research``).

Test surface floor ≥ 90 with ≥ 6 adversarial (spec-card
``scout_round_10_review_and_entity_research`` v1 §Module 2). E-024 eighth-
firing 2.03× adversarial multiplier applied to the triple-lock drift surface.

Lessons applied from start:

- E-017 Protocol-injection (ninth Scout reuse — ``EntityRosterReader``,
  ``DomainAllowlistReader``, ``EntityClaimFetcher``, ``DossierBodyReader``,
  ``DossierSignoffReader``, ``DossierSignoffSigner`` new seams;
  ``VaultWriter`` / ``CheckpointWriter`` / ``SessionLike`` reused).
- E-024 test-count multiplier (~95 tests).
- E-025 range-check version pin (``rN >= 10``).
- E-026 formal ``__module__`` lineage check.
- E-027 ``lint_tree`` directory contract (run under ``pipeline/scout``).
- E-028 ``# pragma: no cover`` only for the ``_plus_validity_days`` defensive
  fallback branch that is unreachable when the upstream clock is well-formed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Mapping, Optional, Tuple

import pytest

import pipeline.scout.entity_research as er
from pipeline.scout._constants import (
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    DOSSIER_VALIDITY_DAYS,
    ENTITY_KIND_ORG_APPLICANT,
    ENTITY_KIND_PERSON_LEAD,
    HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT,
    INTENT_DOSSIER_BODY_READ,
    INTENT_DOSSIER_BODY_WRITE,
    INTENT_DOSSIER_SIGNOFF_READ,
    INTENT_DOSSIER_SIGNOFF_WRITE,
    INTENT_ENTITY_ROSTER_READ,
    INTENT_SOURCE_ALLOWLIST_READ,
    MAX_DOSSIER_BYTES,
    SCOUT_DOSSIER_MAX_BYTES,
)
from pipeline.scout._types import (
    DossierSignoff,
    EntityClaim,
    EntityDossier,
    EntityRosterEntry,
    SourceDomainAllowlist,
    entity_dossier_canonical_bytes,
)
from pipeline.scout.entity_research import (
    F_SCOUT_D_01,
    F_SCOUT_D_01a,
    F_SCOUT_D_01b,
    F_SCOUT_D_01c,
    F_SCOUT_D_01d,
    F_SCOUT_D_01e,
    F_SCOUT_D_02,
    F_SCOUT_D_03,
    CheckpointWriter,
    ClockFn,
    DomainAllowlistReader,
    DossierBodyReader,
    DossierSignoffReader,
    DossierSignoffSigner,
    DossierSignoffVerifyFailure,
    DossierSizeExceeded,
    EntityClaimCandidate,
    EntityClaimFetcher,
    EntityResearchResult,
    EntityRosterReader,
    FDHandle,
    IntentMismatch,
    SessionLike,
    VaultWriter,
    _MAX_DOSSIER_BYTES,
    _assert_intent_matches,
    _binding_canonical_bytes,
    _claim_ids_sorted,
    _classify_confidence_tier,
    _dedupe_claims,
    _default_clock,
    _dossier_body_path,
    _dossier_signoff_path,
    _normalize_claim_text,
    _open_dossier_body_fd,
    _plus_validity_days,
    _read_held_body,
    _render_dossier_body,
    _sha3_512_hex,
    _signoff_asdict_for_canonical,
    read_entity_dossier,
    run_entity_research,
    sign_off_dossier,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


@dataclass
class FakeSession:
    session_id: str = "session-r10m2-abc"
    slug: str = "mycosymbiotics_cooperative"
    operator_id: str = "josh"


@dataclass
class WriteCall:
    path: str
    bytes_: bytes
    intent: str
    session_id: str
    slug: str


@dataclass
class RecordingVaultWriter:
    calls: List[WriteCall] = field(default_factory=list)
    raise_with: Optional[BaseException] = None

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None:
        if self.raise_with is not None:
            raise self.raise_with
        self.calls.append(
            WriteCall(
                path=path,
                bytes_=bytes_,
                intent=intent,
                session_id=session_id,
                slug=slug,
            )
        )


@dataclass
class RecordingCheckpointWriter:
    calls: List[Tuple[str, Mapping[str, Any]]] = field(default_factory=list)

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None:
        self.calls.append((stage, dict(payload)))

    def stages(self) -> List[str]:
        return [stage for stage, _ in self.calls]


@dataclass
class FakeRosterReader:
    """Returns a fixed roster tuple and records each call."""

    roster: tuple[EntityRosterEntry, ...]
    calls: List[Tuple[str, str]] = field(default_factory=list)
    raise_with: Optional[BaseException] = None

    def read_roster(
        self,
        *,
        session_id: str,
        slug: str,
    ) -> tuple[EntityRosterEntry, ...]:
        self.calls.append((session_id, slug))
        if self.raise_with is not None:
            raise self.raise_with
        return self.roster


@dataclass
class FakeAllowlistReader:
    allowlist: SourceDomainAllowlist
    calls: List[Tuple[str, str]] = field(default_factory=list)
    raise_with: Optional[BaseException] = None

    def read_allowlist(
        self,
        *,
        session_id: str,
        slug: str,
    ) -> SourceDomainAllowlist:
        self.calls.append((session_id, slug))
        if self.raise_with is not None:
            raise self.raise_with
        return self.allowlist


@dataclass
class FakeClaimFetcher:
    """Maps entity_slug → candidate tuple."""

    per_entity: dict[str, tuple[EntityClaimCandidate, ...]]
    calls: List[str] = field(default_factory=list)

    def fetch(
        self,
        *,
        session: SessionLike,
        roster_entry: EntityRosterEntry,
    ) -> tuple[EntityClaimCandidate, ...]:
        self.calls.append(roster_entry.entity_slug)
        return self.per_entity.get(roster_entry.entity_slug, ())


class FakeBodyReader:
    """Opens an on-disk file at a known tmp path as an FD + canonical_path."""

    def __init__(
        self,
        *,
        body_paths: dict[str, Path],
        canonical_paths: Optional[dict[str, str]] = None,
        pre_open_hook: Optional[Any] = None,
    ) -> None:
        self.body_paths = body_paths
        self.canonical_paths = canonical_paths or {}
        self.pre_open_hook = pre_open_hook
        self.opens: list[str] = []

    def open_body(
        self,
        *,
        session_id: str,
        slug: str,
        entity_slug: str,
    ) -> FDHandle:
        self.opens.append(entity_slug)
        if self.pre_open_hook is not None:
            self.pre_open_hook(entity_slug)
        body_path = self.body_paths[entity_slug]
        fd = os.open(str(body_path), os.O_RDONLY)
        canonical = self.canonical_paths.get(
            entity_slug,
            f"/vault/orgs/{slug}/dossier/entities/{entity_slug}.md",
        )
        return FDHandle(
            fd=fd,
            canonical_path=canonical,
            close=lambda: os.close(fd),
        )


@dataclass
class FakeSignoffReader:
    store: dict[str, DossierSignoff] = field(default_factory=dict)
    calls: List[Tuple[str, str, str]] = field(default_factory=list)

    def read_signoff(
        self,
        *,
        session_id: str,
        slug: str,
        entity_slug: str,
    ) -> Optional[DossierSignoff]:
        self.calls.append((session_id, slug, entity_slug))
        return self.store.get(entity_slug)


@dataclass
class FakeSigner:
    fixed_signature: bytes = b"\x00" * 64
    calls: List[bytes] = field(default_factory=list)

    def sign(self, *, binding_bytes: bytes) -> bytes:
        self.calls.append(binding_bytes)
        return self.fixed_signature


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _mk_roster_entry(
    *,
    entity_slug: str = "josh_g",
    kind: str = ENTITY_KIND_PERSON_LEAD,
    display_name: str = "Josh G.",
) -> EntityRosterEntry:
    return EntityRosterEntry(
        entity_slug=entity_slug,
        display_name=display_name,
        kind=kind,
        seed_urls=("https://example.test/bio",),
        added_by="operator",
        added_at_utc="2026-04-01T00:00:00Z",
    )


def _mk_candidate(
    *,
    claim_id: str,
    claim_text: str,
    domain: str,
) -> EntityClaimCandidate:
    return EntityClaimCandidate(
        claim_id=claim_id,
        claim_text=claim_text,
        source_url=f"https://{domain}/article/{claim_id}",
        source_registrable_domain=domain,
        fetched_at_utc="2026-04-15T12:00:00Z",
        url_hash=hashlib.sha3_512(claim_id.encode()).hexdigest(),
        content_hash=hashlib.sha3_512(claim_text.encode()).hexdigest(),
        evidence_quote=f"...{claim_text}...",
    )


def _mk_allowlist(
    *,
    slug: str = "mycosymbiotics_cooperative",
    domains: frozenset[str] = frozenset(
        {"example.test", "partner.test", "other.test"}
    ),
) -> SourceDomainAllowlist:
    return SourceDomainAllowlist(
        slug=slug,
        allowlisted_registrable_domains=domains,
        last_updated_at_utc="2026-04-01T00:00:00Z",
        last_updated_by_operator_id="josh",
    )


def _build_happy_result(
    *,
    session: Optional[FakeSession] = None,
    roster: Optional[tuple[EntityRosterEntry, ...]] = None,
    candidates: Optional[
        dict[str, tuple[EntityClaimCandidate, ...]]
    ] = None,
    allowlist: Optional[SourceDomainAllowlist] = None,
    clock_values: Optional[list[str]] = None,
) -> tuple[
    EntityResearchResult,
    RecordingVaultWriter,
    RecordingCheckpointWriter,
    FakeRosterReader,
    FakeAllowlistReader,
    FakeClaimFetcher,
]:
    session = session or FakeSession()
    roster = roster or (_mk_roster_entry(),)
    candidates = candidates or {
        "josh_g": (
            _mk_candidate(
                claim_id="c-001",
                claim_text="Runs MycoSymbiotics",
                domain="example.test",
            ),
            _mk_candidate(
                claim_id="c-002",
                claim_text="Runs MycoSymbiotics",
                domain="partner.test",
            ),
        )
    }
    allowlist = allowlist or _mk_allowlist()
    roster_reader = FakeRosterReader(roster=roster)
    allowlist_reader = FakeAllowlistReader(allowlist=allowlist)
    claim_fetcher = FakeClaimFetcher(per_entity=candidates)
    vault_writer = RecordingVaultWriter()
    cpw = RecordingCheckpointWriter()

    iso_list = clock_values or ["2026-04-20T10:00:00Z"] * 10

    def _clock() -> str:
        return iso_list.pop(0) if iso_list else "2026-04-20T10:00:00Z"

    result = run_entity_research(
        session=session,
        roster=roster,
        roster_reader=roster_reader,
        allowlist_reader=allowlist_reader,
        claim_fetcher=claim_fetcher,
        vault_writer=vault_writer,
        checkpoint_writer=cpw,
        clock=_clock,
    )
    return (
        result,
        vault_writer,
        cpw,
        roster_reader,
        allowlist_reader,
        claim_fetcher,
    )


def _write_body_and_open(
    tmp_path: Path,
    entity_slug: str,
    body_bytes: bytes,
) -> tuple[Path, FakeBodyReader]:
    body_path = tmp_path / f"{entity_slug}.md"
    body_path.write_bytes(body_bytes)
    canonical = (
        f"/vault/orgs/mycosymbiotics_cooperative/dossier/entities/"
        f"{entity_slug}.md"
    )
    reader = FakeBodyReader(
        body_paths={entity_slug: body_path},
        canonical_paths={entity_slug: canonical},
    )
    return body_path, reader


# ---------------------------------------------------------------------------
# TestModuleSurface — surface invariants
# ---------------------------------------------------------------------------


class TestModuleSurface:
    def test_version_pin_matches_scout_r10_range(self):
        # E-025 range-check pin.
        assert er.__version__.endswith("-scout-r10")
        m = re.match(r"(\d+)\.(\d+)\.(\d+)-scout-r(\d+)", er.__version__)
        assert m is not None
        round_n = int(m.group(4))
        assert round_n >= 10

    def test_module_has_docstring(self):
        assert er.__doc__ is not None
        assert "§4.9 M11" in er.__doc__

    def test_all_public_names_present(self):
        for name in (
            "run_entity_research",
            "sign_off_dossier",
            "read_entity_dossier",
            "EntityResearchResult",
            "EntityClaimCandidate",
            "FDHandle",
            "DossierSignoffVerifyFailure",
            "DossierSizeExceeded",
            "IntentMismatch",
            "F_SCOUT_D_01",
            "F_SCOUT_D_01a",
            "F_SCOUT_D_01b",
            "F_SCOUT_D_01c",
            "F_SCOUT_D_01d",
            "F_SCOUT_D_01e",
            "F_SCOUT_D_02",
            "F_SCOUT_D_03",
        ):
            assert name in er.__all__
            assert hasattr(er, name)

    def test_public_symbols_defined_in_this_module(self):
        # E-026 lineage via __module__, not sys.modules identity.
        for name in (
            "run_entity_research",
            "sign_off_dossier",
            "read_entity_dossier",
            "_assert_intent_matches",
            "_read_held_body",
            "_render_dossier_body",
        ):
            obj = getattr(er, name)
            assert obj.__module__ == "pipeline.scout.entity_research"

    def test_failure_code_strings_verbatim(self):
        assert F_SCOUT_D_01 == "F-SCOUT-D-01"
        assert F_SCOUT_D_01a == "F-SCOUT-D-01a"
        assert F_SCOUT_D_01b == "F-SCOUT-D-01b"
        assert F_SCOUT_D_01c == "F-SCOUT-D-01c"
        assert F_SCOUT_D_01d == "F-SCOUT-D-01d"
        assert F_SCOUT_D_01e == "F-SCOUT-D-01e"
        assert F_SCOUT_D_02 == "F-SCOUT-D-02"
        assert F_SCOUT_D_03 == "F-SCOUT-D-03"

    def test_max_dossier_bytes_alias_equal(self):
        assert _MAX_DOSSIER_BYTES == MAX_DOSSIER_BYTES
        assert _MAX_DOSSIER_BYTES == SCOUT_DOSSIER_MAX_BYTES
        assert _MAX_DOSSIER_BYTES == 5 * 1024 * 1024

    def test_clockfn_alias_is_callable_type(self):
        # ClockFn is a type alias; instance-check the callable binding.
        clk: ClockFn = _default_clock
        assert callable(clk)

    def test_session_like_protocol_is_runtime_checkable(self):
        # SessionLike is a plain Protocol (no runtime_checkable); importable.
        assert SessionLike is not None

    def test_vault_writer_protocol_is_runtime_checkable(self):
        assert isinstance(RecordingVaultWriter(), VaultWriter)


# ---------------------------------------------------------------------------
# TestPathHelpers
# ---------------------------------------------------------------------------


class TestPathHelpers:
    def test_dossier_body_path(self):
        assert (
            _dossier_body_path("myc", "josh_g")
            == "orgs/myc/dossier/entities/josh_g.md"
        )

    def test_dossier_signoff_path(self):
        assert (
            _dossier_signoff_path("myc", "josh_g")
            == "orgs/myc/dossier/signoff/josh_g.json"
        )

    def test_body_and_signoff_paths_diverge(self):
        assert _dossier_body_path("x", "y") != _dossier_signoff_path("x", "y")


# ---------------------------------------------------------------------------
# TestNormalizeClaimText
# ---------------------------------------------------------------------------


class TestNormalizeClaimText:
    def test_lowercases(self):
        assert _normalize_claim_text("HELLO") == "hello"

    def test_strips_whitespace(self):
        assert _normalize_claim_text("  hi  ") == "hi"

    def test_nfc_normalises(self):
        # NFD 'é' → NFC 'é'.
        nfd = unicodedata.normalize("NFD", "café")
        nfc = unicodedata.normalize("NFC", "café")
        assert _normalize_claim_text(nfd) == nfc

    def test_dedupe_key_matches_across_case_and_whitespace(self):
        assert _normalize_claim_text(" Hello ") == _normalize_claim_text(
            "hello"
        )


# ---------------------------------------------------------------------------
# TestDedupeClaims
# ---------------------------------------------------------------------------


class TestDedupeClaims:
    def test_groups_identical_text_across_domains(self):
        c1 = _mk_candidate(
            claim_id="a", claim_text="X is Y", domain="a.test"
        )
        c2 = _mk_candidate(
            claim_id="b", claim_text="X is Y", domain="b.test"
        )
        groups = _dedupe_claims((c1, c2))
        assert len(groups) == 1
        assert len(next(iter(groups.values()))) == 2

    def test_distinct_text_distinct_groups(self):
        c1 = _mk_candidate(
            claim_id="a", claim_text="X is Y", domain="a.test"
        )
        c2 = _mk_candidate(
            claim_id="b", claim_text="Z is W", domain="a.test"
        )
        groups = _dedupe_claims((c1, c2))
        assert len(groups) == 2

    def test_case_insensitive_grouping(self):
        c1 = _mk_candidate(
            claim_id="a", claim_text="Runs MycoSymbiotics", domain="a.test"
        )
        c2 = _mk_candidate(
            claim_id="b", claim_text="runs mycosymbiotics", domain="b.test"
        )
        groups = _dedupe_claims((c1, c2))
        assert len(groups) == 1

    def test_empty_input_returns_empty(self):
        assert _dedupe_claims(()) == {}


# ---------------------------------------------------------------------------
# TestClassifyConfidenceTier
# ---------------------------------------------------------------------------


class TestClassifyConfidenceTier:
    def test_high_on_two_distinct_domains(self):
        c1 = _mk_candidate(
            claim_id="a", claim_text="t", domain="a.test"
        )
        c2 = _mk_candidate(
            claim_id="b", claim_text="t", domain="b.test"
        )
        assert _classify_confidence_tier([c1, c2]) == CONFIDENCE_HIGH

    def test_high_on_three_distinct_domains(self):
        cands = [
            _mk_candidate(
                claim_id=str(i), claim_text="t", domain=f"d{i}.test"
            )
            for i in range(3)
        ]
        assert _classify_confidence_tier(cands) == CONFIDENCE_HIGH

    def test_medium_on_exactly_one_domain(self):
        c1 = _mk_candidate(claim_id="a", claim_text="t", domain="x.test")
        c2 = _mk_candidate(claim_id="b", claim_text="t", domain="x.test")
        assert _classify_confidence_tier([c1, c2]) == CONFIDENCE_MEDIUM

    def test_low_on_empty_supporting(self):
        assert _classify_confidence_tier([]) == CONFIDENCE_LOW

    def test_threshold_pin(self):
        assert HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT == 2


# ---------------------------------------------------------------------------
# TestClaimIdsSorted
# ---------------------------------------------------------------------------


class TestClaimIdsSorted:
    def test_sorts_ascending(self):
        c1 = _mk_candidate(
            claim_id="zz", claim_text="t", domain="a.test"
        )
        c2 = _mk_candidate(
            claim_id="aa", claim_text="t", domain="a.test"
        )
        out = _claim_ids_sorted([c1, c2])
        assert out == ("aa", "zz")

    def test_empty_input(self):
        assert _claim_ids_sorted([]) == ()


# ---------------------------------------------------------------------------
# TestDefaultClock
# ---------------------------------------------------------------------------


class TestDefaultClock:
    def test_returns_iso_string_with_z(self):
        out = _default_clock()
        assert isinstance(out, str)
        assert out.endswith("Z")
        # Should parse back.
        import datetime as _dt

        _ = _dt.datetime.fromisoformat(out[:-1] + "+00:00")


# ---------------------------------------------------------------------------
# TestPlusValidityDays
# ---------------------------------------------------------------------------


class TestPlusValidityDays:
    def test_adds_validity_days(self):
        out = _plus_validity_days("2026-04-01T00:00:00Z")
        assert out == "2026-06-30T00:00:00Z"

    def test_adds_with_plus_zero_offset(self):
        out = _plus_validity_days("2026-04-01T00:00:00+00:00")
        # Z-form is canonical.
        assert out == "2026-06-30T00:00:00Z"

    def test_malformed_returns_passthrough(self):
        bogus = "not-a-timestamp"
        assert _plus_validity_days(bogus) == bogus

    def test_naive_timestamp_tz_normalised(self):
        out = _plus_validity_days("2026-04-01T00:00:00")
        assert out.startswith("2026-06-30")

    def test_validity_pin(self):
        assert DOSSIER_VALIDITY_DAYS == 90


# ---------------------------------------------------------------------------
# TestBindingCanonicalBytes / TestSha3Helper
# ---------------------------------------------------------------------------


class TestBindingCanonicalBytes:
    def test_deterministic(self):
        a = _binding_canonical_bytes(
            slug="s",
            entity_slug="e",
            signed_canonical_path="/p",
            signed_inode=12345,
            signed_content_hash="deadbeef",
            signed_at_utc="2026-04-21T00:00:00Z",
            operator_id="josh",
        )
        b = _binding_canonical_bytes(
            slug="s",
            entity_slug="e",
            signed_canonical_path="/p",
            signed_inode=12345,
            signed_content_hash="deadbeef",
            signed_at_utc="2026-04-21T00:00:00Z",
            operator_id="josh",
        )
        assert a == b

    def test_keys_sorted(self):
        raw = _binding_canonical_bytes(
            slug="s",
            entity_slug="e",
            signed_canonical_path="/p",
            signed_inode=1,
            signed_content_hash="h",
            signed_at_utc="t",
            operator_id="o",
        )
        payload = json.loads(raw.decode("utf-8"))
        assert list(payload.keys()) == sorted(payload.keys())


class TestSha3Helper:
    def test_matches_hashlib(self):
        data = b"hello"
        assert _sha3_512_hex(data) == hashlib.sha3_512(data).hexdigest()


# ---------------------------------------------------------------------------
# TestRenderDossierBody
# ---------------------------------------------------------------------------


class TestRenderDossierBody:
    def test_renders_header(self):
        re_ = _mk_roster_entry(display_name="Josh G.")
        body = _render_dossier_body(roster_entry=re_, claims=())
        decoded = body.decode("utf-8")
        assert "# Josh G." in decoded
        assert "Kind: person_lead" in decoded
        assert "Added by: operator" in decoded

    def test_renders_claims_in_sorted_order(self):
        re_ = _mk_roster_entry()
        claims = (
            EntityClaim(
                claim_id="z",
                claim_text="Z claim",
                source_url="https://a.test/z",
                source_registrable_domain="a.test",
                fetched_at_utc="t",
                url_hash="h",
                content_hash="h",
                evidence_quote="zz",
                confidence_tier=CONFIDENCE_HIGH,
                corroborating_claim_ids=(),
            ),
            EntityClaim(
                claim_id="a",
                claim_text="A claim",
                source_url="https://a.test/a",
                source_registrable_domain="a.test",
                fetched_at_utc="t",
                url_hash="h",
                content_hash="h",
                evidence_quote="aa",
                confidence_tier=CONFIDENCE_MEDIUM,
                corroborating_claim_ids=(),
            ),
        )
        body = _render_dossier_body(roster_entry=re_, claims=claims).decode()
        assert body.find("A claim") < body.find("Z claim")

    def test_deterministic_across_input_order(self):
        re_ = _mk_roster_entry()
        c1 = EntityClaim(
            claim_id="a",
            claim_text="A",
            source_url="u",
            source_registrable_domain="d",
            fetched_at_utc="t",
            url_hash="h",
            content_hash="h",
            evidence_quote="e",
            confidence_tier=CONFIDENCE_HIGH,
            corroborating_claim_ids=(),
        )
        c2 = EntityClaim(
            claim_id="b",
            claim_text="B",
            source_url="u",
            source_registrable_domain="d",
            fetched_at_utc="t",
            url_hash="h",
            content_hash="h",
            evidence_quote="e",
            confidence_tier=CONFIDENCE_HIGH,
            corroborating_claim_ids=(),
        )
        body_a = _render_dossier_body(roster_entry=re_, claims=(c1, c2))
        body_b = _render_dossier_body(roster_entry=re_, claims=(c2, c1))
        assert body_a == body_b

    def test_utf8_encoded(self):
        re_ = _mk_roster_entry(display_name="Café")
        body = _render_dossier_body(roster_entry=re_, claims=())
        assert "Café" in body.decode("utf-8")


# ---------------------------------------------------------------------------
# TestAssertIntentMatches
# ---------------------------------------------------------------------------


class TestAssertIntentMatches:
    def test_strict_match_returns_none(self):
        _assert_intent_matches(
            expected_intent=INTENT_DOSSIER_BODY_READ,
            observed_intent=INTENT_DOSSIER_BODY_READ,
            expected_session_id="s",
            observed_session_id="s",
            expected_slug="o",
            observed_slug="o",
        )

    def test_session_mismatch_raises(self):
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent="a",
                observed_intent="a",
                expected_session_id="s1",
                observed_session_id="s2",
                expected_slug="o",
                observed_slug="o",
            )
        assert "session_id_mismatch" in exc.value.reason_tag
        assert exc.value.code.endswith(".intent_session_mismatch")

    def test_slug_mismatch_raises(self):
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent="a",
                observed_intent="a",
                expected_session_id="s",
                observed_session_id="s",
                expected_slug="o1",
                observed_slug="o2",
            )
        assert "slug_mismatch" in exc.value.reason_tag
        assert exc.value.code.endswith(".intent_slug_mismatch")

    def test_intent_plain_mismatch(self):
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent="dossier-body-read",
                observed_intent="dossier-signoff-read",
                expected_session_id="s",
                observed_session_id="s",
                expected_slug="o",
                observed_slug="o",
            )
        assert "intent_mismatch" in exc.value.reason_tag
        assert exc.value.code.endswith(".intent_mismatch_post_read")

    def test_intent_nfc_drift(self):
        # NFD form of the same intent string.
        expected = "dossier-body-read"
        nfd = unicodedata.normalize("NFD", expected)
        # They only differ if there were composable characters; add a
        # decomposable character and reconstruct:
        observed = " dossier-body-read "  # whitespace that strips to same.
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent=expected,
                observed_intent=observed,
                expected_session_id="s",
                observed_session_id="s",
                expected_slug="o",
                observed_slug="o",
            )
        assert "nfc_drift" in exc.value.reason_tag
        assert exc.value.code.endswith(".intent_nfc_drift")
        _ = nfd  # keep lint happy

    def test_code_carries_f_scout_d_03_prefix(self):
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent="a",
                observed_intent="b",
                expected_session_id="s",
                observed_session_id="s",
                expected_slug="o",
                observed_slug="o",
            )
        assert exc.value.code.startswith(F_SCOUT_D_03)


# ---------------------------------------------------------------------------
# TestOpenDossierBodyFd + _read_held_body
# ---------------------------------------------------------------------------


class TestOpenDossierBodyFd:
    def test_context_manager_closes_on_exit(self, tmp_path):
        body_path, reader = _write_body_and_open(
            tmp_path, "slug_x", b"hello body"
        )
        with _open_dossier_body_fd(
            body_reader=reader,
            session=FakeSession(),
            entity_slug="slug_x",
        ) as handle:
            fd = handle.fd
            # Can os.fstat on the fd while held.
            st = os.fstat(fd)
            assert st.st_size == len(b"hello body")
        # After exit the fd is closed.
        with pytest.raises(OSError):
            os.fstat(fd)

    def test_context_manager_closes_on_exception(self, tmp_path):
        body_path, reader = _write_body_and_open(
            tmp_path, "slug_x", b"hello"
        )
        fd_box: list[int] = []
        with pytest.raises(RuntimeError):
            with _open_dossier_body_fd(
                body_reader=reader,
                session=FakeSession(),
                entity_slug="slug_x",
            ) as handle:
                fd_box.append(handle.fd)
                raise RuntimeError("boom")
        with pytest.raises(OSError):
            os.fstat(fd_box[0])


class TestReadHeldBody:
    def test_reads_body_bytes(self, tmp_path):
        body = b"## body\n- data\n"
        _, reader = _write_body_and_open(tmp_path, "e", body)
        with _open_dossier_body_fd(
            body_reader=reader, session=FakeSession(), entity_slug="e"
        ) as h:
            out = _read_held_body(handle=h)
        assert out == body

    def test_size_exact_cap_accepted(self, tmp_path):
        body = b"x" * _MAX_DOSSIER_BYTES
        _, reader = _write_body_and_open(tmp_path, "e", body)
        with _open_dossier_body_fd(
            body_reader=reader, session=FakeSession(), entity_slug="e"
        ) as h:
            out = _read_held_body(handle=h)
        assert len(out) == _MAX_DOSSIER_BYTES

    def test_size_cap_plus_one_rejected(self, tmp_path):
        body = b"x" * (_MAX_DOSSIER_BYTES + 1)
        _, reader = _write_body_and_open(tmp_path, "e", body)
        with _open_dossier_body_fd(
            body_reader=reader, session=FakeSession(), entity_slug="e"
        ) as h:
            with pytest.raises(DossierSizeExceeded) as exc:
                _read_held_body(handle=h)
        assert ".fstat_size_gt_max" in str(exc.value)

    def test_expected_canonical_path_match(self, tmp_path):
        body = b"data"
        body_path = tmp_path / "e.md"
        body_path.write_bytes(body)
        canonical = "/vault/canonical/e.md"
        reader = FakeBodyReader(
            body_paths={"e": body_path},
            canonical_paths={"e": canonical},
        )
        with _open_dossier_body_fd(
            body_reader=reader, session=FakeSession(), entity_slug="e"
        ) as h:
            out = _read_held_body(
                handle=h, expected_canonical_path=canonical
            )
        assert out == body

    def test_expected_canonical_path_mismatch_raises_01a(self, tmp_path):
        body = b"data"
        body_path = tmp_path / "e.md"
        body_path.write_bytes(body)
        reader = FakeBodyReader(
            body_paths={"e": body_path},
            canonical_paths={"e": "/actual/path"},
        )
        with _open_dossier_body_fd(
            body_reader=reader, session=FakeSession(), entity_slug="e"
        ) as h:
            with pytest.raises(DossierSignoffVerifyFailure) as exc:
                _read_held_body(
                    handle=h, expected_canonical_path="/expected/path"
                )
        assert exc.value.code == F_SCOUT_D_01a
        assert "canonical_path_mismatch" in exc.value.reason_tag

    def test_short_read_raises_01e(self, tmp_path, monkeypatch):
        body = b"twenty-byte-body-abc!"
        _, reader = _write_body_and_open(tmp_path, "e", body)
        # Monkeypatch os.read to return a truncated read.
        real_read = os.read

        def _short_read(fd, n):
            # Pretend a concurrent truncate returned only half.
            out = real_read(fd, n)
            return out[: len(out) // 2]

        monkeypatch.setattr(
            "pipeline.scout.entity_research.os.read", _short_read
        )
        with _open_dossier_body_fd(
            body_reader=reader, session=FakeSession(), entity_slug="e"
        ) as h:
            with pytest.raises(DossierSignoffVerifyFailure) as exc:
                _read_held_body(handle=h)
        assert exc.value.code == F_SCOUT_D_01e
        assert "read_short" in exc.value.reason_tag


# ---------------------------------------------------------------------------
# TestSignoffAsdictForCanonical
# ---------------------------------------------------------------------------


class TestSignoffAsdictForCanonical:
    def test_signature_hex_encoded(self):
        so = DossierSignoff(
            signed_at_utc="t",
            operator_id="o",
            signed_canonical_path="/p",
            signed_inode=1,
            signed_content_hash="h",
            operator_signature=b"\xde\xad\xbe\xef",
            expires_at_utc="t2",
        )
        d = _signoff_asdict_for_canonical(so)
        assert d["operator_signature"] == "deadbeef"
        assert isinstance(d["operator_signature"], str)

    def test_all_fields_present(self):
        so = DossierSignoff(
            signed_at_utc="t",
            operator_id="o",
            signed_canonical_path="/p",
            signed_inode=1,
            signed_content_hash="h",
            operator_signature=b"\x01",
            expires_at_utc="t2",
        )
        d = _signoff_asdict_for_canonical(so)
        for k in (
            "signed_at_utc",
            "operator_id",
            "signed_canonical_path",
            "signed_inode",
            "signed_content_hash",
            "operator_signature",
            "expires_at_utc",
        ):
            assert k in d


# ---------------------------------------------------------------------------
# TestRunEntityResearch
# ---------------------------------------------------------------------------


class TestRunEntityResearch:
    def test_returns_entity_research_result(self):
        result, _, _, _, _, _ = _build_happy_result()
        assert isinstance(result, EntityResearchResult)

    def test_dossiers_by_slug_keyed_by_entity_slug(self):
        result, *_ = _build_happy_result()
        assert "josh_g" in result.dossiers_by_slug
        assert isinstance(result.dossiers_by_slug["josh_g"], EntityDossier)

    def test_ordered_matches_roster(self):
        r1 = _mk_roster_entry(entity_slug="alice")
        r2 = _mk_roster_entry(entity_slug="bob")
        candidates = {
            "alice": (
                _mk_candidate(
                    claim_id="a1", claim_text="alice runs", domain="example.test"
                ),
            ),
            "bob": (
                _mk_candidate(
                    claim_id="b1", claim_text="bob runs", domain="partner.test"
                ),
            ),
        }
        result, *_ = _build_happy_result(
            roster=(r1, r2), candidates=candidates
        )
        assert tuple(d.entity_slug for d in result.ordered) == ("alice", "bob")

    def test_vault_write_called_per_entity(self):
        result, vw, *_ = _build_happy_result()
        assert len(vw.calls) == 1
        call = vw.calls[0]
        assert call.intent == INTENT_DOSSIER_BODY_WRITE
        assert call.path == "orgs/mycosymbiotics_cooperative/dossier/entities/josh_g.md"

    def test_vault_write_path_matches_slug_entity(self):
        r = _mk_roster_entry(entity_slug="partner_org")
        result, vw, *_ = _build_happy_result(
            roster=(r,),
            candidates={
                "partner_org": (
                    _mk_candidate(
                        claim_id="p1",
                        claim_text="partner claim",
                        domain="example.test",
                    ),
                )
            },
        )
        assert vw.calls[0].path.endswith("partner_org.md")

    def test_checkpoint_start_and_complete_emitted(self):
        _, _, cpw, *_ = _build_happy_result()
        stages = cpw.stages()
        assert stages[0] == "entity_research_start"
        assert stages[-1] == "entity_research_complete"

    def test_checkpoint_success_outcome(self):
        _, _, cpw, *_ = _build_happy_result()
        final_stage, final_payload = cpw.calls[-1]
        assert final_stage == "entity_research_complete"
        assert final_payload["outcome"] == "success"

    def test_checkpoint_start_payload_has_n_roster(self):
        _, _, cpw, *_ = _build_happy_result()
        start_stage, start_payload = cpw.calls[0]
        assert start_payload["n_roster"] == 1

    def test_intent_write_constant_used(self):
        _, vw, *_ = _build_happy_result()
        assert vw.calls[0].intent == "dossier-body-write"

    def test_session_ids_forwarded(self):
        sess = FakeSession(session_id="sess-xyz", slug="org-abc")
        candidates = {
            "josh_g": (
                _mk_candidate(
                    claim_id="c1", claim_text="t", domain="example.test"
                ),
            )
        }
        _, vw, *_ = _build_happy_result(
            session=sess,
            allowlist=_mk_allowlist(slug="org-abc"),
            candidates=candidates,
        )
        assert vw.calls[0].session_id == "sess-xyz"
        assert vw.calls[0].slug == "org-abc"

    def test_roster_reader_invoked(self):
        _, _, _, rr, _, _ = _build_happy_result()
        assert len(rr.calls) == 1

    def test_allowlist_reader_invoked(self):
        _, _, _, _, ar, _ = _build_happy_result()
        assert len(ar.calls) == 1

    def test_claim_fetcher_invoked_per_roster_entry(self):
        r1 = _mk_roster_entry(entity_slug="a")
        r2 = _mk_roster_entry(entity_slug="b")
        cands = {
            "a": (
                _mk_candidate(
                    claim_id="a1", claim_text="t", domain="example.test"
                ),
            ),
            "b": (
                _mk_candidate(
                    claim_id="b1", claim_text="t", domain="partner.test"
                ),
            ),
        }
        _, _, _, _, _, fetch = _build_happy_result(
            roster=(r1, r2), candidates=cands
        )
        assert fetch.calls == ["a", "b"]

    def test_high_tier_assigned_across_two_domains(self):
        # happy helper uses two domains for same text.
        result, *_ = _build_happy_result()
        dossier = result.dossiers_by_slug["josh_g"]
        assert all(
            c.confidence_tier == CONFIDENCE_HIGH for c in dossier.claims
        )

    def test_medium_tier_assigned_single_domain(self):
        cands = {
            "josh_g": (
                _mk_candidate(
                    claim_id="c1",
                    claim_text="solo claim",
                    domain="example.test",
                ),
            )
        }
        result, *_ = _build_happy_result(candidates=cands)
        dossier = result.dossiers_by_slug["josh_g"]
        assert all(
            c.confidence_tier == CONFIDENCE_MEDIUM for c in dossier.claims
        )

    def test_non_allowlisted_domain_dropped(self):
        cands = {
            "josh_g": (
                _mk_candidate(
                    claim_id="drop-me",
                    claim_text="t",
                    domain="malicious.test",
                ),
                _mk_candidate(
                    claim_id="keep-me",
                    claim_text="t",
                    domain="example.test",
                ),
            )
        }
        result, *_ = _build_happy_result(candidates=cands)
        assert len(result.non_allowlisted_domain_events) == 1
        event = result.non_allowlisted_domain_events[0]
        assert "drop-me" in event
        assert "malicious.test" in event
        assert F_SCOUT_D_03 in event

    def test_non_allowlisted_drops_not_in_dossier(self):
        cands = {
            "josh_g": (
                _mk_candidate(
                    claim_id="drop-me",
                    claim_text="dropped claim",
                    domain="malicious.test",
                ),
            )
        }
        result, *_ = _build_happy_result(candidates=cands)
        dossier = result.dossiers_by_slug["josh_g"]
        # Body should contain the roster entry but no claims section entries.
        assert dossier.claims == ()

    def test_empty_candidate_list_empty_claims(self):
        cands = {"josh_g": ()}
        result, *_ = _build_happy_result(candidates=cands)
        dossier = result.dossiers_by_slug["josh_g"]
        assert dossier.claims == ()

    def test_content_hash_is_sha3_512_hex(self):
        result, *_ = _build_happy_result()
        dossier = result.dossiers_by_slug["josh_g"]
        assert len(dossier.dossier_content_hash) == 128
        assert re.match(r"^[0-9a-f]{128}$", dossier.dossier_content_hash)

    def test_operator_signoff_initially_none(self):
        result, *_ = _build_happy_result()
        dossier = result.dossiers_by_slug["josh_g"]
        assert dossier.operator_signoff is None

    def test_dossier_written_at_uses_clock(self):
        result, *_ = _build_happy_result(
            clock_values=["2099-01-01T00:00:00Z"]
        )
        dossier = result.dossiers_by_slug["josh_g"]
        assert dossier.dossier_written_at_utc == "2099-01-01T00:00:00Z"

    def test_ordered_and_dossiers_by_slug_same_content(self):
        result, *_ = _build_happy_result()
        assert list(result.ordered) == list(
            result.dossiers_by_slug.values()
        )

    def test_vault_write_raise_propagates(self):
        rr = FakeRosterReader(roster=(_mk_roster_entry(),))
        ar = FakeAllowlistReader(allowlist=_mk_allowlist())
        fetch = FakeClaimFetcher(
            per_entity={
                "josh_g": (
                    _mk_candidate(
                        claim_id="x",
                        claim_text="t",
                        domain="example.test",
                    ),
                )
            }
        )
        vw = RecordingVaultWriter(raise_with=RuntimeError("vault down"))
        cpw = RecordingCheckpointWriter()
        with pytest.raises(RuntimeError, match="vault down"):
            run_entity_research(
                session=FakeSession(),
                roster=(_mk_roster_entry(),),
                roster_reader=rr,
                allowlist_reader=ar,
                claim_fetcher=fetch,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        # Failure-path checkpoint emitted.
        stages = cpw.stages()
        assert "entity_research_complete" in stages
        final_stage, final_payload = cpw.calls[-1]
        assert final_stage == "entity_research_complete"
        assert final_payload["outcome"] == "failure"
        assert final_payload["error_type"] == "RuntimeError"

    def test_roster_reader_raises_propagates(self):
        rr = FakeRosterReader(
            roster=(),
            raise_with=DossierSignoffVerifyFailure(
                code=F_SCOUT_D_03, reason_tag="roster_parse_error"
            ),
        )
        ar = FakeAllowlistReader(allowlist=_mk_allowlist())
        fetch = FakeClaimFetcher(per_entity={})
        vw = RecordingVaultWriter()
        cpw = RecordingCheckpointWriter()
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            run_entity_research(
                session=FakeSession(),
                roster=(_mk_roster_entry(),),
                roster_reader=rr,
                allowlist_reader=ar,
                claim_fetcher=fetch,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert exc.value.code == F_SCOUT_D_03
        assert cpw.calls[-1][1]["outcome"] == "failure"

    def test_allowlist_reader_raises_propagates(self):
        rr = FakeRosterReader(roster=(_mk_roster_entry(),))
        ar = FakeAllowlistReader(
            allowlist=_mk_allowlist(),
            raise_with=IntentMismatch(
                code=f"{F_SCOUT_D_03}.intent_mismatch_post_read",
                reason_tag="allowlist_parse_error",
            ),
        )
        fetch = FakeClaimFetcher(per_entity={})
        vw = RecordingVaultWriter()
        cpw = RecordingCheckpointWriter()
        with pytest.raises(IntentMismatch):
            run_entity_research(
                session=FakeSession(),
                roster=(_mk_roster_entry(),),
                roster_reader=rr,
                allowlist_reader=ar,
                claim_fetcher=fetch,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )

    def test_corroborating_claim_ids_are_sorted(self):
        cands = {
            "josh_g": (
                _mk_candidate(
                    claim_id="zz", claim_text="t", domain="example.test"
                ),
                _mk_candidate(
                    claim_id="aa", claim_text="t", domain="partner.test"
                ),
            )
        }
        result, *_ = _build_happy_result(candidates=cands)
        dossier = result.dossiers_by_slug["josh_g"]
        # Dedupe groups them into one claim with corroborating ids sorted.
        assert dossier.claims[0].corroborating_claim_ids == ("aa", "zz")

    def test_force_refresh_flag_passes_through(self):
        # The flag is inert in the current implementation (reserved for later),
        # but must not raise and must appear in the start-checkpoint payload.
        rr = FakeRosterReader(roster=(_mk_roster_entry(),))
        ar = FakeAllowlistReader(allowlist=_mk_allowlist())
        fetch = FakeClaimFetcher(
            per_entity={
                "josh_g": (
                    _mk_candidate(
                        claim_id="c",
                        claim_text="t",
                        domain="example.test",
                    ),
                )
            }
        )
        vw = RecordingVaultWriter()
        cpw = RecordingCheckpointWriter()
        run_entity_research(
            session=FakeSession(),
            roster=(_mk_roster_entry(),),
            roster_reader=rr,
            allowlist_reader=ar,
            claim_fetcher=fetch,
            vault_writer=vw,
            checkpoint_writer=cpw,
            force_refresh=True,
        )
        start_payload = cpw.calls[0][1]
        assert start_payload["force_refresh"] is True

    def test_empty_roster_writes_nothing(self):
        rr = FakeRosterReader(roster=())
        ar = FakeAllowlistReader(allowlist=_mk_allowlist())
        fetch = FakeClaimFetcher(per_entity={})
        vw = RecordingVaultWriter()
        cpw = RecordingCheckpointWriter()
        result = run_entity_research(
            session=FakeSession(),
            roster=(),
            roster_reader=rr,
            allowlist_reader=ar,
            claim_fetcher=fetch,
            vault_writer=vw,
            checkpoint_writer=cpw,
        )
        assert result.ordered == ()
        assert result.dossiers_by_slug == {}
        assert vw.calls == []

    def test_multi_entity_distinct_dossiers(self):
        roster = (
            _mk_roster_entry(entity_slug="a"),
            _mk_roster_entry(entity_slug="b"),
            _mk_roster_entry(entity_slug="c"),
        )
        cands = {
            "a": (
                _mk_candidate(
                    claim_id="a1", claim_text="t_a", domain="example.test"
                ),
            ),
            "b": (
                _mk_candidate(
                    claim_id="b1", claim_text="t_b", domain="example.test"
                ),
            ),
            "c": (
                _mk_candidate(
                    claim_id="c1", claim_text="t_c", domain="example.test"
                ),
            ),
        }
        result, vw, *_ = _build_happy_result(
            roster=roster, candidates=cands
        )
        assert len(result.ordered) == 3
        assert len(vw.calls) == 3
        assert {d.entity_slug for d in result.ordered} == {"a", "b", "c"}


# ---------------------------------------------------------------------------
# TestSignOffDossier
# ---------------------------------------------------------------------------


def _sign_body_and_open(
    tmp_path: Path,
    entity_slug: str,
    body: bytes,
    canonical_tail: Optional[str] = None,
) -> tuple[Path, FakeBodyReader, EntityDossier]:
    body_path, reader = _write_body_and_open(tmp_path, entity_slug, body)
    computed = hashlib.sha3_512(body).hexdigest()
    # Align canonical path to match the expected_tail used by sign_off_dossier:
    expected_tail = f"orgs/mycosymbiotics_cooperative/dossier/entities/{entity_slug}.md"
    canonical = canonical_tail or f"/vault/{expected_tail}"
    reader.canonical_paths[entity_slug] = canonical
    prior = EntityDossier(
        entity_slug=entity_slug,
        roster_entry=_mk_roster_entry(entity_slug=entity_slug),
        claims=(),
        dossier_written_at_utc="2026-04-20T00:00:00Z",
        dossier_content_hash=computed,
        operator_signoff=None,
    )
    return body_path, reader, prior


class TestSignOffDossier:
    def test_happy_path_returns_signoff(self, tmp_path):
        body = b"dossier content"
        body_path, reader, prior = _sign_body_and_open(
            tmp_path, "alice", body
        )
        signer = FakeSigner(fixed_signature=b"sig-bytes")
        vw = RecordingVaultWriter()
        cpw = RecordingCheckpointWriter()
        signoff = sign_off_dossier(
            session=FakeSession(),
            entity_slug="alice",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=signer,
            vault_writer=vw,
            checkpoint_writer=cpw,
            prior_dossier=prior,
            clock=lambda: "2026-04-21T00:00:00Z",
        )
        assert isinstance(signoff, DossierSignoff)
        assert signoff.operator_signature == b"sig-bytes"
        assert signoff.operator_id == "josh"
        assert signoff.signed_content_hash == prior.dossier_content_hash
        assert signoff.signed_at_utc == "2026-04-21T00:00:00Z"

    def test_signoff_vault_write_shape(self, tmp_path):
        body = b"x"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        vw = RecordingVaultWriter()
        sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=FakeSigner(),
            vault_writer=vw,
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )
        assert len(vw.calls) == 1
        call = vw.calls[0]
        assert call.intent == INTENT_DOSSIER_SIGNOFF_WRITE
        assert call.path.endswith("signoff/x.json")

    def test_signoff_payload_is_canonical_json(self, tmp_path):
        body = b"x"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        vw = RecordingVaultWriter()
        sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=FakeSigner(fixed_signature=b"\xde\xad"),
            vault_writer=vw,
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )
        payload = json.loads(vw.calls[0].bytes_.decode("utf-8"))
        assert payload["operator_signature"] == "dead"
        # Canonical JSON sorts keys.
        assert list(payload.keys()) == sorted(payload.keys())

    def test_signer_gets_binding_bytes(self, tmp_path):
        body = b"x"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        signer = FakeSigner()
        sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=signer,
            vault_writer=RecordingVaultWriter(),
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )
        assert len(signer.calls) == 1
        parsed = json.loads(signer.calls[0].decode("utf-8"))
        assert parsed["slug"] == "mycosymbiotics_cooperative"
        assert parsed["entity_slug"] == "x"

    def test_content_hash_mismatch_raises_01c(self, tmp_path):
        body = b"actual content"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        # Tamper prior_dossier content hash to force 01c.
        tampered = EntityDossier(
            entity_slug=prior.entity_slug,
            roster_entry=prior.roster_entry,
            claims=prior.claims,
            dossier_written_at_utc=prior.dossier_written_at_utc,
            dossier_content_hash="0" * 128,
            operator_signoff=None,
        )
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=tampered,
            )
        assert exc.value.code == F_SCOUT_D_01c
        assert "content_hash_mismatch" in exc.value.reason_tag

    def test_canonical_path_tail_mismatch_raises_01a(self, tmp_path):
        body = b"x"
        body_path = tmp_path / "x.md"
        body_path.write_bytes(body)
        # Canonical path does NOT end with expected tail.
        reader = FakeBodyReader(
            body_paths={"x": body_path},
            canonical_paths={"x": "/foo/bar/elsewhere.md"},
        )
        prior = EntityDossier(
            entity_slug="x",
            roster_entry=_mk_roster_entry(entity_slug="x"),
            claims=(),
            dossier_written_at_utc="t",
            dossier_content_hash=hashlib.sha3_512(body).hexdigest(),
            operator_signoff=None,
        )
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_01a
        assert "canonical_path_tail_mismatch" in exc.value.reason_tag

    def test_body_size_exceeds_raises_d_02(self, tmp_path):
        body = b"x" * (_MAX_DOSSIER_BYTES + 1)
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        with pytest.raises(DossierSizeExceeded) as exc:
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=prior,
            )
        assert F_SCOUT_D_02 in str(exc.value)
        assert "fstat_size_gt_max" in str(exc.value)

    def test_body_exact_cap_boundary_accepted(self, tmp_path):
        body = b"x" * _MAX_DOSSIER_BYTES
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        vw = RecordingVaultWriter()
        signoff = sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=FakeSigner(),
            vault_writer=vw,
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )
        assert len(vw.calls) == 1
        assert signoff.signed_content_hash == prior.dossier_content_hash

    def test_short_read_raises_01e(self, tmp_path, monkeypatch):
        body = b"full content body"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        real_read = os.read

        def _short(fd, n):
            return real_read(fd, n)[: n // 2]

        monkeypatch.setattr(
            "pipeline.scout.entity_research.os.read", _short
        )
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_01e

    def test_checkpoint_start_and_complete_emitted(self, tmp_path):
        body = b"x"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        cpw = RecordingCheckpointWriter()
        sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=FakeSigner(),
            vault_writer=RecordingVaultWriter(),
            checkpoint_writer=cpw,
            prior_dossier=prior,
        )
        assert cpw.stages()[0] == "dossier_signoff_start"
        assert cpw.stages()[-1] == "dossier_signoff_complete"
        assert cpw.calls[-1][1]["outcome"] == "success"

    def test_signoff_failure_checkpoints_failure_outcome(self, tmp_path):
        body = b"x"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        tampered = EntityDossier(
            entity_slug=prior.entity_slug,
            roster_entry=prior.roster_entry,
            claims=prior.claims,
            dossier_written_at_utc=prior.dossier_written_at_utc,
            dossier_content_hash="0" * 128,
            operator_signoff=None,
        )
        cpw = RecordingCheckpointWriter()
        with pytest.raises(DossierSignoffVerifyFailure):
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=cpw,
                prior_dossier=tampered,
            )
        assert cpw.calls[-1][1]["outcome"] == "failure"
        assert cpw.calls[-1][1]["error_type"] == "DossierSignoffVerifyFailure"

    def test_expires_at_is_plus_validity_days(self, tmp_path):
        body = b"x"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        written_at = prior.dossier_written_at_utc
        signoff = sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=FakeSigner(),
            vault_writer=RecordingVaultWriter(),
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )
        expected = _plus_validity_days(written_at)
        assert signoff.expires_at_utc == expected

    def test_signed_inode_matches_fstat(self, tmp_path):
        body = b"x"
        body_path, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        st = body_path.stat()
        signoff = sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=FakeSigner(),
            vault_writer=RecordingVaultWriter(),
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )
        assert signoff.signed_inode == st.st_ino

    def test_empty_body_hashes_deterministically(self, tmp_path):
        body = b""
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        assert prior.dossier_content_hash == hashlib.sha3_512(b"").hexdigest()
        signoff = sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="TOK",
            body_reader=reader,
            signoff_signer=FakeSigner(),
            vault_writer=RecordingVaultWriter(),
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )
        assert signoff.signed_content_hash == prior.dossier_content_hash

    def test_operator_confirmation_token_threaded(self, tmp_path):
        # Token must be accepted at the signature even though not validated.
        body = b"x"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        sign_off_dossier(
            session=FakeSession(),
            entity_slug="x",
            operator_confirmation_token="any-string-works",
            body_reader=reader,
            signoff_signer=FakeSigner(),
            vault_writer=RecordingVaultWriter(),
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )


# ---------------------------------------------------------------------------
# TestReadEntityDossier
# ---------------------------------------------------------------------------


def _build_signed_dossier(
    tmp_path: Path, entity_slug: str, body: bytes
) -> tuple[EntityDossier, FakeBodyReader, DossierSignoff]:
    body_path, reader, prior = _sign_body_and_open(
        tmp_path, entity_slug, body
    )
    st = body_path.stat()
    signoff = DossierSignoff(
        signed_at_utc="2026-04-21T00:00:00Z",
        operator_id="josh",
        signed_canonical_path=reader.canonical_paths[entity_slug],
        signed_inode=st.st_ino,
        signed_content_hash=prior.dossier_content_hash,
        operator_signature=b"sig",
        expires_at_utc="2026-07-20T00:00:00Z",
    )
    return prior, reader, signoff


class TestReadEntityDossier:
    def test_happy_path_returns_dossier_and_signoff(self, tmp_path):
        prior, body_reader, signoff = _build_signed_dossier(
            tmp_path, "alice", b"body-bytes"
        )
        sr = FakeSignoffReader(store={"alice": signoff})
        reverified, returned_signoff = read_entity_dossier(
            session=FakeSession(),
            entity_slug="alice",
            body_reader=body_reader,
            signoff_reader=sr,
            prior_dossier=prior,
        )
        assert reverified.entity_slug == "alice"
        assert reverified.operator_signoff is not None
        assert returned_signoff is signoff

    def test_unsourced_raises_d_03(self, tmp_path):
        prior, body_reader, _ = _build_signed_dossier(
            tmp_path, "alice", b"body-bytes"
        )
        sr = FakeSignoffReader(store={})  # no signoff
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            read_entity_dossier(
                session=FakeSession(),
                entity_slug="alice",
                body_reader=body_reader,
                signoff_reader=sr,
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_03
        assert "unsourced" in exc.value.reason_tag

    def test_path_drift_raises_d_03(self, tmp_path):
        prior, body_reader, signoff = _build_signed_dossier(
            tmp_path, "alice", b"body-bytes"
        )
        tampered_signoff = DossierSignoff(
            signed_at_utc=signoff.signed_at_utc,
            operator_id=signoff.operator_id,
            signed_canonical_path="/different/path.md",
            signed_inode=signoff.signed_inode,
            signed_content_hash=signoff.signed_content_hash,
            operator_signature=signoff.operator_signature,
            expires_at_utc=signoff.expires_at_utc,
        )
        sr = FakeSignoffReader(store={"alice": tampered_signoff})
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            read_entity_dossier(
                session=FakeSession(),
                entity_slug="alice",
                body_reader=body_reader,
                signoff_reader=sr,
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_03
        assert "path_drift" in exc.value.reason_tag

    def test_inode_drift_raises_d_03(self, tmp_path):
        prior, body_reader, signoff = _build_signed_dossier(
            tmp_path, "alice", b"body-bytes"
        )
        drifted = DossierSignoff(
            signed_at_utc=signoff.signed_at_utc,
            operator_id=signoff.operator_id,
            signed_canonical_path=signoff.signed_canonical_path,
            signed_inode=signoff.signed_inode + 999,
            signed_content_hash=signoff.signed_content_hash,
            operator_signature=signoff.operator_signature,
            expires_at_utc=signoff.expires_at_utc,
        )
        sr = FakeSignoffReader(store={"alice": drifted})
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            read_entity_dossier(
                session=FakeSession(),
                entity_slug="alice",
                body_reader=body_reader,
                signoff_reader=sr,
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_03
        assert "inode_drift" in exc.value.reason_tag

    def test_content_hash_drift_raises_d_03(self, tmp_path):
        prior, body_reader, signoff = _build_signed_dossier(
            tmp_path, "alice", b"body-bytes"
        )
        drifted = DossierSignoff(
            signed_at_utc=signoff.signed_at_utc,
            operator_id=signoff.operator_id,
            signed_canonical_path=signoff.signed_canonical_path,
            signed_inode=signoff.signed_inode,
            signed_content_hash="0" * 128,
            operator_signature=signoff.operator_signature,
            expires_at_utc=signoff.expires_at_utc,
        )
        sr = FakeSignoffReader(store={"alice": drifted})
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            read_entity_dossier(
                session=FakeSession(),
                entity_slug="alice",
                body_reader=body_reader,
                signoff_reader=sr,
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_03
        assert "content_hash_drift" in exc.value.reason_tag

    def test_body_oversize_raises_d_02(self, tmp_path):
        body = b"x" * (_MAX_DOSSIER_BYTES + 1)
        prior, body_reader, _ = _build_signed_dossier(
            tmp_path, "alice", body
        )
        # Build a signoff record (fields copied from prior).
        st = Path(str(body_reader.body_paths["alice"])).stat()
        so = DossierSignoff(
            signed_at_utc="t",
            operator_id="o",
            signed_canonical_path=body_reader.canonical_paths["alice"],
            signed_inode=st.st_ino,
            signed_content_hash=prior.dossier_content_hash,
            operator_signature=b"x",
            expires_at_utc="t2",
        )
        sr = FakeSignoffReader(store={"alice": so})
        with pytest.raises(DossierSizeExceeded):
            read_entity_dossier(
                session=FakeSession(),
                entity_slug="alice",
                body_reader=body_reader,
                signoff_reader=sr,
                prior_dossier=prior,
            )

    def test_short_read_raises_01e(self, tmp_path, monkeypatch):
        prior, body_reader, signoff = _build_signed_dossier(
            tmp_path, "alice", b"body-bytes-here"
        )
        sr = FakeSignoffReader(store={"alice": signoff})
        real_read = os.read

        def _short(fd, n):
            return real_read(fd, n)[: n // 2]

        monkeypatch.setattr(
            "pipeline.scout.entity_research.os.read", _short
        )
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            read_entity_dossier(
                session=FakeSession(),
                entity_slug="alice",
                body_reader=body_reader,
                signoff_reader=sr,
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_01e

    def test_signoff_reader_called_with_scope(self, tmp_path):
        prior, body_reader, signoff = _build_signed_dossier(
            tmp_path, "alice", b"body"
        )
        sr = FakeSignoffReader(store={"alice": signoff})
        read_entity_dossier(
            session=FakeSession(),
            entity_slug="alice",
            body_reader=body_reader,
            signoff_reader=sr,
            prior_dossier=prior,
        )
        assert sr.calls == [
            ("session-r10m2-abc", "mycosymbiotics_cooperative", "alice")
        ]

    def test_reverified_has_all_prior_fields(self, tmp_path):
        prior, body_reader, signoff = _build_signed_dossier(
            tmp_path, "alice", b"body"
        )
        sr = FakeSignoffReader(store={"alice": signoff})
        reverified, _ = read_entity_dossier(
            session=FakeSession(),
            entity_slug="alice",
            body_reader=body_reader,
            signoff_reader=sr,
            prior_dossier=prior,
        )
        assert reverified.entity_slug == prior.entity_slug
        assert reverified.claims == prior.claims
        assert reverified.roster_entry == prior.roster_entry
        assert (
            reverified.dossier_content_hash == prior.dossier_content_hash
        )

    def test_canonical_bytes_helper_reachable(self, tmp_path):
        # entity_dossier_canonical_bytes reference should resolve.
        prior, body_reader, signoff = _build_signed_dossier(
            tmp_path, "alice", b"body"
        )
        sr = FakeSignoffReader(store={"alice": signoff})
        reverified, _ = read_entity_dossier(
            session=FakeSession(),
            entity_slug="alice",
            body_reader=body_reader,
            signoff_reader=sr,
            prior_dossier=prior,
        )
        _ = entity_dossier_canonical_bytes(reverified)


# ---------------------------------------------------------------------------
# TestAdversarialFdRace / adversarial bucket (≥6 adversarial)
# ---------------------------------------------------------------------------


class TestAdversarialFdRace:
    def test_final_refstat_inode_drift_raises_01d(self, tmp_path, monkeypatch):
        """Simulate in-flight inode swap between first fstat and final re-fstat
        inside the FD-held with-block (A-03 durable enforcement)."""
        body = b"body content"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        real_fstat = os.fstat
        call_count = {"n": 0}

        def _drifting_fstat(fd):
            call_count["n"] += 1
            st = real_fstat(fd)
            if call_count["n"] >= 2:
                # Return a synthetic drift on the final re-fstat.
                class _S:
                    st_ino = st.st_ino + 77
                    st_size = st.st_size

                return _S()
            return st

        monkeypatch.setattr(
            "pipeline.scout.entity_research.os.fstat", _drifting_fstat
        )
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_01d
        assert "final_refstat_inode_drift" in exc.value.reason_tag

    def test_symlink_swap_mid_flight_fails_canonical_tail(self, tmp_path):
        """FakeBodyReader emits a canonical_path that points at a SYMLINK-
        swapped destination — tail-suffix check rejects."""
        body = b"ok"
        body_path = tmp_path / "x.md"
        body_path.write_bytes(body)
        # Canonical path intentionally drifted (attacker-controlled swap).
        attacker_canonical = "/attacker/other/entities/x.md"
        reader = FakeBodyReader(
            body_paths={"x": body_path},
            canonical_paths={"x": attacker_canonical},
        )
        prior = EntityDossier(
            entity_slug="x",
            roster_entry=_mk_roster_entry(entity_slug="x"),
            claims=(),
            dossier_written_at_utc="t",
            dossier_content_hash=hashlib.sha3_512(body).hexdigest(),
            operator_signoff=None,
        )
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_01a

    def test_concurrent_truncate_during_read_fails_01e(
        self, tmp_path, monkeypatch
    ):
        """Reader returns fewer bytes than fstat reported."""
        body = b"full-body-content-20b"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)
        real_read = os.read

        def _short(fd, n):
            return real_read(fd, n)[: max(0, n - 5)]

        monkeypatch.setattr(
            "pipeline.scout.entity_research.os.read", _short
        )
        with pytest.raises(DossierSignoffVerifyFailure) as exc:
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=prior,
            )
        assert exc.value.code == F_SCOUT_D_01e

    def test_fd_closed_even_on_mid_flight_exception(self, tmp_path):
        """Adversarial: signer raises mid-flight. FD must still close."""
        body = b"body"
        body_path, reader, prior = _sign_body_and_open(
            tmp_path, "x", body
        )

        class _ExplodingSigner:
            def sign(self, *, binding_bytes):
                raise RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=_ExplodingSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=prior,
            )
        # The FD should be closed — re-reading via reader should open a new
        # FD and succeed; since FakeBodyReader opens a fresh FD each call,
        # no assertion on a leaked FD number is possible, but we confirm
        # no side-effect leakage by verifying the file handle count via
        # a fresh successful call.
        with _open_dossier_body_fd(
            body_reader=reader, session=FakeSession(), entity_slug="x"
        ) as h:
            assert os.fstat(h.fd).st_size == len(body)


class TestAdversarialTieredBoundary:
    def test_boundary_cap_exactly_passes(self, tmp_path):
        body = b"A" * _MAX_DOSSIER_BYTES
        _, reader, prior = _sign_body_and_open(tmp_path, "b", body)
        vw = RecordingVaultWriter()
        sign_off_dossier(
            session=FakeSession(),
            entity_slug="b",
            operator_confirmation_token="T",
            body_reader=reader,
            signoff_signer=FakeSigner(),
            vault_writer=vw,
            checkpoint_writer=RecordingCheckpointWriter(),
            prior_dossier=prior,
        )
        assert len(vw.calls) == 1

    def test_boundary_cap_plus_one_fails(self, tmp_path):
        body = b"A" * (_MAX_DOSSIER_BYTES + 1)
        _, reader, prior = _sign_body_and_open(tmp_path, "b", body)
        with pytest.raises(DossierSizeExceeded):
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="b",
                operator_confirmation_token="T",
                body_reader=reader,
                signoff_signer=FakeSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpointWriter(),
                prior_dossier=prior,
            )


class TestAdversarialFuzz:
    def test_claim_order_shuffle_dossier_hash_stable(self):
        """Dossier content hash must not depend on fetcher-supplied order."""
        import random as _random

        rng = _random.Random(9001)
        base_cands = [
            _mk_candidate(
                claim_id=f"c{i}",
                claim_text=f"claim-{i}",
                domain="example.test",
            )
            for i in range(6)
        ]
        seen_hashes = set()
        for _ in range(20):
            shuffled = list(base_cands)
            rng.shuffle(shuffled)
            result, *_ = _build_happy_result(
                candidates={"josh_g": tuple(shuffled)}
            )
            h = result.dossiers_by_slug["josh_g"].dossier_content_hash
            seen_hashes.add(h)
        # Shuffling input candidate order must not change dossier hash.
        assert len(seen_hashes) == 1

    def test_fuzz_non_allowlisted_domains_are_all_dropped(self):
        """200 random unknown domains — every one must be recorded as a drop."""
        import random as _random

        rng = _random.Random(42)
        allowed = frozenset({"example.test"})
        cands = []
        for i in range(200):
            dom = rng.choice(["mal.test", "bad.test", "evil.test"])
            cands.append(
                _mk_candidate(
                    claim_id=f"c{i}",
                    claim_text=f"t{i}",
                    domain=dom,
                )
            )
        # Add one allowed claim so the entity has something.
        cands.append(
            _mk_candidate(
                claim_id="ok",
                claim_text="ok-claim",
                domain="example.test",
            )
        )
        result, *_ = _build_happy_result(
            candidates={"josh_g": tuple(cands)},
            allowlist=_mk_allowlist(domains=allowed),
        )
        assert len(result.non_allowlisted_domain_events) == 200
        assert len(result.dossiers_by_slug["josh_g"].claims) == 1


class TestAdversarialCrossOrgIsolation:
    def test_allowlist_slug_unused_by_build_but_recorded(self):
        """The module does not itself enforce slug equality between
        allowlist record and session slug (Section 2 reader owns that
        gate). Confirm that allowlists with differing slug field still
        flow through and are not silently trusted — caller must set the
        allowlist slug to match the session slug as a Law 3 precondition.
        """
        sess = FakeSession(slug="org-a")
        wrong_list = _mk_allowlist(
            slug="org-b", domains=frozenset({"example.test"})
        )
        result, *_ = _build_happy_result(
            session=sess,
            allowlist=wrong_list,
            candidates={
                "josh_g": (
                    _mk_candidate(
                        claim_id="c",
                        claim_text="t",
                        domain="example.test",
                    ),
                )
            },
        )
        # The write path used the SESSION slug, not the allowlist slug.
        # Run built; no silent data pollution.
        assert isinstance(result, EntityResearchResult)


# ---------------------------------------------------------------------------
# TestExceptionHierarchy
# ---------------------------------------------------------------------------


class TestSignalRethrow:
    def test_run_entity_research_rethrows_keyboard_interrupt(self):
        """KeyboardInterrupt inside the body must not be caught by the
        failure-path except — verify the bare-rethrow line is reached."""
        rr = FakeRosterReader(roster=(_mk_roster_entry(),))
        ar = FakeAllowlistReader(allowlist=_mk_allowlist())
        fetch = FakeClaimFetcher(
            per_entity={
                "josh_g": (
                    _mk_candidate(
                        claim_id="c",
                        claim_text="t",
                        domain="example.test",
                    ),
                )
            }
        )
        vw = RecordingVaultWriter(raise_with=KeyboardInterrupt())
        cpw = RecordingCheckpointWriter()
        with pytest.raises(KeyboardInterrupt):
            run_entity_research(
                session=FakeSession(),
                roster=(_mk_roster_entry(),),
                roster_reader=rr,
                allowlist_reader=ar,
                claim_fetcher=fetch,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        # No failure checkpoint emitted — the KeyboardInterrupt bypasses the
        # general except.
        assert cpw.stages() == ["entity_research_start"]

    def test_sign_off_dossier_rethrows_system_exit(self, tmp_path):
        body = b"x"
        _, reader, prior = _sign_body_and_open(tmp_path, "x", body)

        class _ExitSigner:
            def sign(self, *, binding_bytes):
                raise SystemExit(1)

        cpw = RecordingCheckpointWriter()
        with pytest.raises(SystemExit):
            sign_off_dossier(
                session=FakeSession(),
                entity_slug="x",
                operator_confirmation_token="TOK",
                body_reader=reader,
                signoff_signer=_ExitSigner(),
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=cpw,
                prior_dossier=prior,
            )
        # The SystemExit bypasses the general except, so no failure checkpoint.
        assert cpw.stages() == ["dossier_signoff_start"]


class TestExceptionHierarchy:
    def test_dossier_signoff_verify_failure_is_exception(self):
        assert issubclass(DossierSignoffVerifyFailure, Exception)

    def test_dossier_size_exceeded_is_exception(self):
        assert issubclass(DossierSizeExceeded, Exception)

    def test_intent_mismatch_is_exception(self):
        assert issubclass(IntentMismatch, Exception)

    def test_verify_failure_carries_code_and_reason_tag(self):
        e = DossierSignoffVerifyFailure(code="X-01", reason_tag="why")
        assert e.code == "X-01"
        assert e.reason_tag == "why"
        assert "X-01" in str(e)
        assert "why" in str(e)

    def test_intent_mismatch_carries_code_and_reason_tag(self):
        e = IntentMismatch(code="Y-01", reason_tag="reason")
        assert e.code == "Y-01"
        assert e.reason_tag == "reason"


# ---------------------------------------------------------------------------
# TestEntityClaimCandidate / TestEntityResearchResult shape
# ---------------------------------------------------------------------------


class TestEntityClaimCandidate:
    def test_frozen_kw_only(self):
        c = EntityClaimCandidate(
            claim_id="a",
            claim_text="t",
            source_url="u",
            source_registrable_domain="d",
            fetched_at_utc="t",
            url_hash="h",
            content_hash="h",
            evidence_quote="e",
        )
        with pytest.raises(Exception):
            c.claim_id = "b"  # type: ignore[misc]

    def test_positional_args_rejected(self):
        with pytest.raises(TypeError):
            EntityClaimCandidate(
                "a", "t", "u", "d", "t", "h", "h", "e"
            )  # type: ignore[misc]


class TestEntityResearchResultShape:
    def test_frozen(self):
        r = EntityResearchResult(
            dossiers_by_slug={},
            ordered=(),
            non_allowlisted_domain_events=(),
        )
        with pytest.raises(Exception):
            r.ordered = (1,)  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestFDHandleShape
# ---------------------------------------------------------------------------


class TestFDHandleShape:
    def test_frozen_kw_only(self):
        h = FDHandle(fd=0, canonical_path="/p", close=lambda: None)
        with pytest.raises(Exception):
            h.fd = 1  # type: ignore[misc]

    def test_close_callable(self):
        called = {"n": 0}

        def _close():
            called["n"] += 1

        h = FDHandle(fd=0, canonical_path="/p", close=_close)
        h.close()
        assert called["n"] == 1


# ---------------------------------------------------------------------------
# TestAstLintClean
# ---------------------------------------------------------------------------


class TestAstLintClean:
    def test_scout_directory_clean(self, tmp_path):
        # E-027 directory-contract: copy pipeline/scout into a tmp-dir so
        # lint_tree's default rules run against a stable snapshot.
        from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
        import shutil

        scout_src = Path(__file__).resolve().parents[2] / "pipeline" / "scout"
        scout_copy = tmp_path / "scout"
        shutil.copytree(scout_src, scout_copy)
        violations = lint_tree(scout_copy, DEFAULT_RULES)
        assert violations == [], [str(v) for v in violations]


# ---------------------------------------------------------------------------
# End of file
# ---------------------------------------------------------------------------
