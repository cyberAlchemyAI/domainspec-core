# Domain: High-Attention, Low-Parameter Experiment Protocol

## ExperimentProtocol

Immutable versioned contract containing claim boundary, factors, arms, outcomes,
analysis rules, resource boundaries, failure policy, and phase gates.

Required invariants:

- `status = frozen` before materialization or execution.
- Every material change creates a new `protocol_id` and content hash.
- Every decision field points to an approved [ProtocolDecision](#protocoldecision).

## ProtocolDecision

| Field | Constraint |
| --- | --- |
| `decision_id` | Stable and unique. |
| `question` | One consequential choice. |
| `selected` | Explicit value or `unresolved`. |
| `alternatives` | Rejected/available alternatives. |
| `rationale` | Evidence or bounded project preference. |
| `owner` | Human or lifecycle owner. |
| `approval` | Timestamped approval handle or absent. |

## FixtureInstance

One deterministic semantic plan plus rendered variants. It records family,
split, seed, evidence facts, decoys, answer, evidence IDs, contradiction state,
and source/provenance hashes.

## PromptArm

| Arm | Required semantics |
| --- | --- |
| `compact_evidence_complete` | Only necessary evidence plus constant instructions. |
| `full_evidence_complete` | Identical answer evidence plus controlled filler/decoys. |
| `evidence_absent` | Evidence removed; correct behavior is abstention/no-support. |
| `no_answer` | Context explicitly contains no supported answer. |
| `oracle_selection` | Optional selected evidence with oracle receipt; secondary contrast. |
| `retrieved_selection` | Optional frozen retrieval receipt; system costs must be charged. |

## TrialCell

Exact tuple of protocol version, fixture, arm, evidence position, context length,
interference level, model stack, repetition, and seed. A cell is immutable once
queued.

## ModelStack

Immutable identities for checkpoint snapshot, tokenizer, chat template,
runtime image, attention backend, precision, KV policy, hardware, driver, CUDA,
and relevant package versions.

## CapacityWitness

Records requested/rendered token counts, KV allocation, memory high-water mark,
prefill/decode completion, and assertions that truncation, offload, preemption,
fallback, recomputation, and OOM recovery did not occur.

## RunReceipt

Links one trial attempt to the exact input, stack, raw output, timestamps,
prefill/decode telemetry, resource telemetry, attempt number, and typed failure.

## ScoreReceipt

Records parser result, answer outcome, evidence outcome, abstention/support
outcome, false-support eligibility, scorer version, and any adjudication.

## AnalysisResult

Records the frozen analysis-plan hash, included/excluded cells, paired contrasts,
uncertainty, multiplicity adjustment, feasibility, and claim-bounded verdict.

## ResourceFrontier

Named axes and non-dominated cells. At minimum it preserves capability,
prefill latency, decode latency, memory, energy boundary, and parameter count
separately. Cost is added only with a dated, declared accounting source.

## Typed Failure Codes

`manifest_invalid`, `fixture_invalid`, `render_invalid`, `template_mismatch`,
`checkpoint_unavailable`, `capacity_unproven`, `truncated`, `offloaded`,
`preempted`, `fallback_used`, `oom`, `runtime_error`, `parse_error`,
`score_error`, `telemetry_missing`, `analysis_ineligible`, `operator_abort`.
