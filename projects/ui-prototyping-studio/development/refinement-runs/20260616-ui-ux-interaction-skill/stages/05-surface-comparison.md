---
id: surface-comparison-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Surface Comparison Tournament (s5) — Pareto Judge: A overlay vs B TUI vs C local web"
status: decision
node_type: tournament-verdict
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s5-tournament
capability_ref: refine
mode: pareto-tournament
pattern: decision
consumes_decision: decision.research
consumes_frame: frame.evidence-baseline
consumes_handle: handle.define
emits_decision: decision.surface
updatedAt: 2026-06-16
---

# Surface Comparison Tournament (s5)

> **What this stage does.** It scores the three defined surfaces (s2 §5.1) on the five-axis rubric
> (s2 §5.2), builds one comparison table, eliminates dominated surfaces with reasons, and names the
> non-dominated winner (or a synthesis). It is the owner of **ODQ-1** (which surface). It does NOT
> author the SKILL.md or the design (s6), does NOT resolve ODQ-2's exact gate location beyond what the
> verdict constrains, and does NOT prove ergonomics (ODQ-7, s8). Every score below was cross-checked
> against the runnable code, not taken from the advocate briefs.
>
> **Frame receipt.** Consumed `handle.define` (D1–D5): the who-leads-when map (§3.2), the rubric (§5.2),
> the fixed obligations (§5.3), the two-layer scoping rule (§5.4). Consumed `decision.research =
> NO-RESEARCH (local-first)` with the held, unfired gap **G-A11Y** (re-checked in §6).

---

## 0. Verdict (up front)

**Winner: a constrained synthesis — C-as-spine + a deferred A-upgrade path. Plain name: the minimal
local web review page (C), built now, with one explicit annotation-fidelity upgrade hook to A's
in-iframe `data-od-id` element-pick named as a deferred dependency, not built this run.**

- **B (terminal/TUI) is eliminated** — dominated on the two axes that *are* the cold-start problem
  (C3 friction, C4 annotation): it cannot truly render HTML and offloads preview to `open in browser`,
  partially leaving root-cause #4 open, and it annotates by recall-from-a-list, not by pointing.
- **A (browser overlay) is eliminated as the surface to build now** — it is *unbuilt from zero*
  (verified: no `preview` command exists in the CLI), is mouse-shaped (fails `a11y.3` as designed,
  needs the unfired G-A11Y pattern pass), and its best disposal arguments (saw-the-diff, two-gate
  accept) rest on a build dependency that is shared by all three and present in none. A wins **one**
  axis (C4 annotation fidelity) and pays the worst build cost for it.
- **C is non-dominated**: at-or-near-top on C1/C2/C3, contract-valid (not best) on C4, second-cheapest
  on C5 — and its central C5 claim was the most disputed, so I verified it against the code: **C's
  most expensive component (the ephemeral server + JSON API + content store) already exists and runs.**
  C is the only surface that delivers *real live preview* (which B cannot) and *unified, keyboard-native,
  note-connected disposition* (which A risks fragmenting per ODQ-2) at a build cost the codebase has
  already largely paid.

A is not discarded; its sole win (in-DOM `data-od-id` capture) is preserved as a **named deferred
upgrade** to C's annotation path (same-origin `postMessage` element-pick into the iframe), to be pulled
only if `data-od-id` capture is later ruled mandatory rather than preferred (the moment C converges on
A's cost — and the moment G-A11Y fires).

---

## 1. Evidence verification (what I checked before scoring)

The advocates dispute build cost (C5) most sharply, and C5 is the axis with the highest swing. I read the
runnable code rather than trusting the briefs:

| Claim under test | Source checked | Verdict |
|---|---|---|
| A's `preview` command does not exist | `backend/src/cli/studio.ts` (usage string L124, command switch L62–124) | **TRUE.** No `preview` case; usage string omits it. A is unbuilt from zero. |
| B is a veneer over already-built CLI verbs | `studio.ts` L81–119: `variants register`, `baseline select|commit`, `comment add`, `synthesize`, `batch approve`, `batch apply`, `handoff export` all present | **TRUE.** B renders over existing commands. |
| C's server + every loop verb already exists as JSON API | `interface/http-routes.ts` L142–448: POST sessions/prompt/variants/baseline/comments/synthesize/approve/apply/handoff + GET session/variants/draft/revisions/handoff; `index.ts` is a runnable Fastify bootstrap | **TRUE.** C's most expensive component is built. |
| C's only new work is one HTML-serving GET + a static page | `grep text/html\|reply.type\|sendFile` across `backend/src` returns **no** HTML-serving route; `file-artifact-content-store.ts` L50 has `readHtml(ref)` | **TRUE.** The content read exists; only the route + page are new. |
| `odId` is optional in the comment contract (C can fall back) | `http-routes.ts` L51 `CaptureCommentBody.target?: unknown`, validated downstream; `comment add` (CLI L96) uses the same `captureCommentEvent` | **TRUE.** `selector`+`elementLabel` carry the contract; `odId` may be null. C is contract-valid. |
| Two-gate apply (steps 9–10) is unbuilt-in-path for ALL surfaces | `two-gate-apply.ts` exists but `grep` for `validateAndStage\|acceptStaged` outside its own test returns nothing; routes + CLI call single-gate `applyApprovedBatch` | **TRUE.** Shared dependency, charged to none (s2 §5.4). |

**Consequence for scoring.** The define stage scored C as "moderate build cost / still needs
ephemeral-server scaffolding" (s2 §5.1). The code overturns that premise: the scaffolding is the part that
already exists. This is the s4-F6 re-class of C5 made concrete. I score C5 against the *verified* delta
(one GET + one static page), not the define-stage estimate.

---

## 2. The comparison table

Scores are 1–5 (5 = best). The advocate self-scores are shown for traceability; the **judged** score is
mine after code verification. Where I diverge from an advocate, the reason is in the cell.

| Axis (weight) | A — browser overlay | B — terminal/TUI | C — local web page |
|---|---|---|---|
| **C1 who-leads-when clarity** | **4** — splits actors onto two physical channels (agent→CLI, human→browser); clean, but ODQ-2 risks scattering gates back to terminal, capping it | **5** — agent + human visibly co-located in one shell; no surface boundary for authority to blur across. Highest legibility. | **4.5** — single gate panel renders state as sentences + each disposal's enabled/disabled reason inline; *better than A* (A risks fragmenting), *just under B* (a web page is one more boundary than the shell the agent already lives in) |
| **C2 cognitive load** | **4** — recognition-over-recall via rendered variants; capped below 5 by the unbuilt keyboard path and the mouse-shaped default | **4** — sentences not JSON, but human must learn TUI keybindings and offloads preview to a browser tab (context switch = load) | **4** — one page, ≤3 iframes, one panel; web is the medium most humans already model (links/buttons/scroll); native HTML semantics carry recognition. Ties A/B. |
| **C3 friction reduction** | **5** — closes root-cause #4 (live preview) *and* #4-jargon (point, no selector) at one gesture; the reference for friction | **3** — closes #1/#2/#5 (sentences, disabled-reason) but **only partially closes #4**: cannot render HTML, offloads to `open in browser` — breaks "one surface" at the review moment | **4** — closes #4 (real iframes — what B cannot), #2/#5 (always-visible panel reasons), #1/#7 (plain labels); closes #4-*annotation* less finely than A |
| **C4 annotation fidelity** | **5** — captures stable `data-od-id` from the live DOM at the click; zero translation between intent and recorded target. The reference standard. | **2** — picks an id from a *textual list* (recall over a representation); mis-target easy when labels collide; cannot point at "that thing in the corner" with no list entry | **2.5** — iframe-sandboxed; coarse element/region pick, often falls back to `selector`+`elementLabel` with null `odId`. **Contract-valid** (verified `odId` optional), not parity with A |
| **C5 build cost** | **1** — unbuilt from zero (verified: no `preview`); needs ephemeral server + HTML render + overlay injection + click→id capture + an added keyboard path (`a11y.3`). Worst. | **5** — thin renderer + key-handler over already-built CLI verbs (verified `studio.ts`); shortest distance from the runnable CLI; `a11y.3`/`a11y.4` near-free in a TTY | **4** — server/API/content-store **already built and runnable** (verified); only new work = one `text/html` GET + one vanilla static page; `a11y.3` free from native HTML, `a11y.4` = `<dialog>`. Second-cheapest, beats A decisively |

**Shared, not charged to any surface (s2 §5.4):** the two-gate `apply`→`accept` saw-the-diff flow (steps
9–10, `a11y.4`) is a build dependency for A, B, and C alike — `two-gate-apply.ts` exists but is wired into
neither the routes nor the CLI (verified). No surface gets credit for solving it or a penalty for not.

---

## 3. Pareto / dominance analysis

A surface is **dominated** if another scores >= on every axis and > on at least one.

- **B vs C.** C >= B on C2 (tie 4/4), C3 (4 > 3), C4 (2.5 > 2), and C1 is effectively a tie (C 4.5 vs B 5
  — B's half-point edge on C1 does not rescue it). B beats C only on C5 (5 vs 4, a one-point build-cost
  edge). The two axes B loses — **C3 (friction) and C4 (annotation) — are literally the cold-start problem
  this run exists to solve** (s2 §1.1, s1 §4 root-cause #4 is "the single biggest cold-start win"). A
  one-point build-cost saving does not buy back a surface that cannot render the thing the human came to
  see. **B is dominated by C on the axes that matter, and its sole edge (C5) is marginal because C5 is
  already cheap.** → **B eliminated.**

- **A vs C.** Strictly, A is *not* numerically dominated by C (A wins C3 5>4 and C4 5>2.5), and C is not
  dominated by A (C wins C1 4.5>4 and C5 4>>1). So on the raw vectors **both A and C are pareto-non-
  dominated**, and B is the only strictly dominated surface. The tournament must therefore break the A/C
  tie by **weighting against the run's first principle and the §5.3 fixed obligations**, which is exactly
  what the pareto gate is for when the frontier has more than one point.

  The tie-break goes to C for three reasons, in order of force:
  1. **The two axes A wins are the two the run can most afford to defer; the two C wins are the two it
     cannot.** C5 (build cost) decides *what ships this run* — A's 1 means A ships nothing this run
     without first building the server, render, overlay, capture, and keyboard path. C1 (who-leads-when)
     is the charter's clause-1 spine. A's two wins are C3 (C already scores a strong 4) and C4 (where A is
     best but C is contract-valid and the recorded-decision intent, `DEC-INPROTO-ANNOTATION-013`, is
     *preferred `data-od-id`*, not *mandatory* — verified: `odId` optional in the contract).
  2. **A fails a fixed obligation as designed; C satisfies it for free.** `a11y.3` (keyboard-operable
     disposal, §5.3) is a *gate*, not a scored axis. A is mouse-shaped and needs the unfired G-A11Y
     pattern pass to satisfy it (s4 §3). C gets `a11y.3` from native HTML semantics (`<button>`, tab
     order, `aria-disabled`) and `a11y.4` from `<dialog>` — no bespoke keyboard layer. A surface that
     needs new research to pass a fixed gate cannot beat one that passes it by construction.
  3. **A re-opens root-cause #3 unless it also hosts the gates (ODQ-2); C closes it by construction.**
     A's strength is the in-DOM overlay, and the define stage flags (ODQ-2) that A may leave gates in the
     terminal — splitting annotation (browser) from disposition (terminal) re-introduces "disconnected
     from the note" (root-cause #3). For A to keep its C1 score it must *also* host gates, which raises
     its already-worst C5 further. C keeps note + disposition in one served page by construction.

  → **A eliminated as the surface to build now.** Its one decisive capability (C4) is preserved as a
  named deferred upgrade to C (§0, §5), not discarded.

**Frontier result:** raw pareto leaves {A, C} non-dominated and eliminates B; the first-principle +
fixed-obligation tie-break selects **C**, with A's C4 capability folded forward as a deferred hook. This is
the honest "synthesis" the dispatch invites: not a 50/50 merge, but **C-as-spine with a costed path to A's
one advantage** — which is precisely the convergence point both the A and C advocates concede ("that is
exactly the moment C starts converging on A's cost").

---

## 4. Why not the recorded decision's presumed surface (A)?

`DEC-INPROTO-ANNOTATION-013` presumes the overlay (A), and s1 §6/ODQ-1 raised the live tension: *does the
tournament get to overturn a recorded decision, or only choose the surface around it?* The honest answer:

- The recorded decision fixes the **annotation contract and intent** — capture a stable `data-od-id` by
  pointing at a rendered component, surviving regeneration. **That intent is preserved**, not overturned:
  C captures the same `CommentEvent` contract, and the deferred A-upgrade restores in-DOM capture verbatim.
- The recorded decision did **not** fix *build sequencing*. Choosing C-first is a sequencing decision
  inside the decision's own intent, not a reversal of it. The §5.4 two-layer scoping rule already
  established that the surface is "designed against the spec contract … named as a build dependency,"
  which is exactly how A's overlay is now treated: **a named deferred dependency, not this-run work.**

So the tournament does not overturn `DEC-INPROTO-ANNOTATION-013`; it sequences toward it via the
cheapest contract-valid surface that ships now.

---

## 5. Constraints the verdict hands to s6 (design) and s9 (plan)

1. **Build C this run:** add one read-only `text/html` GET to `http-routes.ts` (using
   `file-artifact-content-store.readHtml`), and one vanilla static page (no SPA, no build step) hosting:
   (a) ≤3 sandboxed-iframe variant renders side-by-side (closes #4); (b) one gate panel rendering session
   state as plain sentences with each durable disposal (baseline / approve / apply-accept / export) as a
   native keyboard-operable control annotated with its enabled/disabled reason (closes #2/#5, satisfies
   `a11y.3`/`a11y.5`); (c) comment capture POSTing the identical `CommentEvent` contract.
2. **Keep gates IN the page (resolves ODQ-2 against fragmentation):** disposition must stay co-located
   with the note/diff in the served page — do NOT leave gates in a disconnected terminal (§5.3 fixed
   obligation; root-cause #3).
3. **`a11y.4` accept-diff:** use a `<dialog>` focus trap for the saw-the-diff accept (step 10), gated on
   the two-gate apply build (s2 §5.4 / N1 routed to s9).
4. **Annotation honesty in the SKILL.md narration (§4.4):** the surface captures coarse (often null
   `odId`); the SKILL.md must not let Claude Code assert pixel-fidelity it does not have.
5. **Deferred A-upgrade hook (named, not built):** when/if `data-od-id` capture is ruled mandatory, add
   same-origin `postMessage` element-pick into the iframe to restore A's in-DOM fidelity. This is the
   trigger that **fires G-A11Y** (s4 §3) — at that point the keyboard-AT pattern pass for click-to-annotate
   becomes a real, bounded dependency. Until then G-A11Y stays unfired (C is keyboard-native).

---

## 6. G-A11Y re-check (s4 residue)

s4 held G-A11Y conditional on **s5 selecting surface A**. **s5 did not select A** — it selected C, which
is keyboard-native by construction. Therefore **G-A11Y does NOT fire now.** It is re-armed against the
§5 constraint-5 deferred A-upgrade: if that hook is pulled in a later run, the click-to-annotate
keyboard/AT pattern pass becomes live. Recorded so the trigger is not lost.

---

## 7. Rejected alternatives (residue ledger)

| Rejected | Why rejected | Salvaged value preserved |
|---|---|---|
| **B — terminal/TUI as the surface** | Dominated by C on C3 (can't render HTML, offloads #4 to a browser tab) and C4 (recall-from-list, not point); its only edge (C5) is marginal because C5 is already cheap | B's C1 co-location lesson informs the gate-panel-as-plain-sentences design; `comment add` remains the graceful CLI fallback when the browser is unavailable |
| **A — browser overlay as this-run surface** | Unbuilt from zero (verified no `preview`); fails `a11y.3` as designed (needs unfired G-A11Y); best disposal arguments rest on the shared unbuilt two-gate flow; risks re-opening root-cause #3 via ODQ-2 unless it also hosts gates (further raising worst-in-class C5) | A's in-DOM `data-od-id` capture is the named deferred upgrade to C (§5 constraint 5); A's saw-the-diff rendering is the target for the `<dialog>` accept |
| **Pure A/C 50/50 merge ("overlay + panel both now")** | Pays A's full unbuilt build cost immediately for a C4 gain that is *preferred not mandatory* (verified `odId` optional); contradicts local-first + ship-this-run | Folded into the sequenced synthesis: C now, A's capability as a costed deferred hook |
| **Re-deriving the rubric with a 6th diff-legibility axis (s4-F6)** | The dispatch fixes the five named axes; diff-legibility is a *fixed obligation* (`a11y.4` / saw-the-diff, §5.3) shared by all surfaces, not a discriminating axis — adding it changes no elimination | Captured as s6 design constraint 3 (`<dialog>` accept) rather than a scoring axis |
| **Treating `DEC-INPROTO-ANNOTATION-013` as mandating A** | The decision fixes annotation *intent/contract*, not build *sequencing*; `odId` is optional in the verified contract | Intent preserved by C's identical `CommentEvent` + the deferred A-upgrade |

---

## 8. Stop condition + handoff

- **All three surfaces scored on the five-axis rubric** (§2). **Met.**
- **Comparison table built** (§2). **Met.**
- **Dominated surface eliminated with reasons** (B; §3). **Met.**
- **Non-dominated winner / synthesis named** (C-spine + deferred A-upgrade; §0/§3). **Met.**
- **Rejected alternatives preserved as residue** (§7). **Met.**
- **ODQ-1 owned and resolved** (surface = C). **ODQ-2 constrained** (gates in-page; §5 constraint 2) and
  handed to s6. **G-A11Y re-checked, does not fire** (§6).
- **Ergonomics not asserted** (charter clause 5): all C2/C3 gains remain `human_study`-class, plausible and
  falsifiable in the s8 toy-game, not demonstrated (ODQ-7 unchanged).

**Emits:** `decision.surface = C (minimal local web review page) as the build-now spine, with A's in-DOM
`data-od-id` capture as a named deferred upgrade; B eliminated`. Carried residue to s6/s9: the five §5
constraints; the unfired-but-re-armed G-A11Y; the shared two-gate-apply build dependency (steps 9–10,
N1 routed to s9).
