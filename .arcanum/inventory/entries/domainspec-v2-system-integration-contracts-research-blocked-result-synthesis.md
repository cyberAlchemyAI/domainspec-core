---
id: domainspec-v2-system-integration-contracts-research-blocked-result-synthesis
kind: entry
type: synthesis
title: DomainSpec v2 system-integration contracts research closed at blocked evidence frontier
updated: 2026-08-13
status: candidate
confidence: high
dispatch_id: 2026-08-13-domainspec-v2-system-integration-contracts
dispatch_type: research
working_folder: projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/
tags:
  - inventory
  - strategy-result
  - dispatch
  - subagents
  - research
  - domainspec-v2
  - database
  - validation
  - authority
  - claim-le-proof
  - non-authority
sources:
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/receipts/integration-contract-synthesis-revision-1.json
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/receipts/evidence-closure.json
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/receipts/reviewer-precedent.json
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/receipts/reviewer-non-vacuity.json
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/receipts/reviewer-non-collapse.json
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/orchestration/dsv2sic-20260813T044615Z/final-event-validation.json
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/orchestration/dsv2sic-20260813T044615Z/wave-03-reduce/gate-decision.json
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/DISPATCH-ROUTE.json
  - projects/domainspec-v2/development/research/2026-08-13-system-integration-contracts/dispatch-sheet.json
  - telemetry/agents/subagents-dispatch.yaml
selectors:
  - '#outcome'
  - '#current-state-answer'
  - '#candidate-contract-layer'
  - '#blocked-evidence-frontier'
  - '#claim-ceiling'
  - '#next-owner-gates'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - dispatch-closed-dissent-irreconcilable
  - seven-of-nine-agents-spawned
  - writer-and-auditor-not-admitted
  - findings-md-intentionally-absent
  - non-collapse-nc-01-nc-02-unresolved
  - executable-fixture-closure-blocked
  - runtime-evaluator-registry-missing
  - evaluation-receipt-schema-missing
  - no-definitions-profile-implementation-validator-authority-publication-release-deployment-production-change
---

# DomainSpec v2 System-Integration Contracts Research Closed At Blocked Evidence Frontier

## Outcome

The confirmed research dispatch completed three explorer lanes, one bounded
synthesis, one explorer-feedback loop, and three independent reviewer passes.
Precedent and non-vacuity review passed. Non-collapse review blocked on two
remaining ownership defects, and executable fixture closure independently
blocked. The writer and auditor were therefore not admitted, and no
`findings.md` was created.

The append-only dispatch ledger closes the run as
`dissent_irreconcilable` after seven of nine planned agents and both bounded
feedback loops. The 63-event causal stream passes its final validator.

## Current State Answer

DomainSpec v2 currently owns the logical domain and application surface through
DS-D1 records such as `Operation`, `Query`, `Policy`, `Workflow`, `Interface`,
`Event`, and `Mapping`, plus the existing DS-D8 relations. It does not own a
canonical system-integration contract layer.

The current compiler validates structural formation, profile, graph, digest, and
provenance constraints. The development BTE path supplies bounded structural
receipts, not a generic runtime evaluator registry. A draft
implementation-conformance design proposes an `EvaluationReceipt`, but neither
that runtime schema nor its evaluator owner is implemented or admitted.

Concrete databases, ORM implementations, migration runners, HTTP clients and
servers, brokers, outbox and inbox resources, credentials, topology, and
provider behavior belong in versioned technology or implementation profiles.
They should not become domain meta-types by default.

## Candidate Contract Layer

The synthesis separates eight concerns: domain semantics, application
contract, implementation binding, technology profile, runtime guarantee,
validation obligation, operational evidence, and authority. Its six-record
working set is proposed and unadmitted:

- `PersistenceBinding`
- a reduced `MigrationContract`
- `TransportBinding`, merging the former `ApiBinding` and `MessageChannel`
  candidates
- `TransactionGuaranteeBinding`
- `DeliveryGuaranteeBinding`
- `FailureOutcomeBinding`

Existing `Interface`, `Mapping`, `Policy`, and `Workflow` remain the owners for
repository and API surfaces, logical mappings, strategy, and compensation.
`Database`, ORM implementation, event bus or broker, outbox, inbox, DDL,
migration runner, protocol clients and servers, secret resolution, and topology
remain profile-local. A generic `ConsistencyPolicy` is deferred until an exact
invariant, participants, boundaries, lifecycle, and discriminating witness
exist.

The candidate set is not yet clean enough to write as a finding. NC-01 requires
moving `PersistenceBinding.claim_limits` to validation or evidence and marking
`binding_digest` as generated provenance. NC-02 requires removing duplicate
retry ownership from `TransactionGuaranteeBinding` in favor of one
`failure_outcome_ref` to `FailureOutcomeBinding`.

## Blocked Evidence Frontier

Research claims about current state, absence, external precedent, and candidate
shape close only for the exact cited bytes. Executable fixture closure remains
blocked because the target lacks exact outbound API and webhook records,
consumer and projection records and relations, admitted binding and guarantee
schemas, provider resources and adapters, migrations, outbox and inbox,
transport topology, fault seams, a runtime evaluator registry, an
`EvaluationReceipt` schema, and executed positive and hostile cases.

The hostile matrix includes rollback, partial commit, stale migration,
uniqueness races, lost updates, read anomalies, projection staleness, remote
success followed by timeout, invalid webhook signatures, duplicate and
reordered delivery, poison messages, payload-version mismatch, outbox and inbox
divergence, and controlled replay. Each remains proposed and unexecuted.

## Claim Ceiling

This is an additive, non-authority Inventory read model for a blocked research
frontier. It does not define or admit vocabulary, alter profiles, implement
integrations, prove database or distributed guarantees, establish consistency
or idempotency, accept evidence, promote authority, publish, release, deploy,
or establish production readiness.

## Next Owner Gates

The next candidate must first resolve NC-01 and NC-02 and receive a fresh
non-collapse review. Definitions and semantic-profile owners must then decide
whether to admit the resulting namespace and exact fixture records. Only after
that may implementation-profile owners bind concrete resources and adapters,
and runtime-evidence owners create the evaluator registry, receipt schema,
fault fixtures, and positive and hostile executions. Human acceptance or
promotion remains a separate final gate.
