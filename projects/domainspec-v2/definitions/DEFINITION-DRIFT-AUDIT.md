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
| relationship signature authority | DEFINITIONS.md#ds-d8; relationships.yml `signature_count=31` | yes → `DS-D8` | active | `pass` | endpoint, scope, multiplicity, projection-authorship, and schema-participation checks root authority |
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
| relationship source-effect binding | historical DS-D8 `creates`; DEC-DSV2-OPERATION-CREATES-ENTITY | yes -> `domainspec-v2-D26` | superseded | `pass` | stable historical ID; replaced by edge-canonical generated projection |
| Canonical Single Responsibility Principle | DS-D8 `creates`; DEC-DSV2-CANONICAL-CREATION-RESPONSIBILITY | yes -> `domainspec-v2-D27` | active | `pass` | one primary responsibility, one canonical owner, one authored proposition; `creates` is the executable application |
| DomainSpec obligation lifecycle | GATE-05 separate owner-local lifecycles | yes -> `domainspec-v2-D28` | active | `pass` | closed owner-event fold; currentness and decision dispositions remain separate |
| meta-type realization | current implementation state; frozen baseline realization rows | yes -> `domainspec-v2-D31` | active | `pass` | exact type/language/source/provider/binding identity; not a semantic meta-type |
| canonical implemented meta-type baseline | owner definitions-first decision; current implementation state | yes -> `domainspec-v2-D32` | active | `pass` | immutable versioned set; @1 and @2 retained as historical and @3 is current |
| meta-type instantiation | WP-MTCLI-001; private CLI | yes -> `domainspec-v2-D33` | active | `pass` | closed decoder, artifact plan, guarded atomic publication, receipt, reread, and deterministic package replay implemented |
| target implementation conformance | implementation-conformance ontology; private CLI observer | yes -> `domainspec-v2-D34` | active | `pass` | selected baseline versus observed generated target implemented at the admitted static boundary |
| baseline-bound instantiation receipt | WP-MTCLI-001; private CLI receipt schema and replay | yes -> `domainspec-v2-D35` | active | `pass` | exact input, selection, outputs, reread observations, and conformance binding implemented |
| Workflow Compensation | canonical runtime contract; three-profile generator and observer | yes -> `domainspec-v2-D36` | active | `pass` | forward-recovery Operation role; no new DS-D1 type or DS-D8 verb |

## Gate
- `pass`: every load-bearing term resolves to a tracked, grounded entry.
- `flag`: an owed term is named as a gap but not yet exercised as authority.
- `block`: a load-bearing term is used as authority with no tracked card — stop until it is created.

## Current verdict: pass
The 2026-07-16 FPR-01 reconciliation passes. `DS-D1` now resolves to one active machine registry and one
three-voice human companion with 13 active backend types, an explicit superseded `DS-D1.10` tombstone, nine
non-active UI candidates, and two differentiated deferred UI dispositions. The index carries every stable ID
without presenting the staged labels as a contiguous active set.

The relationship-definition sync also passes: `DS-D2`, `DS-D8`, `domainspec-v2-D9`,
`domainspec-v2-D19`, and `domainspec-v2-D27` resolve to the root authority's 31 active signatures,
bounded typed-composable-graph wording, and edge-canonical partial-one-to-one `creates` application.
`domainspec-v2-D26` remains as a superseded stable historical ID; no active signature uses its former
dual-authored source-effect binding.

The sibling governance-kind gap is closed: `layering governance` resolves to `domainspec-v2-D16`, and
`drift governance` resolves to `domainspec-v2-D17`. Both are active local RATIFIED kinds with the same L2
attestation-seal boundary as `validation governance` (`domainspec-v2-D2`). The pending L2 seal remains
promotion-boundary residue, not definition drift.

The R3 relationship wording gap is closed: `relationship non-collapse test` resolves to `domainspec-v2-D18`,
and `typed composable graph fragment` resolves to `domainspec-v2-D19`. The D18 property split is also tracked:
`domainspec-v2-D20..D25` define the six consequence properties a new relationship must cite before promotion.
This imports the CAV2 non-collapse discipline into DS-D2/DS-D8 without promoting full category law.

The proof-substrate lifecycle term now resolves to `domainspec-v2-D28`. A focused current-authority and
implementation-spec scan found no competing obligation transition table. Existing uses of `killed` for a
detected mutation and `resolved` for an ordinary decision are different typed terms; they do not define an
obligation state. Historical research, reviews, receipts, and staged planning copies remain evidence rather
than current lifecycle authority. Reducers, schemas, validators, and projections remain implementation work
and cannot claim D28 conformance until they enforce its closed transitions and owner-only event admission.

The meta-type implementation-state vocabulary now resolves to `domainspec-v2-D31..D35`. DS-D1 semantic
maturity, implementation-baseline admission, and generated-target conformance are separate axes. The current
machine state is schema-checked against the exact immutable baseline manifest; historical form-queue and
provider/profile findings remain provenance and do not silently regain control of the current baseline.

Workflow compensation now resolves to `domainspec-v2-D36`. Its canonical runtime contract keeps Workflow
evaluation intent-only, reuses `orchestrates` to bind exact Operation targets, preflights the complete executor
registry before mutation, and preserves each Operation's declared effect and failure-continuation boundary.
Durable dispatch across process restart remains product residue rather than being inferred from the in-process
reference executor.

Focused stale scan (2026-07-22): the owned definition/index/audit/meta-type surfaces carry no live 25-label,
14-backend, uniform-UI, or 30-signature authority claim. Candidate/deferred status is not treated as
validation, and unresolved UI correction routes remain visible rather than being laundered into active
authority. Historical review and receipt snapshots retain their dated counts and digests as evidence rather
than current authority.

The same scan repaired current narrative consumers in
`impl/spec/meta-types/LEARNING-ORDER.md`,
`impl/governance/tags/CODE-TAG-COMPOSABILITY-PATTERNS.md`,
`development/architecture-pattern-enforcement/cards/relationships/README.md`,
and `formalization/README.md`. Stale research, review, receipt, and run artifacts
remain dated evidence rather than current authority. The removed
`impl/spec/RELATIONSHIPS.md` projection is no longer cited by canonical cards.

M2-C1 aggregation emits [CONCEPT-REGISTRY.json](./CONCEPT-REGISTRY.json): 37
DS-D1 concepts and 34 DS-D8-valid edges, with zero duplicate IDs and zero type
drift. The intentionally empty sample pack's local `Fixture` label is reported
as one excluded non-DS-D1 concept, not promoted or silently merged.

Validation evidence (2026-07-22): `definitions:aggregate`, `validate:rels`
(5 specs / 34 edges / 31 signatures), `validate:content` (37 concepts / 34
edges / 22 schemas), documentation links, TypeScript, sample lint, 160/160
tooling tests, 15/15 code-tag tests, and 107/107 engine tests all pass.

## Resolved consumer conflict

`DEC-DSV2-ENFORCES-CROSS-FEATURE-SCOPE` closes the former `enforces` conflict.
The active tuple now admits `same-feature` and `cross-feature`, matching its
semantics, `enforces-cross` deprecation record, `relationships.md`,
`impl/spec/meta-types/LEARNING-ORDER.md`, and
`impl/governance/tags/CODE-TAG-COMPOSABILITY-PATTERNS.md`. A positive
cross-feature relationship fixture passes with the canonical `enforces` verb;
the deprecated alias remains a failing code-tag control. No conflicting current
consumer remains in this class.

<!-- Emitted live: the audit runs the moment the domain has terms. Re-run when cards are added/changed. -->
