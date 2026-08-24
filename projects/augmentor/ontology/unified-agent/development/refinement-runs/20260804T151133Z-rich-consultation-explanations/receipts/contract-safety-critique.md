# Subagent Receipt: Contract And Safety Critic

- Agent: `Wittgenstein, Ludwig`
- Runtime agent ID: `/root/rich_explanation_critic`
- Role: `contract-safety-critic`
- Dispatch: `20260804T151133Z-rich-consultation-explanations`
- Step: `p3-contract-safety-critique`
- Capability: `interrogation`
- Status: flag; design repairs required, no refinement blocker
- Observer: not invoked
- Residue: current-state truth binding, glossary ownership/versioning, adversarial text handling, profile budgets, schema-version reconciliation, and measured comprehension

## Surviving Change Requests

| ID | Severity | Change request | Stop condition |
| --- | --- | --- | --- |
| CR-01 | high | Separate projection freshness from current-state truth. Bind modeled posture to field-level evidence, scope, verifier/owner, and verification time. | Do not expose `currentState` as live product truth without current owner evidence. |
| CR-02 | high | Bind projection, explanation packs, and glossary into one version/digest and atomic install boundary. | No independently mutable glossary sidecar. |
| CR-03 | high | Treat every rich text field as non-instructional evidence and add adversarial negative controls. | No new free-text field reaches a caller before instruction-shaped fixtures pass. |
| CR-04 | high | Preserve API/agent responsibility separation and reject API-generated prose. | No final narrative or rhetorical bridging inside the consultation service. |
| CR-05 | medium | Give examples a structural kind and every analogy a separate required limitation. | No unlabeled example or unbounded analogy. |
| CR-06 | medium | Bound profiles and truncate whole explanation units, never individual dependent fields. | No analogy without limitation or state claim without provenance after truncation. |
| CR-07 | medium | Reconcile repository `@0.1.0` JSON schemas with the compiler and consumer `@1.0.0` contracts. | No implementation against unexplained competing schema versions. |
| CR-08 | medium | Keep the glossary non-authoritative and return only referenced terms. | No glossary-created behavior, canonical redefinition, unknown ref, or unused term. |

## Candidate Verdict

- A, enriched records: retain only for small record-local fields; reject as the whole design because it duplicates glossary data and worsens payload/truncation.
- B, glossary sidecar plus explanation pack: accept with repair. It must be closed, non-authoritative, digest-bound, atomically installed, selectively returned, and composed by the agent.
- C, API-generated prose: reject. It contradicts the current service boundary and increases provenance, injection, and unsupported-inference risk.

## Key Evidence

- Compiler allowlist: `build-consumer-projection.mjs:16-19`.
- Every statement marked `freshness: current`: consumer service `augmentor-consultation-service.mjs:49-73`.
- Current text-copy and truncation behavior: same service `90-132`.
- Non-instruction and authority policy: `augmentor-consultation-answer-policy.mjs:16-24`.
- Repository schema version versus compiler/runtime version: `schemas/projection.schema.json:3-8`; compiler line 86; consumer contract version constants.

## Handoff

Candidate B survives only as a projection-bound, closed, size-limited evidence contract. Preserve agent-owned prose composition.
