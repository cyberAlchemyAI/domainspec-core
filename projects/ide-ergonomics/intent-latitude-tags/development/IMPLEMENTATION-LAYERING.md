---
module: intent-latitude-tags
featureCode: ILT
version: current
status: draft
updatedAt: 2026-06-18
docType: implementation-layering
---

# Implementation Layering: Intent-Latitude Tags

## Source Contract

- Transmutation: [../../../../arcanum/transmutations/implementation-layering/SKILL.md](../../../../arcanum/transmutations/implementation-layering/SKILL.md)
- Design: [ARCHITECTURE.md](ARCHITECTURE.md) · Spec: [SPEC.md](SPEC.md)

## Target And Scope

- Target: `intent-latitude-tags` (ILT)
- Scope: feature (a parser + validator), research-only under v2 promotion boundary
- Current state: greenfield

## Layer Boundary Rule

> After this layer, we know whether {decision unlocked}.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| **L0 (POC)** | After this layer, we know whether **grounded `[literal]` enforcement does something a prose header cannot** (refutes the tautology-kill). | Pure `parse(P)` + `checkLiteral(span,O)` run over a fixture set. **No model.** | parser (balance/overlap/nesting/closed-vocab), `[literal]` verbatim check, normalize rule, fixture set with the kill condition | `[goal]`/`[constraint]` enforcement, any LLM-judge, integration into v2 validator, instruction-literal | fixture run: paraphrased literal span → FAIL (true positive); intact → PASS (true negative); **AND** the true-positive fires on outputs a real model actually produces (else RK2 ceremony) | **continue / kill the tag layer** |
| **L1** | After this layer, we know whether the parser + literal check are **repeatable** across realistic prompts/specs and the `[goal]` **exclusion** measurably reduces false verbatim-flags. | `[goal]` exclusion wired; literal check hardened on a larger corpus | goal-span exclusion (mechanical only), expanded fixtures, edge cases (nesting, unicode, whitespace) | judge-based satisfaction, constraint predicates | exclusion reduces false-flags vs untagged baseline; parser handles edge corpus | harden / narrow / stop |
| **L2** | After this layer, we know whether **judge-grounding for `[goal]`/`[constraint]` is acceptable or fails non-tautology (G2 — the central open question).** | A *fixture-validated* `llm-judge` oracle with measured agreement | constraint predicate path, llm-judge oracle, judge-validation harness, FLAG→FAIL promotion rule | scale, packaging | judge agreement on a labelled fixture set ≥ threshold; FLAG-grade documented where it isn't | scale / remediate / **stop (tags stay STRONG-only)** |
| **L3** | After this layer, we know whether ILT can be **wired into the DomainSpec v2 validator** without regressing existing checks. | Integration behind the v2 validator interface | adapter to v2 validator, verdict surfacing, rollout note | broad authoring-UX, fine-tune grounding | integration green on v2 fixtures; no regression | pilot / package / defer |

## Non Regression Guardrails

- L1+ must preserve the L0 STRONG `[literal]` guarantee.
- Deferred scope stays explicit; do not pull judge logic into L0.
- Promotion cites previous-layer evidence, not preference.
- **Complexity note:** L0 is low-complexity (single-file work-pack). Promotion to L1+
  re-evaluates complexity to **medium** (split work-pack, SWU expansion, execution-pack
  required) — see WORK-PACK control fields.

## Recommended Next Layer

- Next layer: **L0**
- Key decision unlocked: does grounded `[literal]` refute the tautology-kill *and* fire on real model output?
- Major deferred scope: all judge-based grounding (L2, G2) — gated behind L0/L1 evidence.
