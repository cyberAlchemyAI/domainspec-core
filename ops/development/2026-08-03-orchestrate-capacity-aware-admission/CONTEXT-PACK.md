# Context Pack

## Task

Author an implementation-ready but non-executing Define, Design, and Plan
package for capacity-aware whole-wave admission in Arcanum Orchestrate.

- Mode: standard
- Strict obligation coverage: pass for authoring
- Runtime handoff pack: none; Context Builder must create it at execution time
- Inventory lookup readiness: pass, with 141 historical tag warnings
- Inventory authority: non-authority read model only

## Obligation matrix

| ID | Obligation | Selected evidence | Status |
| --- | --- | --- | --- |
| O1 | Explain the observed failure without claiming hidden host internals. | failed preflight, event stream, evidence-validation receipt | covered |
| O2 | Find the earliest boundary that can prevent a partial wave. | Orchestrate preflight, host profile, coordinator compile path | covered |
| O3 | Preserve current no-spawn preflight semantics. | `SKILL.md`, preflight tests | covered |
| O4 | Keep host observation separate from deterministic admission. | host profile, coordinator, helper challenge | covered |
| O5 | Represent a host spawn rejection as honest terminal evidence. | run-event schema, receipt schema, evidence validator, incident trace | covered |
| O6 | Offer safe alternatives without silently changing approved parallelism. | Augmentor routing/subagent research results | covered |
| O7 | Separate logical close from physical slot release. | join contract plus current host inventory behavior | covered as required distinction; live release API absent |
| O8 | Preserve public/private and canonical/generated ownership. | repository instructions and Orchestrate generation manifest | covered |
| O9 | Produce L0-L3 layers, atomic SWUs, validation, and closeout contracts. | Invoke Plan contract and templates | covered by planning outputs |

## Selected sources

| Source | Selectors | Why selected |
| --- | --- | --- |
| `arcanum/runtime/orchestrate/SKILL.md` | execute preflight; native spawn/join; failure policy | canonical lifecycle owner and current no-spawn boundary |
| `arcanum/runtime/orchestrate/hosts/codex-native.md` | preflight; spawn mapping; join mapping | current host-specific mapping and evidence limits |
| `arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py` | `compile_first_wave`; `_compile_named_wave_actions`; `reduce_wave_receipts` | expands the full wave and reduces receipts without capacity input |
| `arcanum/runtime/orchestrate/scripts/validate_run_evidence.py` | host results; `receipt_joined`; `gate_decided` | exposes the no-agent spawn-failure evidence gap |
| `arcanum/runtime/orchestrate/schemas/run-event.schema.json` | event enum and conditional identities | current causal event vocabulary |
| `arcanum/runtime/orchestrate/schemas/receipt.schema.json` | required `agent_id`; status/validation | current action receipt cannot represent pre-agent rejection |
| `arcanum/runtime/orchestrate/tests/preflight/test_preflight_contract.py` | `evaluate_preflight`; ready test | proves preflight checks operations and compiles all three actions only |
| `arcanum/runtime/orchestrate/tests/partial-wave/test_partial_wave_recovery.py` | recovery algorithm and tests | proves post-failure cleanup is distinct from prevention |
| `ops/development/2026-08-03-pre-task-session-readiness-gap-research/native-run/run-01/preflight-receipt.json` | entire receipt | observed `wave_ready`, action count 3, capacity absent |
| `ops/development/2026-08-03-pre-task-session-readiness-gap-research/native-run/run-01/events.jsonl` | events 1-6 and 22-23 | two successful spawns, one capacity failure, then synthetic join |
| `ops/development/2026-08-03-pre-task-session-readiness-gap-research/native-run/run-01/evidence-validation.json` | both diagnostics | exact `join_without_host_result` and `gate_missing_joined_receipt` failure |
| `.arcanum/inventory/entries/pre-task-session-readiness-gap-research-blocked-result-synthesis.md` | Outcome; Recovery | non-authority incident orientation and claim ceiling |
| `.arcanum/inventory/entries/augmentor-subagent-strategy-integration-research-result-synthesis.md` | Honest Degraded Modes; Next Owner Route | no invented queue; material route changes need explicit owner control |
| `.arcanum/inventory/entries/augmentor-routing-session-fabric-research-result-synthesis.md` | Classification And Route Decisions; Open Decisions | route offers and session alternatives remain separate owner decisions |

## Evidence and inference boundary

Observed:

- the failed preflight had no capacity fields and emitted three actions;
- two spawns returned agent identifiers and the third returned the literal
  thread-limit error;
- current host inventory lists retained completed child entries;
- current canonical preflight and coordinator accept no capacity evidence;
- the current evidence validator rejects a joined receipt for a failed spawn.

Inferred, not proven:

- retained completed threads may consume a host lifetime or session ceiling;
- a refresh likely creates a new capacity scope;
- an atomic reservation would prevent snapshot races.

The package therefore forbids deriving a numeric capacity limit, release proof,
or reusable slot from status counts or an error string.

## Excluded candidates

- `cyberAlchemy-v2` ontology and authority definitions: no new ontology kind is
  needed for a host scheduling contract.
- generated `.agents`, `.claude`, and `.arcanum/runtime` Orchestrate packages:
  downstream projections only, never authoring sources.
- Task Session product behavior: downstream consumer of a route, not the owner
  of host capacity.
- Augmentor UI implementation: later consumer package after the neutral result
  contract exists.

## Open source-level gaps

- No active host operation currently reports an authoritative capacity limit,
  reservation, or physical release.
- `collaboration.list_agents` reports inventory, not total capacity authority.
- The current host contract does not prove whether completed entries are
  reusable, releasable, or permanently retained.

