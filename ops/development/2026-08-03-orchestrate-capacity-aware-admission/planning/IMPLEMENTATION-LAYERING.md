---
module: orchestrate-capacity-aware-admission
version: candidate-v0
status: approved-plan
updatedAt: 2026-08-03
docType: implementation-layering
---

# Implementation Layering: Capacity-Aware Orchestrate Admission

## Target and scope

- Target: canonical public `arcanum/runtime/orchestrate`
- Scope: host-neutral capacity admission plus Codex profile binding and honest
  failed-spawn evidence
- Current state: Orchestrate is implemented and tested for dispatch validation,
  wave compilation, native spawn/join, partial-wave cleanup, and causal
  validation, but has no pre-spawn capacity input or admission decision
- Complexity: high because strict schemas, canonical/generated ownership, host
  integration, and unresolved lease/release authority cross multiple gates

## Layer decisions

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether Orchestrate can reject a complete wave from frozen capacity evidence before emitting any spawn action and can close a residual pre-agent host failure without fabricating identity. | `SWU-OCA-001` admission seam followed by independent `SWU-OCA-002` failure-evidence repair | versioned evidence/decision schemas, deterministic all-or-zero evaluator, preflight receipt, null-agent blocked failure branch | live provider, reservation, release, route UI, generated sync | positive/missing/stale/insufficient/unknown fixtures; zero actions and attempts on block; valid failed-spawn causal stream | continue to L1, repair, or stop |
| L1 | After this layer, we know whether the current Codex host profile can expose its actual evidence ceiling and return useful owner-safe route alternatives without changing approved topology. | Codex provider/unknown binding plus neutral route-option projection and generated parity | versioned provider capability declaration, current unsupported fallback, synthetic authoritative mapping fixture, reapproval flags, three generated surfaces | live provider when no native operation exists, atomic reservation, physical release, context-safe reuse, consumer UI | provider matrix; no inferred numeric limit; option feasibility/approval tests; generation parity | retain conservative admission, request host extension, or stop |
| L2 | After this layer, we know whether capacity admission remains correct under concurrent allocation and physical lifecycle transitions. | separately admitted host reservation/release canary | atomic lease, expiry, consume/release, physical lifecycle evidence, race fixtures, independent live canary | generalized scheduler and queue | host-owner receipt plus race and release evidence | harden, narrow, or stop |
| L3 | After this layer, we know whether consumer adoption and release are justified. | separately planned adopter package | DomainSpec/Subagent Strategy timing, Augmentor plain-language projection, public release and compatibility process | broader provider ecosystem | consumer fixtures, audited public boundary, release-owner evidence | publish, pilot, or defer |

## Value/cost boundary

- L0 removes the earliest controllable failure and repairs the observed causal
  evidence defect without depending on a live host API.
- L1 makes degraded behavior usable and proves exact generated parity, but
  preserves an honest `unknown` result when the host lacks capacity authority.
- L2 is not pulled forward: snapshot checks cannot provide atomic reservation
  or physical release, and implementing a scheduler inside Orchestrate would
  duplicate the host.
- L3 consumer and release work creates less value for the current defect than
  first proving L0/L1.

## Non-regression guardrails

- Existing dispatch validation, authorization, no-spawn preflight, exactly-once
  action, join-all, partial-wave cleanup, and dependency-gate behavior remain.
- `legacy_v0_1` is confined to a separately named compatibility entrypoint for
  declared current fixtures; governed multi-agent execution always selects
  `strict_whole_wave_v0_2`, where missing or partial inputs block without
  downgrade.
- A blocked capacity decision always has zero action documents and zero spawn
  attempts.
- v0.1 evidence remains distinguishable from candidate v0.2 evidence.
- No layer infers numeric capacity, physical release, or safe reuse.
- Public Arcanum receives no private incident, account, quota, tier, project,
  or consumer prose.
- Generated packages are regenerated from canonical source and never edited as
  authority.

## Recommended next layer

- Next layer: L0
- First selected unit: `SWU-OCA-001`
- Key decision: whether a frozen, versioned capacity input can block the whole
  wave before action emission while preserving current preflight semantics
- L0 policy: snapshot-only; every reservation-required input blocks as
  unsupported until a separately admitted host contract exists
- Major deferral: race-free reservation and physical slot release wait for an
  explicit host contract
