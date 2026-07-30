# One-shot admission prototype validation

Status: **PASS — working candidate-local control prototype**

Date: 2026-07-30

## Result

The prototype now connects a deterministic Work Pack Readiness Audit v2
projection to an approved-epoch finite-frontier chain:

1. WPRA freezes exact input and semantic bindings.
2. WPRA emits either one stable blocker code or a no-authority objective
   execution manifest.
3. A separate approval binds the manifest epoch, risk ceiling, and request
   budget.
4. The chain exposes at most one next Task Session selector.
5. One immutable transition joins the Task Session terminal result with an
   owner receipt or semantic `NO_OP` proof.
6. The chain advances, completes, or stops fail-closed without widening the
   frontier or auto-running compensation.

The chain controller does not launch Task Session. That owner boundary is
intentional and is what keeps the prototype from turning derived evidence into
execution authority.

## Acceptance evidence

| Check | Result |
| --- | --- |
| Additive JSON Schema meta-validation | PASS; 6/6 Draft 2020-12 schemas |
| WPRA legacy regression | PASS; 10 tests |
| WPRA v2 projection | PASS; deterministic projection, 10 pre-route fault classes, 5 semantic invalidation classes |
| Chain legacy regression | PASS; 8/8 controller cases |
| Approved-epoch chain | PASS; hash link, exclusive create, epoch, cursor, frontier, risk, budget, successor, `NO_OP`, and compensation |
| Private frozen-input replay | PASS; 19/19 fixtures over 16 exact Body War bindings |
| Protected Body War bytes | PASS; all 3 declared product hashes unchanged |
| Generated package safety | PASS; partial bootstrap guard and unrelated-package sentinel |
| Generated parity | PASS; canonical README, schemas, and runners match Codex and Claude profiles |
| Public/private denylist | PASS |
| Scoped whitespace | PASS |
| Dispatch document | PASS |
| Handoff Notice integrity | PASS; `HN-3EB333B0A9DB` |
| Parent gitlink immutability | PASS; unchanged at `a0dd82cef5eabebd60382526ef6be4377a8db20c` |

## Implemented artifacts

- Public WPRA v2 schemas, deterministic projection/runtime, and synthetic
  regression suite.
- Public chain schemas, append-only controller runtime, semantic `NO_OP`
  validation, and deterministic regression suite.
- Private 19-case frozen-input fixture contract, runner, individual results,
  and aggregate result.
- Selectively generated Codex and Claude packages for only the two named
  spells.
- Nine SWU receipts and one deferred-governance Handoff Notice.

## Claim ceiling

The private replay executes the public control logic against real frozen
inputs, but PBW-01, post-approval drift, and command failure are
fixture-harness simulations. They are not a new real Task Session execution
and they mutate no Body War product bytes.

This report proves a local candidate control prototype. It does not prove:

- normal Work Pack Readiness or Task Session lifecycle synchronization;
- a real one-shot execution of the Body War work pack;
- registry admission, promotion, publication, release, deployment, or
  production readiness;
- Git commit/push or remote visibility.

## Deferred residue

- Handoff Notice `HN-3EB333B0A9DB` remains open for lifecycle reconciliation.
- `make bump-check` is deferred until an authorized public-submodule
  commit/push route exists; the fast lane forbids its network-backed push
  dry-run, and the parent gitlink has not moved.
- The existing Spellcraft experiment profile reports
  `QUALITY_BAR_STATUS=not_checked`; promotion remains the lifecycle owner's
  decision.
- A separate governed run is required to prove real Task Session launch,
  empirical writes, closeout mutation, and continuation joining.

## Final authority

- Evidence ceiling: `frozen-input-contractual-readiness`
- Authority effect: `none`
- Product mutation: `none`
- Promotion: `not authorized`
- Deployment: `not authorized`
