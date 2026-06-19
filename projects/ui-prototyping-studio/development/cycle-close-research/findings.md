---
id: cycle-close-research-findings
project: ui-prototyping-studio
title: "Findings — necessary changes to close the cycle + deliver a human-testable thing"
dispatch_id: 2026-06-17-ups-cycle-close-research
node_type: research-findings
updatedAt: 2026-06-17
---

# Findings — close the cycle, deliver something humans can test

**One-line answer to the goal:** the studio's loop is *runnable* today but not *deliverable* — close
the cycle with a small, mostly-clerical **Deliverable 1** (a safe, repeatable, agent-mediated CLI test
of governance + integrity ergonomics), and stage the **first-principle visual test (Deliverable 2:
preview + rendered diff)** as the next, genuinely-build-heavy step. preview is *not* needed to test the
gates; it *is* needed to test the project's headline claim.

## The crux the dispatch resolved (claim ≤ proof)

"Open `committed/<hash>.html`" is a faithful **visibility floor** — verified: the content store writes
HTML verbatim and the fixtures are self-contained single-file (Goldratt R2). But it is **not** the gated
"saw-the-diff" (the diff at the approval moment), which a textual/JSON diff turns into a *modality-lie*
(Alexander R2). So: a CLI test credibly witnesses the **integrity floor + governance ergonomics**; it
**cannot** witness the **first-principle visual ergonomics**. Those are two deliverables, not one.

## Verdict matrix

| Candidate change | already-built? (precedent) | needed for a human test? (witness) | distinct? | verdict | deliverable |
|---|---|---|---|---|---|
| Mutation core L0–L2 (schema/port/canon/V3 fence/two-gate machine) | YES (ART-M0*/M1/M2) | n/a | — | **already-deployed** | — |
| `variants register` real HTML + `OD_ID_MISSING` | YES (MR1) | n/a | — | **already-deployed** | — |
| two-gate `apply/accept/discard` + honest od-id diff (DATA) | YES (MW1) | n/a | — | **already-deployed** | — |
| operating SKILL installed + behavior harness | YES (WW3) | n/a | — | **already-deployed** | — |
| **Fix the FALSE README + run-seam** (print the committed `.html` path) | NO | a non-author **cannot run anything**; every README run line is false | distinct | **build-needed** | **D1 / P0** · *src: Goldratt R1/R2 + Grove R1/R2; Kuhn confirmed* |
| **Tester-facing F2 self-disposal disclosure** | NO (only agent-facing SKILL + ledger) | tester cannot give informed consent; agent can self-dispose, core won't stop it | distinct | **build-needed** | **D1 / P0** · *src: Grove R1/R2; Kuhn confirmed* |
| **Test protocol** (task list + feedback capture; scope-disclosed governance-not-visual) | NO (harness validates the SKILL, not humans) | nothing to hand a tester; only path to ergonomics evidence (`GAP-ERGONOMICS-UNPROVEN-001`) | distinct | **build-needed** | **D1 / P0** · *src: Grove R1/R2; Wittgenstein distinct-from-harness* |
| **Reset between runs** | mechanism exists (STUDIO_DATA) | **DEMOTED (Popper):** a fresh `STUDIO_DATA=/tmp/run-N` path isolates fully (artifacts live under `dirname(STUDIO_DATA)`) → zero-code; protocol just says "fresh path per run" | distinct | **nice-to-have** | D1 optional |
| **One handoff commit** freezing D1 | NO (all uncommitted, DEC-020) | **DEMOTED (Popper):** no act a *tester* performs needs it — it's the *deliverer's* handoff/citation workflow | distinct (policy) | **delivery-hygiene (human decision)** | delivery precondition, not a test blocker |
| **Rendered honest diff at the approval gate** | partial (data exists; surface no) | the "saw-the-diff" gate is a modality-lie without it — irreducible | distinct | **build-needed** | **D2 / P1** · *src: Alexander R2 (held through confrontation)* |
| **`preview --annotate`** (render + click-to-annotate → resolved selector) | NO (SKILL flags not-built) | naive user can't hand-author selectors; the annotation loop is unusable | distinct | **build-needed** | **D2 / P1** · *src: Alexander R1/R2 + cold-start findings* |
| **Plain-language onboarding** (CLI disabled-reasons / step order) | partial (agent narration duty only) | solo cold-start human can't self-orient | distinct | **build-needed** | **D2 / P1** · *src: Alexander R2 (boundary vs P0-3 per Wittgenstein)* |
| "Render a variant" surface | — | satisfied by open-the-file for self-contained HTML (contingent) | collapses into open-the-file | **collapsed → nice-to-have** | — |
| e2e Playwright (SWU-E) | NO | protects CI, not a human test | distinct | **not-needed this cycle** | defer |
| M3 recorder atomicity/rollback | NO | durability hardening; happy/reject paths don't hit it | distinct | **not-needed this cycle** | defer |
| F2 core identity gate (code) | NO (interim accepted, DEC-025) | spine + disclosure cover it for a supervised test | distinct | **not-needed this cycle** | defer |
| Full SWU-Z workspace | NO | subsumed by the run-seam fix for D1 | partial overlap | **not-needed (minimal subset only)** | D1 covers the seam |

## The prioritized necessary-changes list

### Deliverable 1 — "humans can safely, repeatably test the loop" — the P0 floor is THREE docs (post-skeptic)
- **P0-1** True README + run-seam: replace the false `pnpm install/build/test` block with what runs today (`cd backend && pnpm install && pnpm studio …`); print the resolved `committed/<hash>.html` path in `apply`/`register` output so a human can open it. *(Wittgenstein: the README-fix + path-print collapse into this one change.)*
- **P0-2** Tester-facing **F2 disclosure**: a short brief — the agent *can* approve+apply+accept its own revision and the core won't stop it (`STUDIO_ACTOR` defaults `cli-user`); the SKILL spine is the control. Informed consent.
- **P0-3** **Test protocol**: the exact tasks a human runs, the instructions they get, the feedback captured — explicitly scoped as *governance/integrity* ergonomics, NOT visual (else it overclaims). The only channel to evidence for the unproven ergonomics floor. The protocol just says "use a fresh `STUDIO_DATA` path per run" (absorbs reset).

**All three are documents** (one of them adds a one-line path-print to the CLI). No new scripts strictly required.

### Delivery-hygiene (real, but NOT a test blocker — Popper demoted)
- **DH-1** Reset between runs → just a protocol instruction ("fresh `STUDIO_DATA` path") — **nice-to-have**, zero code.
- **DH-2** One handoff commit freezing D1 — the *deliverer's* precondition (hand off / reset-to / cite), revisits `DEC-EXT-COMMIT-POLICY-020`; **a human decision**, not something a tester needs.

### Deliverable 2 — "humans can test the FIRST PRINCIPLE (visual ergonomics)" (genuine build; next cycle)
- **P1-1** Rendered honest diff at the approval gate (the irreducible render).
- **P1-2** `preview --annotate` (render + click-to-annotate → resolved selector).
- **P1-3** Plain-language onboarding for a solo cold-start tester.

### Deferred (not-needed to close this cycle)
e2e Playwright (E), M3 recorder atomicity, F2 core identity gate (code), full SWU-Z workspace.

## Honest scope line
D1 tests **that the system told the truth and a human can supervise the gates** (the integrity + governance claim). It does **not** test **that a human can drive the visual prototyping loop** (the first principle) — that is D2. A D1 test must say so or it overclaims.

## Skeptic gate dispositions (zig-zag, applied)
- **Kuhn (precedent):** every already-deployed row verified built (P8 — inspected the actual files, not the synthesis); every build-needed row confirmed by the deciding absence (no root `package.json`/workspace → README run lines literally fail; no path-print; no reset; no tester F2 brief; no human protocol; no preview/rendered-diff/onboarding). Also confirmed (git): the two-gate chain + the live `.claude/` SKILL are UNTRACKED, core files modified-uncommitted. No corrections.
- **Popper (non-vacuity):** demoted **reset** (fresh STUDIO_DATA path closes it, zero code) and **handoff commit** (deliverer's workflow, not a tester capability) out of the P0 test-floor. Confirmed the **D1↔D2 split survives**: rendered diff is genuinely D2 *provided P0-3 keeps its governance-not-visual scope* — if the protocol asks testers to judge anything visual, the rendered diff becomes secretly P0 and the split collapses into overclaim.
- **Wittgenstein (definitional):** confirmed the collapses (README+path-print → run-seam; render-a-variant → open-the-file). One owner-boundary to hold: **Test protocol (P0-3) vs Plain-language onboarding (P1-3)** are DISTINCT-IF-SCOPED — protocol = task list + consent + feedback for the governance test; onboarding = self-orientation for the visual loop. Keep them separate or one author will duplicate the "how to start" prose.

## Bottom line
**To CLOSE this cycle and hand humans a thing to test:** three documents (P0-1 true README + path-print, P0-2 F2 disclosure, P0-3 governance-scoped test protocol). That ships **Deliverable 1** — a safe, repeatable, honestly-scoped test of the gates + governance ergonomics, where humans can also SEE variants (open the self-contained `.html`). It does **not** test the first principle. **Deliverable 2** (rendered diff at the gate, `preview --annotate`, onboarding) is the genuine next build that tests visual ergonomics. The deferred set (e2e, M3, F2 code gate, full SWU-Z) is not needed to close. One **human decision** stands at the seam: revisit `DEC-EXT-COMMIT-POLICY-020` to allow the handoff commit that makes the deliverable citable/resettable.
