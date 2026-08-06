# Whisper Ontology And Proper Runtime — Research Findings

Status: `EXACT_BINDING_FINDINGS_PENDING_AUDIT`.

## Direct answer

Whisper should not begin with a universal story ontology or with a model call wrapped in an application. The evidence supports a smaller system with two deliberately separated layers:

1. a candidate ontology that connects Whisper's already-owned composition provenance to a bounded, owner-deferred story-world graph; and
2. a proper runtime that admits typed commands, appends accepted events, reduces independent state axes, executes generation/validation as retryable activities, and emits digest-bound evidence and read-only projections.

The co-op-engine idea should begin as this private candidate research/prototype seam. Its public card and infrastructure must remain a projection and deployment concern, never the ontology or runtime authority.

## Ontology front

### Selected candidate shape

Reuse canonical Whisper meaning for author intent, composition plan, narrative excerpt, evidence, assessment, correction, receipt, residue, and the composition lifecycle. Do not redefine those meanings in co-op-engine.

Add only the bounded story-world kinds needed by the Mara/Ivo/Observatory L0 witness:

- `CandidateCharacterEntity`
- `CandidatePlaceEntity`
- `CandidateEncounterEntity`

Keep the composition artifacts separate from those candidate entities. A narrative excerpt mentioning Mara does not make the excerpt a character, and a validation result does not create story truth.

### Closed L0 relations

The smallest retained grammar is:

- `CompositionPlanArtifact derived_from AuthorIntentArtifact`
- `NarrativeExcerptArtifact conforms_to_plan CompositionPlanArtifact`
- `NarrativeExcerptArtifact mentions CandidateCharacterEntity | CandidatePlaceEntity | CandidateEncounterEntity`
- `CandidateCharacterEntity participates_in CandidateEncounterEntity`
- `CandidateEncounterEntity occurs_at CandidatePlaceEntity`
- artifact or graph snapshot `assessed_by EvidenceAssessment`
- `AcceptedEvent event_evidenced_by Receipt`
- `Receipt receipt_invalidated_by_correction correction-event`

Each relation must have a named owner, exact endpoint policy, provenance, forbidden substitutions, and stable fail/indeterminate diagnostics. `precedes` is excluded from L0 because one encounter cannot witness a temporal-order relation. Motivation, goals, intentions, causality, contradiction, emotional fit, truth, and comprehension must abstain without separately selected semantics and human/source evidence.

### Validation and authority

Use closed-world validation: unknown kind, predicate, endpoint pair, or policy owner cannot pass. Graph results are `policy-pass | policy-fail | policy-indeterminate`. A GraphValidationReceipt binds exact graph/policy/validator/closure digests, but its `authority_effect` is always `none`.

SHACL and PROV-O are suitable precedents for constraints and provenance; narrative-planning and Story Intention Graph research are precedents for future semantics, not an owner decision to import those semantics. The carrier remains open: the evidence does not require RDF/SHACL, and a JSON implementation may satisfy the same contract if its owner selects it and its finite witnesses pass.

### Ontology conclusion

Research disposition: `SELECT BOUNDED CANDIDATE MODEL; DEFER CANONICAL OWNER BINDING AND ADMISSION`.

No ontology file should be promoted yet. First bind owners for the candidate namespace, each story relation, canonical placement, validation policy, and promotion route. Only then should Ontology Vault/Harness materialize and validate a candidate.

## Proper runtime front

### What a runtime means here

A proper Whisper runtime is the authority-separated mechanism that turns one admitted command into zero or more accepted events and one reproducible state. The model is only an activity worker. It cannot decide command admission, mutate authoritative state, satisfy human gates, or turn its output into approval or ontology meaning.

The minimum runtime responsibilities are:

- typed command envelope with run id, command id, idempotency key, expected revision, canonical closure digest, actor/session evidence, and exact artifact/surface digests;
- admission that rejects stale revision/closure/artifact/surface, duplicate-key conflicts, missing human evidence, illegal phase/gate, and forbidden effects before an activity starts;
- append-only accepted events and non-semantic rejection records;
- a pure reducer over independent `lifecycle_phase`, `pending_gate`, `correction_state`, and `outcome_ceiling` axes;
- immutable content-addressed artifacts, assessments, receipts, graph snapshots, residue, and projections;
- activity scheduling/completion with attempt lineage, retry policy, and idempotent recovery;
- live/replay equality, journal-head binding, and no replay of completed external effects;
- separate editorial approval, comprehension, mechanical validation, post-apply review, and graph-policy evidence;
- actor identity/privacy boundaries, write isolation, denied authority/public/deployment writes, and claim ceilings.

### Candidate topology

For the first local candidate, Python plus SQLite in WAL mode and a content-addressed filesystem is the narrowest evidence-backed topology. SQLite owns the command/idempotency table, event journal, activity attempts, and reducer checkpoints; the content-addressed store owns immutable artifact/evidence bytes. A local worker may execute generation and validation activities. Co-op-engine may submit command envelopes and render digest-bound projections only.

This topology is `SELECT FOR FUTURE CANDIDATE DESIGN, OWNER-BLOCKED`, not an implementation choice already authorized. JSONL/filesystem is acceptable only as a fixture/reference replay. Browser/localStorage/static HTML cannot be authoritative runtime state. Temporal/PostgreSQL or a distributed queue are deferred until a proven concurrency/recovery need appears.

### Repaired state contract

The research has now executed the formerly blocked state-contract subset:

- eight declared `pending_gate` values and neutral `not_assessed` outcome;
- exact EV01-EV26 prior/result states;
- guarded EV22 `COR1 open -> resolved` transition bound to `NE2` and `MA2/pass` digests;
- ten fail-closed negative cases;
- canonical live/replay RS26 equality at `44dbb8106b5094f388e63e7a6ad363061d0499af93ac1c4523871fe428e1280c`;
- non-mutating RP26 derivation.

This closes the research blocker. It does not prove SQLite, a durable journal, activity execution, crashes/retries, idempotency, human sessions, graph validation, privacy, or denied-write behavior. Those remain acceptance requirements for a future prototype Work Pack.

### Runtime conclusion

Research disposition: `SELECT THIN EVENT-SOURCED CANDIDATE RUNTIME; DEFER IMPLEMENTATION UNTIL OWNER BINDINGS AND A SEPARATE WORK PACK`.

## co-op-engine starting seam

Keep development private and candidate-local under co-op-engine. The first future prototype should implement one immutable Mara/Ivo/Observatory fixture end to end, including the mandatory correction, exact editorial/comprehension evidence, graph validation, stale bindings, crash/retry/idempotency cases, replay equality, and separate denied writes.

Co-op-engine may own adapter UX and research/prototype hosting after its owner accepts that boundary. It may not authenticate canonical actors, accept commands, append events, reduce authoritative state, satisfy gates, compute authoritative status, admit ontology meaning, modify Whisper ownership, or treat static reachability as runtime proof.

## Recommended next planning sequence

1. Run an owner/decision package for candidate namespace and relation ownership, runtime contract location, command/event/reducer ownership, identity/privacy, storage/recovery, graph policy, co-op adapter scope, and later ontology admission.
2. Define/design/plan a separate L0 prototype Work Pack with exact files and literal fixture digests. Preserve the state contract proved here as an input, not as full runtime evidence.
3. Execute the prototype through bounded Task Sessions: durable admission/journal/reducer first, activities and recovery second, human/graph evidence third, and co-op adapter/projection last.
4. Only after finite receipts pass, route the candidate ontology through Ontology Vault/Harness. Route public-page change, publication, deployment, promotion, release, and production separately.

## Evidence and claim ceiling

The explorer evidence is in `research.md`; the final repaired contract is in `synthesis-revision-3.md`; executable proof is in `receipts/state-contract-validation.json`; independent review is in `review-completion.md`; and Task Session evidence is in `development/state-contract-repair/execution/task-session-terminal-receipt.json`.

The explorer returns record the inspected Whisper source blobs and their identities. Inventory remained discovery-only.

These are research findings. They create no ontology, runtime, prototype, product mutation, public artifact, publication, deployment, promotion, release, production readiness, or authority grant.
