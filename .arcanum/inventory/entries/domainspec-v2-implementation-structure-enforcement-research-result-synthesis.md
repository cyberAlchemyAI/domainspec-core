---
id: domainspec-v2-implementation-structure-enforcement-research-result-synthesis
kind: entry
type: synthesis
title: DomainSpec v2 implementation structure enforcement research result
updated: 2026-07-30
status: candidate
confidence: high
tags:
  - inventory
  - strategy-result
  - dispatch
  - subagents
  - research
  - domainspec-v2
  - domainspec-implementation
  - architecture-pattern
  - composability
  - language-enforcement
  - typescript
  - python
  - rust
  - ontology
  - authority
  - claim-le-proof
  - non-authority
sources:
  - projects/domainspec-v2/development/research/2026-07-30-implementation-structure-enforcement/findings.md
  - projects/domainspec-v2/development/research/2026-07-30-implementation-structure-enforcement/research.md
  - projects/domainspec-v2/development/research/2026-07-30-implementation-structure-enforcement/reviews/audit-final.md
  - telemetry/agents/subagents-dispatch.yaml
selectors:
  - '#answer-and-current-state-classification'
  - '#enforcement-model'
  - '#candidate-vocabulary-and-authority-map'
  - '#folder-module-and-import-conventions'
  - '#use-case-and-state-machine-example'
  - '#typescript-python-and-rust-toolchain-matrix'
  - '#blind-spots-and-typed-residue'
  - '#required-verdict-matrix'
  - '#claim-ceiling'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - implementation-profile-owner-admission-open
  - code-tag-reformulation-open
  - three-language-fixture-unexecuted
  - tool-version-project-fit-parity-performance-and-ide-evidence-open
  - exception-acceptance-owner-open
  - no-implementation-ontology-authority-promotion-publication-deployment-or-release-authorized
---

# DomainSpec v2 implementation structure enforcement research result

This non-authority Inventory read model records the accepted research result. It
does not admit an implementation profile, change source structure, install a
linter, promote ontology, or establish release or production readiness.

## Accepted boundary

The portable invariant is semantic and graph-shaped: each admitted canonical
`Rule` has one admitted `ImplementationBinding`, one callable entry point, and
each bound Operation/Query use case depends directly on that Rule leaf in the
canonical Rule-`enforces`-Operation direction.

One-file-per-rule, one-export-per-file, arrow-functions-only, and filenames as
semantic proof were rejected as universal laws. They may remain profile-local
ergonomic choices where a language and owner explicitly admit them.

## Candidate vocabulary

The result proposes exactly six implementation-facing terms:

- `ImplementationConformanceProfile`;
- `ImplementationBinding`;
- the existing owner-governed `Obligation`;
- `StateMachineRuntimeContract`;
- deferred `ExceptionRecord`;
- generated, non-authorizing `EvaluationReceipt`.

Language realizations, module constraints, runtime transitions, findings, and
provenance stay nested fields or existing artifacts. They are not new DS-D1
kinds, DS-D2 relationships, or CAV2 authority kinds.

## Structural enforcement

The candidate evaluator separates lexical/style, source-shape, module topology,
native static type, DomainSpec formation and graph checks, binding/provenance
reconciliation, and runtime/temporal evidence. Unsupported dynamic source
constructs fail closed.

The TypeScript lane combines ESLint/typescript-eslint, `tsc`, and a source import
graph; Python combines Ruff, mypy, Import Linter, and a narrow CPython `ast`
reader; Rust combines rustfmt, rustc, Clippy, Cargo package evidence, and a
bounded explicit `mod`/`use` reader. All are proposed and unexecuted against the
three-language fixture.

The v1 public-index/no-internal-import precedent conflicts with mandatory direct
Rule-leaf imports. The result routes that choice to the implementation-profile
owner instead of silently inheriting or overriding the precedent.

## State machines

Canonical State Machine identity and relationships remain ontology-owned. A
separate application-owned runtime contract may bind executable state,
transition selection, guards, effect intent, and runtime invariants. Current
DomainSpec v2 evidence covers only shallow formation and transition derivation,
not runtime correctness.

## Validation and dispatch closeout

- Three independent explorer reports were preserved verbatim.
- One synthesizer incorporated a bounded precedent-owner feedback return.
- Three independent reviewers passed precedent, non-vacuity, and non-collapse
  gates.
- The writer revised the findings through one bounded auditor feedback loop.
- The final auditor returned `ACCEPT` against findings SHA-256
  `ba6f3a537cf4abd408aedf46eb308f8d8e0574fc56adb6331a41a45ab7550027`.
- The dispatch ledger contains one registration row and one resolved close row:
  nine agents and two feedback loops.

## Open residue

Code-tag reformulation, profile ownership and admission, exact tool and parser
versions, project fit, three-language fixture execution, false positives,
caching, CI and IDE performance, exceptions, migration, state-machine
concurrency/effects, promotion, release, and production readiness remain open.

## Next human action

Ask the implementation-profile and code-tag owners to admit or reject the exact
binding/direct-edge contract before any language fixture or linter integration.
Then implement one smallest Rule/use-case/state-machine witness in TypeScript,
Python, and Rust with typed negative mutants and normalized receipts.
