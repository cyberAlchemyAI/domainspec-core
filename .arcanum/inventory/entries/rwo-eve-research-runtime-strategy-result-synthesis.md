---
id: rwo-eve-research-runtime-strategy-result-synthesis
kind: entry
type: synthesis
title: RWO-managed eve research runtime strategy result
updated: 2026-08-12
status: candidate
confidence: high
dispatch_id: 2026-08-12-rwo-eve-research-runtime
dispatch_type: research
working_folder: ops/development/2026-08-12-rwo-eve-research-runtime/
tags:
  - inventory
  - strategy-result
  - dispatch
  - subagents
  - research
  - exact-binding
  - operational-evidence
  - claim-le-proof
  - non-authority
sources:
  - ops/development/2026-08-12-rwo-eve-research-runtime/dispatch-sheet.json
  - ops/development/2026-08-12-rwo-eve-research-runtime/DISPATCH-ROUTE.json
  - ops/development/2026-08-12-rwo-eve-research-runtime/STRATEGY.md
  - ops/development/2026-08-12-rwo-eve-research-runtime/TENSION-GATE.json
  - ops/development/2026-08-12-rwo-eve-research-runtime/EVE-SOURCE-SNAPSHOT.json
  - ops/development/2026-08-12-rwo-eve-research-runtime/strategy-inventory-packet.json
selectors:
  - '#p1-trigger-decision'
  - '#starting-architecture-hypothesis'
  - '#bootstrap-rule'
  - '#lanes-groups-and-subagents'
  - '#dependency-flow'
  - '#required-research-result'
  - '#inventory-preflight'
  - '#gate-and-ledger-state'
  - '#claim-and-authority-boundary'
  - '#next-human-action'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - dispatch-confirmation-pending
  - dispatch-unregistered-and-unexecuted
  - runtime-not-implemented-or-launched
  - nested-orchestrator-inventory-empty-and-blocked
  - current-rwo-runtime-volatile-without-delivery
  - eve-beta-api-drift-risk
  - no-dependency-installation-credentials-lifecycle-sync-git-publication-deployment-or-external-effect
---

# RWO-managed eve research runtime strategy result

This is a non-authority Inventory read model of a confirmation-ready research
proposal. It does not install eve, implement or run an RWO-to-eve bridge,
register the dispatch, launch agents, synchronize RWO lifecycle state, modify
ontology or authority, operate Git, publish, deploy, or prove production
readiness.

## P1 trigger decision

Synthesis, context protection, isolation, and useful parallelism all apply. The
question crosses official eve runtime contracts, the exact current Rust/Go RWO
prototype, DomainSpec research governance, and independent operational failure
and authority concerns.

## Starting architecture hypothesis

The strategy tests a four-owner split: DomainSpec owns research roles,
dependencies, confirmation, registration, and evidence closure; RWO compiles
and reduces deterministic graph state into zero-or-one command intents; a
future delivery coordinator owns durable attempts, dedupe, cancellation, and
result normalization; eve owns bounded sessions, declared agents, model turns,
tools, and tool approvals.

The hypothesis explicitly rejects treating `agent.ts` as the whole research
graph. Official current eve sources describe `agent.ts` as runtime
configuration, while declared specialist identities and their prompts/tools
live under `agent/subagents/<id>/` and adjacent filesystem slots.

## Bootstrap rule

If confirmed, this research uses the current native Codex dispatch path. It
does not use the not-yet-built RWO-to-eve bridge to research that same bridge.
Only accepted findings may later seed a separately governed implementation Work
Pack.

## Lanes, groups, and subagents

- Explorers: Turing owns current official eve semantics; Hewitt owns the exact
  DomainSpec-to-RWO state/event/command mapping; Simon owns failure, security,
  durability, and authority stress tests.
- Synthesizer: Shannon selects or kills topologies and produces the boundary,
  finite fixture, and implementation Work-Pack skeleton.
- Reviewers: Popper attacks non-vacuity; Quine attacks definitional and
  authority collapse.
- Writer: van Lamsweerde may write only `findings.md` after evidence closure.
- Auditor: Brandenburg may accept or return one bounded writer repair. The
  parent remains final approver.

## Dependency flow

Three explorers run in parallel, join into synthesis, then two reviewers run
in parallel with one bounded synthesis repair. Exact-binding evidence closure
gates the writer, auditor, and parent.

## Required research result

The result must select one topology, map all owners, define dispatch-to-RWO
compilation, specify versioned event and command projections, settle approval,
identity, dedupe, retry, replay, cancellation, and crash rules, define the eve
filesystem topology, provide a discriminating local fixture, and return a
sequenced implementation-ready Work Pack with explicit claim ceilings.

## Inventory preflight

The root machine index passed with zero failures and 153 inherited warnings.
The nested orchestrator Inventory is empty and blocked, and no Inventory entry
covers eve. Prior entries are therefore discovery leads only; exact live RWO
sources and pinned official eve sources decide current claims.

## Gate and ledger state

- Sheet schema `0.8.0`: `PASS`.
- Exact sheet SHA-256:
  `83732aff0172411fa9f99136e5f090b271a9a2252bfddd2771b295aba4c92c4f`.
- Dispatch Spec: `PASS` at route SHA-256
  `e0a1c1fbc8aec27f570b90efed6b936e31df60673a5341a89c805bb22c95be6d`.
- Independent tension: `PASS + PASS`, Tests 1 through 5.
- Human confirmation: pending.
- Registration, execution, implementation, lifecycle synchronization, and
  external effects: none.

## Claim and authority boundary

The current RWO evidence is candidate-local and volatile; it does not prove
durable agent execution. Official eve documentation proves a current beta
framework contract, not local installation, compatibility, security,
deployment, or production fitness. A semantic RWO command is not delivery,
execution, approval, or completion evidence.

## Next human action

Reply exactly `confirmed` to authorize one ledger registration and execution of
the eight-seat read-only research dispatch bound to the exact sheet digest. Any
sheet-byte change requires new validation, double tension, and confirmation.
