# Decision Gate: one-shot admission prototype execution route

Status: PASS

Selected route: **A — Candidate-local prototype fast lane**

Decision evidence: the user explicitly selected `A` after the trade-off was
presented. The selection authorizes only the bounded candidate-local work pack;
normal governed admission and lifecycle closeout remain deferred.

## Why normal governed execution remains blocked

The accepted research is not yet a mutation-ready Invoke Plan. The current
Work Pack Readiness Audit cannot authorize Task Session, and Task Session Until
Blocker lacks a production chain runner, approved-epoch consumer, durable
cursor contract, and semantic closeout `NO_OP` proof. A fully governed repair
also expands into upstream Invoke, Structured Interview, and Decision Gate
receipt contracts that were outside the bounded two-spell prototype scope.

Consequential mutation under the normal governed route still requires upstream
repair. Candidate-local prototype mutation may proceed under the selected route.

## Options

### A — Candidate-local prototype fast lane (recommended)

- Benefit: implements and browser/fixture-tests the smallest working WPRA plus
  chain prototype without another per-SWU governance loop.
- Cost/risk: lifecycle synchronization, upstream receipt hardening, registry,
  promotion, publication, and release remain deferred to a Handoff Notice.
- Reversibility: high; local candidate files only, no commit, push, promotion,
  deployment, network integration, or product mutation.
- Downstream: one finite candidate-local Work Pack; required validation is
  still run in full.

### B — Full governed capability migration

- Benefit: closes the complete authority and receipt chain before mutation.
- Cost/risk: expands the objective across Invoke Define/Design/Plan,
  Structured Interview, Decision Gate, WPRA, Task Session Until Blocker,
  Continuation Router, and Refresh; this is not the bounded two-spell work pack.
- Reversibility: local changes are reversible, but the design surface and
  validation burden are substantially larger.
- Downstream: first perform a new Spellcraft design and owner-surface freeze,
  then author and execute a larger work pack.

### C — Defer

Preserve the research and current passing legacy harnesses; make no
implementation changes.

### D — Stop

Close this objective without further planning or implementation.

## Standing non-answer

`Explain / more context` expands the evidence and trade-offs but does not
resolve the gate.

## Recommendation

Choose **A** if the immediate objective is a working local prototype. It is the
only route that matches the repeated request to stop cycling while preserving
validation and keeping governance deferral explicit rather than pretending it
was completed.
