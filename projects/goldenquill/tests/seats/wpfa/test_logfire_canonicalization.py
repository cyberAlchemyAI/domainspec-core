"""Logfire export canonicalization tests. [§17.5.3 Cycle 2 RT-C2-03]"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.orchestrator.seats.wpfa.cycle_accountant import (
    canonicalize_logfire_export,
    collect_resolvable_span_ids,
    load_spans_from_logfire_export,
)


class TestCanonicalizeLogfireExport:
    def test_canonical_form_is_sorted_keys(self) -> None:
        raw = json.dumps({"b": 2, "a": 1}).encode("utf-8")
        out = canonicalize_logfire_export(raw)
        # sort_keys=True puts "a" before "b"
        assert out == b'{"a":1,"b":2}'

    def test_permuted_input_canonicalizes_identically(self) -> None:
        raw1 = json.dumps({"z": [1, 2], "a": "x"}).encode("utf-8")
        raw2 = json.dumps({"a": "x", "z": [1, 2]}).encode("utf-8")
        assert canonicalize_logfire_export(raw1) == canonicalize_logfire_export(raw2)

    def test_non_json_fails_with_schema_drift_advisory(self) -> None:
        with pytest.raises(ValueError, match="schema_drift_advisory"):
            canonicalize_logfire_export(b"not-json{")

    def test_invalid_utf8_fails(self) -> None:
        with pytest.raises(ValueError):
            canonicalize_logfire_export(b"\xff\xfe garbage")

    def test_non_bytes_input_raises_typeerror(self) -> None:
        with pytest.raises(TypeError):
            canonicalize_logfire_export("a string")  # type: ignore[arg-type]


class TestLoadSpansFromLogfireExport:
    def test_loads_llm_spans_only(self, tmp_path: Path) -> None:
        export = {
            "spans": [
                {
                    "span_id": "s1",
                    "trace_id": "t1",
                    "model_id": "m1",
                    "input_tokens": 100,
                    "output_tokens": 50,
                },
                {
                    # No model_id — skipped
                    "span_id": "s-internal",
                    "trace_id": "t1",
                    "kind": "internal",
                },
            ]
        }
        path = tmp_path / "logfire.json"
        path.write_bytes(json.dumps(export).encode("utf-8"))
        spans, canonical = load_spans_from_logfire_export(logfire_export_path=path)
        assert len(spans) == 1
        assert spans[0].span_id == "s1"
        assert spans[0].model_id == "m1"

    def test_malformed_span_raises_value_error(self, tmp_path: Path) -> None:
        export = {
            "spans": [
                {
                    "span_id": "s1",
                    "trace_id": "t1",
                    "model_id": "m1",
                    "input_tokens": "not-an-int",  # malformed
                    "output_tokens": 50,
                },
            ]
        }
        path = tmp_path / "logfire.json"
        path.write_bytes(json.dumps(export).encode("utf-8"))
        with pytest.raises(ValueError):
            load_spans_from_logfire_export(logfire_export_path=path)

    def test_top_level_array_rejected(self, tmp_path: Path) -> None:
        path = tmp_path / "logfire.json"
        path.write_bytes(json.dumps([]).encode("utf-8"))
        with pytest.raises(ValueError, match="must be an object"):
            load_spans_from_logfire_export(logfire_export_path=path)

    def test_spans_not_array_rejected(self, tmp_path: Path) -> None:
        path = tmp_path / "logfire.json"
        path.write_bytes(json.dumps({"spans": "oops"}).encode("utf-8"))
        with pytest.raises(ValueError, match="must be an array"):
            load_spans_from_logfire_export(logfire_export_path=path)


class TestCollectResolvableSpanIds:
    def test_returns_frozenset_of_span_ids(self) -> None:
        from pipeline.orchestrator.seats.wpfa.cycle_accountant import SpanRecord

        spans = [
            SpanRecord(
                span_id="a",
                trace_id="t",
                model_id="m",
                input_tokens=1,
                output_tokens=1,
            ),
            SpanRecord(
                span_id="b",
                trace_id="t",
                model_id="m",
                input_tokens=1,
                output_tokens=1,
            ),
        ]
        result = collect_resolvable_span_ids(spans)
        assert isinstance(result, frozenset)
        assert result == {"a", "b"}
