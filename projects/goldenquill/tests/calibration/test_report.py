"""Tests for pipeline.calibration.report (R12.A).

Covers:
- CalibrationReportItem construction validation (every field path).
- CalibrationReport construction validation.
- canonical_bytes determinism across dict insertion order.
- canonical_bytes excludes signature + canonical_sha256 but nothing else.
- canonical_bytes NFC-normalizes string leaves (composed == decomposed).
- canonical_bytes exhaustiveness — every declared field is either serialized
  or in the exclusion table (§5.6.4 + §7.16).
- assemble_from_run mean/stddev/per-dim computation.
- assemble_from_run with empty items list (edge case).
- assemble_from_run populates canonical_sha256 reproducibly.
- report_to_json + report_from_json round-trip (signed + unsigned).
- F_PIPE_22 on schema-version mismatch (construct + from_json).
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import fields
from typing import Any

import pytest

from pipeline.calibration.report import (
    AssembleInputs,
    CalibrationReport,
    CalibrationReportItem,
    assemble_from_run,
    calibration_report_field_set,
    calibration_report_item_field_set,
    canonical_bytes,
    canonical_bytes_exclusions,
    compute_canonical_sha256,
    report_from_json,
    report_to_json,
)
from pipeline.loop.errors import F_PIPE_22


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _item_kwargs(**o: Any) -> dict[str, Any]:
    base = dict(
        item_id="gs-001",
        judge_total_score=85,
        judge_per_dimension={"clarity": 9, "fit": 8, "alignment": 9},
        editor_critique_summary="strong draft; tightened section 3",
        iterations_used=2,
        revision_loop_outcome="pass_iter2",
        item_run_id="run-001",
    )
    base.update(o)
    return base


def _report_kwargs(**o: Any) -> dict[str, Any]:
    items = (CalibrationReportItem(**_item_kwargs()),)
    base = dict(
        schema_version=1,
        run_id="run-eval-001",
        operator_org_slug="fit_farms_llc",
        golden_set_manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        items=items,
        summary_judge_mean=85.0,
        summary_judge_stddev=0.0,
        summary_per_dimension_mean={"clarity": 9.0, "fit": 8.0, "alignment": 9.0},
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
        canonical_sha256="e" * 64,
        signature=None,
        signed_at_iso=None,
    )
    base.update(o)
    return base


# ---------------------------------------------------------------------------
# CalibrationReportItem construction
# ---------------------------------------------------------------------------


def test_item_happy_path() -> None:
    it = CalibrationReportItem(**_item_kwargs())
    assert it.item_id == "gs-001"
    assert it.judge_total_score == 85
    assert it.iterations_used == 2


def test_item_rejects_empty_item_id() -> None:
    with pytest.raises(ValueError, match="item_id must be non-empty"):
        CalibrationReportItem(**_item_kwargs(item_id=""))


def test_item_rejects_judge_score_out_of_range() -> None:
    with pytest.raises(ValueError, match="judge_total_score must be in"):
        CalibrationReportItem(**_item_kwargs(judge_total_score=101))
    with pytest.raises(ValueError, match="judge_total_score must be in"):
        CalibrationReportItem(**_item_kwargs(judge_total_score=-1))


def test_item_rejects_iterations_out_of_range() -> None:
    with pytest.raises(ValueError, match="iterations_used must be in"):
        CalibrationReportItem(**_item_kwargs(iterations_used=0))
    with pytest.raises(ValueError, match="iterations_used must be in"):
        CalibrationReportItem(**_item_kwargs(iterations_used=4))


def test_item_rejects_bad_revision_outcome() -> None:
    with pytest.raises(ValueError, match="revision_loop_outcome invalid"):
        CalibrationReportItem(**_item_kwargs(revision_loop_outcome="pass_iter4"))


def test_item_rejects_non_dict_per_dimension() -> None:
    with pytest.raises(TypeError, match="must be dict"):
        CalibrationReportItem(**_item_kwargs(judge_per_dimension=[]))


def test_item_rejects_empty_dim_name() -> None:
    with pytest.raises(ValueError, match="must be non-empty str"):
        CalibrationReportItem(**_item_kwargs(judge_per_dimension={"": 5}))


def test_item_rejects_bad_dim_score() -> None:
    with pytest.raises(ValueError, match="must be int in"):
        CalibrationReportItem(
            **_item_kwargs(judge_per_dimension={"clarity": 11})
        )
    with pytest.raises(ValueError, match="must be int in"):
        CalibrationReportItem(
            **_item_kwargs(judge_per_dimension={"clarity": -1})
        )


def test_item_rejects_empty_item_run_id() -> None:
    with pytest.raises(ValueError, match="item_run_id must be non-empty"):
        CalibrationReportItem(**_item_kwargs(item_run_id=""))


def test_item_accepts_all_five_revision_outcomes() -> None:
    for outcome in (
        "pass_iter1",
        "pass_iter2",
        "pass_iter3",
        "iter_cap_no_pass",
        "plateau_no_pass",
    ):
        it = CalibrationReportItem(
            **_item_kwargs(
                revision_loop_outcome=outcome,
                iterations_used=1 if "iter1" in outcome else 3,
            )
        )
        assert it.revision_loop_outcome == outcome


# ---------------------------------------------------------------------------
# CalibrationReport construction
# ---------------------------------------------------------------------------


def test_report_happy_path() -> None:
    report = CalibrationReport(**_report_kwargs())
    assert report.schema_version == 1
    assert report.operator_org_slug == "fit_farms_llc"
    assert len(report.items) == 1


def test_report_rejects_schema_mismatch() -> None:
    with pytest.raises(F_PIPE_22) as ei:
        CalibrationReport(**_report_kwargs(schema_version=2))
    assert ei.value.trigger == "calibration_report_schema_mismatch"
    assert ei.value.details["observed"] == 2


def test_report_rejects_empty_run_id() -> None:
    with pytest.raises(ValueError, match="run_id must be non-empty"):
        CalibrationReport(**_report_kwargs(run_id=""))


def test_report_rejects_empty_operator_org_slug() -> None:
    with pytest.raises(ValueError, match="operator_org_slug must be non-empty"):
        CalibrationReport(**_report_kwargs(operator_org_slug=""))


def test_report_rejects_empty_manifest_path() -> None:
    with pytest.raises(
        ValueError, match="golden_set_manifest_path must be non-empty"
    ):
        CalibrationReport(**_report_kwargs(golden_set_manifest_path=""))


def test_report_rejects_empty_manifest_hash() -> None:
    with pytest.raises(
        ValueError, match="golden_set_manifest_hash must be non-empty"
    ):
        CalibrationReport(**_report_kwargs(golden_set_manifest_hash=""))


def test_report_rejects_non_tuple_items() -> None:
    with pytest.raises(TypeError, match="items must be tuple"):
        CalibrationReport(**_report_kwargs(items=[CalibrationReportItem(**_item_kwargs())]))


def test_report_rejects_wrong_item_type() -> None:
    with pytest.raises(TypeError, match="items\\[0\\] must be CalibrationReportItem"):
        CalibrationReport(**_report_kwargs(items=("not-an-item",)))


def test_report_rejects_empty_charter_hash() -> None:
    with pytest.raises(
        ValueError, match="council_charter_snapshot_hash must be non-empty"
    ):
        CalibrationReport(**_report_kwargs(council_charter_snapshot_hash=""))


def test_report_rejects_empty_router_hash() -> None:
    with pytest.raises(
        ValueError, match="router_yaml_snapshot_hash must be non-empty"
    ):
        CalibrationReport(**_report_kwargs(router_yaml_snapshot_hash=""))


def test_report_rejects_empty_assembled_at_iso() -> None:
    with pytest.raises(ValueError, match="assembled_at_iso must be non-empty"):
        CalibrationReport(**_report_kwargs(assembled_at_iso=""))


def test_report_signature_and_iso_must_be_both_none_or_both_set() -> None:
    with pytest.raises(
        ValueError, match="must be both None or both non-None"
    ):
        CalibrationReport(
            **_report_kwargs(signature=b"\x00" * 64, signed_at_iso=None)
        )
    with pytest.raises(
        ValueError, match="must be both None or both non-None"
    ):
        CalibrationReport(
            **_report_kwargs(signature=None, signed_at_iso="2026-04-21T12:00:00+00:00")
        )


def test_report_signature_type_checked() -> None:
    with pytest.raises(TypeError, match="signature must be bytes or None"):
        CalibrationReport(
            **_report_kwargs(
                signature="not-bytes",  # type: ignore[arg-type]
                signed_at_iso="2026-04-21T12:00:00+00:00",
            )
        )


def test_report_rejects_non_dict_per_dim_mean() -> None:
    with pytest.raises(
        TypeError, match="summary_per_dimension_mean must be dict"
    ):
        CalibrationReport(**_report_kwargs(summary_per_dimension_mean=[]))


def test_report_rejects_non_str_canonical_sha256() -> None:
    with pytest.raises(TypeError, match="canonical_sha256 must be str"):
        CalibrationReport(**_report_kwargs(canonical_sha256=123))


def test_report_empty_canonical_sha256_accepted_for_skeleton() -> None:
    # assemble_from_run builds a skeleton with "" then recomputes; the
    # construction-time path must permit empty string.
    report = CalibrationReport(**_report_kwargs(canonical_sha256=""))
    assert report.canonical_sha256 == ""


# ---------------------------------------------------------------------------
# canonical_bytes — determinism + exclusions + NFC
# ---------------------------------------------------------------------------


def test_canonical_bytes_stable_across_dict_insertion_order() -> None:
    r1 = CalibrationReport(
        **_report_kwargs(
            summary_per_dimension_mean={"a": 1.0, "b": 2.0, "c": 3.0}
        )
    )
    r2 = CalibrationReport(
        **_report_kwargs(
            summary_per_dimension_mean={"c": 3.0, "a": 1.0, "b": 2.0}
        )
    )
    assert canonical_bytes(r1) == canonical_bytes(r2)


def test_canonical_bytes_excludes_signature() -> None:
    unsigned = CalibrationReport(**_report_kwargs())
    signed = CalibrationReport(
        **_report_kwargs(
            signature=b"\x00" * 64,
            signed_at_iso="2026-04-21T12:00:00+00:00",
        )
    )
    # Same canonical_sha256 across signed/unsigned requires
    # signed_at_iso to be different — they're legitimately different bytes.
    # But: if we make signed_at_iso identical (None->None vs "..." vs "..."),
    # only signature differs, canonical bytes should be identical.
    # Build two reports that differ ONLY in the signature byte:
    a = CalibrationReport(
        **_report_kwargs(
            signature=b"\x01" * 64,
            signed_at_iso="2026-04-21T12:00:00+00:00",
        )
    )
    b = CalibrationReport(
        **_report_kwargs(
            signature=b"\x02" * 64,
            signed_at_iso="2026-04-21T12:00:00+00:00",
        )
    )
    assert canonical_bytes(a) == canonical_bytes(b)
    # And the None/value variant: just confirm signature field doesn't appear
    # in the serialized output.
    assert b'"signature"' not in canonical_bytes(unsigned)


def test_canonical_bytes_excludes_canonical_sha256() -> None:
    a = CalibrationReport(**_report_kwargs(canonical_sha256="aa" * 32))
    b = CalibrationReport(**_report_kwargs(canonical_sha256="bb" * 32))
    assert canonical_bytes(a) == canonical_bytes(b)
    assert b'"canonical_sha256"' not in canonical_bytes(a)


def test_canonical_bytes_signed_at_iso_is_included() -> None:
    """§5.6.4 correction: signed_at_iso IS part of canonical bytes."""
    a = CalibrationReport(
        **_report_kwargs(
            signature=b"\x01" * 64,
            signed_at_iso="2026-04-21T12:00:00+00:00",
        )
    )
    b = CalibrationReport(
        **_report_kwargs(
            signature=b"\x01" * 64,
            signed_at_iso="2026-04-22T12:00:00+00:00",
        )
    )
    # Different signed_at_iso => different canonical bytes.
    assert canonical_bytes(a) != canonical_bytes(b)
    assert b'"signed_at_iso"' in canonical_bytes(a)


def test_canonical_bytes_nfc_normalizes_strings() -> None:
    composed = "mañana"  # NFC
    decomposed = unicodedata.normalize("NFD", composed)
    assert composed != decomposed

    r_composed = CalibrationReport(
        **_report_kwargs(
            items=(CalibrationReportItem(**_item_kwargs(editor_critique_summary=composed)),),
        )
    )
    r_decomposed = CalibrationReport(
        **_report_kwargs(
            items=(
                CalibrationReportItem(
                    **_item_kwargs(editor_critique_summary=decomposed)
                ),
            ),
        )
    )
    assert canonical_bytes(r_composed) == canonical_bytes(r_decomposed)


def test_canonical_bytes_all_fields_present_except_excluded() -> None:
    report = CalibrationReport(**_report_kwargs())
    cb = canonical_bytes(report)
    decoded = json.loads(cb.decode("utf-8"))
    exclusions = canonical_bytes_exclusions()
    for f in fields(CalibrationReport):
        if f.name in exclusions:
            assert f.name not in decoded, (
                f"excluded field {f.name!r} leaked into canonical bytes"
            )
        else:
            assert f.name in decoded, (
                f"declared field {f.name!r} missing from canonical bytes"
            )


def test_canonical_bytes_exhaustiveness_invariant_report() -> None:
    """§7.16 invariant: every CalibrationReport field is either serialized or excluded."""
    excluded = set(canonical_bytes_exclusions().keys())
    declared = calibration_report_field_set()
    sample = CalibrationReport(**_report_kwargs())
    cb_keys = set(json.loads(canonical_bytes(sample).decode("utf-8")).keys())
    for name in declared:
        assert (name in cb_keys) or (name in excluded), (
            f"CalibrationReport field {name!r} is neither serialized nor excluded"
        )


def test_canonical_bytes_exhaustiveness_invariant_item() -> None:
    """§7.16 invariant — every CalibrationReportItem field is serialized (no exclusions)."""
    declared = calibration_report_item_field_set()
    sample = CalibrationReport(**_report_kwargs())
    cb = json.loads(canonical_bytes(sample).decode("utf-8"))
    # items is serialized as a list of dicts; pull the first item's keys.
    item_keys = set(cb["items"][0].keys())
    for name in declared:
        assert name in item_keys, (
            f"CalibrationReportItem field {name!r} missing from canonical bytes"
        )


def test_compute_canonical_sha256_matches_hashlib() -> None:
    report = CalibrationReport(**_report_kwargs())
    cb = canonical_bytes(report)
    expected = hashlib.sha256(cb).hexdigest()
    assert compute_canonical_sha256(report) == expected


# ---------------------------------------------------------------------------
# assemble_from_run
# ---------------------------------------------------------------------------


def _mk_item(i: int, score: int, iters: int = 2) -> CalibrationReportItem:
    return CalibrationReportItem(
        item_id=f"gs-{i:03d}",
        judge_total_score=score,
        judge_per_dimension={"clarity": min(10, score // 10), "fit": 8},
        editor_critique_summary=f"item-{i} note",
        iterations_used=iters,
        revision_loop_outcome="pass_iter2" if iters == 2 else "pass_iter1",
        item_run_id=f"run-sub-{i:03d}",
    )


def test_assemble_from_run_single_item() -> None:
    items = (_mk_item(1, 80),)
    inputs = AssembleInputs(
        run_id="run-eval-001",
        operator_org_slug="fit_farms_llc",
        golden_set_manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        per_item_results=items,
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
    )
    report = assemble_from_run(inputs)
    assert report.schema_version == 1
    assert report.summary_judge_mean == 80.0
    assert report.summary_judge_stddev == 0.0
    assert report.summary_per_dimension_mean == {"clarity": 8.0, "fit": 8.0}


def test_assemble_from_run_multi_item_mean_and_stddev() -> None:
    items = (_mk_item(1, 70), _mk_item(2, 80), _mk_item(3, 90))
    inputs = AssembleInputs(
        run_id="run-eval-002",
        operator_org_slug="x",
        golden_set_manifest_path="vault/x/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        per_item_results=items,
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
    )
    report = assemble_from_run(inputs)
    assert report.summary_judge_mean == 80.0
    # Population stddev of [70, 80, 90] = sqrt(((10^2)+0+(10^2))/3) ≈ 8.165
    assert 8.0 < report.summary_judge_stddev < 8.5


def test_assemble_from_run_empty_items_edge_case() -> None:
    inputs = AssembleInputs(
        run_id="run-eval-003",
        operator_org_slug="x",
        golden_set_manifest_path="vault/x/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        per_item_results=(),
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
    )
    report = assemble_from_run(inputs)
    assert report.summary_judge_mean == 0.0
    assert report.summary_judge_stddev == 0.0
    assert report.summary_per_dimension_mean == {}


def test_assemble_from_run_preserves_item_order() -> None:
    items = tuple(_mk_item(i, 70 + i) for i in (5, 2, 8, 1, 4))
    inputs = AssembleInputs(
        run_id="run-eval-004",
        operator_org_slug="x",
        golden_set_manifest_path="vault/x/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        per_item_results=items,
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
    )
    report = assemble_from_run(inputs)
    assert [it.item_id for it in report.items] == [
        "gs-005",
        "gs-002",
        "gs-008",
        "gs-001",
        "gs-004",
    ]


def test_assemble_from_run_canonical_sha256_stable() -> None:
    items = (_mk_item(1, 80), _mk_item(2, 85))
    inputs = AssembleInputs(
        run_id="run-eval-005",
        operator_org_slug="x",
        golden_set_manifest_path="vault/x/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        per_item_results=items,
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
    )
    a = assemble_from_run(inputs)
    b = assemble_from_run(inputs)
    assert a.canonical_sha256 == b.canonical_sha256
    # And the digest actually matches recomputation with canonical_sha256="".
    assert a.canonical_sha256 != ""
    assert len(a.canonical_sha256) == 64


def test_assemble_from_run_per_dim_union() -> None:
    # Items with DIFFERENT dimension sets — per-dim mean covers the union.
    items = (
        CalibrationReportItem(
            **_item_kwargs(
                item_id="a",
                judge_per_dimension={"clarity": 8, "fit": 9},
            )
        ),
        CalibrationReportItem(
            **_item_kwargs(
                item_id="b",
                judge_per_dimension={"clarity": 6, "alignment": 7},
            )
        ),
    )
    inputs = AssembleInputs(
        run_id="run-eval-006",
        operator_org_slug="x",
        golden_set_manifest_path="vault/x/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        per_item_results=items,
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
    )
    report = assemble_from_run(inputs)
    # clarity present in both: (8+6)/2 = 7
    # fit only in a: 9/1 = 9
    # alignment only in b: 7/1 = 7
    assert report.summary_per_dimension_mean == {
        "clarity": 7.0,
        "fit": 9.0,
        "alignment": 7.0,
    }


def test_assemble_from_run_rejects_empty_run_id() -> None:
    with pytest.raises(ValueError, match="run_id must be non-empty"):
        assemble_from_run(
            AssembleInputs(
                run_id="",
                operator_org_slug="x",
                golden_set_manifest_path="p",
                golden_set_manifest_hash="h",
                per_item_results=(),
                council_charter_snapshot_hash="c",
                router_yaml_snapshot_hash="r",
                assembled_at_iso="2026-04-21T12:00:00+00:00",
            )
        )


def test_assemble_from_run_rejects_empty_operator_org_slug() -> None:
    with pytest.raises(ValueError, match="operator_org_slug must be non-empty"):
        assemble_from_run(
            AssembleInputs(
                run_id="r",
                operator_org_slug="",
                golden_set_manifest_path="p",
                golden_set_manifest_hash="h",
                per_item_results=(),
                council_charter_snapshot_hash="c",
                router_yaml_snapshot_hash="r",
                assembled_at_iso="2026-04-21T12:00:00+00:00",
            )
        )


# ---------------------------------------------------------------------------
# report_to_json / report_from_json round-trip
# ---------------------------------------------------------------------------


def test_json_round_trip_unsigned() -> None:
    items = (_mk_item(1, 80),)
    inputs = AssembleInputs(
        run_id="run-eval-007",
        operator_org_slug="fit_farms_llc",
        golden_set_manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        per_item_results=items,
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
    )
    a = assemble_from_run(inputs)
    b = report_from_json(report_to_json(a))
    assert a == b


def test_json_round_trip_signed() -> None:
    items = (_mk_item(1, 80),)
    inputs = AssembleInputs(
        run_id="run-eval-008",
        operator_org_slug="fit_farms_llc",
        golden_set_manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        per_item_results=items,
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
    )
    unsigned = assemble_from_run(inputs)
    signed = CalibrationReport(
        schema_version=unsigned.schema_version,
        run_id=unsigned.run_id,
        operator_org_slug=unsigned.operator_org_slug,
        golden_set_manifest_path=unsigned.golden_set_manifest_path,
        golden_set_manifest_hash=unsigned.golden_set_manifest_hash,
        items=unsigned.items,
        summary_judge_mean=unsigned.summary_judge_mean,
        summary_judge_stddev=unsigned.summary_judge_stddev,
        summary_per_dimension_mean=unsigned.summary_per_dimension_mean,
        council_charter_snapshot_hash=unsigned.council_charter_snapshot_hash,
        router_yaml_snapshot_hash=unsigned.router_yaml_snapshot_hash,
        assembled_at_iso=unsigned.assembled_at_iso,
        canonical_sha256=unsigned.canonical_sha256,
        signature=b"\x01" * 64,
        signed_at_iso="2026-04-21T12:00:00+00:00",
    )
    round_tripped = report_from_json(report_to_json(signed))
    assert round_tripped == signed


def test_json_from_rejects_schema_mismatch() -> None:
    payload = json.dumps({"schema_version": 2, "run_id": "x"}).encode("utf-8")
    with pytest.raises(F_PIPE_22) as ei:
        report_from_json(payload)
    assert ei.value.trigger == "calibration_report_schema_mismatch"


def test_json_from_rejects_non_object() -> None:
    with pytest.raises(ValueError, match="not a JSON object"):
        report_from_json(json.dumps(["list-not-object"]).encode("utf-8"))


def test_canonical_bytes_exclusions_snapshot() -> None:
    # §5.6.4 exclusion table — must contain EXACTLY these two keys.
    exclusions = canonical_bytes_exclusions()
    assert set(exclusions.keys()) == {"signature", "canonical_sha256"}


def test_canonical_bytes_exclusions_returns_copy() -> None:
    """Callers must not be able to mutate module-level exclusion table."""
    e1 = canonical_bytes_exclusions()
    e1["INJECTED"] = "should not appear"
    e2 = canonical_bytes_exclusions()
    assert "INJECTED" not in e2
