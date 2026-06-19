---
id: plan-closed-loop
project: ui-prototyping-studio
title: "Plan — closed-loop: select in preview → Claude Code auto-stages → human accepts"
status: proposal
node_type: implementation-plan
invoke_mode: plan
complexity: medium
source: refinement-runs/20260617-closed-loop-select-autoupdate
updatedAt: 2026-06-17
---

# Plan — closed visual loop (select → auto-pickup → stage → accept)

**Feasibility: YES.** Builds on the live preview (P1/P2) + two-gate apply (MW1). The agent can run the
whole loop — select → stage → **accept** — because the control is **reversibility, not identity-gating**
(supersedes F2 / DEC-F2-INTERIM-025). The single human checkpoint is the **irreversible export edge**.
Non-executed; each SWU a `task-session`.

## Governing principle — reversibility, not gating
We do NOT distinguish human from agent. Safety = every in-studio action is undoable AND visible:
- **stage → discard** (exists).
- **accept → revert** (NEW, CL5): append-only log + content-addressed HTML already preserve every prior
  state by hash; revert appends an *inverse* revision pointing at a prior `candidateHtmlHash` — undo is
  itself a recorded, re-reversible event; head never rewinds destructively; history stays complete.
- the agent may **auto-accept**; staging remains a *visibility* step, not a required gate.
- the ONE human checkpoint is **export/handoff** — the studio's output leaving for downstream consumption
  is the genuine point of no return (gated by irreversibility, not by who is asking).

## SWU manifest (build order)

| SWU | Title | Depends on | Write scope | Acceptance |
|-----|-------|-----------|-------------|------------|
| **CL1** | Selection capture (annotate mode) | preview (done) | `interface/preview-routes.ts` (`/annotate/variant/:label` trusted wrapper + `POST /comment`), page overlay | clicking a rendered component captures its `data-od-id` + note → `captureCommentEvent` (INV-2 gated, DC-1 selector+elementLabel) |
| **CL2** | Agent pickup — next-turn drain (B, ship first) | CL1, synthesize+applyAndStage (done) | a `studio pending` query + a documented agent routine | the agent lists comments with no batch, then synthesize → propose candidate → `applyAndStage`; idempotent (handled comments skipped); **never accepts** |
| **CL3** | Agent pickup — watch loop (A, the "automatic" upgrade) | CL2 | a `studio watch <sid>` helper or a Claude Code `/loop` recipe | Claude Code polls every N s; on a new pending comment → CL2 routine → stage (or auto-accept once CL5 lands); may run UNSUPERVISED because CL5 makes every step reversible + CL4 makes it visible |
| **CL4** | Preview auto-refresh | preview (done) | preview page | the page reflects a newly-staged/accepted candidate without manual reload (meta-refresh/poll/SSE) — the human SEES every change the agent makes |
| **CL5** ✅ DONE | Reversibility guarantee (replaces F2) | append-only log (exists) | `revert-revision.ts` + `studio revert [--to]`; `handoff export --confirm` | **BUILT + verified** (2026-06-18): `studio revert` appends an inverse revision (prior `candidateHtmlHash`) → head forward, content back, history intact, re-revertible; `handoff export` refuses without `--confirm` (exit 3). 5 unit tests + e2e CLI round-trip green (47/47 suite). |

## Per-SWU detail
- **CL1** — `/annotate/variant/:label` serves the registered variant wrapped with ONLY a trusted
  click→`postMessage(odId)` script (`sandbox="allow-scripts"` for this wrapper; raw `/raw/variant` stays
  fully sandboxed). Parent page opens a `{severity,intent,note}` form on a click, POSTs `/comment` →
  `captureCommentEvent`. **Verify:** click cta.primary → a CommentEvent with that od-id; pre-baseline POST rejected (INV-2).
- **CL2** — `studio pending <sid>` returns comments not yet in a batch. Agent routine: pending → synthesize
  → author candidate HTML (the generative act, grounded in the open-design refs) → `applyAndStage`. Idempotent
  by comment id. **Never** calls accept. **Verify:** a pending comment → a staged candidate; re-run doesn't double-stage.
- **CL3** — `studio watch <sid>` (or a `/loop` recipe) polls `pending` and drives CL2 on new items; bounded
  cadence. With CL5 landed it may auto-accept and run unsupervised (every step reversible + visible).
  **Verify:** add a comment via CL1 → within one tick a candidate is staged/accepted; the change shows in
  the preview; `studio revert` walks it back cleanly.
- **CL4** — preview polls session state (or SSE) and refreshes the staged/head section. **Verify:** the
  agent stages or accepts while the page is open → it appears without manual reload.
- **CL5** — `revert-revision.ts` + `studio revert [--to <revId>]`: append an inverse revision whose
  `candidateHtmlHash` = the target prior revision's hash (append-only; head still moves forward; never a
  destructive rewind). Plus an explicit human confirm on `handoff export` (the irreversible edge).
  **Verify:** accept → revert → head HTML equals the pre-accept HTML; the log shows both events; revert is
  itself revertible; `handoff export` refuses without the confirm flag/prompt.

## Implementation-layering
- **L0 (CL1):** the browser can write a selection back to the studio.
- **L1 (CL2):** the agent turns a selection into a staged change (next-turn) — the loop closes.
- **L2 (CL3+CL4):** it FEELS automatic — watch loop + auto-refresh; select and watch it update.
- **L3 (CL5):** safe UNSUPERVISED via **reversibility** — revert for accepts + a human confirm only at the
  irreversible export edge. No identity gate is built (F2 dropped).

## Validation strategy
CL1 → capture test (od-id, INV-2). CL2 → pending→staged idempotency test. CL3 → watch-tick e2e + the
accepted change is revertible. CL4 → refresh-appears check. CL5 → revert round-trip test (head HTML
restored, log shows both events, revert re-revertible) + export-requires-confirm test. Backend suite green.

## Governance boundary (the principle)
Control = **reversibility, not gating**. The agent may run the full loop including **accept**; every action
is undoable (`discard` for staged, `revert` for accepted) and visible (CL4). We do **not** distinguish human
from agent. The **only** human checkpoint is **export/handoff** — the one irreversible, downstream-consumed
edge. Supersedes DEC-F2-INTERIM-025 ("accept is human-only") and the SKILL never-do line that enforced it
(SKILL update is a flagged follow-up, not silently applied).

## Operating modes — AUTO (exploit/explore cycles) · HUMAN-in-the-loop
(from refinement-runs/20260617-two-modes-exploit-explore-hil — design in that run's stages/06-design.md)

The same loop is driven two ways, and the two ways **compose as phases** (handoff pipeline): the HUMAN phase
anchors the fitness signal AUTO needs; AUTO cycles against it and hands a set back.

- **HUMAN-IN-THE-LOOP** — human selects in preview → agent proposes ONE → human accepts/reverts. The human
  IS the fitness signal each step. (= CL1 + CL2 + CL4, already planned.)
- **AUTO** — the agent runs bounded **cycles**, each either **EXPLORE** (from head/baseline → K *divergent*
  candidates) or **EXPLOIT** (from head → candidates that *converge* toward the objective). Stages and (under
  reversibility) may auto-accept; runs until a stop dial.

**Fitness signal (resolves "exploit toward what?"):** human-anchored composite — the **human owns the
objective** (prompt + accepted comments + explicit picks; AUTO never invents one); per-cycle fitness =
**heuristic GATE** (a11y/design-system/spec, a hard discard) + **self-critique ORDERING** vs the frozen
objective; **pause-to-human** when candidates plateau (improvement < ε) or critique disagrees with the gate.
Reversibility is the backstop — any wrong convergence is reverted at the human's next review.

**Explore↔exploit policy:** human dial per run (default); optional auto-policy = *explore-then-exploit*
(explore until a human pick, exploit it, re-explore on plateau). **Stop dials (smallest scope wins):**
`layers`=K candidates/cycle · `loop_cap`=max cycles/run · `max_loops`/budget=dispatch ceiling · plateau-ε
convergence stop · **start gate: AUTO refuses an empty objective**.

### AUTO-mode SWU manifest (layered on CL1–CL5)
| SWU | Title | Depends on | Write scope | Acceptance |
|-----|-------|-----------|-------------|------------|
| **ML1** | Cycle engine | CL2, CL5 | `studio cycle <sid> --mode explore\|exploit --k N` (one bounded cycle: generate → stage/accept under reversibility) | one explore cycle stages K distinct candidates; one exploit cycle stages a candidate closer to the objective; idempotent + bounded |
| **ML2** | Fitness signal | ML1 | objective resolver (prompt+accepted comments+picks) + heuristic gate (a11y/design-system/spec) + self-critique ordering; `studio pick`/`rate` to anchor | failing-gate candidates discarded; survivors ordered; empty objective ⇒ start refused |
| ML2+ | *(DEFERRED, post-MVP)* UX-constraint fitness backing | ML2 + ux-evidence-validator + axe/layout runner | replaces the heuristic part of ML2 with the studio's UX-constraint layers as a machine `FitnessSignal` (hard gates = a11y/layout/deterministic-flow; soft gradient = cognitive/laws-of-ux) | specced under SPEC §3 DEFERRED "UX-constraint exploit/explore fitness" (OQ-5); not an MVP SWU — see refinement-runs/20260618-ux-constraints-exploit-explore-spec |
| **ML3** | Explore/exploit policy + stop dials | ML1, ML2 | the dial (human default) + explore-then-exploit auto-policy; `loop_cap`/`max_loops`/plateau-ε; pause-to-human | `loop_cap=3` halts at 3; contradictory comments ⇒ pause not thrash |
| **ML4** | AUTO driver | ML1–ML3, CL3 | the `/loop`/watch that runs cycles to a stop condition (CL3 extended with mode + stop) | start AUTO → cycles run → stops on dial/plateau → every accept revertible |
| **ML5** | Mode surface | CL1, ML4 | preview toggle (Auto/Human) + the phase handoff (human pick → AUTO → returned set) | toggling switches who-leads; AUTO returns a reviewable set to the human |

**Validation (modes):** ML1 cycle converge/diverge tests · ML2 gate-discard + empty-objective-refused · ML3
loop_cap-halt + plateau-pause · ML4 driver e2e (runs, stops, all-revertible) · ML5 toggle/handoff check.
Falsification done in this run's stages/08-toygame.md (exploit converges, explore diverges, dial halts, weak
signal pauses, export still gated). Backend suite stays green.

**Governance (unchanged):** both modes keep **export as the only human-required edge** (DEC-026). AUTO's
autonomy is safe *because* every step is reversible + visible, not because the agent is identified.

## Build status (2026-06-18 — batched decision-gate build)
Decisions (one pass): scope = **everything buildable now** · AUTO default = **auto-accept under reversibility** ·
AUTO fitness = **lighter (self-critique + human objective)**; only UX-constraint backing (OQ-5) deferred.

**BUILT + verified (backend suite 53/53 + e2e CLI/HTTP):**
- **CL1** ✅ annotate route `/annotate/variant/:label` (trusted click→`postMessage`; raw stays sandboxed) + POST `/comment` (browser→studio write) + overlay form. Verified: click→comment→pending.
- **CL2** ✅ `studio pending` (`list-pending-comments.ts`) — comments on head not yet batched; idempotent.
- **CL4** ✅ preview `/state` + poll-refresh (reloads only on state/head/staged change).
- **CL5** ✅ revert + `handoff export --confirm` (see CL5 row).
- **ML1/ML2/ML3** ✅ `run-cycle.ts` — one exploit/explore cycle: agent supplies candidate HTML + self-critique score; core gates via the M1 fence (exploit = head od-ids only; explore = +candidate od-ids, free divergence) and **auto-accepts the top score** (reversible). Empty-objective start gate. Verified: exploit converges, explore admits divergence, revert restores.
- **ML4 (thin)** ✅ `studio watch` = single-shot driver tick (the agent's `/loop` calls it each interval). **Honest limit:** generation/synthesis are the agent's act; stop dials (loop_cap/max_loops/plateau) live in the agent `/loop`, not the core — documented, not core-enforced.
- **ML5 (CLI-first)** ✅ `studio cycle`/`pending`/`watch` + the preview annotate surface. A dedicated Auto/Human preview toggle is a thin follow-up.

**Honest residue:** EXPLORE auto-accepts the top-scored candidate rather than presenting K simultaneously (the store holds one staged slot) — the "diverse population to pick from" UX is a follow-up. The rigorous **UX-constraint fitness (ML2+) stays deferred** (OQ-5, needs the axe/layout runner).

## Next route
`task-session`: **CL1 → CL2 → CL4** (HUMAN mode, the loop visible) → **CL5** (revert + export-confirm) →
**ML1 → ML2 → ML3** (the AUTO cycle + fitness + dials) → **ML4 → ML5** (AUTO driver + mode surface) →
CL3 folds into ML4. ML2 (fitness signal) is the keystone of AUTO — it's what makes "exploit" mean anything.
