"""§11 Intake — AWARD_INGEST mode integration tests (Code phase).

Per Blueprint §11.6.3 + §11.13.3 + §11.13.5.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

import pytest

from pipeline.orchestrator.seats.intake import (
    ExtractedCommitment,
    FunderSignatureMaterial,
    IntakeAwardInput,
    ParsedDocument,
    SOURCE_FORMAT_MD,
    SignedClaimEvidenceMap,
    award_ingest,
)


@dataclass
class FakeParser:
    parses: dict[str, ParsedDocument]

    def parse(self, file_path: str, source_format: str) -> ParsedDocument:
        return self.parses[file_path]


@dataclass
class FakeCommitmentExtractor:
    rows: list[ExtractedCommitment]

    def extract_commitments(
        self, *, org_slug: str, grant_id: str, parsed: ParsedDocument,
    ) -> Sequence[ExtractedCommitment]:
        return self.rows


def _seed_grant(tmp_path: Path) -> tuple[Path, Path, bytes, str]:
    grant_root = tmp_path / "orgs" / "demo_org" / "vault" / "grants" / "g_won"
    sub = grant_root / "submission"
    award = grant_root / "award"
    sub.mkdir(parents=True)
    award.mkdir(parents=True)
    submission_artifact = sub / "draft_3.md"
    submission_artifact.write_text(
        "# Won proposal\n\nWe will hire 4 staff in year 1.\nWe will serve 200 farmers in year 2.\n",
    )
    bytes_ = submission_artifact.read_bytes()
    digest = hashlib.sha3_512(bytes_).hexdigest()
    award_doc = award / "award_letter.pdf"
    award_doc.write_bytes(b"%PDF-1.0 fake award letter")
    return submission_artifact, award_doc, bytes_, digest


def _good_signed_map(digest: str) -> SignedClaimEvidenceMap:
    return SignedClaimEvidenceMap(
        payload_canonical_bytes=b"signed payload",
        signature=b"\x01" * 64,
        signed_by="op_key_1",
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        signer_public_key=b"\x02" * 32,
        submission_artifact_content_sha3_512=digest,
    )


def _commitments(parsed_lines: Sequence[str]) -> list[ExtractedCommitment]:
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


def test_award_ingest_writes_proposal_commitments_pending_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    submission, award_doc, _, digest = _seed_grant(tmp_path)
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
        run_id="award_run_a",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
        award_doc_unsigned_attestation=True,  # bypass funder leg for test
    )
    result = award_ingest(
        aw,
        parser=FakeParser(parses={str(submission): parsed}),
        extractor=FakeCommitmentExtractor(rows=_commitments(parsed.lines or [])),
        signed_claim_evidence_map=_good_signed_map(digest),
        funder_signature_material=None,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    assert result.state.mode_completed is True
    assert result.state.candidates_in_queue == 2
    commitments_path = result.proposal_commitments_path
    assert commitments_path is not None
    payload = json.loads(commitments_path.read_text())
    assert payload["status"] == "PENDING_OPERATOR_REVIEW"
    assert payload["schema_version"] == "proposal_commitments.v1"
    assert len(payload["proposal_commitments"]) == 2

    trail_path = result.signature_trail_path
    assert trail_path is not None and trail_path.is_file()
    trail = json.loads(trail_path.read_text())
    assert trail["submission_signature_outcome"] == "PASS"


def test_award_ingest_proposal_signature_invalid_blocks_extraction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    submission, award_doc, _, digest = _seed_grant(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(submission), source_format=SOURCE_FORMAT_MD, lines=[]
    )
    aw = IntakeAwardInput(
        run_id="award_run_b",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
        award_doc_unsigned_attestation=True,
    )
    extractor = FakeCommitmentExtractor(rows=_commitments([]))
    result = award_ingest(
        aw,
        parser=FakeParser(parses={str(submission): parsed}),
        extractor=extractor,
        signed_claim_evidence_map=_good_signed_map(digest),
        funder_signature_material=None,
        signature_verify=lambda *_: False,  # signature fails
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    assert result.state.mode_completed is False
    assert "F-EXTRACTOR-AWARD-SIGNATURE-INVALID" in (result.state.failure_reason or "")
    assert result.proposal_commitments_path is None
    assert result.signature_trail_path is not None


def test_award_ingest_hash_mismatch_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    submission, award_doc, _, _ = _seed_grant(tmp_path)
    bogus_digest = "0" * 128
    parsed = ParsedDocument(
        source_doc=str(submission), source_format=SOURCE_FORMAT_MD, lines=[]
    )
    aw = IntakeAwardInput(
        run_id="award_run_hash",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
        award_doc_unsigned_attestation=True,
    )
    result = award_ingest(
        aw,
        parser=FakeParser(parses={str(submission): parsed}),
        extractor=FakeCommitmentExtractor(rows=[]),
        signed_claim_evidence_map=_good_signed_map(bogus_digest),
        funder_signature_material=None,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    assert result.state.mode_completed is False
    assert ".hash_mismatch" in (result.state.failure_reason or "")


def test_award_ingest_unsigned_funder_no_attestation_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    submission, award_doc, _, digest = _seed_grant(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(submission), source_format=SOURCE_FORMAT_MD, lines=[]
    )
    aw = IntakeAwardInput(
        run_id="award_run_unsigned",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
        award_doc_unsigned_attestation=False,
    )
    result = award_ingest(
        aw,
        parser=FakeParser(parses={str(submission): parsed}),
        extractor=FakeCommitmentExtractor(rows=[]),
        signed_claim_evidence_map=_good_signed_map(digest),
        funder_signature_material=None,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    assert result.state.mode_completed is False
    assert ".award_unsigned_no_attestation" in (result.state.failure_reason or "")


def test_award_ingest_signed_funder_award_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    submission, award_doc, _, digest = _seed_grant(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(submission),
        source_format=SOURCE_FORMAT_MD,
        lines=[
            "# Won proposal", "",
            "We will hire 4 staff in year 1.",
            "We will serve 200 farmers in year 2.",
        ],
    )
    fsm = FunderSignatureMaterial(
        signature=b"\x01" * 64,
        message_bytes=b"award letter bytes",
        public_key=b"\x02" * 32,
    )
    aw = IntakeAwardInput(
        run_id="award_run_signed",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
    )
    result = award_ingest(
        aw,
        parser=FakeParser(parses={str(submission): parsed}),
        extractor=FakeCommitmentExtractor(rows=_commitments(parsed.lines or [])),
        signed_claim_evidence_map=_good_signed_map(digest),
        funder_signature_material=fsm,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    assert result.state.mode_completed is True
    assert result.state.candidates_in_queue == 2


def test_award_ingest_award_doc_outside_vault_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    submission, _, _, digest = _seed_grant(tmp_path)
    bad_award = tmp_path / "outside" / "award.pdf"
    bad_award.parent.mkdir(parents=True)
    bad_award.write_bytes(b"%PDF-1.0")
    aw = IntakeAwardInput(
        run_id="award_outside",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(bad_award),
        award_doc_unsigned_attestation=True,
    )
    result = award_ingest(
        aw,
        parser=FakeParser(parses={}),
        extractor=FakeCommitmentExtractor(rows=[]),
        signed_claim_evidence_map=_good_signed_map(digest),
        funder_signature_material=None,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    assert result.state.mode_completed is False
    assert "F-INTAKE-ORG-CROSS-REF" in (result.state.failure_reason or "")


def test_award_ingest_with_page_tolerance_flag_passes_in_award_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Per RT-04: ±1 page tolerance only applies in AWARD_INGEST + flag set."""
    monkeypatch.chdir(tmp_path)
    submission, award_doc, _, digest = _seed_grant(tmp_path)
    # Build a parsed doc with pages mapping where the quote is on page 2 but
    # the commitment claims source_page=1 — only AWARD + flag should pass.
    parsed = ParsedDocument(
        source_doc=str(submission),
        source_format="pdf",  # type: ignore[arg-type]
        pages={1: "intro", 2: "We will hire 4 staff."},
    )
    aw = IntakeAwardInput(
        run_id="award_run_pagetol",
        org_slug="demo_org",
        grant_id="g_won",
        submission_artifact_ref=str(submission),
        award_doc_path=str(award_doc),
        award_doc_unsigned_attestation=True,
    )
    cmt = ExtractedCommitment(
        source_section="Outcomes",
        commitment_text="We will hire 4 staff.",
        commitment_proposal_offset=10,
        measurable_metric="staff_count",
        target_value=4.0,
        target_unit="people",
        due_period="year_1",
        source_page=1,  # off-by-one
        page_tolerance_applied=True,
    )

    class _PdfParser:
        def parse(self, file_path: str, source_format: str) -> ParsedDocument:
            return parsed

    result = award_ingest(
        aw,
        parser=_PdfParser(),
        extractor=FakeCommitmentExtractor(rows=[cmt]),
        signed_claim_evidence_map=_good_signed_map(digest),
        funder_signature_material=None,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
        vault_root=tmp_path,
    )
    # AWARD_INGEST + page_tolerance_applied=True → off-by-one passes.
    assert result.state.mode_completed is True
    assert result.state.candidates_in_queue == 1
    payload = json.loads(result.proposal_commitments_path.read_text())
    assert payload["proposal_commitments"][0]["page_tolerance_applied"] is True
