---
node_type: handoff
is_session: false
status: candidate
boundary: INTERNAL — invoke handoff (new-lifecycle-thread) for the governance-organ architecture
created: 2026-06-29
authored_by: invoke (mode: handoff)
handoff_type: new-lifecycle-thread
observed_capability: invoke
target_artifact: governance-organ architecture (authority-triage + Mint)
target_owner: sigil-development (authority-triage owner + Mint owner); decision-gate for the lane-vs-spell fork
source_session: 2026-06-29 — domainspec-v2 mint + the governance-organ design discussion
related_handoff: cyberAlchemy-v2/development/mint/development/handoffs/2026-06-29-first-real-mint-domainspec-v2.md
---

# Handoff — Governance-organs via authority-triage (the orthogonal-axes synthesis)

## Identity & source session

A design synthesis that emerged after the domainspec-v2 mint: *should each governance in a minted
authority model (drift / validation / layering) become a focused executable organ that controls its
definitions / disciplines / constitutions?* The precedent sweep landed on `authority-triage` as the
build-from-owned routing foundation. This packet hands that design to its next lifecycle. It mutates
nothing.

## New-session prompt

> Design the governance-organ architecture: reify a minted domain's governances as executable organs
> WITHOUT rebuilding routing (build-from-owned on authority-triage) and WITHOUT re-skinning the
> cross-cutting governance sigils. Resolve the lane-vs-spell fork, extend authority-triage if needed,
> and define how Mint emits governances as authority-triage owner-routes.

## Handoff type & route rationale

`new-lifecycle-thread` — this is a new design idea (a governance-organ layer) needing its own design
lifecycle, not just a fix to one sigil. It carries a blocker-level fork (lane vs spell) → first stop is
`decision-gate`, then `invoke design`, then `sigil-development` for the two capability threads.

## Context Builder selection summary

Selected only the synthesis claims + the two enhancement routes + the open decision; excluded the
domainspec-v2 mint mechanics (covered by the related Mint handoff).

## Obligation coverage matrix

| # | Obligation | Coverage | Evidence |
| - | --- | --- | --- |
| O1 | The core architectural claim | covered | Orthogonal-axes finding below. |
| O2 | What is already owned (don't rebuild) | covered | `authority-triage` (router; routes-not-owns; promotes-nothing). |
| O3 | The open decision | covered | Lane-vs-spell fork below. |
| O4 | The capability enhancements + next route | covered | Mint + authority-triage routes below. |

## Selected session context — the synthesis

**Core claim — two orthogonal axes.** `authority-triage` routes by **KIND** (definition / constitution /
discipline / decision) — cross-cutting. A governance-organ governs by **DOMAIN-GOVERNANCE** (drift /
validation / layering). These are orthogonal: **kind × governance**. authority-triage is therefore a
*component* of a governance-organ, not the organ.

**The integration (the "already started").** In a minted authority model, **the governances ARE the
owner-routes** (`validation-governance`, `drift-governance`, `layering-governance`). authority-triage
*routes candidates to owner-routes*. So inside a minted domain, authority-triage is already the
front-door that dispatches a candidate to its governance. A governance-organ =
**authority-triage (route) + the methods (exercise) + the constitution slice (enforce)** — compose the
router, don't rebuild it.

**The two guardrails authority-triage already proves (keep them).**
1. **Routes, doesn't own** — it writes nothing into an owner's surface; the definition/constitution/
   discipline LIFECYCLES stay with the cross-cutting governance sigils. A per-governance organ must
   likewise BIND/ENFORCE its slice, never re-own those kinds (that would re-skin them — the exact Mint
   F3(c) hazard).
2. **Promotes nothing** — the promotion DECISION stays with the owner (write-authority proviso /
   map-vs-decision non-collapse). An organ EXERCISES + ENFORCES; it does not decide promotion.

**Worked example (domainspec-v2).** Candidate "new derived-obligation rule" → authority-triage classifies
*kind = Constitution* → routes to narrowest owner = `validation-governance` → which (if a real organ)
enforces via the engine `derive`/`lint`. authority-triage + validation-governance compose; neither owns
the other's job.

## The open decision (route to decision-gate)

**Lane vs spell, per governance:**
- **(a) Lane** — the governance is a scope/tag the existing authority-triage dispatches on; owners stay
  the cross-cutting sigils + the methods. Lightest; no new capability.
- **(b) Spell** — a per-governance spell = authority-triage (route) + its methods + its constitution
  slice. Executable organ; more power, more surface.

Author's lean: **(a) default; (b) only where a governance does real composed enforcement** (e.g.
validation via the engine). Do not mint a spell that merely renames `constitution-governance`.

## Excluded context

The domainspec-v2 mint emit mechanics, the §7 results, and the import-triage — all in the related Mint
handoff; not repeated here.

## Target lifecycle / project boundary

Owner = `sigil-development` for the two capability threads + `decision-gate` for the fork. Proposal-only;
mutates neither `authority-triage` nor `Mint`. The domainspec-v2 spine is the worked instance, owned
separately.

## Gaps & blockers

- **authority-triage is unvalidated** — `development/VALIDATION-EXPERIMENT.md` is authored but **not
  run**; it is `status: candidate`, promotion-target `arcanum/arcana/`. Leaning on it for governance-organs
  means validating it first (build-from-owned **but not deployed**).
- **Governance-SCOPE is not in authority-triage today** — it routes by kind, not by a governance lane;
  option (a) needs a scope/lane concept added.
- **The lane-vs-spell fork is unresolved** (decision-gate).
- **The kind × governance orthogonality is a candidate design claim**, not validated.

## Next-session start prompt

> Resolve lane-vs-spell (decision-gate). Then `invoke design` the governance-organ layer:
> authority-triage gains a governance-scope/lane; Mint emits each minted governance as an
> authority-triage owner-route (lane by default, spell where real enforcement exists). Validate
> authority-triage (run its VALIDATION-EXPERIMENT) before depending on it.

## Next route

`decision-gate` (lane vs spell) → `invoke design` (governance-organ layer) → `sigil-development`
(authority-triage validate+extend; Mint emit-governances-as-owner-routes).

## Dispatch technique trace

`frame_handoff` · `handle_handoff` (route to decision-gate then design) · `owner_boundary_check`
(invoke authors; sigil-development owns the capabilities; decision-gate owns the fork) · `residue_ledger`
(gaps/blockers above) · `concrete_path_evidence` (cites authority-triage SKILL + VALIDATION-EXPERIMENT +
the domainspec-v2 spine). No full dispatch JSON needed (single handoff packet).

## Provenance & output paths

- Observed capability: `invoke` · Mode: `handoff` · Type: `new-lifecycle-thread`
- Output: `development/authority-triage/development/handoffs/2026-06-29-governance-organs-via-triage.md`
- Reflected on: `development/authority-triage/SKILL.md` + `development/VALIDATION-EXPERIMENT.md`;
  `cyberAlchemy-v2/development/mint/` (the emit side); `projects/domainspec-v2/authority/` (the worked instance).
