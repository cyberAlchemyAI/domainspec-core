# RWO-managed eve research runtime strategy

Status: `confirmation-ready — sheet, route, and double tension pass`

This package answers a narrow question: can the Recursive Work Orchestrator
manage a governed DomainSpec research strategy while
[eve](https://eve.dev/docs/agent-config) runs the bounded agent work?

The likely answer is **yes, but not by treating eve as RWO and not through
`agent.ts` alone**. The research must establish the exact seam before any
runtime implementation is authorized.

## P1 trigger decision

All four governed-research triggers fire:

- **Synthesis:** the answer must reconcile an external beta framework, the
  current Rust/Go RWO prototype, and DomainSpec dispatch governance.
- **Context protection:** raw framework, compiler, reducer, delivery, failure,
  and approval details would overwhelm one parent context.
- **Isolation:** eve behavior, RWO semantics, and security/recovery claims need
  different source corpora and methods.
- **Parallelism:** those three evidence lanes can run independently before one
  bounded synthesis.

The task therefore merits a governed research dispatch rather than an inline
architecture guess.

## Starting architecture hypothesis

The dispatch will test, not assume, this four-part split:

```text
DomainSpec strategy
  owns roles, dependencies, confirmation, registration, evidence closure
        |
        v
RWO compiler + reducer
  owns deterministic graph state and zero-or-one next CommandIntent
        |
        v
delivery coordinator / eve adapter
  owns durable attempt, dedupe, cancellation, and result normalization
        |
        v
eve agent host
  owns bounded sessions, model turns, declared agents, tools, and tool approval
```

eve's official current model is filesystem-first. `agent.ts` selects model,
reasoning, compaction, limits, output schema, and optional workflow backing.
Specialist identities and surfaces live in folders such as
`agent/subagents/<id>/`, with their own prompts and tools. The research must
determine the exact programmatic task-mode API and whether fixed declared
agents can serve as leaf executors while eve's own built-in `agent` and
experimental `Workflow` scheduling stay disabled or outside the control path.

The current RWO prototype cannot yet perform this job end to end. It has a real
Rust semantic child and a volatile Go cursor/outbox coordinator, but no durable
journal, recovery, retry scheduling, command delivery, or eve adapter. Those
are implementation gaps, not paperwork gaps.

## Bootstrap rule

This research dispatch, if confirmed, runs through the repository's current
native Codex subagent route. It does **not** claim to run through the unbuilt
RWO-to-eve bridge it is researching. The accepted findings may later feed an
Invoke/Work-Pack route that builds and tests that bridge.

## Lanes, groups, and subagents

### Exploration wave — three read-only agents in parallel

- **Turing, Alan — eve runtime explorer.** Pins the official eve configuration,
  declared-subagent, session, task-mode, approval, cancellation, and invocation
  contracts and proposes the smallest filesystem topology.
- **Hewitt, Carl — RWO control explorer.** Compiles the DomainSpec research
  lifecycle conceptually into RWO states, accepted events, cursor facts, and
  command intents while preserving human and DomainSpec ownership.
- **Simon, Herbert — failure and authority explorer.** Attacks duplicate
  delivery, timeout, cancellation, partial fanout, stale confirmation, retries,
  persistence, secrets, egress, overlapping writes, crash recovery, and dual
  scheduler topologies.

### Synthesis wave

- **Shannon, Claude** selects or kills topologies, specifies the event/command
  seam, maps the eve app layout, defines the finite witness, and produces the
  implementation-ready Work-Pack skeleton.

### Review wave — two read-only agents in parallel

- **Popper, Karl** forces the architecture through a discriminating local
  positive and negative witness.
- **Quine, Willard Van Orman** prevents DomainSpec, RWO, Go, eve, the model, the
  human, approval, persistence, retry, and evidence owners from collapsing.

### Persistence and audit

- **van Lamsweerde, Axel** may write only `findings.md` after exact evidence
  closure.
- **Brandenburg, Martin** audits that file and may request one bounded writer
  repair. The parent remains final approver.

## Dependency flow

```text
three explorers in parallel
  -> synthesizer
  <-> two reviewers in parallel, one bounded repair loop
  -> exact-binding evidence closure
  -> findings writer
  -> auditor
  -> parent
```

Missing, partial, mismatched, timed-out, or unclosed receipts block the next
wave. Reviewer feedback cannot silently broaden the confirmed strategy.

## Required research result

The final findings must provide all of the following:

1. a selected topology and explicit killed alternatives;
2. a responsibility map for DomainSpec, RWO/Rust, Go delivery coordination,
   eve, models, tools, and humans;
3. dispatch-sheet-to-RWO compilation rules;
4. versioned launch/progress/completion/block/cancel/unknown event and command
   projections;
5. identity, dedupe, retry, replay, cancellation, and crash-recovery rules;
6. the exact eve filesystem and `agent.ts`/subagent configuration topology;
7. a finite two-explorer fixture with positive and negative controls;
8. a sequenced implementation Work Pack with exact owners, inputs, write
   boundaries, tests, and claim ceilings;
9. explicit missing decisions and evidence.

## Inventory preflight

The root machine Inventory is lookup-ready with zero failures and 153 inherited
uncontrolled-tag warnings. It contributes prior RWO/ARE, Arcanum building
system, runtime-separation, and adapter precedents as discovery leads.

The nested `cyberalchemy-orchestrator` Inventory is empty and validation-blocked.
No Inventory entry covers eve. Consequently:

- current RWO claims bind directly to the local report and source hashes;
- eve claims bind to the official repository commit and source snapshot;
- no result may be called precedent-clean merely because Inventory found no
  match;
- the explorers must re-open primary sources for every load-bearing claim.

## Gate and ledger state

- Candidate sheet schema: `0.8.0`
- Candidate sheet validation: `PASS`
- Candidate sheet SHA-256:
  `83732aff0172411fa9f99136e5f090b271a9a2252bfddd2771b295aba4c92c4f`
- Dispatch Spec: `PASS` at route SHA-256
  `e0a1c1fbc8aec27f570b90efed6b936e31df60673a5341a89c805bb22c95be6d`
- Independent tension checker: `PASS`, Tests 1 through 5
- Independent tension reviewer: `PASS`, Tests 1 through 5
- Human confirmation: pending
- Registration: none
- Research execution: none
- Runtime implementation: none
- Git, push, deployment, credentials, and external effects: none

## Claim and authority boundary

This proposal and any later findings are private research evidence. They do not
install eve, prove local compatibility, reconcile RWO lifecycle state, select
implementation, authorize dependency downloads, launch product agents, create
credentials, mutate ontology or authority, commit, push, publish, deploy, or
establish production readiness.

## Next human action

Reply exactly `confirmed` to authorize exactly one ledger registration and the
eight-seat read-only research dispatch bound to sheet SHA-256
`83732aff0172411fa9f99136e5f090b271a9a2252bfddd2771b295aba4c92c4f`.
Questions, discussion, approval to revise, or a different phrase do not launch
the dispatch. Any sheet-byte change requires fresh validation, double tension,
and confirmation.
