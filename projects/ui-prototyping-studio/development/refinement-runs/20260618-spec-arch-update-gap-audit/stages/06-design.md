---
id: design-spec-arch-sync
run_id: 20260618-spec-arch-update-gap-audit
step_id: s2+s5+s6 (drift x-ray + distill + design, consolidated)
capability_ref: invoke+distill (inline)
updatedAt: 2026-06-18
---

# Design — the doc drift, and the minimal sync edits

## §1 Drift x-ray — built vs documented

| Built (code+tests) | SPEC says | ARCH says | Edit |
|---|---|---|---|
| Reversibility, not gating (DEC-026); export the one `--confirm` edge | "human disposes every durable change" (§2, §7) | "human disposes every durable change" (§1, §6, §7) | add an Operating-model-update section to both; note export is the irreversible edge |
| Two modes: HUMAN + AUTO exploit/explore (DEC-027) | absent | absent | document both + the verb surface |
| Verbs: revert/cycle/pending/watch/preview(+annotate,/comment,/state)/export --confirm | only the old list (§2 interaction model) | old loop (§6) | list the real surface |
| 53 unit + 12 e2e (incl. blind + governance falsifiers) | "L1/L2 acceptance" only | — | note the test reality |
| INV-7 escaping is at RENDER, not persistence (F8) | "escaped before persistence" | — | correct to "escaped at render" |
| `buildDiffSummary` still live in legacy apply (F3) | "deletes buildDiffSummary" | "delete buildDiffSummary" | downgrade to: two-gate=honest diff; legacy batch apply=deprecated, counts-only |
| HTTP `/handoff/export` ungated (F1); HTTP surface ungated+untested (F7) | — | "gates live in the core, never the adapter" (§4) — VIOLATED by CLI-only confirm | record the hole + the fix (gate→core) as a named gap + ARCH note |

## §2 Distill — the minimal sync (don't rewrite, correct + append)

Rather than rewrite 277+162 lines, the smallest honest sync is:
1. **Append an "Operating-model update (DEC-026/027)" section** to SPEC and ARCH: reversibility-not-gating, the
   two modes, the real verb surface, the one `--confirm` edge. (Removes the biggest drift in one place.)
2. **Correct the two specific factual overclaims inline:** INV-7 escaping (F8), buildDiffSummary status (F3).
3. **Append a "Known gaps — gap-audit 2026-06-18" table** to both, listing F1–F13 with severity + pointer to
   the run + PLAN-NEXT. (Future readers see the holes where they read the contract.)
4. Everything code-level (F1/F2/F5/F9/F10/F12/F13) + the README cluster (F4) → **PLAN-NEXT**, prioritized.

This keeps owner-boundary (SPEC+ARCH+PLAN-NEXT) and avoids overclaiming a fuller rewrite than evidence supports.

## §3 The reconciliations the sync must state (not hand-wave)
- **F2 / INV-4:** AUTO `cycle` is the *sanctioned* auto-accept path under DEC-026 (reversibility is the control);
  INV-4 "auto-apply forbidden" scopes to the human comment→batch apply path. The SPEC must say this explicitly
  so code≠contract stops reading as a hole.
- **F1 / gate-in-core:** the `--confirm` gate currently lives in the CLI adapter — which ARCH §4 forbids
  ("gates live in the core"). The honest sync records this as a real architecture violation + the fix
  (move confirm into `exportDesignHandoff`), not a gl  oss.
- **The UI dead-end** (prior finding) + F6: the browser loop ends at annotate; accept/revert are CLI-only.
  PLAN-NEXT's first build SWU is the in-preview accept/revert control (governed by the export-confirm edge).
