# Define: Invoke Design Coverage

Status: approved authoring baseline.

Discovery: accepted governed research exists; no waiver.

Implementation status: not started.

## Problem

Invoke Design requires six views and companion selection evidence, but those
checks are authored from the same bounded context that they judge. A complete-
looking Design can omit an actor, interface, queue, store, writer, sink,
deployment boundary, compatibility boundary, or human semantic surface and
still satisfy structural checks.

The current contract also treats Design declarations, validator results, and
later runnable evidence too loosely. This makes false N/A, circular readiness,
and over-broad or under-broad UX selection possible.

## Objective

Add the smallest generic Design-selection protocol that:

1. closes and digests the inspected scope;
2. extracts an independent concern denominator;
3. assigns exact concern ownership and one of four dispositions;
4. verifies a deterministic two-pass fixed point;
5. strengthens architecture and UX only when triggered; and
6. separates authored Design, Design validation, and Plan evidence.

## Required outcomes

| ID | Required outcome |
| --- | --- |
| DVC-R01 | A `DesignScopeManifest` closes normalized sources, target footprint, actors, surfaces, interfaces, stores, queues, writers, rules, effects, sinks, deployment, compatibility, claims, and unknowns against an exact input digest. |
| DVC-R02 | A deterministic extractor independent of the manifest author emits a digest-bound `DesignDenominatorReceipt`. |
| DVC-R03 | The denominator is the union of authored concerns and extracted signals; every signal binds to one primary concern. |
| DVC-R04 | Every concern disposition is exactly `required`, `recommended`, `not-applicable-with-rationale`, or `block`. |
| DVC-R05 | Missing input, unknown scope, unbound signal, unresolved owner, stale/self-issued receipt, or absent fixed point blocks. |
| DVC-R06 | Selection runs exactly two passes; any changed scope, signal, owner, disposition, or output after pass two blocks. |
| DVC-R07 | Every concern names accountable, contributing, artifact, and validator owners. |
| DVC-R08 | Six views remain mandatory navigation; risk-triggered architecture extensions add only the depth demanded by detected concerns. |
| DVC-R09 | `ux-plan` is required only when a natural person and a new or changed human-facing semantic contract are both present. |
| DVC-R10 | Design owns planned `fixture_spec` and `validator_contract` records; Plan owns runnable validators, fixtures, and version-bound receipts. |
| DVC-R11 | Evidence states remain distinct: `authored-complete`, `design-validator-pass`, and `plan-evidence-pending|pass|fail`. |
| DVC-R12 | Frozen controls prove both non-omission and bounded selection; ordinary cases do not select every extension. |
| DVC-R13 | Canonical-first/generated-second synchronization is owner-controlled and parity-checked. |
| DVC-R14 | Public outputs are generic; Inventory and observability cannot set Design or Plan authority. |

## Scope

Included:

- generic scope-manifest, denominator-receipt, and selection-result schemas;
- deterministic extraction, classification, ownership, and fixed-point checks;
- exact diagnostics for missing, unknown, stale, self-issued, unbound, and
  changed-pass conditions;
- Design mode, architecture, DomainSpec architecture-bundle, and UX template
  contract updates;
- frozen positive, negative, bounded-selection, and mutation fixtures;
- integration with the Invoke validation runner;
- canonical-to-generated synchronization and public/private scans;
- one generic live Define → Design → Plan proof.

Excluded:

- implementing a general repository scanner;
- source-language semantic analysis beyond normalized declared selectors;
- universal specialist template families;
- executing downstream product work;
- changing DomainSpec or Saturn authority;
- promoting, publishing, committing, pushing, or bumping submodule pointers;
- absorbing unrelated dirty Invoke changes.

## Actors and authority

| Role | Authority |
| --- | --- |
| Invoke Design artifact author | authors a scope manifest and concern declarations; cannot validate its own denominator |
| `invoke-design-scope-extractor` | deterministically emits extracted signals for exact inputs; cannot select companions or promote artifacts |
| `invoke-design-selection-validator` | verifies schemas, digests, total binding, ownership, fixed point, and evidence-state legality |
| Spellcraft | owns canonical Invoke revision, lifecycle validation, generated synchronization authorization, and promotion readiness |
| Plan/work-pack owner | materializes runnable fixtures and validators; cannot rewrite Design evidence state |
| developer/maintainer | reads diagnostics and decides or repairs missing scope/ownership |
| Inventory/observability | discovery and execution evidence only |

The extractor and validator are distinct component identities even though
Spellcraft owns their public lifecycle.

## Behavioral law

```text
approved Define sources
  -> author and close DesignScopeManifest
  -> independent extractor emits DesignDenominatorReceipt
  -> validator unions authored + extracted signals
  -> classify, own, and disposition every concern
  -> select mandatory baseline and triggered companions/extensions
  -> repeat extraction and selection once
  -> unchanged fixed point => design-validator-pass
  -> Plan materializes runnable evidence
```

No authored manifest can self-issue its denominator. No negative prose alone
can establish N/A. No Design result can claim `plan-evidence-pass`.

## Decisions

1. Keep six views mandatory but explicitly non-sufficient.
2. Use one closed manifest and independent denominator per Design input digest.
3. Use four dispositions and exactly two selection passes.
4. Bind each signal to one primary concern before allowing overlays.
5. Keep architecture as the structural owner and route risk depth through
   triggered extensions.
6. Select UX from human semantic consequence, not file or UI keywords.
7. Keep planned witness contracts in Design and runnable evidence in Plan.
8. Add three interoperable schemas rather than one large lifecycle document.
9. Implement deterministic Python components within the existing Invoke
   package and reuse its validation runner.
10. Keep this authoring package private and all public implementation generic.

## Acceptance

- DVC-R01 through DVC-R14 map to Design components, tasks, SWUs, fixtures, and
  closure evidence.
- Omitted queue, store, API, sink, writer, and human surface fixtures fail.
- Pure local, static artifact, style-token, backend-only, CRUD, operator,
  lifecycle, and migration controls receive exact bounded selections.
- Mutation tests exist for every selection predicate.
- Stale and self-issued receipts reject.
- Pass two cannot change scope, selection, ownership, or output.
- UX positive and negative controls prove the semantic trigger.
- The first implementation SWU freezes the fixture denominator before runtime
  contracts are changed.

## Define-stage trace

- Techniques: `sequence`, `owner_boundary_check`,
  `artifact_contract_bridge`, `concrete_path_evidence`, `residue_ledger`.
- Distill sanity: pass; the coherent target is one Design-selection admission
  boundary, not a generalized analysis engine.
- Layering seed: L0 freeze the denominator; L1 prove schemas and algorithms; L2
  integrate contracts/templates; L3 synchronize and prove live.
- Next route: Design.

