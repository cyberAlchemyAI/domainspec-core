# Plan Distill Validation

Mode: Validate
Role path: local Balancer-led critique with Proposer reconciliation; no
subagents authorized
Verdict: pass
Evidence emission: not configured; artifact verdict is independent

## Objective and Output

- Objective: validate the OEW implementation layering, split work pack, 20 SWUs,
  execution route, and gap ledger.
- Output: a smallest-unit, atomicity, recomposition, hidden-gap, and navigation
  verdict before mutation-capable handoff.
- Optimization target: smallest reversible trust-building first step while
  retaining a path to the full interface.

## Balancer Review

### Objection 1 — The first unit could smuggle the adapter

Category: first-unit narrowness.

The interface cannot be trusted until input admission exists. SWU-OEW-001 owns
only path containment, the existing independent verifier, and a verified handle.
It writes no presentation/view output.

Reconciliation: pass. Keep SWU-001 as the sole recommendation.

### Objection 2 — Node and edge projection could be one convenient adapter task

Category: independent acceptance.

Node totality/identity and relation semantics/policy loss have different
falsifiers. They are SWU-002 and 003. Immutable writer/receipt/determinism is
separate SWU-004.

Reconciliation: pass.

### Objection 3 — Native viewer serving and the custom workbench could be one UI

Category: premature complexity.

The L0 decision is upstream compatibility with a generalized projection. L1
decides whether the OEW-specific trust/evidence UI works. Combining them would
hide whether failure belongs to the adapter/upstream or custom interface.

Reconciliation: pass.

### Objection 4 — The workbench task contains seven UI regions

Category: task-shaped SWU risk.

The task is only a grouping. SWUs 007–013 each own one independently reviewable
behavior: load/store, trust rail, inspector, view parity, navigation, tour, and
responsive composition. Browser/a11y closure is SWU-014.

Reconciliation: pass.

### Objection 5 — Code analysis and admission could be conflated

Category: external-effect boundary.

SWU-015's primary behavior is admission of one human-approved scoped output.
The model/provider analysis action is an explicit gated input action and cannot
start without G-OEW-L2-SCOPE. Mapping and rendering remain 016/017.

Reconciliation: pass with stable gate. If a future runtime treats graph
generation as an owned repeatable product behavior, re-plan it as its own SWU.

### Objection 6 — L3 could claim release readiness

Category: evidence ceiling.

Upgrade compatibility, performance, and local packaging are separate SWUs.
TASK-OEW-VERIFY explicitly cannot grant public release, production, ontology
admission, or manual UX pass.

Reconciliation: pass.

## SWU Atomicity Result

- SWU count: 20
- Task-shaped SWUs: 0
- Missing split analyses: 0
- Missing target inventories: 0
- Missing validation commands: 0
- Missing closeout/owner receipts: 0
- Closure-only exemption: 1 (`TASK-OEW-VERIFY`), allowed
- First-unit narrowness: pass

## Recomposition Proof

```text
001 verified source handle
  -> 002 node projection
  -> 003 exact relation/sidecar mapping
  -> 004 deterministic adapter run
  -> 005 immutable upstream artifact
  -> 006 native-viewer proof
  -> 007–013 trust-aware workbench semantics
  -> 014 automated browser/a11y receipt
  -> optional 015–017 scoped code context
  -> 018–020 update/measure/package
  -> terminal audit
```

Each step consumes named predecessor receipts. L0 outputs remain valid without
L1. L1 remains valid without L2. L3 preserves prior guarantees.

## Hidden Gap Review

| Gap | Acceptance critical now? | Owner/path |
| --- | --- | --- |
| upstream network/build permission | only for SWU-005 | exact Task Session approval; block before fetch |
| L2 provider/private scope | only for SWU-015 | G-OEW-L2-SCOPE |
| named manual screen-reader/usability runners | not for automated L1; required for manual/overall pass | TASK-OEW-VERIFY |
| future IOLM adoption | no | separate IOLM owner/new design |
| upstream extension API changes | no at current pin | SWU-018/new Design if contract changes |

No hidden acceptance-critical Plan gap remains.

## Deferred Complexity

- whole-repository analysis;
- automatic evidence-code inference;
- cross-run or collaborative server state;
- automatic upstream pin updates;
- IOLM/Craft/authority integration;
- public release and production.

## Premortem

Likely failure: a visually polished generalized edge is mistaken for exact
source semantics.

Guardrail: source admission precedes mapping; exact sidecar mapping is blocking;
inspector displays exact relation and loss; three-view parity and Poker
acceptance verify it; receipts retain `authority_effect:none`.

## Frame Expiry

Re-run Define/Design/Plan if the candidate run version changes, authority effect
changes, upstream exposes a materially different extension/data contract, the
delivery scope includes IOLM/public release, or multi-user state becomes
required.

## Navigation Guide

Start only at `SWU-OEW-001` after explicit selection. Use
`work-pack/swu-manifest.json` for machine routing and the parent task for
implementation detail. Stop after each Task Session receipt.

## Telemetry

Not configured for this child validation. No child telemetry row is claimed;
the missing telemetry does not alter the pass verdict or authorize mutation.

## Next Route

Deferred. Ask for explicit `SWU-OEW-001` selection, then run Task Session
preflight.

## Open Questions

See [../define/SPEC.md](../define/SPEC.md#open-questions).
