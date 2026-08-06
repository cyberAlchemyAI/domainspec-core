# Synthesis Revision 2

Status: `READY_FOR_FINAL_REVIEW`. Zig-zag loops used: 2 of 2.

This revision preserves `synthesis-revision-1.md` and closes only `review-round-2.md`. Nothing below was implemented or executed. Every future digest is a manifest obligation, not a claim that bytes were created or hashed.

## Evidence and ownership boundary

- OX-01 and RX-01 bindings and observed/unverified statuses remain unchanged.
- Candidate composition/story namespaces remain **DEFER OWNER BINDING**.
- Python plus SQLite/CAS remains **SELECT FOR FUTURE CANDIDATE DESIGN, OWNER-BLOCKED**.
- Canonical Whisper ownership remains limited to observed meanings, schemas, standalone validators, and review projection components.
- All commands, events, transition policy, admission, identity/privacy, journal, reducer, activities, replay, recovery, ontology kinds/relations, and fixture behavior remain proposal-only.
- Co-op remains research-local with no lifecycle, ontology, journal, status, promotion, publication, or deployment authority.

## Immutable future fixture and byte rules

Future root:

`projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/prototype/fixtures/whisper-l0-mara-ivo-001/`

A byte change creates a new fixture version/root. Text/HTML is UTF-8, no BOM, LF, no trailing spaces, exactly one terminal LF. JSON is RFC 8785 JCS, UTF-8, no BOM, no insignificant whitespace, no terminal LF. Digests are lowercase SHA-256 over raw bytes. Arrays retain source order. `manifest.json` must contain literal digests; missing/placeholders/mismatches/alternate bytes fail.

Required paths:

- artifacts: `raw-intent.txt` (`AI1`), `plan-v1.json` (`CP1`), `plan-v2.json` (`CP2`), `audition-v1.md` (`AU1`), `audition-v2.md` (`AU2`), `draft-v1.md` (`NE1`), `draft-v2.md` (`NE2`), `residue-v1.json` (`LR1`)
- surfaces: `audition-v1.html` (`SF1`), `audition-v2.html` (`SF2`), `comprehension-v2.html` (`SF3`)
- evidence: `editorial-decision-v1.json` (`EA-ED1`), `mechanical-validation-v1.json` (`EA-MA1`), `post-apply-review-v1.json` (`EA-PAR1`), `correction-v1.json` (`COR1`), `editorial-decision-v2.json` (`EA-ED2`), `mechanical-validation-v2.json` (`EA-MA2`), `graph-policy-v1.json` (`EA-GA1`), `comprehension-v2.json` (`EA-CA1`)
- graph: `graph-snapshot-v1.json` (`GS1`), `graph-policy-v1.json` (`GP1`)
- state/projection: `state/run-state-r26.json` (`RS26`), `projections/run-projection-r26.json` (`RP26`), `projections/run-projection-r26.html`
- closure and manifest: `closure/canonical-closure.json`, `manifest.json`

Exact text payloads, each with one terminal LF:

```text
Mara meets Ivo at the observatory; afterward Mara remembers the warning.
```

```text
Mara met Ivo beneath the observatory dome. Afterward, she remembered the warning.
```

```text
Mara met Ivo beneath the observatory dome. Later, as she left, Mara remembered Ivo's warning.
```

Exact future human-evidence JSON values, stored as JCS bytes:

```json
{"actor_ref":"actor-editor-local-001","artifact_ref":"AU1","artifact_sha256_ref":"manifest.digests.audition_v1_sha256","assessment_id":"ED1","assessment_kind":"editorial_decision","assessment_result":"approve","challenge_ref":"challenge-editorial-audition-v1","decision":"approve","receipt_id":"ER1","session_ref":"session-editorial-local-001","surface_ref":"SF1","surface_sha256_ref":"manifest.digests.audition_surface_v1_sha256"}
```

```json
{"actor_ref":"actor-editor-local-001","artifact_ref":"AU2","artifact_sha256_ref":"manifest.digests.audition_v2_sha256","assessment_id":"ED2","assessment_kind":"editorial_decision","assessment_result":"approve","challenge_ref":"challenge-editorial-audition-v2","decision":"approve","receipt_id":"ER2","session_ref":"session-editorial-local-002","surface_ref":"SF2","surface_sha256_ref":"manifest.digests.audition_surface_v2_sha256"}
```

```json
{"actor_ref":"actor-reader-local-001","answers":[{"answer":"At the observatory.","question_id":"Q1"},{"answer":"Ivo's warning.","question_id":"Q2"}],"artifact_ref":"NE2","artifact_sha256_ref":"manifest.digests.draft_v2_sha256","assessment_id":"CA1","assessment_kind":"comprehension_assessment","assessment_result":"pass","challenge_ref":"challenge-comprehension-draft-v2","questions":[{"question":"Where do Mara and Ivo meet?","question_id":"Q1"},{"question":"What does Mara remember afterward?","question_id":"Q2"}],"receipt_id":"CAR1","session_ref":"session-comprehension-local-001","surface_ref":"SF3","surface_sha256_ref":"manifest.digests.comprehension_surface_v2_sha256"}
```

```json
{"actor_ref":"actor-author-local-001","affected_artifact_ref":"NE1","affected_artifact_sha256_ref":"manifest.digests.draft_v1_sha256","assessment_id":"PAR1","assessment_kind":"post_apply_review","assessment_result":"correction_required","correction_id":"COR1","instruction":"Make the final sentence explicitly identify Ivo as the source of the warning.","invalidated_receipt_ref":"MR1","receipt_id":"CR1","session_ref":"session-author-review-local-001"}
```

Manifest obligations include every artifact/surface/evidence/graph/policy/receipt/residue/state/projection digest, canonical closure, journal head after each `EV01..EV26`, live state, and replay state. `live_state_sha256` must equal `replay_state_sha256`; truncated review identity is forbidden.

## Assessment vocabulary

| Kind | Results |
|---|---|
| `mechanical_validation` | `pass | flag | block` |
| `editorial_decision` | `approve | reject | request_correction` |
| `comprehension_assessment` | `pass | flag | block` |
| `post_apply_review` | `accepted | correction_required` |
| `graph_policy` | `policy-pass | policy-fail | policy-indeterminate` |

No result may satisfy another kind’s gate.

## Proposed exact command/event/state sequence

Rejected commands are non-semantic rejection records and do not advance revision or head. State axes are `lifecycle_phase`, `pending_gate`, `correction_state`, and `outcome_ceiling`. Each listed semantic event binds the corresponding `manifest.digests.journal_head_after_evNN_sha256`.

| Command @ expected revision | Exact accepted events | Resulting revision/state | Produced IDs |
|---|---|---|---|
| `CMD01 SubmitIntent @0` | `EV01 IntentRecorded` | r1 `intake_recorded`; gate `intent_freeze`; correction `none`; ceiling `absent` | `AI1,AR1` |
| `CMD02 FreezeIntent @1` | `EV02 IntentFrozen` | r2 `intent_frozen`; none/none/absent | `IFR1` |
| `CMD03 GeneratePlanV1 @2` | `EV03 PlanGenerationScheduled`; `EV04 PlanProduced` | r4 `plan_ready`; none/none/absent | `CP1,PA1,PR1` |
| `CMD04 GenerateAuditionV1 @4` | `EV05 AuditionGenerationScheduled`; `EV06 AuditionProduced` | r6 `awaiting_editorial_decision`; gate editorial; none/absent | `AU1,SF1,AA1,AUR1` |
| `CMD05 RecordEditorialDecisionV1 @6` | `EV07 EditorialDecisionRecorded` | r7 `editorial_decision_recorded`; none/none/absent | `EA-ED1,ED1,ER1` |
| `CMD06 GenerateDraftV1 @7` | `EV08 DraftGenerationScheduled`; `EV09 DraftProduced` | r9 `draft_ready`; gate mechanical; none/absent | `NE1,DA1,DR1` |
| `CMD07 ValidateDraftV1 @9` | `EV10 DraftValidationScheduled`; `EV11 MechanicalAssessmentRecorded` | r11 `mechanically_validated`; gate post-apply; none/flag | `EA-MA1,MA1,MR1` |
| `CMD08 SubmitCorrectionV1 @11` | `EV12 CorrectionRecorded` | r12 `correction_pending`; gate refreeze; open/block | `COR1,EA-PAR1,PAR1,CR1`; invalidates `MR1` |
| `CMD09 FreezeCorrectedIntent @12` | `EV13 IntentFrozen` | r13 `intent_frozen`; none/open/block | `IFR2` |
| `CMD10 GeneratePlanV2 @13` | `EV14 PlanGenerationScheduled`; `EV15 PlanProduced` | r15 `plan_ready`; none/open/block | `CP2,PA2,PR2` |
| `CMD11 GenerateAuditionV2 @15` | `EV16 AuditionGenerationScheduled`; `EV17 AuditionProduced` | r17 `awaiting_editorial_decision`; editorial/open/block | `AU2,SF2,AA2,AUR2` |
| `CMD12 RecordEditorialDecisionV2 @17` | `EV18 EditorialDecisionRecorded` | r18 `editorial_decision_recorded`; none/open/block | `EA-ED2,ED2,ER2` |
| `CMD13 GenerateDraftV2 @18` | `EV19 DraftGenerationScheduled`; `EV20 DraftProduced` | r20 `draft_ready`; mechanical/open/block | `NE2,SF3,DA2,DR2` |
| `CMD14 ValidateDraftV2 @20` | `EV21 DraftValidationScheduled`; `EV22 MechanicalAssessmentRecorded` | r22 `mechanically_validated`; graph/resolved/flag | `EA-MA2,MA2,MR2` |
| `CMD15 ValidateGraph @22` | `EV23 GraphValidationScheduled`; `EV24 GraphAssessmentRecorded` | r24 `graph_validated`; comprehension/resolved/flag | `GS1,GP1,EA-GA1,GA1,GVR1` |
| `CMD16 RecordComprehension @24` | `EV25 ComprehensionAssessmentRecorded` | r25 `reviewed`; none/resolved/pass | `EA-CA1,CA1,CAR1` |
| `CMD17 RecordResidue @25` | `EV26 ResidueRecorded` | r26 `residue_recorded`; none/resolved/pass | `LR1,RR1,RS26` |

`RS26` is reduced from the closure plus `EV01..EV26`. `RunProjection RP26` is derived separately from `RS26`, `RR1`, and the event head. Rendering RP26 adds no event/revision and cannot alter state, receipts, journal, ceiling, or human evidence.

EV07 binds actor `actor-editor-local-001`, session `session-editorial-local-001`, challenge `challenge-editorial-audition-v1`, `AU1/SF1`, exact decision bytes, `EA-ED1/ED1/ER1`. EV18 binds the v2 equivalents. EV25 binds actor `actor-reader-local-001`, session `session-comprehension-local-001`, challenge `challenge-comprehension-draft-v2`, `NE2/SF3`, exact question/answer bytes, `EA-CA1/CA1/CAR1`. Approval and comprehension never substitute.

## Exact GraphSnapshot and relations

`GS1` is one RFC 8785 JCS object with schema version `candidate.whisper.graph-snapshot.v0`, owner `owner-fixture-author-local-001`, canonicalization `RFC8785-JCS-UTF8`, policy `GP1`, policy digest ref, expected graph digest ref, and these records:

- nodes: `AI1 AuthorIntentArtifact` authored; `CP2 CompositionPlanArtifact` derived; `NE2 NarrativeExcerptArtifact` derived; `CC1/CC2 CandidateCharacterEntity` authored with labels Mara/Ivo; `PL1 CandidatePlaceEntity` authored label Observatory; `CE1 CandidateEncounterEntity` authored label Mara-Ivo-observatory-encounter.
- edges with owner/provenance: `CP2 derived_from AI1`; `NE2 conforms_to_plan CP2`; `NE2 mentions CC1,CC2,PL1,CE1`; `CC1/CC2 participates_in CE1`; `CE1 occurs_at PL1`.

Every retained relation has exact meaning and forbidden substitution:

- `derived_from`: plan used exact intent; never reverse inference.
- `conforms_to_plan`: excerpt declares the exact plan reference; not proof of quality/approval/comprehension.
- `mentions`: explicit reference only; not participation, location, truth, or motivation.
- `participates_in`: candidate character assertion only; not place participation or causal agency.
- `occurs_at`: candidate encounter-place assertion only; not excerpt location.
- `assessed_by`: exact subject bytes were input to a typed assessment; does not say result. Instances: `AU1→ED1`, `NE1→MA1/PAR1`, `AU2→ED2`, `NE2→MA2/CA1`, `GS1→GA1`.
- `event_evidenced_by`: strictly `AcceptedEvent→Receipt`; evidence is not authority/state. Instances: `EV07→ER1`, `EV11→MR1`, `EV12→CR1`, `EV18→ER2`, `EV22→MR2`, `EV24→GVR1`, `EV25→CAR1`, `EV26→RR1`.
- `receipt_invalidated_by_correction`: `MR1→EV12`; bytes/history remain immutable.

`precedes` stays killed for L0.

## Exact stale controls

| Control | Changed command field | Expected/actual | Rejection |
|---|---|---|---|
| Closure | `CMD03-STC.canonical_closure_sha256` | supplied `negative/stale-closure.json#supplied_sha256`; actual manifest closure digest | `REJ-STC-001 / STALE_CANONICAL_CLOSURE`; r2/head EV02 unchanged; zero starts |
| Artifact | `CMD05-STA.artifact_sha256` | supplied `negative/stale-artifact.json#supplied_sha256`; actual audition-v1 digest | `REJ-STA-001 / STALE_ARTIFACT_DIGEST`; r6/head EV06 unchanged; zero starts |
| Surface | `CMD05-STS.surface_sha256` | supplied `negative/stale-surface.json#supplied_sha256`; actual surface-v1 digest | `REJ-STS-001 / STALE_SURFACE_DIGEST`; r6/head EV06 unchanged; zero starts |

Each admission-rejection receipt binds rejected-command digest, expected/supplied refs, unchanged revision/head, activity-start count `0`, and `authority_effect:none`; it is not an AcceptedEvent receipt.

Other revision-1 negatives remain mandatory: missing approval/comprehension, reversed edge, forbidden endpoint, ownerless predicate, both crash points, same/different-byte duplicates, volatile fan-out, split runtime/journal, ontology-promotion, and public/deployment denied writes with equal protected before/after digests, and exact live/replay equality with no repeated completed effect.

## Remaining blockers and claim ceiling

Owners remain unbound for namespaces/relations, canonical runtime location, transitions/ceiling, admission/idempotency/effects, identity/privacy, journal/reducer/SQLite/CAS/recovery, canonicalization, activities, graph policy/validator, projection, co-op hosting, final acceptance, ontology promotion, product mutation, publication, deployment, release, and production.

This revision is a research-only acceptance contract. It creates no fixture, ontology, runtime, authority, product mutation, deployment, publication, release, or production proof.
