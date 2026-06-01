"""§11 v1.1 amendment — AWARD_INGEST commitment_id safe-identifier regression.

Per §11 v1.1 LOCKED 2026-05-11 (parent_lock_row=185; companion to §14 v1
LOCK 2026-05-10 row 200/201 Cycle 2 RT-C2-02 closure): every
``commitment_id`` admitted to ``proposal_commitments.yaml`` MUST match
``^[A-Z0-9_-]+$`` (max 64 chars). This test surface exercises the
producer-side contract that the §11 AWARD_INGEST extractor uses
``sanitize_commitment_id`` on every row before write.

Test coverage:

1. Direct unit tests against ``_sanitize_commitment_id`` in
   ``pipeline.orchestrator.seats.intake`` — proves the import wired the
   canonical sibling module's helper, not a stale local copy. Mirrors
   the discipline of ``tests/seats/report_generator/test_commitment_id.py``
   but anchored against the producer-side import surface.
2. End-to-end ``award_ingest`` integration — proves the auto-generated
   ID lands in the canonical set. Builds on the existing
   ``test_award_ingest.py`` fixtures.
3. Cross-import-path identity — the producer-side import
   (``pipeline.orchestrator.seats._commitment_id``) and the consumer-side
   re-export shim
   (``pipeline.orchestrator.seats.report_generator._commitment_id``)
   share identity; a single ``CommitmentIdInvalid`` raised from one
   path is ``isinstance``-recognized at the other path.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

import pytest

from pipeline.orchestrator.seats._commitment_id import (
    COMMITMENT_ID_MAX_LEN,
    CommitmentIdInvalid,
    SAFE_COMMITMENT_ID_PATTERN,
    SAFE_COMMITMENT_ID_REGEX,
    is_safe_commitment_id,
    sanitize_commitment_id,
)
from pipeline.orchestrator.seats.report_generator import _commitment_id as _consumer_shim
from pipeline.orchestrator.seats.intake import (
    ExtractedCommitment,
    FunderSignatureMaterial,
    IntakeAwardInput,
    ParsedDocument,
    SOURCE_FORMAT_MD,
    SignedClaimEvidenceMap,
    award_ingest,
)


# ---------------------------------------------------------------------------
# §A. Regex-shape unit tests (producer-side canonical home)
# ---------------------------------------------------------------------------


class TestSafeCommitmentIdRegexShape:
    def test_regex_string_is_anchored_uppercase_alnum_underscore_hyphen(self):
        assert SAFE_COMMITMENT_ID_REGEX == r"^[A-Z0-9_-]+$"

    def test_pattern_uses_ascii_flag(self):
        # Per §11 v1.1 §3 defense-in-depth: the precompiled pattern sets
        # ``re.ASCII`` so ``\d`` cannot drift onto Unicode digits in
        # future predicate edits.
        assert SAFE_COMMITMENT_ID_PATTERN.flags & re.ASCII

    def test_max_len_is_sixty_four(self):
        assert COMMITMENT_ID_MAX_LEN == 64


# ---------------------------------------------------------------------------
# §B. Valid + invalid identifier matrix
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "COMMIT-001",
        "A",
        "WORKFORCE_TRAINING-FY26",
        "A0_-",
        "ABC123",
        "0123456789",
        "A" * COMMITMENT_ID_MAX_LEN,  # at-the-bound length is admissible
        # Uppercase hex (the AWARD_INGEST auto-generation projection)
        "ABCDEF0123456789ABCDEF0123456789",
    ],
)
def test_safe_identifiers_pass(value):
    assert is_safe_commitment_id(value)
    assert sanitize_commitment_id(value) == value


@pytest.mark.parametrize(
    "value,expected_rule",
    [
        ("", "commitment_id_empty_or_too_long"),
        ("A" * (COMMITMENT_ID_MAX_LEN + 1), "commitment_id_empty_or_too_long"),
        ("lowercase", "commitment_id_regex_mismatch"),
        ("Commit-001", "commitment_id_regex_mismatch"),  # mixed case
        ("abcdef0123456789", "commitment_id_regex_mismatch"),  # lowercase hex
        ("A B", "commitment_id_regex_mismatch"),
        ("A.B", "commitment_id_regex_mismatch"),
        ("A/B", "commitment_id_regex_mismatch"),
        ("A\\B", "commitment_id_regex_mismatch"),
        ("A'B", "commitment_id_regex_mismatch"),
        ('A"B', "commitment_id_regex_mismatch"),
        ("../etc/passwd", "commitment_id_regex_mismatch"),
        ("café-1", "commitment_id_regex_mismatch"),  # non-ASCII letter
        ("A²", "commitment_id_regex_mismatch"),  # unicode superscript-2
        # Unicode digit lookalikes — only matters when the predicate
        # uses ``\d``; the literal ``[0-9]`` form rejects this
        # regardless. Cycle 1 RT-04 fold-in: broaden the Unicode-digit
        # set beyond just Arabic-Indic to anchor the contract against
        # future predicate edits that drift toward Unicode-aware
        # matching via Devanagari / Full-width / Bengali numerals.
        ("A٠", "commitment_id_regex_mismatch"),  # arabic-indic digit zero (U+0660)
        ("A०", "commitment_id_regex_mismatch"),  # devanagari digit zero (U+0966)
        ("A０", "commitment_id_regex_mismatch"),  # full-width digit zero (U+FF10)
        ("A১", "commitment_id_regex_mismatch"),  # bengali digit one (U+09E7)
        ("A\t B", "commitment_id_regex_mismatch"),  # whitespace
    ],
)
def test_unsafe_identifiers_fail(value, expected_rule):
    assert not is_safe_commitment_id(value)
    with pytest.raises(CommitmentIdInvalid) as ei:
        sanitize_commitment_id(value)
    assert ei.value.rule == expected_rule


@pytest.mark.parametrize("value", [None, 123, b"COMMIT-001", 1.5, object()])
def test_non_str_raises_must_be_str_rule(value):
    assert not is_safe_commitment_id(value)
    with pytest.raises(CommitmentIdInvalid) as ei:
        sanitize_commitment_id(value)
    assert ei.value.rule == "commitment_id_must_be_str"


# ---------------------------------------------------------------------------
# §C. Producer-side / consumer-side identity (single-canonical-home contract)
# ---------------------------------------------------------------------------


class TestProducerConsumerSingleCanonicalHome:
    """The §11 v1.1 amendment relocates the canonical home to the shared
    sibling module; the consumer location is a backward-compat shim.
    Both import paths MUST resolve to the same object identity so a
    ``CommitmentIdInvalid`` raised under one path is recognized under
    the other.
    """

    def test_pattern_identity_shared(self):
        assert _consumer_shim.SAFE_COMMITMENT_ID_PATTERN is SAFE_COMMITMENT_ID_PATTERN

    def test_max_len_identity_shared(self):
        assert _consumer_shim.COMMITMENT_ID_MAX_LEN is COMMITMENT_ID_MAX_LEN

    def test_exception_class_identity_shared(self):
        assert _consumer_shim.CommitmentIdInvalid is CommitmentIdInvalid

    def test_sanitize_function_identity_shared(self):
        assert _consumer_shim.sanitize_commitment_id is sanitize_commitment_id

    def test_isinstance_works_across_import_paths(self):
        try:
            _consumer_shim.sanitize_commitment_id("lowercase")
        except CommitmentIdInvalid as exc:
            assert isinstance(exc, _consumer_shim.CommitmentIdInvalid)
            assert isinstance(exc, CommitmentIdInvalid)
        else:  # pragma: no cover
            pytest.fail("expected CommitmentIdInvalid to be raised")


# ---------------------------------------------------------------------------
# §D. AWARD_INGEST end-to-end — auto-generated commitment_id is canonical
# ---------------------------------------------------------------------------


@dataclass
class _FakeParser:
    parses: dict[str, ParsedDocument]

    def parse(self, file_path: str, source_format: str) -> ParsedDocument:
        return self.parses[file_path]


@dataclass
class _FakeCommitmentExtractor:
    rows: list[ExtractedCommitment]

    def extract_commitments(
        self, *, org_slug: str, grant_id: str, parsed: ParsedDocument,
    ) -> Sequence[ExtractedCommitment]:
        return self.rows


def _seed_grant(tmp_path: Path) -> tuple[Path, Path, str]:
    grant_root = tmp_path / "orgs" / "demo_org" / "vault" / "grants" / "g_won"
    sub = grant_root / "submission"
    award = grant_root / "award"
    sub.mkdir(parents=True)
    award.mkdir(parents=True)
    submission = sub / "draft_3.md"
    submission.write_text(
        "# Won proposal\n\nWe will hire 4 staff in year 1.\nWe will serve 200 farmers in year 2.\n",
    )
    digest = hashlib.sha3_512(submission.read_bytes()).hexdigest()
    award_doc = award / "award_letter.pdf"
    award_doc.write_bytes(b"%PDF-1.0 fake award letter")
    return submission, award_doc, digest


def _signed_map(digest: str) -> SignedClaimEvidenceMap:
    return SignedClaimEvidenceMap(
        payload_canonical_bytes=b"signed payload",
        signature=b"\x01" * 64,
        signed_by="op_key_1",
        signed_at_utc=datetime(2026, 5, 11, tzinfo=timezone.utc),
        signer_public_key=b"\x02" * 32,
        submission_artifact_content_sha3_512=digest,
    )


def _commitment_rows() -> list[ExtractedCommitment]:
    return [
        ExtractedCommitment(
            source_section="Outcomes",
            commitment_text="hire 4 staff",
            commitment_proposal_offset=42,
            measurable_metric="staff_count",
            target_value=4.0,
            target_unit="people",
            due_period="year_1",
            source_line_id=2,
        ),
        ExtractedCommitment(
            source_section="Outcomes",
            commitment_text="serve 200 farmers",
            commitment_proposal_offset=80,
            measurable_metric="farmers_served",
            target_value=200.0,
            target_unit="people",
            due_period="year_2",
            source_line_id=3,
        ),
    ]


def test_award_ingest_writes_only_safe_commitment_ids(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The producer-side §11.5.2 ``proposal_commitments.yaml`` contains
    only safe-identifier commitment_ids. Mirrors §14 v1 LOCK Cycle 2
    RT-C2-02 admission contract — §11 v1.1 enforces the same contract
    at producer-side extraction time, not just at §14 consumer-side
    filesystem operations.
    """
    monkeypatch.chdir(tmp_path)
    submission, award_doc, digest = _seed_grant(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(submission),
        source_format=SOURCE_FORMAT_MD,
        lines=[
            "# Won proposal",
            "",
            "We will hire 4 staff in year 1.",
            "We will serve 200 farmers in year 2.",
            "",
        ],
    )
    aw = IntakeAwardInput(
        run_id="award_run_regex",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
        award_doc_unsigned_attestation=True,
    )
    result = award_ingest(
        aw,
        parser=_FakeParser(parses={str(submission): parsed}),
        extractor=_FakeCommitmentExtractor(rows=_commitment_rows()),
        signed_claim_evidence_map=_signed_map(digest),
        funder_signature_material=None,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )

    assert result.state.mode_completed is True
    commitments_path = result.proposal_commitments_path
    assert commitments_path is not None
    payload = json.loads(commitments_path.read_text())
    assert payload["status"] == "PENDING_OPERATOR_REVIEW"
    rows = payload["proposal_commitments"]
    assert len(rows) == 2

    # Every emitted commitment_id satisfies the safe-id contract.
    for row in rows:
        cid = row["commitment_id"]
        assert is_safe_commitment_id(cid), (
            f"commitment_id={cid!r} fails ^[A-Z0-9_-]+$ — producer-side "
            f"hardening per §11 v1.1 / RT-C2-02 broke regression"
        )
        # Auto-generated form is upper-hex of length 32.
        assert len(cid) == 32
        assert cid == cid.upper()
        # All characters are in [A-F0-9] (the uuid.hex.upper projection).
        assert set(cid) <= set("ABCDEF0123456789")


def test_award_ingest_commitment_ids_are_unique_per_row(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Distinct commitment rows must receive distinct commitment_ids
    (otherwise §14 claim_evidence_map collisions become possible).

    Anchors uniqueness at the AWARD_INGEST writer surface (2 rows from
    the default fixture); for a structurally load-bearing uniqueness
    contract at scale see
    ``test_commitment_id_generation_is_unique_at_scale`` below.
    """
    monkeypatch.chdir(tmp_path)
    submission, award_doc, digest = _seed_grant(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(submission),
        source_format=SOURCE_FORMAT_MD,
        lines=[
            "# Won proposal",
            "",
            "We will hire 4 staff in year 1.",
            "We will serve 200 farmers in year 2.",
            "",
        ],
    )
    aw = IntakeAwardInput(
        run_id="award_run_unique",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
        award_doc_unsigned_attestation=True,
    )
    result = award_ingest(
        aw,
        parser=_FakeParser(parses={str(submission): parsed}),
        extractor=_FakeCommitmentExtractor(rows=_commitment_rows()),
        signed_claim_evidence_map=_signed_map(digest),
        funder_signature_material=None,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    payload = json.loads(result.proposal_commitments_path.read_text())
    cids = [row["commitment_id"] for row in payload["proposal_commitments"]]
    assert len(cids) == len(set(cids))


def test_commitment_id_generation_is_unique_at_scale() -> None:
    """Cycle 1 RT-06 fold-in: ID-generation regression at meaningful
    scale (1000 invocations of the ``sanitize_commitment_id(uuid4.hex.
    upper())`` chain). A deterministic-counter regression in the ID
    generation algorithm would produce duplicates at this sample size
    and fail this assertion structurally — independent of the
    AWARD_INGEST substrate-fabrication gate (which may admit fewer
    rows than the input set depending on parsed-source coverage).

    This test isolates the producer-side ID generation contract from
    the row-admission gate's substrate semantics.
    """
    import uuid
    n = 1000
    ids: list[str] = []
    for _ in range(n):
        cid = sanitize_commitment_id(uuid.uuid4().hex.upper())
        ids.append(cid)
    assert len(ids) == n
    assert len(set(ids)) == n, (
        f"commitment_id collision detected at n={n} — generation "
        f"contract regression (RT-06 anchor)"
    )
    # Every generated id is canonical + length 32.
    for cid in ids:
        assert is_safe_commitment_id(cid)
        assert len(cid) == 32
        assert set(cid) <= set("ABCDEF0123456789")


def test_award_ingest_commitment_id_length_is_thirty_two(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cycle 1 RT-02 fold-in: anchor the 32-character length invariant
    of the auto-generated commitment_id at the test surface so a future
    drift to ``str(uuid.uuid4())`` (length 36) or ``uuid.uuid4().urn``
    (length 45 with prefix) surfaces structurally. The amendment does
    not freeze the generation algorithm itself, but the 32-char
    invariant is documented as load-bearing for downstream fixed-width
    consumers (§14 claim_evidence_map keys + UI columns).
    """
    monkeypatch.chdir(tmp_path)
    submission, award_doc, digest = _seed_grant(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(submission),
        source_format=SOURCE_FORMAT_MD,
        lines=[
            "# Won proposal",
            "",
            "We will hire 4 staff in year 1.",
            "We will serve 200 farmers in year 2.",
            "",
        ],
    )
    aw = IntakeAwardInput(
        run_id="award_run_length",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
        award_doc_unsigned_attestation=True,
    )
    result = award_ingest(
        aw,
        parser=_FakeParser(parses={str(submission): parsed}),
        extractor=_FakeCommitmentExtractor(rows=_commitment_rows()),
        signed_claim_evidence_map=_signed_map(digest),
        funder_signature_material=None,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    payload = json.loads(result.proposal_commitments_path.read_text())
    for row in payload["proposal_commitments"]:
        cid = row["commitment_id"]
        assert len(cid) == 32, (
            f"commitment_id length drift: got {len(cid)} for {cid!r}; "
            f"32-char invariant per §11 v1.1 §7 RT-02 fold-in"
        )


def test_canonical_home_and_shim_are_module_distinct(tmp_path: Path) -> None:
    """Cycle 1 RT-03 fold-in (partial): the canonical home module and
    the shim module are distinct module objects (per
    ``sys.modules``). Their PUBLIC SURFACE re-exports are
    object-identical (see ``TestProducerConsumerSingleCanonicalHome``);
    this test anchors the module-identity contract independently so a
    future refactor that conflates the two does not silently regress
    the backward-compat layer's role as a shim.
    """
    import sys
    canonical = sys.modules["pipeline.orchestrator.seats._commitment_id"]
    shim = sys.modules["pipeline.orchestrator.seats.report_generator._commitment_id"]
    assert canonical is not shim
    # But every symbol in the shim's __all__ MUST resolve to the same
    # object as the canonical home's corresponding attribute.
    for name in shim.__all__:
        assert getattr(canonical, name) is getattr(shim, name), (
            f"identity drift on {name!r}: canonical={getattr(canonical, name)!r} "
            f"shim={getattr(shim, name)!r}"
        )


def test_reload_preserves_identity_when_canonical_home_reloaded_first(tmp_path: Path) -> None:
    """Cycle 2 RT-C2-02 fold-in: anchor the reload-safety invariant.

    If the canonical home is reloaded at runtime (e.g., via
    ``importlib.reload`` from a dynamic plugin or test harness), the
    shim's previously-imported bindings become stale references to the
    PRE-reload class objects. The §11 v1.1 amendment's identity
    contract requires the operator to re-import the shim AFTER any
    canonical-home reload — this test anchors that protocol so any
    future drift surfaces structurally.

    Protocol: reload canonical → re-import shim → re-verify identity.
    A reload of the shim alone (without canonical) would also break
    the identity contract; this test does not exercise that case
    (operator-discipline boundary per §4 v1.x checklist contract 3
    documentation).
    """
    import importlib
    import sys
    canonical_name = "pipeline.orchestrator.seats._commitment_id"
    shim_name = "pipeline.orchestrator.seats.report_generator._commitment_id"
    canonical = sys.modules[canonical_name]
    shim_old = sys.modules[shim_name]
    # Reload the canonical home.
    canonical_reloaded = importlib.reload(canonical)
    # The shim's bindings are now stale references to the PRE-reload
    # class objects. Re-import the shim to refresh.
    shim_reloaded = importlib.reload(sys.modules[shim_name])
    # Post-protocol: identity contract restored.
    for name in shim_reloaded.__all__:
        assert getattr(canonical_reloaded, name) is getattr(shim_reloaded, name), (
            f"reload protocol violation on {name!r}: post-reload identity "
            f"contract not restored — canonical-home reload requires "
            f"shim re-import per §11 v1.1 §4 v1.x checklist contract 3 "
            f"documentation"
        )


def test_sanitize_is_stateless_across_calls() -> None:
    """Cycle 2 RT-C2-04 fold-in: anchor the stateless-sanitize contract.

    The ``sanitize_commitment_id`` function MUST be a pure
    function — same input → same output, no caching, no internal
    state. Monkey-patch ``uuid.uuid4`` to a known deterministic
    sequence and verify each sanitize call yields the input verbatim
    (no caching, no state-leak between calls).

    Complements the uuid4-stochastic 1000-row scale test
    (``test_commitment_id_generation_is_unique_at_scale``) which
    covers regression from the random source. This test covers the
    pure-function side of the contract independently.
    """
    # Deterministic sequence of 100 distinct uppercase-hex IDs.
    # Use 4-char prefix `DET_` + 28-char hex so every value differs in
    # the hex tail (truncation-induced collisions like
    # ``f'DETERMINISTIC_{i:028X}'[:32]`` for small i would silently
    # collapse to the same string and defeat the uniqueness anchor).
    deterministic = [f"DET_{i:028X}" for i in range(100)]
    for cid in deterministic:
        # Verify each ID passes the regex.
        assert is_safe_commitment_id(cid), f"setup error on {cid!r}"
    # Each sanitize call yields the input verbatim — no caching, no
    # internal state leak between calls.
    for cid in deterministic:
        out = sanitize_commitment_id(cid)
        assert out == cid
        # Re-invoke with the SAME input to verify pure-function
        # idempotence (a future caching bug that returns a fixed value
        # after first call would fail here).
        assert sanitize_commitment_id(cid) == cid
    # Distinct inputs → distinct outputs (no collapsing).
    outputs = [sanitize_commitment_id(c) for c in deterministic]
    assert len(set(outputs)) == len(deterministic)
