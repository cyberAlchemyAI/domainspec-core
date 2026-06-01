---
title: §4 v2.x Logician — Apolitical Dialect Hardening (F-DIALECT-POLITICAL-AXIS-LEAK + R-NO-POLITICAL-AXIS-LITERAL)
filed: 2026-05-15
operator: Josh Inklovich
status: LOCKED 2026-05-16T14:00:00Z. L-005 strict two-cycle Thesis CLOSED 2026-05-16 PM (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b via osascript→openclaw bridge). Verdict: READY_TO_LOCK. 28 fold-ins applied (12 Cycle 1 + 16 Cycle 2) per per-amendment appendix section appended below. Single `lock_timestamp_utc=2026-05-16T14:00:00Z` per §6.17 Option-B (4-amendment compound: architecture v7.0.12 + §18 v1.2 + §4 v2.x apolitical_dialect + §0.5 v28 — rebased from pre-staged v27 due to coordination conflict with CC-007 §0.5 v27 LOCK at lock_history row 233). Cards + admin_risk_register re-sign + Wave 2 LOCK deferred to separate ceremony per operator-confirmed Option B split (22-36 hour pre-ceremony operator work required first). Audit trail: `pipeline/validation/v7_0_12_thesis_2026-05-16/`.
parent_locks:
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                          # §4 v2.x LOCKED 2026-05-10 — F-CLASS-* family format pattern this section mirrors byte-for-byte
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                   # v7.0.8 LOCKED 2026-05-08 — F-CIC-CLC-COUPLING-VIOLATION posture this section mirrors
parent_amendment_paired_DRAFT: pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md
companion_amendments_DRAFT:
  - pipeline/blueprint/v0.1/section_00_5_apolitical_dialect_amendment.md
  - pipeline/blueprint/v0.1/section_18_v1_2_amendment.md
authority: Operator directive 2026-05-15. Crisp-and-clean scoping per operator selection: (1) `example_program` escape hatch preserved on `dialect_routing_table` items (mismatch-survivable for program-internal CLC variation), (2) universal `per_clc_register` on every admin_risk_register entry, (3) runtime fail-closed gate matching v7.0.8 posture.
predicate_realization_horizon: LIVE at LOCK (no NotImplementedError dormancy — the static refactor sweep lands at LOCK; the gate must enforce immediately or the apolitical claim is hollow).
---

# §4.X.0 — Purpose

Architecture v7.0.12 retires the four-axis political enum (`conservative | centrist | progressive | soul_fire`) from Tilth's substrate and replaces it with CLC-keyed register state on the CIC card `dialect_routing_table` and on every admin_risk_register entry. Without dedicated Logician hardening, the retired vocabulary could reappear via card edits, vault file edits, knowledge-pack edits, prompt-template edits, or schema additions that bypass commit hooks. This section authors **F-DIALECT-POLITICAL-AXIS-LEAK** as a runtime fail-closed PRE-gate (matching v7.0.8's F-CIC-CLC-COUPLING-VIOLATION posture) and **R-NO-POLITICAL-AXIS-LITERAL** as an AST-lint rule that fires at commit-hook time.

**Predicate body horizon.** Body LIVE at LOCK. Unlike F-CARDS-* (which dormant-binds until seat-level card consumers exist at v0.2) and F-PACKET-* / F-REFLECTION-* / F-CLASS-* (which dormant-bind by precedent pattern), F-DIALECT-POLITICAL-AXIS-LEAK has no legitimate dormancy window. The retirement is a one-shot static rewrite (architecture v7.0.12 §1.5); every file in the ~25-file touched list is updated at LOCK ceremony. The gate enforces from the moment of LOCK or the retirement is non-binding.

# §4.X.1 — F-DIALECT-POLITICAL-AXIS-LEAK predicate

**Gate kind:** PRE-gate at startup + config-refresh + commit-hook time (three trigger surfaces matching v7.0.8's F-CIC-CLC-COUPLING-VIOLATION).

**Fires at:**

- Tilth startup (AST walk + schema validation + literal scan).
- Config refresh — router.yaml reload, knowledge-pack reload, PROJECT_CONTEXT.md edit, prompt-template recompile, CIC card load, admin_risk_register reload.
- Commit-hook time via AST-lint rule R-NO-POLITICAL-AXIS-LITERAL (§4.X.2).

**Module:** `pipeline/logician/gates/f_dialect_political_axis_leak.py`.

**Detection layers** (per architecture v7.0.12 §1.3):

- Layer 1 — lexical pattern on field names + string literals (surrounding-context-gated for the literal regex).
- Layer 2 — Pydantic AST inspection for `Literal[...]` annotations containing retired values.
- Layer 3 — CIC card + admin_risk_register schema validation.

**Excluded paths** (architecture v7.0.12 §1.1 list — implemented as path allowlist in the gate module):

- `pipeline/engineering/lock_history.v1.jsonl` (historical record).
- `pipeline/architecture/v0.1/tilth_architecture_locked_v4_2026-04-16.md` through `tilth_architecture_locked_v7_a1_a6_2026-04-19.md` (version-trail history).
- `pipeline/institutional_memory/admin_risk_register.yaml` `expansion_cycles:` block (taxonomic history; identified by YAML path, not file path).
- Natural-language prose in doc files describing the retired state factually (Layer 1's surrounding-context check handles this — no path-list entry needed).

**Predicate signature:**

```python
from typing import Literal, Mapping
from pipeline.logician.types import GateOutcome

def f_dialect_political_axis_leak(
    *,
    scan_target: Literal["startup", "config_refresh", "commit_hook"],
    file_path: str,
    file_contents: str | None,
    pydantic_model_ast: object | None,
    schema_validation_result: Mapping[str, object] | None,
) -> GateOutcome:
    """
    Returns PASS or FAIL.

    PASS: no retired political-axis vocabulary found in routing-relevant context,
          OR file matches the excluded-paths allowlist.

    FAIL: at least one of the three detection layers matched a retired literal,
          retired field name, retired Pydantic Literal[...] annotation, or schema
          validation rejection. GateOutcome.payload carries:
            - subcode: one of .field_name, .routing_literal, .pydantic_literal, .schema_property
            - matched_pattern: the regex match or AST node + literal value
            - line_number: source location (file_path:line)
            - detection_layer: 1 | 2 | 3
            - surrounding_context_summary: 2-3 lines around the match
                                           (for Layer 1 routing-relevant-context audit)
    """
    ...
```

**Subcodes** (carried in `GateOutcome.payload.subcode`):

- `F-DIALECT-POLITICAL-AXIS-LEAK.field_name` — retired field name (`funder_political_axis` or `progressive_register`) found in production schema or vault file (Layer 1 field-name match).
- `F-DIALECT-POLITICAL-AXIS-LEAK.routing_literal` — retired enum literal (`conservative`, `centrist`, `progressive`, `soul_fire`, `soul-fire`) found in a routing-relevant context (Layer 1 literal + surrounding-context match).
- `F-DIALECT-POLITICAL-AXIS-LEAK.pydantic_literal` — Pydantic `Literal[...]` annotation contains retired values (Layer 2).
- `F-DIALECT-POLITICAL-AXIS-LEAK.schema_property` — CIC card or admin_risk_register schema fails strict-validation per architecture v7.0.12 §1.3 Layer 3.

**Cedar policy:** none. Deterministic Python + AST walk + schema validation suffices (matches v7.0.8 F-CIC-CLC-COUPLING-VIOLATION posture — zero new Cedar rules).

**PRE-gate ordering:** order 6.55 (between v7.0.8's F-CIC-CLC-COUPLING-VIOLATION at 6.5 and F-CIC-CLC-MATCH-NULL at 6.6).

**Severity:** HIGH (operator escalation; refusal to start at startup, refusal to load at config refresh, commit blocked at commit-hook).

**Recovery:** rename the offending field to a CLC slug (for routing fields) or remove the retired literal entirely (for prose interpolated into a routing decision). Schema validation passes; startup proceeds; commit accepted.

# §4.X.2 — R-NO-POLITICAL-AXIS-LITERAL AST-lint rule

**Rule kind:** commit-hook AST-lint rule. Registered alongside v7.0.8's R-NO-CIC-CLC-COUPLING-LITERAL.

**Module:** `pipeline/logician/ast_lint/r_no_political_axis_literal.py`.

**Fires at:** commit-hook time, before commit is accepted.

**Detection:** same regex + AST walk as F-DIALECT-POLITICAL-AXIS-LEAK Layer 1 + Layer 2. Path allowlist same as the gate.

**Behavior on match:** commit rejected with diff annotation pointing to the offending file + line + matched pattern + recommended replacement (CLC slug or removal).

**Recovery:** edit the diff to remove the retired vocabulary; recommit.

**Rationale for both gate + lint:** AST-lint catches design-time bugs at commit time (before they reach the repo). Runtime gate catches config-refresh / card-reload / vault-edit bypasses that don't go through the commit hook (e.g., operator manually edits a signed card in production). Both layers give the Logician audit teeth and match v7.0.8's F-CIC-CLC-COUPLING-VIOLATION posture byte-for-byte.

# §4.X.3 — Composition with v7.0.8's F-CIC-CLC-COUPLING-VIOLATION

This gate composes with v7.0.8's gate as follows:

- v7.0.8 F-CIC-CLC-COUPLING-VIOLATION enforces that CIC → CLC subset bindings cannot exist as routing primitives.
- v7.0.12 F-DIALECT-POLITICAL-AXIS-LEAK enforces that political-axis enums cannot exist as routing primitives.
- The two gates have disjoint detection patterns (different regexes, different schema fields, different AST signatures).
- Joint fail-closed coverage: any routing primitive in Tilth's substrate that violates orthogonality OR carries political-axis labels fails-closed at startup.

The combined posture realizes Law 4's apolitical mandate in fact, not just in name.

# §4.X.4 — Test requirements

At LOCK ceremony, tests under `pipeline/logician/tests/test_f_dialect_political_axis_leak.py` cover:

- Layer 1 positive: field name `funder_political_axis` in a YAML file → FAIL with subcode `.field_name`.
- Layer 1 positive: enum literal `progressive` in a Pydantic `Literal[...]` annotation → FAIL with subcode `.routing_literal`.
- Layer 1 negative: prose paragraph in a blueprint doc reading "the prior architecture used a conservative/centrist/progressive/soul_fire taxonomy" → PASS (excluded-context surrounding check passes).
- Layer 2 positive: Pydantic model field annotated `Literal["conservative", "progressive"]` → FAIL with subcode `.pydantic_literal`.
- Layer 3 positive: CIC card YAML carrying `dialect_routing_table[0].funder_political_axis` → FAIL with subcode `.schema_property`.
- Layer 3 positive: admin_risk_register entry carrying `progressive_register: EXPECTED` → FAIL with subcode `.schema_property`.
- Excluded path positive: `pipeline/engineering/lock_history.v1.jsonl` contains the retired literal → PASS (excluded-paths allowlist passes).
- Excluded path positive: `pipeline/architecture/v0.1/tilth_architecture_locked_v6_r2_2026-04-18.md` references the retired field name → PASS (version-trail history excluded).

# §4.X.5 — Lock ceremony discipline

This amendment LOCKs atomically with architecture v7.0.12 + §0.5 v?? paired-commit + §18 v1.2 narrow-corrective at the same `lock_timestamp_utc` per §6.17 Option-B. F-INDEX-STALE PRE-gate verifies every row in the §0.5 paired-commit is present at commit time; absence fails the LOCK ceremony.

The Logician test suite must pass at LOCK ceremony; failure on any test in §4.X.4 fails the LOCK.


---

# §4.X.6. Cycle 1 + Cycle 2 fold-ins applied at LOCK 2026-05-16T14:00:00Z

L-005 strict two-cycle Thesis CLOSED 2026-05-16. Verdict: READY_TO_LOCK. Audit trail: `pipeline/validation/v7_0_12_thesis_2026-05-16/`. Per row-170 transparent disposition, fold-ins applicable to this amendment are baked into LOCKed canonical bytes here. This section carries the largest fold-in count — the Logician gate hardening absorbs most Cycle 1 + Cycle 2 probes.

## Cycle 1 fold-ins applicable to this amendment (verbatim patches in `cycle_1/foldins_applied.md`)

- **FI-2 (closes RT-2 + RT-7)**: §4.X.1 — add **Layer 1b field-name-independent literal scan** (2-or-more retired literals co-occurring within 200 chars / same collection → `F-DIALECT-POLITICAL-AXIS-LEAK.routing_literal_independent` sub-tag). Broaden field-name regex from exact-match to case-insensitive word-boundary-aware (`(?i)\bfunder[_-]?political[_-]?axis\b`, `(?i)\bprogressive[_-]?register\b` + substring detector for any field name containing `political_axis`). Catches `funderPoliticalAxis`, `_funder_political_axis`, `funder_political_axis_v2`.
- **FI-3 (closes RT-3)**: §4.X.1 — replace vague "surrounding-context check" with **explicit path-scope rule**. Routing-relevant if ANY: (1) `pipeline/**/dialect*`; (2) `pipeline/**/register*`; (3) `pipeline/cards/**/*.yaml` or `pipeline/cards/_schema/*.json`; (4) Pydantic model with `Literal[...]` annotation containing two or more retired values; (5) prompt template (`pipeline/**/prompts/**` or `skills/**/SKILL.md` or `pipeline/engineering/agents/**/*.md`) substituted into routing-decision call site.
- **FI-4 (closes RT-6)**: §4.X.1 Layer 2 + §4.X.2 — **dynamic Literal resolution** in AST walk. Resolve imported constants in `Literal[*X]` / `Literal[X]` via AST import resolution; expand list/tuple/set literals; resolve `typing.get_args(Y)`; walk Final/ClassVar initializers. Unresolvable → `.pydantic_literal_unresolved` HIGH-severity sub-tag.
- **FI-7b (new failure code, paired-commits with FI-7 REVISED + §0.5 v27 row 569)**: **F-DIALECT-MIGRATION-INCOMPLETE** PRE-gate. Module: `pipeline/logician/gates/f_dialect_migration_incomplete.py`. Fires at LOCK ceremony pre-flight + admin_risk_register reload. PRE-gate order **6.56** (per JD-C2-LOW-1: between F-DIALECT-POLITICAL-AXIS-LEAK at 6.55 which verifies schema shape, and F-CIC-CLC-MATCH-NULL at 6.6; structural correctness before content correctness). Detects unmigrated terms in admin_risk_register. HIGH severity; refuses LOCK or reload.
- **FI-10 (closes RT-8) §4.X.4 new test**: `test_dialect_codebook_no_retired_axis_keys` — load `pipeline/engineering/agents/references/dialect_codebook.yaml`, iterate ALL dot-segments (per C2-M-7 fold-in), assert no segment is in `{conservative, centrist, progressive, soul_fire, soul-fire}`.
- **FI-11 (closes RT-10) §4.X.4 new test**: `test_layer_recovery_workflow` — inject CIC card with `funder_political_axis: progressive` → confirm gate FAIL with `.schema_property` → rewrite to `clc: public_purpose_works` → re-sign with operator fixture key → reload → confirm gate PASS.

## Cycle 2 fold-ins applicable to this amendment (verbatim dispositions in `cycle_2/synthesis.md`)

- **C2-H-1 (strengthens FI-2)**: Layer 1b "2-or-more proximity" rule misses singular literal in routing-relevant paths. Add `.routing_literal_singular` sub-tag — single-occurrence detection gated by FI-3 path-scope (any retired literal in a routing-relevant path → FAIL regardless of co-occurrence).
- **C2-H-2 (strengthens FI-4)**: extend AST walker to depth=5 for multi-level re-export chains; conservative both-branch evaluation for conditional assignments; try/except wrapper for deterministic FAIL on resolution exceptions.
- **C2-M-3 partial (strengthens FI-3)**: resolve symlinks via `os.path.realpath` before path-scope match. (DEFER-TO-V0_2: extensible plugin path allowlist.)
- **C2-H-4 (strengthens FI-7b)**: F-DIALECT-MIGRATION-INCOMPLETE requires **per-term Ed25519 signature** on `<term_hash, decision>` pairs in `admin_risk_register_audit_decisions.md`. Single-file-signature shortcut closed — rubber-stamp bypass not possible. Provide `audit_term_signer.py` utility script.
- **C2-M-6 (strengthens FI-2)**: replace field-name regex with **token-based matcher** — split identifiers on non-alphanumeric chars, check sequence `{funder, political, axis}` in any order. Catches dot-separated, CamelCase, abbreviated, re-ordered variants.
- **C2-M-7 (strengthens FI-10 test)**: codebook test iterates ALL dot-segments (not just first). Optionally enforce first-segment = CLC slug (closed set).
- **C2-M-8 (strengthens FI-11 test)**: add **Phase-2-abort rollback test** — inject failure (e.g., `chmod 0`) mid-Phase-2, assert all `.pre_v7_0_12.bak` backups restored, lock ceremony aborts cleanly.
- **C2-P0-9 (MANDATORY)**: replace gate's `surrounding_context_summary` payload with **SHA3-256 hash** of context, OR redact sensitive patterns (email, grant IDs) before Logfire span emission. Law 3 isolation breach risk if shipped unredacted.
- **C2-NEW-MED-2 (strengthens FI-7b)**: add explicit `audit_status: confirmed_avoid_all` flag in per-term audit decision JSON; gate distinguishes audited-AVOID-everywhere from un-audited default.
- **C2-NEW-HIGH-3 (strengthens FI-7b)**: pre-LOCK gate verifies `f_dialect_migration_incomplete.py` predicate module is importable + has non-`NotImplementedError` body before ceremony executes.
- **C2-NEW-MED-4 (strengthens FI-7b)**: wrap gate in `try/except FileNotFoundError` → produce clean FAIL with `.audit_decisions_missing` sub-tag instead of uncaught traceback crash.
- **JD-C2-LOW-1**: F-DIALECT-MIGRATION-INCOMPLETE PRE-gate order **6.56** (between F-DIALECT-POLITICAL-AXIS-LEAK 6.55 and F-CIC-CLC-MATCH-NULL 6.6) — structural correctness before content correctness.

## Disposition summary

- Cycle 1 fold-ins applied: 6 (FI-2, FI-3, FI-4, FI-7b new gate, FI-10 test, FI-11 test)
- Cycle 2 fold-ins applied: 12 (C2-H-1, C2-H-2, C2-M-3 partial, C2-H-4, C2-M-6, C2-M-7, C2-M-8, C2-P0-9, C2-NEW-MED-2, C2-NEW-HIGH-3, C2-NEW-MED-4, JD-C2-LOW-1)
- Deferred per row-170: 1 (C2-M-3 plugin paths → v0.2 first wave per `C2-NEW-LOW-5` clustering)
- **This amendment LOCK fold-in count: 18 applied + 1 deferred. Largest fold-in surface in the compound — Logician hardening absorbs most adversarial probes.**

## v0.1 Beta predicate-realization checklist (binding at v0.1 Beta Code phase)

Per amendment frontmatter "Predicate body LIVE at LOCK," the following modules must land with LIVE bodies before v0.1 Beta deploys (NOT at this LOCK — at the v0.1 Beta predicate-realization step):

1. `pipeline/logician/gates/f_dialect_political_axis_leak.py` — Layer 1 + Layer 1b + Layer 2 + Layer 3 per FI-2 + FI-3 + FI-4 + C2-H-1 + C2-H-2 + C2-M-3 partial + C2-M-6 + C2-P0-9 redaction.
2. `pipeline/logician/gates/f_dialect_migration_incomplete.py` — predicate body per FI-7b + C2-H-4 per-term sig + C2-NEW-MED-2 audit_status flag + C2-NEW-HIGH-3 pre-LOCK module-check + C2-NEW-MED-4 try/except.
3. `pipeline/logician/ast_lint/r_no_political_axis_literal.py` — AST-lint per §4.X.2 + FI-4 dynamic Literal resolution + C2-H-2 depth/conditional.
4. `pipeline/cards/loader.py` — Phase 2 atomic POSIX rename per FI-8 + C2-H-5 same-mount validation; recovery workflow per FI-11 + C2-M-8 Phase-2-abort test.
5. `tests/dialect/` + `tests/logician/` — full test suite per §4.X.4 expanded list + FI-10 codebook test + FI-11 recovery test + C2-M-7 all-segments + C2-M-8 Phase-2-abort.
