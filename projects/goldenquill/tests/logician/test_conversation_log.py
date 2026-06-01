"""§4 Logician Round 4 — `conversation_log.py` BT9 + §4.6.4 anchor verifier."""

from __future__ import annotations

import dataclasses
import hashlib
import hmac
import json

import pytest

from pipeline.logician import conversation_log as cl
from pipeline.logician.conversation_log import (
    AnchorVerifyResult,
    ChainVerifyResult,
    ConversationLogAppendRace,
    ConversationLogChainBroken,
    ConversationLogEntry,
    F_BT9_01,
    F_BT9_02,
    F_BT9_03,
    F_POST_05_INVALID,
    F_POST_05_MISSING_ENTRY,
    F_POST_05_SUPERSEDED,
    F_POST_05_WRONG_KEY,
    GENESIS_PREV_HASH,
    SessionKeyVerifier,
    VALID_SPEAKERS,
    build_appended_entry,
    compute_content_hash,
    compute_entry_hash,
    parse_entry_line,
    parse_log_text,
    serialise_entry_line,
    signing_payload,
    verify_chain,
    verify_user_data_anchor,
)


# ---------------------------------------------------------------------------
# Helpers — fake signer + verifier
# ---------------------------------------------------------------------------


_TEST_KEY: bytes = b"k" * 32


def _hmac_sign(payload: bytes, key: bytes = _TEST_KEY) -> bytes:
    return hmac.new(key, payload, hashlib.sha3_512).digest()


class _FixedKeyVerifier:
    """Treats any non-empty signature as ACTIVE.

    A unit test that needs INVALID / WRONG_KEY / RETIRED / unknown-status
    pathways uses one of the dedicated verifiers below.
    """

    def verify_entry(self, entry: ConversationLogEntry) -> str:
        return "ACTIVE" if entry.session_key_signature else "INVALID"


class _AlwaysInvalidVerifier:
    def verify_entry(self, entry: ConversationLogEntry) -> str:
        return "INVALID"


class _AlwaysWrongKeyVerifier:
    def verify_entry(self, entry: ConversationLogEntry) -> str:
        return "WRONG_KEY"


class _AlwaysRetiredVerifier:
    def verify_entry(self, entry: ConversationLogEntry) -> str:
        return "RETIRED"


class _UnknownStatusVerifier:
    def verify_entry(self, entry: ConversationLogEntry) -> str:
        return "BANANA"


def _make_entry_chain(
    n: int,
    *,
    session_id: str = "sess-1",
    org_slug: str = "fit_farms_llc",
    speaker: str = "operator",
    contents: list[str] | None = None,
) -> tuple[ConversationLogEntry, ...]:
    entries: list[ConversationLogEntry] = []
    if contents is None:
        contents = [f"utterance {i+1}" for i in range(n)]
    for i in range(n):
        entries.append(
            build_appended_entry(
                prior_entries=tuple(entries),
                utc_timestamp=f"2026-04-19T00:00:0{i}Z",
                session_id=session_id,
                org_slug=org_slug,
                speaker=speaker,
                content=contents[i],
                signer=_hmac_sign,
            )
        )
    return tuple(entries)


# ---------------------------------------------------------------------------
# TestConstants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_bt9_codes_pinned(self) -> None:
        assert F_BT9_01 == "F-BT9-01"
        assert F_BT9_02 == "F-BT9-02"
        assert F_BT9_03 == "F-BT9-03"

    def test_post_05_subtag_codes_pinned(self) -> None:
        assert F_POST_05_INVALID == "F-POST-05.conversation_anchor_invalid"
        assert F_POST_05_MISSING_ENTRY == "F-POST-05.conversation_anchor_missing_entry"
        assert F_POST_05_SUPERSEDED == "F-POST-05.conversation_anchor_superseded"
        assert F_POST_05_WRONG_KEY == "F-POST-05.conversation_anchor_wrong_key"

    def test_valid_speakers_pinned(self) -> None:
        assert VALID_SPEAKERS == frozenset(
            {"operator", "scribe", "scout", "editor", "judge", "logician"}
        )

    def test_genesis_prev_hash_is_128_zeros(self) -> None:
        assert GENESIS_PREV_HASH == "0" * 128
        assert len(GENESIS_PREV_HASH) == 128


# ---------------------------------------------------------------------------
# TestEntryShape
# ---------------------------------------------------------------------------


class TestEntryShape:
    def test_entry_is_frozen_dataclass(self) -> None:
        entry = _make_entry_chain(1)[0]
        assert dataclasses.is_dataclass(entry)
        with pytest.raises(dataclasses.FrozenInstanceError):
            entry.content = "mutated"  # type: ignore[misc]

    def test_entry_requires_kw_only(self) -> None:
        with pytest.raises(TypeError):
            ConversationLogEntry(  # type: ignore[misc]
                1,
                "2026-04-19T00:00:00Z",
                "sess-1",
                "org",
                "operator",
                "hi",
                "h",
                GENESIS_PREV_HASH,
                "h",
                b"",
            )


# ---------------------------------------------------------------------------
# TestComputeContentHash
# ---------------------------------------------------------------------------


class TestComputeContentHash:
    def test_returns_128_hex_chars(self) -> None:
        h = compute_content_hash("hello")
        assert len(h) == 128
        int(h, 16)  # must parse as hex

    def test_deterministic(self) -> None:
        assert compute_content_hash("hello") == compute_content_hash("hello")

    def test_rejects_non_str(self) -> None:
        with pytest.raises(TypeError):
            compute_content_hash(b"hello")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TestComputeEntryHash
# ---------------------------------------------------------------------------


class TestComputeEntryHash:
    def _kwargs(self, **overrides):
        base = dict(
            seq_id=1,
            utc_timestamp="2026-04-19T00:00:00Z",
            session_id="sess-1",
            org_slug="fit_farms_llc",
            speaker="operator",
            content_hash=compute_content_hash("hi"),
            prev_entry_hash=GENESIS_PREV_HASH,
            corrects=None,
        )
        base.update(overrides)
        return base

    def test_deterministic(self) -> None:
        a = compute_entry_hash(**self._kwargs())
        b = compute_entry_hash(**self._kwargs())
        assert a == b
        assert len(a) == 128

    def test_includes_prev_entry_hash(self) -> None:
        a = compute_entry_hash(**self._kwargs())
        b = compute_entry_hash(**self._kwargs(prev_entry_hash="1" * 128))
        assert a != b

    def test_includes_corrects(self) -> None:
        a = compute_entry_hash(**self._kwargs(corrects=None))
        b = compute_entry_hash(**self._kwargs(corrects="abc"))
        assert a != b

    def test_includes_seq_id(self) -> None:
        a = compute_entry_hash(**self._kwargs(seq_id=1))
        b = compute_entry_hash(**self._kwargs(seq_id=2))
        assert a != b


# ---------------------------------------------------------------------------
# TestSerialiseRoundTrip
# ---------------------------------------------------------------------------


class TestSerialiseRoundTrip:
    def test_serialise_ends_with_newline(self) -> None:
        entry = _make_entry_chain(1)[0]
        line = serialise_entry_line(entry)
        assert line.endswith("\n")

    def test_round_trip_identity(self) -> None:
        entry = _make_entry_chain(1)[0]
        round_tripped = parse_entry_line(serialise_entry_line(entry).rstrip("\n"))
        assert round_tripped == entry

    def test_serialise_canonical_json(self) -> None:
        entry = _make_entry_chain(1)[0]
        body = json.loads(serialise_entry_line(entry))
        assert body["seq_id"] == 1
        assert body["session_key_signature"] == entry.session_key_signature.hex()

    def test_parse_entry_line_rejects_non_str(self) -> None:
        with pytest.raises(TypeError):
            parse_entry_line(b"{}")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TestParseLogText
# ---------------------------------------------------------------------------


class TestParseLogText:
    def test_empty_returns_empty_tuple(self) -> None:
        assert parse_log_text("") == ()
        assert parse_log_text("   \n  \n") == ()

    def test_multi_line_round_trip(self) -> None:
        entries = _make_entry_chain(3)
        text = "".join(serialise_entry_line(e) for e in entries)
        assert parse_log_text(text) == entries

    def test_skips_blank_lines(self) -> None:
        entries = _make_entry_chain(2)
        text = serialise_entry_line(entries[0]) + "\n" + serialise_entry_line(entries[1])
        assert parse_log_text(text) == entries

    def test_rejects_non_str(self) -> None:
        with pytest.raises(TypeError):
            parse_log_text(b"")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TestVerifyChain
# ---------------------------------------------------------------------------


class TestVerifyChain:
    def test_empty_chain_intact_no_head(self) -> None:
        result = verify_chain(())
        assert result.chain_intact is True
        assert result.head_seq_id is None
        assert result.failure_code is None

    def test_single_genesis_entry(self) -> None:
        entries = _make_entry_chain(1)
        result = verify_chain(entries)
        assert result.chain_intact is True
        assert result.head_seq_id == 1

    def test_three_chain_intact(self) -> None:
        entries = _make_entry_chain(3)
        result = verify_chain(entries)
        assert result.chain_intact is True
        assert result.head_seq_id == 3

    def test_broken_prev_entry_hash(self) -> None:
        entries = list(_make_entry_chain(2))
        bad = dataclasses.replace(entries[1], prev_entry_hash="9" * 128)
        result = verify_chain((entries[0], bad))
        assert result.chain_intact is False
        assert result.failure_code == F_BT9_01
        assert "prev_entry_hash" in result.failure_detail

    def test_seq_id_gap(self) -> None:
        entries = list(_make_entry_chain(2))
        # entries[1] has seq_id=2; mutate to 3 to create a gap
        bad = dataclasses.replace(entries[1], seq_id=3)
        result = verify_chain((entries[0], bad))
        assert result.chain_intact is False
        assert result.failure_code == F_BT9_01
        assert "seq_id gap" in result.failure_detail

    def test_replayed_seq_id_detected(self) -> None:
        entries = list(_make_entry_chain(2))
        replay = dataclasses.replace(entries[0])
        result = verify_chain((entries[0], entries[1], replay))
        assert result.chain_intact is False
        assert result.failure_code == F_BT9_03
        assert "replayed" in result.failure_detail

    def test_entry_hash_recompute_mismatch(self) -> None:
        entries = list(_make_entry_chain(1))
        bad = dataclasses.replace(entries[0], entry_hash="f" * 128)
        result = verify_chain((bad,))
        assert result.chain_intact is False
        assert result.failure_code == F_BT9_01
        assert "entry_hash" in result.failure_detail

    def test_content_hash_mismatch(self) -> None:
        # Build a valid genesis, then tamper content_hash (also tamper
        # entry_hash to match the new body, so we hit the content_hash check
        # rather than the entry_hash check).
        entry = _make_entry_chain(1)[0]
        bogus_content_hash = "a" * 128
        new_entry_hash = compute_entry_hash(
            seq_id=entry.seq_id,
            utc_timestamp=entry.utc_timestamp,
            session_id=entry.session_id,
            org_slug=entry.org_slug,
            speaker=entry.speaker,
            content_hash=bogus_content_hash,
            prev_entry_hash=entry.prev_entry_hash,
            corrects=entry.corrects,
        )
        bad = dataclasses.replace(
            entry,
            content_hash=bogus_content_hash,
            entry_hash=new_entry_hash,
        )
        result = verify_chain((bad,))
        assert result.chain_intact is False
        assert result.failure_code == F_BT9_01
        assert "content_hash" in result.failure_detail

    def test_non_entry_in_sequence_rejected(self) -> None:
        result = verify_chain(("not-an-entry",))  # type: ignore[arg-type]
        assert result.chain_intact is False
        assert result.failure_code == F_BT9_01


# ---------------------------------------------------------------------------
# TestBuildAppendedEntry
# ---------------------------------------------------------------------------


class TestBuildAppendedEntry:
    def test_genesis_uses_zero_prev(self) -> None:
        entry = build_appended_entry(
            prior_entries=(),
            utc_timestamp="2026-04-19T00:00:00Z",
            session_id="sess-1",
            org_slug="fit_farms_llc",
            speaker="operator",
            content="hello",
            signer=_hmac_sign,
        )
        assert entry.seq_id == 1
        assert entry.prev_entry_hash == GENESIS_PREV_HASH

    def test_continuation_threads_prev_hash(self) -> None:
        entries = _make_entry_chain(2)
        assert entries[1].seq_id == 2
        assert entries[1].prev_entry_hash == entries[0].entry_hash

    def test_signer_called_with_signing_payload(self) -> None:
        captured: list[bytes] = []

        def cap_signer(payload: bytes) -> bytes:
            captured.append(payload)
            return b"sig-bytes"

        entry = build_appended_entry(
            prior_entries=(),
            utc_timestamp="2026-04-19T00:00:00Z",
            session_id="sess-1",
            org_slug="fit_farms_llc",
            speaker="scribe",
            content="hi",
            signer=cap_signer,
        )
        assert entry.session_key_signature == b"sig-bytes"
        assert captured == [signing_payload(entry)]

    def test_invalid_speaker_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_appended_entry(
                prior_entries=(),
                utc_timestamp="t",
                session_id="s",
                org_slug="o",
                speaker="hacker",
                content="x",
                signer=_hmac_sign,
            )

    def test_signer_must_return_bytes(self) -> None:
        with pytest.raises(TypeError):
            build_appended_entry(
                prior_entries=(),
                utc_timestamp="t",
                session_id="s",
                org_slug="o",
                speaker="operator",
                content="x",
                signer=lambda _payload: "not-bytes",  # type: ignore[arg-type,return-value]
            )

    def test_signer_must_be_callable(self) -> None:
        with pytest.raises(TypeError):
            build_appended_entry(
                prior_entries=(),
                utc_timestamp="t",
                session_id="s",
                org_slug="o",
                speaker="operator",
                content="x",
                signer="not-callable",  # type: ignore[arg-type]
            )

    def test_corrects_populated_when_set(self) -> None:
        first = _make_entry_chain(1)[0]
        retraction = build_appended_entry(
            prior_entries=(first,),
            utc_timestamp="2026-04-19T00:01:00Z",
            session_id="sess-1",
            org_slug="fit_farms_llc",
            speaker="operator",
            content="strike that",
            signer=_hmac_sign,
            corrects=first.entry_hash,
        )
        assert retraction.corrects == first.entry_hash


# ---------------------------------------------------------------------------
# TestVerifyUserDataAnchor — happy path + each FAIL pathway
# ---------------------------------------------------------------------------


class TestVerifyUserDataAnchor:
    def _log_text(self, entries) -> str:
        return "".join(serialise_entry_line(e) for e in entries)

    def test_happy_path_returns_pass(self) -> None:
        entries = _make_entry_chain(
            3,
            contents=[
                "We grow shiitake on hardwood substrate.",
                "Our 2025 yield was 4,200 lbs.",
                "We sell to three restaurants weekly.",
            ],
        )
        result = verify_user_data_anchor(
            claim_text="2025 yield was 4,200 lbs",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_FixedKeyVerifier(),
        )
        assert result.tag == "USER_DATA"
        assert result.verify_result == "PASS"
        assert result.verify_method == "conversation_anchor"
        assert result.matched_seq_id == 2
        assert result.matched_entry_hash == entries[1].entry_hash
        assert result.failure_code is None

    def test_empty_log_returns_missing_entry(self) -> None:
        result = verify_user_data_anchor(
            claim_text="foo",
            log_text="",
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_FixedKeyVerifier(),
        )
        assert result.tag == "UNSOURCED"
        assert result.failure_code == F_POST_05_MISSING_ENTRY

    def test_no_substring_match_returns_missing_entry(self) -> None:
        entries = _make_entry_chain(2, contents=["nothing here", "nor here"])
        result = verify_user_data_anchor(
            claim_text="never appears anywhere",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_FixedKeyVerifier(),
        )
        assert result.failure_code == F_POST_05_MISSING_ENTRY
        assert result.matched_seq_id is None

    def test_broken_chain_returns_invalid(self) -> None:
        entries = list(_make_entry_chain(2))
        bad = dataclasses.replace(entries[1], prev_entry_hash="9" * 128)
        result = verify_user_data_anchor(
            claim_text="utterance 1",
            log_text=self._log_text((entries[0], bad)),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_FixedKeyVerifier(),
        )
        assert result.failure_code == F_POST_05_INVALID
        assert "chain verify failed" in result.verify_detail

    def test_invalid_signature_returns_invalid(self) -> None:
        entries = _make_entry_chain(1, contents=["unique phrase here"])
        result = verify_user_data_anchor(
            claim_text="unique phrase",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_AlwaysInvalidVerifier(),
        )
        assert result.failure_code == F_POST_05_INVALID
        assert result.matched_seq_id == 1

    def test_wrong_key_returns_wrong_key(self) -> None:
        entries = _make_entry_chain(1, contents=["another phrase"])
        result = verify_user_data_anchor(
            claim_text="another phrase",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_AlwaysWrongKeyVerifier(),
        )
        assert result.failure_code == F_POST_05_WRONG_KEY
        assert result.matched_seq_id == 1

    def test_retired_key_still_passes(self) -> None:
        entries = _make_entry_chain(1, contents=["historic statement"])
        result = verify_user_data_anchor(
            claim_text="historic statement",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_AlwaysRetiredVerifier(),
        )
        assert result.tag == "USER_DATA"
        assert result.verify_result == "PASS"
        assert "BT6-retired" in result.verify_detail

    def test_unknown_status_returns_invalid(self) -> None:
        entries = _make_entry_chain(1, contents=["whatever"])
        result = verify_user_data_anchor(
            claim_text="whatever",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_UnknownStatusVerifier(),
        )
        assert result.failure_code == F_POST_05_INVALID
        assert "BANANA" in result.verify_detail

    def test_superseded_entry_returns_superseded(self) -> None:
        first = build_appended_entry(
            prior_entries=(),
            utc_timestamp="2026-04-19T00:00:00Z",
            session_id="sess-1",
            org_slug="fit_farms_llc",
            speaker="operator",
            content="our 2024 yield was 3000 lbs",
            signer=_hmac_sign,
        )
        retraction = build_appended_entry(
            prior_entries=(first,),
            utc_timestamp="2026-04-19T00:00:01Z",
            session_id="sess-1",
            org_slug="fit_farms_llc",
            speaker="operator",
            content="actually we miscounted that estimate",
            signer=_hmac_sign,
            corrects=first.entry_hash,
        )
        result = verify_user_data_anchor(
            claim_text="2024 yield was 3000 lbs",
            log_text=self._log_text((first, retraction)),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_FixedKeyVerifier(),
        )
        assert result.failure_code == F_POST_05_SUPERSEDED
        assert result.matched_seq_id == 1
        assert result.matched_entry_hash == first.entry_hash

    def test_session_id_mismatch_rejected(self) -> None:
        entries = _make_entry_chain(1)
        result = verify_user_data_anchor(
            claim_text="utterance 1",
            log_text=self._log_text(entries),
            expected_session_id="different-session",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_FixedKeyVerifier(),
        )
        assert result.failure_code == F_POST_05_INVALID
        assert "session_id" in result.verify_detail

    def test_org_slug_mismatch_rejected(self) -> None:
        entries = _make_entry_chain(1)
        result = verify_user_data_anchor(
            claim_text="utterance 1",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="mycosymbiotics_inc",
            signature_verifier=_FixedKeyVerifier(),
        )
        assert result.failure_code == F_POST_05_INVALID
        assert "org_slug" in result.verify_detail

    def test_case_insensitive_opt_in(self) -> None:
        entries = _make_entry_chain(1, contents=["WE GROW SHIITAKE"])
        result = verify_user_data_anchor(
            claim_text="we grow shiitake",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_FixedKeyVerifier(),
            case_sensitive=False,
        )
        assert result.tag == "USER_DATA"
        assert result.verify_result == "PASS"

    def test_case_sensitive_default_misses(self) -> None:
        entries = _make_entry_chain(1, contents=["WE GROW SHIITAKE"])
        result = verify_user_data_anchor(
            claim_text="we grow shiitake",
            log_text=self._log_text(entries),
            expected_session_id="sess-1",
            expected_org_slug="fit_farms_llc",
            signature_verifier=_FixedKeyVerifier(),
        )
        assert result.failure_code == F_POST_05_MISSING_ENTRY


# ---------------------------------------------------------------------------
# TestExceptions
# ---------------------------------------------------------------------------


class TestExceptions:
    def test_chain_broken_carries_code_and_detail(self) -> None:
        exc = ConversationLogChainBroken("prev_entry_hash mismatch")
        assert exc.code == F_BT9_01
        assert exc.detail == "prev_entry_hash mismatch"
        assert isinstance(exc, RuntimeError)

    def test_append_race_carries_code_and_detail(self) -> None:
        exc = ConversationLogAppendRace("seq_id 5 replayed")
        assert exc.code == F_BT9_03
        assert exc.detail == "seq_id 5 replayed"


# ---------------------------------------------------------------------------
# TestSessionKeyVerifierProtocol
# ---------------------------------------------------------------------------


class TestSessionKeyVerifierProtocol:
    def test_protocol_is_runtime_checkable(self) -> None:
        assert isinstance(_FixedKeyVerifier(), SessionKeyVerifier)
        assert isinstance(_AlwaysInvalidVerifier(), SessionKeyVerifier)

    def test_callable_only_object_is_not_a_verifier(self) -> None:
        # Plain function lacks .verify_entry method
        def f(entry):
            return "ACTIVE"

        assert not isinstance(f, SessionKeyVerifier)


# ---------------------------------------------------------------------------
# TestResultShape
# ---------------------------------------------------------------------------


class TestResultShape:
    def test_chain_verify_result_frozen_kw_only(self) -> None:
        r = ChainVerifyResult(
            chain_intact=True, head_seq_id=1, failure_code=None, failure_detail=""
        )
        assert dataclasses.is_dataclass(r)
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.chain_intact = False  # type: ignore[misc]
        with pytest.raises(TypeError):
            ChainVerifyResult(True, 1, None, "")  # type: ignore[misc]

    def test_anchor_verify_result_frozen_kw_only(self) -> None:
        r = AnchorVerifyResult(
            tag="USER_DATA",
            verify_result="PASS",
            verify_method="conversation_anchor",
            verify_detail="",
            matched_seq_id=1,
            matched_entry_hash="h",
            failure_code=None,
        )
        assert dataclasses.is_dataclass(r)
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.tag = "UNSOURCED"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestTypeGates
# ---------------------------------------------------------------------------


class TestTypeGates:
    def test_claim_text_must_be_str(self) -> None:
        with pytest.raises(TypeError):
            verify_user_data_anchor(
                claim_text=b"x",  # type: ignore[arg-type]
                log_text="",
                expected_session_id="s",
                expected_org_slug="o",
                signature_verifier=_FixedKeyVerifier(),
            )

    def test_log_text_must_be_str(self) -> None:
        with pytest.raises(TypeError):
            verify_user_data_anchor(
                claim_text="x",
                log_text=b"",  # type: ignore[arg-type]
                expected_session_id="s",
                expected_org_slug="o",
                signature_verifier=_FixedKeyVerifier(),
            )

    def test_session_id_must_be_str(self) -> None:
        with pytest.raises(TypeError):
            verify_user_data_anchor(
                claim_text="x",
                log_text="",
                expected_session_id=1,  # type: ignore[arg-type]
                expected_org_slug="o",
                signature_verifier=_FixedKeyVerifier(),
            )
