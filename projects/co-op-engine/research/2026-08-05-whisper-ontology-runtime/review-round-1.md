# Review Round 1

All three independent reviewer lanes returned `REPAIR`. This is a design-gate result, not an implementation failure.

## Precedent and ownership

- Reclassify SQLite/CAS from selected architecture to `SELECT FOR FUTURE CANDIDATE DESIGN, OWNER-BLOCKED`.
- Reclassify the mapped namespace graph from `MERGE` to `DEFER OWNER BINDING` until the story-world kinds, relations, and mapping policy have a named owner.
- Narrow canonical ownership to existing Whisper intent, lifecycle, substrate, receipt, validation, and human-evidence meanings. Command/event, transition, admission, identity/privacy, journal, reducer, and execution contracts remain proposal-only.
- Keep the co-op adapter research-local and zero-authority.

## Definitional and authority non-collapse

- Rename run-local kinds so they cannot impersonate canonical concepts: `AuthorIntentArtifact`, `CompositionPlanArtifact`, `NarrativeExcerptArtifact`, `CandidateCharacterEntity`, `CandidatePlaceEntity`, and `CandidateEncounterEntity`.
- Remove `EvidenceRecord` as an ontology node; separate `EvidenceArtifact`, `EvidenceAssessment`, and transition `Receipt`.
- Split `RunReducer` from `RunStateSnapshot`; split lifecycle phase, pending gate, correction state, and outcome ceiling.
- Split assertion provenance, assessment kind, and independent `authority_grant_ref`.
- Repair edges: `conforms_to_plan`, `assessed_by`, `transition_evidenced_by`, and correction-specific invalidation; close all endpoint grammars.
- A rejected command is a non-semantic rejection record unless an owner explicitly defines rejection as a domain occurrence.

## Non-vacuity

- Make the finite fixture byte-bound: raw intent, closure, expected commands/revisions, exact audition/draft/graph/evidence/residue/projection digests, human actors/challenges, journal head, and replay-state digest.
- Instantiate separate editorial approval and comprehension evidence, plus distinct missing-evidence negatives.
- Add separate stale closure, artifact, and surface controls.
- Make correction mandatory after an initial mechanical pass, then regenerate and re-run gates.
- Split crash recovery after activity completion from recovery after activity start.
- Split denied writes for runtime/journal, ontology admission/promotion, and public-site/deployment effects.
- Kill `precedes` for L0 unless a second encounter is added; kill or instantiate every other retained edge/node.
- Define a graph-validation receipt with graph snapshot, policy/closure digest, diagnostics, result, validator identity, and `authority_effect:none`.

## Route consequence

Use one declared synthesizer-to-reviewers zig-zag turn. No explorer feedback is needed because the defects concern interpretation and contract precision, not missing source evidence.
