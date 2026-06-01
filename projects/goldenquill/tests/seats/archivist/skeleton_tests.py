"""§15 Archivist — skeleton tests at LOCK ceremony.

Spec card: ``pipeline/blueprint/v0.1/section_15_archivist.md`` (§15 v1 LOCKED 2026-05-10).

Skeleton-test scope (per §15.13.1 + §15.15 LOCK ceremony done-definition; NON-NEGOTIABLE
per dispatch packet — these prevent any future contributor from quietly turning the stub
into auto-apply behavior):

- Validate exactly two cadences register in the dispatcher (§15.6.0 cadence summary).
- Validate the v1 gate codes resolve to imported predicate stubs raising NotImplementedError.
- Validate input/output dataclasses are frozen + kw_only per Tilth convention.
- Validate proposes-only structural discipline at the AST level: no canonical-write-intent
  calls; no subprocess of canonical-write CLI (RT-01); no foreign-helper file-write imports
  (RT-02); no raw open() against canonical-substrate paths (RT-11); no yaml.load (RT-09);
  all writes target only the allowed digest-prefix paths.
- Validate zero network egress (sovereignty promise).

Full per-gate behavior tests + per-cadence integration tests live at v1.x amendment per
§15.13.2 (the v1.x horizon test list includes test_f_archivist_cadence_drift_is_fail_closed_at_v1_x,
test_f_archivist_read_without_vault_intent_raw_open, test_f_archivist_auto_apply_subprocess_canonical_cli,
etc.).
"""

from __future__ import annotations

import ast
from dataclasses import is_dataclass
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.orchestrator.seats.archivist import (
    ArchivistQuarterlyPerOrgInput,
    ArchivistQuarterlyWorkspaceInput,
    ArchivistState,
    ArchivistWeeklyInput,
    FunderIntelQuarterlyEntry,
    GateResult,
    KfrRefreshDigestEntry,
    LessonsProposalEntry,
    MatchDbLessonsDeltaEntry,
    f_archivist_auto_apply_attempted,
    f_archivist_cadence_drift,
    f_archivist_cross_org_leak,
    f_archivist_lesson_instance_leak,
    f_archivist_read_without_vault_intent,
    get_cadence_handler_name,
    get_quarterly_submode_handler_name,
    list_registered_cadences,
    list_registered_quarterly_submodes,
)


# ---------------------------------------------------------------------------
# §15.6.0 cadence dispatch tests
# ---------------------------------------------------------------------------


def test_two_cadences_register_in_dispatcher() -> None:
    """Per §15.6.0: assert exactly two cadences registered (weekly + quarterly).

    Quarterly further routes to quarterly_workspace OR quarterly_per_org per §15.4.2 split
    — those are submodes of quarterly, not separate top-level cadences. No third top-level
    cadence silently leaks through type-checker holes.
    """
    cadences = list_registered_cadences()
    assert len(cadences) == 2
    assert set(cadences) == {"weekly", "quarterly"}


def test_two_quarterly_submodes_register_in_dispatcher() -> None:
    """Per §15.4.2: assert exactly two quarterly submodes registered."""
    submodes = list_registered_quarterly_submodes()
    assert len(submodes) == 2
    assert set(submodes) == {"quarterly_workspace", "quarterly_per_org"}


def test_cadence_handler_lookup_weekly() -> None:
    """weekly cadence resolves to weekly_tick handler."""
    assert get_cadence_handler_name("weekly") == "weekly_tick"


def test_cadence_handler_lookup_quarterly() -> None:
    """quarterly cadence resolves to quarterly_review handler."""
    assert get_cadence_handler_name("quarterly") == "quarterly_review"


def test_cadence_handler_unknown_cadence_raises() -> None:
    """Unknown cadence raises ValueError with available cadences listed."""
    with pytest.raises(ValueError, match="Unknown Archivist cadence"):
        get_cadence_handler_name("bogus")  # type: ignore[arg-type]


def test_quarterly_submode_handler_lookup_workspace() -> None:
    """quarterly_workspace submode resolves to quarterly_workspace_review handler."""
    assert get_quarterly_submode_handler_name("quarterly_workspace") == "quarterly_workspace_review"


def test_quarterly_submode_handler_lookup_per_org() -> None:
    """quarterly_per_org submode resolves to quarterly_per_org_review handler."""
    assert get_quarterly_submode_handler_name("quarterly_per_org") == "quarterly_per_org_review"


# ---------------------------------------------------------------------------
# §15.4 input contracts — frozen + kw_only per Tilth convention
# ---------------------------------------------------------------------------


def test_archivist_weekly_input_is_frozen_kw_only() -> None:
    """ArchivistWeeklyInput is frozen + kw_only dataclass (per §15.4.1)."""
    assert is_dataclass(ArchivistWeeklyInput)
    sample = ArchivistWeeklyInput(
        run_id="test-run",
        org_slug="test_org",
        kfr_register_path="orgs/test_org/vault/kfr/register.yaml",
        match_database_path="orgs/test_org/match_database/register.yaml",
        lessons_json_path="pipeline/institutional_memory/lessons.json",
    )
    with pytest.raises(Exception):  # FrozenInstanceError
        sample.org_slug = "other_org"  # type: ignore[misc]


def test_archivist_quarterly_workspace_input_is_frozen_kw_only() -> None:
    """ArchivistQuarterlyWorkspaceInput is frozen + kw_only (per §15.4.2.A)."""
    assert is_dataclass(ArchivistQuarterlyWorkspaceInput)
    sample = ArchivistQuarterlyWorkspaceInput(
        run_id="test-run",
        funder_intel_register_path="vault_shared/funder_intelligence/register.yaml",
        benchmarks_register_path="vault_shared/benchmarks/register.yaml",
    )
    with pytest.raises(Exception):
        sample.run_id = "other-run"  # type: ignore[misc]


def test_archivist_quarterly_per_org_input_is_frozen_kw_only() -> None:
    """ArchivistQuarterlyPerOrgInput is frozen + kw_only (per §15.4.2.B)."""
    assert is_dataclass(ArchivistQuarterlyPerOrgInput)
    sample = ArchivistQuarterlyPerOrgInput(
        run_id="test-run",
        org_slug="test_org",
        kfr_register_path="orgs/test_org/vault/kfr/register.yaml",
        match_database_path="orgs/test_org/match_database/register.yaml",
        reports_dir="orgs/test_org/vault/grants/",
    )
    with pytest.raises(Exception):
        sample.org_slug = "other_org"  # type: ignore[misc]


def test_archivist_weekly_input_default_lookback_window() -> None:
    """ArchivistWeeklyInput.lookback_window_days defaults to 7 (per §15.4.1)."""
    sample = ArchivistWeeklyInput(
        run_id="test-run",
        org_slug="test_org",
        kfr_register_path="orgs/test_org/vault/kfr/register.yaml",
        match_database_path="orgs/test_org/match_database/register.yaml",
        lessons_json_path="pipeline/institutional_memory/lessons.json",
    )
    assert sample.lookback_window_days == 7


def test_archivist_quarterly_workspace_default_freshness() -> None:
    """ArchivistQuarterlyWorkspaceInput.freshness_threshold_days defaults to 90 (per §15.4.2.A)."""
    sample = ArchivistQuarterlyWorkspaceInput(
        run_id="test-run",
        funder_intel_register_path="vault_shared/funder_intelligence/register.yaml",
        benchmarks_register_path="vault_shared/benchmarks/register.yaml",
    )
    assert sample.freshness_threshold_days == 90


def test_archivist_weekly_input_cadence_immutable() -> None:
    """ArchivistWeeklyInput.cadence is hardcoded to 'weekly'."""
    sample = ArchivistWeeklyInput(
        run_id="test-run",
        org_slug="test_org",
        kfr_register_path="orgs/test_org/vault/kfr/register.yaml",
        match_database_path="orgs/test_org/match_database/register.yaml",
        lessons_json_path="pipeline/institutional_memory/lessons.json",
    )
    assert sample.cadence == "weekly"


# ---------------------------------------------------------------------------
# §15.5 digest schemas — frozen + kw_only
# ---------------------------------------------------------------------------


def test_kfr_refresh_digest_entry_is_frozen_kw_only() -> None:
    """KfrRefreshDigestEntry is frozen + kw_only (per §15.5.0 schema delta)."""
    assert is_dataclass(KfrRefreshDigestEntry)


def test_match_db_lessons_delta_entry_is_frozen_kw_only() -> None:
    """MatchDbLessonsDeltaEntry is frozen + kw_only (per §15.5.0)."""
    assert is_dataclass(MatchDbLessonsDeltaEntry)


def test_funder_intel_quarterly_entry_is_frozen_kw_only() -> None:
    """FunderIntelQuarterlyEntry is frozen + kw_only (per §15.5.0)."""
    assert is_dataclass(FunderIntelQuarterlyEntry)


def test_lessons_proposal_entry_is_frozen_kw_only() -> None:
    """LessonsProposalEntry is frozen + kw_only (per §15.5.0)."""
    assert is_dataclass(LessonsProposalEntry)


def test_archivist_state_is_frozen_kw_only() -> None:
    """ArchivistState is frozen + kw_only (per Rule 1 Save State Always)."""
    assert is_dataclass(ArchivistState)


# ---------------------------------------------------------------------------
# §15.9 gate code resolution — predicates importable + raise NotImplementedError at v0.2
# ---------------------------------------------------------------------------


def test_v1_gate_codes_resolve_to_predicates() -> None:
    """Per §15.9 v1 gate roster: 5 owned predicate stubs are importable + callable.

    F-ARCHIVIST-CROSS-ORG-LEAK             → f_archivist_cross_org_leak
    F-ARCHIVIST-LESSON-INSTANCE-LEAK       → f_archivist_lesson_instance_leak
    F-ARCHIVIST-AUTO-APPLY-ATTEMPTED       → f_archivist_auto_apply_attempted
    F-ARCHIVIST-CADENCE-DRIFT              → f_archivist_cadence_drift
    F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT  → f_archivist_read_without_vault_intent (NEW per RT-11)
    """
    predicates = [
        f_archivist_cross_org_leak,
        f_archivist_lesson_instance_leak,
        f_archivist_auto_apply_attempted,
        f_archivist_cadence_drift,
        f_archivist_read_without_vault_intent,
    ]
    for predicate in predicates:
        assert callable(predicate), f"{predicate.__name__} is not callable"


def test_gate_predicates_raise_not_implemented_at_v0_2() -> None:
    """Skeleton predicates raise NotImplementedError at v0.2 LOCK.

    Full predicate bodies land at v1.x amendment per §15.9 + §15.12 v0.2-vs-v1.x posture
    summary. The skeleton tests confirm the predicates are importable + callable; full
    per-gate behavior tests live in tests/logician/gates/test_f_archivist_*.py after the
    §4 v2.x amendment populates them at v1.x.
    """
    sample_input = ArchivistWeeklyInput(
        run_id="test-run",
        org_slug="test_org",
        kfr_register_path="orgs/test_org/vault/kfr/register.yaml",
        match_database_path="orgs/test_org/match_database/register.yaml",
        lessons_json_path="pipeline/institutional_memory/lessons.json",
    )
    with pytest.raises(NotImplementedError, match="§15.9.1 predicate scaffold"):
        f_archivist_cross_org_leak(cadence_input=sample_input)
    with pytest.raises(NotImplementedError, match="§15.9.2 predicate scaffold"):
        f_archivist_lesson_instance_leak(
            proposed_lesson_text="test", org_index_path="orgs/ORG_INDEX.md",
            funder_intel_register_path="vault_shared/funder_intelligence/register.yaml",
        )
    with pytest.raises(NotImplementedError, match="§15.9.3 predicate scaffold"):
        f_archivist_auto_apply_attempted(
            attempted_write_path="orgs/test/vault/kfr/register.yaml",
            attempted_call_site="archivist:test",
        )
    with pytest.raises(NotImplementedError, match="§15.9.4 predicate scaffold"):
        f_archivist_cadence_drift(
            current_invocation_at_utc=datetime.now(timezone.utc),
            prior_state_path=None,
            cadence="weekly",
        )
    with pytest.raises(NotImplementedError, match="§15.9.5 predicate scaffold"):
        f_archivist_read_without_vault_intent(
            attempted_read_path="orgs/test/vault/kfr/register.yaml",
            attempted_call_site="archivist:test",
        )


def test_gate_result_pass_factory() -> None:
    """GateResult.PASS() returns passed=True."""
    result = GateResult.PASS()
    assert result.passed is True
    assert result.code is None


def test_gate_result_fail_factory() -> None:
    """GateResult.FAIL() returns passed=False with code + sub_tag + detail."""
    result = GateResult.FAIL(
        code="F-ARCHIVIST-CROSS-ORG-LEAK",
        sub_tag=".symlink_escape",
        detail="Path resolves outside org subtree",
    )
    assert result.passed is False
    assert result.code == "F-ARCHIVIST-CROSS-ORG-LEAK"
    assert result.sub_tag == ".symlink_escape"


# ---------------------------------------------------------------------------
# §15.9.3 + §15.9.5 proposes-only AST-lint — implemented as pytest assertions at v0.2
# (the §4 v2.x amendment promotes these to proper AST-lint rules at v1.x)
# ---------------------------------------------------------------------------


_ARCHIVIST_SEAT_DIR = Path(__file__).resolve().parents[3] / "pipeline" / "orchestrator" / "seats" / "archivist"


def _archivist_seat_source_files() -> list[Path]:
    """Return all .py source files under the Archivist seat package."""
    return sorted(_ARCHIVIST_SEAT_DIR.rglob("*.py"))


def _walk_seat_ast() -> list[tuple[Path, ast.AST]]:
    """Return (path, AST) pairs for every Archivist seat source file."""
    out = []
    for path in _archivist_seat_source_files():
        with path.open("r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(path))
        out.append((path, tree))
    return out


# Forbidden canonical-write-intent + canonical-CLI tokens (per §15.9.3 R-ARCHIVIST-NO-CANONICAL-MUTATE)
_FORBIDDEN_WRITE_INTENT_NAMES = {
    "kfr_write_intent",
    "funder_intel_write_intent",
    "match_db_write_intent",
    "lessons_json_write_intent",
    "benchmarks_write_intent",
}

_FORBIDDEN_CLI_TOKENS = {"tilth", "kfr", "funder-intel", "match-db", "lessons", "benchmarks"}

_FORBIDDEN_PROCESS_CREATION_NAMES = {
    "Popen",  # subprocess.Popen
    "run",    # subprocess.run
    "call",   # subprocess.call
    "check_call",
    "check_output",
    "system",  # os.system
    "popen",   # os.popen
    "spawn",   # os.spawn*
    "spawnl",
    "spawnle",
    "spawnlp",
    "spawnlpe",
    "spawnv",
    "spawnve",
    "spawnvp",
    "spawnvpe",
    "exec",  # os.exec*
    "execv",
    "execve",
    "execvp",
    "execvpe",
    "execl",
    "execle",
    "execlp",
    "execlpe",
}


def test_archivist_proposes_only_no_canonical_write_intent_calls() -> None:
    """Per §15.9.3 R-ARCHIVIST-NO-CANONICAL-MUTATE — no direct canonical-write-intent calls.

    Scans pipeline/orchestrator/seats/archivist/** for any call to KFR / Funder Intel / Match
    DB / lessons.json / Benchmarks Register canonical write intents. Mismatch → test fail
    (signals a future contributor introduced a forbidden write path; CI catches before merge).
    """
    violations: list[tuple[Path, int, str]] = []
    for path, tree in _walk_seat_ast():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name: str | None = None
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                if func_name in _FORBIDDEN_WRITE_INTENT_NAMES:
                    violations.append((path, node.lineno, func_name))
    assert not violations, (
        f"R-ARCHIVIST-NO-CANONICAL-MUTATE violations (canonical write intent calls): {violations}"
    )


def test_archivist_no_subprocess_canonical_cli() -> None:
    """Per §15.9.3 RT-01 closure — no subprocess of `tilth <substrate-cli>` from Archivist.

    Scans for subprocess.* / os.system / os.popen / os.exec* / os.spawn* / pexpect.* calls;
    if any literal argument contains forbidden tokens (tilth + canonical-write sub-commands),
    fail the test. This is the AST-lint rule at the pytest layer; §4 v2.x amendment
    promotes to a proper AST-lint rule at v1.x.
    """
    violations: list[tuple[Path, int, str]] = []
    for path, tree in _walk_seat_ast():
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            # Detect the call name (subprocess.run, os.system, etc.)
            call_name: str | None = None
            if isinstance(node.func, ast.Attribute):
                call_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                call_name = node.func.id
            if call_name not in _FORBIDDEN_PROCESS_CREATION_NAMES:
                continue
            # Inspect the call arguments for forbidden CLI tokens
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if any(tok in arg.value for tok in _FORBIDDEN_CLI_TOKENS):
                        violations.append((path, node.lineno, f"{call_name}({arg.value!r})"))
                elif isinstance(arg, ast.List):
                    for elt in arg.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            if elt.value in _FORBIDDEN_CLI_TOKENS:
                                violations.append((path, node.lineno, f"{call_name}([..., {elt.value!r}, ...])"))
    assert not violations, (
        f"RT-01 closure violations (subprocess of canonical-write CLI from Archivist): {violations}"
    )


def test_archivist_no_raw_open_on_canonical_substrate() -> None:
    """Per §15.9.5 RT-11 closure — no raw open() against canonical-substrate paths.

    All canonical-substrate reads MUST go through Vault read intent wrappers
    (vault_read_intent_kfr / vault_read_intent_funder_intel / vault_read_intent_match_db /
    vault_read_intent_lessons / vault_read_intent_benchmarks).
    """
    canonical_substrate_prefixes = (
        "orgs/<slug>/vault/kfr/",
        "vault_shared/funder_intelligence/",
        "orgs/<slug>/match_database/",
        "pipeline/institutional_memory/lessons.json",
        "vault_shared/benchmarks/",
        "orgs/<slug>/vault/grants/",
    )
    violations: list[tuple[Path, int, str]] = []
    for path, tree in _walk_seat_ast():
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            call_name: str | None = None
            if isinstance(node.func, ast.Attribute):
                call_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                call_name = node.func.id
            if call_name in ("open", "read_text", "read_bytes"):
                # Only flag when the literal path argument matches a canonical substrate prefix
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        for prefix in canonical_substrate_prefixes:
                            if arg.value.startswith(prefix.replace("<slug>", "")) or "vault/kfr" in arg.value or "match_database" in arg.value or "funder_intelligence" in arg.value or "lessons.json" in arg.value or "benchmarks/register" in arg.value:
                                violations.append((path, node.lineno, f"{call_name}({arg.value!r})"))
    assert not violations, (
        f"RT-11 closure violations (raw open against canonical substrate): {violations}"
    )


def test_archivist_yaml_safe_load_only() -> None:
    """Per §15.5 + RT-09 closure — only yaml.safe_load permitted; yaml.load forbidden.

    Scans for `yaml.load(...)` calls; assert ZERO matches in Archivist seat code.
    """
    violations: list[tuple[Path, int]] = []
    for path, tree in _walk_seat_ast():
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "load":
                    # Check if it's yaml.load (not safe_load)
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "yaml":
                        violations.append((path, node.lineno))
    assert not violations, (
        f"RT-09 closure violations (yaml.load — must use yaml.safe_load): {violations}"
    )


# ---------------------------------------------------------------------------
# Module-level sanity check
# ---------------------------------------------------------------------------


def test_archivist_seat_module_imports_cleanly() -> None:
    """Sanity check: the Archivist seat module imports without raising at v0.2 LOCK."""
    import pipeline.orchestrator.seats.archivist as archivist_module
    assert hasattr(archivist_module, "list_registered_cadences")
    assert hasattr(archivist_module, "f_archivist_cross_org_leak")
    assert hasattr(archivist_module, "f_archivist_read_without_vault_intent")  # NEW per RT-11
