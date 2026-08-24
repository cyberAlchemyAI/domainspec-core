# RWO–Eve research runtime repair dispatch proposal

Dispatch ID: `2026-08-13-rwo-eve-research-runtime-repair-002`

## P1 trigger decision

Dispatch is warranted by synthesis, isolation, and independent checking. One exact
closed corpus must be repaired without reopening exploration, and the repaired
contract must survive two different skeptical attack vectors before any durable
findings can be written. Five named seats keep synthesis, review, writing, and audit
separate while the parent retains both evidence closure and final approval.

## Objective and evidence boundary

The dispatch repairs only six defects preserved by the closed recovery-001 run:

1. canonical command payload bytes and reproducible identity preimages;
2. exact per-action input manifests, digests, mutation/write/forbidden scopes,
   outputs, and owners;
3. separate discriminating crash cut-point controls;
4. distinct missing-approval and denied-approval controls proving zero tool use;
5. a defined `A-SINGLE-SCHEDULER-01` assertion bound to the RWO ablation; and
6. a distinct parent `FinalApprovalV1` after `AuditAcceptanceV1`.

`SOURCE-BINDING.json` freezes the original completed exploration and the closed
recovery-001 synthesis/review/closeout corpus by exact path, SHA-256, and byte size.
No new source search, browsing, or exploration is allowed. The selected topology is
preserved: DomainSpec and humans own strategy and authority; RWO owns semantic
scheduling and admission; a future durable Go coordinator owns physical
coordination; Eve remains one bounded leaf executor.

All outputs are private, candidate research artifacts. This proposal grants no
implementation, product mutation, Eve installation or execution, credentials,
authority or promotion, ontology or lifecycle synchronization, publication,
deployment, commit, push, or external effect.

## Lanes, groups, and subagents

- `repair-synthesizer` — Ashby, W. Ross; synthesizer; read-only. Produces one
  replacement contract/fixture synthesis that addresses exactly the six defects
  and preserves every prior PASS and claim ceiling.
- `repair-reviewers` — Popper, Karl and Wittgenstein, Ludwig; two independent
  skeptics in parallel on the attack-vector axis.
  - Popper attempts literal reproduction and falsifies non-vacuity, manifests,
    crash classification, approval denial, and the single-scheduler assertion.
  - Wittgenstein attacks definitional collapse, owner substitution, and any attempt
    to let audit acceptance substitute for parent final approval.
  - Predicted disagreement: literal precision may satisfy Popper while still hiding
    an authority transfer caught by Wittgenstein; strict owner separation may
    satisfy Wittgenstein while remaining operationally non-reproducible to Popper.
- Parent evidence closure — no subagent seat. The parent checks the exact synthesis
  and fresh PASS/PASS reviews against the `exact-binding` research contract before
  the writer becomes eligible.
- `repair-writer` — Eilenberg, Samuel; writer; the only mutating seat, limited to
  `recovery-002/findings.md` after evidence closure.
- `repair-auditor` — Bourbaki, Nicolas; auditor; read-only. Returns
  `AuditAcceptanceV1` or one bounded writer revision; cannot issue parent approval.

## Dependency flow

`synthesizer → reviewers` is a zig-zag with `loop_cap: 1`. Both reviewers must
return fresh PASS before parent exact-binding evidence closure can return `ready`.
Closure then unlocks the writer. `writer → auditor` is sequential, and
`auditor → writer` is a feedback edge with `loop_cap: 1`. After an auditor ACCEPT,
the parent must separately issue `FinalApprovalV1`; only then can closeout be
eligible. The dispatch-wide `max_loops` is `1`.

## Inventory preflight

The machine index is lookup-ready and parseable, with partial source coverage. Four
non-authority entries were selected:

- the prior RWO/ARE research strategy;
- its auditor-accepted current-state result;
- the orchestrator purpose/classification result; and
- the agent reasoning-engine contract result.

They preserve the current/proposed boundary, strict owner separation, finite-witness
need, and non-promotion ceiling. Broad adjacent architecture and unrelated recursive
workflow results were excluded because they do not address the six exact defects and
would broaden the frozen corpus. Concrete lane effect: synthesis is constrained to
the existing four-layer topology; Popper receives reproducibility gaps;
Wittgenstein receives ownership/authority gaps; writer and auditor receive the
non-authority and claim-ceiling obligations. Inventory is not proof or authority.

## Gate and ledger state

- Schema: `0.8.0`
- Sheet SHA-256: `874230c1650920df5bdf84e8d44f652a83d8be936d0fa1511d939a980f941e2b`
- Material-strategy SHA-256:
  `78144e8ae884033fa42b7d1ce2dc6ba862764edca17a2301de68da0de32c00aa`
- Registrar form validation: PASS, non-mutating
- Dispatch Spec validation: PASS
- Tension checker: PASS; receipt SHA-256
  `7606a6eb8f719dd679099d147d61944e431e9775a0c5c952c41a6bcd61738d2d`
- Independent tension reviewer: PASS; receipt SHA-256
  `73b24616d5eac0bbf8c3c0b5cd76c14c29407f67ad74645a174ebfa6627abd03`
- Human confirmation: pending
- Authorization: `requires_user_permission`
- Registration: unregistered; ledger unchanged
- Execution/closeout: not started; no agents spawned

The publication/privacy/effect guardrail is fail-closed. Any source-binding drift,
non-PASS reviewer receipt, unresolved exact-binding row, exceeded loop, scope breach,
or attempt to infer final approval blocks downstream work.

## Required response shape for the eventual run

Each seat returns a structured receipt containing dispatch, step, wave, role and
agent identities; spawn/join/close state; capability target and mode; effective
write scope; exact input/output artifact bindings; validation; blockers; residue;
reroute; effect report; and claim ceiling. The parent returns separate
`EvidenceClosureV1`, `FinalApprovalV1`, and dispatch closeout artifacts. Prose alone,
an auditor ACCEPT, or artifact existence cannot open the next gate.

## Next human action

The form, Dispatch Spec, source-binding, and two independent tension gates all pass
against the exact persisted sheet digest. The user may now explicitly confirm that
exact sheet. Only that confirmation permits registration and launch; this proposal
itself does not.
