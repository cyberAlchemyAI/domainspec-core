---
id: refine-seed-operating-contract-type
project: ui-prototyping-studio
title: "Refine Seed — the 'operating-contract' artifact class vs Craft; do we need another type?"
status: seed
node_type: refine-seed
run_id: 20260617-operating-contract-type
updatedAt: 2026-06-17
---

# Refine Seed — operating-contract type vs Craft

## Target

The artifact class identified as **framework-gap #6**: a *project-local operating contract for an
agent-as-engine* (instance: `06-SKILL-draft.md`). Characterize it, compare it against **Craft**
(`arcana/craft/` — the recursive-ledger method primitive and its type system) and the other type
registries, and **decide whether we need to define another type**.

## The question, sharpened

There are three distinct "type" registries in the repo, and the artifact keeps almost-fitting and
falling out of each:
1. **Capability taxonomy** — formulae/transmutation/arcana; sigil/spell. (Already ruled out: not a
   sigil, not a spell.)
2. **`artifact_type`** (ARTIFACT-METADATA-CONSTITUTION) — kinds of artifacts (`constitution`/`schema`/
   `skill-contract`/…). #6 proposes adding `operating-contract` here.
3. **Craft ledger type system** (CRAFT-LEDGER-TYPE-SYSTEM) — types *ledger conditions*
   (blocker/gate/enabler + operational lane → role), plus `typed_items` for ledger entries.

So "do we need another type?" = which registry (if any) owns "an operating contract for an
agent-as-engine," and does it already have a slot — or is a new type warranted?

## Standing prior (must be honored, not silently overturned)

#6 was **deferred** (handoff `20260617T021958Z-framework-enforcement-honesty`): single instance, and the
metadata constitution is itself `candidate` with no validator. The "is it a spell?" turn added a new
*angle* but not a second *instance*. The bar set was **≥2 instances** before modeling the class.

## Source context (local-first)

- `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md` (the `artifact_type` enum + status).
- `arcanum/development/craft/CRAFT-LEDGER-TYPE-SYSTEM.md`, `arcana/craft/` (Craft method + ledger types).
- `arcana/spellcraft/README.md` + the sigil/spell defs (capability taxonomy).
- `06-SKILL-draft.md` (the instance) + the conformance audit + the #6 deferral handoff.

## What this run must produce

- An **x-ray** of the three type registries placing (or failing to place) the artifact in each.
- A **tournament** of the candidate homes: (A) new `operating-contract` artifact_type; (B) reuse an
  existing slot (`skill-contract` / Craft typed-item); (D) **defer** (hold the prior).
- A **decision** (define / reuse / defer) with rationale, honoring the standing prior, decision-gate-ready.
- If "define": where it lives + that it is a proposal to public arcanum (route via sigil-development --reflect).

## Run parameters

- **Preset:** standard. **Research:** no-research (all evidence local).
- **Write scope:** this run folder (private parent). Any arcanum change is proposal-only.
- **Validation surface:** the tournament pareto judgment + the standing-prior consistency check.
- **Overlays:** x_ray (registry structure) · tournament + pareto_gate (candidate homes) · dialectic +
  residue_ledger (define-vs-reuse) · memory_loop (the #6 deferral prior) · baseline sequence /
  owner-boundary (arcanum public) / observability.
