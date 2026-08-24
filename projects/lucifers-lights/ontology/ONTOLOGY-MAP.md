# Lucifer's Lights Whisper Ontology Map

Status: `candidate-local`; author review pending

## Scope

- Repository: `/home/vrondelli/projects/domainspec-core/projects/lucifers-lights`
- Mode: `map`
- Mapping date: 2026-08-09
- Ontology type: `knowledge-vault`
- Project-local alias: `whisper-story-ontology`
- Runtime: `inline`
- Primary source boundary: project brief, Whisper intent, voice guide, Chapter 1,
  story-bible records, Craft state, and the earlier audited Whisper ontology findings

## Ontology type selection

Selection source is `inferred` with high confidence. The job is to preserve and
challenge narrative knowledge across author intent, manuscript evidence, canon
commitment, unresolved mysteries, editorial learning, and derivative drift.

Strongest excluded candidates:

- `business-domain` could model characters, rules, and story behavior, but would
  under-model revision evidence, canon commitment, and learning residue.
- `authority-governance` supports the source and owner boundaries, but ownership is
  not the ontology's primary modeling job.

No branch arguments are derived for `knowledge-vault`. The alias is local and does
not extend the reusable Ontology Vault catalog.

## Observed structures

| Structure | Local name | Generic concept | Evidence | Posture |
| --- | --- | --- | --- | --- |
| Creative intent | Project brief | author intent | `../PROJECT.md` | active-local |
| Composition substrate | Whisper intent | text intent substrate | `WHISPER-INTENT.md` | candidate-local |
| Prose | Chapter 1 | narrative artifact | `[repo-root] drafts/chapter-01.md` | editorial candidate |
| Character/place facts | Story bible | evidence index | `../story-bible/*.md` | active-local reference |
| Voice rule | tether rule | editorial constraint | `../editorial/VOICE-GUIDE.md` | active-local |
| Project state | Craft ledger | gate/gap/decision authority | `../.craft/ledger.yml` | authoritative for project state |
| Visual/audio work | derivative artifacts | transport projection | `[repo-root] drafts/graphic-novel/chapter-01/` | stale against current prose until checked |
| Prior research | Whisper ontology findings | synthesis evidence | `[repo-root] projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/findings.md` | research, not admission |

## Roles and axes

| Generic concept | Local labels | Purpose | Challenge response |
| --- | --- | --- | --- |
| Knowledge role | claim, rule, choice, mystery, constraint, drift, premise, reserve, residue | Distinguish how a statement may be relied upon or challenged. | Unknown roles fail validation. |
| Evidence confidence | explicit, corroborated, inferred, contested, unsupported | Describe source support. | Never converted automatically into commitment. |
| Commitment confidence | proposed, candidate, author-accepted, frozen-baseline, reserve, retired | Describe author reliance. | Author gate required for promotion. |
| Intent state | forming, volatile, frozen | Control Whisper derivative fan-out. | Current state is volatile; full derivative fan-out pauses. |
| Source posture | manuscript, intent, reference, project state, derivative, research | Preserve source authority and attribution. | A lower-authority source cannot silently override its owner. |
| Policy result | policy-pass, policy-fail, policy-indeterminate | Report finite graph-policy validation. | A pass has `authority_effect: none`. |

## Bounded story-world model

Whisper's existing composition meanings are reused rather than redefined:

- `AuthorIntentArtifact`
- `CompositionPlanArtifact`
- `NarrativeExcerptArtifact`
- `EvidenceAssessment`

Only three story-world kinds are introduced locally:

- `CandidateCharacterEntity`
- `CandidatePlaceEntity`
- `CandidateEncounterEntity`

Current witness:

| Kind | Instances |
| --- | --- |
| Candidate characters | Lucifer, Mara, Elena, Ruth, Michael, the pursuer pair |
| Candidate places | Vesper, Halo Café, old cathedral, Saint Orison Hospital, Saint Orison Station |
| Candidate encounters | Halo request, contract conflict/amendment, Halo escape, locker dead drop, tracker reveal, Michael request |

Props, typed requests/contracts, organizations, motives, causality, emotional truth,
temporal ordering, and place containment are deliberately deferred. Current story
knowledge about them remains in source-backed records rather than unowned graph
semantics.

## Edge rules

| Predicate | Owner | Allowed source | Allowed target | Cycle policy |
| --- | --- | --- | --- | --- |
| `derived_from` | Whisper | `CompositionPlanArtifact` | `AuthorIntentArtifact` | forbidden |
| `conforms_to_plan` | Whisper | `NarrativeExcerptArtifact` | `CompositionPlanArtifact` | forbidden |
| `mentions` | Whisper composition | `NarrativeExcerptArtifact` | any of the three candidate entity kinds | forbidden |
| `participates_in` | author-local | `CandidateCharacterEntity` | `CandidateEncounterEntity` | forbidden |
| `occurs_at` | author-local | `CandidateEncounterEntity` | `CandidatePlaceEntity` | forbidden |
| `assessed_by` | Whisper editorial | `NarrativeExcerptArtifact` | `EvidenceAssessment` | forbidden |

The validator rejects an unknown predicate, kind, endpoint pairing, or policy owner.
Relationship-like narrative statements such as request conflict or derivative drift
remain knowledge records until their typed semantics and owners are separately
approved.

## Load-bearing knowledge records

- A live transaction is the selected recurring scene engine.
- Lucifer's mythology is attributed testimony, not objective exposition.
- The prior Light constrains Mara's later request.
- Mara voluntarily accepts the narrower amendment and keeps agency in later choices.
- Sunrise is 5:38; the 2:13, 2:43, and 2:51 checkpoints retain exact arithmetic.
- Michael's identity and the unexpected request mechanism remain unresolved.
- Shared `Saint Orison` naming does not prove a hospital/station relationship.
- Ruth's removed son history remains reserve material.
- The bracelet action differs between prose and visual/audio adaptation and remains an
  explicit drift record.

## Premise review

Premise: the transaction-to-consequence engine can carry the series without becoming
formulaic.

- Evidence confidence: `corroborated` by the project brief, Whisper substrate, and
  Chapter 1 structure.
- Commitment confidence: `candidate`.
- Counterpressure: repetition could make later outcomes predictable.
- Falsification criterion: revise or split the premise if later chapters repeatedly
  need a different dramatic engine or the pattern suppresses character-specific
  movement.
- Recommendation: `keep`, without promotion.

## Inflection assessment

- Domain knowledge: `medium`
- Uncertainty: `high`
- Investment posture: `focused-experiment`
- Rationale: Chapter 1 supports one useful closed witness, but the wider series,
  long-arc history, deep contract semantics, and additional entity/relation needs
  remain unknown. A small validated ontology is justified; a universal fiction model
  is not.

## Gaps and drift

1. Chapter 1 and this ontology both await author acceptance.
2. Props, typed requests/contracts, and richer story relations are not admitted.
3. Chapter 2 and the larger series arc have no source evidence.
4. The bracelet prose/derivative drift is recorded but unresolved.
5. Graphic and audio derivatives remain unsynchronized with the current prose.
6. No Whisper runtime, query engine, Inventory projection, canonical ontology
   admission, publication, or release exists.

## Validation and authority

The package uses a closed-world Python validator and six negative fixtures. The
baseline returned `policy-pass`: 12 sources, 21 nodes, 40 edges, 23 knowledge
records, and six edge policies validated with no errors. All six negative fixtures
returned `policy-fail` with their expected diagnostic.

Even after a mechanical pass:

- the ontology remains `candidate-local`;
- `authority_effect` remains `none`;
- the current manuscript remains an editorial candidate;
- only the author may accept the ontology or promote local canon commitment;
- new kinds or predicates require a convention update with migration impact,
  negative evidence, and rollback.

## Ontology Vault Result

- Mode: `map`
- Repository: `/home/vrondelli/projects/domainspec-core/projects/lucifers-lights`
- Ontology type: `knowledge-vault`
- Type selection source: `inferred`
- Type selection confidence: `high`
- Ambiguity candidates: `business-domain`, `authority-governance`
- User selection required: `no`
- Project-local type alias: `whisper-story-ontology`
- Branch: `none`
- Runtime profile: `runtime-profile.json`
- Runtime mode: `inline`
- Sources reviewed: 12
- Business documents mapped: 0
- System documents mapped: 0
- Bridge edges checked: 0
- Drift findings: 1
- Traceability gaps: 6
- Sessions distilled: 0
- Delegated research records: 1
- Synthesis findings checked: 1
- Premises reviewed: 1
- Promotions recommended: 0
- Demotions recommended: 0
- Convention changes proposed: 0
- Contradictions found: 1
- Blockers: 0
- Outputs: `WHISPER-INTENT.md`, `whisper-story-ontology.json`, `ONTOLOGY-MAP.md`, `runtime-profile.json`, validator, negative fixtures
- Validation: `flag` — mechanical `policy-pass`; author review pending
- Next action: review the Whisper intent, entity set, knowledge roles, and deferred semantics; then accept or correct the candidate ontology.
