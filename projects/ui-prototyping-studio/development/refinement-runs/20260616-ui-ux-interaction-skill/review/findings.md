---
id: review-findings-ups-skill-design
project: ui-prototyping-studio
title: "Review findings — synthesized change requests, ups-skill-design-review"
node_type: review-findings
dispatch_id: 2026-06-16-ups-skill-design-review
run_id: 20260616-ui-ux-interaction-skill
targets: [06-SKILL-draft.md, stages/06-interaction-design.md, RESULT.md]
governing_context: stages/02-define-and-flow-xray.md (s2)
synthesizer: "Shannon, Claude"
severity_taxonomy: "CRITICAL=breaks system/corrupts record/contradicts governing law; MAJOR=functional gap/drift/doc-vs-code mismatch/load-bearing omission; MINOR=wording/stale/fuzzy pointer"
updatedAt: 2026-06-16
---

# Findings — ups-skill-design-review

De-duplicated, severity-ranked change requests over the SKILL draft, the interaction design, and the
RESULT. Governing context: the s2 x-ray. **claim <= proof:** every finding quotes the artifact and cites
the attacker it came from.

## The single root defect (read first — do NOT triple-count)

All three attackers converge on **one** defect: **the core enforces no human-vs-agent identity at the
durable gates.** Code-verified by A1: `approve-mutation-batch.ts:61-77` checks only that `approvedBy` is
non-empty; `apply-approved-batch.ts:32-41` refuses only the literal `"system:auto"`; `studio.ts:24`
`const ACTOR = process.env.STUDIO_ACTOR ?? "cli-user"` is the one actor every verb uses. This root has
**three distinct, non-duplicate consequences** that ARE counted separately below because each lives in a
different artifact and each has its own fix:

- **F1 (CRITICAL)** — the design step-table *asserts the absent backstop as present* (a contradiction with governing code, on the build-consumption surface).
- **F3 (MAJOR)** — the SKILL spine *forbids executing but not authoring* the decision (a load-bearing omission, the SKILL-fixable core of the abuse exploits).
- **F2 (build-blocking ROUTE)** — the irreducible residue *routes to the core* (R-S7-1); a build-blocking dependency, **not** a doc-defect change-request (reclassified from CRITICAL per Gödel's verification: severity in this review ranks edits over the targets; F2 closes by no target edit).

A3's explicit convergence flag is honored: F1 + F3 + the A2 exploits are **ONE defect seen three ways**;
they are not three independent criticals.

---

## CRITICAL

### F1 — Design step-7 asserts a server-side backstop that does not exist
- **Artifact:** `stages/06-interaction-design.md` (interaction design), step-7 cell.
- **Quote (`:219`):** "Human disposes; **Claude Code refused server-side if it tries**
  (`AUTO_APPLY_FORBIDDEN` lineage / INV-3)".
- **Why CRITICAL:** flatly contradicts governing code. Per A1 (R2, verified) the **approve** path has
  **zero** actor check; `AUTO_APPLY_FORBIDDEN` exists only in `apply-approved-batch.ts:33` as a
  `system:auto` string-literal denylist — it is categorically false for approve. Per A3 the design
  **self-contradicts** (the §3 overclaim vs the R3 residue ledger at `:383`), and **BUILD consumes the
  step table, not the residue ledger** — so a correction off the consumption surface is "a contradiction
  with a footnote." This is the exact F-CRIT-1 overclaim the SKILL already retired, resurfacing in the
  design.
- **Attackers:** A3 (raised + held CRITICAL across both rounds); A1 (R2 endorses, code-verified).
- **Fix:** rewrite the step-7 cell (and any sibling cell that implies a server-side identity refusal) to
  state honestly: scope is enforced server-side, **identity is not**; the never-do spine is the binding
  control; the real identity gate is routed to core owners. Put the correction **on the step table**, not
  only in the residue ledger.
- **Verifier note:** I expect this to survive. The quote is verbatim and the code facts are A1-verified.

---

## BUILD-BLOCKING ROUTE (not a target-doc change-request)

### F2 — Core has no human-only gate token at the 5 durable gates (ROUTE, build-blocking)
- **Artifact:** the core (not a doc) — routed via RESULT §3.4 `R-S7-1 / R3` and design residue.
- **Quote (RESULT `:64`):** "durable gates need a real human-vs-agent identity signal; today scope + a
  `system:auto` string match is the only server check."
- **Why build-blocking (reclassified from CRITICAL):** this is the irreducible residue A2 isolated in R2 — once the SKILL forbids agent
  narration and command-authoring (F3), the *human pastes agent content verbatim* relay still satisfies
  "the human ran it." No SKILL wording can close it; only the core can. A2 reconciles with A3: fixing the
  design overclaim (F1) **deletes the illusion of a backstop**, leaving this as the sole real control gap.
- **Attackers:** A2 (R-S7-1, sole irreducible CORE-level CRITICAL); A1 (confirms code-real); A3 (= convergent root).
- **Disposition:** this is a **build-blocking ROUTE to core owners (R-S7-1 / P-c3)**, NOT a doc-fix in
  this review's targets. It is already named in RESULT §3.4 and §5.3 — the change request is to keep it
  as an explicit pre-build gate, not to silently rely on the SKILL spine alone.
- **Verifier note:** survives as a routed obligation; do not expect a doc edit to close it.

---

## MAJOR

### F3 — The SKILL never-do spine forbids EXECUTING the verb but not AUTHORING the decision
- **Artifact:** `06-SKILL-draft.md` (SKILL draft), the never-do spine + command table.
- **Quote (`:105-108`):** "**Never approve, apply, or accept** — those are human gates, always. … **Never
  annotate, select a baseline, or export a handoff *for* the human.** Record only what the human authored."
  The spine names execution prohibitions but no rule against the agent **authoring** the decision the
  human then enacts. The "**offer, don't decide**" (`:80`) and "**only on the human's behalf**" (`:79`)
  cells are the undefined surfaces A2 weaponizes.
- **Why MAJOR:** load-bearing omission, not a contradiction. A3-NEW (R2) retracts A3's round-1
  "SKILL is clean": the spine is the SKILL-level analog of the design's phantom backstop and **survives
  the F1 fix.** It is the SKILL-fixable core of A2's downgraded exploits:
  - **X1 narrate-to-yes** (agent narrates readiness; cold-start human approves unread) — MAJOR; "the SKILL CAN forbid recommendatory narration at gates."
  - **X2 command-dictation** (agent authors the exact gate command string the human pastes) — MAJOR; "the SKILL can forbid the agent authoring the command string."
  - **X4 "offer don't decide" semantic gap** (`:80` undefined; sole-next-step framing weaponized) — MAJOR, "cleanest genuine finding, pure-words fix."
  - **X5 "on the human's behalf" laundering** (`:79`/`:107` scope-creep from `comment add` to baseline/handoff) — MAJOR, lexical rule.
- **Attackers:** A3-NEW (R2 MAJOR); A2 (X1/X2/X4/X5, all MAJOR in R2); A1 (confirms the gap is code-real).
- **Fix:** extend the never-do spine with an **authorship** clause: forbid recommendatory/sole-next-step
  narration at any gate; forbid the agent authoring the verbatim gate command string; define
  "offer, don't decide" operationally; tighten "on the human's behalf" to a closed set (comment text the
  human dictated) and bar its use for baseline / handoff.
- **Verifier note:** survives. This is the residual SKILL defect after F1; A1 confirms the underlying
  code gap, so the fix is real and not cosmetic.

### F4 — s2 x-ray propagates the same "refused server-side" overclaim with no forward-correction
- **Artifact:** `stages/02-define-and-flow-xray.md` (s2, governing context for the design).
- **Quote (`:141`, step-7):** "Human disposes; **Claude Code is refused server-side** if it tries (INV-3,
  AC-L0-6/10)". Also `:144` (step-10) "the strongest disposal-side ergonomic". §1.2 `:74` frames the SKILL
  as the contract while asserting "the gates are enforced server-side regardless."
- **Why MAJOR:** doc-vs-code drift in the upstream artifact that **seeds** F1, carried forward with **no
  forward-correction banner** (A3). s2 is governing context, so the drift propagates to every consumer.
- **Attackers:** A3 (R1 MAJOR, held R2); A1 (R2 endorses).
- **Fix:** add a forward-correction banner / inline note at §1.2, §3.2 (`:141`), §4.3 — identity is NOT
  enforced server-side; align with the F1 rewrite so consumers do not re-import the overclaim.
- **Verifier note:** survives; same code facts as F1, different artifact.

---

## MINOR

### F5 — RESULT §3.1 attaches the "web-ui default" to the wrong gate
- **Artifact:** `RESULT.md` §3.1.
- **Quote (`:53`):** "the **apply** gate refuses only the literal lowercased string `system:auto` … while
  the route defaults the actor to `"web-ui"`" — but the surrounding grammar attaches the web-ui default to
  the **approve** gate reasoning.
- **Why MINOR:** wording/precision. Per A1 (R1, held R2) the web-ui default is on the **apply** route only;
  the **approve** route uses `parseRequiredString` (throws `APPROVAL_METADATA_REQUIRED` if missing), no
  web-ui default. The conclusion (no identity check) is correct; the attribution is loose.
- **Attacker:** A1 (R1 raised, R2 kept).
- **Fix:** scope the web-ui-default clause to the apply route; note the approve route's distinct
  `parseRequiredString` / `APPROVAL_METADATA_REQUIRED` behavior.

### F6 — step-9/10 cells should lead with single-gate honesty (M2)
- **Artifact:** `RESULT.md` §3.4 (M2) / `stages/06-interaction-design.md` step-9/10 cells.
- **Quote (RESULT `:68`):** "mirror single-gate honesty into the step-9/10 table cells".
- **Why MINOR:** the two-gate narrowing **is** disclosed honestly elsewhere (SKILL `:85`; design §4.3
  `:264-271`; RESULT §2.4 `:45`) — A3 logs this as PASS/B1. The nit is ordering: the step-9/10 cells lead
  with the *target* two-gate behavior before the single-gate caveat.
- **Attacker:** A3 (R1 MINOR, held).
- **Fix:** lead the step-9/10 cells with the runnable single-gate reality, then name the two-gate as target.

### F7 — Design §3 table-cell superlatives assert ergonomic gain (C2)
- **Artifact:** `stages/06-interaction-design.md` §3 — the **step-3 and step-10 table cells** (Popper R2 location correction: these are table cells, not "§3 prose").
- **Quotes:** "the single biggest cold-start win" (`:215`); "the strongest control-side ergonomic" (`:222`).
- **Why MINOR:** wording in tension with charter clause 5 + RESULT §3.3 "no ergonomic gain asserted
  anywhere" (`:61`). Superlative framing, not a settled claim — but it reads as an unproven ergonomic assertion.
- **Attacker:** A3 (R1 MINOR C2, held R2; unaffected by A2).
- **Fix:** soften to hypothesis framing (e.g., "expected to be …, pending the cold-start study") consistent
  with the `human_study` class the same cells carry.

### F8 — Gate-count framing differs across artifacts (D1) — *reworded after verification*
- **Artifact:** `06-SKILL-draft.md` vs `stages/06-interaction-design.md` §0 / s2 §3.3.
- **Quotes:** SKILL `:59` "five are durable gates … one is terminal"; design §0 `:53` / s2 §3.3 `:150`
  treat "handoff = 5th gate".
- **Why MINOR:** stale/fuzzy. Same disposed-set {4,7,9,10,12}; the SKILL frames it "5 gates + 1 terminal"
  while design/s2 fold handoff into "5 durable gates".
- **Verifier correction (Popper R2):** the finding's *original* load-bearing evidence — "the SKILL table
  lists **6** NO-rows" — **does not reproduce**: the command table has **5** `NO — human gate` rows
  (`:82` select, `:83` commit, `:84` approve, `:85` apply, `:86` handoff). That miscount is **dropped**.
  The residual true nit: the table splits `baseline` into two command-rows (`select`/`commit`) while the
  prose counts baseline as one gate — a far weaker observation than originally stated.
- **Attacker:** A3 (R1 MINOR D1, held R2); **partially refuted by Popper (R2)**.
- **Fix:** state one count convention once; note `baseline` = two commands at one gate. (Lowest priority.)

---

## Per-artifact verdicts

| Artifact | Surviving CRITICAL | Surviving MAJOR | Verdict |
|---|---|---|---|
| `stages/06-interaction-design.md` (interaction design) | F1 | (F7 MINOR) | **FIX** |
| `06-SKILL-draft.md` (SKILL draft) | — | F3 | **FIX** |
| `RESULT.md` | — | — (only F5/F6 MINOR) | **KEEP** |
| `stages/02-define-and-flow-xray.md` (s2, governing context) | — | F4 | **FIX** (precondition to the F1 design fix; s2 is governing context, not a primary target) |
| **Core** (routed, not a target doc) | — | — | **build-blocking ROUTE** (F2 / R-S7-1) |

Verdict rule applied: FIX iff >=1 surviving CRITICAL or MAJOR.

## Change-request count by severity (post-verification)

- **CRITICAL: 1** — F1 (design step-7 phantom backstop, doc-fix).
- **MAJOR: 2** — F3 (SKILL authorship-silence) + F4 (s2 propagation, precondition to F1).
- **MINOR: 3** — F5 (RESULT §3.1 grammar), F6 (step-9/10 ordering), F7 (ergonomic superlatives).
- **Build-blocking ROUTE: 1** — F2 (core identity gate / R-S7-1), distinct from the doc change-request tally.
- **Partially refuted / reworded: 1** — F8 (gate-count; the "6 NO-rows" evidence dropped by Popper, residual weak MINOR).

**Total: 7 surviving change requests + 1 build-blocking ROUTE.** A2's two initial CRITICALs (X1, X2)
relaxed to MAJOR and fold into F3; the root defect (no server-side identity gate) is counted as its
distinct consequences (F1 doc, F3 SKILL, F2 core ROUTE), not triple-counted as independent criticals.

## Verifier disposition (zig-zag, both turns terminated with no further objection)
- **F2** — Gödel: reclassified CRITICAL → **build-blocking ROUTE** (P10 — severity ranks target edits; F2
  closes by no target edit). Applied above.
- **F8** — Popper: the "**6** NO-rows" evidence **does not reproduce** (table has 5); dropped as authored,
  reworded to the residual weak MINOR. Applied above.
- **F7** — Popper: location-label correction (table cells, not "§3 prose"). Applied above.
- **F4** — Gödel: stays MAJOR; reframed as a **precondition** to F1 (s2 is governing context). Applied above.
- **F1, F3, F5, F6** — both verifiers: SURVIVE, calibrated, claim ≤ proof. No change.
