---
id: refine-seed-spec-arch-gap-audit
run_id: 20260618-spec-arch-update-gap-audit
dispatch_id: refine-ups-spec-arch-update-gap-audit-20260618
capability_ref: refine
preset: standard
research: research-if-gap-appears
updatedAt: 2026-06-18
---
# Refine Seed — sync SPEC + ARCHITECTURE to reality, plan next, then a subagent gap-audit

## Target
The studio's canonical docs (SPEC.md, ARCHITECTURE.md) have drifted behind the build (closed loop + two
modes + reversibility shipped & tested). Sync them, produce a next-build plan, then run an **independent
gap-auditor subagent** to find gaps the inline work missed, and fold its findings into the plan.

## Operator intent (verbatim)
"lets update specs and architecture and then create a plan add a sub agent to see if there is more gaps"

## The drift (built but not in SPEC/ARCH)
- **Reversibility, not gating** (DEC-026): control is reversibility; export is the one human-`--confirm` edge.
- **Two modes** (DEC-027): HUMAN-in-the-loop + AUTO exploit/explore cycles (auto-accept under reversibility).
- **New core/CLI surface:** `revert` (append inverse revision), `cycle`, `pending`, `watch`, `preview`
  (+ annotate `/comment` `/state`), `handoff export --confirm`.
- **Tests:** 53 unit + 12 Playwright e2e (incl. blind naive-user + governance falsifiers, mutation-verified).
- **Known UI dead-end:** the browser-only loop ends at annotate; accept/revert are CLI-only (no preview control).
- **Deferred:** UX-constraint fitness (SPEC L5+/OQ-5).

## Source context (local, strong)
SPEC.md (277L), ARCHITECTURE.md (162L), PLAN-CLOSED-LOOP.md (build-status), the built code (run-cycle,
revert-revision, list-pending-comments, studio.ts preview), backend e2e/, the ledger decisions
(DEC-024/025/026/027) + gaps (GAP-CORE-IDENTITY-GATE-010 resolved, OQ-5).

## Write scope
This run folder + SPEC.md + ARCHITECTURE.md (sync to reality) + a new next-build plan
(development/PLAN-NEXT.md). One subagent gap-audit (P11 helper — single, within scope). No code; no public-push.

## Done criteria
SPEC + ARCH reflect the reversibility model, the two modes, the full verb surface, and the test reality, with
the UI dead-end + OQ-5 listed as named gaps/deferrals. A next-build plan (UI accept/revert control first, plus
any subagent-found gaps). A gap-audit report from an independent subagent, its gaps triaged into the plan.

## Validation surface
Dispatch validates (pass). The gap-audit returns a structured gap list; each gap is triaged (in-plan /
deferred / rejected) with a reason — trust-but-verify the subagent's claims against the actual code/docs (P8).

## Preset / research / subagent
standard · research-if-gap-appears · **subagent: recommended** (one gap-auditor; needs operator permission).
