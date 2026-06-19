---
id: result-spec-arch-gap-audit
project: ui-prototyping-studio
title: "RESULT — SPEC+ARCH synced to reality + independent gap-audit + PLAN-NEXT"
status: pass
node_type: refinement-result
run_id: 20260618-spec-arch-update-gap-audit
dispatch_id: refine-ups-spec-arch-update-gap-audit-20260618
capability_ref: refine
updatedAt: 2026-06-18
---

# RESULT — docs synced, gaps found by an independent agent, plan written

## Answer
SPEC.md + ARCHITECTURE.md synced to the built reality (reversibility model, two modes, real verb surface,
test reality), two factual overclaims corrected, and a known-gaps table embedded in both. An independent
gap-auditor subagent swept the whole studio; all HIGH findings were trust-but-verified true; everything is
triaged into PLAN-NEXT.md.

## Doc sync (SPEC + ARCH)
- Appended an **Operating-model update (DEC-026/027)** section to both: reversibility-not-gating, the two
  modes, the full runnable verb surface, the one `--confirm` edge, the 53 unit + 12 e2e reality.
- **Corrected overclaims:** INV-7 escaping is at render not persistence (F8); `buildDiffSummary` is NOT
  deleted — the two-gate path is honest, the legacy `batch apply` is deprecated/counts-only (F3).
- **Reconciled F2:** AUTO `cycle` is the sanctioned auto-accept path under DEC-026; INV-4 scopes to the human
  apply path — so code≠contract no longer reads as a hole.
- Embedded a **Known-gaps table** (F1–F13 + the UI dead-end) in SPEC §2b and ARCH §6c, pointing to PLAN-NEXT.

## Independent gap-audit (the subagent)
1 `gap-auditor` (read-only, agent_id a9403c5d28449d6e1), 13 file-cited findings, **0 rejected**. Parent
trust-but-verified all 5 HIGH against the files (P8):
- **F1 (HIGH, verified):** HTTP `/handoff/export` bypasses the `--confirm` edge — the reversibility model's
  single human checkpoint is reachable over `0.0.0.0:8787` with no confirm. The highest-value catch; I missed
  it because I was focused on the CLI seam. → PLAN-NEXT N1 (move the gate into the core use-case).
- **F2 (HIGH, verified):** `cycle` auto-accepts with no `system:auto` guard vs INV-4 → reconciled in the docs.
- **F3/F4/F5 (HIGH, verified):** buildDiffSummary drift; README says "no preview/e2e yet"; `revert --to` with
  no hash silently restores baseline. → corrected / queued / N4.
- F6–F13 (MED/LOW, verified; F11 partial) → triaged into PLAN-NEXT.

## Plan
`development/PLAN-NEXT.md` — P0 governance holes (N1 export-gate-to-core, N2 HTTP-surface decision) → P1
visual loop + revert fix (N3 in-preview Accept/Revert control — closes the UI dead-end; N4) → P2 accuracy +
AUTO soundness (N5–N9) → P3 low (N10–N11). N1 is the keystone.

## Stage evidence
s1–s10 pass (drift x-ray + sync design in stages/06-design.md; the subagent audit + verification + triage in
stages/08-gap-audit.md; SPEC/ARCH edits + PLAN-NEXT are the plan outputs). Research: research-if-gap — none.
Subagent: 1 gap-auditor, joined, parent_synthesis, 0 rejected (P11 helper; receipt in stages/08).

## Residue
README/TESTER cluster (F4) is queued in PLAN-NEXT N5, deliberately outside this run's SPEC/ARCH edit boundary.
The deepest catch (F1) means a governance fix should land before any deployment that mounts the HTTP server.

## Recommended next routes
`task-session`: **N1 → N2** (close the holes), then **N3** (the visual loop). The MAKE-MVP DOC public-republish
should wait until N1 + N5 land (the public docs would otherwise carry the export-over-HTTP hole + stale claims).
