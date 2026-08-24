# Lucifer's Lights Whisper Ontology

This package is a candidate-local authoring ontology for *Lucifer's Lights*. It lets
Whisper retrieve the smallest source-backed context needed to continue or revise the
novel while keeping evidence, canon commitment, mysteries, editorial constraints,
and derivative drift distinct.

It is not a universal story ontology, an accepted Chapter 1 baseline, a generation
runtime, or an Arcanum vocabulary extension.

## Start here

1. Read [WHISPER-INTENT.md](WHISPER-INTENT.md) for the resonance, relevance, and
   trajectory substrate.
2. Read [ONTOLOGY-MAP.md](ONTOLOGY-MAP.md) for the human model and its gaps.
3. Query or inspect [whisper-story-ontology.json](whisper-story-ontology.json) for
   typed entities, closed relations, knowledge records, evidence, and confidence.
4. Check [runtime-profile.json](runtime-profile.json) before any map, validation,
   confidence, premise, or drift operation.
5. Run the local validator and read the latest file under [receipts/](receipts/).

## Package

| File | Responsibility |
| --- | --- |
| `WHISPER-INTENT.md` | Derived authoring substrate and Whisper composition contract for this novel. |
| `whisper-story-ontology.json` | Machine-readable candidate ontology and source registry. |
| `ONTOLOGY-MAP.md` | Human-readable Ontology Vault map and current claim boundary. |
| `runtime-profile.json` | Inline runtime scope, owner gates, allowed outputs, blocked effects, and residue route. |
| `scripts/validate.py` | Dependency-free closed-world validator. |
| `fixtures/closed-world-negatives.json` | Negative witnesses for unknown kinds, predicates, endpoints, owners, confidence values, and sources. |
| `receipts/` | Validation evidence; never ontology or project-state authority. |

## Model boundary

Whisper continues to own composition meanings such as author intent, composition
plan, narrative excerpt, and evidence assessment. This project introduces only:

- `CandidateCharacterEntity`
- `CandidatePlaceEntity`
- `CandidateEncounterEntity`

Rules, choices, mysteries, editorial constraints, drift, premises, reserve material,
and learning residue are knowledge records. They do not become new universal entity
kinds by proximity.

The graph admits only six predicates in this first version:

- `derived_from`
- `conforms_to_plan`
- `mentions`
- `participates_in`
- `occurs_at`
- `assessed_by`

Every predicate has exact endpoint kinds and a named local policy owner. Unknown
kinds, predicates, endpoint pairs, owners, evidence states, commitment states, or
source references fail closed.

## Validate

From the repository root:

```bash
python3 projects/lucifers-lights/ontology/scripts/validate.py --self-test
```

A successful run proves JSON integrity, source digests where pinned, profile
completeness, closed-world graph policy, evidence references, confidence vocabulary,
coverage invariants, and rejection of the negative fixtures. It does not prove
editorial quality, canon acceptance, a working Whisper runtime, or derivative sync.

## Use for later Whisper work

A later composition pass may use the ontology to answer bounded questions such as:

- Which established characters and places can enter the next encounter?
- Which story rules constrain a proposed Light?
- Which live dramatic job earns a Lucifer aside?
- Which mysteries must remain unresolved?
- Which derivative actions drift from the bound manuscript?

The result is context or a warning, never permission to mutate the manuscript. New
story text must still pass Whisper composition and author review.

## Update discipline

1. Change or add the owning manuscript or author-approved source first.
2. Preserve its path and evidence posture in `source_registry`.
3. Update only the affected nodes, edges, or knowledge records.
4. Add a negative fixture before admitting a new kind or predicate.
5. Run validation and preserve the result under `receipts/`.
6. Route author commitment, Craft state, derivative synchronization, publication,
   and release through their separate owners.

If a source digest changes unexpectedly, validation fails. The Craft ledger and
source map are live owner surfaces and are intentionally path-bound rather than
digest-pinned here to avoid circular authority.

## Authority

- Manuscript owns prose.
- Project brief and voice guide own active-local creative intent and constraints.
- Story bible indexes Chapter 1 evidence and unknowns.
- This ontology owns only its candidate-local graph and knowledge records.
- Craft owns project gates, gaps, decisions, and next moves.
- Graphic and audio artifacts remain derivatives.
- The author owns acceptance and local canon commitment.

`authority_effect` remains `none` for every validation receipt.
