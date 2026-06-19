---
id: plan-d1-d2-d3
project: ui-prototyping-studio
title: "Execution Plan — D1 (close cycle), D2 (first-principle build), D3 (deliver to humans)"
status: proposal
node_type: implementation-plan
invoke_mode: plan
complexity: medium
source: development/cycle-close-research/findings.md (dispatch 2026-06-17, resolved)
updatedAt: 2026-06-17
---

# Execution Plan — D1 · D2 · D3

Sequences the cycle-close research into executable SWUs. **D1** closes the cycle (3 docs → a safe,
honestly-scoped governance test). **D3** delivers D1 into humans' hands (handoff commit + running the
test + capturing evidence) — it can run *before* D2. **D2** is the genuine build that tests the first
principle (visual ergonomics). One **blocker decision** is surfaced, not decided: the commit policy.

Planning artifact — `[PROPOSAL]`; each SWU runs via a separate `task-session`. Nothing here is executed.

## Standing facts (from the research, do not re-derive)
- Already-deployed: mutation core L0–L2, MR1 register, MW1 two-gate apply/accept + honest od-id diff,
  live operating SKILL, behavior harness. (Kuhn verified against the repo, P8.)
- Everything is **uncommitted** (`DEC-EXT-COMMIT-POLICY-020`); the two-gate chain + live `.claude/` SKILL
  are untracked.
- D1 tests **governance/integrity ergonomics** only; it must NOT claim to test the visual first principle
  (that is D2). Keep the D1 protocol and the D2 onboarding distinct (Wittgenstein owner-boundary).

## Wave / layer map
```
L0  D1 — close the cycle (3 docs)         : D1a README+run-seam · D1b F2 tester brief · D1c test protocol
G   DECISION GATE — commit policy         : DEC-D3-COMMIT (revisit DEC-EXT-COMMIT-POLICY-020)  ← blocker, human
L1  D3 — deliver D1 to humans             : D3a handoff commit (gated) · D3b run the test + capture evidence
L2  D2 — first-principle visual build     : D2a rendered diff core · D2b preview --annotate · D2c onboarding
L3  D2 — deliver + close the ergonomics gap: D3c run the visual test → evidence for GAP-ERGONOMICS-UNPROVEN-001
```
Promotion is by evidence from the prior layer. **D1 → D3-deliver can happen now; D2 follows; do not block D1 on D2.**

## SWU manifest

| SWU | Title | Layer | Depends on | Write scope | Acceptance (one-line) |
|-----|-------|-------|-----------|-------------|-----------------------|
| **D1a** | True README + run-seam + path-print | L0 | — | `README.md`, `backend/src/cli/studio.ts` | a non-author following the README runs a session; `apply`/`register` print the openable `committed/<hash>.html` path |
| **D1b** | Tester-facing F2 disclosure | L0 | — | `TESTER-BRIEF.md` (new) | a short consent brief: agent *can* self-dispose, core won't stop it, spine is the control |
| **D1c** | Governance-scoped test protocol | L0 | D1a | `TEST-PROTOCOL.md` (new) | exact tasks + instructions + feedback capture; scope = governance-not-visual; "fresh STUDIO_DATA per run" |
| **DEC-D3-COMMIT** | Commit-policy decision | G | D1a-c | decision record | `decision-gate` resolves: lift `DEC-020` for a handoff commit, or keep uncommitted |
| **D3a** | Handoff commit freezing D1 | L1 | DEC-D3-COMMIT=allow | git (private parent) | D1 docs + the path-print change committed; resettable/citable baseline (submodule discipline) |
| **D3b** | Run the governance test + capture | L1 | D3a (or D1 if uncommitted ok) | `evidence/` (new) | ≥1 human runs TEST-PROTOCOL.md; feedback captured |
| **D2a** | Rendered honest diff (render core) | L2 | MW1 (done) | new web/render module | the `DiffSummaryHonest` before/after renders visually (build the renderer once) |
| **D2b** | `preview --annotate` surface | L2 | D2a | `backend/src/cli/preview.ts` + overlay asset + ephemeral server | render variant in browser; click-to-annotate → `CommentEvent` with resolved selector (DC-1) |
| **D2c** | Plain-language onboarding | L2 | — | CLI disabled-reasons / step-order surface | a solo cold-start human self-orients to first gate without reading source |
| **D3c** | Run the visual test → ergonomics evidence | L3 | D2a-c, D3b | `evidence/` | ≥1 human runs the visual loop; evidence feeds `GAP-ERGONOMICS-UNPROVEN-001` |

## Per-SWU detail (execution-ready)

### D1a — True README + run-seam + path-print
- **Steps:** rewrite README "Running" to the real path (`cd backend && pnpm install && pnpm studio session open …`; note `STUDIO_DATA`/`STUDIO_DOCS_ROOT`); delete the false root `pnpm install/build/test` block; in `studio.ts`, append the resolved absolute `committed/<hash>.html` (and `staged/<hash>.html`) path to the `apply`/`register`/`accept` output JSON (a `paths` field) so a human can `xdg-open` it.
- **Edge/failure:** README must not reference unbuilt verbs (`preview`); path-print must resolve the real artifact dir (`dirname(STUDIO_DATA)/artifacts/committed`). **Verify:** from a fresh checkout, the README commands run a full loop; `apply` output contains a real openable path.

### D1b — Tester-facing F2 disclosure  `[doc]`
- **Content:** one page — what the studio is; the loop; the **interim risk** (the agent could approve+apply+accept its own in-scope revision; `STUDIO_ACTOR` defaults `cli-user`; the SKILL never-do spine is the sole control; scope fence bounds damage; append-only = reversible); how to watch for it. **Verify:** review against `DEC-F2-IDENTITY-GATE-INTERIM-025` wording; no overclaim.

### D1c — Governance-scoped test protocol  `[doc]`
- **Content:** the exact tester tasks (drive generate→register→baseline→comment→synthesize→approve→apply→accept; try a reject; open the printed `.html`), the instructions, the feedback form (what to capture), and an explicit **scope line: this tests governance/integrity ergonomics, NOT visual ergonomics**. Says "use a fresh `STUDIO_DATA` path per run" (absorbs reset). **Owner-boundary:** do NOT include visual-loop self-orientation (that's D2c). **Verify:** a dry walkthrough produces structured feedback; scope line present.

### DEC-D3-COMMIT — commit-policy decision  `[decision-gate, BLOCKER]`
- **Question:** lift `DEC-EXT-COMMIT-POLICY-020` to allow a handoff commit (so D1 is citable/resettable/deliverable), or keep everything uncommitted? **This is a human decision** — route via `decision-gate`; do not auto-resolve. Submodule discipline applies if "allow" (private parent; the public arcanum handoff is separate).

### D3a — Handoff commit freezing D1  (gated on DEC-D3-COMMIT=allow)
- **Steps:** one scoped commit of the D1 docs + the D1a path-print change in the private parent; follow SUBMODULE-DISCIPLINE (submodule-first if any submodule touched — here it's the parent project). **Verify:** `git status` clean for the D1 scope; the baseline is taggable/resettable.

### D3b — Run the governance test + capture
- **Steps:** hand TESTER-BRIEF.md + TEST-PROTOCOL.md to ≥1 human; they run a fresh-`STUDIO_DATA` session; capture feedback into `evidence/`. **Verify:** ≥1 completed run + captured feedback.

### D2a/D2b/D2c — the first-principle build  `[algorithmic / surface]`
- **D2a render core:** render `DiffSummaryHonest` (per-od-id fragments) as a visual before/after; build the renderer as a shared module (Wittgenstein: one renderer, two surfaces). **D2b preview --annotate:** ephemeral local server serves the rendered variant/diff; click-to-annotate captures `data-od-id` → `CommentEvent` (gated INV-2; DC-1 selector+elementLabel). **D2c onboarding:** CLI disabled-reasons + step order for a solo cold-start human. **Verify:** D2a unit + screenshot-review; D2b e2e click→CommentEvent; D2c a cold-start walkthrough reaches the first gate unaided.

### D3c — Run the visual test → ergonomics evidence
- **Steps:** ≥1 human runs the full visual loop (preview + rendered diff + annotate); capture evidence → `GAP-ERGONOMICS-UNPROVEN-001`. **Verify:** captured visual-ergonomics feedback; the gap moves from unproven toward measured.

## Implementation-layering (value/cost + promotion evidence)
- **L0 (D1):** the honesty/runnability floor — 3 docs + a one-line path-print. Promotion = a fresh-checkout README run + path-print e2e. *Closes the cycle.*
- **L1 (D3-deliver):** D1 in a human's hands. Promotion = the commit decision resolved + ≥1 captured governance-test run.
- **L2 (D2):** the visual build. Promotion = render core unit + preview e2e + onboarding walkthrough.
- **L3 (D2-deliver):** the first-principle evidence. Promotion = captured visual-ergonomics feedback against `GAP-ERGONOMICS-UNPROVEN-001`.

## Validation strategy (per slice)
D1a → fresh-checkout README run + path-print e2e. D1b/D1c → review + dry walkthrough. DEC-D3-COMMIT →
persisted decision record. D3a → scoped `git status` clean. D3b/D3c → captured human feedback. D2a →
unit + screenshot-review. D2b → e2e click→CommentEvent. D2c → cold-start walkthrough.

## Decisions / blockers
- **DEC-D3-COMMIT (blocker):** commit-policy — human decision via `decision-gate` before D3a. The ONLY
  thing gating delivery; D1 authoring + D2 build do not depend on it.

## Next route
`task-session` for **D1a → D1b → D1c** now (no dependency, closes the cycle). Then `decision-gate` for
**DEC-D3-COMMIT**; then `task-session` D3a/D3b. D2 (L2) is a separate build cycle; run after D1 is delivered.
