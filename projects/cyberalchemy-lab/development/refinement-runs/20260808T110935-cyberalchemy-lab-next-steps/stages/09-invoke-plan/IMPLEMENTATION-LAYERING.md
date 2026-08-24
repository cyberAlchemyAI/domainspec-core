---
title: Tower Evidence Navigator Implementation Layering
status: candidate-plan
updatedAt: 2026-08-08
owner: cyberalchemy-lab-plan-owner
scope: research-workflow
---

# Tower Evidence Navigator Implementation Layering

## Context

- Target: private candidate Tower Evidence Navigator.
- Current state: greenfield product surface with accepted research and a validated run-local design; no product files exist.
- Primary operator: a researcher validating selector-bound tower evidence before adding an IDE surface.
- Primary constraint: research validity and owner/authority separation.
- Source references: `../05-distill.md`, `../06-invoke-design/ARCHITECTURE.md`, `../08-distill-repair.md`.

## Layering method and boundary heuristic

Each layer ends at the smallest slice that changes what the team can responsibly decide next.

```text
Layer value = decision unlocked + operator-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden
```

The next unit moves to a later layer when it adds less value-per-cost to the current decision than beginning the next decision. Promotion is evidence-gated; preference, fixture similarity, and passing unrelated checks are insufficient.

## Layer decision table

| Layer | Decision question | Minimum working unit | Operator outcome | Risk reduced | Promotion decision |
| --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether the closed identity/relation/privacy contract can deterministically accept one complete synthetic tower and reject controlled mutants. | Private candidate package, compiler, complete synthetic fixture, package snapshot, disposable projection, independent ValidationRecords. | Inspectable one-tower mechanics projection with exact failure evidence. | Circular identity, relation drift, privacy leaks, authority uplift, and fixture ambiguity become falsifiable. | Continue to L1 only if all 15 mutants fail correctly and deterministic reruns match. |
| L1 | After this layer, we know whether the same contract can admit one corpus-owner-selected real tower without semantic or privacy drift. | Exact owner decision, real complete ordered manifest, one real projection and independent validation. | One bounded real research tower can be navigated as evidence. | Synthetic-to-real substitution and representativeness ambiguity are exposed. | Continue to L2 only after corpus, ontology, privacy, and validation owners accept exact evidence. |
| L2 | After this layer, we know whether a direct-GET trusted shell can navigate one exact projection without hidden state or protected effects. | Allowlisted adapter, trusted shell, session/revision binding, browser/runtime/privacy/accessibility evidence. | Interactive evidence navigation. | UI masking, stale view, state mutation, transport, and accessibility risks are tested. | Continue to L3 only on independent runtime/browser/UX evidence. |
| L3 | After this layer, we know whether bounded multi-tower reuse and packaging are credible. | Additional owner-selected towers, aggregation contract, degraded modes, packaging/operational evidence. | Repeatable bounded Lab workflow. | Cross-tower identity, scaling, support, and rollout risks are tested. | Pilot/package/defer; authority, publication, deployment, release, and production remain separate gates. |

## Capability progression

| Area | L0 | L1 | L2 | L3 |
| --- | --- | --- | --- | --- |
| Evidence input | one complete synthetic tower | one owner-selected real tower | unchanged one real projection | bounded additional selected towers |
| Identity | local canonical profile and exact snapshot formulas | real bytes/owner identity | revision/session binding | cross-tower aggregation without ID collapse |
| Meaning | closed candidate records/relations | real-source candidate review | presentation only | bounded comparative views |
| Validation | unit, schema, 15 mutants, deterministic bytes | real-source integration/privacy | runtime/browser/accessibility/UX | replication/degraded-mode/operations |
| Interface | versioned projection file | same projection contract | direct GET + trusted shell | multi-tower query/navigation contract |
| Authority | none | none absent separate owner decision | none | none absent separate owner decisions |

## Layer definitions

### L0 — Synthetic mechanics proof

Included:

- Research Tower navigation/closure spine;
- `cal-canonical-json-v1` and normalized package self-binding;
- closed record/relation/privacy/projection contracts;
- exactly one complete synthetic tower fixture;
- dependency-free Node compiler and test harness;
- 15 deterministic negative mutants;
- source package snapshot and separate witness-run output;
- independent exact-input ValidationRecords.

Deferred: T04/T26/other real selection, Inventory ingestion, IDE code, HTTP runtime, browser/UX/accessibility, multiple towers, graph storage, external/public effects, authority/promotion.

Exit evidence:

- every authored package file appears exactly once in the normalized package snapshot;
- repeated compilation produces byte-identical projection and revision;
- all 15 mutants fail with their bound stable code and do not replace the valid output;
- the final projection passes schema, privacy scan, relation closure, residue/promotion invariants, and independent-validator checks;
- all evidence says `synthetic-contract-fixture` and `authority_effect: none`.

Continue when all exit evidence passes. Pivot if canonicalization/self-binding cannot be implemented without ambiguity. Stop if privacy/authority invariants cannot be fail-closed.

### L1 — One real tower

Adds an exact corpus-owner decision and complete manifest for T04, mechanics-only T26, or another eligible tower. It must preserve all L0 identity, privacy, failure, and no-authority guarantees. The synthetic receipt is never reclassified as real evidence.

### L2 — Interactive workbench

Adds an IDE-owned direct-GET adapter and natural-person rendered surface. It preserves source/package/projection identities and may not add POST, publication, domain mutation, interaction persistence, or hidden authority. UX, accessibility, runtime, and browser validation become mandatory here, not earlier.

### L3 — Bounded reuse and packaging

Adds owner-selected additional towers, aggregation/degraded-mode rules, and packaging evidence. It does not imply public release or production readiness.

## L0 implementation wave backbone

| Wave | Goal | SWUs | Promotion evidence |
| --- | --- | --- | --- |
| W0 | Prove the smallest deterministic identity primitive. | `SWU-CAL-001` | canonical bytes/digest tests pass and invalid value classes reject |
| W1 | Close schemas, package governance, and one valid fixture. | `SWU-CAL-002` through `SWU-CAL-006` | record/relation/privacy/package/fixture contract tests pass |
| W2 | Implement transformation and fail-closed mutants. | `SWU-CAL-007`, `SWU-CAL-008` | valid compile passes; 15 mutants fail with exact codes |
| W3 | Bind complete source package identity and independent witness evidence. | `SWU-CAL-009`, `SWU-CAL-010` | package snapshot, deterministic projection, and independent records pass |

## Non-regression guardrails

- Logical identity stays distinct from byte digest and snapshot identity.
- Manifest order changes snapshot identity.
- Generated projection remains outside source package identity.
- Synthetic mechanics evidence never becomes real-source evidence.
- Open residue, contradiction, and blocked promotion remain visible.
- Candidate/projection artifacts keep `authority_effect: none`.
- No layer silently adds public/private crossing, external transport, promotion, deployment, release, or production claims.

## Open decisions and major deferral

- Corpus owner must select and lock one real tower before L1.
- IDE owner must separately approve the direct-GET surface before L2.
- Most important deferral: any claim that CyberAlchemy Lab combines all repository research; the denominator and eligibility decisions do not exist.

## Implementation Layering Result

- Target: Tower Evidence Navigator
- Artifact: this file
- Mode: created
- Layer count: 4
- Recommended next layer: L0
- Boundary heuristic: applied
- Key decision unlocked by L0: whether identity/relation/privacy mechanics are deterministic and fail closed for one complete synthetic tower
- Major deferred scope: real-tower selection and all IDE/multi-tower/effect/authority work
- Validation: structure and plan-level Distill validation only; product commands not run

