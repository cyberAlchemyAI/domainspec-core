---
id: result-operating-contract-type
project: ui-prototyping-studio
title: "RESULT — operating-contract type vs Craft; do we need another type?"
status: pass
node_type: refinement-result
run_id: 20260617-operating-contract-type
dispatch_id: refine-ups-operating-contract-type-20260617
capability_ref: refine
updatedAt: 2026-06-17
---

# RESULT — do we need to define another type?

## Answer

**No — we do not need to define another *framework* type now. But there is a real, cheap thing to do:
give the artifact a one-line *name* (denotation), not a type (enforcement).**

The question conflated two axes. Separating them dissolves it:

- **Typing (enforcement) — DEFER.** A new `artifact_type: operating-contract` would buy *nothing
  enforceable today*: ARTIFACT-METADATA-CONSTITUTION is `lifecycle_status: candidate`, every rule in it
  is `candidate`/`future`, and there is no validator or metadata parser. With n=1 (and that one instance
  *unreviewed* — residue R-S7-3), minting a type is classification theater. All three advocates agree the
  enforcement payoff now is ~0. The standing #6 prior (≥2 instances + a validator) **holds**.
- **Naming (denotation) — DO NOW, cheaply.** The genuine recurring cost is that the artifact is
  *unclassified*, so every reader re-runs the "is it a sigil? a spell?" disambiguation (this very session
  did, twice). That cost is **per-reader, not per-instance**, so the ≥2-instance trigger never retires it.
  The fix is a single co-located sentence, not a framework type.

## How it compares with Craft (the explicit ask)

Craft is the **wrong registry for the artifact's *kind*** and the **right registry for *tracking* it**:
- Craft's type system types **ledger conditions** (blocker/gate/enabler + operational lane → role) and
  **ledger entries** (`typed_items`) — not artifact kinds. So Craft cannot answer "what kind of artifact
  is this"; only the `artifact_type` enum can.
- Craft *can* hold the artifact's **governance/placement** as a context-specific `typed_item` (e.g. a
  `design`/`authority`-lane item) with **no enum amendment** — that is exactly what Craft's
  context-specific subtypes are for. So Craft complements the answer; it does not absorb the type question.

Net: the operating-contract is a third kind on the **artifact-kind** axis (not sigil, not spell, not a
Craft condition); Craft is where you'd *track* it, the `artifact_type` enum is where you'd eventually
*classify* it.

## Decision (decision-gate-ready)

1. **Defer the framework `artifact_type: operating-contract`** behind the existing trip-wire, now sharpened:
   *flip when a 2nd consuming project grows the same shape (an AI agent bound as propose-only engine of a
   host app via a CLI seam with human gates) OR a `skill-contract` validator needs to branch on
   product-bound-vs-portable.* At that point it is the right home (the x-ray confirms the enum owns "kind",
   and the instance is genuinely distinct from `skill-contract`).
2. **Record a one-line disambiguation note now**, co-located with the artifact (denotation, not a type):
   *"operating-contract — a project-local contract binding an AI agent (Claude Code) as the propose-only
   engine of a consuming app via a CLI seam with human gates; NOT a sigil, NOT a spell, NOT a Craft
   condition."* Ends the recurring confusion for ~0 cost, no framework change.
3. **Interim classification (reuse, per advocate B):** treat the instance as `skill-contract`-family with
   a project-local `owner`/scope qualifier, and (optionally) track its governance as a Craft
   context-specific `typed_item`. No new enum value.

## Stage evidence (this run)

- s1 context / s2 define+x-ray: the three-registry x-ray (stages/05 §x-ray) — pass.
- s3 review: the binary "define vs reuse vs defer" framing flagged as conflating naming with typing — pass.
- s4 research: no-research (all local) — pass.
- s5 distill/tournament: 3 advocates (A/B/D) + pareto judgment — pass (stages/05-tournament.md + agent receipts).
- s6 design/dialectic + s8 repair: the naming-vs-typing split is the synthesis; residue carried — pass.
- s9 plan: the 3-part decision above is the non-executed plan — pass.
- s10 final synthesis: this document — pass.

## Honoring the prior

The #6 deferral is **upheld, with cause and a sharpened trigger** — not overturned. What changed is only
that we now pay the *naming* cost (which the deferral had silently left on every future reader) without
paying the *typing* cost (which buys nothing until a validator + a 2nd instance exist).

## Recommended next routes

- **Now (cheap, in-bounds):** add the one-line disambiguation note to `06-SKILL-draft.md` frontmatter/intro
  (and optionally the project glossary). Offered, not executed by this refine run.
- **On trigger:** `sigil-development --reflect` to add the `operating-contract` `artifact_type` (folds
  into the existing framework-improvement handoff `20260617T021958Z`, candidate #6) when a 2nd instance or
  a `skill-contract` validator-branch appears.
- **Optional:** register the instance as a Craft context-specific `typed_item` for governance tracking.
