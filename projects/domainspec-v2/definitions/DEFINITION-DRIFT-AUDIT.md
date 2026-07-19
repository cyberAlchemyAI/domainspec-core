<!-- MINT-BASELINE BACKFILL (2026-07-01) for domainspec-v2 — cast from templates/definition-drift-audit.md
     (Tier-1 addition #8, SWU-5), which post-dates v2's 2026-06-29 first mint. INTERNAL/private.
     INHERITS the drift-audit PROCEDURE + report FORMAT; LOCALIZES the audited terms. -->

# DomainSpec v2 Definition Drift Audit

Status: active (review-mode; a deterministic scan is a domain follow-up)
Owner: definitions-governance (domain-local)
Reconciles: [DEFINITIONS.md](./DEFINITIONS.md) against [DEFINITIONS-INDEX.md](./DEFINITIONS-INDEX.md), with
DS-D1 machine/human authority cross-checked against [meta-types.yml](./meta-types/meta-types.yml) and
[meta-types.md](./meta-types/meta-types.md), and DS-D8 cross-checked against
[relationships.yml](./relationships/relationships.yml)
Authority: this audit is the enforcement target named by the constitution's Load-Bearing Term Tracking
rule (`C(meta-4)`).

## What this audit checks
A **load-bearing term** = a symbol/named quantity in a formal expression, a fixture FAIL-region, a
candidate invariant, a decidable rule, a governance-kind name carrying authority, or the normative content
of a claim-ledger entry. For every load-bearing term used in the repo's definitions surface:

1. **tracked?** — does it have a row in `DEFINITIONS-INDEX.md` resolving to a card in `DEFINITIONS.md`?
2. **grounded?** — if the card is `candidate`, does it carry an `Open / to-ground:` field?
3. **non-collapsed?** — `candidate` status is not treated as validation.
4. **property-split?** — if a definition uses a closed set of load-bearing properties, each property has
   its own tracked row or is explicitly declared non-load-bearing.

A term failing (1) is a **drift defect** — create it as a `candidate` card + index row (stage in
`reviews/`), do not use it as authority until grounded.

## Audit ledger
| Load-bearing term | First cited in | Tracked (index row)? | Card status | Verdict | Route |
| --- | --- | --- | --- | --- | --- |
| drift / convergence | DEFINITIONS.md#domainspec-v2-d1 | yes → `domainspec-v2-D1` | active | `pass` | — |
| validation governance | DEFINITIONS.md#domainspec-v2-d2 | yes → `domainspec-v2-D2` | active | `pass` | — |
| edge-law admissibility | DEFINITIONS.md#domainspec-v2-d3 | yes → `domainspec-v2-D3` | active | `pass` | — |
| executable typed graph | DEFINITIONS.md#domainspec-v2-d4 | yes → `domainspec-v2-D4` | active | `pass` | — |
| two-plane boundary | DEFINITIONS.md#domainspec-v2-d5 | yes → `domainspec-v2-D5` | active | `pass` | — |
| meta-type system | DEFINITIONS.md#ds-d1; meta-types.yml | yes → `DS-D1` | active | `pass` | 24 staged labels; maturity is explicit per slice |
| backend meta-types | meta-types.yml `members` | yes → `DS-D1.1..9`, `DS-D1.11..14` | active | `pass` | exact non-contiguous 13-member active set |
| retired DS-D1.10 stable ID gap | meta-types.yml `superseded.DS-D1.10` | yes → `DS-D1.10` | superseded | `pass` | historical ID retained; reuse forbidden |
| UI candidate meta-types | meta-types.yml `maturity.ui.candidate` | yes → `DS-D1.15..23` | candidate | `pass` | nine shape-evidenced labels remain explicitly non-active |
| Adapter | meta-types.yml `maturity.ui.deferred` | yes → `DS-D1.24` | deferred/merge-candidate | `pass` | collapse toward Mapping remains unresolved by definitions owner |
| State Indicator | meta-types.yml `maturity.ui.deferred` | yes → `DS-D1.25` | deferred/split-candidate | `pass` | domain-state/async-state split remains unresolved |
| edge-participation signature | DEFINITIONS.md#domainspec-v2-d9 | yes → `domainspec-v2-D9` | active | `pass` | method term now cites `DS-D8`; no alias drift |
| relationship verb set | DEFINITIONS.md#ds-d2; relationships.yml active signatures | yes → `DS-D2` | active | `pass` | root relationship authority owns canonical labels |
| relationship signature authority | DEFINITIONS.md#ds-d8; relationships.yml `signature_count=30` | yes → `DS-D8` | active | `pass` | endpoint validator + schema participation consistency check root authority |
| layering governance | AUTHORITY-MODEL.md; CONSTITUTION.md C6; reformulate-batch1 L1 | yes -> `domainspec-v2-D16` | active | `pass` | RATIFIED local governance kind; L2 seal still pending |
| drift governance | AUTHORITY-MODEL.md; CONSTITUTION.md C7; DRIFT-CONVERGENCE.md; DEFINITIONS.md#domainspec-v2-d1 | yes -> `domainspec-v2-D17` | active | `pass` | RATIFIED local governance kind; L2 seal still pending |
| relationship non-collapse test | relationships.yml; relationships.md; R3 category-boundary findings; D3 | yes -> `domainspec-v2-D18` | active | `pass` | new/disputed relationship labels need a tracked D20-D25 property before promotion |
| typed composable graph fragment | relationships.yml `category_wording`; relationships.md; DS-D8 | yes -> `domainspec-v2-D19` | active | `pass` | current R3 graph wording; full category law remains a future route |
| reject/allow decision | DEFINITIONS.md#domainspec-v2-d18 property set | yes -> `domainspec-v2-D20` | active | `pass` | validator/fixture/owner-gate outcome property |
| derivation consequence | DEFINITIONS.md#domainspec-v2-d18 property set | yes -> `domainspec-v2-D21` | active | `pass` | public obligation/test/check derivation property |
| projection consequence | DEFINITIONS.md#domainspec-v2-d18 property set | yes -> `domainspec-v2-D22` | active | `pass` | governed view/read-model/projection property |
| composition path consequence | DEFINITIONS.md#domainspec-v2-d18 property set | yes -> `domainspec-v2-D23` | active | `pass` | finite DS-D8 path/code-connection property |
| owner route consequence | DEFINITIONS.md#domainspec-v2-d18 property set | yes -> `domainspec-v2-D24` | active | `pass` | changed owner/gate/remediation-route property |
| generated artifact consequence | DEFINITIONS.md#domainspec-v2-d18 property set | yes -> `domainspec-v2-D25` | active | `pass` | changed generated output/provenance property |

## Gate
- `pass`: every load-bearing term resolves to a tracked, grounded entry.
- `flag`: an owed term is named as a gap but not yet exercised as authority.
- `block`: a load-bearing term is used as authority with no tracked card — stop until it is created.

## Current verdict: pass
The 2026-07-16 FPR-01 reconciliation passes. `DS-D1` now resolves to one active machine registry and one
three-voice human companion with 13 active backend types, an explicit superseded `DS-D1.10` tombstone, nine
non-active UI candidates, and two differentiated deferred UI dispositions. The index carries every stable ID
without presenting the staged labels as a contiguous active set.

The relationship-definition sync also passes: `DS-D2`, `DS-D8`, `domainspec-v2-D9`, and
`domainspec-v2-D19` resolve to the root authority's 30 active signatures and bounded typed-composable-graph
wording.

The sibling governance-kind gap is closed: `layering governance` resolves to `domainspec-v2-D16`, and
`drift governance` resolves to `domainspec-v2-D17`. Both are active local RATIFIED kinds with the same L2
attestation-seal boundary as `validation governance` (`domainspec-v2-D2`). The pending L2 seal remains
promotion-boundary residue, not definition drift.

The R3 relationship wording gap is closed: `relationship non-collapse test` resolves to `domainspec-v2-D18`,
and `typed composable graph fragment` resolves to `domainspec-v2-D19`. The D18 property split is also tracked:
`domainspec-v2-D20..D25` define the six consequence properties a new relationship must cite before promotion.
This imports the CAV2 non-collapse discipline into DS-D2/DS-D8 without promoting full category law.

Focused stale scan (2026-07-16): the owned definition/index/audit/meta-type surfaces carry no live 25-label,
14-backend, uniform-UI, or 31-signature authority claim. Candidate/deferred status is not treated as
validation, and the unresolved UI correction routes remain visible rather than being laundered into active
authority.

<!-- Emitted live: the audit runs the moment the domain has terms. Re-run when cards are added/changed. -->
