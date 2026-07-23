---
tags: [inventory, strategy-result, dispatch, subagents, review-change-request, audit, observability, capability, claim-le-proof]
node_type: findings
is_session: false
layer: workflow
nature: reference
status: verified
created: 2026-07-23
sources: [ops/development/2026-07-22-most-used-skills-efficiency-review/attacks.md, ops/development/2026-07-22-most-used-skills-efficiency-review/findings.md, .arcanum/observability/reflections/20260723T005559Z-most-used-skills-efficiency-review.md]
---

# Most-Used Skills Efficiency Review

- ID: `most-used-skills-efficiency-review-strategy-result`
- Type: synthesis
- Status: verified
- Confidence: high

## Result

A confirmed four-agent review audited the six most frequently observed named
skills separately: Task Session, Invoke, DomainSpec Subagents Strategy,
Decision Gate, Inventory, and Whisper. Two opposed attackers confronted one
another, a synthesizer reconciled the evidence, and an adversarial verifier
accepted ten bounded change requests after one revision cycle.

The accepted direction replaces ceremony with earlier falsifiable boundaries:
machine-enforced dispatch admission, acceptance-critical Task Session blocking,
material-package validation before mutation handoff, typed Decision Gate
overrides, a conformant Inventory machine view, and generated runtime assembly
from canonical bases plus declared overlays. It retains controls with concrete
authority, mutation, publication, destructive-action, or false-readiness
witnesses.

## Scope And Boundary

The result is a prioritized maintenance queue, not a combined patch. No audited
skill, public Arcanum source, runtime mirror, appender, validator, or application
code was modified by the review. Each change request requires its own bounded
maintenance task and negative controls.

Inventory remains a non-authoritative read model. This entry points to the
durable attacks, verified findings, and Workflow Reflect report; it does not
promote their proposals or authorize implementation.

## Current Validation Residue

The review directly confirmed that `.arcanum/inventory/index.json` is parseable
but fails its current kind validator because 15 existing records use kinds
outside the validator enum. This entry therefore uses the supported `entry`
kind, while the package-level validation failure remains visible until INT-1 is
implemented.

## Next Action

Start with DSS-1 as one maintenance task: make registration reject new RESERVED
dispatch types, orphan closes, working-agent self-approval, and destination
escape while grandfathering historical rows and preserving duplicate-close
idempotence. Continue one accepted change request at a time only after its own
negative controls pass.
