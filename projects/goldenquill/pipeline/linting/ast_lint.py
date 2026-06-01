"""Cross-section AST lint harness (ARCH-04 + ARCH-05).

ARCH-04 shipped five deterministic, single-pass rules (R1–R5). ARCH-05
row-appends two walker-intensive rules (R6 alias-walker, R7 CFG-dominance)
that close the alias/attribute-chain/dynamic-import bypass class and the
preflight-dominance bypass class that R1–R5 intentionally admitted under
the v0.1 trusted-operator envelope.

Pure-Python. No third-party dependencies. Runs in the pinned 3.14 venv;
collection-compatible with 3.11+.

Blueprint anchors:
  - section_04_logician.md §3.1 (line 414) — ARCH-04 candidate filing
  - section_04_logician.md §7.4            — no-LLM-client invariant
  - section_04_logician.md §7.6            — no-direct-vault-open invariant
  - section_03_scout.md §7.16              — simple pair (R4 + R5) and
    walker-intensive pair (R6 + R7), refinements A-v3-03, A-v3-07, A-v4-02,
    A-v4-03, B-v5-01, B-v5-02, B-v5-03.

Threat model:
  - R1–R5 catch *honest* drift under the trusted-operator envelope.
  - R6 closes alias/attribute-chain/dynamic-import bypasses per A-v3-03,
    A-v4-03, B-v5-02 (termination guard).
  - R7 enforces CFG-dominance of a module-scope literal-init `Final[bool]`
    preflight sentinel over every `fd_broker.request(...)` sink per A-v3-07,
    A-v4-02, B-v5-01 (literal-init), B-v5-03 (cross-module resolution).

Public surface: see ``__all__``.
"""

from __future__ import annotations

import sys
from pathlib import Path

__all__ = [
    "BLUEPRINT_DEPS",
    "Rule",
    "Violation",
    "lint_tree",
    "LOGICIAN_IMPORT_BAN",
    "LOOP_LOGICIAN_BAN",
    "LOGICIAN_OPEN_BAN",
    "SCOUT_NO_SETATTR_OPERATOR_DECISION",
    "SCOUT_NO_EVAL",
    "AST_NO_INDIRECT_VAULT_READ",
    "AST_PREFLIGHT_DOMINATES_FD_REQUEST",
    "AliasWalkerNonTerminationError",
    "UPLOADER_NO_SUBMIT",
    "UPLOADER_ALLOW_LIST",
    "DEFAULT_RULES",
]

BLUEPRINT_DEPS: dict[str, dict[str, object]] = {
    "section_04_logician.md": {
        "sections_implemented": ["3.1", "7.4", "7.6", "10"],
        "hash_at_lock": "b7e5439cac97b2fe",  # sha3_512[:16] per engineering_process §4.6
        "hash_source_version": "v2.1",
    },
    "section_03_scout.md": {
        "sections_implemented": [
            "7.16-simple",
            "7.16-walker-intensive",  # ARCH-05 R6 + R7
        ],
        "hash_at_lock": "0a82d955f95b0fca",  # sha3_512[:16] per engineering_process §4.6
        "hash_source_version": "v0.1",
    },
}




from pipeline.linting._rule_types import Rule, Violation
from pipeline.linting.ast.runner import lint_tree, _glob_matches_path
from pipeline.linting.ast.rules.r_basic import (
    LOGICIAN_IMPORT_BAN,
    LOOP_LOGICIAN_BAN,
    LOGICIAN_OPEN_BAN,
    SCOUT_NO_SETATTR_OPERATOR_DECISION,
    SCOUT_NO_EVAL,
)
from pipeline.linting.ast.rules.r_alias_walker import (
    AST_NO_INDIRECT_VAULT_READ,
    AliasWalkerNonTerminationError,
    _MAX_ALIAS_WALKER_STEPS,
)
from pipeline.linting.ast.rules.r_cfg_dominance import (
    AST_PREFLIGHT_DOMINATES_FD_REQUEST,
)
from pipeline.linting.ast.rules.r_uploader_no_submit import (
    R_UPLOADER_NO_SUBMIT as UPLOADER_NO_SUBMIT,
    UPLOADER_ALLOW_LIST,
)

DEFAULT_RULES: list[Rule] = [
    LOGICIAN_IMPORT_BAN,
    LOOP_LOGICIAN_BAN,
    LOGICIAN_OPEN_BAN,
    SCOUT_NO_SETATTR_OPERATOR_DECISION,
    SCOUT_NO_EVAL,
    AST_NO_INDIRECT_VAULT_READ,
    AST_PREFLIGHT_DOMINATES_FD_REQUEST,
    UPLOADER_NO_SUBMIT,
]

def _wsl_slice4_rules() -> list[Rule]:
    """Lazy-import the WS-L Slice 4 rules to avoid circular imports.

    Each lint-rule module re-imports :class:`Rule` and :class:`Violation`
    from this file; eager top-level imports here would cycle.
    """
    from pipeline.linting.r_currency_no_float_compare import (
        CURRENCY_GATE_NO_FLOAT_COMPARE,
        CURRENCY_NO_FLOAT_COMPARE,
    )
    from pipeline.linting.r_benchmark_no_short_circuit_compare import (
        BENCHMARK_NO_SHORT_CIRCUIT_COMPARE,
    )
    from pipeline.linting.r_intake_no_logfire_import_before_env import (
        INTAKE_NO_LOGFIRE_IMPORT_BEFORE_ENV,
        INTAKE_SEAT_NO_LOGFIRE_IMPORT_BEFORE_ENV,
    )

    return [
        CURRENCY_NO_FLOAT_COMPARE,
        CURRENCY_GATE_NO_FLOAT_COMPARE,
        BENCHMARK_NO_SHORT_CIRCUIT_COMPARE,
        INTAKE_NO_LOGFIRE_IMPORT_BEFORE_ENV,
        INTAKE_SEAT_NO_LOGFIRE_IMPORT_BEFORE_ENV,
    ]


def _section_04_v2_x_1_rules() -> list[Rule]:
    """Lazy-import the §4 v2.x.1 corrective rules (Tilth-RT-07 closure).

    Lands the AST-lint enumeration extension that closes the Tilth-RT-07
    PARTIAL: R-ARCHIVIST-NO-CANONICAL-MUTATE gains five low-level rename
    primitives as forbidden-call patterns (os.replace, os.rename,
    shutil.move, shutil.copy family, os.link/symlink) per §4 v2.x.1
    SCOPING DRAFT 2026-05-10.
    """
    from pipeline.linting.r_archivist_no_canonical_mutate import (
        ARCHIVIST_NO_CANONICAL_MUTATE,
    )

    return [
        ARCHIVIST_NO_CANONICAL_MUTATE,
    ]


def _section_13_data_collector_slice_3_rules() -> list[Rule]:
    """Lazy-import the §13 Data Collector Slice 3 AST-lint extensions.

    Lands at WS-I Code phase Slice 3 (2026-05-11) — 13 rules per §13 v1
    LOCK §13.16.6.4 final AST-lint roster. The rule module imports
    :class:`Rule` from :mod:`pipeline.linting._rule_types`; eager top-level
    imports here would cycle.
    """
    from pipeline.linting.r_datacollector_slice_3 import ALL_RULES

    return list(ALL_RULES)


def _section_14_report_generator_slice_3_rules() -> list[Rule]:
    """Lazy-import the §14 Report Generator Slice 3 AST-lint extensions.

    Lands at WS-J Code phase Slice 3 (2026-05-11) — 3 rules per §14 v1
    LOCK §14.16 + §14.9.4 + Cycle 2 RT-C2-01 closure:

      - R-REPORT-NO-AUTO-FINALIZE — Layer 1 of three-layer defense
        against auto-finalize.
      - R-REPORT-VAULT-INTENT-REQUIRED — Layer 1 of three-layer defense
        against raw open() / Path.read_text() / yaml.safe_load(...) calls
        inside the §14 substrate.
      - R-REPORT-DECIMAL-MANDATE — Layer 1 of three-layer defense
        against float() coercion / float-literal arithmetic / float-
        literal comparison / Decimal(float_literal) in the §14
        substrate (scope EXTENDED to composers + report_mode per Cycle
        2 RT-C2-01 closure).
    """
    from pipeline.linting.r_report_no_auto_finalize import (
        REPORT_NO_AUTO_FINALIZE,
    )
    from pipeline.linting.r_report_vault_intent_required import (
        REPORT_VAULT_INTENT_REQUIRED,
    )
    from pipeline.linting.r_report_decimal_mandate import REPORT_DECIMAL_MANDATE

    return [
        REPORT_NO_AUTO_FINALIZE,
        REPORT_VAULT_INTENT_REQUIRED,
        REPORT_DECIMAL_MANDATE,
    ]


def _section_17_wpfa_rules() -> list[Rule]:
    """Lazy-import the §17 WPFA AST-lint rules (Layer 1 + A12 energy extension).

    Lands at §17 v1 LOCK + §4 v2.x.z LOCK 2026-05-11:
      - R-WPFA-NO-AUTOSIGN — Layer 1 of three-layer defense for buyer-PDF.
      - R-WPFA-DECIMAL-MANDATE-ENERGY — A12 extension to energy field names
        (_minor_units|_micro|_saved)$ across seats/wpfa, vault/sub_kinds,
        and logician/gates/f_wpfa_* scopes.
    """
    from pipeline.linting.r_wpfa_no_autosign import WPFA_NO_AUTOSIGN
    from pipeline.linting.r_wpfa_decimal_mandate_energy import (
        WPFA_DECIMAL_MANDATE_ENERGY,
        WPFA_DECIMAL_MANDATE_ENERGY_GATES,
        WPFA_DECIMAL_MANDATE_ENERGY_VAULT,
    )

    return [
        WPFA_NO_AUTOSIGN,
        WPFA_DECIMAL_MANDATE_ENERGY,
        WPFA_DECIMAL_MANDATE_ENERGY_VAULT,
        WPFA_DECIMAL_MANDATE_ENERGY_GATES,
    ]


def _v7_0_10_rules() -> list[Rule]:
    """Lazy-import the architecture v7.0.10 AST-lint rules.

    Lands at v7.0.10 LOCKED 2026-05-11 paired-commit (§0.5 v21 amendment).

      - R-V0-10-NO-SLOT-TOKEN-EMISSION — Layer 1 defense forbidding `[SLOT_*]`
        token literals in orchestrator + seat modules. Two Rule instances
        registered (one per target_glob) because the harness matches a single
        glob per Rule.
      - R-CLASS-POSTURE-FIELD-COVERAGE — Enforces that the F-CLASS-REGISTER-*
        gate module references the `selected_posture` field added at v7.0.10
        §1.4 (Classification Review UX surface flip).
    """
    from pipeline.linting.r_v0_10_no_slot_token_emission import (
        V0_10_NO_SLOT_TOKEN_EMISSION,
        V0_10_NO_SLOT_TOKEN_EMISSION_SEATS,
    )
    from pipeline.linting.r_class_posture_field_coverage import (
        CLASS_POSTURE_FIELD_COVERAGE,
    )

    return [
        V0_10_NO_SLOT_TOKEN_EMISSION,
        V0_10_NO_SLOT_TOKEN_EMISSION_SEATS,
        CLASS_POSTURE_FIELD_COVERAGE,
    ]


def _section_04_v2_x_5_rules() -> list[Rule]:
    """Lazy-import the §4 v2.x.5 corrective rules (CC-007 closure).

    Lands the AST-lint rule R-NO-DIRECT-PROVIDER-HTTP per §4 v2.x.5
    LOCKED 2026-05-16 row 232. Mirrors the §4 v2.x.1 row 198 sub-tag-
    extension precedent (R-ARCHIVIST-NO-CANONICAL-MUTATE shape): five
    sub-tags + RT-14 fold-in `.unknown_http_library_import` + CC-003
    carry-forward `pipeline_deprecated_imported_from_runtime` ban.

    The CC-003 quarantine logic (pre-§4-v2.x.5) is folded into this
    rule's body; the standalone _cc003_rules block is retired.
    """
    from pipeline.linting.r_no_direct_provider_http import (
        NO_DIRECT_PROVIDER_HTTP,
    )

    return [NO_DIRECT_PROVIDER_HTTP]


def _section_04_v2_x_apolitical_dialect_rules() -> list[Rule]:
    """Lazy-import the §4 v2.x apolitical_dialect AST-lint rules.

    Lands R-NO-POLITICAL-AXIS-LITERAL per §4 v2.x apolitical_dialect §4.X.2
    + §0.5 v28 row 551 (LOCKED 2026-05-16T14:00:00Z; lock_history rows
    236/249 and 237/246). Architecture v7.0.12 retires the four-axis
    political enum (conservative | centrist | progressive | soul_fire |
    soul-fire). The rule is registered as three instances (one per target
    glob: cards / types / logician-gates) because the harness matches a
    single glob per Rule. Companion runtime gate:
    F-DIALECT-POLITICAL-AXIS-LEAK at PRE-gate order 6.55.
    """
    from pipeline.linting.r_no_political_axis_literal import (
        NO_POLITICAL_AXIS_LITERAL_CARDS,
        NO_POLITICAL_AXIS_LITERAL_LOGICIAN,
        NO_POLITICAL_AXIS_LITERAL_TYPES,
    )

    return [
        NO_POLITICAL_AXIS_LITERAL_CARDS,
        NO_POLITICAL_AXIS_LITERAL_TYPES,
        NO_POLITICAL_AXIS_LITERAL_LOGICIAN,
    ]


DEFAULT_RULES.extend(_wsl_slice4_rules())
DEFAULT_RULES.extend(_section_04_v2_x_1_rules())
DEFAULT_RULES.extend(_section_17_wpfa_rules())
DEFAULT_RULES.extend(_section_13_data_collector_slice_3_rules())
DEFAULT_RULES.extend(_section_14_report_generator_slice_3_rules())
DEFAULT_RULES.extend(_v7_0_10_rules())
DEFAULT_RULES.extend(_section_04_v2_x_5_rules())
DEFAULT_RULES.extend(_section_04_v2_x_apolitical_dialect_rules())


def _format_violation(v: Violation) -> str:
    return (
        f"{v.file}:{v.line}:{v.col}: {v.rule_name} "
        f"[{v.reason_tag}] {v.message}"
    )

def main(argv: list[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    target = Path(args[0]) if args else Path("pipeline")
    violations = lint_tree(target, DEFAULT_RULES)
    if not violations:
        return 0
    for v in violations:
        print(_format_violation(v), file=sys.stderr)
    print(
        f"ast_lint: {len(violations)} violation(s) under {target}",
        file=sys.stderr,
    )
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
