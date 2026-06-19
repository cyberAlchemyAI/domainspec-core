---
id: gap-audit-spec-arch
run_id: 20260618-spec-arch-update-gap-audit
step_id: s8 (independent subagent gap-audit + trust-but-verify)
capability_ref: distill (validate) + 1 gap-auditor subagent
updatedAt: 2026-06-18
---

# Gap-audit — independent subagent + parent verification (P8)

**Subagent:** 1 `gap-auditor` (general-purpose, read-only), agent_id `a9403c5d28449d6e1`, joined, parent_synthesis.
P11 helper (single, within scope) — no ledger dispatch row; reported post-hoc here + in the manifest.
13 findings returned, all file-cited. Parent **trust-but-verified** each HIGH against the actual files.

## Findings + verification + triage

| ID | Sev | Gap | Verified? | Triage |
|----|-----|-----|-----------|--------|
| **F1** | HIGH | HTTP `/handoff/export` route calls `exportDesignHandoff` with **no `--confirm`** — the DEC-026 irreversible edge is bypassable over the network (`0.0.0.0:8787`) | ✅ http-routes.ts:356 + index.ts:23 | **IN-PLAN (P0)** — move the confirm gate INTO the core use-case (gate-in-core, ARCH §4); both CLI+HTTP then enforce it |
| **F2** | HIGH | AUTO `runCycle` auto-accepts with **no `system:auto` actor check** while apply paths reject it (INV-4); code vs SPEC unreconciled | ✅ run-cycle.ts (no guard) vs apply-and-stage.ts:48 | **IN-PLAN (P0, decision)** — reconcile: AUTO is the *sanctioned* auto path under DEC-026; INV-4 scopes to the human apply path. Document in SPEC; reject only `system:auto` literal as a smoke-test |
| **F3** | HIGH | `buildDiffSummary` (counts-from-changeType) still exists + used by legacy `applyApprovedBatch`; SPEC says "deleted/replaced by honest diff" | ✅ apply-approved-batch.ts:129,165 | **IN-PLAN** — SPEC overclaims; downgrade to "two-gate path uses honest diff; legacy `batch apply` is deprecated + counts-only"; optionally delete by routing legacy via honest diff |
| **F4** | HIGH | README:31/67 say "no preview, no `test:e2e`, no in-app preview yet" — all false now (preview+annotate+`/comment`+12 e2e shipped) | ✅ README:31,67 | **IN-PLAN** — README/TESTER-BRIEF/TEST-PROTOCOL doc-sync (queued; outside this run's SPEC/ARCH edit boundary) |
| **F5** | HIGH | `revert --to <revId>` when the target has **no `candidateHtmlHash`** silently restores the **baseline** instead of erroring (wrong-target undo) | ✅ revert-revision.ts:84,104-107 | **IN-PLAN (P1)** — reject with an explicit error when the target carries no committed hash |
| F6 | MED | The two-gate `studio accept` CLI verb has **no e2e**; only AUTO `cycle` auto-accept is e2e-covered | ✅ (e2e greps; only m2-wire unit) | IN-PLAN — folded into the UI-accept-control SWU + its e2e |
| F7 | MED | Legacy HTTP route surface has **zero tests** and lacks the new gates; mounted + network-bound | ✅ (no test refs; index binds) | IN-PLAN (decision) — gate+test to CLI parity OR remove the bootstrap (ARCH calls CLI the surface) |
| F8 | MED | SPEC INV-7 claims notes/prompt are escaped **before persistence**; `captureCommentEvent` only `trim()`s (escaping is at render) | ✅ capture-comment-event.ts:68-130 | IN-PLAN — correct INV-7 to "escaped at render" (accurate) |
| F9 | MED | AUTO fitness = agent self-critique score with **no validation** (ties→first, NaN/missing→0/NaN, gamed score auto-wins) | ✅ run-cycle.ts:126, studio.ts score parse | IN-PLAN — reject NaN/missing; document tie-break; note trust rests on revert |
| F10 | MED | Stop dials (loop_cap/plateau) are **not in the core** — nothing prevents an unbounded auto-accept run | ✅ (self-disclosed in PLAN + cli) | IN-PLAN — add a per-session cycle/budget ceiling in the core |
| F11 | MED | Claim: `synthesize` re-folds the same head comments after a revert | ⚠️ PARTIAL — comments bind to revisionId; after accept/revert head≠rev-0000 so `listComments(head)` orphans them (no double-fold reproduced, but comment-lifecycle-across-head-moves IS underspecified) | IN-PLAN (lower) — spec the comment lifecycle across revisions |
| F12 | LOW | File store: whole-doc rewrite, no lock (last-writer-wins) AND **silent reset to empty on corrupt JSON** (data-loss footgun) | ✅ file-studio-session-store.ts | IN-PLAN (low) — don't swallow parse errors into a reset; document single-writer |
| F13 | LOW | `preview` binds fixed default port 4317, no EADDRINUSE fallback | ✅ studio.ts:186 | IN-PLAN (low) — auto-pick a free port / handle EADDRINUSE |

## Verdict
**0 rejected.** All HIGH verified true; F11 verified *partial* (claim refined, underlying issue real). The audit
surfaced two genuine governance holes I missed (F1 export-over-HTTP, F2 cycle auto-actor) — the highest-value
catches, both invisible to my self-review because I was focused on the CLI seam. F1 is the most serious:
the reversibility model's single human checkpoint is bypassable through a network surface I'd forgotten was wired.

## Receipt (P11 helper, post-hoc)
agents_spawned: [{ agent_id: a9403c5d28449d6e1, role: gap-auditor, status: joined, spawn: ok, close: ok,
residue: none, reroute: none, findings: 13, verified_high: 5/5, rejected: 0 }]
