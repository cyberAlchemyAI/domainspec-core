---
tags: [inventory, strategy-result, dispatch, subagents, research, ddd, event-sourcing, process-manager, uniqueness, claim-le-proof, idempotency]
node_type: synthesis
is_session: false
layer: research
nature: reference
status: candidate
created: 2026-06-30
dispatch_id: 2026-06-30-ddd-process-manager-uniqueness
dispatch_type: research
working_folder: research/ddd-event-sourcing/2026-06-30-process-manager-uniqueness/
sources: [research/ddd-event-sourcing/2026-06-30-process-manager-uniqueness/research.md, research/ddd-event-sourcing/2026-06-30-process-manager-uniqueness/findings.md, telemetry/agents/subagents-dispatch.yaml]
---

# DDD Process Manager Email Uniqueness Strategy Result

This is a non-authority Inventory read model for the governed research dispatch
`2026-06-30-ddd-process-manager-uniqueness`. It records the strategy result and
points to the durable research artifacts. It does not promote a DDD definition,
event-sourcing implementation, privacy policy, or uniqueness rule by itself.

## Strategy Summary

**P1 trigger decision:** dispatch was justified by synthesis, context
protection, isolation, and parallelism. The question combined DDD/process-manager
lineage, Vaughn Vernon aggregate-boundary guidance, event-store persistence
mechanics, and mutable-email policy/operations.

**Lanes / groups:**

- `explorers` ran in parallel with a composite `source-corpus + methodology`
  anti-bias axis.
- `synthesizer` reconciled explorer returns into a candidate synthesis.
- `reviewers` evaluated the synthesis through precedent, non-vacuity, and
  definitional-soundness gates, then converged via robot-talk.
- `writer` produced `findings.md` only.
- `auditor` evaluated `findings.md` and accepted without revision.

**Subagents and angles:**

- `Hewitt, Carl` — historical/process-flow corpus over Greg Young, CQRS
  Journey, process-manager vs saga lineage, and workflow coordination.
- `Simon, Herbert` — Vaughn Vernon and aggregate-design corpus over consistency
  boundaries, bounded contexts, and cross-aggregate uniqueness.
- `Turing, Alan` — event-store/mechanism corpus over stream identity,
  expected-revision or no-stream preconditions, projections, unique indexes,
  command-side lookup, and idempotency.
- `Meadows, Donella H.` — business-policy and operations methodology over
  mutable email, verification, release/tombstone policy, normalization, privacy,
  compensation, and UX failure modes.
- `Noether, Emmy` — synthesizer.
- `Rittel, Horst` — precedent skeptic.
- `Popper, Karl` — non-vacuity skeptic.
- `Quine, Willard Van Orman` — definitional-soundness skeptic.
- `Shannon, Claude` — writer.
- `Brandenburg, Martin` — auditor and final approver.

**Dependency flow:** explorers -> synthesizer -> reviewers -> writer -> auditor.
The sheet included synthesizer<->reviewers zig-zag (`loop_cap: 2`),
synthesizer->explorers feedback (`loop_cap: 1`), and auditor->writer feedback
(`loop_cap: 1`). Reviewers required concrete repairs before acceptance; no
auditor revision was required.

**Gate / ledger state:** the check-tension gate returned double PASS before
human confirmation. The human confirmed. The dispatch row and close row are
appended to `telemetry/agents/subagents-dispatch.yaml`; close state is
`exit_reason: resolved` with `loops_used: 1`. The close row records reviewer
feedback requiring precedent labels, term boundaries, a write-side collision
contract, concrete create/change races, old-email release semantics,
failure/compensation handling, a falsifiable invariant, and projection,
idempotency, normalization, and process-manager boundary corrections.

## Result

The auditor-accepted finding is conservative: a process manager or saga
implementation orchestrates registration and mutable-email workflows, but it
does not prove uniqueness. Hard uniqueness belongs to a write-side consistency
boundary or constraint that serializes all contenders for the same normalized
key.

The recommended default is stable `UserId`, versioned `EmailKey`, a separate
`EmailClaim` or reservation boundary keyed by
`{scope}:{normalizationPolicyVersion}:{normalizedEmail}`, and a process manager
that coordinates create/change/verify/release/expire workflows. The decisive
mechanism is same-key serialization, an event-store precondition, an inline
unique index, or an external unique reservation/claim table.

## Source Refs

- `research/ddd-event-sourcing/2026-06-30-process-manager-uniqueness/research.md`
  — explorer transcript.
- `research/ddd-event-sourcing/2026-06-30-process-manager-uniqueness/findings.md`
  — auditor-accepted synthesis, technique taxonomy, race walkthroughs, and
  implementation sketch.
- `telemetry/agents/subagents-dispatch.yaml` — dispatch and close rows.

## Downstream Use

Use this entry when designing identity/account email-change workflows,
event-sourced uniqueness constraints, process-manager boundaries, or
DDD/event-sourcing teaching material. Treat the result as evidence-backed
guidance, not a universal implementation mandate: the findings require the
local domain to choose uniqueness scope, normalization policy, release/tombstone
semantics, privacy retention, and the actual transactional primitive.

## Residue

- No code, schema, event-store configuration, or database constraint was
  implemented.
- Privacy/legal policy for tombstones and old-email retention remains
  domain-specific.
- Event store capabilities must be verified against the deployed product and
  version before choosing multi-stream append, preconditions, or inline
  projection mechanics.
