# Synthesis Revision 1

Status: `READY_FOR_REREVIEW`. Zig-zag loop used: 1.

This revision applies all three round-1 reviewer repair sets using only OX-01 and RX-01. It adds no source, implementation, ontology admission, authority, product, deployment, or production claim.

## Evidence and claim discipline

- `OX:S1–S11`, `OX:E1–E4`, and `RX:E1–E16` retain the immutable identities, exact selectors, evidence scopes, explorer labels, and statuses recorded in `research.md`.
- `observed` refers only to inspected source/component/distinction evidence.
- Every ontology kind, edge, runtime contract, topology, fixture, digest binding, or execution behavior below is `unverified`.
- Canonical Whisper currently owns only the observed intent, lifecycle, evidence, correction, residue, and claim-ceiling meanings and the existing standalone components cited by the explorers. Command vocabulary, event grammar, legal transitions, admission, actor identity/privacy, journal, reducer, recovery, effects, projection invalidation, and story-world kinds remain candidate design material with unbound owners.

## Repaired dispositions

| Candidate | Disposition | Boundary |
|---|---|---|
| Two namespaces: composition provenance plus bounded story world | **DEFER OWNER BINDING** | Useful hypothesis only; no admitted namespace, relation, or mapping owner |
| Local Python coordinator plus SQLite journal/WAL and content-addressed artifacts | **SELECT FOR FUTURE CANDIDATE DESIGN, OWNER-BLOCKED** | Smallest proposed topology, not an authorized architecture or implementation choice |
| JSONL plus filesystem | **NARROW** to fixture/reference replay | No authoritative concurrency/admission claim |
| SHACL/RDF carrier | **DEFER** | Constraint precedent does not select a carrier |
| Temporal/PostgreSQL | **DEFER** | No observed L0 need |
| Browser/localStorage/static site as authority | **KILL** | Projection is not lifecycle authority |
| Receipt as mutable state | **KILL** | Evidence is not state |
| Model invocation as lifecycle engine | **KILL** | Generation is an activity, not admission/reduction/gate/evidence |

The co-op boundary remains research-local with `authority_effect:none`. The adapter may transport a decision-command envelope and render a digest-bound projection. It cannot authenticate the actor, accept the command, append an event, reduce state, satisfy a gate, compute authoritative status, admit ontology meaning, edit the public page/infra, or deploy.

## Repaired kinds and independent axes

| Partition | Kind | Unique meaning and forbidden substitution |
|---|---|---|
| Run artifact | `AuthorIntentArtifact` | Immutable captured author bytes; not the author, intent state, canonical definition, approval, or authority |
| Run artifact | `CompositionPlanArtifact` | Immutable plan bytes; not planning activity, phase, or story-world fact |
| Run artifact | `NarrativeExcerptArtifact` | Immutable excerpt bytes; not proof of truth, approval, or comprehension |
| Candidate entity | `CandidateCharacterEntity` | Candidate-local fixture assertion; not canonical character meaning |
| Candidate entity | `CandidatePlaceEntity` | Candidate-local fixture assertion; not universal place semantics |
| Candidate entity | `CandidateEncounterEntity` | Candidate-local bounded encounter assertion |
| Evidence | `EvidenceArtifact` | Immutable evidence-bearing bytes; not an ontology node or assessment conclusion |
| Assessment | `EvidenceAssessment` | Typed machine/human assessment bound to exact artifacts/surfaces; not authority |
| Receipt | `Receipt` | Immutable evidence for one transition/evaluation and its exact inputs/outputs/tools/event range; not mutable state, approval, or authority |
| Runtime function | `RunReducer` | Proposed pure reducer; not source of facts or the state it derives |
| Runtime projection | `RunStateSnapshot` | Derived result at an exact event head; cannot admit commands or append events |

Independent fields:

- `lifecycle_phase`: lifecycle position only.
- `pending_gate`: `none | editorial_approval | comprehension`.
- `correction_state`: `none | open | resolved`.
- `outcome_ceiling`: `pass | flag | block`; not approval or terminality.
- `assertion_provenance`: `authored | derived | observed`.
- `assessment_kind`: `mechanical_validation | editorial_approval | comprehension | post_apply_review | graph_policy`.
- `authority_grant_ref`: separately owned capability reference; absence or unresolved identity means no permission. Approval never creates authority.

A rejected command creates a non-semantic `CommandRejectionRecord` outside the accepted semantic-event sequence unless a future owner explicitly defines rejection as a domain occurrence. It does not advance revision or phase.

## Closed relation grammar

| Relation | Exact endpoints | Instantiated L0 assertion |
|---|---|---|
| `derived_from` | `CompositionPlanArtifact → AuthorIntentArtifact` | `CP2 derived_from AI1` |
| `conforms_to_plan` | `NarrativeExcerptArtifact → CompositionPlanArtifact` | `NE2 conforms_to_plan CP2` |
| `mentions` | `NarrativeExcerptArtifact → CandidateCharacterEntity | CandidatePlaceEntity | CandidateEncounterEntity` | `NE2` mentions `CC1`, `CC2`, `PL1`, `CE1` |
| `participates_in` | `CandidateCharacterEntity → CandidateEncounterEntity` | `CC1/CC2 participates_in CE1` |
| `occurs_at` | `CandidateEncounterEntity → CandidatePlaceEntity` | `CE1 occurs_at PL1` |
| `assessed_by` | run artifact or graph snapshot → `EvidenceAssessment` | `NE1 assessed_by MA1`; `NE2 assessed_by MA2`; `GS1 assessed_by GA1` |
| `transition_evidenced_by` | accepted semantic transition/event → `Receipt` | `EV11 transition_evidenced_by MR1`; `EV24 transition_evidenced_by GVR1` |
| `receipt_invalidated_by_correction` | `Receipt → correction event` | `MR1 receipt_invalidated_by_correction EV12` |

`precedes` is killed for L0 because the fixture contains only one encounter. No retained L0 kind or edge is uninstantiated. Story assertions remain candidate-local and transfer no identity or authority to/from canonical Whisper.

## Proposed GraphValidationReceipt

The later receipt must bind `receipt_id`, `run_id`, graph snapshot ref/SHA-256, policy ref/SHA-256, canonical-closure SHA-256, validator source ref/SHA-256/version, stable diagnostics with code/severity/assertion/endpoint/policy rule, `policy-pass | policy-fail | policy-indeterminate`, timestamp, `authority_effect:none`, and receipt SHA-256.

Unknown predicate, endpoint, or owner can never pass. `policy-pass` means only conformity to the bounded policy; it is not approval, comprehension, ontology admission, publication, deployment, or authority.

## Proposed byte-bound fixture

Nothing here has run. A later manifest must replace every digest name with a literal 64-hex SHA-256 over the referenced raw or canonical bytes and reject placeholders, omissions, mismatches, and alternate bytes.

- `run_id`: `whisper-l0-mara-ivo-001`
- raw UTF-8 intent, no BOM, exact bytes including final newline: `Mara meets Ivo at the observatory; afterward Mara remembers the warning.\n`
- actors: `actor-author-local-001`, `actor-editor-local-001`, `actor-reader-local-001`
- challenges: `challenge-editorial-audition-v1`, `challenge-editorial-audition-v2`, `challenge-comprehension-draft-v2`
- candidate entities: `CC1=Mara`, `CC2=Ivo`, `PL1=Observatory`, `CE1=Mara-Ivo-observatory-encounter`

`canonical-closure.json` must enumerate the exact explorer-observed blobs for Whisper README `cfffe6f…cbd`, design `978ea58…498`, substrate schema `938bcdc…e6e`, editorial receipt schema `5de010d…202`, correction schema `439938b…7e5`, draft validator `01f51da…e9f`, receipt evaluator `b79879a…51c`, and review builder `3ba7de6…455`. Its canonical JSON digest is distinct from every raw YAML/file digest. YAML canonicalization remains owner-blocked.

Required literal digest fields include raw intent; closure; plan/audition/surface/draft/mechanical assessment/receipt for v1; correction; plan/audition/surface/editorial evidence/draft/mechanical assessment for v2; graph snapshot/policy/validation receipt; comprehension evidence; residue; projection; journal head; live state; replay state. `live_state_sha256` must equal `replay_state_sha256`; no truncated review ID may substitute.

### Exact proposed semantic sequence

Rejected commands never enter this sequence.

1. `CMD01 SubmitIntent` at revision 0 → `EV01 IntentRecorded` → revision 1.
2. `CMD02 FreezeIntent` at 1 → `EV02 IntentFrozen` → 2.
3. `CMD03 GeneratePlanV1` at 2 → scheduled/produced `EV03–EV04` → 4.
4. `CMD04 GenerateAuditionV1` at 4 → scheduled/produced `EV05–EV06` → 6.
5. `CMD05 RecordEditorialDecisionV1` at 6 → `EV07 EditorialApprovalRecorded` → 7.
6. `CMD06 GenerateDraftV1` at 7 → scheduled/produced `EV08–EV09` → 9.
7. `CMD07 ValidateDraftV1` at 9 → scheduled/`EV11 MechanicalAssessmentRecorded(pass)` → 11.
8. Mandatory `CMD08 SubmitCorrectionV1` at 11 → `EV12 CorrectionRecorded` → 12; opens correction, invalidates `MR1`, restores volatile intent.
9. `CMD09 FreezeCorrectedIntent` at 12 → `EV13 IntentFrozen` → 13.
10. `CMD10 GeneratePlanV2` at 13 → `EV14–EV15` → 15.
11. `CMD11 GenerateAuditionV2` at 15 → `EV16–EV17` → 17.
12. `CMD12 RecordEditorialDecisionV2` at 17 → `EV18 EditorialApprovalRecorded` → 18.
13. `CMD13 GenerateDraftV2` at 18 → `EV19–EV20` → 20.
14. `CMD14 ValidateDraftV2` at 20 → `EV21–EV22 MechanicalAssessmentRecorded(pass)` → 22.
15. `CMD15 ValidateGraph` at 22 → `EV23–EV24 GraphAssessmentRecorded(policy-pass)` → 24.
16. `CMD16 RecordComprehension` at 24 → `EV25 ComprehensionRecorded` → 25.
17. `CMD17 RecordResidue` at 25 → `EV26 ResidueRecorded` → 26.

The final projection is a pure derivation at revision 26 and adds no semantic event. An admitted `EditorialApprovalRecorded` event whose independently validated digest-bound assessment is approved may satisfy the editorial gate under the selected policy. The adapter display, submitted command, record alone, or validator result cannot open generation.

### Required independent negatives

- Missing approval: draft command rejected; revision/head unchanged; zero activity starts.
- Missing comprehension: machine/graph checks may finish, but the required final claim remains flag/block; approval cannot substitute.
- Separate stale closure, stale artifact, and stale surface rejections.
- Reversed direction: `EDGE_DIRECTION_INVALID`.
- Invalid endpoint: `ENDPOINT_PAIR_FORBIDDEN`.
- Ownerless predicate `CC1 intends CE1`: `POLICY_OWNER_UNBOUND`, never pass.
- Crash after schedule/before completion: policy-authorized new attempt with lineage; no invented completion.
- Crash after committed completion/before response: identical retry returns prior result; completed effect count stays one.
- Duplicate same bytes: return prior outcome, no new semantic event. Same key/different bytes: conflict rejection, unchanged head.
- Volatile intent requests derivative fan-out: denial and zero derivative attempts.
- Separate denied runtime/journal write, ontology admission/promotion write, and public-page/infra/deployment write; each records `AUTHORITY_WRITE_DENIED` and equal protected before/after digests.
- Replay `EV01..EV26`: exact live/replay state and journal-head equality, with no increased completed-activity count.

## Ordered route and remaining blockers

1. Define and bind owners for the candidate namespaces/relations, runtime contract location, transitions/status, admission/effects, actor identity/privacy, journal/reducer/storage/recovery, canonicalization, projection invalidation, and co-op boundary.
2. Design the closed grammar, commands/admission/rejections/events, independent state axes, human challenges, byte rules, recovery, write isolation, and claim ceilings.
3. Plan one separately authorized candidate-local Work Pack with exact paths and fixtures.
4. Prototype only after owner and write-scope approval. SQLite/CAS remains only the selected future candidate design.
5. Execute every positive, negative, correction, crash, retry, replay, stale-binding, human-gate, and denied-write witness.
6. Review claims against actual receipts.
7. Route ontology admission, canonical placement, public mutation, publication, deployment, release, and production separately.

This revision remains research synthesis only. It creates no ontology, runtime, prototype, product mutation, deployment, publication, promotion, release, or production proof.
