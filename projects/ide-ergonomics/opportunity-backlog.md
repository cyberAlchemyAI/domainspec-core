---
tags: [ide, ergonomics, backlog, intake, candidate]
node_type: backlog
is_session: false
layer: workflow
nature: queue
status: active
created: 2026-06-24
---

# Ergonomic Opportunity Backlog

Append-only capture queue. To add one, see
[OPPORTUNITY-INTAKE.md](OPPORTUNITY-INTAKE.md) (copy the template, fill five fields,
append under `## Captured`). Everything here is **candidate-only** — captured, not
promoted. Status flow: `captured → triaged → in-lifecycle → admitted | dropped`.

## Status legend

| status | meaning |
| --- | --- |
| `captured` | just dropped here; not yet triaged |
| `triaged` | priority set + owner confirmed (or dropped with reason) |
| `in-lifecycle` | the `ide-assisted-arcanum-routing` spell is running it |
| `admitted` | owner-gated through the coordinate-admission / decision gate |
| `dropped` | rejected — keep the reason as residue |

## Captured

### OPP-001 Easy opportunity intake (this on-ramp)
- friction: good ergonomic ideas evaporate because there is no cheap, governed place to drop them.
- coordinate: session-state
- first-owner: PRODUCT-VIEW.md owner
- priority-guess: P1
- status: in-lifecycle
- captured: 2026-06-24
- notes: built 2026-06-24 (OPPORTUNITY-INTAKE.md + this backlog). Meta: the intake is itself an ergonomic affordance.

### OPP-002 Admission-gate runner for NEW:? coordinates
- friction: a captured `NEW:?` coordinate has no easy way to be run through the irreducibility admission gate, so candidate coordinates stall.
- coordinate: NEW:? (model-governance)
- first-owner: PRODUCT-VIEW.md owner / governance review
- priority-guess: P1
- status: captured
- captured: 2026-06-24
- notes: governed by `provisional-model-stewardship` (cyberAlchemy-v2). The runner produces an irreducibility-proof package; it never owns/admits the gate itself.

### OPP-003 Schema-verify the dispatch-grammar mapping
- friction: the routing-grammar coordinate mapping was never checked against dispatch.schema.yml, so it may lag the real enum (carried residue from the spine-model review).
- coordinate: routing-grammar
- first-owner: dispatch-spec
- priority-guess: P2
- status: captured
- captured: 2026-06-24
- notes: discharges GAP-COORD-RESIDUE in the Craft ledger.

### OPP-004 Run input-side + social through the admission gate
- friction: two candidate coordinates (input-side, social) are stuck pending the irreducibility gate, so primitives that resist the three original axes have no confirmed home.
- coordinate: input-side / social
- first-owner: PRODUCT-VIEW.md owner
- priority-guess: P1
- status: captured
- captured: 2026-06-24
- notes: input-side home = intent-latitude-tags/; social home = teammate-handoff-memos/. Both flagged `resists grammar, by analogy only` in the model.

### OPP-005 Render agent choice-routing as multi-select with comments
- friction: when the agent ends a message offering A-or-B as prose, the user must retype the choice; any bounded choice the agent offers should render as a structured multi-select where the user picks one or several options and adds per-option comments.
- coordinate: routing-grammar (the bounded route-menu primitive applied to the agent's OWN choice-offers; touches input-side — user selection + comment)
- first-owner: dispatch-spec (route-menu owner) / IDE Ergonomics host surface
- priority-guess: P1
- status: captured
- captured: 2026-06-24
- notes: user-requested 2026-06-24; "this type of routing should always be a select-multiple-with-comments." Demonstrated immediately in the same message (the part-3 choice below is rendered as a multi-select). The agent's prose A-or-B is itself an ergonomic anti-pattern — it pushes a bounded menu back onto the user's keyboard.

## Triaged

_(none yet — triage moves a captured item here with confirmed priority + owner, or drops it with a reason)_
