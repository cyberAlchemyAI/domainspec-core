---
id: subagent-research-context-footprint-research-result-synthesis
kind: entry
type: synthesis
title: Subagent research context-footprint closed result
updated: 2026-09-01
status: candidate
confidence: high
dispatch_id: 2026-09-01-subagent-research-context-footprint
dispatch_type: research
working_folder: cyberAlchemy-v2/development/research/2026-09-01-subagent-research-context-footprint/
tags:
  - inventory
  - strategy-result
  - dispatch
  - subagents
  - research
  - long-context
  - operational-evidence
  - claim-le-proof
sources:
  - cyberAlchemy-v2/development/research/2026-09-01-subagent-research-context-footprint/dispatch-sheet.json
  - cyberAlchemy-v2/development/research/2026-09-01-subagent-research-context-footprint/research.md
  - cyberAlchemy-v2/development/research/2026-09-01-subagent-research-context-footprint/findings.md
  - cyberAlchemy-v2/development/research/2026-09-01-subagent-research-context-footprint/evidence-closure.json
  - cyberAlchemy-v2/development/research/2026-09-01-subagent-research-context-footprint/runtime-usage-report.json
  - cyberAlchemy-v2/development/research/2026-09-01-subagent-research-context-footprint/final-approval.json
selectors:
  - '#direct-result'
  - '#observed-runtime-footprint'
  - '#h200-qwen-hypothesis'
  - '#verdicts-and-residue'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - five-minute-completion-not-achieved-this-run
  - maximum-useful-fanout-unmeasured
  - luna-sol-quality-parity-unproven
  - h200-qwen-live-trace-absent
  - runtime-token-category-attribution-incomplete
---

# Subagent research context-footprint closed result

This is a non-authority Inventory read model of one closed research dispatch.
It preserves observed host usage and bounded serving hypotheses; it does not
admit an optimization, quality-parity, H200-throughput, provisioning,
deployment, publication, or product claim.

## Direct result

The confirmed nine-agent dispatch closed `resolved` after one synthesizer
zig-zag repair and one auditor-to-writer revision. The final Sol auditor
returned `ACCEPT`, and the parent accepted findings SHA-256
`994bc04e43b0cdc51149e21f320b625ea62d2243fd0fa3b28d2673fcd4439faf`.

The topology schedules nine logical roles in five dependency waves and uses at
most three concurrent child instances. Three is a physical host ceiling, not a
measured maximum useful fan-out.

## Observed runtime footprint

Across the nine registered execution-agent sessions, native receipts report:

- 6,116,802 input tokens;
- 5,622,784 cached input tokens (91.9% of input);
- 494,018 uncached input tokens;
- 62,338 output tokens, including 31,486 reasoning-output tokens as a
  subdivision rather than an additional total;
- 6,179,140 aggregate provider-accounted total tokens; and
- a 23.51-minute first-explorer-to-final-auditor wall window.

These totals sum repeated context across every call in multi-call sessions.
They are aggregate processing, not peak single-call context. They exclude the
parent, the two preconfirmation tension agents, and the parent's post-agent web
verification.

The static sheet contains 5,539 persisted prompt characters, 14,600 declared
output targets, 18,200 base declared handoff tokens, and 33,800 declared
handoff tokens when every optional edge traverses once. The gap between static
payload arithmetic and actual aggregate receipts is expected: fixed runtime
context, tool schemas, retrievals, repeated calls, caching, and feedback are
not represented by the sheet's prompt text or output targets.

## H200 Qwen hypothesis

Qwen3.8-27B-FP8 is a 27B multimodal model with a 30.9-GB artifact tree and
native 262,144-token context. H200 supplies 141 GB HBM3e. Conditional arithmetic
with unmeasured loaded weights and runtime reserve yields memory-only bounds of
roughly four to five BF16-KV or eight to ten FP8-KV full-context requests.
Those bounds are not safe concurrency, throughput, latency, or quality proof.
The maximum-independent-replica recommendation is KILL; one shared-weight
engine is only the stronger long-context hypothesis.

## Verdicts and residue

- Context accounting: candidate build-from-owned instrument.
- Nine-agent Luna route: candidate under test, not optimized.
- Direct control: Luna/`fork_turns:none` versus Sol/`fork_turns:none`.
- Five-minute result: not achieved by this run; retain 300 seconds only as a
  hard-stop instrumentation cell until a frozen experiment contract exists.
- Luna quality parity: deferred and unknown.
- H200 serving: conditional capacity hypothesis only; live trace absent.

The next bounded step is a separate frozen experiment/propose contract with
byte-identical Luna/Sol cells, section-level token receipts, per-call timing,
hard 300-second stops, blind scoring, a quality non-inferiority margin, and
explicit failure rules.
