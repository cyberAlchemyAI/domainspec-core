---
id: ui-prototyping-studio-deep-spec-result
feature: ui-prototyping-studio
title: "Deep-Spec Dispatch Result (ui-prototyping-studio-deep-spec-001)"
status: proposal
node_type: result
dispatch_id: ui-prototyping-studio-deep-spec-001
updatedAt: 2026-06-15
---

# Deep-Spec Dispatch — RESULT

**Dispatch:** `ui-prototyping-studio-deep-spec-001` · **Run:** `wf_ee6ffee8-68a`
**Execution:** 12 subagents · ~838k tokens · 6 phases · `subagent_lifecycle: pass` (all joined + closed)
**Guardrail:** every artifact below is a **proposal**. The canonical SPEC is NOT mutated. Promotion is held behind gate `g8-final-approval` (operator).

## Readiness verdict (s10) — CONDITIONAL

> A one-shot build of **all six UX layers (L0–L6) is not realistic.** A one-shot build of **L0→L2 (the survival/trust floor) is.**

The readiness agent ground-truthed the plan against the repo (`models.ts`, `mock-api.ts`, `apps/web/e2e/`) rather than trusting it:

- **L0 genuinely exists** — the 10-state `StudioSessionState` machine is in `models.ts`; governance enforcement (auto-apply forbidden, approval-before-apply, stale checks) is real in `mock-api.ts`; two real e2e specs exist.
- **L1–L6 are design, not code.** The `FX-*` fixture corpus is a paper design (zero `FX` IDs in `e2e/`); `@axe-core/playwright` is not installed; `mock-api` has no failure-injection or D5/failure states; L4 identity/conformance types (`UIElementIdentity`, `UIVisualSignature`, …) **do not exist** in `models.ts` (`DiffSummary` is just `{added,changed,removed}` counts).
- So **L3–L5 are net-new backend + mock + type builds, not additive increments**, and **L6's ergonomics payoff is unproven and human-study-gated.**

**Recommended next routes (in order):**
1. Scope the realistic one-shot to **L0→L2** only.
2. `decision-gate` on the 4 open questions (OQ-1 trust meter, OQ-2 saw-the-diff proxy, OQ-3 operator-handoff carry/reset, OQ-4 import-integrity MVP boundary) — OQ-3 blocks L5, OQ-1/2 block L6.
3. `task-session` per layer for L3 / L4 / L5 (each co-delivers backend + mock + fixtures).
4. SPEC/invariant calibration pass to fold the 8 proposed invariants (`Inv-1..8`) into the canonical SPEC against authored fixtures.
5. `ux-evidence-validator` calibrate pass to author the `FX-*` corpus and promote the 11 specified-but-unpromoted hard gates.
6. Re-run the s8 naive-user study as an acceptance step after L4/L6.

## Artifacts (all proposals)

| Step | Artifact | What it gives you |
|------|----------|-------------------|
| s0 | `CONTEXT-PACK.md` | Evidence baseline + ergonomics charter + shallow-area questions |
| s1 | `RESEARCH-EVIDENCE-CARDS-token-philosophy.md` | resonant-os-design-tokens philosophy ↔ domainspec Visual DNA |
| s1 | `RESEARCH-EVIDENCE-CARDS-tooling.md` | Web tooling survey, reuse-vs-build verdicts |
| s2 | `LANE-A-NOVEL-DESIGN.md` | Challenger: novel/better directions, pareto-ranked |
| s3 | `LANE-B-DEFENSE.md` | Defender: D-001..D-009 defended; absorb/reject verdicts |
| s4 | `SYNTHESIZED-DEEP-DESIGN.md` | Resolved dialectic — the load-bearing deepened design |
| s5 | `RESIDUALITY-STRESSORS.md` | Stressors → residue → invariants `Inv-1..8`, attractors |
| s6 | `UX-EVIDENCE-REPORT.md` + `UX-FIXTURE-PLAN.md` | Validator-safe checks (L0–L6), fixture corpus |
| s7 | `PLAYWRIGHT-TEST-PLAN.md` | Whole planned-mode test suite (no execution) |
| s8 | `COLD-START-USABILITY-FINDINGS.md` | Context-isolated naive-user friction (genuine cold start) |
| s9 | `DEEP-SPEC-PROPOSAL.md` | Deepened spec resolving the shallow areas |
| s9 | `ONE-SHOT-IMPLEMENTATION-PLAN.md` | Layered, traceable build plan |
| — | `SUBAGENT-LIFECYCLE.json` | AFK-safe closeout ledger (status: pass) |

## Carried residue (must be owned before/at implementation)

R-1 component-registry persistence entity unspecified · R-2 full CommentEvent→MutationTask conflict algebra · R-3 rule-track preference learning (deferred behind D-009) · R-4 enum/token semantic binding stays human-confirmed · R-5 **entire ergonomics floor unproven (L4 proxy / L6 human-study only)** · R-7 TypedReference-pending DNA fields incomplete token mapping · `Inv-1..8` proposed-not-calibrated · OQ-1..4 open decisions · contract drift: `RevisionApplied` vs `RevisionRecorded` state emission.
