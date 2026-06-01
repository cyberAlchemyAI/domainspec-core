"""Tests for pipeline.linting.ast_lint — cross-section AST-lint harness.

Blueprint anchors:
  - pipeline/blueprint/v0.1/section_04_logician.md §3.1 (line 414),
    §7.4, §7.6, §10 ARCH-04 (line 1620)
  - pipeline/blueprint/v0.1/section_03_scout.md §7.16 (AST-NO-SETATTR-
    OPERATOR-DECISION + AST-NO-EVAL-IN-SCOUT simple pair)

Covers five rules:
  R1 LOGICIAN_IMPORT_BAN              — provider-SDK imports banned under pipeline/logician/**
  R2 LOOP_LOGICIAN_BAN                — pipeline.logician internal-module imports banned under pipeline/loop/**
  R3 LOGICIAN_OPEN_BAN                — open('orgs/...' | 'vault_shared/...') banned under pipeline/logician/**
  R4 SCOUT_NO_SETATTR_OPERATOR_DECISION — operator_decision attribute-stores banned outside review_stage.py
  R5 SCOUT_NO_EVAL                    — eval/exec/compile banned under pipeline/scout/**

Test surface matches the spec card at
pipeline/engineering/spec_cards/arch04_logician_ast_lint.md v2.
"""

from __future__ import annotations

import os
from pathlib import Path
from textwrap import dedent

import pytest

from pipeline.linting.ast_lint import (
    AST_NO_INDIRECT_VAULT_READ,
    AST_PREFLIGHT_DOMINATES_FD_REQUEST,
    AliasWalkerNonTerminationError,
    DEFAULT_RULES,
    LOGICIAN_IMPORT_BAN,
    LOGICIAN_OPEN_BAN,
    LOOP_LOGICIAN_BAN,
    SCOUT_NO_EVAL,
    SCOUT_NO_SETATTR_OPERATOR_DECISION,
    Rule,
    Violation,
    lint_tree,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_ROOT = REPO_ROOT / "tests" / "corpus" / "ast_lint" / "v1"


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _write(path: Path, source: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(source).lstrip("\n"), encoding="utf-8")
    return path


def _reason_tags(vs: list[Violation]) -> list[str]:
    return sorted(v.reason_tag for v in vs)


# ---------------------------------------------------------------------------
# Dataclass contract (public API floor)
# ---------------------------------------------------------------------------


def test_rule_and_violation_are_frozen_kw_only_dataclasses():
    import dataclasses
    import inspect

    for cls in (Rule, Violation):
        assert dataclasses.is_dataclass(cls)
        params = cls.__dataclass_params__
        assert params.frozen is True
        # _DataclassParams.kw_only is not present on every supported
        # interpreter. Inspect the generated __init__ instead: every field
        # parameter after self must be keyword-only.
        init_params = inspect.signature(cls.__init__).parameters
        non_self = [p for name, p in init_params.items() if name != "self"]
        assert non_self, f"{cls.__name__}.__init__ has no fields"
        for param in non_self:
            assert param.kind == inspect.Parameter.KEYWORD_ONLY, (
                f"{cls.__name__}.__init__ param {param.name} "
                f"kind={param.kind}; expected KEYWORD_ONLY"
            )


def test_default_rules_list_is_the_eight_published_constants():
    # R1-R7 + R-UPLOADER-NO-SUBMIT (added in §4 v2.7 amendment) + WS-L
    # Slice 4 corrective rules (R-CURRENCY-NO-FLOAT-COMPARE × 2,
    # R-BENCHMARK-NO-SHORT-CIRCUIT-COMPARE,
    # R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV × 2) per architecture
    # v7.0.4-M1 §5.2.1 / §6.2.3 / §8.4 + §4 v2.x.1 corrective rule
    # R-ARCHIVIST-NO-CANONICAL-MUTATE (Tilth-RT-07 PARTIAL closure
    # 2026-05-10).
    from pipeline.linting.ast_lint import UPLOADER_NO_SUBMIT
    from pipeline.linting.r_archivist_no_canonical_mutate import (
        ARCHIVIST_NO_CANONICAL_MUTATE,
    )
    from pipeline.linting.r_benchmark_no_short_circuit_compare import (
        BENCHMARK_NO_SHORT_CIRCUIT_COMPARE,
    )
    from pipeline.linting.r_currency_no_float_compare import (
        CURRENCY_GATE_NO_FLOAT_COMPARE,
        CURRENCY_NO_FLOAT_COMPARE,
    )
    from pipeline.linting.r_intake_no_logfire_import_before_env import (
        INTAKE_NO_LOGFIRE_IMPORT_BEFORE_ENV,
        INTAKE_SEAT_NO_LOGFIRE_IMPORT_BEFORE_ENV,
    )
    from pipeline.linting.r_wpfa_no_autosign import WPFA_NO_AUTOSIGN
    from pipeline.linting.r_wpfa_decimal_mandate_energy import (
        WPFA_DECIMAL_MANDATE_ENERGY,
        WPFA_DECIMAL_MANDATE_ENERGY_GATES,
        WPFA_DECIMAL_MANDATE_ENERGY_VAULT,
    )
    from pipeline.linting.r_datacollector_slice_3 import ALL_RULES as DC_SLICE_3_RULES
    from pipeline.linting.r_report_no_auto_finalize import REPORT_NO_AUTO_FINALIZE
    from pipeline.linting.r_report_vault_intent_required import (
        REPORT_VAULT_INTENT_REQUIRED,
    )
    from pipeline.linting.r_report_decimal_mandate import REPORT_DECIMAL_MANDATE
    from pipeline.linting.r_v0_10_no_slot_token_emission import (
        V0_10_NO_SLOT_TOKEN_EMISSION,
        V0_10_NO_SLOT_TOKEN_EMISSION_SEATS,
    )
    from pipeline.linting.r_class_posture_field_coverage import (
        CLASS_POSTURE_FIELD_COVERAGE,
    )
    from pipeline.linting.r_no_direct_provider_http import (
        NO_DIRECT_PROVIDER_HTTP,
    )
    from pipeline.linting.r_no_political_axis_literal import (
        NO_POLITICAL_AXIS_LITERAL_CARDS,
        NO_POLITICAL_AXIS_LITERAL_LOGICIAN,
        NO_POLITICAL_AXIS_LITERAL_TYPES,
    )

    assert DEFAULT_RULES == [
        LOGICIAN_IMPORT_BAN,
        LOOP_LOGICIAN_BAN,
        LOGICIAN_OPEN_BAN,
        SCOUT_NO_SETATTR_OPERATOR_DECISION,
        SCOUT_NO_EVAL,
        AST_NO_INDIRECT_VAULT_READ,
        AST_PREFLIGHT_DOMINATES_FD_REQUEST,
        UPLOADER_NO_SUBMIT,
        # WS-L Slice 4 (M1 corrective)
        CURRENCY_NO_FLOAT_COMPARE,
        CURRENCY_GATE_NO_FLOAT_COMPARE,
        BENCHMARK_NO_SHORT_CIRCUIT_COMPARE,
        INTAKE_NO_LOGFIRE_IMPORT_BEFORE_ENV,
        INTAKE_SEAT_NO_LOGFIRE_IMPORT_BEFORE_ENV,
        # §4 v2.x.1 corrective (Tilth-RT-07 PARTIAL closure)
        ARCHIVIST_NO_CANONICAL_MUTATE,
        # §17 WPFA v1 LOCK 2026-05-11 — Layer-1 defense + A12 energy extension
        WPFA_NO_AUTOSIGN,
        WPFA_DECIMAL_MANDATE_ENERGY,
        WPFA_DECIMAL_MANDATE_ENERGY_VAULT,
        WPFA_DECIMAL_MANDATE_ENERGY_GATES,
        # §13 Data Collector Slice 3 (WS-I Code phase) — 13 AST-lint rules
        *list(DC_SLICE_3_RULES),
        # WS-J §14 Slice 3 (Report Generator) — 3 AST-lint rules
        REPORT_NO_AUTO_FINALIZE,
        REPORT_VAULT_INTENT_REQUIRED,
        REPORT_DECIMAL_MANDATE,
        # v7.0.10 LOCKED 2026-05-11 paired-commit — 3 AST-lint rules
        # (R-V0-10-NO-SLOT-TOKEN-EMISSION × 2 globs + R-CLASS-POSTURE-FIELD-COVERAGE)
        V0_10_NO_SLOT_TOKEN_EMISSION,
        V0_10_NO_SLOT_TOKEN_EMISSION_SEATS,
        CLASS_POSTURE_FIELD_COVERAGE,
        # CC-003 quarantine — direct provider HTTP + deprecated import ban
        NO_DIRECT_PROVIDER_HTTP,
        # §4 v2.x apolitical_dialect LOCKED 2026-05-16 — 3 AST-lint rule
        # instances (one per target glob: cards / types / logician-gates).
        # Companion runtime gate: F-DIALECT-POLITICAL-AXIS-LEAK.
        NO_POLITICAL_AXIS_LITERAL_CARDS,
        NO_POLITICAL_AXIS_LITERAL_TYPES,
        NO_POLITICAL_AXIS_LITERAL_LOGICIAN,
    ]


def test_rule_constants_name_and_reason_tag_surface():
    assert LOGICIAN_IMPORT_BAN.reason_tag == "logician_imports_llm_client"
    assert LOOP_LOGICIAN_BAN.reason_tag == "loop_imports_logician_internal"
    assert LOGICIAN_OPEN_BAN.reason_tag == "logician_opens_vault_path"
    assert (
        SCOUT_NO_SETATTR_OPERATOR_DECISION.reason_tag
        == "scout_setattr_operator_decision_outside_review_stage"
    )
    assert SCOUT_NO_EVAL.reason_tag == "scout_dynamic_code_execution"
    # R6 / R7 rule-level reason_tag is the rule slug; per-violation tags
    # carry the specific bypass-class string.
    assert AST_NO_INDIRECT_VAULT_READ.reason_tag == "ast_no_indirect_vault_read"
    assert (
        AST_PREFLIGHT_DOMINATES_FD_REQUEST.reason_tag
        == "ast_preflight_dominates_fd_request"
    )


# ---------------------------------------------------------------------------
# Live-tree property tests (tree is currently clean — regression guard)
# ---------------------------------------------------------------------------


def test_logician_tree_has_zero_violations():
    vs = lint_tree(REPO_ROOT / "pipeline" / "logician", DEFAULT_RULES)
    assert vs == [], f"Logician tree drifted: {vs}"


def test_scout_tree_has_zero_violations():
    scout_rules = [SCOUT_NO_SETATTR_OPERATOR_DECISION, SCOUT_NO_EVAL]
    vs = lint_tree(REPO_ROOT / "pipeline" / "scout", scout_rules)
    assert vs == [], f"Scout tree drifted: {vs}"


def test_loop_tree_has_zero_violations_or_is_absent():
    loop_root = REPO_ROOT / "pipeline" / "loop"
    if not loop_root.is_dir():
        pytest.skip("pipeline/loop/ not yet created (§5 orchestrator pending)")
    vs = lint_tree(loop_root, [LOOP_LOGICIAN_BAN])
    assert vs == [], f"Loop tree drifted: {vs}"


def test_full_tree_passes_default_rules():
    vs = lint_tree(REPO_ROOT / "pipeline", DEFAULT_RULES)
    assert vs == [], f"Monorepo regression: {vs}"


# ---------------------------------------------------------------------------
# R1 LOGICIAN_IMPORT_BAN — failure-code tests
# ---------------------------------------------------------------------------


def test_r1_detects_anthropic_import(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        """
        import anthropic
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert [v.reason_tag for v in vs] == ["logician_imports_llm_client"]
    assert vs[0].rule_name == "LOGICIAN_IMPORT_BAN"


def test_r1_detects_submodule_import(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        """
        from openai.types import Completion
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert len(vs) == 1
    assert vs[0].reason_tag == "logician_imports_llm_client"


@pytest.mark.parametrize(
    "module_name",
    ["anthropic", "openai", "groq", "google.generativeai", "ollama"],
)
def test_r1_catches_all_five_providers(tmp_path, module_name):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        f"import {module_name}\n",
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert len(vs) == 1
    assert vs[0].reason_tag == "logician_imports_llm_client"


def test_r1_admits_stdlib_import(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "ok.py",
        """
        import json
        from pathlib import Path
        from pipeline.sovereignty.audit import verify_ledger
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert vs == []


def test_r1_does_not_fire_outside_logician(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "elsewhere.py",
        "import anthropic\n",
    )
    vs = lint_tree(tmp_path / "pipeline", [LOGICIAN_IMPORT_BAN])
    assert vs == []


# ---------------------------------------------------------------------------
# R2 LOOP_LOGICIAN_BAN — failure-code tests
# ---------------------------------------------------------------------------


def test_r2_rejects_internal_module_import_from_loop(tmp_path):
    _write(
        tmp_path / "pipeline" / "loop" / "runner.py",
        """
        from pipeline.logician.cedar_eval import evaluate
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "loop", [LOOP_LOGICIAN_BAN])
    assert [v.reason_tag for v in vs] == ["loop_imports_logician_internal"]


def test_r2_admits_public_api_import_from_loop(tmp_path):
    _write(
        tmp_path / "pipeline" / "loop" / "runner.py",
        """
        from pipeline.logician import LogicianGateRunner
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "loop", [LOOP_LOGICIAN_BAN])
    assert vs == []


def test_r2_does_not_fire_outside_loop(tmp_path):
    # Logician itself is allowed to import its own submodules internally.
    _write(
        tmp_path / "pipeline" / "logician" / "internal.py",
        "from pipeline.logician.cedar_eval import evaluate\n",
    )
    vs = lint_tree(tmp_path / "pipeline", [LOOP_LOGICIAN_BAN])
    assert vs == []


# ---------------------------------------------------------------------------
# R3 LOGICIAN_OPEN_BAN — failure-code tests
# ---------------------------------------------------------------------------


def test_r3_rejects_open_on_orgs_path(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        """
        def f():
            return open("orgs/fit_farms/vault/x.json", "r")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_OPEN_BAN])
    assert [v.reason_tag for v in vs] == ["logician_opens_vault_path"]


def test_r3_rejects_open_on_vault_shared_path(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        """
        def f():
            return open("vault_shared/trust_root.v1.json", "rb")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_OPEN_BAN])
    assert [v.reason_tag for v in vs] == ["logician_opens_vault_path"]


def test_r3_admits_non_literal_open(tmp_path):
    """Dynamic first-arg is out of scope for v0.1 static analysis."""
    _write(
        tmp_path / "pipeline" / "logician" / "ok.py",
        """
        def f(path):
            return open(path, "r")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_OPEN_BAN])
    assert vs == []


def test_r3_admits_open_on_other_paths(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "ok.py",
        """
        def f():
            return open("/tmp/cache.json", "r")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_OPEN_BAN])
    assert vs == []


def test_r3_does_not_fire_outside_logician(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "ok.py",
        """
        def f():
            return open("orgs/fit_farms/vault/x.json", "r")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline", [LOGICIAN_OPEN_BAN])
    assert vs == []


# ---------------------------------------------------------------------------
# R4 SCOUT_NO_SETATTR_OPERATOR_DECISION — failure-code tests
# ---------------------------------------------------------------------------


def test_r4_rejects_setattr_operator_decision_outside_review_stage(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "bad.py",
        """
        def sneaky(item):
            setattr(item, "operator_decision", "ACCEPT")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "scout",
        [SCOUT_NO_SETATTR_OPERATOR_DECISION],
    )
    assert [v.reason_tag for v in vs] == [
        "scout_setattr_operator_decision_outside_review_stage"
    ]


def test_r4_rejects_object_setattr_form(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "bad.py",
        """
        def sneaky(item):
            object.__setattr__(item, "operator_decision", "ACCEPT")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "scout",
        [SCOUT_NO_SETATTR_OPERATOR_DECISION],
    )
    assert [v.reason_tag for v in vs] == [
        "scout_setattr_operator_decision_outside_review_stage"
    ]


def test_r4_rejects_direct_attribute_store(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "bad.py",
        """
        def sneaky(item):
            item.operator_decision = "ACCEPT"
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "scout",
        [SCOUT_NO_SETATTR_OPERATOR_DECISION],
    )
    assert [v.reason_tag for v in vs] == [
        "scout_setattr_operator_decision_outside_review_stage"
    ]


def test_r4_admits_setattr_inside_review_stage_module(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "review_stage.py",
        """
        def record_operator_decision(item, decision):
            setattr(item, "operator_decision", decision)
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "scout",
        [SCOUT_NO_SETATTR_OPERATOR_DECISION],
    )
    assert vs == []


def test_r4_admits_setattr_on_other_attribute(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "ok.py",
        """
        def ok(item):
            setattr(item, "something_else", "value")
            item.other = "x"
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "scout",
        [SCOUT_NO_SETATTR_OPERATOR_DECISION],
    )
    assert vs == []


# ---------------------------------------------------------------------------
# R5 SCOUT_NO_EVAL — failure-code tests
# ---------------------------------------------------------------------------


def test_r5_rejects_eval(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "bad.py",
        "def f(s): return eval(s)\n",
    )
    vs = lint_tree(tmp_path / "pipeline" / "scout", [SCOUT_NO_EVAL])
    assert [v.reason_tag for v in vs] == ["scout_dynamic_code_execution"]


def test_r5_rejects_exec(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "bad.py",
        "def f(s): exec(s)\n",
    )
    vs = lint_tree(tmp_path / "pipeline" / "scout", [SCOUT_NO_EVAL])
    assert [v.reason_tag for v in vs] == ["scout_dynamic_code_execution"]


def test_r5_rejects_compile(tmp_path):
    _write(
        tmp_path / "pipeline" / "scout" / "bad.py",
        "def f(s): return compile(s, '<str>', 'exec')\n",
    )
    vs = lint_tree(tmp_path / "pipeline" / "scout", [SCOUT_NO_EVAL])
    assert [v.reason_tag for v in vs] == ["scout_dynamic_code_execution"]


def test_r5_admits_these_outside_scout(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "ok.py",
        "def f(s): return eval(s)\n",
    )
    vs = lint_tree(tmp_path / "pipeline", [SCOUT_NO_EVAL])
    assert vs == []


# ---------------------------------------------------------------------------
# Adversarial tests (test_adv_*) — documented-scope limitations
# ---------------------------------------------------------------------------


def test_adv_r1_alias_import_still_caught_via_module_name(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        "import anthropic as a\n",
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert len(vs) == 1 and vs[0].reason_tag == "logician_imports_llm_client"


def test_adv_r1_conditional_import_inside_try(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        """
        try:
            import openai
        except ImportError:
            openai = None
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert len(vs) == 1 and vs[0].reason_tag == "logician_imports_llm_client"


def test_adv_r2_dotted_submodule_access_still_caught(tmp_path):
    _write(
        tmp_path / "pipeline" / "loop" / "bad.py",
        """
        from pipeline.logician.cedar_eval import CedarDecision
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "loop", [LOOP_LOGICIAN_BAN])
    assert len(vs) == 1 and vs[0].reason_tag == "loop_imports_logician_internal"


def test_adv_r3_open_via_pathlib_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: Path("orgs/...").open() chain is now caught.

    Flip of the pre-ARCH-05 adv test: R1/R3/R5 still pass this shape
    (R3 only matches `ast.Name(id="open")`), but R6 resolves `Path` to
    `attr:pathlib.Path` and emits `logician_indirect_vault_read_via_alias`.
    """
    _write(
        tmp_path / "pipeline" / "logician" / "bypass.py",
        """
        from pathlib import Path
        def f():
            return Path("orgs/fit_farms/vault/x.json").open("r")
        """,
    )
    vs_r3 = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_OPEN_BAN])
    assert vs_r3 == []  # R3 honestly unchanged
    vs_r6 = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs_r6 != []
    assert any(
        v.reason_tag == "logician_indirect_vault_read_via_alias" for v in vs_r6
    )


def test_adv_r4_dynamic_attribute_name_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: literal-aliased setattr name is now caught."""
    _write(
        tmp_path / "pipeline" / "scout" / "bypass.py",
        """
        def sneaky(item):
            attr_name = "operator_decision"
            setattr(item, attr_name, "ACCEPT")
        """,
    )
    vs_r4 = lint_tree(
        tmp_path / "pipeline" / "scout",
        [SCOUT_NO_SETATTR_OPERATOR_DECISION],
    )
    assert vs_r4 == []  # R4 honestly unchanged
    vs_r6 = lint_tree(
        tmp_path / "pipeline" / "scout", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs_r6 != []
    assert any(
        v.reason_tag == "scout_indirect_operator_decision_write_via_alias"
        for v in vs_r6
    )


def test_adv_r5_getattr_builtins_eval_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: getattr(__builtins__, "eval")(s) is now caught."""
    _write(
        tmp_path / "pipeline" / "scout" / "bypass.py",
        """
        def sneaky(s):
            return getattr(__builtins__, "eval")(s)
        """,
    )
    vs_r5 = lint_tree(tmp_path / "pipeline" / "scout", [SCOUT_NO_EVAL])
    assert vs_r5 == []  # R5 honestly unchanged
    vs_r6 = lint_tree(
        tmp_path / "pipeline" / "scout", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs_r6 != []
    assert any(
        v.reason_tag == "scout_indirect_dynamic_code_via_alias" for v in vs_r6
    )


def test_adv_r2_attribute_access_via_package_import_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: `import pipeline.logician as L; L.cedar_eval.evaluate()` is caught.

    The alias walker resolves `L` → `module:pipeline.logician`, chains
    `L.cedar_eval.evaluate` → `attr:pipeline.logician.cedar_eval.evaluate`,
    and flags the two-segment tail as internal-surface access.
    """
    _write(
        tmp_path / "pipeline" / "loop" / "bypass.py",
        """
        import pipeline.logician as L
        def run():
            return L.cedar_eval.evaluate({})
        """,
    )
    vs_r2 = lint_tree(tmp_path / "pipeline" / "loop", [LOOP_LOGICIAN_BAN])
    assert vs_r2 == []  # R2 honestly unchanged
    vs_r6 = lint_tree(tmp_path / "pipeline" / "loop", [AST_NO_INDIRECT_VAULT_READ])
    assert vs_r6 != []
    assert any(
        v.reason_tag == "loop_indirect_logician_internal_via_alias" for v in vs_r6
    )


def test_adv_r3_open_rebound_to_local_name_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: `o = open; o("orgs/...")` is now caught."""
    _write(
        tmp_path / "pipeline" / "logician" / "bypass.py",
        """
        o = open
        def f():
            return o("orgs/fit_farms/vault/secret.json", "rb")
        """,
    )
    vs_r3 = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_OPEN_BAN])
    assert vs_r3 == []  # R3 honestly unchanged
    vs_r6 = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs_r6 != []
    assert any(
        v.reason_tag == "logician_indirect_vault_read_via_alias" for v in vs_r6
    )


def test_adv_r5_eval_rebound_to_local_name_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: `e = eval; e("1+1")` is now caught."""
    _write(
        tmp_path / "pipeline" / "scout" / "bypass.py",
        """
        e = eval
        def f(s):
            return e(s)
        """,
    )
    vs_r5 = lint_tree(tmp_path / "pipeline" / "scout", [SCOUT_NO_EVAL])
    assert vs_r5 == []  # R5 honestly unchanged
    vs_r6 = lint_tree(
        tmp_path / "pipeline" / "scout", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs_r6 != []
    assert any(
        v.reason_tag == "scout_indirect_dynamic_code_via_alias" for v in vs_r6
    )


def test_adv_r1_dynamic_import_via_importlib_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: `importlib.import_module("anthropic")` is now caught."""
    _write(
        tmp_path / "pipeline" / "logician" / "bypass.py",
        """
        import importlib
        def load():
            return importlib.import_module("anthropic")
        """,
    )
    vs_r1 = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert vs_r1 == []  # R1 honestly unchanged
    vs_r6 = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs_r6 != []
    assert any(
        v.reason_tag == "logician_indirect_llm_client_via_alias" for v in vs_r6
    )


def test_adv_r3_builtins_open_attribute_form_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: `builtins.open("orgs/...")` is now caught."""
    _write(
        tmp_path / "pipeline" / "logician" / "bypass.py",
        """
        import builtins
        def f():
            return builtins.open("orgs/fit_farms/vault/secret.json", "rb")
        """,
    )
    vs_r3 = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_OPEN_BAN])
    assert vs_r3 == []  # R3 honestly unchanged
    vs_r6 = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs_r6 != []
    assert any(
        v.reason_tag == "logician_indirect_vault_read_via_alias" for v in vs_r6
    )


def test_adv_r5_builtins_eval_attribute_form_now_caught_by_r6(tmp_path):
    """ARCH-05 R6 closure: `builtins.eval(...)` attribute form is now caught."""
    _write(
        tmp_path / "pipeline" / "scout" / "bypass.py",
        """
        import builtins
        def f(s):
            return builtins.eval(s)
        """,
    )
    vs_r5 = lint_tree(tmp_path / "pipeline" / "scout", [SCOUT_NO_EVAL])
    assert vs_r5 == []  # R5 honestly unchanged
    vs_r6 = lint_tree(
        tmp_path / "pipeline" / "scout", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs_r6 != []
    assert any(
        v.reason_tag == "scout_indirect_dynamic_code_via_alias" for v in vs_r6
    )


# ---------------------------------------------------------------------------
# R6 AST_NO_INDIRECT_VAULT_READ — targeted green + admit + termination tests
# (the bypass-catch cases for R6 live with the flipped test_adv_* above).
# ---------------------------------------------------------------------------


def test_r6_admits_open_of_non_vault_path(tmp_path):
    """R6 only fires when the literal path prefix matches vault surfaces."""
    _write(
        tmp_path / "pipeline" / "logician" / "ok.py",
        """
        from pathlib import Path
        def f():
            return Path("/tmp/diagnostic.json").open("r")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs == []


def test_r6_admits_legit_setattr_non_operator_decision(tmp_path):
    """R6's setattr branch only fires when the aliased name is
    ``literal:operator_decision``; other attributes pass."""
    _write(
        tmp_path / "pipeline" / "scout" / "ok.py",
        """
        def harmless(item):
            attr_name = "display_title"
            setattr(item, attr_name, "hello")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "scout", [AST_NO_INDIRECT_VAULT_READ])
    assert vs == []


def test_r6_admits_pipeline_logician_public_surface(tmp_path):
    """``L.evaluate(...)`` (single-segment tail) is the public API and
    must not fire — only two-or-more-segment tails are internal access."""
    _write(
        tmp_path / "pipeline" / "loop" / "ok.py",
        """
        import pipeline.logician as L
        def run():
            return L.evaluate({})
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "loop", [AST_NO_INDIRECT_VAULT_READ])
    assert vs == []


def test_r6_review_stage_may_setattr_operator_decision(tmp_path):
    """The blueprint carve-out: ``pipeline/scout/review_stage.py`` is the
    only file allowed to write ``operator_decision`` via setattr — so R6's
    setattr branch must admit it even under aliased-name form."""
    _write(
        tmp_path / "pipeline" / "scout" / "review_stage.py",
        """
        def accept(item):
            attr_name = "operator_decision"
            setattr(item, attr_name, "ACCEPT")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "scout", [AST_NO_INDIRECT_VAULT_READ])
    assert vs == []


def test_r6_termination_guard_decidability_cap(tmp_path, monkeypatch):
    """B-v5-02 termination guard: a synthetic module that would
    otherwise exceed the cap is rejected with a single
    ``ast_alias_walker_overflow`` violation rather than looping."""
    import pipeline.linting.ast_lint as mod

    # Cap low so we can force the overflow path deterministically.
    monkeypatch.setattr(mod, "_MAX_ALIAS_WALKER_STEPS", 1)
    _write(
        tmp_path / "pipeline" / "logician" / "heavy.py",
        # Many assigns with resolvable rhs exercise the fixed-point loop.
        "\n".join(
            ["from pathlib import Path"]
            + [f"x{i} = Path" for i in range(20)]
            + ["def f():", "    return Path('x.json').open('r')"]
        )
        + "\n",
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert any(v.reason_tag == "ast_alias_walker_overflow" for v in vs)


def test_r6_admits_when_section_is_outside_target_surfaces(tmp_path):
    """R6 only targets logician/, scout/, loop/ under pipeline/."""
    _write(
        tmp_path / "pipeline" / "sovereignty" / "anywhere.py",
        """
        import importlib
        def load():
            return importlib.import_module("anthropic")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "sovereignty",
        [AST_NO_INDIRECT_VAULT_READ],
    )
    assert vs == []


# ---------------------------------------------------------------------------
# R7 AST_PREFLIGHT_DOMINATES_FD_REQUEST — failure-code + admit tests
# ---------------------------------------------------------------------------


def test_r7_catches_missing_preflight(tmp_path):
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        def run():
            return fd_broker.request("https", host="api.example.com")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []
    assert any(
        v.reason_tag == "loop_fd_request_not_preflight_dominated" for v in vs
    )


def test_r7_admits_preflight_dominator(tmp_path):
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        PREFLIGHT_OK: Final[bool] = True
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="api.example.com")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs == []


def test_r7_short_circuit_and_admits(tmp_path):
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        PREFLIGHT_OK: Final[bool] = True
        def run(ready):
            if PREFLIGHT_OK and ready:
                return fd_broker.request("https", host="api.example.com")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs == []


def test_r7_catches_or_fallback(tmp_path):
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        PREFLIGHT_OK: Final[bool] = True
        def run(emergency):
            if PREFLIGHT_OK or emergency:
                return fd_broker.request("https", host="api.example.com")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []
    assert any(
        v.reason_tag == "fd_request_preflight_short_circuit_or_bypass" for v in vs
    )


def test_r7_catches_non_literal_sentinel_initializer(tmp_path):
    """B-v5-01: a ``Final[bool]`` with a *non-literal* initializer does
    not qualify as a preflight sentinel — the guard is rejected and the
    fd_broker.request downstream is flagged."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        import os
        PREFLIGHT_OK: Final[bool] = bool(os.environ.get("READY"))
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="api.example.com")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []
    assert any(
        v.reason_tag == "fd_request_preflight_sentinel_non_literal" for v in vs
    )


def test_r7_cross_module_sentinel_resolution(tmp_path):
    """B-v5-03: sentinel imported from a sibling module is resolved
    statically against the on-disk source tree."""
    _write(
        tmp_path / "pipeline" / "loop" / "preflight.py",
        """
        from typing import Final
        PREFLIGHT_OK: Final[bool] = True
        """,
    )
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        from pipeline.loop.preflight import PREFLIGHT_OK
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="api.example.com")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs == []


def test_r7_only_fires_on_loop_and_channel_f_under_scout(tmp_path):
    """A-v4-02 scope narrowing: Channel A/B/C/D/E scout paths have their
    own nonce-reserve-release discipline. Only ``channel_f_*.py`` under
    scout is in R7 scope, per blueprint §7.16."""
    _write(
        tmp_path / "pipeline" / "scout" / "channel_a_federal_apis.py",
        """
        import fd_broker
        def run(host):
            return fd_broker.request("https", host=host)
        """,
    )
    _write(
        tmp_path / "pipeline" / "scout" / "channel_f_websearch.py",
        """
        import fd_broker
        def run(host):
            return fd_broker.request("https", host=host)
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "scout", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    files = [v.file.name for v in vs]
    assert "channel_a_federal_apis.py" not in files
    assert "channel_f_websearch.py" in files


def test_r7_admits_non_fd_request_call(tmp_path):
    """A bare ``fd_broker.other_method(...)`` is not the sink R7 targets."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        def run():
            return fd_broker.close()
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs == []


def test_r7_typing_final_bool_attribute_form_accepted(tmp_path):
    """``typing.Final[bool]`` attribute-form annotation is accepted as a
    valid sentinel annotation (structural equivalence)."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import typing
        import fd_broker
        PREFLIGHT_OK: typing.Final[bool] = True
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs == []


def test_r7_final_non_bool_is_not_a_sentinel(tmp_path):
    """``Final[int]`` does not qualify — must be ``Final[bool]``."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        LIMIT: Final[int] = 1
        def run():
            if LIMIT:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_classify_test_nonsentinel_name_and_bare_other_bool_ops(tmp_path):
    """A guard test that is a non-sentinel Name, or an And/Or with no
    sentinel leaves, does not count as a dominator — the sink fires."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        def run(ready, emergency):
            if ready:
                return fd_broker.request("https", host="a")
            if ready and emergency:
                return fd_broker.request("https", host="b")
            if ready or emergency:
                return fd_broker.request("https", host="c")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert len(vs) == 3
    assert all(
        v.reason_tag == "loop_fd_request_not_preflight_dominated" for v in vs
    )


def test_r7_outside_pipeline_is_out_of_scope(tmp_path):
    """R7 target_section returns None outside pipeline/."""
    _write(
        tmp_path / "other_root" / "caller.py",
        """
        import fd_broker
        def run():
            return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(tmp_path, [AST_PREFLIGHT_DOMINATES_FD_REQUEST])
    assert vs == []


def test_r7_cross_module_import_from_unbounded_surface_unresolved(tmp_path):
    """An `if X:` guard where X is imported from outside the bounded
    resolve surface (Scout/Section-2/loop/logician) is a candidate name
    but resolves to None → specific "not preflight dominated" message."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        from some_external_pkg import PREFLIGHT_OK
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []
    assert any(
        v.reason_tag == "loop_fd_request_not_preflight_dominated" for v in vs
    )
    # The message mentions the bounded-surface resolution failure.
    assert any("bounded module surface" in v.message for v in vs)


def test_r7_imported_sentinel_from_surface_but_missing_file(tmp_path):
    """Import matches a bounded surface but the target file doesn't exist
    in the on-disk tree — resolution fails → not-dominated."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        from pipeline.scout.not_there import PREFLIGHT_OK
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_imported_sentinel_name_missing_in_origin(tmp_path):
    """Origin file is resolvable on disk but does not declare the
    requested name as a sentinel."""
    _write(
        tmp_path / "pipeline" / "loop" / "preflight.py",
        # Has an int Final, not a bool; the name does not resolve as sentinel.
        """
        from typing import Final
        LIMIT: Final[int] = 3
        """,
    )
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        from pipeline.loop.preflight import LIMIT
        def run():
            if LIMIT:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_deep_descendant_of_if_body_still_dominated(tmp_path):
    """The sink buried inside a ``with``/``try`` under the ``if`` body
    still resolves as dominated via ``_is_descendant_of_list``."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        PREFLIGHT_OK: Final[bool] = True
        def run():
            if PREFLIGHT_OK:
                try:
                    return fd_broker.request("https", host="x")
                except Exception:
                    return None
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs == []


def test_r7_sink_in_else_branch_is_not_dominated(tmp_path):
    """A sink reached only via ``else:`` is NOT dominated by the ``if``
    test — the dominator check must reject it."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        PREFLIGHT_OK: Final[bool] = True
        def run():
            if PREFLIGHT_OK:
                return None
            else:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r6_getattr_with_non_constant_name_returns_none(tmp_path):
    """R6 only resolves ``getattr(obj, "literal")`` — dynamic name args
    leave the resolve chain unresolved (coverage for line 606)."""
    _write(
        tmp_path / "pipeline" / "logician" / "ok.py",
        """
        def f(name, obj):
            return getattr(obj, name)()
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs == []


def test_r6_getattr_on_module_alias_resolves_through_attr(tmp_path):
    """`getattr(pathlib, "Path")` via getattr yields ``attr:pathlib.Path``;
    calling ``.open(...)`` on that is caught."""
    _write(
        tmp_path / "pipeline" / "logician" / "bypass.py",
        """
        import pathlib
        def f():
            P = getattr(pathlib, "Path")
            return P("orgs/fit_farms/vault/x.json").open("r")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs != []


def test_r7_annotation_is_none_not_a_sentinel(tmp_path):
    """A bare Assign (no annotation) is not a sentinel (covers line 853)."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        PREFLIGHT_OK = True  # no annotation → not a Final[bool]
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_sentinel_init_with_attribute_rejected(tmp_path):
    """A Final[bool] whose init sub-tree contains an Attribute is non-literal."""
    _write(
        tmp_path / "pipeline" / "loop" / "flags.py",
        """
        from typing import Final
        ENABLED: Final[bool] = True
        """,
    )
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        import flags
        # Attribute-containing init → non-literal per B-v5-01.
        PREFLIGHT_OK: Final[bool] = flags.ENABLED
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []
    assert any(
        v.reason_tag == "fd_request_preflight_sentinel_non_literal" for v in vs
    )


def test_r7_sentinel_init_with_non_bool_name_rejected(tmp_path):
    """Init tree with a Name that is not True/False → non-literal."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        OTHER = True
        PREFLIGHT_OK: Final[bool] = OTHER
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_sentinel_init_with_non_bool_constant_rejected(tmp_path):
    """Init tree with a non-bool Constant → non-literal."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        # truthy int constant, not bool — B-v5-01 rejects.
        PREFLIGHT_OK: Final[bool] = 1
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_sentinel_annassign_with_no_value_is_skipped(tmp_path):
    """``X: Final[bool]`` without an initializer is silently skipped as a
    sentinel candidate (covers line 899)."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        from typing import Final
        import fd_broker
        PREFLIGHT_OK: Final[bool]  # declared but not initialized
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_find_tree_root_missing_pipeline_ancestor(tmp_path, monkeypatch):
    """When there is no `pipeline/` ancestor on disk, cross-module
    resolution fails gracefully (covers line 917 + 953)."""
    # Place the source under a path lacking any `pipeline/` directory.
    src_dir = tmp_path / "workspace_root"
    _write(
        src_dir / "caller.py",
        """
        import fd_broker
        from pipeline.loop.preflight import PREFLIGHT_OK  # unresolvable on disk
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    # _r7_target_section keys on "pipeline" in parts — we need at least a
    # pipeline/loop/ path for R7 to even inspect. Plant a sibling that DOES
    # exist so the section matches, but the ImportFrom target does not.
    _write(
        tmp_path / "pipeline" / "loop" / "outer.py",
        """
        import fd_broker
        from pipeline.loop.preflight_missing import PREFLIGHT_OK
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST])
    # The imported-from-missing-file case emits a not-dominated violation.
    assert vs != []


def test_r7_cross_module_origin_syntax_error_fails_closed(tmp_path):
    """If the origin file parses with a SyntaxError, resolution returns
    None fail-closed (covers lines 962-963)."""
    _write(
        tmp_path / "pipeline" / "loop" / "preflight.py",
        "def broken(:\n",  # deliberately invalid
    )
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        from pipeline.loop.preflight import PREFLIGHT_OK
        def run():
            if PREFLIGHT_OK:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_nested_fd_broker_attribute_form(tmp_path):
    """``pkg.fd_broker.request(...)`` attribute-chain form is also a sink
    (covers lines 1007-1009)."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import pkg
        def run():
            return pkg.fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r7_classify_test_unrelated_construct_is_not_dominator(tmp_path):
    """A Compare / Call / arithmetic in the `if` test yields no sentinel
    match (covers line 1074 — the classify_test final fall-through)."""
    _write(
        tmp_path / "pipeline" / "loop" / "caller.py",
        """
        import fd_broker
        def run(n):
            if n > 0:
                return fd_broker.request("https", host="x")
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "loop", [AST_PREFLIGHT_DOMINATES_FD_REQUEST]
    )
    assert vs != []


def test_r6_getattr_on_attr_module_resolves_chain(tmp_path):
    """`getattr(M.sub, "evaluate")` where M is `pipeline.logician` yields
    an attr chain two segments deep → R6 loop surface catches it
    (covers lines 619, 622-623)."""
    _write(
        tmp_path / "pipeline" / "loop" / "bypass.py",
        """
        import pipeline.logician as L
        def run():
            fn = getattr(L.cedar_eval, "evaluate")
            return fn({})
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "loop", [AST_NO_INDIRECT_VAULT_READ])
    # The getattr wiring resolves the inner attribute; the
    # indirect logician internal call is flagged.
    assert vs != []
    assert any(
        v.reason_tag == "loop_indirect_logician_internal_via_alias"
        for v in vs
    )


def test_r6_first_str_arg_bare_call_with_no_args_is_noop(tmp_path):
    """`open()` with no args can't leak a literal vault path — R6 is a noop.
    Covers the early return in _r6_first_str_arg."""
    _write(
        tmp_path / "pipeline" / "logician" / "ok.py",
        """
        o = open
        def f():
            return o()
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs == []


def test_r6_from_relative_import_with_no_module(tmp_path):
    """``from . import X`` has ``node.module=None`` — covers line 532.
    Even so, the local name ``X`` receives an ``attr:X`` binding and
    does not false-positive as a vault leak."""
    _write(
        tmp_path / "pipeline" / "logician" / "__init__.py",
        "",
    )
    _write(
        tmp_path / "pipeline" / "logician" / "ok.py",
        """
        from . import ok as other
        def f():
            return other
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "logician", [AST_NO_INDIRECT_VAULT_READ]
    )
    assert vs == []


# ---------------------------------------------------------------------------
# Multi-file / multi-rule behaviour
# ---------------------------------------------------------------------------


def test_lint_tree_aggregates_violations_across_files(tmp_path):
    _write(tmp_path / "pipeline" / "logician" / "a.py", "import anthropic\n")
    _write(tmp_path / "pipeline" / "logician" / "b.py", "import openai\n")
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert len(vs) == 2
    files = sorted(v.file.name for v in vs)
    assert files == ["a.py", "b.py"]


def test_lint_tree_aggregates_across_rules(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        """
        import anthropic
        def f():
            return open("orgs/x/vault/y.json", "r")
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", DEFAULT_RULES)
    tags = _reason_tags(vs)
    assert "logician_imports_llm_client" in tags
    assert "logician_opens_vault_path" in tags


def test_lint_tree_skips_unreadable_files(tmp_path, monkeypatch):
    """Syntax-error or encoding-failed files are skipped, not crash."""
    _write(tmp_path / "pipeline" / "logician" / "broken.py", "def f( ::: syntax error\n")
    # Must not raise:
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert vs == []


def test_violation_line_and_col_populated(tmp_path):
    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        """
        import json
        import anthropic
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_IMPORT_BAN])
    assert len(vs) == 1
    assert vs[0].line == 2
    assert vs[0].col >= 0
    assert vs[0].file.name == "bad.py"


def test_lint_tree_handles_nonexistent_root(tmp_path):
    vs = lint_tree(tmp_path / "does_not_exist", DEFAULT_RULES)
    assert vs == []


def test_r2_rejects_direct_import_of_internal_submodule(tmp_path):
    """`import pipeline.logician.cedar_eval` in a loop file is banned."""
    _write(
        tmp_path / "pipeline" / "loop" / "runner.py",
        "import pipeline.logician.cedar_eval\n",
    )
    vs = lint_tree(tmp_path / "pipeline" / "loop", [LOOP_LOGICIAN_BAN])
    assert len(vs) == 1
    assert vs[0].reason_tag == "loop_imports_logician_internal"


def test_r3_ignores_open_with_no_args(tmp_path):
    """open() with zero args is not a vault-path literal — skip silently."""
    _write(
        tmp_path / "pipeline" / "logician" / "weird.py",
        """
        def f():
            return open()  # type: ignore[call-arg]
        """,
    )
    vs = lint_tree(tmp_path / "pipeline" / "logician", [LOGICIAN_OPEN_BAN])
    assert vs == []


def test_r4_rejects_aug_assign_operator_decision(tmp_path):
    """obj.operator_decision += 1 is still an operator_decision write."""
    _write(
        tmp_path / "pipeline" / "scout" / "bad.py",
        """
        def sneaky(item):
            item.operator_decision += "_APPENDED"
        """,
    )
    vs = lint_tree(
        tmp_path / "pipeline" / "scout",
        [SCOUT_NO_SETATTR_OPERATOR_DECISION],
    )
    assert [v.reason_tag for v in vs] == [
        "scout_setattr_operator_decision_outside_review_stage"
    ]


def test_glob_with_bare_filename_pattern_matches_anywhere(tmp_path):
    """Custom rule with target_glob='*.py' (no dir parts) matches any file."""
    from pipeline.linting.ast_lint import Rule, Violation as _V
    seen: list[_V] = []

    def _always(tree, path):
        yield _V(
            rule_name="DEBUG",
            reason_tag="debug",
            file=path,
            line=1,
            col=0,
            message="x",
        )

    rule = Rule(
        name="DEBUG",
        reason_tag="debug",
        target_glob="*.py",
        check=_always,
    )
    _write(tmp_path / "anywhere" / "file.py", "x = 1\n")
    vs = lint_tree(tmp_path, [rule])
    assert len(vs) == 1
    assert vs[0].file.name == "file.py"


# ---------------------------------------------------------------------------
# Corpus tests — preserved fixtures for regression
# ---------------------------------------------------------------------------


def test_corpus_pass_fixtures_produce_no_violations():
    pass_root = CORPUS_ROOT / "pass"
    if not pass_root.is_dir() or not any(pass_root.rglob("*.py")):
        pytest.skip("pass corpus not present")
    vs = lint_tree(pass_root, DEFAULT_RULES)
    assert vs == [], f"Corpus pass fixture produced violations: {vs}"


def test_corpus_fail_fixtures_produce_expected_violations():
    fail_root = CORPUS_ROOT / "fail"
    if not fail_root.is_dir() or not any(fail_root.rglob("*.py")):
        pytest.skip("fail corpus not present")
    vs = lint_tree(fail_root, DEFAULT_RULES)
    # Every fail fixture must produce at least one violation.
    fixture_files = {p.name for p in fail_root.rglob("*.py")}
    violated_files = {v.file.name for v in vs}
    assert violated_files == fixture_files, (
        f"Every fail fixture must violate; missing: {fixture_files - violated_files}"
    )


# ---------------------------------------------------------------------------
# CLI / main entry (scripts/run_lint.sh backbone)
# ---------------------------------------------------------------------------


def test_main_returns_zero_on_clean_tree(tmp_path):
    from pipeline.linting.ast_lint import main

    _write(tmp_path / "pipeline" / "logician" / "ok.py", "import json\n")
    assert main([str(tmp_path / "pipeline")]) == 0


def test_main_returns_one_on_violation_and_writes_stderr(tmp_path, capsys):
    from pipeline.linting.ast_lint import main

    _write(
        tmp_path / "pipeline" / "logician" / "bad.py",
        "import anthropic\n",
    )
    rc = main([str(tmp_path / "pipeline")])
    assert rc == 1
    err = capsys.readouterr().err
    assert "LOGICIAN_IMPORT_BAN" in err
    assert "logician_imports_llm_client" in err


def test_main_default_root_is_pipeline(tmp_path, monkeypatch):
    """With no arg, main() lints the live pipeline/ tree."""
    from pipeline.linting.ast_lint import main

    monkeypatch.chdir(REPO_ROOT)
    assert main([]) == 0


# ---------------------------------------------------------------------------
# Public-API surface stability
# ---------------------------------------------------------------------------


def test_public_api_exports_complete():
    import pipeline.linting.ast_lint as mod

    assert set(mod.__all__) == {
        "BLUEPRINT_DEPS",
        "Rule",
        "Violation",
        "AliasWalkerNonTerminationError",
        "lint_tree",
        "LOGICIAN_IMPORT_BAN",
        "LOOP_LOGICIAN_BAN",
        "LOGICIAN_OPEN_BAN",
        "SCOUT_NO_SETATTR_OPERATOR_DECISION",
        "SCOUT_NO_EVAL",
        "AST_NO_INDIRECT_VAULT_READ",
        "AST_PREFLIGHT_DOMINATES_FD_REQUEST",
        "UPLOADER_NO_SUBMIT",
        "UPLOADER_ALLOW_LIST",
        "DEFAULT_RULES",
    }


def test_blueprint_deps_populated():
    import pipeline.linting.ast_lint as mod

    assert "section_04_logician.md" in mod.BLUEPRINT_DEPS
    assert "section_03_scout.md" in mod.BLUEPRINT_DEPS
    for entry in mod.BLUEPRINT_DEPS.values():
        assert "sections_implemented" in entry
        assert "hash_at_lock" in entry
        assert "hash_source_version" in entry
        # §4.6 discipline: hash_at_lock is a 16-char sha3_512 hex prefix.
        h = entry["hash_at_lock"]
        assert isinstance(h, str)
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)


def test_blueprint_deps_hashes_match_live_blueprints():
    """Drift guard — if a blueprint file is edited without bumping the pin, fail.

    Reads the two live blueprint files and recomputes sha3_512[:16]. When the
    blueprint is intentionally revised, this test fails loudly and the author
    must update BLUEPRINT_DEPS as part of the same commit.
    """
    import hashlib
    from pathlib import Path

    import pipeline.linting.ast_lint as mod

    repo_root = Path(__file__).resolve().parents[2]
    for rel, entry in mod.BLUEPRINT_DEPS.items():
        bp_path = repo_root / "pipeline" / "blueprint" / "v0.1" / rel
        if not bp_path.is_file():
            continue  # blueprint layout drift is its own failure, not this test's
        data = bp_path.read_bytes()
        expected = hashlib.sha3_512(data).hexdigest()[:16]
        assert entry["hash_at_lock"] == expected, (
            f"BLUEPRINT_DEPS drift for {rel}: pinned {entry['hash_at_lock']!r} "
            f"but live sha3_512[:16]={expected!r}"
        )
