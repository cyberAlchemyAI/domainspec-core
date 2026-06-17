---
id: ui-prototyping-studio-decision-gate-2026-06-16
project: ui-prototyping-studio
title: "Decision Gate — 2026-06-16 (close open blockers + separate research)"
status: PASS
node_type: decision-record
updatedAt: 2026-06-16
---

# Decision Gate — 2026-06-16

**Result: PASS** — no open or blocking decisions remain. Source: operator choices via the
decision-gate ask interface (all recommended options selected). Canonical decision store is
`.craft/ledger.yml`; this is the reviewable summary.

## Resolved (closed)

| Decision | Selected | Why |
|---|---|---|
| **DEC-ONE-SHOT-SCOPE-002** | **L0→L2 survival/trust floor** | Deep-spec verdict + C-1 spike proved L0→L2's hardest piece (the V3 fence) buildable; L3–L6 are net-new and deferred. |
| **DEC-OQ1-TRUST-METER** | **No trust meter in MVP; question → UX research track** | Not armchair-decidable; plan forbids shipping unvalidated. |
| **DEC-OQ2-SAW-DIFF** | **The accept-diff gate is the proxy** | Resolved by `DEC-MUTATION-EXEC-015`: accept-diff previews `DiffSummaryHonest` and commits exactly the previewed `candidateHtmlHash` (seen==recorded). "Felt" non-theater validation folds into the L6 ergonomics research. |
| **DEC-R2-CSS-ATTRIBUTION-017** | **Separate as a focused spike** | Decide R2-a vs R2-b with evidence (cascade/specificity + node identity), not blind; doesn't block L0. |

## Deferred (recorded, not blocking)

| Decision | Disposition | Trigger to revisit |
|---|---|---|
| **DEC-OQ3-HANDOFF-CARRY** | Moot in MVP — no session-scoped tuning until L5 | When L5 preference-learning is designed |
| **DEC-OQ4-IMPORT-INTEGRITY** | Post-MVP hardening | Within-session forge already caught by `frozenBaselineBinding`; cross-import is later |

## Separated research tracks (the "suggest separated research")

1. **UX / ergonomics research** — `GAP-ERGONOMICS-UNPROVEN-001` + OQ-1 (trust meter) + the non-theater "felt" half of OQ-2. A human-study/usability investigation; outputs feed L6. *The honest home for "does this actually improve human work" — the first principle, still unmeasured.*
2. **CSS-attribution & node-identity spike** — `GAP-V3-NODE-IDENTITY-008` + `DEC-R2-CSS-ATTRIBUTION-017`. A pre-registered spike (like C-1) on cascade/specificity and reordering-robust node identity; decides R2-a vs R2-b with evidence.

## Effect

No decision blocks the build. **Next:** `task-session` L0 (schema + artifact content port + canonicalizer) → L1 (V3 fence). The two research tracks run in parallel and are *not* on the L0→L2 critical path.
