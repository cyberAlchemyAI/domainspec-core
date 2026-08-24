---
title: Ontology Vault Machine Semantic Source Implementation Layering
status: candidate
updatedAt: 2026-08-06
owner: Ontology Vault lifecycle owner through Sigil Development
scope: capability
---

# Ontology Vault Machine Semantic Source Implementation Layering

## Context

- Target: reusable semantic-source and derived-view spine for Ontology Vault
- Current state: brownfield candidate architecture; record/lifecycle work exists, source/projection spine does not
- Primary users: ontology authors, reviewers, package owners, and read-model consumers
- Primary constraints: one-source integrity, authoring usability, deterministic evidence, migration safety, and public/private isolation
- Sources: `stages/05-distill.md`, `stages/06-invoke-design.md`, `stages/07-interrogation-design-review.md`, `stages/08-distill-repair.md`

## Layer Boundary Heuristic

```text
Layer value = decision unlocked + user-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden
```

Each layer stops at the smallest evidence set that changes the next responsible
decision. Later layers preserve every earlier guarantee.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | User/operator outcome | Risk reduced | Promotion decision |
|---|---|---|---|---|---|
| L0 | After this layer, we know whether one closed JSON source can deterministically produce and correct one humane Markdown view without gaining authority. | Package schemas + canonicalizer + normalizer + Markdown operation graph + verifier/receipt + one SourcePatch witness | Author can view and propose correction from one source | Parallel truth, nondeterminism, validity-as-authority | Continue only if all positive and negative fixtures discriminate |
| L1 | After this layer, we know whether authoring and multiple projections are repeatable and usable. | Schema-guided authoring, semantic diff, atomic patch application, GraphView and QueryView | Author/reviewer can create, compare, preview, recover, and query | Hostile machine-first workflow and projection drift | Harden only after repeated source/view parity and UX evidence |
| L2 | After this layer, we know whether admission, migration, rollback, and private-boundary behavior hold under failure. | Admission event chain, total MigrationMap/Receipt, copy-and-verify cutover, leakage negatives | Owner can safely admit/migrate/rollback exact package versions | False authority, identity loss, irreversible migration, private leakage | Proceed only with owner and negative-control evidence |
| L3 | After this layer, we know whether the convention can be packaged and adopted through Ontology Vault lifecycle controls. | Sigil Development integration, generated projection sync, observability, one bounded adopter pilot | Reusable governed capability candidate | Packaging drift, lifecycle bypass, unsupported adoption | Candidate release/pilot only through explicit owner gates |

## Capability Progression

| Area | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| Source | Closed JSON single/multi-module fixtures | Form/editor authoring | Exact admitted package resolution | Reusable profiles and packaging |
| Projection | Markdown only | Markdown + graph + query | Stale/private/compatibility failure handling | Packaged projectors and observability |
| Correction | One SourcePatch witness | Semantic diff, atomic apply, invalid-draft recovery | Migration patches and rollback | Owner-routed lifecycle synchronization |
| Governance | Negative no-admission witness | No automatic authority under authoring tools | Admission events and PromotionRecord separation | Public convention and adopter gates |

## Layer Definitions

### L0 — Source-to-view trust kernel

Included:

- five source SchemaSuite modules and supporting protocol schemas;
- single- and multi-module fixtures;
- OV-CANON-JSON/v1 exact/canonical digest implementation;
- deterministic normalized model;
- Markdown ProjectionDefinition closed operation algebra;
- independent projection verifier, trace, and receipt;
- one generated-view selector to SourcePatch proposal;
- stale-view, invented-claim, missing endpoint, nondeterminism, IR-as-source,
  and schema-valid-without-admission negatives.

Deferred: full form UI, graph/query projectors, patch acceptance UX, migration,
admission resolver, lifecycle packaging, public convention mutation.

Exit evidence:

- two identical builds are byte-identical;
- semantic and structural emission checks pass;
- every declared negative fails for the intended reason;
- no source, view, or receipt claims admission/promotion;
- a correction changes source only through a typed patch.

### L1 — Repeatable humane authoring and projection parity

Adds schema-guided forms/editor, non-semantic AuthoringProfile, semantic versus
formatting diff, atomic patch application/rebase/recovery, and graph/query
projectors. Preserves one admitted source and the L0 verifier.

### L2 — Governance and migration hardening

Adds immutable admission events, exact package resolver, total identity maps,
copy-and-verify migration, retained rollback bytes, compatibility/residue
states, and synthetic private-leakage fixtures. Preserves every L0/L1 digest and
no-writeback guarantee.

### L3 — Lifecycle integration and reusable packaging

Adds public capability contracts only after owner approval, canonical-source
mutation through Sigil Development, generated skill synchronization, validation
matrix, observability, documentation, and one separately authorized adopter
pilot. Preserves public/private and authority boundaries.

## Implementation Wave Backbone

| Wave | Layer | Goal | Exit evidence |
|---|---|---|---|
| W0 | L0 | Prove the source-to-view-to-patch trust kernel | Executed deterministic and negative fixtures |
| W1 | L1 | Prove repeatable humane authoring and projection parity | Authoring/semantic-diff/graph/query evidence |
| W2 | L2 | Prove admission/migration/rollback/private isolation | Owner-bound governance and recovery witnesses |
| W3 | L3 | Package the reusable convention through lifecycle owners | Sigil Development validation and explicit approvals |

## Non-Regression Guardrails

- One semantic fact has one authored source.
- IR and views remain derived and disposable.
- Projection verification is independent of projector-authored claims.
- Stable identity is independent of file position, display order, title, and content digest.
- Validation, admission, promotion, and operational reliance remain distinct.
- Migration never overwrites the last admitted source.
- Public artifacts never contain private adopter semantics by proximity.

## Recommended Next Layer

- Next: L0, only after the Work Pack blockers are resolved.
- Decision unlocked: whether the exact source/projection architecture works at all.
- Major deferral: migration, admission runtime, public mutation, packaging, and adopter integration.
