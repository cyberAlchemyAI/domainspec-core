# Stage 05: Distill

- Capability: `distill`
- Mode: deep tournament
- Verdict: pass

## Broad Layer

The broad target is “make agents explain Augmentor better.” That includes source authoring, projection, retrieval, policy, narrative composition, page rendering, glossary, examples, analogies, current-state truth, and overhead.

## Candidate Tournament

| Candidate | Fit | Authority safety | Overhead | Evolution | Verdict |
| --- | --- | --- | --- | --- | --- |
| A. Enrich records only | medium | medium | poor through duplication | medium | retain only as a record-local mechanism |
| B. Explanation packs plus digest-bound glossary sidecar | high | high when repaired | high through selective return | high | select |
| C. API-generated prose | superficially high | poor | poor; adds model/runtime coupling | poor | reject |

## Smallest Coherent Unit

`ExplanationSupportBundle` is the smallest unit that remains meaningful:

- one neutral projection;
- record-local explanation packs;
- one glossary sidecar;
- one manifest that binds both artifacts and their schemas;
- one combined bundle digest used by loader, cache, and responses.

Removing the glossary creates repeated or undefined terms. Removing record-local packs destroys subject binding. Removing the shared manifest permits mixed versions. Adding final prose crosses the API owner boundary.

## Recomposition

```text
ExplanationSupportBundle
  + bounded consultation result
  + unchanged answer policy
  + agent composition profile
  + page rendering
  = deeper user answer without new authority
```

## Evolution Profile

Expected evolution is new concepts, revised beginner explanations, new glossary terms, and additional response transports. The smallest extension boundary is versioned profile metadata and optional pack fields inside the same closed bundle. A graph database, model call, whole reasoning engine, or canonical glossary owner is not justified.

## Premortem

Most likely failure: richer text sounds authoritative and current while it is only a reviewed ontology description. Guardrail: scoped posture, field provenance, explicit forbidden inferences, and negative fixtures that reject live-state overclaims.

## Navigation

Start with `stages/06-design.md`. Implement later from `WORK-PACK.md`, beginning with schema-version reconciliation before adding fields.
