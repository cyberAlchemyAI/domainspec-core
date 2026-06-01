# Spec card — Logician gate F-AMENDMENT-SELF-REFERENCE-DETECT (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit/` — EN-003 F-4-Cycle3
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #7

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 2 (reads lock_history.v1.jsonl + router.yaml)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-07`

---

## Gate name and failure code

- **Gate:** `F-AMENDMENT-SELF-REFERENCE-DETECT`
- **Failure code:** `F-AMDT-07`
- **Kind:** PRE-gate on amendment with `modifies_committee: true`

## Purpose

When an amendment adds a reviewer to a governed committee (e.g., the Code Thesis Committee), and the added reviewer belongs to the same model family as the active Judge, the Judge would be scoring an amendment that benefits its own family — a self-referencing conflict. This gate detects the three-condition trigger (modifies committee + added family matches Judge family + amendment author is from a different family) and requires the amendment to include an explicit Judge reassignment to a non-self-referencing family. Makes the conflict-of-interest check structural rather than procedural.

## Trigger condition

Fires as a PRE-gate on any amendment whose frontmatter contains `modifies_committee: true`. The three-condition check determines whether DENY is warranted:

1. `modifies_committee: true` (amendment touches committee composition).
2. `added_reviewer_family` matches `judge_primary_family` from `router.yaml`.
3. `author_family` ≠ `judge_primary_family` (the amendment is not authored by the Judge's own family — that case is a different conflict vector).

All three must hold AND the amendment must NOT include a `judge_reassigned_to` field specifying a non-self-referencing family.

## Input contract

```python
@runtime_checkable
class RouterConfigReaderCallable(Protocol):
    def __call__(self) -> dict: ...
```

- `amendment_frontmatter: dict` — must contain `modifies_committee: true` (trigger), plus `added_reviewer_family: str`, `author_family: str`. May contain `judge_reassigned_to: str`.
- `router_config_reader: RouterConfigReaderCallable` — injected callable returning parsed `router.yaml` content. Gate reads `judge_primary_family` from this.

## Pass/fail criteria (deterministic — no LLM)

1. Confirm `amendment_frontmatter["modifies_committee"]` is `True`. If not → no-op PASS.
2. Read `judge_primary_family` from `router_config_reader()`. If unreadable → FAIL (fail-closed on ambiguity).
3. Extract `added_reviewer_family` from frontmatter. If missing → FAIL.
4. Extract `author_family` from frontmatter. If missing → FAIL.
5. **Condition check:** all three conditions hold:
   - `modifies_committee` is True ✓ (already confirmed)
   - `added_reviewer_family == judge_primary_family`
   - `author_family != judge_primary_family`
6. If all three hold:
   a. Check for `judge_reassigned_to` in frontmatter.
   b. If present AND `judge_reassigned_to != judge_primary_family` AND `judge_reassigned_to != added_reviewer_family` → PASS (reassignment resolves the conflict).
   c. If absent or self-referencing → **FAIL (`F-AMDT-07`)**.
7. If any of the three conditions does NOT hold → PASS (no self-reference conflict detected).
8. **FAIL (`F-AMDT-07`):** any missing required field or router.yaml unreadable. Fail-closed.
9. False negatives (conditions partially ambiguous) logged to `lessons.md` as recurring-pattern candidates per consolidated backlog spec.

## Failure behavior

- **DENY** the amendment promotion.
- Emit structured failure record to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-07"`, `gate: "F-AMENDMENT-SELF-REFERENCE-DETECT"`, `judge_family`, `added_family`, `author_family`, `reassignment: null|<value>`.
- Operator must either add a `judge_reassigned_to` field with a non-conflicting family or restructure the amendment.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- Injected `RouterConfigReaderCallable` for `router.yaml` access (E-017 pattern). No direct YAML parsing in gate code.
- String comparisons are exact (model family names are canonical lowercase strings in `router.yaml`).
- The `judge_reassigned_to` field must differ from BOTH `judge_primary_family` AND `added_reviewer_family` to resolve the conflict — reassigning Judge to the same family being added is still self-referencing.
- Lives at `pipeline/logician/gates/f_amendment_self_reference_detect.py`.
- AST-lint R1–R5 clean at module load.
- False-negative logging: when any of the three fields is present but ambiguous (e.g., empty string), gate DENY but also appends a structured entry to an injected lessons log for pattern tracking.

## Test criteria

### Unit tests (≥30)
- All three conditions met, no reassignment → DENY.
- All three conditions met, valid reassignment to third family → PASS.
- All three conditions met, reassignment to judge's own family → DENY.
- All three conditions met, reassignment to the added family → DENY.
- `modifies_committee: false` → no-op PASS.
- `modifies_committee: true`, `added_reviewer_family` ≠ `judge_primary_family` → PASS (condition 2 fails).
- `modifies_committee: true`, `author_family` == `judge_primary_family` → PASS (condition 3 fails — author IS Judge's family).
- Missing `added_reviewer_family` → DENY (fail-closed).
- Missing `author_family` → DENY (fail-closed).
- Router.yaml returns empty dict → DENY (fail-closed on missing `judge_primary_family`).
- Parametrized over family names: anthropic, google, groq, openai, meta.
- `judge_reassigned_to` is empty string → DENY (not a valid family).

### Adversarial tests (≥5)
- `test_adv_router_config_reader_raises` → DENY (fail-closed).
- `test_adv_modifies_committee_is_string_true` → `"true"` not `True` → no-op PASS (strict `is True`).
- `test_adv_family_name_case_mismatch` → `"Anthropic"` vs `"anthropic"` → PASS (no match — family names are canonical lowercase; gate does not normalize).
- `test_adv_judge_reassigned_to_same_as_added_family` → reassignment to the family being added → DENY (still self-referencing).
- `test_adv_all_three_families_identical` → author, added, and judge all same family → condition 3 fails (`author_family == judge_primary_family`) → PASS (different conflict vector, not this gate's scope).

## Dependencies

- `router.yaml` with `judge_primary_family` field (exists today).
- `RouterConfigReaderCallable` Protocol.
- §4 v2.1 gate infrastructure (PRE-gate hook on amendment promotion).
- Lessons logging infrastructure for false-negative tracking.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_amendment_self_reference_detect.py` |
| Tests | `tests/logician/gates/test_f_amendment_self_reference_detect.py` + `tests/logician/gates/test_adv_f_amendment_self_reference_detect.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-AMENDMENT-SELF-REFERENCE-DETECT"`, `failure_code: "F-AMDT-07"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-07 |
| Memory | MEMORY.md index entry |

---

## v1.1 extension — C4-NEW-04 author-family anti-collision coverage

**Origin:** EN-003 Cycle 4 Red Team Finding C4-NEW-04 (2026-04-20). The existing anti-collision invariant in the Code Thesis Committee covers primary/secondary/tertiary fallback layers but NOT the amendment author's family. If `author_family == tertiary_fallback_family` (e.g., OpenAI-direct author colliding with Codex tertiary), the committee silently resolves with two same-family voices in the review pool — a self-reference vector the v1 gate did not see.

**Scope of extension:** expand the trigger condition and pass/fail criteria to include `author_family` in the anti-collision check across ALL fallback layers, not just the Judge primary.

### Extended trigger condition

Gate fires (as v1) on `modifies_committee: true`. The three-condition check expands to a four-condition check:

1. `modifies_committee: true` (as v1).
2. `added_reviewer_family` matches `judge_primary_family` from `router.yaml` (as v1).
3. `author_family` ≠ `judge_primary_family` (as v1).
4. **(NEW in v1.1)** `author_family` does NOT collide with ANY of: `code_reviewer_1.primary_family`, `code_reviewer_1.fallback_family`, `code_reviewer_2.primary/fallback_family`, … through all five code_reviewer slots' primary AND fallback families.

If condition 4 is violated — `author_family` matches any committee slot primary or fallback — the amendment must include a `committee_slot_reassigned_away_from_author_family: str` field identifying which slot and its non-conflicting replacement family.

### Extended input contract

```python
# RouterConfigReaderCallable reads full router.yaml including all committee slots.
# No new Protocol required; existing reader returns full parsed config.
```

### Extended pass/fail criteria

Add after v1 step 6:

7. **Author-family anti-collision (v1.1):** from `router_config_reader()`, extract the committee slot family set:
   ```
   committee_families = {
     code_reviewer_1.primary_family, code_reviewer_1.fallback_family,
     code_reviewer_2.primary_family, code_reviewer_2.fallback_family,
     code_reviewer_3.primary_family, code_reviewer_3.fallback_family,
     code_reviewer_4.primary_family, code_reviewer_4.fallback_family,
     code_reviewer_5.primary_family, code_reviewer_5.fallback_family,
   }
   ```
   If `author_family` ∈ `committee_families`:
   a. Check for `committee_slot_reassigned_away_from_author_family` field.
   b. If present AND reassignment is to a family NOT in `committee_families ∪ {author_family}` → PASS.
   c. If absent or reassignment itself collides → **FAIL `F-AMDT-07-AUTHOR-COLLISION`**.

### Extended test criteria

**Additional unit tests (≥6):**
- Author family not in any committee slot → PASS (v1 behavior preserved).
- Author family matches code_reviewer_1 primary → DENY without reassignment.
- Author family matches code_reviewer_4 fallback (gpt-oss-20b case) → DENY without reassignment.
- Author family collides + valid reassignment to external family → PASS.
- Author family collides + reassignment to same colliding family → DENY.
- Author family collides + reassignment targets a DIFFERENT committee slot's existing family → DENY (reassignment must escape the committee family set entirely).

**Additional adversarial tests (≥3):**
- `test_adv_author_collides_with_tertiary_not_primary` — author=OpenAI-direct, code_reviewer_1.primary=Codex (openai family), fallback=gpt-4o (openai family) → DENY (collision with any layer).
- `test_adv_author_family_collides_post_fallback` — simulate live fallback scenario where a primary has failed and the slot now serves from its fallback; author was cleared against primary-family but now collides with live fallback-family → DENY at amendment-time (gate reads BOTH primary and fallback families at check time, not live resolution).
- `test_adv_committee_has_homoglyph_family_name` — e.g., "openai" vs "OpenAI" → gate treats as NOT matching (canonical lowercase per existing convention).

### §0.5 paired-commit rows (v1.1 additions)

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_amendment_self_reference_detect.py` (extended from v1) |
| Tests | Additional test methods in existing `test_f_amendment_self_reference_detect.py` + `test_adv_*.py` |
| Lock history | v1.1 row in `pipeline/engineering/lock_history.v1.jsonl` with `gate: "F-AMENDMENT-SELF-REFERENCE-DETECT"`, `version: "v1.1"`, `failure_code: "F-AMDT-07-AUTHOR-COLLISION"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-07-AUTHOR-COLLISION sub-code |

---

*Spec card v1 — 2026-04-20 — per-gate card split from consolidated logician_v2_2_gates.md.*
*Spec card v1.1 — 2026-04-20 — author-family anti-collision extension from EN-003 Cycle 4 C4-NEW-04. Single-gate extension rather than new gate; scope is additive within same failure-code parent.*
