---
id: arcanum-framework-runtime-and-observability-boundary
kind: page
type: architecture-layer
title: Arcanum framework runtime and observability boundary
updated: 2026-08-06
status: verified
confidence: high
tags:
  - inventory
  - arcanum
  - arcanum-runtime
  - observability
  - determinism
  - public-private-boundary
  - claim-le-proof
sources:
  - arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md
  - arcanum/framework/observability/HOOK-OPERATIONS-LEDGER.md
  - arcanum/framework/observability/OBSERVED-RUNS.md
  - arcanum/framework/observability/README.md
  - arcanum/framework/observability/REPOSITORY-PACKAGE.md
  - arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md
  - arcanum/framework/runtime/README.md
  - arcanum/framework/runtime/adapters/codex-exec.md
  - arcanum/framework/runtime/adapters/local-skill.md
selectors:
  - '#current-architecture-in-one-sentence'
  - '#execution-paths'
  - '#scattered-or-conflicting-surfaces'
  - '#storage-pattern'
  - '#status-model'
  - '#adapters'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - direct-skill-observation-is-not-uniformly-deterministic
  - storage-default-drift-is-documented
  - skill-aware-observation-bridge-remains-a-recommended-move
  - codex-exec-is-legacy-explicit-not-the-runtime-model
---

# Arcanum framework runtime and observability boundary

The durable runtime is a generic handoff-and-evidence substrate. Orchestrators own workflow meaning; `tools/arcanum` owns command resolution, adapter selection, requested output capture, and optional durable envelopes; adapters own runtime-specific translation and outcome classification. Terminal statuses are `passed`, `flagged`, `blocked`, and `failed` with contract, adapter-safety, or execution validation grades.

`local-skill` is the default native-agent handoff/receipt contract and must not spawn a nested model-backed CLI. `codex-exec` is an explicit legacy adapter: Codex does not own Arcanum runtime semantics, and isolated Codex state is opt-in.

Observability separates capability telemetry from hook operations. The central append-only invocation ledger is the signal source of truth; per-sigil and per-capability surfaces are rebuildable indexes. Long work uses observed-run bundles with checkpoints and closed or partial observation. Hook operation rows carry `observe: false` and must not recursively trigger observation.

## Live discrepancy preserved by the source

The architecture overview documents that direct native skill invocation is not observed as uniformly or deterministically as legacy wrapper paths, that storage defaults have drifted across documents and installed behavior, and that a skill-aware observation bridge remains recommended work. This Inventory entry preserves those tensions; it does not claim they are resolved.

## Privacy and authority boundary

Telemetry must exclude secrets and mark missing evidence as not checked. Observability evidence supports reflection and maintenance; it does not rewrite the underlying run verdict, promote a capability, or prove production behavior.
