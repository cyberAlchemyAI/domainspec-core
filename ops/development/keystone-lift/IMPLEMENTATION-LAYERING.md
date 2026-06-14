---
module: keystone-lift
version: current
status: draft
updatedAt: 2026-06-14
docType: implementation-layering
---

# Implementation Layering: Keystone Lift (DomainSpec template + taxonomy/definitions wedge → public arcanum)

## Purpose
Keep L0 minimal: prove the DomainSpec wedge (template + definitions) can live coherently in public arcanum **before** cutting over invoke's default or removing Module Formulae. Promote only on evidence.

## Source Contract
- Decision basis: [../domainspec-arcanum-build-decisions.md](../domainspec-arcanum-build-decisions.md) (B1/B2/B3 + C1/C2/C3)
- Evidence basis: [../domainspec-wedge-inventory.md](../domainspec-wedge-inventory.md)
- Transmutation: `arcanum/transmutations/implementation-layering/`

## Target And Scope
- Target: keystone-lift
- Scope: feature (cross-repo — public `arcanum` + private `implementation/domainspec`)
- Current state: greenfield in arcanum (definitions absent); brownfield in invoke (Module Formulae present)

## Layer Boundary Rule
`After this layer, we know whether {decision unlocked}.`

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| **L0 (POC)** | After this layer, we know whether the DomainSpec **wedge definitions** + **SPEC template** can live coherently in public arcanum. | Lift DS-D1/DS-D2 (25 types + 29 edges) into `arcanum/definitions/` as canonical (collision-safe IDs) **and** place the sanitized DomainSpec SPEC+aspect templates in invoke's template dir — **without** cutting over invoke's default. | DS-D1/D2/D3/D7/D8/D10/P1-3 lift; template placement; sanitization of those artifacts. | invoke cutover; prose recompose; Module Formulae removal; DS-side references. | arcanum link-checker + definitions-index green on new defs; templates render; zero moat terms present. | continue / pivot / stop |
| **L1** | After this layer, we know whether invoke `define` can produce DomainSpec-format specs end to end. | Wire `define` to the DomainSpec template (cutover), update SKILL.md + `define.md` "Module Formulae baseline" text, add discovery-existence soft gate. | invoke contract + routing changes; discovery soft gate w/ `--skip-discovery` waiver. | full Module Formulae removal; downstream pipeline sigils. | one `define` dry-run emits a DomainSpec SPEC + aspect docs referencing canonical IDs. | harden / narrow / stop |
| **L2** | After this layer, we know whether the split holds under governance with **no moat leak**. | Complete the DEFINITIONS.md split (moat cluster stays private; DS references arcanum); recompose prose as example layer; pass the g05 whole-diff moat-leak + sanitization audit. | DS-side reference rewrite; D4/D5/D6 held private; prose→example; moat-leak audit. | packaging for dependent pipeline. | g05 whole-diff audit green; DS references resolve; no moat term/ID/private-path public. | scale / remediate / stop |
| **L3** | After this layer, we know whether the keystone is packaged for the dependent pipeline (M1 items that read the template). | Remove the Module Formulae family; update all references; confirm a stable spec contract for test-engine/doc→metrics/sync-registry to build on. | `module-formulae/` removal; dev-doc/craft reference updates; contract freeze. | M2 pipeline sigils (separate plan). | no `module-formulae` references remain; arcanum gates green; contract documented for M2. | proceed to M2 pipeline |

## Non Regression Guardrails
- Later layers preserve earlier guarantees: once the moat-leak audit passes (L2), no L3 change may reintroduce a moat term/path.
- Deferred scope stays explicit: D4/D5/D6 stay private until proven decoupled (do not pull into L0/L1).
- Promotion cites evidence (validator output / dry-run), not preference.
- Submodule-first discipline: arcanum changes commit+push in arcanum before any parent gitlink bump (`make bump-check`).
