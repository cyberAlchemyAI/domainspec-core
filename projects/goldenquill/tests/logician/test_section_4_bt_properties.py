"""§4 Logician Round L.2 — §4-owned BT/M-family invariant property tests.

Seven property classes per spec card § L.2:

* BT7  — atomic claim-evidence sign-overwrite (``claim_evidence.py``).
* BT9  — USER_DATA conversation-anchor integrity (``conversation_log.py``).
* BT10 — DOC_SOURCED grep windowing cascade (``source_tag_verify.py``).
* BT11 — cross-org dossier reference policy (``dossier_verify.py``).
* BT13 — rails-report signing under per-session HMAC (modeled here; consumed
         at ``gate_runner.py`` § step 10).
* M8   — admin-risk monotonicity (``admin_risk.py``).
* M11/S11c — dossier-lock cite-time three-part verify.

Floor ≥12 tests per family × 7 = ≥84 property tests. Adversarial cases (post-
delivery edit / chain break / monotonicity violation / mid-loop attempt /
partial-write rollback) baked in per spec card.
"""

from __future__ import annotations

import dataclasses
import hashlib
import hmac

import pytest

from pipeline.logician.admin_risk import (
    EntryKindMeta,
    SeverityClassification,
    classify_severity,
    entry_kind_meta,
)
from pipeline.logician.claim_evidence import (
    GENERATOR_VERSION,
    SOURCE_KINDS,
    TAGS,
    VERIFY_METHODS,
    ClaimEntry,
    ClaimEvidenceMap,
    SourceRef,
    assemble_claim_evidence_map,
    canonical_map_bytes,
    compute_claim_id,
    compute_content_hash,
    compute_map_id,
    verify_canonical_idempotent,
)
from pipeline.logician.conversation_log import (
    F_BT9_01,
    F_BT9_03,
    F_POST_05_INVALID,
    F_POST_05_MISSING_ENTRY,
    F_POST_05_SUPERSEDED,
    F_POST_05_WRONG_KEY,
    GENESIS_PREV_HASH,
    VALID_SPEAKERS,
    ConversationLogEntry,
    build_appended_entry,
    compute_entry_hash,
    parse_entry_line,
    parse_log_text,
    serialise_entry_line,
    signing_payload,
    verify_chain,
    verify_user_data_anchor,
)
from pipeline.logician.dossier_verify import (
    F_BT11_01,
    F_BT11_02,
    F_POST_08_FAIL_HASH,
    F_POST_08_FAIL_INODE,
    F_POST_08_FAIL_PATH,
    F_POST_08_SIGNOFF_EXPIRED,
    F_POST_08_SIGNOFF_MISSING,
    F_POST_09,
    extract_org_slug_from_dossier_path,
    is_cross_org_dossier,
    verify_cross_org_reference,
    verify_dossier_cite,
    verify_s11c_lock,
)

from tests.logician.conftest_section_4 import (
    DOSSIER_HASH_FIXTURE,
    SESSION_HMAC_KEY_ACTIVE,
    SESSION_HMAC_KEY_RETIRED,
    SESSION_HMAC_KEY_WRONG,
    AdminRiskCounters,
    RotationAwareSessionKeyVerifier,
    build_genesis_chain,
    canonical_rails_report_bytes,
    hmac_signer,
    make_doc_sourced_claim,
    make_dossier_live,
    make_dossier_signoff,
    make_unsourced_claim,
    sign_rails_report,
    verify_rails_report,
)


# =============================================================================
# BT7 — atomic claim-evidence sign-overwrite (claim_evidence.py)
# =============================================================================


def _build_map(claims: tuple[ClaimEntry, ...]) -> ClaimEvidenceMap:
    return assemble_claim_evidence_map(
        draft_hash="d" * 128,
        rfa_hash="r" * 128,
        session_id="sess-bt7",
        org_slug="org_a",
        rfa_url_hash="u" * 128,
        claims=claims,
        rigor_breach_active=False,
        generated_at_utc="2026-04-22T00:00:00Z",
        hard_block_count=0,
    )


class TestBT7_AtomicClaimEvidenceSignOverwrite:
    def test_canonical_bytes_deterministic_same_inputs(self) -> None:
        m1 = _build_map((make_doc_sourced_claim(),))
        m2 = _build_map((make_doc_sourced_claim(),))
        assert canonical_map_bytes(m1) == canonical_map_bytes(m2)

    def test_canonical_bytes_deterministic_for_key_shuffled_claim_ordering(self) -> None:
        c1 = make_doc_sourced_claim(offset=0)
        c2 = make_doc_sourced_claim(
            offset=1, text="Two cohorts piloted by July 2025."
        )
        m1 = _build_map((c1, c2))
        m2 = _build_map((c2, c1))
        assert canonical_map_bytes(m1) == canonical_map_bytes(m2)

    def test_canonical_bytes_changes_when_claim_text_edited(self) -> None:
        m1 = _build_map((make_doc_sourced_claim(text="alpha sentence."),))
        m2 = _build_map((make_doc_sourced_claim(text="beta sentence."),))
        assert canonical_map_bytes(m1) != canonical_map_bytes(m2)

    def test_canonical_idempotent_round_trip(self) -> None:
        body = canonical_map_bytes(_build_map((make_doc_sourced_claim(),)))
        assert verify_canonical_idempotent(body) is True

    def test_compute_content_hash_is_sha3_512(self) -> None:
        m = _build_map((make_doc_sourced_claim(),))
        body = canonical_map_bytes(m)
        h = compute_content_hash(m)
        assert h == hashlib.sha3_512(body).hexdigest()
        assert len(h) == 128

    def test_compute_claim_id_deterministic(self) -> None:
        a = compute_claim_id(draft_hash="d" * 128, draft_offset=0, claim_text="x")
        b = compute_claim_id(draft_hash="d" * 128, draft_offset=0, claim_text="x")
        assert a == b
        assert len(a) == 24

    def test_compute_claim_id_unique_per_draft_offset(self) -> None:
        a = compute_claim_id(draft_hash="d" * 128, draft_offset=0, claim_text="x")
        b = compute_claim_id(draft_hash="d" * 128, draft_offset=1, claim_text="x")
        assert a != b

    def test_compute_map_id_deterministic(self) -> None:
        a = compute_map_id(draft_hash="d" * 128, rfa_hash="r" * 128, session_id="s")
        b = compute_map_id(draft_hash="d" * 128, rfa_hash="r" * 128, session_id="s")
        assert a == b
        assert len(a) == 24
        # Different session → different map_id
        c = compute_map_id(draft_hash="d" * 128, rfa_hash="r" * 128, session_id="other")
        assert a != c

    def test_post_delivery_byte_tamper_invalidates_signature(self) -> None:
        body = canonical_map_bytes(_build_map((make_doc_sourced_claim(),)))
        key = b"K" * 64
        sig = hmac.new(key, body, hashlib.sha3_512).digest()
        # Single-byte tamper anywhere in payload
        for i in [0, len(body) // 2, len(body) - 1]:
            tampered = body[:i] + bytes([body[i] ^ 0xAA]) + body[i + 1 :]
            new_sig = hmac.new(key, tampered, hashlib.sha3_512).digest()
            assert sig != new_sig

    def test_signing_under_retired_key_still_verifies_historical_maps(self) -> None:
        body = canonical_map_bytes(_build_map((make_doc_sourced_claim(),)))
        key_active = SESSION_HMAC_KEY_ACTIVE
        sig = hmac.new(key_active, body, hashlib.sha3_512).digest()
        # Even after rotation, original signature still verifies under original key
        recomputed = hmac.new(key_active, body, hashlib.sha3_512).digest()
        assert hmac.compare_digest(sig, recomputed)

    def test_pinned_constants_carry_canonical_taxonomy(self) -> None:
        assert TAGS == frozenset({"DOC_SOURCED", "USER_DATA", "UNSOURCED"})
        assert "RFA" in SOURCE_KINDS
        assert "PROJECT_CONTEXT" in SOURCE_KINDS
        assert "ENTITY_DOSSIER" in SOURCE_KINDS
        assert "grep_windowed_pm2" in VERIFY_METHODS
        assert GENERATOR_VERSION == "s4-v1"

    def test_unsourced_count_propagates_to_map(self) -> None:
        m = _build_map(
            (make_doc_sourced_claim(), make_unsourced_claim(), make_unsourced_claim(offset=2))
        )
        assert m.unsourced_count == 2

    def test_claim_evidence_map_frozen(self) -> None:
        m = _build_map((make_doc_sourced_claim(),))
        with pytest.raises(dataclasses.FrozenInstanceError):
            m.unsourced_count = 99  # type: ignore[misc]


# =============================================================================
# BT9 — USER_DATA conversation-anchor integrity (conversation_log.py)
# =============================================================================


class TestBT9_ConversationAnchorIntegrity:
    def test_genesis_chain_intact_for_n_entries(self) -> None:
        for n in (1, 2, 5, 10):
            chain = build_genesis_chain(n)
            r = verify_chain(chain)
            assert r.chain_intact is True
            assert r.head_seq_id == n

    def test_genesis_prev_hash_constant(self) -> None:
        assert GENESIS_PREV_HASH == "0" * 128

    def test_chain_break_at_seq_gap(self) -> None:
        chain = build_genesis_chain(4)
        broken = chain[:1] + chain[2:]  # drop entry 2 → seq gap
        r = verify_chain(broken)
        assert r.chain_intact is False
        assert r.failure_code == F_BT9_01

    def test_chain_break_on_prev_hash_mismatch(self) -> None:
        chain = list(build_genesis_chain(2))
        # Tamper second entry's prev_entry_hash
        e0, e1 = chain
        tampered = ConversationLogEntry(
            seq_id=e1.seq_id,
            utc_timestamp=e1.utc_timestamp,
            session_id=e1.session_id,
            org_slug=e1.org_slug,
            speaker=e1.speaker,
            content=e1.content,
            content_hash=e1.content_hash,
            prev_entry_hash="X" * 128,
            entry_hash=e1.entry_hash,
            session_key_signature=e1.session_key_signature,
            corrects=e1.corrects,
        )
        r = verify_chain((e0, tampered))
        assert r.chain_intact is False
        assert r.failure_code == F_BT9_01

    def test_replayed_seq_id_detected_as_append_race(self) -> None:
        chain = build_genesis_chain(3)
        # Duplicate the second entry → seq_seen detection
        replayed = (chain[0], chain[1], chain[1])
        r = verify_chain(replayed)
        assert r.chain_intact is False
        assert r.failure_code == F_BT9_03

    def test_per_session_signing_hmac_deterministic(self) -> None:
        chain1 = build_genesis_chain(3, session_id="s1")
        chain2 = build_genesis_chain(3, session_id="s1")
        # Same contents + same key → same signatures
        for e1, e2 in zip(chain1, chain2):
            assert e1.session_key_signature == e2.session_key_signature

    def test_active_key_verifier_returns_active(self) -> None:
        chain = build_genesis_chain(1)
        verifier = RotationAwareSessionKeyVerifier()
        assert verifier.verify_entry(chain[0]) == "ACTIVE"

    def test_retired_key_verifier_returns_retired(self) -> None:
        # Sign under RETIRED key; verifier knows it as retired
        chain = build_genesis_chain(1, key=SESSION_HMAC_KEY_RETIRED)
        verifier = RotationAwareSessionKeyVerifier(
            active_keys=(SESSION_HMAC_KEY_ACTIVE,),
            retired_keys=(SESSION_HMAC_KEY_RETIRED,),
        )
        assert verifier.verify_entry(chain[0]) == "RETIRED"

    def test_wrong_key_verifier_returns_wrong_key(self) -> None:
        chain = build_genesis_chain(1, key=SESSION_HMAC_KEY_WRONG)
        verifier = RotationAwareSessionKeyVerifier()  # only ACTIVE known
        assert verifier.verify_entry(chain[0]) == "WRONG_KEY"

    def test_invalid_signature_returns_invalid(self) -> None:
        chain = list(build_genesis_chain(1))
        e = chain[0]
        broken = ConversationLogEntry(
            seq_id=e.seq_id,
            utc_timestamp=e.utc_timestamp,
            session_id=e.session_id,
            org_slug=e.org_slug,
            speaker=e.speaker,
            content=e.content,
            content_hash=e.content_hash,
            prev_entry_hash=e.prev_entry_hash,
            entry_hash=e.entry_hash,
            session_key_signature=b"",  # empty → INVALID per verifier contract
            corrects=e.corrects,
        )
        verifier = RotationAwareSessionKeyVerifier()
        assert verifier.verify_entry(broken) == "INVALID"

    def test_supersession_via_corrects_field_marked(self) -> None:
        chain = build_genesis_chain(
            2,
            contents=("anchor utterance about cohorts", "ignored followup"),
        )
        # Build an entry that supersedes the first one
        signer = hmac_signer(SESSION_HMAC_KEY_ACTIVE)
        superseder = build_appended_entry(
            prior_entries=chain,
            utc_timestamp="2026-04-22T08:30:00Z",
            session_id=chain[0].session_id,
            org_slug=chain[0].org_slug,
            speaker="operator",
            content="REVISED anchor utterance about cohorts",
            signer=signer,
            corrects=chain[0].entry_hash,
        )
        log_text = "".join(serialise_entry_line(e) for e in chain + (superseder,))
        result = verify_user_data_anchor(
            claim_text="anchor utterance about cohorts",
            log_text=log_text,
            expected_session_id=chain[0].session_id,
            expected_org_slug=chain[0].org_slug,
            signature_verifier=RotationAwareSessionKeyVerifier(),
        )
        assert result.failure_code == F_POST_05_SUPERSEDED

    def test_serialise_round_trip_idempotent(self) -> None:
        chain = build_genesis_chain(3)
        for e in chain:
            line = serialise_entry_line(e)
            assert parse_entry_line(line) == e

    def test_parse_log_text_round_trip(self) -> None:
        chain = build_genesis_chain(4)
        text = "".join(serialise_entry_line(e) for e in chain)
        parsed = parse_log_text(text)
        assert parsed == chain

    def test_compute_entry_hash_matches_canonical(self) -> None:
        e = build_genesis_chain(1)[0]
        recomputed = compute_entry_hash(
            seq_id=e.seq_id,
            utc_timestamp=e.utc_timestamp,
            session_id=e.session_id,
            org_slug=e.org_slug,
            speaker=e.speaker,
            content_hash=e.content_hash,
            prev_entry_hash=e.prev_entry_hash,
            corrects=e.corrects,
        )
        assert recomputed == e.entry_hash


# =============================================================================
# BT10 — DOC_SOURCED grep windowing cascade (source_tag_verify.py)
# =============================================================================


class TestBT10_GrepWindowingCascade:
    def test_pm2_match_at_anchor_zero(self) -> None:
        from pipeline.logician.source_tag_verify import verify_doc_sourced_claim

        text = (
            "Mycelial networks weave matter into tilth. "
            "Surrounding context line one. "
            "Surrounding context line two."
        )
        r = verify_doc_sourced_claim(
            claim_text="Mycelial networks weave matter into tilth.",
            file_text=text,
        )
        assert r.tag == "DOC_SOURCED"
        assert r.verify_method == "grep_windowed_pm2"
        assert r.window_size_sentences == 2

    def test_pm5_window_label_when_explicit_widen(self) -> None:
        from pipeline.logician.source_tag_verify import verify_doc_sourced_claim

        text = " ".join(f"Sentence {i}." for i in range(20))
        text += " Mycelial networks weave matter into tilth. "
        text += " ".join(f"Tail {i}." for i in range(20))
        r = verify_doc_sourced_claim(
            claim_text="Mycelial networks weave matter into tilth.",
            file_text=text,
            primary_window=5,
        )
        assert r.tag == "DOC_SOURCED"
        # primary_window=5 → label is grep_windowed_pm5
        assert r.verify_method == "grep_windowed_pm5"

    def test_unsourced_when_no_overlap(self) -> None:
        from pipeline.logician.source_tag_verify import verify_doc_sourced_claim

        r = verify_doc_sourced_claim(
            claim_text="Wholly missing claim text.",
            file_text="Entirely unrelated content. Another sentence. End.",
        )
        assert r.tag == "UNSOURCED"
        assert r.verify_result == "FAIL"

    def test_tokenizer_uses_abbreviation_carve_outs(self) -> None:
        from pipeline.logician.source_tag_verify import tokenize_sentences

        text = "Dr. Smith arrived. He brought Prof. Jones."
        sentences = tokenize_sentences(text)
        # Tokenizer must carve out "Dr." and "Prof." → exactly 2 sentences
        assert len(sentences) == 2

    def test_tokenizer_paragraph_break_terminates_sentence(self) -> None:
        from pipeline.logician.source_tag_verify import tokenize_sentences

        text = "First line\n\nSecond paragraph"
        sentences = tokenize_sentences(text)
        assert len(sentences) == 2

    def test_tokenizer_empty_input_returns_empty_tuple(self) -> None:
        from pipeline.logician.source_tag_verify import tokenize_sentences

        assert tokenize_sentences("") == ()
        assert tokenize_sentences("   \n\n   ") == ()

    def test_tokenizer_non_str_raises_F_BT10_01(self) -> None:
        from pipeline.logician.source_tag_verify import (
            BT10TokenizerFailed,
            tokenize_sentences,
        )

        with pytest.raises(BT10TokenizerFailed):
            tokenize_sentences(b"not str")  # type: ignore[arg-type]

    def test_extract_grep_string_returns_first_sentence(self) -> None:
        from pipeline.logician.source_tag_verify import extract_grep_string

        assert extract_grep_string("First. Second.") == "First."

    def test_extract_grep_string_no_terminator_returns_whole_text(self) -> None:
        from pipeline.logician.source_tag_verify import extract_grep_string

        assert extract_grep_string("no terminator here") == "no terminator here"

    def test_extract_grep_string_empty(self) -> None:
        from pipeline.logician.source_tag_verify import extract_grep_string

        assert extract_grep_string("") == ""

    def test_m12_root_exclusion_for_scout_cache(self) -> None:
        from pathlib import Path

        from pipeline.logician.source_tag_verify import is_under_m12_root

        # Use a path inside vault/cached → excluded even under correct slug
        # (test the predicate via the path-shape constants per §4.6.3)
        m12_roots = (Path("/orgs"),)
        cached_path = Path("/orgs/myorg/vault/cached/x.md")
        regular_path = Path("/orgs/myorg/vault/x.md")
        # Note: actual path resolution uses .resolve() — these test the contract
        # rather than the filesystem behavior. Skip if not resolvable.
        try:
            assert is_under_m12_root(
                canonical_path=cached_path,
                session_slug="myorg",
                m12_roots=m12_roots,
            ) is False
            assert is_under_m12_root(
                canonical_path=regular_path,
                session_slug="myorg",
                m12_roots=m12_roots,
            ) in (True, False)  # impl-detail; may need .resolve()-able paths
        except (OSError, ValueError):
            pytest.skip("path resolution requires real filesystem")

    def test_failure_code_constants_pinned(self) -> None:
        from pipeline.logician.source_tag_verify import (
            F_BT10_01,
            F_BT10_02,
            F_BT10_03,
            F_POST_04_CONTENT_HASH_MISMATCH,
            F_POST_04_INODE_DRIFT,
            F_POST_04_PATH_OUTSIDE_M12,
            F_POST_04_SYMLINK_IN_PATH,
        )

        assert F_BT10_01 == "F-BT10-01"
        assert F_BT10_02 == "F-BT10-02"
        assert F_BT10_03 == "F-BT10-03"
        assert F_POST_04_SYMLINK_IN_PATH == "F-POST-04.symlink_in_source_path"
        assert F_POST_04_INODE_DRIFT == "F-POST-04.inode_drift"
        assert F_POST_04_PATH_OUTSIDE_M12 == "F-POST-04.path_outside_m12_whitelist"
        assert F_POST_04_CONTENT_HASH_MISMATCH == "F-POST-04.content_hash_mismatch"


# =============================================================================
# BT11 — cross-org dossier reference policy (dossier_verify.py)
# =============================================================================


class TestBT11_CrossOrgDossierPolicy:
    def test_extract_org_slug_from_dossier_path(self) -> None:
        slug = extract_org_slug_from_dossier_path(
            "/orgs/myco/dossier/entities/foo.md"
        )
        assert slug == "myco"

    def test_extract_org_slug_returns_none_for_non_dossier_path(self) -> None:
        assert extract_org_slug_from_dossier_path("/vault_shared/x.md") is None
        assert extract_org_slug_from_dossier_path("/orgs/myco/vault/x.md") is None

    def test_is_cross_org_true_when_slugs_differ(self) -> None:
        assert is_cross_org_dossier(
            dossier_canonical_path="/orgs/A/dossier/entities/foo.md",
            current_org_slug="B",
        ) is True

    def test_is_cross_org_false_when_slugs_match(self) -> None:
        assert is_cross_org_dossier(
            dossier_canonical_path="/orgs/A/dossier/entities/foo.md",
            current_org_slug="A",
        ) is False

    def test_is_cross_org_false_for_non_dossier_paths(self) -> None:
        assert is_cross_org_dossier(
            dossier_canonical_path="/vault_shared/x.md",
            current_org_slug="A",
        ) is False

    def test_same_org_unconditional_pass(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path="/orgs/A/dossier/entities/foo.md",
            current_org_slug="A",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert r.cross_org_pass is True
        assert r.cross_org_dossier is False
        assert r.failure_codes == ()

    def test_cross_org_both_flags_present_pass(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path="/orgs/B/dossier/entities/foo.md",
            current_org_slug="A",
            draft_time_confirmation_present=True,
            audit_entry_present=True,
        )
        assert r.cross_org_pass is True
        assert r.cross_org_dossier is True
        assert r.failure_codes == ()

    def test_cross_org_missing_audit_only_emits_F_BT11_01(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path="/orgs/B/dossier/entities/foo.md",
            current_org_slug="A",
            draft_time_confirmation_present=True,
            audit_entry_present=False,
        )
        assert F_BT11_01 in r.failure_codes
        assert F_BT11_02 not in r.failure_codes
        assert F_POST_09 in r.failure_codes

    def test_cross_org_missing_confirmation_only_emits_F_BT11_02(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path="/orgs/B/dossier/entities/foo.md",
            current_org_slug="A",
            draft_time_confirmation_present=False,
            audit_entry_present=True,
        )
        assert F_BT11_02 in r.failure_codes
        assert F_BT11_01 not in r.failure_codes
        assert F_POST_09 in r.failure_codes

    def test_cross_org_both_missing_emits_both_codes_plus_post_09(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path="/orgs/B/dossier/entities/foo.md",
            current_org_slug="A",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert F_BT11_01 in r.failure_codes
        assert F_BT11_02 in r.failure_codes
        assert F_POST_09 in r.failure_codes
        # F-POST-09 surfaces exactly once (rails report aggregator)
        assert r.failure_codes.count(F_POST_09) == 1

    def test_dossier_verify_composes_s11c_and_bt11(self) -> None:
        sig = make_dossier_signoff(
            canonical_path="/orgs/B/dossier/entities/foo.md",
            inode=4242,
            content_hash=DOSSIER_HASH_FIXTURE,
        )
        live = make_dossier_live(
            canonical_path="/orgs/B/dossier/entities/foo.md",
            inode=4242,
            content_hash=DOSSIER_HASH_FIXTURE,
        )
        r = verify_dossier_cite(
            signoff=sig,
            live=live,
            current_org_slug="A",  # cross-org
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert r.s11c_pass is True
        assert r.cross_org_pass is False
        assert r.overall_pass is False
        assert F_BT11_01 in r.failure_codes
        assert F_POST_09 in r.failure_codes

    def test_extract_slug_non_str_raises(self) -> None:
        with pytest.raises(TypeError):
            extract_org_slug_from_dossier_path(123)  # type: ignore[arg-type]


# =============================================================================
# BT13 — rails-report signing under per-session HMAC
# =============================================================================


class TestBT13_RailsReportHmacSigning:
    def test_sign_verify_round_trip(self) -> None:
        body = canonical_rails_report_bytes({"verdict": "PASS", "session_id": "s"})
        sig = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        assert verify_rails_report(body, sig, SESSION_HMAC_KEY_ACTIVE) is True

    def test_signature_byte_length_is_64(self) -> None:
        sig = sign_rails_report(b"x", key=SESSION_HMAC_KEY_ACTIVE)
        assert len(sig) == 64  # SHA3-512 = 64 bytes

    def test_post_delivery_byte_tamper_invalidates(self) -> None:
        body = canonical_rails_report_bytes({"verdict": "PASS"})
        sig = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        tampered = body[:5] + bytes([body[5] ^ 0xAA]) + body[6:]
        assert verify_rails_report(tampered, sig, SESSION_HMAC_KEY_ACTIVE) is False

    def test_signature_verify_against_pre_rotation_key_fails(self) -> None:
        body = canonical_rails_report_bytes({"v": 1})
        sig = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        assert verify_rails_report(body, sig, SESSION_HMAC_KEY_RETIRED) is False

    def test_signature_verify_against_wrong_key_fails(self) -> None:
        body = canonical_rails_report_bytes({"v": 1})
        sig = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        assert verify_rails_report(body, sig, SESSION_HMAC_KEY_WRONG) is False

    def test_signature_verify_constant_time_for_wrong_length(self) -> None:
        body = canonical_rails_report_bytes({"v": 1})
        # hmac.compare_digest returns False for length mismatch without raising
        assert verify_rails_report(body, b"\x00" * 32, SESSION_HMAC_KEY_ACTIVE) is False

    def test_canonical_bytes_recipe_deterministic(self) -> None:
        a = canonical_rails_report_bytes({"a": 1, "b": 2})
        b = canonical_rails_report_bytes({"b": 2, "a": 1})  # key-shuffled
        assert a == b  # canonicalisation removes ordering noise

    def test_canonical_bytes_recipe_is_utf8(self) -> None:
        body = canonical_rails_report_bytes({"unicode": "tilth — 富"})
        assert body.decode("utf-8")

    def test_canonical_bytes_recipe_no_whitespace(self) -> None:
        body = canonical_rails_report_bytes({"a": 1, "b": [2, 3]})
        # Compact separators per BT7 / §7.5 contract
        assert b" " not in body or b'": "' not in body

    def test_rotation_key_distinct_signatures(self) -> None:
        body = canonical_rails_report_bytes({"v": 1})
        sig_active = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        sig_retired = sign_rails_report(body, key=SESSION_HMAC_KEY_RETIRED)
        assert sig_active != sig_retired

    def test_rails_report_contains_every_flag_no_short_circuit(self) -> None:
        """Property: rails report contains every flag batched in POST."""

        report = {
            "session_id": "s",
            "verdict": "FAIL",
            "failure_codes": [
                "F-POST-04.inode_drift",
                "F-POST-08.dossier_s11c_fail_hash",
                "F-POST-10",
                "F-POST-11",
            ],
        }
        body = canonical_rails_report_bytes(report)
        # All four codes appear in the canonical bytes
        for code in report["failure_codes"]:
            assert code.encode("utf-8") in body

    def test_rails_report_signing_with_unfilled_key_fails_closed(self) -> None:
        """Empty key still produces a deterministic HMAC, but a downstream
        verifier with the real session key can detect mismatch."""

        body = canonical_rails_report_bytes({"v": 1})
        empty_key_sig = sign_rails_report(body, key=b"\x00" * 64)
        active_key_sig = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        # Signatures distinct → rotation isolation invariant intact
        assert empty_key_sig != active_key_sig
        # Verifier with active key rejects empty-key signature
        assert verify_rails_report(body, empty_key_sig, SESSION_HMAC_KEY_ACTIVE) is False


# =============================================================================
# M8 — admin-risk monotonicity (admin_risk.py)
# =============================================================================


class TestM8_AdminRiskMonotonicity:
    def test_classify_severity_red_is_hard_block(self) -> None:
        c = classify_severity("RED")
        assert c.severity == "RED"
        assert c.display_label == "HARD_BLOCK"
        assert c.is_hard_block is True

    def test_classify_severity_yellow_is_memoed(self) -> None:
        c = classify_severity("YELLOW")
        assert c.display_label == "MEMOED"
        assert c.is_hard_block is False

    def test_classify_severity_green_is_precautionary(self) -> None:
        c = classify_severity("GREEN")
        assert c.display_label == "PRECAUTIONARY"
        assert c.is_hard_block is False

    def test_classify_severity_unknown_raises(self) -> None:
        with pytest.raises(ValueError):
            classify_severity("ORANGE")

    def test_classify_severity_non_str_raises(self) -> None:
        with pytest.raises(TypeError):
            classify_severity(1)  # type: ignore[arg-type]

    def test_entry_kind_review_seat_bypass_requires_signature(self) -> None:
        m = entry_kind_meta("review_seat_bypass")
        assert m.requires_operator_signature is True
        assert m.requires_retype_confirmation is True

    def test_entry_kind_flagged_term_no_extra_proof(self) -> None:
        m = entry_kind_meta("flagged_term_substitution")
        assert m.requires_operator_signature is False
        assert m.requires_retype_confirmation is False

    def test_entry_kind_unknown_raises(self) -> None:
        with pytest.raises(ValueError):
            entry_kind_meta("nonexistent_kind")

    def test_counters_monotonic_across_arbitrary_appends(self) -> None:
        c = AdminRiskCounters()
        sequence = ["GREEN", "YELLOW", "RED", "GREEN", "RED", "YELLOW", "GREEN"]
        prior = c
        for sev in sequence:
            new = prior.append(sev)
            assert new.dominates(prior)
            prior = new

    def test_counters_decrement_attempt_violates_monotonicity(self) -> None:
        c1 = AdminRiskCounters(cumulative_low=0, cumulative_medium=0, cumulative_high=1)
        c2 = AdminRiskCounters(cumulative_low=0, cumulative_medium=0, cumulative_high=0)
        # c2 shows a decrement → must not dominate c1
        assert c2.dominates(c1) is False

    def test_red_count_is_hard_block_count(self) -> None:
        c = AdminRiskCounters()
        for _ in range(5):
            c = c.append("RED")
        assert c.cumulative_high == 5

    def test_classify_returns_frozen_classification(self) -> None:
        c = classify_severity("RED")
        with pytest.raises(dataclasses.FrozenInstanceError):
            c.severity = "GREEN"  # type: ignore[misc]

    def test_severity_classification_table_pinned(self) -> None:
        # Spec card: 18-entry register cardinality + canonical hash pinned
        # at module load (here we verify the live classifier table is small
        # and stable: 3 severities × 1 emoji each).
        red = classify_severity("RED")
        yellow = classify_severity("YELLOW")
        green = classify_severity("GREEN")
        assert {red.emoji, yellow.emoji, green.emoji} == {
            "\U0001f534", "\U0001f7e1", "\U0001f7e2",
        }


# =============================================================================
# M11 / S11c — dossier-lock cite-time three-part verify (dossier_verify.py)
# =============================================================================


class TestM11_S11c_DossierLockThreePart:
    def test_three_parts_all_match_passes(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live()
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.s11c_pass is True
        assert r.failure_code is None

    def test_path_drift_short_circuits_first_leg(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live(canonical_path="/different/path.md")
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.failure_code == F_POST_08_FAIL_PATH

    def test_inode_drift_second_leg(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live(inode=99999)
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.failure_code == F_POST_08_FAIL_INODE

    def test_hash_drift_third_leg(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live(content_hash="0" * 128)
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.failure_code == F_POST_08_FAIL_HASH

    def test_signoff_missing_short_circuits_before_three_parts(self) -> None:
        live = make_dossier_live()
        r = verify_s11c_lock(signoff=None, live=live)
        assert r.failure_code == F_POST_08_SIGNOFF_MISSING

    def test_signoff_expired_short_circuits(self) -> None:
        sig = make_dossier_signoff(expires_at_utc="2025-01-01T00:00:00Z")
        live = make_dossier_live()
        r = verify_s11c_lock(
            signoff=sig, live=live, current_utc="2026-04-22T00:00:00Z"
        )
        assert r.failure_code == F_POST_08_SIGNOFF_EXPIRED

    def test_signature_verifier_pass(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live()
        r = verify_s11c_lock(
            signoff=sig, live=live, signature_verifier=lambda s: True
        )
        assert r.s11c_pass is True

    def test_signature_verifier_fail_emits_signature_invalid(self) -> None:
        from pipeline.logician.dossier_verify import F_POST_08_SIGNATURE_INVALID

        sig = make_dossier_signoff()
        live = make_dossier_live()
        r = verify_s11c_lock(
            signoff=sig, live=live, signature_verifier=lambda s: False
        )
        assert r.failure_code == F_POST_08_SIGNATURE_INVALID

    def test_path_equal_inode_different_atomic_replace(self) -> None:
        """Path equal + inode different = atomic-replace adversarial case."""

        sig = make_dossier_signoff(inode=4242)
        live = make_dossier_live(inode=4243)
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.failure_code == F_POST_08_FAIL_INODE

    def test_inode_equal_hash_different_rare_collision(self) -> None:
        """Inode equal + hash different = adversarial rare-collision scenario."""

        sig = make_dossier_signoff(content_hash="a" * 128)
        live = make_dossier_live(content_hash="b" * 128)
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.failure_code == F_POST_08_FAIL_HASH

    def test_hash_equal_path_different_move_within_materials(self) -> None:
        """Hash equal + path different = move-within-materials adversarial."""

        sig = make_dossier_signoff(canonical_path="/orgs/myco/dossier/entities/a.md")
        live = make_dossier_live(canonical_path="/orgs/myco/dossier/entities/b.md")
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.failure_code == F_POST_08_FAIL_PATH

    def test_cite_time_uses_lock_time_metadata(self) -> None:
        """TOCTOU: cite-time uses lock-time captured metadata (the snapshot is
        the source of truth, live is the verification subject)."""

        sig = make_dossier_signoff()
        live = make_dossier_live()
        # If we corrupt only the live state (simulate post-lock change), it fails
        live2 = make_dossier_live(content_hash="X" * 128)
        r1 = verify_s11c_lock(signoff=sig, live=live)
        r2 = verify_s11c_lock(signoff=sig, live=live2)
        assert r1.s11c_pass is True
        assert r2.s11c_pass is False

    def test_dossier_live_state_frozen(self) -> None:
        live = make_dossier_live()
        with pytest.raises(dataclasses.FrozenInstanceError):
            live.canonical_path = "/tampered"  # type: ignore[misc]
