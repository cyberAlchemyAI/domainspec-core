---
module: intent-latitude-tags
featureCode: ILT
version: current
status: draft
updatedAt: 2026-06-18T08:02:30.000Z
docType: work-pack
---

# WORK-PACK: intent-latitude-tags

## Purpose

Canonical executable plan for the **L0 PoC** of Intent-Latitude Tags: prove (or
kill) that grounded `[literal]` enforcement does something a prose header cannot.
Single-file because the active layer is low-complexity; L1–L3 stay deferred in
[IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md).

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | L0 has no blocker affecting acceptance |
| complexity | low | active layer = L0 only; L1+ re-evaluates to medium |
| outputMode | single-file | split required when promoted to L1+ |
| executionPackRef | n/a | required at L1+ medium |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | |
| activeLayerWindow | L0 | |
| lastUpdatedAt | 2026-06-18T08:02:30.000Z | |
| readinessProfile | pilot | research PoC, promotion-gated |

## Objective Summary

- Objective: implement the pure parser + `[literal]` verbatim checker and run them
  over a fixture set whose pass/fail **is** the L0 kill condition.
- Primary inputs: [SPEC.md](SPEC.md), [ARCHITECTURE.md](ARCHITECTURE.md) §6 interfaces, [../SPEC.md](../SPEC.md) §4.0–4.1.
- Success condition: paraphrased literal span → FAIL; intact → PASS; and the
  true-positive fires on output a real model actually produces. Failure of the last
  clause = **kill the tag layer** (a successful, cheap negative).

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Pure parser with author-time rejection | L0 | W0 | none | unit tests on balance/overlap/nesting/unknown-tag |
| S-002 | `[literal]` verbatim checker + normalize | L0 | W0 | S-001 | unit tests: TP paraphrase→FAIL, TN intact→PASS |
| S-003 | Fixture set + runner encoding the kill condition | L0 | W0 | S-002 | runner green on fixtures; manual real-model spot check |

## Compact Layer Mapping

All three slices are **L0**. They answer one layer question: *does grounded
`[literal]` refute the tautology-kill?* Promotion evidence created = the fixture
run + the real-model spot check. L1–L3 are not decomposed here (deferred per
layering artifact; decomposing them before L0 evidence is the ceremony we are
avoiding).

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-PARSE | Pure tag parser + author-time errors | L0 | low | W0 | [SPEC.md](SPEC.md#parse-tagged-prompt-inline), [../SPEC.md](../SPEC.md) §4.0 | ready | not-started |
| TASK-LITERAL | `[literal]` verbatim check + normalize | L0 | low | W0 | [SPEC.md](SPEC.md#enforce-literal-span-inline), [../SPEC.md](../SPEC.md) §4.1 | ready | not-started |
| TASK-FIXTURES | Fixture set + runner with kill condition | L0 | low | W0 | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) L0 exit evidence | ready | not-started |
| TASK-VERIFY | L0 decision: continue or kill | L0 | low | W0 | this work-pack objective | ready-after-implementation | not-started |

## Implementation Detail (inline — low complexity)

### TASK-PARSE
- Purpose: turn prompt text `P` into `TaggedSpan[]` or a `ParseError`.
- Inputs: `P: string`. Outputs: `TaggedSpan[] | ParseError`.
- State: none (pure).
- Algorithm: scan for `[tag]…[/tag]` where `tag ∈ {literal,goal,constraint}`; record `{tag, id?, text, start, end}`; maintain an open-tag stack.
- Rules: reject on (a) unbalanced open/close, (b) overlap, (c) nesting other than `literal` inside `goal`/`constraint`, (d) unknown tag name. Optional `id="…"` captured.
- Edge cases: empty span; adjacent tags; escaped brackets (decide: literal `[` outside a tag is plain text); nested same-tag (reject).
- Failure modes: `ParseError{reason, offset}` — author-time, before any model run.
- Acceptance: unit tests cover each rejection + a valid multi-tag parse.

### TASK-LITERAL
- Purpose: decide whether a `[literal]` span survived verbatim in output `O`.
- Inputs: `span: TaggedSpan`, `O: string`. Outputs: `Finding{tag:literal, id, result, strength:strong, rationale}`.
- Algorithm: `normalize(span.text)` contiguous-substring-of `normalize(O)` ? PASS : FAIL.
- `normalize`: collapse internal whitespace runs → single space; trim; NFC unicode. **Declared once, deterministic.**
- Edge cases: case sensitivity (default: case-sensitive — legal text); punctuation; the disclaimer worked example from ../SPEC.md §2.
- Failure modes: none beyond FAIL finding; pure.
- Acceptance: TP (paraphrase) → FAIL; TN (intact, whitespace-variant) → PASS.

### TASK-FIXTURES
- Purpose: encode the L0 kill condition as runnable cases.
- Inputs: fixture files `{prompt, output, expected}`. Outputs: runner report.
- Cases (minimum): (1) intact disclaimer → PASS; (2) paraphrased disclaimer → FAIL; (3) whitespace/unicode variant intact → PASS; (4) parser-rejection cases.
- Real-model clause: at least one fixture's `output` is captured from an actual model run on the tagged prompt, to test RK2 (does the check ever fire in practice).
- Acceptance: runner green; the real-model case documented with which model + date.

## Smallest Working Units

SWU IDs: `SWU-ILT-NNN`. Each maps to one parent task.

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-ILT-001 | TASK-PARSE | [../SPEC.md](../SPEC.md) §2,§4.0; [SPEC.md](SPEC.md) R1 | ARCHITECTURE §6 parser iface | none | parser module + its unit test | parse returns spans for valid input, ParseError for each illegal case | test file green | test runner | subagent | ready |
| SWU-ILT-002 | TASK-LITERAL | [../SPEC.md](../SPEC.md) §4.1 | ARCHITECTURE §6 literal checker | SWU-ILT-001 | literal-checker module + unit test | TP→FAIL, TN→PASS incl. whitespace/unicode variants | test file green | test runner | subagent | ready |
| SWU-ILT-003 | TASK-FIXTURES | IMPLEMENTATION-LAYERING L0 exit evidence | the disclaimer worked example (../SPEC.md §2) | SWU-ILT-002 | fixtures dir + runner | runner green on cases 1–4; ≥1 real-model output captured | runner report + recorded model/date | runner command | local-fallback | ready |
| SWU-ILT-004 | TASK-VERIFY | this WORK-PACK Objective | FINDINGS tautology-kill | SWU-ILT-003 | a short L0-DECISION note | states continue-or-kill with the fixture evidence | decision note committed | review | manual | ready |

Expected subagent result shape per SWU follows plan.md (`swu_id … handoff_note`).

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| (none for L0) | — | G2 (judge grounding) is an L2 concern, not an L0 blocker | — | revisit at L1→L2 promotion | — |

## Validation Strategy

- Per slice: unit tests (S-001, S-002) + fixture runner (S-003) + decision note (TASK-VERIFY).
- L0 gate: the kill condition in the Objective. A clean kill is a successful close.
- No mutation of v1 templates/validators (promotion boundary).

## Gate Checks

1. workPackGateStatus = pass before any execution. ✔ (L0 has no acceptance blocker)
2. Medium/high execution-pack: n/a at L0.
3. Layer mappings consistent with layering artifact deferred scope. ✔
4. No unresolved blocker affecting L0 acceptance. ✔
5. Every SWU has parent task, write scope, done criteria, acceptance evidence, validation surface, owner. ✔
6. TASK-VERIFY uses the `VERIFY` closure exemption (no source mutation).

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-18 | Initial L0 work-pack from invoke plan | invoke (vrondelli) |
