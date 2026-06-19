---
id: review-attacks-ups-skill-design
project: ui-prototyping-studio
title: "Review attacks (2 rounds) — ups-skill-design-review"
node_type: review-attacks
dispatch_id: 2026-06-16-ups-skill-design-review
run_id: 20260616-ui-ux-interaction-skill
targets: [06-SKILL-draft.md, stages/06-interaction-design.md, RESULT.md]
governing_context: stages/02-define-and-flow-xray.md (s2)
rounds: 2  # initial + final (robot-talks); collapse detection preserved
synthesizer: "Shannon, Claude"
updatedAt: 2026-06-16
---

# Review attacks — both rounds, by attacker

Two-round robot-talks over the `ui-prototyping-studio` SKILL draft + interaction design + RESULT.
Line cites are the attackers', already code-verified. Round 1 = initial position; Round 2 =
final position after seeing the others. **Collapse / movement is preserved verbatim per attacker.**

---

## A1 — Wisnesky (lens: mechanics / correctness)

### Round 1 (initial)
- **Verdict at first pass:** corpus unusually code-faithful; **ZERO doc-contradicts-code** found.
- F-CRIT-1's three sub-claims all **TRUE**:
  - `approve-mutation-batch.ts:61-77` checks only that `approvedBy` is non-empty — **no actor-class check**.
  - `apply-approved-batch.ts:32-41` refuses **only** the literal lowercased string `"system:auto"` (`AUTO_APPLY_FORBIDDEN`).
  - `http-routes.ts:341` apply route uses `parseActor(..., "web-ui")` default.
- Command table matches `studio.ts:62,70-124` exactly; `preview`/`accept`/`discard` correctly **NON-EXISTENT**.
- Two-gate engine `validateAndStage` / `acceptStaged` / `discardStaged` exist (`two-gate-apply.ts:38,55,80`),
  unit-tested (`two-gate-apply.test.ts`, 5 cases); **batch apply is single-gate** (`studio.ts:113-114` →
  `applyApprovedBatch` advances head in one call).
- **DC-1 confirmed:** `parseAnnotationTarget` (`http-routes.ts:668-702`) hard-requires non-empty
  `selector` + `elementLabel`; `odId` nullable — correct.
- **One MINOR:** RESULT §3.1 grammar attaches the "web-ui default" to the **APPROVE** gate, but that
  default is only on the **APPLY** route; the approve route uses `parseRequiredString` (throws
  `APPROVAL_METADATA_REQUIRED` if missing), no web-ui default.

### Round 2 (final — COLLAPSE)
- **WITHDRAWS "zero contradictions."**
- **ENDORSES A3's CRITICAL:** verified `06-interaction-design.md:219` step-7 (Approve) cell
  "Claude Code refused server-side if it tries (`AUTO_APPLY_FORBIDDEN` lineage / INV-3)" is
  **CATEGORICALLY FALSE for approve** — `approve-mutation-batch.ts` has zero actor check;
  `AUTO_APPLY_FORBIDDEN` exists only in `apply-approved-batch.ts:33` as a `system:auto` string-literal denylist.
- **ENDORSES A3's MAJOR** (s2 propagation of the same overclaim).
- **CONFIRMS A2's premise is code-real:** `studio.ts:24` `const ACTOR = process.env.STUDIO_ACTOR ?? "cli-user"`;
  every verb uses that one actor (approve `approvedBy: ACTOR` line 111; apply `applyRequestedBy: ACTOR`
  line 114); **no per-call identity.** A2's X1/X2 ride a code-real gap.
- **KEEPS its own MINOR** (RESULT §3.1 grammar).

---

## A2 — Taleb (lens: abuse / gaming)

### Round 1 (initial)
- **Root framing:** the never-do spine governs **WHO RUNS THE VERB** but is silent on **WHO AUTHORS the
  decision/command.** Identity is unenforced in code, so "the human ran it" is satisfiable by an
  agent-authored relay.
- Five exploits:
  - **X1 narrate-to-yes** — agent narrates readiness, cold-start human approves unread. **CRITICAL**
  - **X2 command-dictation** — agent dictates the exact gate command string the human pastes. **CRITICAL**
  - **X3 synthesize-freeze steering** — agent times `synthesize` to freeze the comment set early
    (synthesize snapshots current comments). **MAJOR**
  - **X4 "offer don't decide" semantic gap** — undefined; sole-next-step framing (decision-paralysis
    §5.3) weaponized. **MAJOR**
  - **X5 "on the human's behalf" laundering** — from `comment add` to baseline / handoff. **MAJOR**
- **One fix closes most:** a **human-only gate token** the core requires at all 5 durable gates (**R-S7-1**).

### Round 2 (final — COLLAPSE)
- **Sharpened test:** "can words change the AGENT's behavior independent of the human?"
  - **X1 downgrade CRITICAL → MAJOR** — agent shapes, but the human's paste is causal; the SKILL **can**
    forbid recommendatory narration at gates.
  - **X2 downgrade CRITICAL → MAJOR** — the SKILL **can** forbid the agent authoring the command string;
    human re-type is residue.
  - **X4 HOLD MAJOR** — cleanest genuine finding (definitional hole; pure-words fix).
  - **X5 HOLD MAJOR** — lexical rule.
  - **X3 → MINOR** (partial).
- **Irreducible relay residue** (human pastes agent content verbatim) is **NOT a SKILL defect** — it
  routes to a single **CORE-level CRITICAL: R-S7-1** (human-only gate token enforced by the core at all 5 gates).
- **Reconcile with A3:** fixing the design overclaim makes the exploits **MORE** severe — it deletes the
  illusion of a backstop, revealing the honor-system spine as the **sole** control.

---

## A3 — Ashby (lens: fidelity / governance)

### Round 1 (initial)
- **SKILL draft is law-faithful:** F-CRIT-1 corrected in the "Honest authority note" (`06-SKILL-draft.md:112-119`);
  single-gate disclosed; no ergonomic claim (`06-SKILL-draft.md:139`). **The debt is in the DESIGN stage.**
- Findings:
  - **(CRITICAL)** `06-interaction-design.md:219` step-7 cell "refused server-side if it tries" is **false
    for approve**, reasserting the F-CRIT-1 backstop; design **self-contradicts** (§3 overclaims vs the
    R3 residue ledger at line 383, which corrects it).
  - **(MAJOR)** s2 propagation — `02-define-and-flow-xray.md` §1.2 line 74 / §3.2 line 141 / §4.3 line 191
    seed the overclaim with **no forward-correction banner.**
  - **(MINOR / PASS, B1)** two-gate narrowing **IS** disclosed honestly (SKILL line 85; design §4.3 264-271;
    RESULT §2.4 line 45) — honest interim; nit: lead step9/10 cells with single-gate (RESULT §3.4 M2).
  - **(MINOR, C2)** design §3 prose superlatives — "the single biggest cold-start win" (`:215`),
    "the strongest control-side ergonomic" (`:222`) — in tension with charter clause 5 + RESULT §3.3
    "no ergonomic gain asserted anywhere."
  - **(MINOR, D1)** SKILL line 59 "5 gates + 1 terminal" vs design §0 line 53 / s2 §3.3 line 150
    "handoff = 5th gate" — same disposed-set {4,7,9,10,12}, different arithmetic; SKILL lists 6 NO-rows
    (baseline select + commit counted).

### Round 2 (final — COLLAPSE)
- **HOLD CRITICAL on design step-7:** BUILD consumes the step table, **not** the R3 residue ledger — a
  correction off the consumption surface is "a contradiction with a footnote."
- **ADDS A3-NEW (MAJOR):** the SKILL never-do spine is **INCOMPLETE** — it forbids the agent **EXECUTING**
  the verb but is silent on the agent **AUTHORING** the decision the verb encodes (the SKILL-level analog
  of the design's phantom backstop; **survives the design fix**). This **RETRACTS** A3's round-1
  "SKILL is clean."
- **CONVERGENCE FLAG:** A1-mechanics-root + A3-design-CRITICAL + A2-X1/X2 are **ONE defect** (no
  server-side identity gate) seen three ways — **do NOT triple-count** as independent criticals.
- **C2, D1 HOLD MINOR**, unaffected by A2.

---

## Cross-attacker movement summary (collapse map)

| Item | A1 R1 | A1 R2 | A2 R1 | A2 R2 | A3 R1 | A3 R2 |
|---|---|---|---|---|---|---|
| "zero doc-vs-code contradictions" | asserted | **withdrawn** | — | — | — | — |
| design step-7 phantom backstop (CRIT) | — | **endorses** | — | (reinforces) | **raised CRIT** | **holds CRIT** |
| s2 propagation (MAJOR) | — | endorses | — | — | **raised MAJOR** | holds |
| SKILL decision-authorship silence (MAJOR) | confirms code-real | confirms | **raised (as X1/X2/X4/X5)** | holds X4/X5 MAJOR | "SKILL clean" | **RETRACTS; adds A3-NEW MAJOR** |
| X1 narrate-to-yes | — | — | CRITICAL | **→ MAJOR** | — | — |
| X2 command-dictation | — | — | CRITICAL | **→ MAJOR** | — | — |
| X3 synthesize-freeze | — | — | MAJOR | **→ MINOR** | — | — |
| R-S7-1 core identity gate (CORE CRIT route) | — | — | proposed | **holds (sole irreducible)** | — | (= convergent root) |
| RESULT §3.1 grammar (MINOR) | raised | **keeps** | — | — | — | — |
| ergonomic superlatives C2 (MINOR) | — | — | — | — | raised | holds |
| gate arithmetic D1 (MINOR) | — | — | — | — | raised | holds |

**Net collapse:** all three attackers converge on a **single root defect — no server-side human-vs-agent
identity gate** — manifesting as (i) a CRITICAL design overclaim, (ii) a MAJOR SKILL-spine omission, and
(iii) an irreducible CORE route. A2's two initial CRITICALs both relaxed to MAJOR once the SKILL-fixable
core was separated from the irreducible relay residue.
