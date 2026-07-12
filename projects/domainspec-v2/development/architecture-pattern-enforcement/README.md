---
node_type: development-package
docType: package-index
module: architecture-pattern-enforcement
feature_code: APE
status: draft
scope: full architecture-validation program
authored_by: invoke (define → design → plan)
updatedAt: 2026-07-12
---

# Architecture-Pattern Enforcement (APE) — development package

The governed development package for standing up **architecture-pattern validation & enforcement**
in domainspec-v2 — and carrying it across projects. Authored via `invoke` (complete chain:
define → design → plan). Nothing here is canonical authority; every artifact is a candidate that
owes owner-promotion (see [cav2 guardrail](#guardrail) below).

## Why this package exists

domainspec-v2 already **owns** the pieces of an architecture-validation system — a meta-type schema
layer, an edge-law, validators, an engine, and (in v1) a full pattern-library. Static node and edge
validation is now witnessed on the financial-settlement pack; bounded dynamic code-tag composability
now consumes root DS-D8 authority. CI repeatability, a second corpus, broader code-call semantics,
and card triage remain incomplete. This package sequences the owned
pieces and names what each part still owes before it can bind.

## Evidence base

This package does **not** re-derive its facts. Its load-bearing evidence is the research dispatch:

- [research findings](../../research/2026-07-02-architecture-patterns-enforcement/findings.md) — verdict matrix + phased plan (the corrected, skeptic-reviewed version).
- [collected returns](../../research/2026-07-02-architecture-patterns-enforcement/research.md) — E1 authority / E2 owned-inventory / E3 start-now.
- cav2 authority: [ARCHITECTURE-KNOWLEDGE-GOVERNANCE.md](../../../../cyberAlchemy-v2/architecture/ARCHITECTURE-KNOWLEDGE-GOVERNANCE.md).
- owned substrate: [impl/spec/](../../impl/spec/), [impl/governance/tags/](../../impl/governance/tags/), [impl/test-derivation-engine/](../../impl/test-derivation-engine/), v1 [architecture/pattern-library/](../../../../implementation/domainspec/architecture/pattern-library/).

## Chain (invoke)

| Stage | Artifact | Status |
| --- | --- | --- |
| define | [SPEC.md](SPEC.md) · [GLOSSARY.md](GLOSSARY.md) | drafted |
| design | [architecture-bundle.md](architecture-bundle.md) | drafted |
| plan | [implementation-layering.md](implementation-layering.md) · [execution-pack.md](execution-pack.md) · [WORK-PACK.md](WORK-PACK.md) | drafted |
| context | `.craft/` ledger (this package's recursive development context) | bootstrapped |

## Guardrail

cav2's core rule governs the whole package: **"has a tree ≠ has authority."** Standing up a
validator or writing a dependency rule produces *evidence*, not authority. A mechanism becomes
binding only after its owner-route promotes it (definitions-governance for a term,
constitution-governance for a rule). "architecture pattern" is not one of the nine authority kinds —
it must promote **into** a Definition or Constitution to bind. This package therefore ships
**candidate handles**, not authority, and every task names the promotion it still owes.

## Next route

`task-session` per SWU in [WORK-PACK.md](WORK-PACK.md). L0 is complete on the financial-settlement
feature pack, and bounded dynamic DS-D8 enforcement is complete through
[`TASK-R3C-EDGE`](../r3-closeout-plan/work-pack/tasks/TASK-R3C-EDGE.md) (`SWU-R3C-001..003`).
Second-corpus evidence is complete through `SWU-R3C-004`: the normalized AEO
pack passes current node/edge validation and its seeded invalid edge is
rejected. Card triage begins at `SWU-R3C-005`. APE-local CI and cleanup work
remain open.
