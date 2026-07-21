# Backend Test Engine Implementation Architecture X-Ray

## x-ray Result

- Status: `flag`
- Mode: `architecture`
- Target boundary: DomainSpec v2 backend structural proof implementation, from versioned machine sources and profile selection through compilation, exact obligation/test derivation, execution, mutation, receipts, replay, and independent consumer receipt validation
- User intent: understand clearly how the Backend Test Engine will be implemented, not only why Option 2 was selected
- Reader baseline: `newcomer`
- Output: [`index.html`](index.html)
- Machine lanes: [`lanes.json`](lanes.json)
- Layer interaction: `stacked`, `isolate`, `compare`, `trace`
- Renderer level: `L0 static HTML/SVG`

## Status Meaning

The x-ray output passes its structural validation. The inspected architecture is flagged because the current package has a completed Define but no current Design artifact. `IMPLEMENTATION-LAYERING.md` and `PLAN.md` predate audit 002 and contain superseded formation-authority and readiness assumptions. Their code-level detail is evidence of earlier intent, not authorization for implementation.

The page therefore separates:

1. source-backed existing code;
2. requirements-backed proposed architecture;
3. owner-controlled decisions and admission gates;
4. missing Design contracts that must be materialized before source work.

## Lane Handles

- surface: `surface.summary`
- properties: `properties.catalog`
- components: `components.map`
- internal_dependencies: `dependencies.internal`
- external_dependencies: `dependencies.external`
- flow: `flow.graph`
- lifecycle: `lifecycle.timeline`
- risk_questions: `risk.questions`
- visual_composition: `visual.model`

## Architecture Result

The recommended architecture has four non-collapsible planes:

1. Authority and authored input: successor profile, formation contracts, JSON retirement map, relationship admission, and project/feature/node/edge sources.
2. Compiler runtime: resolver, contract loader, envelope validation, shared criterion kernel, edge resolution, normalized graph, and source manifest.
3. Proof and evidence: independent `O_spec`, minted proof adapter, derived `O_gen`, exact-set comparison, TestCase/Binding/Evaluator runtime, execution, mutation, receipts, replay, and `verify:bte:core`.
4. Independent consumers and gates: fresh IOLM and Body War receipts, `verify:bte:consumers`, terminal `verify:bte`, and externally controlled admission/release decisions.

The central correction is to add a dedicated `MintedGraph` plus `MintedSourceManifest` proof path. The existing engine entrypoint parses Markdown/aspect documents into a legacy `ConceptGraph`; it must not become the canonical minted-project derivation input. Deterministic utilities may be reused only where their contracts preserve all required profile, source, schema, criterion, evaluator, and digest identities.

## Visual Library

Canonical components:

- `shape.node`
- `shape.boundary`
- `shape.layer-panel`
- `shape.risk-marker`
- `connector.arrow`
- `connector.branch`
- `connector.feedback-loop`
- `chart.timeline-strip`
- `chart.risk-matrix`

Canonical patterns:

- `pattern.dependency-boundary`
- `pattern.lifecycle-stack`
- `pattern.evidence-inference-split`

Custom-pattern nudge: a reusable `exact-proof-chain` pattern may be justified after Design validates the stable-ID equality and causal digest chain beyond this one example. It is local explanatory inference in this x-ray, not a canonical library addition.

## Evidence Boundary

Source-backed facts include current code modules and behaviors, requirements, the accepted formation direction, current-v1 profile declarations, exact denominators, gap states, the existing compiler graph/manifest, the legacy engine input path, first-match bindings, and skip/todo emitter behavior.

Inference includes the four-plane decomposition, dedicated minted proof IR, proposed module names and homes, immutable stage-record style, and seven implementation slices. These recommendations preserve the live requirements but require Invoke Design acceptance.

## Reader On-Ramp

The page introduces the architecture as four plain-language planes before using local terms. It defines authority plane, compiler plane, proof plane, normalized graph, source manifest, independent catalogue, binding, evaluator, mutation, receipt/replay, and exact-set proof with why-it-matters and misuse warnings.

## Validation

- X-ray example validation: `PASS`
- Lane schema: canonical `arcanum/arcana/x-ray/schemas/xray-lane-model.schema.yml`
- Required layer controls: present
- All nine lanes and reader outcomes: present
- Source-backed and inference labels: present
- Local linked source artifacts: present
- Remote scripts, stylesheets, images, and links: absent
- First schema pass: blocked on unsupported mixed authority labels and a missing external-dependency reader outcome; both were corrected before the final pass
- Browser screenshot inspection: unavailable because the environment has no Chromium executable; the page will be served for direct browser review

## Missing Design Contracts

Invoke Design must still freeze at least:

- successor profile ID/version and formation-authority record;
- JSON-to-YAML retirement-map schema, migration statuses, compatibility corpus, and failure precedence;
- literal `required_structure`, Interface/Mapping closed domains, and structural Value Object equality;
- independent edge schema, source roots, scope/direction/order/lifecycle rules, and relationship admission handle;
- minted proof IR and obligation identity schema;
- TestCase, Binding, Evaluator, ExecutionResult, MutationResult, Receipt, and replay schemas;
- exact aggregate manifests and error taxonomy;
- accepted module boundaries and filenames;
- regenerated implementation layering, Plan, work-pack dependencies, and next Task Session candidate.

## Signal Observer Result

- Observed sigil: `x-ray`
- Result: `recorded`
- Ledger: `.arcanum/observability/signals/sigil-invocations.jsonl`, line 269
- Signals: quality pass, user-correction rework, one low process gap, one medium intent-routing gap, and one high missing-Design input gap
- Quality Bar: `pass`
- Anti-Pattern hits: none in the revised run
- Reflection trigger: `manual`
- Recommendation: `reflect-now`
- Validation: the first observer attempt exposed an empty-run-ID dedupe collision; adding a unique run ID recorded the distinct invocation successfully
