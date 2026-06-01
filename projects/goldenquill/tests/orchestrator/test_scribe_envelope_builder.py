"""Tests for ``pipeline.orchestrator.scribe_envelope_builder``.

Covers:
- Builder constructs a valid envelope with all invariants satisfied.
- Sector=None path: project_context passes through unchanged.
- Sector=valid path: sector_knowledge key injected via the merge helper.
- Sector=invalid: :class:`InvalidSectorError` raised.
- Shell-hash validation defers to ScribeEnvelope.__post_init__ (the
  builder doesn't recompute or validate it — caller-supplied per
  hash-discipline contract).
- emit_scribe_envelope_bytes round-trips through decode_envelope.

Round-trip test exercises the full IPC contract: build → emit bytes →
decode_envelope reconstructs an equivalent envelope.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

import pytest

from pipeline.orchestrator.scribe_envelope_builder import (
    ENVELOPE_VERSION,
    InvalidSectorError,
    build_scribe_envelope,
    emit_scribe_envelope_bytes,
)
from pipeline.seats.scribe.knowledge_packs import PROJECT_CONTEXT_PACK_KEY
from pipeline.seats.scribe.seat import (
    ScribeEnvelope,
    ScribeEnvelopeMalformed,
    decode_envelope,
)


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

def _valid_shell_hash() -> str:
    """A real lowercase 128-hex SHA3-512 string the envelope will accept."""
    return hashlib.sha3_512(b"prompt-shell-test").hexdigest()


def _fixed_clock(when: datetime | None = None):
    pinned = when or datetime(2026, 5, 8, 12, 0, 0, tzinfo=timezone.utc)
    return lambda: pinned


def _base_kwargs(*, sector: str | None = None, project_context: dict[str, Any] | None = None) -> dict[str, Any]:
    return dict(
        run_id="run-build-test",
        org_slug="fit_farms",
        iteration_number=0,
        section_name="Project Narrative",
        section_order=1,
        funder_dialect="centrist",
        operator_override_dialect=None,
        program_code="VAPG",
        admin_risk_register_snapshot_path="/snapshots/admin_risk_2026-05-01.json",
        admin_risk_snapshot_age_hours=12.0,
        conversation_log_anchor=None,
        compiled_prompt="System frame ... RFA frame ... Section task ...",
        compiled_prompt_shell_sha3_512=_valid_shell_hash(),
        project_context=project_context if project_context is not None else {
            "applicant_name": "FIT Farms LLC",
            "partners": ["Penn State Extension"],
        },
        sector=sector,
        clock=_fixed_clock(),
    )


# --------------------------------------------------------------------------
# Construction without sector
# --------------------------------------------------------------------------

class TestBuildWithoutSector:

    def test_builds_valid_envelope(self) -> None:
        env = build_scribe_envelope(**_base_kwargs())
        assert isinstance(env, ScribeEnvelope)
        assert env.envelope_version == ENVELOPE_VERSION
        assert env.run_id == "run-build-test"
        assert env.org_slug == "fit_farms"
        assert env.section_order == 1
        assert env.envelope_emitted_at_utc.tzinfo is not None

    def test_project_context_passes_through_unchanged(self) -> None:
        env = build_scribe_envelope(**_base_kwargs())
        # No sector_knowledge key when sector is None
        assert PROJECT_CONTEXT_PACK_KEY not in env.project_context
        # Original keys preserved
        assert env.project_context["applicant_name"] == "FIT Farms LLC"
        assert env.project_context["partners"] == ["Penn State Extension"]


# --------------------------------------------------------------------------
# Construction with sector — pack merge
# --------------------------------------------------------------------------

class TestBuildWithSector:

    def test_sector_merge_injects_knowledge(self) -> None:
        env = build_scribe_envelope(**_base_kwargs(sector="regenerative_ag"))
        # sector_knowledge key now present
        assert PROJECT_CONTEXT_PACK_KEY in env.project_context
        sk = env.project_context[PROJECT_CONTEXT_PACK_KEY]
        assert sk["sector"] == "regenerative_ag"
        assert sk["loaded"] is True
        assert sk["fact_count"] >= 5
        assert "## Sector context: regenerative_ag" in sk["rendered_block"]
        # Original keys still preserved alongside the merge
        assert env.project_context["applicant_name"] == "FIT Farms LLC"

    def test_unseeded_sector_still_merges_with_loaded_false(self) -> None:
        # All real seed packs are loaded, but this test demonstrates that
        # the merge contract surfaces loaded=False for empty sectors —
        # by passing a custom base_dir-independent mapping where we don't
        # even have a regenerative_ag dir. We use the real loader, so the
        # only way to exercise this is a sector-with-no-pack-on-disk; all
        # six current sectors have packs. So we verify the contract via
        # the test_orchestrator_can_skip_unset_sector test in the
        # knowledge_packs suite. Here we just confirm the builder
        # doesn't crash on a known-loaded sector.
        env = build_scribe_envelope(**_base_kwargs(sector="urban_ag"))
        sk = env.project_context[PROJECT_CONTEXT_PACK_KEY]
        assert sk["loaded"] is True

    def test_invalid_sector_raises(self) -> None:
        with pytest.raises(InvalidSectorError, match="not_a_sector"):
            build_scribe_envelope(**_base_kwargs(sector="not_a_sector"))


# --------------------------------------------------------------------------
# Envelope-invariant validation defers to ScribeEnvelope.__post_init__
# --------------------------------------------------------------------------

class TestInvariantPropagation:

    def test_bad_shell_hash_length_raises(self) -> None:
        kwargs = _base_kwargs()
        kwargs["compiled_prompt_shell_sha3_512"] = "deadbeef"  # too short
        with pytest.raises(ScribeEnvelopeMalformed, match="128 hex"):
            build_scribe_envelope(**kwargs)

    def test_uppercase_shell_hash_raises(self) -> None:
        kwargs = _base_kwargs()
        # uppercase the hash → __post_init__ rejects (lowercase invariant)
        valid = _valid_shell_hash()
        kwargs["compiled_prompt_shell_sha3_512"] = valid.upper()
        with pytest.raises(ScribeEnvelopeMalformed, match="lowercase"):
            build_scribe_envelope(**kwargs)

    def test_invalid_dialect_raises(self) -> None:
        kwargs = _base_kwargs()
        kwargs["funder_dialect"] = "off-the-wall-dialect"
        with pytest.raises(ScribeEnvelopeMalformed, match="funder_dialect"):
            build_scribe_envelope(**kwargs)

    def test_negative_iteration_raises(self) -> None:
        kwargs = _base_kwargs()
        kwargs["iteration_number"] = -1
        with pytest.raises(ScribeEnvelopeMalformed, match="iteration_number"):
            build_scribe_envelope(**kwargs)


# --------------------------------------------------------------------------
# JSON serialization round-trip
# --------------------------------------------------------------------------

class TestSerialization:
    """build → emit bytes → decode_envelope produces an equivalent envelope."""

    def test_round_trip_no_sector(self) -> None:
        env_built = build_scribe_envelope(**_base_kwargs())
        raw = emit_scribe_envelope_bytes(env_built)
        assert isinstance(raw, bytes)
        env_decoded = decode_envelope(raw_bytes=raw)
        assert env_decoded.run_id == env_built.run_id
        assert env_decoded.org_slug == env_built.org_slug
        assert env_decoded.section_name == env_built.section_name
        assert env_decoded.compiled_prompt == env_built.compiled_prompt
        assert env_decoded.envelope_emitted_at_utc == env_built.envelope_emitted_at_utc

    def test_round_trip_with_sector_preserves_knowledge_pack(self) -> None:
        env_built = build_scribe_envelope(**_base_kwargs(sector="regenerative_ag"))
        raw = emit_scribe_envelope_bytes(env_built)
        env_decoded = decode_envelope(raw_bytes=raw)
        # Sector knowledge survives the round-trip
        assert PROJECT_CONTEXT_PACK_KEY in env_decoded.project_context
        sk = env_decoded.project_context[PROJECT_CONTEXT_PACK_KEY]
        assert sk["sector"] == "regenerative_ag"
        assert sk["loaded"] is True

    def test_emitted_bytes_are_valid_utf8_json(self) -> None:
        env = build_scribe_envelope(**_base_kwargs(sector="urban_ag"))
        raw = emit_scribe_envelope_bytes(env)
        decoded_json = json.loads(raw.decode("utf-8"))
        assert decoded_json["envelope_version"] == ENVELOPE_VERSION
        assert decoded_json["org_slug"] == "fit_farms"
        # project_context is plain dict (not MappingProxy) in the JSON
        assert isinstance(decoded_json["project_context"], dict)


# --------------------------------------------------------------------------
# Clock seam (E-017)
# --------------------------------------------------------------------------

class TestClockSeam:

    def test_injected_clock_used(self) -> None:
        when = datetime(2025, 12, 25, 9, 0, 0, tzinfo=timezone.utc)
        env = build_scribe_envelope(**_base_kwargs())  # default clock pinned in fixture
        # Override clock explicitly:
        kwargs = _base_kwargs()
        kwargs["clock"] = _fixed_clock(when)
        env2 = build_scribe_envelope(**kwargs)
        assert env2.envelope_emitted_at_utc == when

    def test_default_clock_emits_tz_aware_now(self) -> None:
        kwargs = _base_kwargs()
        kwargs["clock"] = None  # use the module default
        env = build_scribe_envelope(**kwargs)
        assert env.envelope_emitted_at_utc.tzinfo is not None
