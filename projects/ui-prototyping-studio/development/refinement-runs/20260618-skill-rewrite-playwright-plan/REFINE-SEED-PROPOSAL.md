---
id: refine-seed-skill-rewrite-playwright
run_id: 20260618-skill-rewrite-playwright-plan
dispatch_id: refine-ups-skill-rewrite-playwright-20260618
capability_ref: refine
preset: standard
research: research-if-gap-appears
updatedAt: 2026-06-18
---
# Refine Seed — SKILL rewrite (reversibility model) + a Playwright closed-loop test plan

## Target
Two coupled deliverables for the now-built closed loop + two modes:
1. **Rewrite the installed operating contract** `.claude/skills/ui-prototyping-studio/SKILL.md` to the
   reversibility model (DEC-026, DEC-027). The current SKILL encodes the OLD philosophy and now makes a
   FALSE claim.
2. **Plan a Playwright e2e test** for the closed loop (HUMAN + AUTO modes) over the preview HTTP surface.

## Operator intent (verbatim)
"skill rewrite and plan a test with playwright"

## The conflict to resolve (SKILL)
The SKILL's spine is **"You propose. The human disposes."** — accept/baseline/approve/export are ALL
"human gates", `studio accept` is tagged **"Never call this"**, and the never-do spine is "the only thing
that holds the line; the core cannot tell you apart from the human" (the F2 identity gate). But:
- **DEC-026** dropped the identity gate — control is **reversibility, not gating**.
- **DEC-027** shipped **AUTO mode**: the agent auto-accepts (reversible via `studio revert`, visible in preview).
So the SKILL is both philosophically stale AND factually wrong (it forbids what AUTO now does). The rewrite
must reconcile: HUMAN mode (human accepts — a workflow choice) vs AUTO mode (agent auto-accepts — safe because
reversible); the ONE human-required edge becomes **export** (`handoff export --confirm`, the irreversible edge).

## Source context (local, strong)
- The current SKILL.md (12-step loop, propose/dispose table, never-do spine, F-CRIT-1 honest authority note).
- DEC-REVERSIBILITY-NOT-GATING-026 + DEC-AUTO-BUILD-027 (ledger).
- The BUILT surface: studio.ts (apply/accept/discard/revert/cycle/pending/watch/preview annotate+/comment+/state),
  run-cycle.ts, revert-revision.ts, list-pending-comments.ts. PLAN-CLOSED-LOOP build-status block.
- Existing Playwright material: development/deep-spec-dispatch/PLAYWRIGHT-TEST-PLAN.md + UX-FIXTURE-PLAN.md;
  the `ux-evidence-validator` skill (validator-safe Playwright checks). No Playwright is wired yet (no e2e dir).

## Write scope
This run folder + a rewritten `.claude/skills/ui-prototyping-studio/SKILL.md` + a new
`development/PLAYWRIGHT-CLOSED-LOOP-TEST-PLAN.md`. No test code executed (plan only). No public-push.

## Done criteria
- SKILL rewritten: reversibility posture, the two modes + who-leads-when, accept reframed (HUMAN vs AUTO),
  export as the one human-confirmed irreversible edge, the never-do spine rewritten (never export without
  confirm; never bypass the scope fence; always leave a revertible, honestly-diffed trail), false "never
  accept" claim removed, the new verbs (revert/cycle/pending/watch/annotate) documented.
- Playwright plan: e2e over the preview server — annotate click→comment→pending→synthesize→stage→accept→
  revert→export-confirm, both modes, plus a GOVERNANCE falsification test (export-without-confirm must FAIL;
  revert must restore; auto-accept must be revertible). Fixtures, selectors, runner wiring, validator-safety.

## Validation surface
Dispatch validates (pass). Toy-game: the planned governance test actually catches a violation (a test that
would FAIL if export proceeded without --confirm, and if revert didn't restore the prior HTML).

## Preset / research
standard · research-if-gap-appears (Playwright + the local ux-evidence-validator are known; no external expected).
