---
module: inventory-runtime-faceted-layout
handoffOwner: sigil-development
targetSigil: inventory
status: owner-integration-required
updatedAt: 2026-07-24
---

# Sigil Handoff: Inventory Runtime And Faceted Layout

## Sigil Identity

- Sigil: `inventory`
- Lifecycle route: `sigil-development inventory --update`
- Invoke package: this directory
- Proposed first implementation unit: `SWU-IFR-001`
- Existing selected canonical unit: `SWU-INT-001`

## Purpose

Add a deterministic append-operation runtime and a non-combinatorial faceted
layout for new Inventory entries while keeping Inventory a non-authoritative
discovery/read-model surface.

## Operator Modes

| Mode | Contract |
|---|---|
| `dry-run` | Resolve the package, validate baseline and candidate state, compute exact changes and receipt bytes, and write nothing. |
| `apply` | Execute the already-computed managed writes sequentially, report every observed write, and fail closed with `partial_mutation_possible=true` when completion cannot be proved. |
| `sync --check` | Compare canonical runtime members with the declared generated managed set; write nothing. |
| `sync --apply` | Update only declared generated runtime members and emit a sync receipt. |

No mode supplies replace, update, delete, migration, locking, recovery, or
currentness verification.

## Input Contract

- repository or package root resolved independently of caller CWD;
- one candidate entry conforming to the admitted schema;
- controlled tags plus:
  - `namespace`: one stable physical grouping;
  - `record_class`: one physical record category distinct from existing
    content `type`;
  - `concepts`: zero or more logical multi-valued facets;
- explicit dry-run/apply selection;
- canonical package manifest when operating through installed runtime.

## Output Contract

Every operation returns a canonical receipt with:

- operation and mode identity;
- baseline and candidate digests;
- validator results and warning delta;
- planned or observed managed writes;
- terminal status and blockers;
- partial-mutation flag;
- artifact references;
- runtime manifest identity when invoked from a generated package.

Receipt bytes must be stable for equal inputs. A stored receipt proves only its
historical operation; it does not prove currentness.

## Facet Contract

- New physical path:
  `.arcanum/inventory/entries/<namespace>/<record-class>/<stable-id>.md`.
- `namespace` and `record_class` are single-valued and path-safe.
- `concepts` is multi-valued, normalized, sorted, and deduplicated.
- Derived maps are `by_namespace`, `by_record_class`, and `by_concept`.
- Human views may group by the same facets but remain generated read models.
- Existing flat and nested legacy entries remain valid and unmoved.
- No directory may be derived from a tag or concept combination.

## Required Validation Examples

1. Equal inputs produce byte-identical receipts.
2. Dry-run from an unrelated CWD writes zero bytes.
3. Baseline historical warnings do not become new failures.
4. Candidate warnings are reported as an exact delta.
5. No-op, conflict, missing helper, and malformed candidate fail
   deterministically.
6. Injected apply failure reports observed writes and partial-mutation risk.
7. Postwrite alteration is detected.
8. Facet path traversal and normalized collisions block.
9. Legacy entries validate without new required fields.
10. Exact derived maps and human projections match the admitted records.
11. Generated-runtime managed-set drift blocks.
12. An isolated installed consumer reproduces the acceptance suite.

## Observability

- Group by `dispatch_id + step_id + swu_id + run_id`.
- Append one Task Session receipt per SWU.
- Preserve warning delta and partial-write evidence.
- Do not infer lifecycle acceptance, currentness, promotion, release, commit,
  push, or publication from operation receipts.

## Owner Decision Required

Before source mutation, Sigil Development must:

1. compare this delta with
   `arcanum/arcana/inventory/development/WORK-PACK.md`;
2. explicitly sequence, merge, or supersede its selected `SWU-INT-001`;
3. confirm the proposed canonical and generated write scopes; and
4. issue an owner-acceptance receipt.

If any item remains unresolved, return `block` with residue. Invoke does not
choose on the lifecycle owner's behalf.
