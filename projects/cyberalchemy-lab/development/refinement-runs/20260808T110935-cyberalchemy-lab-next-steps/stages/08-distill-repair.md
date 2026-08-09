# Stage 08 — Distill Repair

## Repair verdict

- Mode: `validate`
- Target: Stage 06 selected-unit-B design plus Stage 07 attack ledger
- Role path: parent-owned Proposer/Balancer simulation required by the confirmed Refine route
- Verdict: `pass`
- Evidence emission: `not-configured`; observability is outside the confirmed write scope
- Next route: Invoke Plan

The repair keeps the selected product boundary unchanged. It supersedes only underspecified canonicalization and fixture-validation details below.

## Repair 1 — Closed canonical JSON profile

Replace the architecture's generic RFC 8785 implementation reference with `cal-canonical-json-v1`:

- accepted JSON values: `null`, booleans, strings, arrays, objects, and integers in JavaScript safe range;
- floats, exponent notation, `NaN`, infinities, and negative zero are schema-invalid;
- all schema field names and object keys are printable ASCII and unique;
- object keys sort by ascending raw ASCII byte value;
- array order is preserved;
- strings serialize with the deterministic JSON escaping produced by ECMAScript `JSON.stringify` for one string value; UTF-8 encodes the result;
- objects contain no insignificant whitespace;
- a parser step rejects duplicate keys before ordinary `JSON.parse` materialization;
- every digest formula includes the profile ID and schema version.

This profile is deliberately smaller than general JSON canonicalization and can be implemented/tested without a new dependency or package root. A future broader number/key vocabulary requires a versioned profile and migration decision; it cannot silently reinterpret existing IDs.

## Repair 2 — Non-circular definition binding

The single fixture `DefinitionReference` binds:

- source: `projects/cyberalchemy-lab/development/research/2026-08-07-foundation/findings.md`;
- current source digest: `07a29e2fc62f92b6eb2d28c197b19c2ccc036a9952b75474f52c5ac9a44de11d`;
- selector: the Research Tower package definition under `Definition and non-goals`;
- binding status: `accepted-research-definition-reference`, not canonical-definition promotion;
- misuse warning: neither the fixture nor its projection may redefine Research Tower or infer canonical ownership.

The candidate cites accepted external evidence; it does not cite itself or the generated projection as definition proof.

## Repair 3 — Exact valid toy fixture

Planned fixture path: `fixtures/valid/synthetic-one-tower.json`.

Its source tree contains exactly one synthetic Research Tower at `fixtures/source/toy-tower/` with the seven owned spine files:

1. `README.md`
2. `TOWER.md`
3. `levels/L0-corpus.md`
4. `levels/L1-residue-map.md`
5. `levels/L2-closure-plan.md`
6. `gates/closure-gates.md`
7. `residue/open-residue.md`

The valid fixture cardinality is closed:

| Object | Exact count | Required state |
| --- | ---: | --- |
| `TowerPackageSnapshot` | 1 | complete ordered seven-artifact manifest; `fixture_class: synthetic-contract-fixture` |
| `SourceSnapshot` | 7 | one per artifact; exact bytes/digest/size; logical IDs stay distinct even for equal bytes |
| `Claim` | 1 | one falsifiable proposition sourced from the toy `L0-corpus.md`; candidate ceiling |
| `DefinitionReference` | 1 | external accepted research binding described above |
| `ResidueItem` | 1 | status `open`; blocks the candidate and promotion |
| `EvidenceAnchor` | 2 | one raw-byte anchor for the claim source and one for the external definition binding |
| `OntologyCandidate` | 1 | status `candidate`; review pending; `authority_effect: none` |
| `PromotionRecord` | 1 | one primary candidate; `gate_result: block`; no decision reference claiming approval |
| input `Relation` | exact required closure | `package_contains` for each record, `anchored_by`, `supports`, `references_definition`, and `blocked_by`; no inferred semantic edge |

The projection compiler adds `derived_from` edges for every projected snapshot/record dependency. It may not edit the input relation set or the blocked state.

## Repair 4 — Privacy scan

After field-level filtering and before atomic rename, the compiler recursively walks the final projection value and canonical serialized bytes:

1. reject any key outside the projection schema;
2. reject keys on the privacy policy's denied-key set at any depth;
3. reject exact denied locator/content values and configured byte-pattern sentinels;
4. require every projected record to carry `privacy_class` and the applied `privacy_policy_digest`;
5. prove the serialized object validates again after filtering;
6. fail without replacing an existing valid projection.

This is a bounded deterministic leak check, not a general privacy certification.

## Required deterministic mutant matrix

Each mutant changes one primary condition and maps to one stable failure code. A mutant passes only when compilation/validation fails with that code and emits no replacement projection.

| ID | Mutant | Expected failure code | Validation owner |
| --- | --- | --- | --- |
| M01 | Change one source byte but retain digest. | `CAL_SOURCE_DIGEST_MISMATCH` | compiler test |
| M02 | Set an anchor beyond source bounds or wrong selected-byte digest. | `CAL_SELECTOR_INVALID` | compiler test |
| M03 | Reuse one `source_snapshot_id` for a distinct logical source merely because bytes match, or add inferred `same_as`. | `CAL_IDENTITY_COLLAPSE` | compiler test |
| M04 | Reorder manifest artifacts while retaining `tower_snapshot_id`. | `CAL_TOWER_SNAPSHOT_STALE` | compiler test |
| M05 | Reference an absent relation endpoint. | `CAL_RELATION_DANGLING` | compiler test |
| M06 | Add an unknown record or relation kind. | `CAL_KIND_UNSUPPORTED` | schema/compiler test |
| M07 | Include a denied private locator/content field or sentinel in final projection. | `CAL_PRIVACY_EXPOSURE` | compiler/output scan |
| M08 | Change an input/rule/generator/privacy binding while retaining projection revision. | `CAL_PROJECTION_STALE` | projection validator |
| M09 | Supply a ValidationRecord whose exact input set/profile/command is missing or mismatched. | `CAL_VALIDATION_UNBOUND` | independent validator |
| M10 | Mark open residue or a contradiction dependency as cleared in projection. | `CAL_RESIDUE_STATE_MISMATCH` | projection validator |
| M11 | Change `authority_effect`, PromotionRecord gate/status, or assert promotion from projection. | `CAL_AUTHORITY_EFFECT_FORBIDDEN` | schema/compiler test |
| M12 | Put `POST`, publication, or another effectful transport in the reserved consumer contract. | `CAL_TRANSPORT_EFFECT_FORBIDDEN` | static contract validation only |
| M13 | Present a tower not named by the exact allowlist/input lock. | `CAL_TOWER_NOT_ALLOWLISTED` | compiler test |
| M14 | Break `normalized-self-v1`/`cal-canonical-json-v1` self digest. | `CAL_PACKAGE_MANIFEST_STALE` | package validator |
| M15 | Let compiler identity issue the passing ValidationRecord. | `CAL_VALIDATOR_NOT_INDEPENDENT` | independent validator |

M12 does not prove runtime GET-only behavior; it proves only that the first package cannot specify POST/publication as its reserved seam. Runtime transport proof belongs to the later IDE Work Pack.

## Repair role trace

- Proposer claim: closed fixture cardinality and failure codes make the design executable without broadening its product scope.
- Balancer objection category — false closure: the synthetic fixture still cannot validate a real repository tower.
- Reconciliation: the plan must have two evidence lanes: L0 synthetic mechanics and L1 owner-selected real source. No success status or successor may automatically promote L0 evidence into L1.
- Balancer objection category — hidden algorithm complexity: general JSON canonicalization violates the dependency-free boundary.
- Reconciliation: restrict schema values/keys and version `cal-canonical-json-v1`; reject broader values.
- Stable disagreement: none. The corpus-owner selection remains intentionally unresolved and outside the repair.

## Closure checks

| Check | Result | Reason |
| --- | --- | --- |
| Circular definition | `pass` | DefinitionReference binds external accepted research bytes. |
| Package/projection identity cycle | `pass` | generated output remains outside package; self-hash normalization is closed. |
| Canonicalization executability | `pass` | restricted profile is dependency-free and versioned. |
| Privacy leakage detection | `pass` | final-value and serialized-byte scan are explicit. |
| Fixture cardinality | `pass` | exactly one tower/claim/definition/residue/candidate/promotion and two anchors. |
| Required negative failures | `pass` | all seed failures plus manifest/self-validator risks have stable codes. |
| Fixture-only evidence substitution | `pass` | mechanics and real-source states cannot promote into each other. |
| Recomposition | `pass` | later direct GET consumes unchanged projection contract. |

## Navigation

Invoke Plan must consume Stage 06 plus these superseding repair rules. Start with the narrowest reversible schema/canonicalization contract SWU, keep the representative decision as an L1 owner prerequisite, and keep all IDE work outside the first Work Pack.

