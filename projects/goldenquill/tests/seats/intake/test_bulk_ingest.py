"""§11 Intake — BULK_INGEST mode integration tests (Code phase).

Per Blueprint §11.6.1 + §11.13.5 + §11.13.9.

Stubs the document parser and extractor LLM with deterministic fakes; the
seat module's substrate dispatch and gate stack are exercised end-to-end
through ``bulk_ingest()``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

import pytest

from pipeline.orchestrator.seats.intake import (
    DocumentParserProtocol,
    ExtractedCandidate,
    FactExtractorProtocol,
    IntakeBulkInput,
    ParsedDocument,
    SOURCE_FORMAT_DOCX,
    SOURCE_FORMAT_MD,
    SOURCE_FORMAT_PDF,
    SOURCE_FORMAT_TXT,
    bulk_ingest,
)


@dataclass
class FakeParser:
    """Returns a fixed ParsedDocument per file_path."""
    parses: dict[str, ParsedDocument]

    def parse(self, file_path: str, source_format: str) -> ParsedDocument:
        if file_path in self.parses:
            return self.parses[file_path]
        # Fallback: empty parse — gate will reject downstream candidates.
        return ParsedDocument(source_doc=file_path, source_format=source_format)


@dataclass
class FakeExtractor:
    """Returns a fixed list of candidates per source_doc."""
    candidates: dict[str, list[ExtractedCandidate]]

    def extract_facts(
        self, *, org_slug: str, parsed: ParsedDocument,
    ) -> Sequence[ExtractedCandidate]:
        return self.candidates.get(parsed.source_doc, [])


def _seed_inbox(tmp_path: Path, org: str = "demo_org") -> Path:
    inbox = tmp_path / "orgs" / org / "intake" / "inbox"
    inbox.mkdir(parents=True)
    return inbox


def test_bulk_writes_pending_facts_yaml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = _seed_inbox(tmp_path)
    pdf_doc = inbox / "annual_report.pdf"
    pdf_doc.write_bytes(b"%PDF-1.0 fake")
    parsed = ParsedDocument(
        source_doc=str(pdf_doc),
        source_format=SOURCE_FORMAT_PDF,
        pages={1: "We employed 12 staff in FY24."},
    )
    cand = ExtractedCandidate(
        source_doc=str(pdf_doc),
        source_format=SOURCE_FORMAT_PDF,
        source_page=1,
        source_paragraph_id=None,
        source_line_id=None,
        source_quote="We employed 12 staff",
        confidence_score=0.95,
        fact_payload={"who": "demo_org", "what": "headcount", "value": 12},
    )

    parser = FakeParser(parses={str(pdf_doc): parsed})
    extractor = FakeExtractor(candidates={str(pdf_doc): [cand]})

    bulk = IntakeBulkInput(
        run_id="run_bulk_a",
        org_slug="demo_org",
        inbox_dir=str(inbox),
    )
    result = bulk_ingest(
        bulk, parser=parser, extractor=extractor, vault_root=tmp_path,
    )

    assert result.state.mode_completed is True
    assert result.state.candidates_emitted_to_LLM == 1
    assert result.state.candidates_in_queue == 1
    assert result.state.candidates_rejected == 0

    queue_path = result.pending_facts_path
    assert queue_path is not None and queue_path.is_file()
    queue_payload = json.loads(queue_path.read_text())
    assert queue_payload["schema_version"] == "pending_facts.v1"
    assert len(queue_payload["pending_facts"]) == 1
    row = queue_payload["pending_facts"][0]
    assert row["intake_run_id"] == "run_bulk_a"
    assert row["source_quote"] == "We employed 12 staff"
    assert row["autopromote_batch"] is True

    state_path = result.state_file_path
    assert state_path.is_file()
    state_payload = json.loads(state_path.read_text())
    assert state_payload["mode_completed"] is True
    assert state_payload["mode"] == "BULK_INGEST"


def test_bulk_appends_across_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = _seed_inbox(tmp_path)
    md_doc = inbox / "boilerplate.md"
    md_doc.write_text("Org snapshot.\nEIN: 12-3456789\n")

    parsed = ParsedDocument(
        source_doc=str(md_doc),
        source_format=SOURCE_FORMAT_MD,
        lines=["Org snapshot.", "EIN: 12-3456789"],
    )
    cand = ExtractedCandidate(
        source_doc=str(md_doc),
        source_format=SOURCE_FORMAT_MD,
        source_page=None,
        source_paragraph_id=None,
        source_line_id=1,
        source_quote="EIN: 12-3456789",
        confidence_score=0.92,
    )

    parser = FakeParser(parses={str(md_doc): parsed})
    extractor = FakeExtractor(candidates={str(md_doc): [cand]})

    for run_id in ("run_a", "run_b"):
        bulk = IntakeBulkInput(
            run_id=run_id,
            org_slug="demo_org",
            inbox_dir=str(inbox),
        )
        bulk_ingest(bulk, parser=parser, extractor=extractor, vault_root=tmp_path)

    queue_path = tmp_path / "orgs" / "demo_org" / "vault" / "kfr" / "pending_facts.yaml"
    payload = json.loads(queue_path.read_text())
    assert len(payload["pending_facts"]) == 2
    run_ids = {r["intake_run_id"] for r in payload["pending_facts"]}
    assert run_ids == {"run_a", "run_b"}


def test_bulk_skips_unsupported_formats_and_records_in_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = _seed_inbox(tmp_path)
    md_doc = inbox / "ok.md"
    md_doc.write_text("OK content")
    xlsx_doc = inbox / "skip.xlsx"
    xlsx_doc.write_text("not allowed at v1")

    parsed = ParsedDocument(
        source_doc=str(md_doc),
        source_format=SOURCE_FORMAT_MD,
        lines=["OK content"],
    )
    parser = FakeParser(parses={str(md_doc): parsed})
    extractor = FakeExtractor(candidates={})

    bulk = IntakeBulkInput(
        run_id="run_skip",
        org_slug="demo_org",
        inbox_dir=str(inbox),
    )
    result = bulk_ingest(bulk, parser=parser, extractor=extractor, vault_root=tmp_path)
    assert str(xlsx_doc) in result.state.skipped_unsupported
    assert result.state.mode_completed is True


def test_bulk_rejects_fabrication_to_audit_trail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = _seed_inbox(tmp_path)
    docx_doc = inbox / "report.docx"
    docx_doc.write_bytes(b"PK\x03\x04 fake docx")

    parsed = ParsedDocument(
        source_doc=str(docx_doc),
        source_format=SOURCE_FORMAT_DOCX,
        paragraphs=["Para 0", "Para 1 contains real data", "Para 2"],
    )
    fabricated = ExtractedCandidate(
        source_doc=str(docx_doc),
        source_format=SOURCE_FORMAT_DOCX,
        source_page=None,
        source_paragraph_id=0,
        source_line_id=None,
        source_quote="Para 1 contains real data",  # actually in idx 1, not 0
        confidence_score=0.99,
    )
    parser = FakeParser(parses={str(docx_doc): parsed})
    extractor = FakeExtractor(candidates={str(docx_doc): [fabricated]})

    bulk = IntakeBulkInput(
        run_id="run_fab",
        org_slug="demo_org",
        inbox_dir=str(inbox),
    )
    result = bulk_ingest(bulk, parser=parser, extractor=extractor, vault_root=tmp_path)

    assert result.state.candidates_rejected == 1
    assert result.state.candidates_in_queue == 0
    assert result.pending_facts_path is None
    assert result.rejects_dir is not None and result.rejects_dir.is_dir()
    rejects = list(result.rejects_dir.glob("*.yaml"))
    assert len(rejects) == 1
    payload = json.loads(rejects[0].read_text())
    assert payload["reject_reason_code"] == "F-EXTRACTOR-FABRICATION"
    assert payload["reject_sub_tag"] == ".docx_paragraph_mismatch"


def test_bulk_below_threshold_not_autopromote(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = _seed_inbox(tmp_path)
    txt_doc = inbox / "notes.txt"
    txt_doc.write_text("low confidence note\n")
    parsed = ParsedDocument(
        source_doc=str(txt_doc),
        source_format=SOURCE_FORMAT_TXT,
        lines=["low confidence note"],
    )
    cand = ExtractedCandidate(
        source_doc=str(txt_doc),
        source_format=SOURCE_FORMAT_TXT,
        source_page=None,
        source_paragraph_id=None,
        source_line_id=0,
        source_quote="low confidence note",
        confidence_score=0.50,
    )
    parser = FakeParser(parses={str(txt_doc): parsed})
    extractor = FakeExtractor(candidates={str(txt_doc): [cand]})
    bulk = IntakeBulkInput(
        run_id="run_low",
        org_slug="demo_org",
        inbox_dir=str(inbox),
        confidence_autopromote_threshold=0.85,
    )
    result = bulk_ingest(bulk, parser=parser, extractor=extractor, vault_root=tmp_path)
    payload = json.loads(result.pending_facts_path.read_text())
    assert payload["pending_facts"][0]["autopromote_batch"] is False


def test_bulk_pre_gate_failure_writes_state_with_failure_reason(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    # No inbox dir is created — F-INTAKE-INPUT-MISSING fires.
    bulk = IntakeBulkInput(
        run_id="run_fail",
        org_slug="demo_org",
        inbox_dir=str(tmp_path / "orgs" / "demo_org" / "intake" / "inbox"),
    )
    parser = FakeParser(parses={})
    extractor = FakeExtractor(candidates={})
    result = bulk_ingest(bulk, parser=parser, extractor=extractor, vault_root=tmp_path)
    assert result.state.mode_completed is False
    assert result.state.failure_reason is not None
    assert "F-INTAKE-INPUT-MISSING" in result.state.failure_reason
    assert result.state_file_path.is_file()


def test_bulk_migration_target_path_processes_single_md(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """§11.11 MIGRATION_BULK_INGEST: scoped to a single PROJECT_CONTEXT.md."""
    monkeypatch.chdir(tmp_path)
    org_root = tmp_path / "orgs" / "demo_org"
    org_root.mkdir(parents=True)
    inbox = org_root / "intake" / "inbox"
    inbox.mkdir(parents=True)
    pc = org_root / "PROJECT_CONTEXT.md"
    pc.write_text("Org context.\nEIN: [NEEDED]\n")

    parsed = ParsedDocument(
        source_doc=str(pc),
        source_format=SOURCE_FORMAT_MD,
        lines=["Org context.", "EIN: [NEEDED]"],
    )
    cand = ExtractedCandidate(
        source_doc=str(pc),
        source_format=SOURCE_FORMAT_MD,
        source_page=None,
        source_paragraph_id=None,
        source_line_id=1,
        source_quote="EIN: [NEEDED]",
        confidence_score=0.7,
    )
    parser = FakeParser(parses={str(pc): parsed})
    extractor = FakeExtractor(candidates={str(pc): [cand]})

    bulk = IntakeBulkInput(
        run_id="run_migrate",
        org_slug="demo_org",
        inbox_dir=str(inbox),
        migration_target_path=str(pc),
    )
    result = bulk_ingest(bulk, parser=parser, extractor=extractor, vault_root=tmp_path)
    assert result.state.candidates_in_queue == 1
    payload = json.loads(result.pending_facts_path.read_text())
    assert payload["pending_facts"][0]["source_doc"] == str(pc)
