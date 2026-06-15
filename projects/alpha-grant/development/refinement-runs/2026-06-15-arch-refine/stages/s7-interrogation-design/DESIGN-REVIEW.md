# s7 — Interrogation (refine-design-review)

- Capability: `interrogation` · Mode: `refine-design-review`
- Receipt kind: native-stage · Status: `flag` (proceed; repairs named for s8)
- Inputs: `stages/s6-invoke-design/DESIGN.md`, `tension-residue.md`
- Boundary auditor cross-check applied (O1–O6)

## Q1 — Does the design actually encode O1–O6 structurally, or restate them?

**Pass with note.** Each boundary now attaches to a place (node/asset/ask) with a
fail-action, and O2/O4/O6 are blocking. This is structural, not cautionary.
**Repair R-a:** the table lists fail-actions but the design does not say *who*
runs the blocking check at outreach time. Name the gate owner (N1 board for O4;
N5 QC + N1 sign-off for O2/O6) in the plan.

## Q2 — Is the authority/ownership split (F1) enforceable, or aspirational?

**Flag.** The rule is clear, but enforceability depends on the entity-home: only
`new-nonprofit` enforces O4 by *charter*; `fiscal-sponsor` enforces by *envelope*;
a service agreement enforces by *contract*. The design recommends the staged route
but doesn't state the **minimum enforceable artifact** for the Stage-1 (fiscal
sponsor) period. **Repair R-b:** require a signed asset-ownership agreement (N1
owns accessions; N5/FIT operates by service contract) as a Stage-1 precondition,
so F1 is enforced contractually before the nonprofit charter exists.

## Q3 — Does the recomposition contract (three connectors) actually hold for the hardest lane?

**Pass.** Tested against N4 Houston (the hardest): C1 shared accession standard ✓,
C2 MTA-governed asset use ✓, C3 UH sponsored-research entity-home ✓. Houston
recomposes without crossing O3/O4 *provided* the MTA exists — which is gated by
O2 (verification status). Consistent.

## Q4 — Is residue Z1 (outreach timing) safe to leave open into the plan?

**Flag.** Z1 is the one residue that affects near-term action. Leaving it fully
open risks an outreach step starting before entity-home approval. **Repair R-c:**
the plan must encode the *safe default* explicitly — parallel preparation is
allowed; funder **contact** is blocked until (g7 entity-home approved) AND
(partner verification-status ≥ written). This converts the residue into a guarded
default, not an open question.

## Q5 — Any boundary the design still risks crossing in its own framing?

**Pass.** The design keeps KU/INVAM as protected, frames Houston as research node,
and never lists commercial revenue in the N1 budget. The boundary-auditor's
highest-likelihood hotspot (N5/FIT defaulting to "owner") is directly addressed by
the authority/ownership split. No self-inflicted crossing.

## Outcome

- Status: `flag` — design is sound and boundary-faithful; three repairs (R-a gate
  owners, R-b Stage-1 enforceable artifact, R-c Z1 guarded default) go to Distill
  Repair (s8) before planning.
- No new external-context gap (research decision unchanged).
