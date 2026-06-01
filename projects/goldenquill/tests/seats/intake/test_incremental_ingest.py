"""§11 Intake — INCREMENTAL_INGEST mode integration tests (Code phase).

Per Blueprint §11.6.2 + §11.13.1 + §11.13.5 + §11.13.7.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pytest

from pipeline.orchestrator.seats.intake import (
    ExtractedCandidate,
    IntakeIncrementalInput,
    ParsedDocument,
    SOURCE_FORMAT_MD,
    incremental_ingest,
)


@dataclass
class FakeParser:
    parses: dict[str, ParsedDocument]

    def parse(self, file_path: str, source_format: str) -> ParsedDocument:
        return self.parses[file_path]


@dataclass
class FakeExtractor:
    candidates: dict[str, list[ExtractedCandidate]]

    def extract_facts(
        self, *, org_slug: str, parsed: ParsedDocument,
    ) -> Sequence[ExtractedCandidate]:
        return self.candidates.get(parsed.source_doc, [])


def _seed_doc(tmp_path: Path, name: str = "doc.md") -> Path:
    inbox = tmp_path / "orgs" / "demo_org" / "intake" / "inbox"
    inbox.mkdir(parents=True)
    doc = inbox / name
    doc.write_text("Snapshot.\nKey fact: 42.\n")
    return doc


def test_incremental_records_watcher_trigger(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    doc = _seed_doc(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(doc),
        source_format=SOURCE_FORMAT_MD,
        lines=["Snapshot.", "Key fact: 42."],
    )
    cand = ExtractedCandidate(
        source_doc=str(doc),
        source_format=SOURCE_FORMAT_MD,
        source_page=None,
        source_paragraph_id=None,
        source_line_id=1,
        source_quote="Key fact: 42",
        confidence_score=0.91,
    )
    inc = IntakeIncrementalInput(
        run_id="inc_w",
        org_slug="demo_org",
        doc_path=str(doc),
        trigger="watcher",
    )
    result = incremental_ingest(
        inc,
        parser=FakeParser(parses={str(doc): parsed}),
        extractor=FakeExtractor(candidates={str(doc): [cand]}),
        vault_root=tmp_path,
    )
    assert result.state.trigger == "watcher"
    assert result.state.candidates_in_queue == 1


def test_incremental_records_operator_explicit_trigger(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    doc = _seed_doc(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(doc),
        source_format=SOURCE_FORMAT_MD,
        lines=["Snapshot.", "Key fact: 42."],
    )
    inc = IntakeIncrementalInput(
        run_id="inc_op",
        org_slug="demo_org",
        doc_path=str(doc),
        trigger="operator_explicit",
    )
    result = incremental_ingest(
        inc,
        parser=FakeParser(parses={str(doc): parsed}),
        extractor=FakeExtractor(candidates={}),
        vault_root=tmp_path,
    )
    assert result.state.trigger == "operator_explicit"
    assert result.state.mode_completed is True


def test_incremental_appends_to_existing_queue(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    doc = _seed_doc(tmp_path)
    parsed = ParsedDocument(
        source_doc=str(doc),
        source_format=SOURCE_FORMAT_MD,
        lines=["Snapshot.", "Key fact: 42."],
    )
    cand = ExtractedCandidate(
        source_doc=str(doc),
        source_format=SOURCE_FORMAT_MD,
        source_page=None,
        source_paragraph_id=None,
        source_line_id=1,
        source_quote="Key fact: 42",
        confidence_score=0.91,
    )
    parser = FakeParser(parses={str(doc): parsed})
    extractor = FakeExtractor(candidates={str(doc): [cand]})

    for run in ("inc_1", "inc_2"):
        incremental_ingest(
            IntakeIncrementalInput(
                run_id=run, org_slug="demo_org",
                doc_path=str(doc), trigger="operator_explicit",
            ),
            parser=parser, extractor=extractor, vault_root=tmp_path,
        )
    queue_path = tmp_path / "orgs" / "demo_org" / "vault" / "kfr" / "pending_facts.yaml"
    payload = json.loads(queue_path.read_text())
    assert len(payload["pending_facts"]) == 2


def test_incremental_unsupported_format_pre_gate_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = tmp_path / "orgs" / "demo_org" / "intake" / "inbox"
    inbox.mkdir(parents=True)
    doc = inbox / "data.xlsx"
    doc.write_text("noop")
    inc = IntakeIncrementalInput(
        run_id="inc_xlsx",
        org_slug="demo_org",
        doc_path=str(doc),
        trigger="watcher",
    )
    parser = FakeParser(parses={})
    extractor = FakeExtractor(candidates={})
    result = incremental_ingest(
        inc, parser=parser, extractor=extractor, vault_root=tmp_path,
    )
    assert result.state.mode_completed is False
    assert "F-INTAKE-UNSUPPORTED-FORMAT" in (result.state.failure_reason or "")


def test_incremental_org_cross_ref_pre_gate_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    other = tmp_path / "orgs" / "other_org" / "intake" / "inbox"
    other.mkdir(parents=True)
    foreign = other / "leak.md"
    foreign.write_text("leak")
    inc = IntakeIncrementalInput(
        run_id="inc_leak",
        org_slug="demo_org",
        doc_path=str(foreign),
        trigger="watcher",
    )
    parser = FakeParser(parses={})
    extractor = FakeExtractor(candidates={})
    result = incremental_ingest(
        inc, parser=parser, extractor=extractor, vault_root=tmp_path,
    )
    assert result.state.mode_completed is False
    assert "F-INTAKE-ORG-CROSS-REF" in (result.state.failure_reason or "")


def test_incremental_toctou_symlink_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    inbox = tmp_path / "orgs" / "demo_org" / "intake" / "inbox"
    inbox.mkdir(parents=True)
    real = inbox / "real.md"
    real.write_text("real")
    link = inbox / "link.md"
    link.symlink_to(real)
    inc = IntakeIncrementalInput(
        run_id="inc_toctou",
        org_slug="demo_org",
        doc_path=str(link),
        trigger="watcher",
    )
    parser = FakeParser(parses={})
    extractor = FakeExtractor(candidates={})
    result = incremental_ingest(
        inc, parser=parser, extractor=extractor, vault_root=tmp_path,
    )
    assert result.state.mode_completed is False
    assert "F-INTAKE-WATCHER-TOCTOU" in (result.state.failure_reason or "")
