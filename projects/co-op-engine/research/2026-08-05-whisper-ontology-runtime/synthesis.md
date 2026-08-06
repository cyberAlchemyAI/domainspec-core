# Whisper Ontology And Runtime System Synthesis

**Verdict:** PASS for an owner-preserving design target. No ontology, runtime, validator, fixture, browser behavior, deployment, or external effect was implemented or executed by this synthesis.

## Direct answer

Whisper already owns a meaningful composition lifecycle, typed evidence distinctions, deterministic validation tools, and a generated runtime-facing projection. It does **not** yet have either a canonical story-world ontology or an end-to-end executable runtime.

The smallest defensible next system is a mapped pair:

1. an Arcanum-referenced **composition provenance graph**, whose meaning stays with canonical Whisper; and
2. a candidate-local **four-kind story-world slice** containing `Character`, `Place`, `Encounter`, and `NarrativeExcerpt`, with only the relations needed for one finite witness.

That graph should be exercised by a single-process, local, no-external-effect coordinator using an append-only SQLite journal and content-addressed artifacts. The coordinator may invoke current validators as activities, but it may not redefine Whisper, infer approval, admit ontology meaning, mutate the co-op public page, deploy, or claim production readiness.

This preserves the central disagreement rather than averaging it:

- **Semantic closure constrains runtime:** the runtime must carry a canonical closure digest, preserve independent intent/evidence/approval axes, enforce Whisper’s volatile-intent and human-gate rules, and refuse unknown semantics.
- **Executable witnesses constrain ontology:** the first ontology cannot include motivations, goals, arbitrary causal truth, universal story semantics, or an open predicate vocabulary because no current executable witness or owner can distinguish their valid and invalid use. Those concepts remain deferred or indeterminate.

## Binding key

Every synthesis reference below preserves the explorer’s immutable identity, selector, evidence scope, return label, and status.

- `OX:S1–S11` and `OX:E1–E4` mean the exact immutable rows in OX-01’s **Source key** in `research.md`, including their blobs/URLs, selectors, scopes, `OX-01` label, and `observed` status.
- `RX:E1–E16` mean the exact immutable rows in RX-01’s **Evidence key** in `research.md`, including their repository revisions/blobs or external identities, selectors, scopes, `RX-01` label, and `observed` status.
- A synthesis item marked `unverified` is proposed even where its constraining source is observed.
- No explorer identity, selector, scope, status, or return label is upgraded by this synthesis.

## Current-state map

| Layer | Current reality | Owner and forbidden inference | Binding |
|---|---|---|---|
| Canonical Arcanum source | Whisper defines intent, SCU cores, composition stages, convergence, transport gates, human evidence distinctions, correction, residue, and claim ceilings. | Public Arcanum/Whisper owns meaning. Existing prose and schemas do not prove orchestration. | `OX:S1–S5` · OX-01 · observed; `RX:E1–E5` · RX-01 · observed |
| Generated runtime projection | Generated Codex/runtime-facing material projects canonical Whisper guidance for invocation. | Projection is not the canonical spell and does not become lifecycle authority. | `RX:E1,E2` · RX-01 · observed |
| Deterministic validators | Draft CLI produces mechanical PASS/FLAG/BLOCK; receipt evaluator validates shape and computes a ceiling; review builder produces local HTML. | These tools do not admit commands, persist history, authenticate humans, approve meaning, replay work, or prove production. | `RX:E6–E8` · RX-01 · observed |
| Human evidence | Receipt schema distinguishes editorial approval, comprehension, audition, render, correction, and post-apply evidence. | Typed capacity is present; authenticated actor/session binding and live evidence ingestion are absent. Validator PASS cannot substitute. | `OX:S4,S6,S7` · OX-01 · observed; `RX:E4,E7,E8` · RX-01 · observed |
| Co-op public summary | `#project-whisper` describes the vision and explicitly identifies the current limit/future graph. | Portfolio projection only. It is not an ontology, application runtime, event store, or runtime proof. | `OX:S9` · OX-01 · observed; `RX:E9` · RX-01 · observed |
| Static deployment boundary | Co-op infrastructure deploys static material and has no database/application runtime. | Static reachability proves neither Whisper execution nor production behavior. | `RX:E10` · RX-01 · observed |
| End-to-end runtime | No observed command handler, journal, reducer, scheduler, lease, retry, resumability, replay, or projection invalidation owner. | Must be described as absent. Existing parts are substantial but independently invoked. | `RX:E1–E8` · RX-01 · observed |
| Story-world ontology | The public card suggests characters, places, encounters, timeline, and connections. No canonical local semantics were found. | Candidate interpretation only; no ontology admission or promotion. | `OX:S9,S10,S11,E3,E4` · OX-01 · observed |

## Ontology contract

The ontology is two namespaces joined by explicit mapping edges, not one undifferentiated graph.

| Partition | Minimum retained contract | Constraint/authority rule | Binding and status |
|---|---|---|---|
| Composition nodes | `AuthorIntent`, `CompositionPlan`, `NarrativeExcerpt`, `EvidenceRecord`, `LearningResidue` | Reference canonical Whisper meanings; do not redefine them locally. | `OX:S1–S5,E2` · OX-01 · observed basis; proposed graph representation unverified |
| Story-world nodes | `Character`, `Place`, `Encounter` | Candidate-local instances only. No universal character/event ontology is claimed. | `OX:S9,E3,E4` · OX-01 · unverified |
| Provenance relations | `derived_from`, `planned_by`, `supported_by`, `invalidated_by` | Direction is closed and deterministic; provenance never turns a derived assertion into authored fact. | `OX:S4,S5,E2` · OX-01 · observed basis; endpoint grammar unverified |
| Story/map relations | `mentions`, `participates_in`, `occurs_at` | Only enumerated endpoint triples pass: excerpt→entity/event, character→encounter, encounter→place. | `OX:S9,S11,E1` · OX-01 · unverified |
| Temporal relation | `precedes` | NARROW to explicit encounter→encounter assertions in the fixture; require acyclicity; infer no transitive story truth. | `OX:S9,S11` · OX-01 · unverified |
| State axes | intent `forming/volatile/frozen`; evidence `pass/flag/block/absent`; policy `policy-pass/fail/indeterminate` | Axes remain independent. Artifact is not state; validation is not approval. | `OX:S1,S4,S11` · OX-01 · observed |
| Evidence kinds | machine validation, editorial audition, comprehension, post-apply review, source binding | Each binds exact artifact/surface identities. Missing required human evidence limits or blocks the claim. | `OX:S4,S6–S8` · OX-01 · observed |
| Authority partition | authored, derived, observed, approved, authority-bearing | Only named owners author assertions or policy; derived/observed/approved records never promote meaning. Candidate validator and adapter have `authority_effect:none`. | `OX:S1,S4,S10,S11,E2` · OX-01 · observed |
| Closed-world result | `policy-pass`, `policy-fail`, or `policy-indeterminate` with stable diagnostics | Unknown kind, predicate, endpoint, required evidence, or owner cannot pass. Ownerless semantics yield `POLICY_OWNER_UNBOUND`. | `OX:S11,E1` · OX-01 · observed precedent; implementation unverified |

Explicit reductions:

- `AuthorIntent`, `CompositionPlan`, and `NarrativeExcerpt` stay distinct because each has a different authoring/provenance role.
- `Encounter` is retained only because the witness discriminates participants, location, and ordering.
- Separate `Timeline` and `Connection` nodes are **KILL for L0**: edges already witness these roles.
- Character goals, motivations, causal necessity, contradiction, emotional fit, and truth are **DEFER**: precedent exists, but local owner and executable policy do not.
- `ApprovalRecorded` and `EvidenceObserved` belong in runtime history, not as timeless story-world facts.
- `GraphValidationReceipt` is evidence about a graph snapshot, not a node that grants authority.

## Runtime contract

| Kind | Minimum contract and behavior | Failure boundary | Binding and status |
|---|---|---|---|
| Command | Identity/type/run/actor/time, canonical closure digest, content-bound inputs, expected revision, idempotency key, requested effect, payload | Request only. Reject stale closure/input/revision, unknown type, key collision with different bytes, or unauthorized effect. | `RX:E1,E3,E11,E12,E15` · RX-01 · unverified |
| Event | Identity/type/run/sequence, causation/correlation, producer/time, prior-event digest, canonicalized data, event digest | Append-only occurrence. Retry cannot invent a second semantic outcome. | `RX:E5,E11,E12,E15` · RX-01 · unverified |
| Artifact | Immutable identity/kind/media/digest/length, creation event, derivation refs, closure digest, storage ref | New bytes require a new identity. Storage does not own meaning. | `RX:E3,E4,E13,E15` · RX-01 · unverified |
| Activity attempt | Type, input digest, lease, start/completion events, exit/output refs, effect class | Only activities perform model/file/subprocess/network work. Replay consumes recorded results and repeats no completed effect. | `RX:E6,E7,E11` · RX-01 · unverified |
| Receipt | Transition revisions, command digest, event range, artifact manifest, evidence axes, computed decisions, validator/closure identities, receipt digest | Evidence, not mutable state or approval. Any digest/reference mismatch invalidates it. | `RX:E4,E7,E15` · RX-01 · unverified |
| Projection | Revision/event-head/source-receipt/projection digests plus display payload | Read-only and disposable. Stale projection must disclose staleness and cannot accept a human decision against changed bytes. | `RX:E8,E9,E16` · RX-01 · unverified |
| Reducer/state | Pure reduction of closure plus ordered events into revision, phase, intent state, pending gate, latest artifacts, open corrections, ceiling, and event head | State/projection cannot append facts. Illegal transition blocks before activity launch. | `RX:E1,E4,E5,E7,E11` · RX-01 · unverified |
| Replay/recovery | Rebuild identical state/projection from journal; pending attempts may resume according to policy; completed effects are not rerun | Live/replay digest mismatch, sequence break, or repeated completed effect blocks acceptance. | `RX:E11` · RX-01 · observed precedent; Whisper implementation unverified |
| Human gates | Editorial and comprehension commands bind actor, challenge/session, artifact digest, and surface digest | Approval is not comprehension; machine validation is neither; stale decisions block. Identity/privacy policy remains owner-blocked. | `RX:E4,E8` · RX-01 · observed distinction; ingestion unverified |

Phase transitions are event-driven:

`empty → intake_recorded → intent_forming → intent_frozen → plan_ready → audition_ready → awaiting_editorial_approval → draft_ready → mechanically_validated → awaiting_comprehension | correction_pending | reviewed → residue_recorded → terminal_flag | terminal_pass | terminal_block`

The runtime may not move from volatile intent to full derivative generation. A correction invalidates the referenced prior receipt and may restore volatility. Final status cannot exceed the weakest required evidence axis.

## Canonical Whisper versus co-op demonstrator

| Canonical Arcanum/Whisper owns | Candidate co-op demonstrator may do | Demonstrator must never do |
|---|---|---|
| Intent and SCU meanings; lifecycle/gates; substrate and receipt semantics; transition/status policy once defined; canonical closure identity; validator meaning | Construct candidate commands; host research-local fixtures; render digest-bound projections; present audition/comprehension surfaces; relay human commands; display evidence labels | Redefine canonical terms; silently normalize intent; reduce authoritative state; rewrite journal/receipts; compute authoritative status independently; fabricate approval/comprehension; admit/promote ontology; modify public HTML; deploy |
| Bindings: `OX:S1–S5,S10`; `RX:E1–E5,E16` · observed | Bindings: `RX:E4,E8,E9,E16` · proposed/unverified | Bindings: `OX:S9,S10`; `RX:E9,E10,E16` · observed boundary |

The existing `projects/co-op-engine/index.html` remains an honest static summary. The candidate prototype belongs under its research folder only until separate product, public/private, deployment, and promotion decisions are authorized.

## Topology options

| Option | Verdict | Reason and evidence |
|---|---|---|
| Single local Python coordinator + SQLite append-only journal/WAL + content-addressed filesystem artifacts | **SELECT** for L0 | Smallest transactional executable witness; aligns with current Python tools while preserving journal/artifact separation. Hash-chain, reducer, recovery, and concurrency limits still require implementation. `RX:E6,E7,E14,E15` · RX-01 · unverified |
| JSONL journal + filesystem artifacts | **NARROW** to fixtures/reference replay | Excellent inspectability, but not accepted as the concurrent authority store without locking and uniqueness discipline. `RX:E5,E11,E15` · RX-01 · unverified |
| Mapped composition-provenance plus bounded story-world graph | **MERGE** as two namespaces, not two authorities | Reuses owned Whisper semantics while permitting one candidate story-map witness. `OX:S1–S5,S9,S10` · OX-01 · observed basis; mapping unverified |
| RDF/SHACL as required carrier | **DEFER** | SHACL supplies sound constraint precedent, but behavior should be fixed before carrier selection; no RDF requirement follows. `OX:E1,S11` · OX-01 · observed precedent |
| Temporal or PostgreSQL distributed runtime | **DEFER** | Useful durability precedent, unjustified before L0 recovery/concurrency evidence. `RX:E10,E11,E14` · RX-01 · observed/unverified |
| Browser/localStorage or static deploy directory as authority | **KILL** | Cannot own durable ordering, effect isolation, or authenticated admission; current co-op host is static. `RX:E8–E10` · RX-01 · observed |
| Receipt JSON as mutable run state | **KILL** | Collapses evidence into authority and destroys replay/provenance. `RX:E4,E5,E11,E13` · RX-01 · observed |
| Direct model call as lifecycle engine | **KILL** | Generation is an activity result, not admission, reduction, approval, or evidence. `RX:E1,E4,E11` · RX-01 · observed |
| Universal story ontology with goals/motivation/causal truth | **KILL for L0; DEFER generally** | No bound local owner or finite discriminating policy. `OX:E3,E4,S9,S11` · OX-01 · observed precedent, local semantics unverified |

## Minimum finite ontology-plus-runtime witness

Use eight graph nodes: `I1 AuthorIntent`, `P1 CompositionPlan`, `X1 NarrativeExcerpt`, `C1 Character(Mara)`, `C2 Character(Ivo)`, `L1 Place(Observatory)`, `E1 Encounter`, and `V1 EvidenceRecord`.

Positive graph:

- `P1 derived_from I1`
- `X1 planned_by P1`
- `X1 mentions E1`
- `C1 participates_in E1`
- `C2 participates_in E1`
- `E1 occurs_at L1`
- `X1 supported_by V1`

Runtime witness:

1. `SubmitIntent` records immutable `I1`.
2. Owner decisions freeze intent.
3. `GeneratePlan` produces `P1`.
4. `GenerateAudition` produces a digest-bound surface.
5. `RecordEditorialDecision` binds the exact audition; only approval opens draft generation.
6. `GenerateDraft` produces immutable `X1`.
7. `ValidateDraft` invokes the existing CLI as an activity.
8. `ValidateGraph` checks the seven edges against the closed grammar.
9. Required `RecordComprehension` remains separate.
10. `SubmitCorrection`, if present, appends invalidation and routes a new revision.
11. `RecordResidue` emits non-canonical learning and a terminal projection.

This whole witness is **unverified**. Its semantic constraints derive from `OX:S1,S4,S5,S9,S11,E1,E2` · OX-01; its executable contract derives from `RX:E1,E3–E8,E11–E15` · RX-01.

Negative controls required for acceptance:

| Control | Expected result |
|---|---|
| `I1 derived_from P1` | `policy-fail / EDGE_DIRECTION_INVALID` |
| `L1 participates_in E1` | `policy-fail / ENDPOINT_PAIR_FORBIDDEN` |
| `C1 intends E1` without selected owner | `policy-indeterminate / POLICY_OWNER_UNBOUND` |
| Unknown predicate/kind | fail or indeterminate; never pass |
| Stale artifact/surface approval | block; gate stays open |
| Machine PASS with missing required comprehension | mechanical pass only; final flag/block |
| Volatile intent requests full derivative fan-out | block and zero derivative activity starts |
| Duplicate command, same bytes | return prior outcome; no semantic duplicate |
| Same idempotency key, different bytes | block conflict |
| Interrupted run | replay to identical state without repeating completed effects |
| Correction after prior pass | invalidate prior receipt; current result no longer pass |
| Candidate adapter attempts canonical/authority/public-site/deployment write | `AUTHORITY_WRITE_DENIED`; protected digests unchanged |

Bindings: `OX:S1,S4–S7,S10,S11,E1,E2` · OX-01 · observed basis/unverified execution; `RX:E1,E4–E7,E9–E12,E15,E16` · RX-01 · observed basis/unverified execution.

## Ordered route

1. **Define:** bind owners and unique meanings for runtime location, legal transitions, story-world kinds/edges, authority/effect admission, human identity/evidence, and digest canonicalization. No ontology admission yet.
2. **Design:** freeze the mapped-pair contract, closed endpoint grammar, commands/events/reducer, artifact and receipt identities, replay semantics, human gates, write isolation, privacy, and claim ceilings.
3. **Plan:** authorize one finite candidate-local work pack with exact write scope, fixtures, tool identities, negative bank, validation commands, and unchanged-path proof.
4. **Prototype:** implement only the local coordinator, SQLite journal, CAS, fake/injectable generation port, graph validator, current-validator activity adapters, read-only projection, and fixture-bound human commands. No provider integration or public-site mutation.
5. **Validate:** execute contract, reducer, replay, stale-digest, idempotency, missing-human, volatile-intent, denied-authority, browser-projection, and unchanged-boundary checks. Capture immutable receipts.
6. **Review:** compare executed evidence with claim ceilings; retain unresolved semantics as residue, not inferred truth.
7. **Later promotion:** only a separately authorized owner route may admit definitions/relations, move canonical runtime contracts into Arcanum, modify a product surface, publish, deploy, release, or claim production readiness.

## Proposed research/prototype layout

```text
projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/
├── findings.md
├── decisions/
│   ├── semantic-scope.md
│   ├── runtime-ownership.md
│   └── human-evidence.md
└── prototype/
    ├── README.md
    ├── contracts/
    │   ├── command.schema.json
    │   ├── event.schema.json
    │   ├── graph.schema.json
    │   ├── transition-policy.yaml
    │   └── projection.schema.json
    ├── fixtures/
    │   ├── positive/
    │   ├── negative/
    │   ├── indeterminate/
    │   └── recovery/
    ├── runtime/
    │   ├── coordinator.py
    │   ├── journal.py
    │   ├── reducer.py
    │   ├── artifacts.py
    │   └── activities.py
    ├── ontology/
    │   ├── policy.yaml
    │   └── validate_graph.py
    ├── adapter/
    │   └── local_projection/
    ├── tests/
    │   ├── test_contract_*.py
    │   ├── test_replay.py
    │   ├── test_negative_witnesses.py
    │   └── browser/
    ├── tools/
    │   └── run_acceptance.py
    └── receipts/
```

This is a proposed placement only. It does not authorize creating these paths. It deliberately excludes `projects/co-op-engine/index.html`, `projects/co-op-engine/infra/`, and `arcanum/spells/whisper/` from prototype mutation.

## Residue

| Residue | Owner | Evidence required to close |
|---|---|---|
| Canonical runtime contract location | Arcanum maintainers | Accepted design locating command/event/transition/replay contracts without duplicating Whisper |
| Story-world semantic owner | Whisper design owner plus ontology/definitions route | Definitions and negative examples for `Character`, `Place`, `Encounter`, `precedes`; explicit rejection/deferment of intention semantics |
| Transition/status policy owner | Whisper lifecycle owner | Complete transition table with illegal-transition witnesses and status-axis interaction |
| Human identity/evidence policy | Product/privacy and Whisper owners | Actor/session binding, retention, revocation, privacy, stale-decision, and comprehension protocol |
| Admission/effect authority | Runtime/security owner | Capability policy and denial receipts for model, file, network, deployment, and authority effects |
| YAML canonicalization | Contract owner | Exact raw-byte versus canonical-data rules and cross-implementation digest fixtures |
| Storage/recovery limits | Prototype owner | SQLite transaction, corruption, backup, migration, crash, retry, and concurrency witnesses |
| Review projection identity | Projection owner | Full digest-bound manifest; decision rejection after any surface/artifact change |
| Co-op hosting boundary | Co-op product owner plus Whisper owner | Decision between research-only prototype, separate candidate app, or later authorized route |
| “Working prototype” claim | Final approver | Executed positive, negative, indeterminate, determinism, replay, stale-digest, human-gate, and write-isolation receipts |
| Ontology admission/promotion | Definitions/ontology authority owner | Separately authorized promotion package after prototype evidence; no admission by this research |
| Deployment/production | Deployment and operational owners | Separate deployment receipt, then operational evidence under declared security/SLO/recovery scope |

The load-bearing gap is not lack of vocabulary or scripts. It is the absence of bound owners and executed evidence connecting canonical meaning to deterministic admission, durable history, human decisions, replay, and write isolation. Until those gaps close, the correct claim is: **owner-preserving design target, not implemented ontology, working runtime, deployed application, or production system.**
