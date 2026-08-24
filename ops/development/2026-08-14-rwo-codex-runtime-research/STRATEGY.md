# RWO and Codex Runtime Migration — Research Strategy

## P1 Trigger Decision

This is a governed `research` dispatch. Synthesis, context protection,
isolation, and parallelism all apply: the answer must reconcile the current RWO
Rust semantic kernel, the dirty candidate-local Go durability layer, all active
Eve coupling, the current official Codex App Server protocol, Arcanum's public
runtime and Task Session owners, and lifecycle/privacy constraints.

The research result will be an architecture and migration Work Pack, not the
migration itself. It will not remove or rename Eve bytes, start App Server,
invoke a model, register an adapter, synchronize lifecycle state, or operate
Git.

## Objective And Evidence Boundary

The dispatch must select the smallest coherent runtime topology for this chain:

```text
admitted Arcanum work
  -> one semantic RWO command
  -> one durable physical attempt
  -> one bounded Codex App Server turn
  -> raw ordered provider evidence
  -> one admitted RWO terminal event
  -> zero or one next RWO command
  -> separately typed Arcanum executor, owner, and closeout receipts
```

The central open question is placement: whether `arcanum/framework/runtime`
envelopes the RWO Go host, whether the RWO Go host implements the public runtime
adapter contract, or whether a narrower private bridge makes one layer a client
of the other. The synthesis must select one or return a typed blocker. Any
topology with two semantic schedulers, durable causal journals, admission
owners, retry authorities, or receipt truths is rejected.

“Remove Eve” is split into two auditable sets:

- active runtime, test, fixture, schema, naming, and current-document bytes that
  may need replacement, generalization, rename, or retirement; and
- historical research, audit, validation, Work-Pack, and provenance evidence
  that remains immutable or is explicitly superseded.

This prevents both a rename-only migration and a destructive rewrite of proof.

## Lanes, Groups, And Subagents

Three explorers run in parallel:

- `Hewitt, Carl` inventories every active and historical Eve occurrence and
  reconstructs reusable versus provider-coupled RWO Rust/Go behavior.
- `van Lamsweerde, Axel` reconstructs current Codex App Server protocol,
  identity, permission, interruption, recovery, terminal, and fixture contracts.
- `Beer, Stafford` resolves RWO-Go-Arcanum placement, authority, receipts,
  lifecycle, observation, Craft/Goal, and public/private boundaries.

`Turing, Alan` selects one topology and builds the migration contract. Three
skeptics then attack it independently:

- `Lakatos, Imre`: duplicate owner and competing runtime precedent;
- `Popper, Karl`: finite success, failure, crash, ambiguity, retry, and replay
  witnesses;
- `Quine, Willard Van Orman`: rename-only replacement, identity and approval
  collapse, historical rewrite, and private/public leakage.

`Ahrens, Sönke` may write only `findings.md` after exact-binding evidence
closure. `Brandenburg, Martin` audits only that file. The parent remains final
approver.

## Dependency Flow

```text
three explorers in parallel
  -> synthesizer
  <-> three skeptics in parallel, bounded to two exchanges
  -> exact-binding evidence closure
  -> writer
  -> auditor
  -> parent closeout
```

One evidence-repair feedback from synthesis to explorers and one
auditor-to-writer revision are available. A missing, partial, mismatched, or
timed-out receipt blocks downstream work.

## Required Research Result

The final findings must contain:

1. current RWO semantic, durable, provider, Arcanum, and lifecycle layer map;
2. complete Eve occurrence denominator with active/historical classification;
3. reusable versus provider-specific RWO component ledger;
4. one selected RWO-Go-Codex-Arcanum topology or typed blocker;
5. provider profile and provider-neutral leaf/host-result contract;
6. complete identity, cursor, receipt, approval, and state namespace matrices;
7. exact RWO command -> Codex thread/turn/item -> RWO accepted-event flow;
8. sandbox, permission, interruption, cancellation, ambiguity, recovery,
   retry, replay, terminal, and closeout rules;
9. public Arcanum/private RWO boundary and generated-package implications;
10. active-byte changed-file candidate inventory and schema/name migration map;
11. deterministic success plus failure/crash/replay fixture and eval matrix;
12. dependency-ordered, non-executed implementation Work Pack;
13. proof labels and explicit residue for every load-bearing claim.

The non-vacuity gate requires one complete success trace and explicit permission,
stale-input, interruption, ambiguous delivery, duplicate, replay mismatch,
invalid terminal, failed closeout, and durability-cut traces.

## Inventory Preflight

The root Inventory passed lookup readiness with zero failures and 153 inherited
uncontrolled-tag warnings. It supplied the repaired RWO-Eve topology, the
audited App Server map, the earlier RWO current-state route, the framework
runtime source map, and the current native Orchestrate execution precedent.

The nested RWO Inventory contains zero entries, so it cannot establish RWO
coverage. This changed the strategy materially: direct current RWO source is
mandatory, the first explorer owns an exact occurrence denominator, dirty and
untracked bytes must be preserved, and Inventory absence cannot be interpreted
as source absence. Inventory remains a non-authority discovery view.

## Gate And Ledger State

- Dispatch type: `research`, LIVE
- Sheet schema: `0.8.0`
- Candidate sheet: `dispatch-sheet.json`, no `evidence_binding`
- Sheet SHA-256:
  `73e0413a1a6bf877f3b0887d4619671f94199ecd5af59317c08b41ef1a445f74`
- Material-strategy SHA-256:
  `46a728d0749a7cbeb0d71193ec86f7fdbe445d3a00a41feaebf7d5a6ef701518`
- Confirmation readiness: `PASS`
- Capability-bound Dispatch Spec: `PASS`
- Route SHA-256:
  `5bb2c3c031185a14c8639e13ac694a5023496f6480c06e9597b301641b5617a7`
- Independent tension checker: `PASS`, Tests 1-5
- Independent tension reviewer: `PASS`, Tests 1-5
- Human confirmation: pending
- Authorization: `requires_user_permission`
- Registration: none
- Research agents spawned: zero
- Dispatch ledger mutation: none
- Eve removal, Codex execution, and implementation: none

## Claim And Authority Boundary

The current Go candidate proves local durability and failure behavior against a
real RWO Rust child and an in-process fake Eve-shaped leaf. It does not prove
Codex compatibility. The local App Server fixture proves deterministic
translation of one synthetic successful trace only. The audited integration map
is architecture evidence, not a live adapter witness.

RWO retains semantic command and accepted-event authority. Any future Go host
owns only physical durability and delivery. Codex App Server can own only its
process/thread/turn/item/request state. Task Session, capability owners,
Orchestrate, Craft, Goal, eval, observation, and lifecycle owners retain their
separate authority. Public Arcanum remains provider-neutral; private RWO terms
stay out of public sources.

## Next Human Action

Reply exactly `confirmed` to authorize one append-only dispatch registration and
execution of this nine-agent read-only research pipeline. Any material change
requires the revised strategy to return through readiness, independent tension,
and confirmation.
