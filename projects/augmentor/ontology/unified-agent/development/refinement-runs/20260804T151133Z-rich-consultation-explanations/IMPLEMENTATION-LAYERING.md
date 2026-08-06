# Implementation Layering: Rich Consultation Explanations

## Layer Map

| Layer | Outcome | Evidence required before advancing | Claim ceiling |
| --- | --- | --- | --- |
| L0 Contract baseline | One reconciled schema/version family and closed explanation/glossary/bundle contracts. | schema fixtures, producer/consumer drift tests, zero behavior change | contract authored and validated |
| L1 Neutral producer | Structured beginner sources compile into one leakage-safe atomic bundle. | deterministic build, manifest closure, source/ref checks, adversarial leakage fixtures | candidate-local projection evidence |
| L2 Consumer and agent | Consumer loads/caches the bundle, returns bounded packs, and agents compose three profiles under unchanged policy. | service, cache, truncation, adversarial text, profile parity, and integration tests under Node >=22.13.0 | local consumer implementation evidence |
| L3 Page and acceptance | Page renders rich support and browser agents consume the same contract; budgets are measured. | build, unit, browser, accessibility, responsive, payload, latency, and scenario evidence | validated local acceptance; no deployment claim |

## Layer Decisions

### L0

Resolve the current `@0.1.0` repository schemas versus `@1.0.0` compiler/runtime contracts before adding fields. This is not bookkeeping: an implementation against the wrong schema would produce false validation evidence.

### L1

The glossary may be a separate file for reuse, but it is not a separate release. Projection, glossary, schemas, and manifest form one atomic bundle. The producer remains one-way and cannot write back to ontology sources.

### L2

Profile selection is optional and backward-compatible. It changes the amount of support returned, not evidence status. The service remains deterministic and adds no model call. The answering agent owns transitions, storytelling, and final response selection.

### L3

The API page defaults to `guided`, visibly labels teaching material, and preserves raw JSON. Browser acceptance uses the shared Playwright runtime. Deployment is a separate future route and is not included here.

## Promotion And Owner Gates

- Private ontology explanation owner accepts structured source changes.
- Projection data owner accepts new neutral fields and leakage rules.
- Consumer service owner accepts schema, loader, cache, and service changes.
- Answer-policy/agent owner accepts composition conformance without prose generation in the API.
- Page owner accepts rendering and browser-agent contract changes.
- No canonical definitions, authority state, public Arcanum capability, deployment, release, or production status changes in these layers.

## Measurement Gates

Proposed targets, to be accepted or revised by the service owner:

- compact installed bundle for 22 records: at most 64 KiB;
- brief support: at most 6 KiB and 1,200 estimated tokens;
- guided support: at most 16 KiB and 2,400 estimated tokens;
- deep support: at most 32 KiB and 4,800 estimated tokens;
- added in-memory support assembly p95: at most 10 ms over at least 1,000 fixture iterations;
- zero pack-integrity failures under every truncation limit;
- zero policy changes across brief/guided/deep for identical evidence;
- all five question scenarios pass deterministic content assertions.

Passing these targets would establish bounded local behavior, not human comprehension. A human study remains separate research.
