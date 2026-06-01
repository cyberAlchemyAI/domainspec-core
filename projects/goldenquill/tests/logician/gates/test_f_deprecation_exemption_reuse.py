"""Unit tests for F-DEPRECATION-EXEMPTION-REUSE (F-AMDT-06)."""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_06,
    DeprecationExemptionDetail,
    DeprecationExemptionResult,
    check_deprecation_exemption_reuse,
)


def _exists_true(_: str) -> bool:
    return True


def _exists_false(_: str) -> bool:
    return False


def _artifact(verdict: dict, *, cycle_fixes: list | None = None) -> dict:
    d = {"red_team_verdict": verdict}
    if cycle_fixes is not None:
        d["cycle_fixes"] = cycle_fixes
    return d


def _make_reader(artifact: dict):
    def _r(_: str) -> dict:
        return artifact
    return _r


# ---------------------------------------------------------------------------
# Trigger discipline — no-op PASS when gate doesn't fire
# ---------------------------------------------------------------------------


def test_forced_replacement_absent_no_op() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"title": "routine amendment"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is True
    assert r.detail is None


def test_forced_replacement_false_no_op() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": False},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is True


@pytest.mark.parametrize("bogus", ["true", "True", 1, 0, [], {}, None])
def test_forced_replacement_truthy_but_not_true_no_op(bogus: object) -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": bogus},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Happy path — clean verdict
# ---------------------------------------------------------------------------


def test_clean_non_blocking_verdict_passes() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p/audit.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(
            _artifact({"blocking": False, "findings": []})
        ),
    )
    assert r.success is True


def test_clean_non_blocking_verdict_with_no_findings_key_passes() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "p/audit.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({"red_team_verdict": {"blocking": False}}),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Happy path — blocking with full cycle_fixes coverage
# ---------------------------------------------------------------------------


def test_blocking_with_all_findings_addressed_passes() -> None:
    verdict = {
        "blocking": True,
        "findings": [
            {"finding_id": "F1"},
            {"finding_id": "F2"},
            {"finding_id": "F3"},
        ],
    }
    fixes = [
        {"finding_id": "F1", "fix_description": "fixed", "closure_evidence": "commit"},
        {"finding_id": "F2", "fix_description": "fixed", "closure_evidence": "commit"},
        {"finding_id": "F3", "fix_description": "fixed", "closure_evidence": "commit"},
    ]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p/a.md"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is True


def test_blocking_with_extra_fixes_passes() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}]}
    fixes = [
        {"finding_id": "F1", "fix_description": "fixed", "closure_evidence": "ok"},
        {"finding_id": "F99", "fix_description": "redundant", "closure_evidence": "ok"},
    ]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p/a.md"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is True


@pytest.mark.parametrize("n", [1, 2, 5, 10])
def test_scale_all_findings_addressed(n: int) -> None:
    ids = [f"F{i}" for i in range(n)]
    verdict = {"blocking": True, "findings": [{"finding_id": fid} for fid in ids]}
    fixes = [
        {"finding_id": fid, "fix_description": "x", "closure_evidence": "y"}
        for fid in ids
    ]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Denial paths — missing artifact
# ---------------------------------------------------------------------------


def test_audit_path_missing_denied() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_06
    assert r.detail.reason_tag == "audit_artifact_path_missing"


def test_audit_path_empty_string_denied() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "audit_artifact_path_missing"


def test_audit_path_non_string_denied() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": 42,
        },
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "audit_artifact_path_missing"


def test_file_does_not_exist_denied() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_false,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "audit_artifact_file_absent"


# ---------------------------------------------------------------------------
# Artifact shape failures
# ---------------------------------------------------------------------------


def test_artifact_empty_dict_denied() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "red_team_verdict_key_missing"


def test_artifact_not_a_dict_denied() -> None:
    def _reader(_: str) -> dict:
        return "not a dict"  # type: ignore[return-value]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_reader,
    )
    assert r.success is False
    assert r.detail.reason_tag == "audit_artifact_not_dict"


def test_red_team_not_a_dict_denied() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({"red_team_verdict": "bad"}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "red_team_verdict_not_dict"


@pytest.mark.parametrize("bad_blocking", [1, 0, "true", "false", None, [], {}])
def test_blocking_not_strict_bool_denied(bad_blocking: object) -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact({"blocking": bad_blocking})),
    )
    assert r.success is False
    assert r.detail.reason_tag == "red_team_blocking_not_bool"


def test_findings_not_a_list_denied() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(
            {"red_team_verdict": {"blocking": True, "findings": "not a list"}}
        ),
    )
    assert r.success is False
    assert r.detail.reason_tag == "red_team_findings_not_list"


def test_cycle_fixes_not_a_list_denied() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}]}
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(
            {"red_team_verdict": verdict, "cycle_fixes": "not a list"}
        ),
    )
    assert r.success is False
    assert r.detail.reason_tag == "cycle_fixes_not_list"


# ---------------------------------------------------------------------------
# Unaddressed findings
# ---------------------------------------------------------------------------


def test_blocking_with_no_fixes_denied() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}]}
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=[])),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"
    assert r.detail.unaddressed_finding_ids == ("F1",)


def test_blocking_with_partial_coverage_denied() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}, {"finding_id": "F2"}]}
    fixes = [{"finding_id": "F1", "fix_description": "x", "closure_evidence": "y"}]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is False
    assert r.detail.unaddressed_finding_ids == ("F2",)


def test_blocking_fix_empty_description_denied() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}]}
    fixes = [{"finding_id": "F1", "fix_description": "", "closure_evidence": "evidence"}]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"


def test_blocking_fix_empty_closure_evidence_denied() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}]}
    fixes = [{"finding_id": "F1", "fix_description": "did it", "closure_evidence": ""}]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"


def test_blocking_fix_mismatched_finding_id_denied() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}]}
    fixes = [{"finding_id": "F99", "fix_description": "x", "closure_evidence": "y"}]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is False
    assert r.detail.unaddressed_finding_ids == ("F1",)


def test_finding_without_finding_id_denied() -> None:
    """A blocking finding without a finding_id cannot be addressed by any fix."""
    verdict = {"blocking": True, "findings": [{"description": "bad thing"}]}
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=[])),
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_findings_without_matching_fixes"
    assert any("findings_without_finding_id" in fid for fid in r.detail.unaddressed_finding_ids)


def test_blocking_duplicate_finding_id_requires_two_fixes() -> None:
    """Two findings with the same finding_id each need their own fix entry."""
    verdict = {
        "blocking": True,
        "findings": [{"finding_id": "F1"}, {"finding_id": "F1"}],
    }
    fixes = [
        {"finding_id": "F1", "fix_description": "x", "closure_evidence": "y"},
    ]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is False
    assert r.detail.unaddressed_finding_ids == ("F1",)


def test_blocking_duplicate_finding_id_with_two_fixes_passes() -> None:
    verdict = {
        "blocking": True,
        "findings": [{"finding_id": "F1"}, {"finding_id": "F1"}],
    }
    fixes = [
        {"finding_id": "F1", "fix_description": "x", "closure_evidence": "y"},
        {"finding_id": "F1", "fix_description": "x2", "closure_evidence": "y2"},
    ]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Fix-entry shape failures
# ---------------------------------------------------------------------------


def test_fix_missing_finding_id_not_counted() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}]}
    fixes = [
        {"fix_description": "x", "closure_evidence": "y"},  # no finding_id
        {"finding_id": "F1", "fix_description": "x", "closure_evidence": "y"},
    ]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    # Second fix covers F1; first is ignored — PASS.
    assert r.success is True


def test_fix_not_a_dict_ignored() -> None:
    verdict = {"blocking": True, "findings": [{"finding_id": "F1"}]}
    fixes = [
        "malformed string",
        {"finding_id": "F1", "fix_description": "x", "closure_evidence": "y"},
    ]
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader(_artifact(verdict, cycle_fixes=fixes)),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Result shape
# ---------------------------------------------------------------------------


def test_pass_result_shape() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert isinstance(r, DeprecationExemptionResult)
    assert r.detail is None


def test_fail_result_shape() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    assert isinstance(r, DeprecationExemptionResult)
    assert isinstance(r.detail, DeprecationExemptionDetail)
    assert r.failure_code == F_AMDT_06


def test_result_is_frozen() -> None:
    r = check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True},
        file_exists=_exists_true,
        audit_artifact_reader=_make_reader({}),
    )
    with pytest.raises(Exception):
        r.success = True  # type: ignore[misc]


def test_failure_code_constant_value() -> None:
    assert F_AMDT_06 == "F-AMDT-06"


# ---------------------------------------------------------------------------
# Reader call discipline
# ---------------------------------------------------------------------------


def test_reader_called_exactly_once_on_pass() -> None:
    reads = {"n": 0}
    def _reader(_: str) -> dict:
        reads["n"] += 1
        return _artifact({"blocking": False})
    check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_true,
        audit_artifact_reader=_reader,
    )
    assert reads["n"] == 1


def test_reader_not_called_when_gate_doesnt_fire() -> None:
    reads = {"n": 0}
    def _reader(_: str) -> dict:
        reads["n"] += 1
        return {}
    check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": False},
        file_exists=_exists_true,
        audit_artifact_reader=_reader,
    )
    assert reads["n"] == 0


def test_reader_not_called_when_file_absent() -> None:
    reads = {"n": 0}
    def _reader(_: str) -> dict:
        reads["n"] += 1
        return {}
    check_deprecation_exemption_reuse(
        amendment_frontmatter={"forced_replacement": True, "audit_artifact_path": "p"},
        file_exists=_exists_false,
        audit_artifact_reader=_reader,
    )
    assert reads["n"] == 0


def test_file_exists_called_with_exact_path() -> None:
    paths: list[str] = []
    def _checker(p: str) -> bool:
        paths.append(p)
        return False
    check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "orgs/mycosymbiotics/audits/2026-04-20.md",
        },
        file_exists=_checker,
        audit_artifact_reader=_make_reader({}),
    )
    assert paths == ["orgs/mycosymbiotics/audits/2026-04-20.md"]


def test_reader_called_with_exact_path() -> None:
    reader_paths: list[str] = []
    def _reader(p: str) -> dict:
        reader_paths.append(p)
        return _artifact({"blocking": False})
    check_deprecation_exemption_reuse(
        amendment_frontmatter={
            "forced_replacement": True,
            "audit_artifact_path": "orgs/mycosymbiotics/audits/2026-04-20.md",
        },
        file_exists=_exists_true,
        audit_artifact_reader=_reader,
    )
    assert reader_paths == ["orgs/mycosymbiotics/audits/2026-04-20.md"]
