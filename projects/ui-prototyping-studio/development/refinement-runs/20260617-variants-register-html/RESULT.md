---
id: result-variants-register-html
project: ui-prototyping-studio
title: "RESULT — the missing variants register HTML-ingestion capability"
status: pass
node_type: refinement-result
run_id: 20260617-variants-register-html
dispatch_id: refine-ups-variants-register-html-20260617
capability_ref: refine
updatedAt: 2026-06-17
---

# RESULT — variants register HTML ingestion

## What the missing capability is

A **bridge between two existing, disconnected pieces**: variant metadata (`PrototypeVariant.htmlArtifactRef`)
and the M0b content port (`stageHtml`/`commitHtml`/`readHtml`). Today the stub `generateVariants` writes a
**dangling ref** (no body, no `data-od-id`) and the variant HTML never enters the content store — so
preview, annotation, mutation, and M2 all starve. The fix canonicalizes ingested HTML (M0c), **enforces
`data-od-id` presence**, commits it content-addressed (M0b), and points the ref at real content.

## Decisions

1. **Ingestion interface = Option A** — `studio variants register <sid> --label X --file path` (repeatable);
   the agent writes each variant's HTML to a file then registers it. Won the tournament on agent-ergonomics
   + determinism + minimal scope. `--from <dir>` is optional later sugar. (stdin / manifest rejected.)
2. **`data-od-id` is owned by BOTH the agent (stamps) and the core (validates + rejects)** — the *good
   mirror of F2*. Identity (F2) is structurally unenforceable so it's documentary-only; `data-od-id`
   presence **is** structurally checkable, so the core enforces it as a real admission gate
   (`OD_ID_MISSING`). This upgrades M2 from a documentary Quality-bar line to an enforced check.
3. **`variants generate` (stub) stays** as the testable-surface path; `register` is the real path.
4. **MVP gate is coarse** (≥1 `data-od-id`); per-component granularity is deferred (`GAP-OD-ID-GRANULARITY`).

## Toy-game (falsification)

GOOD (has od-id) → admit + `readHtml(ref)` returns canonical HTML; BAD (no od-id) → `OD_ID_MISSING`, nothing
staged; re-register GOOD → same committed hash (M0b idempotent). The gate fires; registration is deterministic.

## Plan

One SWU **MR1** (`registerVariants` use-case + `OD_ID_MISSING` gate + CLI `--label/--file` + harness M2
closure). All dependencies (M0b, M0c, the ref field) exist; **no F2 dependency; buildable now.** See
`stages/09-plan.md`.

## Stage evidence

- s1 context / s2 define+x-ray: the seam x-ray (stages/05 §1) — pass.
- s3 review: confirmed the capability is wiring + one gate, not new substrate — pass.
- s4 research: no-research — pass.
- s5 distill/tournament: ingestion-interface tournament → Option A (stages/05 §2) — pass.
- s6 design/dialectic: `data-od-id` responsibility → agent-stamps + core-validates (stages/05 §3) — pass.
- s7 design-review: enforcement-honesty consistency (the good mirror of F2) — pass.
- s8 distill-repair/toy-game: GOOD/BAD/idempotent falsification (stages/05 §4) — pass.
- s9 plan: MR1 SWU (stages/09-plan.md) — pass.
- s10 final synthesis: this document — pass.

## Recommended next routes

- `task-session` to build **MR1** (lifts WW2; no F2 needed). Then the first test's M2 becomes exercisable.
- Unchanged: WW3 (install) still waits on the F2 identity-gate decision.
- Deferred: `GAP-OD-ID-GRANULARITY` (per-component od-id requirement); `--from <dir>` sugar.
