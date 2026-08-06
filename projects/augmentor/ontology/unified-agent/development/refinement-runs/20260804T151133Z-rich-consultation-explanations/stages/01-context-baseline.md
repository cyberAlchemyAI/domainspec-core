# Stage 01: Context Builder Evidence Baseline

- Capability: `context-builder`
- Mode: deep, strict, both formats, runtime handoff
- Verdict: pass with environment flag
- Subagent input: `../receipts/current-state-map.md`
- Handoff: `../context-builder/runtime-handoff.md`

## Current System, In Plain Language

Augmentor currently has a working read-only consultation path over a reviewed neutral projection. It can find matching records, return source-linked evidence, and tell an answering agent whether to answer, qualify, clarify, or abstain. It does not write the answer, decide truth, change memory, approve work, or run a reasoning engine.

## Authored-To-Consumer Map

```text
private ontology node + beginner explanation
  -> allowlisted compiler
  -> opaque 22-record neutral projection + manifest
  -> consumer loader, access policy, cache, and retrieval
  -> evidence statements + answer policy
  -> answering agent composes user-facing prose
  -> page renders evidence and exposes a browser-agent API
```

The beginner source has seven explanatory fields. The compiler currently carries four contents: friendly name, plain meaning, process, and boundary. It drops the present/planned state, concrete example, and analogy.

## Verified Versus Absent

| Area | Verified now | Not established |
| --- | --- | --- |
| Ontology presentation | 22 beginner explanations, lanes, candidate claim ceiling | official authority or production truth |
| Projection | deterministic, opaque, allowlisted, source-linked bundle | rich explanation pack or glossary |
| Retrieval | exact-ID and exact-token overlap with bounded results | semantic reasoning or inferred conclusions |
| Answer policy | answer, qualify, clarify, abstain; citations; no instructions; authority none | final prose composition contract |
| Reasoning | private bounded evaluator witness exists elsewhere | admitted Augmentor reasoning adapter, catalog/applicability owner, or effect integration |
| Page | API view, question form, result evidence, raw JSON, browser-agent methods/events | rich narrative answer rendering |

## Current Validation

- Projection `--check`: pass; output digest `235af912339c8fae0c21f21e1ace40eab37d5141bd3e9d37365497f016937e49`.
- Candidate consultation suite: 25/25 pass.
- Consumer consultation suite: 8/8 targeted tests pass locally.
- Environment flag: local Node is `v22.12.0`; consumer requires `>=22.13.0`.

## Context Builder Result

- Files selected: 15 bounded sources plus three subagent receipts.
- Obligation coverage: 100 percent covered or explicitly resolved.
- Noise: low; whole repositories were not loaded.
- Runtime handoff: pass.
- Blockers: none for planning.
