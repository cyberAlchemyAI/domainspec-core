"""§11 Intake — gate-predicate unit tests (Code phase).

Per Blueprint §11 v1 LOCKED 2026-05-10 row 185 + WS-E Code-phase done-definition.

Each test exercises a single predicate's PASS / FAIL paths. Production-side
substrate (pypdf / python-docx / FAISS / Pydantic AI / Mistral) is NOT
required — predicates are deterministic Python.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.orchestrator.seats.intake import (
    ExtractedCandidate,
    FunderSignatureMaterial,
    GateResult,
    IntakeAwardInput,
    IntakeBulkInput,
    IntakeIncrementalInput,
    IntakeState,
    LOCALHOST_HOSTS,
    ParsedDocument,
    SOURCE_FORMAT_DOCX,
    SOURCE_FORMAT_MD,
    SOURCE_FORMAT_PDF,
    SOURCE_FORMAT_TXT,
    SUPPORTED_FORMATS,
    SignedClaimEvidenceMap,
    SignedConfigBlock,
    f_extractor_award_signature_invalid_award,
    f_extractor_award_signature_invalid_proposal,
    f_extractor_fabrication,
    f_intake_config_signature_invalid,
    f_intake_embedding_endpoint_invalid,
    f_intake_embedding_ns_mismatch,
    f_intake_input_missing,
    f_intake_org_cross_ref,
    f_intake_queue_integrity_post_write,
    f_intake_queue_integrity_pre_run,
    f_intake_unsupported_format,
    f_intake_watcher_toctou,
)


# ---------------------------------------------------------------------------
# F-INTAKE-ORG-CROSS-REF (§11.9.4)
# ---------------------------------------------------------------------------


def test_org_cross_ref_bulk_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = tmp_path / "orgs" / "demo_org" / "intake" / "inbox"
    inbox.mkdir(parents=True)
    bulk = IntakeBulkInput(
        run_id="r1", org_slug="demo_org", inbox_dir=str(inbox),
    )
    assert f_intake_org_cross_ref(bulk).passed is True


def test_org_cross_ref_bulk_path_outside(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    other = tmp_path / "orgs" / "other_org" / "intake" / "inbox"
    other.mkdir(parents=True)
    bulk = IntakeBulkInput(
        run_id="r1", org_slug="demo_org", inbox_dir=str(other),
    )
    result = f_intake_org_cross_ref(bulk)
    assert result.passed is False
    assert result.code == "F-INTAKE-ORG-CROSS-REF"
    assert result.sub_tag == ".path_outside_inbox"


def test_org_cross_ref_incremental_path_outside(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    other = tmp_path / "orgs" / "other_org" / "intake" / "inbox" / "doc.txt"
    other.parent.mkdir(parents=True)
    other.write_text("x")
    inc = IntakeIncrementalInput(
        run_id="r1",
        org_slug="demo_org",
        doc_path=str(other),
        trigger="operator_explicit",
    )
    result = f_intake_org_cross_ref(inc)
    assert result.passed is False
    assert result.sub_tag == ".path_outside_inbox"


def test_org_cross_ref_award_doc_outside_vault(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    grant_root = tmp_path / "orgs" / "demo_org" / "vault" / "grants" / "g1"
    sub_dir = grant_root / "submission"
    sub_dir.mkdir(parents=True)
    (sub_dir / "draft_1.md").write_text("d")
    bad_award = tmp_path / "orgs" / "demo_org" / "vault" / "grants" / "g2" / "award" / "x.pdf"
    bad_award.parent.mkdir(parents=True)
    bad_award.write_text("p")
    aw = IntakeAwardInput(
        run_id="r1",
        org_slug="demo_org",
        grant_id="g1",
        submission_artifact_ref=str(sub_dir / "draft_1.md"),
        award_doc_path=str(bad_award),
    )
    result = f_intake_org_cross_ref(aw)
    assert result.passed is False
    assert result.sub_tag in {".cross_grant", ".award_doc_outside_vault"}


# ---------------------------------------------------------------------------
# F-INTAKE-INPUT-MISSING (§11.9.5)
# ---------------------------------------------------------------------------


def test_input_missing_inbox_dir_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    bulk = IntakeBulkInput(
        run_id="r1",
        org_slug="demo_org",
        inbox_dir=str(tmp_path / "orgs" / "demo_org" / "intake" / "inbox"),
    )
    result = f_intake_input_missing(bulk)
    assert result.passed is False
    assert result.sub_tag == ".inbox_dir_absent"


def test_input_missing_doc_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = tmp_path / "orgs" / "demo_org" / "intake" / "inbox"
    inbox.mkdir(parents=True)
    inc = IntakeIncrementalInput(
        run_id="r1",
        org_slug="demo_org",
        doc_path=str(inbox / "ghost.txt"),
        trigger="operator_explicit",
    )
    result = f_intake_input_missing(inc)
    assert result.passed is False
    assert result.sub_tag == ".doc_absent"


# ---------------------------------------------------------------------------
# F-INTAKE-UNSUPPORTED-FORMAT (§11.9.6)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("ext", sorted(SUPPORTED_FORMATS))
def test_unsupported_format_supported_pass(ext: str) -> None:
    assert f_intake_unsupported_format(f"orgs/o/intake/inbox/d.{ext}", mode="BULK_INGEST").passed


def test_unsupported_format_xlsx_rejected_in_bulk() -> None:
    res = f_intake_unsupported_format("orgs/o/intake/inbox/d.xlsx", mode="BULK_INGEST")
    assert res.passed is False
    assert res.code == "F-INTAKE-UNSUPPORTED-FORMAT"


def test_unsupported_format_award_doc_must_be_pdf_or_docx() -> None:
    res = f_intake_unsupported_format(
        "orgs/o/vault/grants/g/award/award.txt", mode="AWARD_INGEST",
    )
    assert res.passed is False
    assert res.sub_tag == ".award_doc"


# ---------------------------------------------------------------------------
# F-INTAKE-EMBEDDING-NS-MISMATCH (§11.9.8 + RT-09 + RT-10)
# ---------------------------------------------------------------------------


def test_ns_mismatch_org_slug() -> None:
    res = f_intake_embedding_ns_mismatch(
        expected_org_slug="org_a",
        expected_grant_id=None,
        tool_arg_org_slug="org_b",
        tool_arg_grant_id=None,
    )
    assert res.passed is False
    assert res.sub_tag == ".org_slug_mismatch"


def test_ns_mismatch_grant_id() -> None:
    res = f_intake_embedding_ns_mismatch(
        expected_org_slug="org_a",
        expected_grant_id="g1",
        tool_arg_org_slug="org_a",
        tool_arg_grant_id="g2",
    )
    assert res.passed is False
    assert res.sub_tag == ".grant_id_mismatch"


def test_ns_mismatch_compound_key_collision() -> None:
    res = f_intake_embedding_ns_mismatch(
        expected_org_slug="org_a",
        expected_grant_id=None,
        tool_arg_org_slug="org_a",
        tool_arg_grant_id=None,
        embedding_storage_path="orgs/org_a/vault/intake/embeddings/org_a_DEADBEEF",
        existing_storage_owners={
            "orgs/org_a/vault/intake/embeddings/org_a_DEADBEEF": "org_b",
        },
    )
    assert res.passed is False
    assert res.sub_tag == ".compound_key_collision"


def test_ns_mismatch_clean_pass() -> None:
    res = f_intake_embedding_ns_mismatch(
        expected_org_slug="org_a",
        expected_grant_id="g1",
        tool_arg_org_slug="org_a",
        tool_arg_grant_id="g1",
    )
    assert res.passed is True


# ---------------------------------------------------------------------------
# F-INTAKE-CONFIG-SIGNATURE-INVALID (§11.9.9 + RT-07)
# ---------------------------------------------------------------------------


def test_config_signature_absent_file_passes(tmp_path: Path) -> None:
    res = f_intake_config_signature_invalid(str(tmp_path / "missing.yaml"))
    assert res.passed is True


def test_config_signature_present_file_no_loader_fail_closed(tmp_path: Path) -> None:
    cfg = tmp_path / "intake_config.yaml"
    cfg.write_text("confidence_autopromote_threshold: 0.85")
    res = f_intake_config_signature_invalid(str(cfg))
    assert res.passed is False
    assert res.sub_tag == ".signature_absent"


def test_config_signature_invalid_signature_rejected(tmp_path: Path) -> None:
    cfg = tmp_path / "intake_config.yaml"
    cfg.write_text("x")
    block = SignedConfigBlock(
        payload_canonical_bytes=b"x",
        signature=b"\x00" * 64,
        signed_by="op_key_1",
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        signer_public_key=b"\x00" * 32,
    )
    res = f_intake_config_signature_invalid(
        str(cfg),
        signed_block_loader=lambda _: block,
        signature_verify=lambda *_: False,
        key_active_lookup=lambda *_: True,
    )
    assert res.passed is False
    assert res.sub_tag == ".signature_invalid"


def test_config_signature_retired_key_rejected(tmp_path: Path) -> None:
    cfg = tmp_path / "intake_config.yaml"
    cfg.write_text("x")
    block = SignedConfigBlock(
        payload_canonical_bytes=b"x",
        signature=b"\x00" * 64,
        signed_by="retired_key",
        signed_at_utc=datetime(2025, 1, 1, tzinfo=timezone.utc),
        signer_public_key=b"\x00" * 32,
    )
    res = f_intake_config_signature_invalid(
        str(cfg),
        signed_block_loader=lambda _: block,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda key, _ts: key != "retired_key",
    )
    assert res.passed is False
    assert res.sub_tag == ".retired_key"


def test_config_signature_valid_block_passes(tmp_path: Path) -> None:
    cfg = tmp_path / "intake_config.yaml"
    cfg.write_text("x")
    block = SignedConfigBlock(
        payload_canonical_bytes=b"x",
        signature=b"\x00" * 64,
        signed_by="op_key_1",
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        signer_public_key=b"\x00" * 32,
    )
    res = f_intake_config_signature_invalid(
        str(cfg),
        signed_block_loader=lambda _: block,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
    )
    assert res.passed is True


# ---------------------------------------------------------------------------
# F-INTAKE-EMBEDDING-ENDPOINT-INVALID (§11.9.10 + RT-13)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://localhost:8765/embed",
        "http://127.0.0.1:8765/embed",
        "http://[::1]:8765/embed",
        "unix:///tmp/embed.sock",
    ],
)
def test_embedding_endpoint_localhost_pass(endpoint: str) -> None:
    assert f_intake_embedding_endpoint_invalid(endpoint).passed is True


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://api.openai.com/v1/embeddings",
        "https://example.com/embed",
        "ftp://localhost/embed",
    ],
)
def test_embedding_endpoint_external_rejected(endpoint: str) -> None:
    res = f_intake_embedding_endpoint_invalid(endpoint)
    assert res.passed is False
    assert res.code == "F-INTAKE-EMBEDDING-ENDPOINT-INVALID"


def test_localhost_hosts_constant_complete() -> None:
    assert "localhost" in LOCALHOST_HOSTS
    assert "127.0.0.1" in LOCALHOST_HOSTS
    assert "::1" in LOCALHOST_HOSTS


# ---------------------------------------------------------------------------
# F-INTAKE-WATCHER-TOCTOU (§11.9.11 + RT-11)
# ---------------------------------------------------------------------------


def test_toctou_clean_file_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = tmp_path / "orgs" / "demo_org" / "intake" / "inbox"
    inbox.mkdir(parents=True)
    doc = inbox / "doc.txt"
    doc.write_text("clean")
    res = f_intake_watcher_toctou(
        str(doc), expected_org_subtree=str(inbox),
    )
    assert res.passed is True


def test_toctou_symlink_at_gate_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = tmp_path / "orgs" / "demo_org" / "intake" / "inbox"
    inbox.mkdir(parents=True)
    real = inbox / "real.txt"
    real.write_text("clean")
    link = inbox / "link.txt"
    link.symlink_to(real)
    res = f_intake_watcher_toctou(
        str(link), expected_org_subtree=str(inbox),
    )
    assert res.passed is False
    assert res.code == "F-INTAKE-WATCHER-TOCTOU"


def test_toctou_path_outside_subtree_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = tmp_path / "orgs" / "demo_org" / "intake" / "inbox"
    inbox.mkdir(parents=True)
    elsewhere = tmp_path / "elsewhere.txt"
    elsewhere.write_text("not allowed")
    res = f_intake_watcher_toctou(
        str(elsewhere), expected_org_subtree=str(inbox),
    )
    assert res.passed is False
    assert res.sub_tag == ".pre_resolve_outside_subtree"


# ---------------------------------------------------------------------------
# F-INTAKE-QUEUE-INTEGRITY (§11.9.7 + RT-12)
# ---------------------------------------------------------------------------


def test_queue_integrity_pre_run_state_corrupted(tmp_path: Path) -> None:
    state_file = tmp_path / "state.yaml"
    state_file.write_text("not yaml{{{")

    def _loader(p: str) -> dict[str, object]:
        raise ValueError("malformed")

    res = f_intake_queue_integrity_pre_run(
        state_file_path=str(state_file), state_loader=_loader,
    )
    assert res.passed is False
    assert res.sub_tag == ".state_corrupted"


def test_queue_integrity_pre_run_no_prior_state_passes(tmp_path: Path) -> None:
    res = f_intake_queue_integrity_pre_run(
        state_file_path=str(tmp_path / "missing.yaml"),
    )
    assert res.passed is True


def test_queue_integrity_pre_run_count_drift(tmp_path: Path) -> None:
    state_file = tmp_path / "state.yaml"
    state_file.write_text("ignored")
    queue_file = tmp_path / "queue.yaml"
    queue_file.write_text("ignored")

    def _state_loader(_: str) -> dict[str, object]:
        return {
            "run_id": "rA",
            "mode": "BULK_INGEST",
            "candidates_emitted_to_LLM": 5,
            "candidates_in_queue": 3,
            "candidates_rejected": 1,
        }

    def _queue_loader(_: str) -> list[dict[str, object]]:
        return [{"intake_run_id": "rA"}, {"intake_run_id": "rA"}, {"intake_run_id": "rA"}]

    res = f_intake_queue_integrity_pre_run(
        state_file_path=str(state_file),
        queue_file_path=str(queue_file),
        reject_count_for_run=1,
        state_loader=_state_loader,
        queue_loader=_queue_loader,
    )
    # emitted=5 != in_queue=3 + rejected=1 → fires
    assert res.passed is False
    assert res.sub_tag == ".cross_run_drift"


def test_queue_integrity_post_write_count_match(tmp_path: Path) -> None:
    state = IntakeState(
        run_id="rA",
        org_slug="o",
        grant_id=None,
        mode="BULK_INGEST",
        invoked_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        mode_completed=True,
        candidates_emitted_to_LLM=4,
        candidates_in_queue=3,
        candidates_rejected=1,
    )
    queue = [
        {"intake_run_id": "rA"},
        {"intake_run_id": "rA"},
        {"intake_run_id": "rA"},
    ]
    res = f_intake_queue_integrity_post_write(
        state=state,
        queue_file_path=str(tmp_path / "q.yaml"),
        queue_loader=lambda _: queue,
        reject_count_for_run=1,
    )
    assert res.passed is True


# ---------------------------------------------------------------------------
# F-EXTRACTOR-FABRICATION (§11.9.1 — substrate dispatch)
# ---------------------------------------------------------------------------


def test_extractor_fabrication_pdf_pass() -> None:
    parsed = ParsedDocument(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        pages={1: "Background only", 2: "We will hire 4 staff to deliver."},
    )
    cand = ExtractedCandidate(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        source_page=2,
        source_paragraph_id=None,
        source_line_id=None,
        source_quote="We will hire 4 staff",
        confidence_score=0.9,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is True


def test_extractor_fabrication_pdf_page_off_by_one_reject_in_bulk() -> None:
    parsed = ParsedDocument(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        pages={1: "Cover page.", 2: "Match number 42 here."},
    )
    cand = ExtractedCandidate(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        source_page=1,
        source_paragraph_id=None,
        source_line_id=None,
        source_quote="Match number 42",
        confidence_score=0.9,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is False
    assert res.sub_tag == ".page_mismatch"


def test_extractor_fabrication_pdf_off_by_one_pass_in_award_with_flag() -> None:
    parsed = ParsedDocument(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        pages={1: "Cover page.", 2: "Match number 42 here."},
    )
    cand = ExtractedCandidate(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        source_page=1,
        source_paragraph_id=None,
        source_line_id=None,
        source_quote="Match number 42",
        confidence_score=0.9,
    )
    res = f_extractor_fabrication(
        cand, mode="AWARD_INGEST", parsed=parsed,
        operator_award_page_offset_flag=True,
    )
    assert res.passed is True


def test_extractor_fabrication_pdf_multiple_page_match_rejected_without_override() -> None:
    parsed = ParsedDocument(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        pages={
            1: "Header: ABC Org Annual Report",
            3: "Header: ABC Org Annual Report",
            7: "Header: ABC Org Annual Report content",
        },
    )
    cand = ExtractedCandidate(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        source_page=3,
        source_paragraph_id=None,
        source_line_id=None,
        source_quote="ABC Org Annual Report",
        confidence_score=0.95,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is False


def test_extractor_fabrication_pdf_multiple_page_match_passes_with_override() -> None:
    parsed = ParsedDocument(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        pages={
            1: "Header: ABC Org Annual Report",
            3: "Header: ABC Org Annual Report",
        },
    )
    cand = ExtractedCandidate(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        source_page=1,
        source_paragraph_id=None,
        source_line_id=None,
        source_quote="ABC Org Annual Report",
        confidence_score=0.95,
        multiple_page_match=True,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is True


def test_extractor_fabrication_docx_paragraph_match_pass() -> None:
    parsed = ParsedDocument(
        source_doc="d.docx",
        source_format=SOURCE_FORMAT_DOCX,
        paragraphs=[
            "Cover.",
            "Annual revenue grew to $1.2M.",
            "Other content.",
        ],
    )
    cand = ExtractedCandidate(
        source_doc="d.docx",
        source_format=SOURCE_FORMAT_DOCX,
        source_page=None,
        source_paragraph_id=1,
        source_line_id=None,
        source_quote="revenue grew to $1.2M",
        confidence_score=0.88,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is True


def test_extractor_fabrication_docx_paragraph_mismatch_reject() -> None:
    parsed = ParsedDocument(
        source_doc="d.docx",
        source_format=SOURCE_FORMAT_DOCX,
        paragraphs=["Para A", "Para B", "Para C"],
    )
    cand = ExtractedCandidate(
        source_doc="d.docx",
        source_format=SOURCE_FORMAT_DOCX,
        source_page=None,
        source_paragraph_id=0,
        source_line_id=None,
        source_quote="Para B",  # actually in paragraph 1, not 0
        confidence_score=0.9,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is False
    assert res.sub_tag == ".docx_paragraph_mismatch"


def test_extractor_fabrication_markdown_multiline_reject() -> None:
    parsed = ParsedDocument(
        source_doc="d.md",
        source_format=SOURCE_FORMAT_MD,
        lines=["First line", "Second line", "Third line"],
    )
    cand = ExtractedCandidate(
        source_doc="d.md",
        source_format=SOURCE_FORMAT_MD,
        source_page=None,
        source_paragraph_id=None,
        source_line_id=0,
        source_quote="First line\nSecond line",
        confidence_score=0.9,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is False
    assert res.sub_tag == ".markdown_multiline"


def test_extractor_fabrication_txt_line_pass() -> None:
    parsed = ParsedDocument(
        source_doc="d.txt",
        source_format=SOURCE_FORMAT_TXT,
        lines=["Header", "EIN: 12-3456789", "Footer"],
    )
    cand = ExtractedCandidate(
        source_doc="d.txt",
        source_format=SOURCE_FORMAT_TXT,
        source_page=None,
        source_paragraph_id=None,
        source_line_id=1,
        source_quote="EIN: 12-3456789",
        confidence_score=0.95,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is True


def test_extractor_fabrication_ellipsis_substring_reject() -> None:
    parsed = ParsedDocument(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        pages={1: "Some content here"},
    )
    cand = ExtractedCandidate(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        source_page=1,
        source_paragraph_id=None,
        source_line_id=None,
        source_quote="Some...here",
        confidence_score=0.9,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is False
    assert res.sub_tag == ".ellipsis_substring"


def test_extractor_fabrication_mode_immutable_against_threshold_flip() -> None:
    """RT-04: tolerance comes from mode arg (plumbed from input bundle) only.

    Even with an off-by-one candidate, BULK_INGEST mode rejects regardless of
    any config-level threshold.
    """
    parsed = ParsedDocument(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        pages={1: "p1", 2: "actual quote here"},
    )
    cand = ExtractedCandidate(
        source_doc="d.pdf",
        source_format=SOURCE_FORMAT_PDF,
        source_page=1,
        source_paragraph_id=None,
        source_line_id=None,
        source_quote="actual quote here",
        confidence_score=0.0,
    )
    res = f_extractor_fabrication(cand, mode="BULK_INGEST", parsed=parsed)
    assert res.passed is False


# ---------------------------------------------------------------------------
# F-EXTRACTOR-AWARD-SIGNATURE-INVALID (§11.9.2 + §11.9.3)
# ---------------------------------------------------------------------------


def test_award_signature_proposal_pass() -> None:
    submission_bytes = b"draft contents"
    import hashlib as _h
    digest = _h.sha3_512(submission_bytes).hexdigest()
    map_payload = b"signed payload"
    aw = IntakeAwardInput(
        run_id="r1",
        org_slug="demo_org",
        grant_id="g1",
        submission_artifact_ref="orgs/demo_org/vault/grants/g1/submission/draft_1.md",
        award_doc_path="orgs/demo_org/vault/grants/g1/award/award.pdf",
    )
    cem = SignedClaimEvidenceMap(
        payload_canonical_bytes=map_payload,
        signature=b"\x01" * 64,
        signed_by="op_key_1",
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        signer_public_key=b"\x02" * 32,
        submission_artifact_content_sha3_512=digest,
    )
    res = f_extractor_award_signature_invalid_proposal(
        aw,
        submission_artifact_bytes=submission_bytes,
        signed_claim_evidence_map=cem,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
    )
    assert res.passed is True


def test_award_signature_proposal_hash_mismatch() -> None:
    submission_bytes = b"draft contents"
    cem = SignedClaimEvidenceMap(
        payload_canonical_bytes=b"x",
        signature=b"\x01" * 64,
        signed_by="op_key_1",
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        signer_public_key=b"\x02" * 32,
        submission_artifact_content_sha3_512="0" * 128,
    )
    aw = IntakeAwardInput(
        run_id="r1",
        org_slug="demo_org",
        grant_id="g1",
        submission_artifact_ref="orgs/demo_org/vault/grants/g1/submission/draft_1.md",
        award_doc_path="orgs/demo_org/vault/grants/g1/award/award.pdf",
    )
    res = f_extractor_award_signature_invalid_proposal(
        aw,
        submission_artifact_bytes=submission_bytes,
        signed_claim_evidence_map=cem,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
    )
    assert res.passed is False
    assert res.sub_tag == ".hash_mismatch"


def test_award_signature_proposal_legacy_unhashed() -> None:
    cem = SignedClaimEvidenceMap(
        payload_canonical_bytes=b"x",
        signature=b"\x01" * 64,
        signed_by="op_key_1",
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        signer_public_key=b"\x02" * 32,
        submission_artifact_content_sha3_512=None,
    )
    aw = IntakeAwardInput(
        run_id="r1",
        org_slug="demo_org",
        grant_id="g1",
        submission_artifact_ref="orgs/demo_org/vault/grants/g1/submission/draft_1.md",
        award_doc_path="orgs/demo_org/vault/grants/g1/award/award.pdf",
    )
    res = f_extractor_award_signature_invalid_proposal(
        aw,
        submission_artifact_bytes=b"x",
        signed_claim_evidence_map=cem,
        signature_verify=lambda *_: True,
        key_active_lookup=lambda *_: True,
    )
    assert res.passed is False
    assert res.sub_tag == ".legacy_unhashed"


def test_award_signature_award_unsigned_no_attestation_reject() -> None:
    aw = IntakeAwardInput(
        run_id="r1",
        org_slug="demo_org",
        grant_id="g1",
        submission_artifact_ref="orgs/demo_org/vault/grants/g1/submission/draft_1.md",
        award_doc_path="orgs/demo_org/vault/grants/g1/award/award.pdf",
        award_doc_unsigned_attestation=False,
    )
    res = f_extractor_award_signature_invalid_award(
        aw,
        funder_signature_material=None,
        signature_verify=lambda *_: False,
    )
    assert res.passed is False
    assert res.sub_tag == ".award_unsigned_no_attestation"


def test_award_signature_award_unsigned_with_attestation_pass() -> None:
    aw = IntakeAwardInput(
        run_id="r1",
        org_slug="demo_org",
        grant_id="g1",
        submission_artifact_ref="orgs/demo_org/vault/grants/g1/submission/draft_1.md",
        award_doc_path="orgs/demo_org/vault/grants/g1/award/award.pdf",
        award_doc_unsigned_attestation=True,
    )
    res = f_extractor_award_signature_invalid_award(
        aw,
        funder_signature_material=None,
        signature_verify=lambda *_: False,
    )
    assert res.passed is True


def test_award_signature_award_signed_funder_pass() -> None:
    aw = IntakeAwardInput(
        run_id="r1",
        org_slug="demo_org",
        grant_id="g1",
        submission_artifact_ref="orgs/demo_org/vault/grants/g1/submission/draft_1.md",
        award_doc_path="orgs/demo_org/vault/grants/g1/award/award.pdf",
    )
    fsm = FunderSignatureMaterial(
        signature=b"\x01" * 64,
        message_bytes=b"award doc bytes",
        public_key=b"\x02" * 32,
    )
    res = f_extractor_award_signature_invalid_award(
        aw,
        funder_signature_material=fsm,
        signature_verify=lambda *_: True,
    )
    assert res.passed is True


def test_award_signature_award_signed_funder_invalid_reject() -> None:
    aw = IntakeAwardInput(
        run_id="r1",
        org_slug="demo_org",
        grant_id="g1",
        submission_artifact_ref="orgs/demo_org/vault/grants/g1/submission/draft_1.md",
        award_doc_path="orgs/demo_org/vault/grants/g1/award/award.pdf",
    )
    fsm = FunderSignatureMaterial(
        signature=b"\x01" * 64,
        message_bytes=b"award doc bytes",
        public_key=b"\x02" * 32,
    )
    res = f_extractor_award_signature_invalid_award(
        aw,
        funder_signature_material=fsm,
        signature_verify=lambda *_: False,
    )
    assert res.passed is False


def test_gate_result_pass_factory() -> None:
    r = GateResult.PASS()
    assert r.passed is True
    assert r.code is None


def test_gate_result_fail_factory() -> None:
    r = GateResult.FAIL(code="X", sub_tag=".y", detail="z")
    assert r.passed is False
    assert r.code == "X"
    assert r.sub_tag == ".y"
    assert r.detail == "z"
