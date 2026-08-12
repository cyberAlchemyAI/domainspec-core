# Specialist Return: Governance Migration Adversary

## 1. Source selectors and observed facts

### Observed facts

- `REFINE-SEED-PROPOSAL.md` — “Fixed Direction And Claim Ceiling,” “Required Invariants,” and “Scope And Boundaries”:
  - Machine source primacy begins only through an owner admission route.
  - Parsing, validation, normalization, compilation, and projection cannot promote meaning.
  - Schema validity, evidence confidence, commitment confidence, promotion, and authority are separate axes.
  - Migration must preserve IDs or emit explicit queryable identity maps.
  - Reusable public conventions must exclude private adopter evidence and vocabulary.
  - The RWO composition-form identity gate remains unresolved and out of scope.
- `stages/01-context-pack.json` — obligations O1, O2, O7, O8 and gaps G1–G3:
  - Canonical public Ontology Vault sources outrank candidate development evidence, private pressure evidence, and Inventory.
  - Existing lifecycle, entry, relation, confidence, and `PromotionRecord` work is build-from-owned evidence.
  - Migration and projection contracts are acknowledged gaps.
  - Private evidence can pressure-test a reusable model but cannot determine or enter public conventions.
- `stages/02-invoke-define.md` — “Inputs,” “Outputs,” “Candidate Vocabulary,” and “Negative Requirements”:
  - `MigrationMap` is required for legacy adoption; it must be total or preserve explicit residue.
  - `MigrationReceipt` records identity preservation, changes, residue, and rollback.
  - `AdmissionRecord` is explicitly candidate and must be tested against `PromotionRecord` overlap.
  - View writeback, validity-as-truth, normalization-as-promotion, missing-evidence-as-pass, and private vocabulary leakage are forbidden.
- `stages/03-interrogation.md` — fixed decisions and R4–R6:
  - Owner admission and promotion are fixed as separate from schema/compiler/projection success.
  - The governance lane owns the `AdmissionRecord` non-vacuity test, identity-preserving migration, and public/private module boundary.
- `evidence-index.json`:
  - The lifecycle model is exploratory, while the governed candidate bundle is a published candidate.
  - `promotion_record` is canonical as an Ontology Vault record-kind, but the development schema is not a final canonical schema.
  - No external standards source is admitted.
- `arcanum/arcana/ontology-vault/SKILL.md` — Steps 3–6, quality bar, and anti-patterns:
  - Delegated evidence and projections are evidence, not authority.
  - Promotion requires evidence coverage, explicit owner routing, contradiction handling, and approval.
  - Convention changes require migration impact, affected files, rollback, and explicit approval.
  - Project-local aliases and profiles cannot become reusable vocabulary by proximity.
  - Lifecycle mutation for the capability belongs to the owning sigil/capability route.
- `GENERAL-ONTOLOGY-LIFECYCLE-MODEL.md` — “PromotionRecord Boundary,” “Review Owner Rules,” and “Operational Use Rules”:
  - A `PromotionRecord` governs one primary claim or decision and must not contain unrelated bundled claims or replace the ontology entry.
  - It may carry owner, scope, gate result, contradiction, rollback, retirement, and supersession information.
  - No item may reach promoted/policy/constitution/axiom state with an unknown owner.
  - Operational use cannot mutate canonical sources or skip owner review.
- `GOVERNED-CANDIDATE-BUNDLE.md` — “Published Candidate Boundaries” and “Current Candidate Model”:
  - `promotion_record` is canonical for owner-routed promotion decisions about one primary claim or relation.
  - The bundle cannot authorize canonical template mutation or external-system adoption.
  - Public convention adoption remains behind later gates.

### Inference from those facts

`PromotionRecord` and package admission are distinct decisions:

- Admission answers: “Is this exact package version now the owner-recognized source for this package and scope?”
- Promotion answers: “May this particular claim or relation be relied upon at this lifecycle level and scope?”

Making one `PromotionRecord` admit a multi-claim package would violate its one-primary-claim boundary. Package state alone is also insufficient because a mutable `state: admitted` field does not independently preserve who decided, for which digest and scope, why, under which gate, and how to undo it.

## 2. Candidate recommendation

Retain a distinct, narrowly scoped `AdmissionRecord`. It is non-vacuous only if it:

- binds one package ID, version, canonical source digest, schema-suite digest, owner, admission scope, decision time, gate result, rationale, compatibility posture, and rollback target;
- declares source primacy for that exact package version without asserting that every contained claim is true, promoted, or operationally relied upon;
- references applicable `PromotionRecord` objects without replacing or aggregating them;
- is immutable; supersession creates a new record;
- cannot be emitted by validators, normalizers, migration tools, or projectors.

Exact movement owners:

| Movement | Owner |
|---|---|
| Draft source creation | Author; draft has no admitted authority |
| Draft → admitted source version | Named semantic-package owner through `AdmissionRecord` |
| Structural validation | SchemaSuite validator; evidence only |
| Source → normalized IR | Deterministic normalizer; no decision authority |
| IR → projections | Projection compiler; derived artifacts only |
| Correction proposal | Author/reviewer via `SourcePatch` |
| Patch acceptance into source | Semantic-package owner |
| Claim/relation lifecycle promotion | Claim-appropriate review owner through one `PromotionRecord` |
| Legacy migration approval and cutover | Adopter/package owner |
| Migration execution | Digest-pinned migration tool under that approval |
| Migration rollback | Same adopter/package owner, using retained pre-migration source |
| Reusable public convention mutation | Ontology Vault lifecycle owner through later Sigil Development and explicit gate |
| Private profile adoption | Private adopter owner; never the public capability by proximity |

Candidate compatibility states should be explicit: `exact`, `backward-readable`, `forward-readable`, `migration-required`, `partial-with-residue`, `incompatible`, and `unknown`. Only `exact` or an owner-approved, successfully verified migration may proceed to admission. `partial-with-residue`, `incompatible`, and `unknown` block cutover.

`MigrationMap` should bind old/new package and schema versions and digests; classify each identity as `preserved`, `renamed`, `split`, `merged`, `retired`, or `unresolved`; retain provenance and confidence; and require explicit mappings for every old identity. Split/merge mappings must not claim semantic identity automatically. A `MigrationReceipt` should bind tool/version, inputs, outputs, validation result, unresolved residue, pre-migration snapshot, and rollback command/target. Migration should be copy-and-verify before owner cutover, never destructive in place.

## 3. Representation comparison

| Representation | Governance advantage | Principal failure |
|---|---|---|
| Closed JSON | Smallest closure and canonicalization surface; easiest to prohibit undeclared vocabulary | Human ergonomics may encourage unofficial Markdown side sources |
| Constrained JSON-LD | Explicit graph semantics | Remote contexts, vocabulary expansion, aliases, and context drift can leak or change meaning unless every context is local, digest-pinned, closed, and network-independent |
| Typed authoring compiled to canonical JSON | Better authoring may reduce generated-view editing | Adds a compiler trust boundary and risks treating compiled JSON or normalized IR as a second editable source |

Governance preference: closed JSON is the safest baseline. Typed authoring remains viable only when the authored document is unambiguously the sole source and compiler/schema/canonical-output digests are bound. Final representation selection belongs to the schema specialist and parent synthesis.

## 4. Finite positive and negative witnesses

### Positive witnesses

1. Admit package digest `P1` through owner-signed `AdmissionRecord A1`; schema validity alone leaves it draft.
2. Rename an ID through a total `MigrationMap`; old queries resolve through an explicit alias and provenance remains inspectable.
3. Attempt migration with two unresolved IDs; output is retained as `partial-with-residue`, while the pre-migration package remains admitted.
4. Rebuild a projection with a newer compiler; the compiler digest changes, so the prior receipt cannot validate the new output.
5. Validate a synthetic private-profile fixture where private tokens remain confined to the profile module and output; the reusable public schema contains only generic extension hooks.

### Negative witnesses that must fail

1. Schema-valid package with fabricated evidence is automatically marked true or promoted.
2. Normalized IR is edited directly and later accepted as source.
3. A generated Markdown view is edited and written back by proximity.
4. A stale view’s source digest differs from the admitted package digest.
5. Schema version changes while a validator silently uses old compatibility assumptions.
6. One old ID splits into two new IDs without typed mapping, rationale, or uncertainty.
7. Two IDs merge and silently discard contradictory provenance.
8. Migration changes 90% of records, drops the rest, and still cuts over.
9. Rollback depends on reconstructing overwritten source rather than retaining exact pre-migration bytes.
10. A public fixture copies private adopter vocabulary, paths, examples, or prose.
11. Missing evidence becomes a positive fact instead of typed `unknown` or `unsupported`.
12. A contradiction is normalized away rather than retained as a typed, source-bound challenge.
13. One package-level `PromotionRecord` bundles unrelated claims to simulate admission.
14. An `AdmissionRecord` is emitted automatically after successful compilation.
15. The current run is used to select or migrate the paused RWO ontology identity.

## 5. Rejected alternatives

- **Use `PromotionRecord` alone for package admission:** rejected because its canonical boundary is one primary claim or relation; package admission is a different scope and does not promote all contained semantics.
- **Use mutable package state alone:** rejected because it cannot independently prove the owner decision, exact digest, gate, scope, or rollback.
- **Treat normalized IR as the admitted source:** rejected because it creates a second source and obscures authored provenance.
- **Allow projection writeback with reconciliation:** rejected because edit provenance and authority become ambiguous.
- **Permit partial migration with warnings:** rejected for cutover; partial output is useful only as recoverable residue.
- **Embed private profile vocabulary in public optional fields or fixtures:** rejected because optionality does not remove leakage or proximity-based canonization.
- **Resolve compatibility by semantic-version strings alone:** rejected because compatibility depends on schemas, canonicalization, compilers, identities, and actual mappings.

## 6. Claim ceiling

This return supports a candidate governance and migration recommendation plus finite validation witnesses. It does not establish a canonical schema, implemented runtime, admitted package, promoted ontology, public convention change, adopter migration, or RWO decision. All cited development materials retain their stated candidate or exploratory posture.

## 7. Residue and reroute

- Parent synthesis must reconcile this admission boundary with the schema and authoring specialists.
- Exact `AdmissionRecord`, `MigrationMap`, compatibility, and receipt schemas require candidate design and negative fixtures.
- Public convention changes must route later through Ontology Vault convention-update, Sigil Development, and explicit owner approval.
- Private profile pressure tests should use synthetic/redacted fixtures or remain private; no private terms should be copied into public artifacts.
- The RWO identity gate remains paused and must be rerouted to its existing owner decision process.

Status: **pass**. Blockers to research return: none. Blockers to implementation or promotion: unresolved representation/canonicalization contracts, unapproved candidate schemas, missing migration fixtures, and later owner gates.
