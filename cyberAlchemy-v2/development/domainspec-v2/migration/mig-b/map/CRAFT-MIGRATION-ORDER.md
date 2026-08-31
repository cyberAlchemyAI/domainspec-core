# Craft MIG-B Migration Order

Status: **M00 refresh and freeze complete; M01 not started**
Authority effect: **none**
Machine view: [CRAFT-MIGRATION-ORDER.json](CRAFT-MIGRATION-ORDER.json)

## Identity And Migration Rule

Craft is the current name of the DomainSpec v2 Product lineage. This is a staged rename and relocation of the
same Product, not construction of a successor Product. Active destinations use `craft`; exact old-name source,
staging, candidate, and receipt paths remain immutable migration or historical evidence until the final Craft
vertical passes.

The migration source is the refreshed current working project at `projects/domainspec-v2`. The existing
`current-candidate-v2` through `current-candidate-v9` trees are diagnostic migration evidence. They are not a
ladder that must be continued, and candidate v9 is not a validated source of truth.

## What The Map Says

- 10,956 source entries and 98,598,963 bytes were refreshed at `2026-08-31T02:01:05Z`.
- 1,027 consumer files contain 9,073 literal `projects/domainspec-v2` occurrences after excluding the MIG-B preparation package from its own consumer population.
- All 53 development directories have one lifecycle and migration disposition.
- One directory, `implementation-conformance`, is an active runtime dependency.
- 26 directories are current continuations, 16 are completed evidence, four are superseded, and six are
  historical.
- Stage-2 additive copying and stage-3 old-name rebinding produced evidence, but no numbered baseline-v11
  candidate has a passing final aggregate receipt. Candidate v9 is unvalidated.

## Execution Order

| Order | Phase | Result required before continuing |
| ---: | --- | --- |
| 0 | Refresh and freeze | **Completed.** Source content remained digest-identical; the refreshed consumer and map epoch is bound by the M00 receipt. |
| 1 | Finalize Craft entry surfaces | Product, Project, Method, ontology, and source maps all express `same-product-renamed`. |
| 2 | Close the exact active dependency set | Every file and old-root occurrence is classified as active, continuation, completed, superseded, historical, or retained legacy evidence. |
| 3 | Materialize canonical Craft layers | Product, architecture, authority, ontology, research, and formalization enter final `/craft` roots from the frozen working source. |
| 4 | Materialize one runtime closure | One standalone Node 26 implementation and CLI exists at `cyberAlchemy-v2/implementation/craft`; no new numbered candidate tree is created. |
| 5 | Carry active runtime development | Move the single active dependency selected by `DW-01` and pass its real consumers from the final path. |
| 6 | Carry continuations | Move the 26 active or blocked continuation directories without executing or promoting their pending work. |
| 7 | Preserve completed evidence | Copy the 16 completed packages as evidence, retaining original path and digest identity. |
| 8 | Archive superseded evidence | Archive four superseded packages with no current runtime or authority role. |
| 9 | Archive historical evidence | Archive six historical packages without rewriting their historical claims. |
| 10 | Rebind current consumers | Point current consumers at Craft; allowlist every retained old-name reference as immutable evidence. |
| 11 | Validate the final Craft vertical | Run the complete final-path runtime, CLI, profile, Operation, Workflow, target-project, conformance, and determinism surface. |
| 12 | Freeze the current Craft baseline | Freeze the passing graph once, switch current internal references, and leave legacy roots read-only and reversible. |

## Directory Order

The directory order comes directly from `MIGRATION-MATRIX.json`; it is not a new interpretation of work-pack
status. Each selector is machine-checked and together they cover every directory exactly once.

| Wave | Matrix disposition | Count | Destination role |
| ---: | --- | ---: | --- |
| 1 | `carry-forward-active-dependency` | 1 | Current Craft continuation required by runtime validation |
| 2 | `carry-forward-continuation` | 26 | Non-canonical active or blocked continuation |
| 3 | `preserve-completed-provenance` | 16 | Completed evidence |
| 4 | `archive-superseded-provenance` | 4 | Superseded evidence archive |
| 5 | `archive-historical-provenance` | 6 | Historical evidence archive |

Within a wave, directories are copied in lexical order for determinism. That lexical copy order is not an
execution or implementation priority. Pending work remains governed by each directory's own current state.

## Final Active Roots

| Concern | Active destination |
| --- | --- |
| Product | `cyberAlchemy-v2/product/craft` |
| Architecture | `cyberAlchemy-v2/architecture/craft` |
| Authority | `cyberAlchemy-v2/authority/craft` |
| Ontology | `cyberAlchemy-v2/ontology/craft` |
| Implementation and formalization | `cyberAlchemy-v2/implementation/craft` |
| Research | `cyberAlchemy-v2/research/craft` |
| Development | `cyberAlchemy-v2/development/craft` |

Old `/domainspec-v2` roots remain evidence surfaces. This order does not authorize their deletion.

## Why The Order Stops The Candidate Loop

The migration does not build candidate v10, v11, or another numbered copy. It refreshes one source epoch, writes
one final Craft staging root, repairs that same root until every reachable final-path check passes, and freezes
one current Craft baseline only after the complete vertical succeeds. A failed validation changes no source or
legacy evidence and resumes at the failed phase on the same staging root.

## Completion Proof

Migration is complete only when:

1. the final Craft package installs, typechecks, tests, and builds in the repository Node 26 container;
2. TypeScript, Python, and Rust realizations pass independent conformance from final paths;
3. Operation and Workflow enforce declared reads, writes, effects, guards, atomic state and outbox, explicit
   failure continuation, undeclared-effect rejection, relationship constraints, and durable recovery bindings;
4. a target project is generated from typed intent and checked against exact selected realization and byte
   digests;
5. two identical runs produce identical target bytes, manifests, and conformance results; and
6. every old-root occurrence is either rebound or explicitly retained as immutable evidence.

## Current Blockers

There is no open semantic decision gate for the migration order. M00 is complete. Later execution remains
mechanically blocked until the 1,027 consumer files and 9,073 occurrences are partitioned and the final Craft
root—not candidate v9—passes the complete validation vertical.

Validate this order with:

```text
toolchains/node-typescript/bin/node-env run --project projects/domainspec-v2/impl -- node ../../../cyberAlchemy-v2/development/domainspec-v2/migration/mig-b/validate-craft-migration-order.mjs
```
