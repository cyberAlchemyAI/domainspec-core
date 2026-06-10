# Refine Result: Infra-Spec Research Strategy

- **Target:** `ops/development/infra-spec-research-strategy.dispatch.json` + `infra-spec-research-strategy.md` (the existing 7-lane research route toward a future `infra-spec` capability)
- **Status:** **pass**
- **Preset:** full
- **Research:** research-if-gap-appears (no external research run; one local gap recorded)
- **Run manifest:** `ops/development/refinement-runs/2026-06-08-infra-spec-research-strategy/RUN-MANIFEST.md`
- **Evidence index:** `…/evidence-index.json`
- **Seed proposal:** `…/REFINE-SEED-PROPOSAL.md`
- **Dispatch route (this run):** `…/REFINE-DISPATCH.json` (validated `pass`)
- **Runtime handoff:** `…/RUNTIME-HANDOFF.md`

## Dispatch strategy

- Selected overlays: `baseline_sequence`, `route_menu_for_ambiguity`, `dialectic_for_tension`, `tournament_for_alternatives`, `memory_residue_for_context_recovery` (xray / toy_game / protected_context recorded as not-selected with reasons).
- Subagent strategy: `recommended` → operator authorized "Run with subagents" → 3 role-bound reviewers executed (fanout → parent_synthesis). Authorization: granted.

## Headline outcome

The strategy was well-designed but **failed the dispatch validator it requires of itself**, and its self-test command pointed at an uninitialized submodule. Three surgical, verified improvements were applied; all original lane design was preserved.

| # | Improvement | Before | After | Verified by |
| --- | --- | --- | --- | --- |
| B1 | Dispatch passes the native validator | `VALIDATION=block` (receipt fields + 4 capability flags) | `VALIDATION=pass` | `validate-dispatch.py` on canonical path |
| B2 | Self-test command is runnable | pointed at empty `arcanum/` submodule | points at `.claude/skills/dispatch-spec/scripts/validate-dispatch.py` | path exists; produced the pass |
| B3 | Scope is unambiguous | infra-spec conflatable with runtime-surface convergence | added "Scope Boundary" section | reviewer + parent both conflated it pre-fix |
| B4 | No design regression | — | lanes/gates/guardrails byte-identical | semantic diff: "everything-else identical: True" |

## Stage evidence

- Context Builder evidence baseline: **pass** (re-baselined after target correction)
- Invoke Define: **pass** (re-baselined)
- Interrogation refine-review: **flag** (MVP-first demoted to residue) → proceed
- Research decision: **pass** (no external research; local gap recorded)
- Distill: **pass** (selected "validity-and-clarity repair" over lane-rewrite / document-only)
- Invoke Redefine / Design: **pass** (surgical, pre-verified to validate)
- Interrogation refine-design-review: **pass**
- Distill Repair: **pass** (T1–T6)
- Invoke Plan + Emit: **pass** (promoted + `.md` patched)
- Final Interrogation and Synthesis: **pass**

## Subagent receipts

- `dispatch-route-reviewer` — **pass-with-findings**; *corrected the parent's target mis-resolution* by reading the real artifacts.
- `owner-boundary-and-evidence-reviewer` — **pass**; confirmed the write scope is in-bounds.
- `convergence-tension-reviewer` — **flag (scope drift)**; drifted to the adjacent runtime-surface program; quarantined and repurposed as evidence for B3.
- Full receipts: `…/stages/subagent-receipts.md`.

## Honest note on process

This run initially **mis-resolved the target** as the `ops/` runtime-surface convergence program (the file appeared absent until the branch was fast-forwarded). A delegated reviewer caught it; the run was re-baselined to the true target. The mistake is recorded in Stage 01 rather than hidden — and it directly motivated improvement B3.

## Final synthesis

The infra-spec research strategy moved from *non-executable as specified* to *valid, runnable, and unambiguous*, with its strong original design fully preserved. The artifacts are ready for their own next route (read-only fan-out execution).

## Recommended next routes (not executed)

1. `task-session` (read-only) — execute the strategy's MVP-first first pass: lanes **L1 (cartographer) + L2 (Lean translator) + L7 (gap hunter)**.
2. Operator decision on **B-opt** — adopt MVP-first ordering into the route, or run the full 7-lane fan-out as written.
3. `git submodule update --init arcanum` — clear the local gap before any deep Lean-formalization linkage.

## Residue

- B-opt MVP-first ordering (unforced recommendation).
- `arcanum/` submodule uninitialized (local gap, owner = fan-out executor).
- Runtime-surface convergence tension ledger (out-of-target; belongs to that program's own refinement).
