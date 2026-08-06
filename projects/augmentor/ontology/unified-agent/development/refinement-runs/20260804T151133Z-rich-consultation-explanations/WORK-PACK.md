---
module: augmentor-rich-consultation-explanations
version: candidate-0.1.0
status: implementation-ready-plan-owner-admission-required
updatedAt: 2026-08-04
docType: work-pack
---

# WORK-PACK: Rich Consultation Explanations

## Control Fields

| Field | Value |
| --- | --- |
| Work Pack gate | planning pass; mutation admission absent |
| Complexity | medium-high, two repositories and five retained owners |
| First unit | `SWU-RCE-000` |
| Execution order | serial within each owner boundary; stop at first failed gate |
| Product write authorization | not granted by this Refine run |
| External research | forbidden without a new confirmation |
| Deployment | excluded |
| Runtime | consumer validation requires Node `>=22.13.0` |
| Browser runtime | shared global Playwright; do not add a package root |

## Objective

Implement a digest-bound explanation-support bundle that lets agents produce deeper beginner-friendly responses while the consultation API remains read-only evidence retrieval and the agent remains the final prose owner.

## Required Inputs

- `stages/06-design.md`
- `stages/07-design-review.md`
- `stages/08-distill-repair.md`
- `stages/08-question-scenarios.md`
- `FEATURE-GLOSSARY.md`
- `WHISPER-COMPOSITION.md`

## Task Board

| Task | Units | Owner boundary | Status |
| --- | --- | --- | --- |
| [TASK-RCE-00](work-pack/tasks/TASK-RCE-00-SCHEMAS.md) | 000-001 | projection contract owners | ready for owner admission |
| [TASK-RCE-01](work-pack/tasks/TASK-RCE-01-PRODUCER.md) | 002-003 | private ontology and projection producer | blocked on 001 receipt |
| [TASK-RCE-02](work-pack/tasks/TASK-RCE-02-CONSUMER.md) | 004-006 | ResonantOS service and answering-agent owners | blocked on L1 bundle |
| [TASK-RCE-03](work-pack/tasks/TASK-RCE-03-PAGE-ACCEPTANCE.md) | 007-008 | page/product and validation owners | blocked on L2 |

## SWU Manifest

| SWU | Primary behavior | Exact target | Depends on | Acceptance boundary |
| --- | --- | --- | --- | --- |
| RCE-000 | Reconcile canonical producer/consumer schema versions without changing behavior. | repository schemas, compiler constants, consumer contract constants/tests | none | one version matrix; current projection/API tests unchanged |
| RCE-001 | Define closed explanation-pack, glossary, bundle-manifest, query, and result extensions. | DomainSpec consultation schemas/fixtures/validator | 000 | positive/negative schema fixtures and drift rejection |
| RCE-002 | Author structured examples, analogy limitations, glossary refs, keywords, and scoped state metadata for all 22 concepts. | `explanations/beginner.json` plus explanation validation | 001 | total coverage, jargon limits, example/analogy/glossary integrity |
| RCE-003 | Compile and validate one atomic neutral bundle. | compiler, generated projection/glossary/manifest, leakage tests | 002 | deterministic bytes, combined digest, atomic install contract, no private leakage |
| RCE-004 | Load and cache the atomic bundle in ResonantOS. | consumer contract/loader/cache/host service | 003 | mixed-version/digest/stale bundles fail closed; cache keyed by bundle digest |
| RCE-005 | Return optional bounded explanation support with semantic truncation and adversarial text safety. | consumer query/result/service tests | 004 | profile caps, whole-unit truncation, omissions, unchanged policy, injection negatives |
| RCE-006 | Compose brief/guided/deep answers outside the API. | answer-policy integration/reference/tests | 005 | identical evidence truth/status across profiles; citations, labels, limits, 2-5 used terms |
| RCE-007 | Render guided support and expose it to browser agents. | visualization template/build/output/tests | 006 | human and window API show the same safe support; raw JSON preserved |
| RCE-008 | Measure and close the five-scenario acceptance matrix. | producer/consumer/page tests and evidence report | 007 | budgets, browser, accessibility, responsive, no-console/page-error, compliant runtime |

## Recomposition

```text
000 version truth
 -> 001 closed contracts
 -> 002 total structured sources
 -> 003 atomic neutral bundle
 -> 004 verified consumer load/cache
 -> 005 bounded support return
 -> 006 agent-owned composition
 -> 007 page/browser-agent presentation
 -> 008 measured acceptance
```

No unit may be skipped. In particular, a UI-only edit would reintroduce unverified prose, and a glossary-only edit would create a driftable non-owner vocabulary source.

## Exact Source Scope

DomainSpec candidate sources:

- `projects/augmentor/ontology/unified-agent/explanations/beginner.json`
- `.../development/consultation-api/schemas/{query,result,projection,projection-manifest,evidence-statement}.schema.json`
- new `.../schemas/{glossary,explanation-support}.schema.json`
- `.../scripts/build-consumer-projection.mjs`
- `.../scripts/validate-contract.mjs`
- `.../scripts/validate-projection-leakage.mjs`
- generated consumer bundle
- consultation API tests and fixtures
- `scripts/build-visualization.mjs`, visualization template/output/tests

ResonantOS consumer sources:

- `browser-first/host/augmentor-consultation-contract.mjs`
- `browser-first/host/augmentor-consultation-service.mjs`
- `browser-first/host/augmentor-consultation-cache.mjs`
- `browser-first/host/augmentor-consultation-host-service.mjs`
- `browser-first/host/augmentor-consultation-answer-policy.mjs`
- `browser-first/test/augmentor-consultation*.test.mjs`
- `docs/reference/AUGMENTOR_CONSULTATION_API.md`

## Validation Commands

DomainSpec, after each producer unit:

```bash
node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/build-consumer-projection.mjs --check
node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-contract.mjs --scope query
node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-contract.mjs --scope result
node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-contract.mjs --scope projection
node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-projection-leakage.mjs
node --test projects/augmentor/ontology/unified-agent/development/consultation-api/tests/*.test.mjs
node projects/augmentor/ontology/unified-agent/scripts/build-visualization.mjs --check
node --test projects/augmentor/ontology/unified-agent/tests/visualization.test.mjs
```

ResonantOS under Node `>=22.13.0`:

```bash
node --test --test-concurrency=1 browser-first/test/augmentor-consultation.test.mjs browser-first/test/augmentor-consultation-deployment.test.mjs
npm run test:browser-first
npm run test:module-ownership
npm run docs:check
npm run test:docs
npm run verify:alpha
```

Browser acceptance from DomainSpec with the shared runtime:

```bash
node projects/augmentor/ontology/unified-agent/tests/agent-api.browser.mjs "$(npm root -g)/playwright"
```

## Global Stop Conditions

- Producer and consumer versions remain contradictory after RCE-000.
- A rich state claim lacks scope, verification time, owner/source binding, or non-establishment limits.
- Projection and glossary can be installed or cached under different digests.
- Any private path, concept ID, authority record, credential, or blocked field crosses the neutral boundary.
- Instruction-shaped retrieved text changes answer policy or becomes a tool/action request.
- Truncation separates example kind/text, analogy text/limitation, state/provenance, or glossary ref/entry.
- Any profile changes truth, evidence status, confidence, or authority.
- Final prose appears in the API response.
- The targeted profile budgets fail without owner-approved revision.
- Consumer final validation is run below Node `22.13.0`.
- Work expands into deployment, external research, canonical definitions, reasoning integration, or durable user preference storage.

## Owner And Admission Gaps

| Gap | Required owner action |
| --- | --- |
| G-01 schema owner | accept the canonical version family and compatibility rule |
| G-02 glossary/explanation source owner | accept structured source fields for 22 concepts |
| G-03 projection data owner | accept allowlist and atomic bundle rules |
| G-04 consumer service owner | accept query/result/loader/cache/service changes |
| G-05 answering-agent and page owners | accept profile composition and rendering contracts |
| G-06 validation owner | accept budgets, corpus, sample count, and browser evidence |

## Distill Validation

- All nine units own one primary behavior and a reviewable acceptance boundary.
- RCE-000 is the unique reversible first unit.
- Each later unit consumes the exact prior receipt and stops on drift.
- The chain recomposes into one `ExplanationSupportBundle` plus caller-owned composition.
- Deployment is intentionally absent.

## Next Route

Run `implementation-readiness` against this complete Work Pack. Freeze exact bytes and owner decisions for RCE-000 before any product mutation. Do not begin Task Session directly from this plan.
