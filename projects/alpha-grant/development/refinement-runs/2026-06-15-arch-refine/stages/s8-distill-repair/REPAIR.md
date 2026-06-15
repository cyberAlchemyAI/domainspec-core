# s8 — Distill Repair

- Capability: `distill` · Mode: `validate`
- Receipt kind: native-stage · Status: `pass`
- Inputs: `stages/s6-invoke-design/DESIGN.md`, `stages/s7-interrogation-design/DESIGN-REVIEW.md`

Applies the three repairs from s7 and re-checks the recomposition proof.

## R-a — Name the gate owners (was: fail-actions without an owner)

| Boundary gate | Blocking? | Owner of the check | When it runs |
|---------------|-----------|--------------------|--------------|
| O2 unverified partners | block | N5 QC flags → **N1 owner sign-off** required | before any outward ask/claim naming a partner |
| O4 public/private separation | block | **N1 board** (asset disposition) | before any cross-node budget or shared-asset ask |
| O6 funder exposure | block | **N5 QC + N1 owner** joint review | before any funder/program-officer contact |
| O1 / O3 / O5 | flag | N1 governance (O1, O5) / lane owner (O3) | at artifact authoring |

**Resolved:** every blocking gate has a named human owner.

## R-b — Minimum enforceable artifact for the Stage-1 (fiscal-sponsor) period

F1 (authority ≠ ownership) is enforced *before* the nonprofit charter exists by a
**Stage-1 asset-ownership agreement**, signed as a precondition to A1 Bridge
spending:

> N1 (under the fiscal sponsor's mission envelope) owns the accessions, vouchers,
> host cultures, database, and governance policy. FIT Farms / Golden Quill
> operate by service contract (routing, QC, proposal production) and hold no
> title and no board authority over asset disposition.

**Resolved:** O4/F1 is contractually enforceable on day one, not only after the
nonprofit determination.

## R-c — Convert residue Z1 into a guarded default

Outreach timing is no longer open. The guarded default:

> **Preparation in parallel is allowed** (concept notes for A1/A2/A3/A4/A5 may be
> drafted during the bridge period). **Funder CONTACT is blocked** until BOTH:
> (1) entity-home approved at gate g7, AND (2) the named partner's
> `verification_status ≥ written`.

**Resolved:** Z1 becomes a blocking guard in the plan, not an unresolved choice.
Z2 (endowment timing) and Z3 (contribution threshold) remain correctly deferred
post-spine with owners (no near-term action).

## Recomposition re-check (`recomposition_proof`)

Full network = Library Spine (N1 + A1 + A2 + entity-home) **+** extension lanes
via three connectors. Re-tested after repairs:

- N3 Field → C1 ✓ C2 ✓ (licensed) C3 ✓ (service agreement) — recomposes.
- N4 Houston → C1 ✓ C2 ✓ (MTA) C3 ✓ (UH sponsored-research) — recomposes, O3-safe.
- Lane 4 co-op → C1 ✓ C2 ✓ C3 ✓ (co-op program extension home) — recomposes.
- Lane 6 MycoFest → C1 ✓ C2 ✓ C3 ✓ (co-hosted w/ N1) — recomposes.
- Lane 7 endowment → deferred (Z2), not in spine.

No connector violation. Spine stands alone and recomposes.

## Repair verdict

`pass` — all three s7 repairs applied; recomposition holds; boundaries intact and
now owner-assigned. Ready for the non-executed plan.
