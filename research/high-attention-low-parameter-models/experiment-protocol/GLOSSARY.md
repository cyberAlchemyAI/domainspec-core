---
module: high-attention-low-parameter-experiment-protocol
status: draft
updatedAt: 2026-07-18
docType: feature-glossary
observedCapability: invoke
invokeMode: define
---

# Glossary: High-Attention, Low-Parameter Experiment Protocol

These definitions govern this experiment package only. They do not promote
canonical Arcanum or DomainSpec vocabulary.

| Term | Definition | Status | Source / rationale |
| --- | --- | --- | --- |
| Present tokens | Exact post-template token sequence supplied to the runtime. Presence says nothing about retention or successful use. | linked | [Research findings](../experiment-protocol-research/findings.md#repaired-constructs-and-estimands) |
| KV-retained tokens | Tokens whose key/value state is proven resident under the frozen runtime policy. Retention says nothing about behavioral use. | linked | Research findings |
| Retrieval-selected tokens | Exact tokenized material selected under a frozen retrieval receipt. Selection is not equivalent to raw visibility. | linked | Research findings |
| Successful information use | Correct answer plus separately correct evidence provenance when evidence is required. It is a fixture-level outcome. | linked | Research findings |
| Visible context | Input positions accepted and presented by a model/runtime stack. | partial | Prior framing; operationalized here as present tokens plus admission evidence. |
| Usable context | Prohibited as a single unqualified metric. Use named retention, checkpoint, position, support, and false-support estimands instead. | linked | Prior formulation received typed KILL. |
| Full-context retention | Frozen score difference or ratio between full and compact arms containing identical answer evidence. Evaluated as non-inferiority. | linked | Research findings |
| Added-evidence behavior | Paired evidence-present support and evidence-absent abstention behavior. | linked | Research findings |
| Direct checkpoint contrast | Paired outcome difference between admitted checkpoints on the same instance and condition. | linked | Research findings |
| Difference-in-retention | Difference between checkpoints' full-versus-compact retention. Required for a “uses long context better” claim. | linked | Research findings |
| Middle loss | Middle-position outcome minus the mean of early and late rotations of the same semantic instance. | linked | Research findings |
| False support | Erroneous support assertions divided by eligible evidence-absent or contradiction controls. | linked | Research findings |
| Prompt arm | One frozen evidence/context condition with its own correct-output semantics. | feature-local | This spec. |
| Trial cell | Fully specified factor tuple for one model invocation attempt. | feature-local | This spec. |
| Model stack | Immutable checkpoint, tokenizer, chat template, runtime, backend, precision, KV policy, hardware, and driver identities. | feature-local | Platform ownership surface. |
| Capacity witness | Machine-readable evidence that a model/length cell fits without prohibited fallback behavior. It is not capability evidence. | feature-local | Platform ownership surface. |
| Run receipt | Immutable linkage from trial cell and manifests to raw output, timing, telemetry, and failure state. | feature-local | This spec. |
| Resource frontier | Non-dominated set over explicitly named capability and resource axes with infeasible cells preserved. | linked | Budgeted-comparison findings. |
| Decision pilot | First paired run capable of changing the project's experiment/deployment decision. | linked | Staged escalation findings. |
| Runnable witness | Minimal material tuple of generator/data, renderer/scorer, admitted stack, repetitions, thresholds, and validation needed to execute a falsifiable trial. | linked | Reviewer non-vacuity gate. |

## Forbidden Collapses

- Present is not retained; retained is not selected; selected is not used.
- Long advertised context is not a capacity witness.
- Dense resident KV is not a behavioral attention result.
- Within-family checkpoint comparison is not parameter causality.
- External-family comparison is not an independent replicate.
- Capability, latency, energy, cost, and parameter count are not one score.

## Promotion Boundary

All terms are `linked`, `partial`, or `feature-local`. Nothing in this file
promotes a candidate to canonical Definitions Governance authority.
