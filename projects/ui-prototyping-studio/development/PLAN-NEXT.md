---
id: plan-next
project: ui-prototyping-studio
title: "PLAN-NEXT — close the gap-audit findings + the UI dead-end"
status: proposal
node_type: implementation-plan
source: refinement-runs/20260618-spec-arch-update-gap-audit
updatedAt: 2026-06-18
---

# PLAN-NEXT — post-build hardening + the visual loop

> **BUILD STATUS — 2026-06-18: whole work pack EXECUTED.** N1–N11 done (N8 doc-only via the SPEC/ARCH sync;
> N9 via a no-double-fold test + note). Unit **61/61**, Playwright e2e **13/13**, `tsc` clean.
> - **N1** ✅ export-confirm moved INTO `exportDesignHandoff` (core) — CLI + HTTP both refuse unconfirmed; fastify-inject test proves the network door is closed (F1).
> - **N2** ✅ HTTP surface kept; the critical export route is now gated (N1) + tested. (No removal — conservative default.)
> - **N3** ✅ in-preview **Accept / Discard / Revert** buttons + `POST /accept|/discard|/revert`; export stays button-less terminal `--confirm`. Closes the UI dead-end; blind ceiling test flipped; new `preview-accept` e2e.
> - **N4** ✅ `revert --to` with no committed content now errors (F5).
> - **N5** ✅ README / TESTER-BRIEF / TEST-PROTOCOL synced (preview/annotate/cycle/e2e shipped).
> - **N6** ✅ non-finite cycle scores rejected (`CYCLE_SCORE_INVALID`); tie-break documented (F9).
> - **N7** ✅ core cycle ceiling (`CYCLE_CEILING_REACHED`, default 25) — termination enforced in the core, not just the agent loop (F10).
> - **N8** ✅ INV-7 + buildDiffSummary overclaims corrected in SPEC/ARCH (no risky code deletion).
> - **N9** ✅ no-double-fold property tested; comment-lifecycle noted (F11).
> - **N10** ✅ corrupt data file now errors instead of silently resetting (F12).
> - **N11** ✅ preview auto-picks a free port + handles bind errors (F13).


Non-executed. Sourced from the 2026-06-18 gap-audit (independent subagent, all HIGH trust-but-verified) +
the prior UI dead-end finding. Each SWU is a `task-session`. Priority: governance holes first (they break the
reversibility model's one promise), then the visual loop, then accuracy + soundness, then low.

## P0 — governance holes (the reversibility model's single promise is currently bypassable)

| SWU | Title | Gap | Write scope | Acceptance |
|-----|-------|-----|-------------|------------|
| **N1** | Move the export-confirm gate INTO the core | F1 | `application/export-design-handoff.ts` (require an explicit `confirmedBy`/`confirm` arg; throw `HANDOFF_CONFIRMATION_REQUIRED` without it); CLI passes it from `--confirm`; HTTP route must pass it too | the Fastify `/handoff/export` route refuses without confirmation **at the use-case level**; an e2e/unit proves both CLI and HTTP refuse unconfirmed (gate-in-core, ARCH §4) |
| **N2** | Decide the legacy HTTP surface | F7 | `src/index.ts` + `interface/http-routes.ts` | a recorded decision: either (a) bring every mutating route to CLI gate-parity + add route tests, or (b) remove the bootstrap (CLI is the surface). No ungated, untested, network-bound mutation path remains |

## P1 — the visual loop + correctness

| SWU | Title | Gap | Write scope | Acceptance |
|-----|-------|-----|-------------|------------|
| **N3** | In-preview Accept / Revert control | UI dead-end, F6 | `studio.ts` preview: an "Accept" + "Revert" button on the staged section → `POST /accept`, `POST /revert` (same use-cases); CL4 poll refreshes | a browser-only user completes the loop (annotate→…→accept→revert) without a terminal; export still needs `--confirm`; the blind-test ceiling assertion flips to "button works"; e2e covers it |
| **N4** | Revert wrong-target fix | F5 | `revert-revision.ts` | `revert --to <rev>` where the target has no `candidateHtmlHash` throws an explicit error (not a silent baseline restore); unit test |

## P2 — accuracy + AUTO soundness

| SWU | Title | Gap | Write scope | Acceptance |
|-----|-------|-----|-------------|------------|
| **N5** | Doc-sync the tester cluster | F4 | README.md, TESTER-BRIEF.md, TEST-PROTOCOL.md | the preview/annotate surface, AUTO `cycle`/`watch`, and `test:e2e` are documented; no "no preview yet" claims remain |
| **N6** | Validate AUTO fitness scores | F9 | `run-cycle.ts` + CLI score parse | reject NaN/missing scores (`CYCLE_SCORE_INVALID`); tie-break documented (first-seen); a test |
| **N7** | Core cycle ceiling | F10 | `run-cycle.ts` / session state | a per-session cycle/budget ceiling enforced in the core (not only the agent `/loop`); exceeding it refuses; test |
| **N8** | INV-7 + buildDiffSummary | F3, F8 | (mostly done in SPEC sync) optionally delete `buildDiffSummary` by routing legacy apply through the honest diff | no counts-only path remains, OR the deprecation is explicit + tested |
| **N9** | Comment lifecycle across head moves | F11 | `domain`/`synthesize`/`pending` + SPEC | define + enforce what happens to head comments after accept/revert (carry-forward vs resolve); test the no-double-fold property |

## P3 — low (footguns)

| SWU | Title | Gap | Acceptance |
|-----|-------|-----|------------|
| **N10** | File-store safety | F12 | corrupt JSON does NOT silently reset to empty (error instead); single-writer assumption documented |
| **N11** | Preview port resilience | F13 | `preview` auto-selects a free port / handles `EADDRINUSE` gracefully |

## Validation strategy
Each SWU lands with a unit and/or e2e test. The governance SWUs (N1) extend the **governance falsifier**
suite — the export-confirm e2e must now also cover the HTTP path. Backend unit (53) + e2e (12) stay green;
the count grows with N1/N3/N4/N6/N7.

## Sequence
`task-session`: **N1 → N2** (close the holes) → **N3 → N4** (visual loop + revert fix) → N5–N9 (accuracy +
soundness) → N10–N11 (low). N1 is the keystone — until it lands, the reversibility model's single human
checkpoint is bypassable over HTTP.

## Provenance
All findings: `refinement-runs/20260618-spec-arch-update-gap-audit/stages/08-gap-audit.md` (independent
gap-auditor subagent, parent trust-but-verified, 0 rejected, 5/5 HIGH confirmed).
