---
id: ui-prototyping-studio-architecture
project: ui-prototyping-studio
title: "UI Prototyping Studio — Receipt-Backed Architecture"
status: active
node_type: architecture
updatedAt: 2026-07-27
---

# Architecture

> The current implementation contract is
> [development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md](development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md).
> Its Task Session and joined Invoke closeout receipts under
> `development/invoke-runs/20260727T044346Z-chain-contract-refresh/` own
> implementation evidence. The June deep-spec and refinement material remains
> useful design history, not current execution or release authority.

## One sentence

The Studio is a local governance harness around an external UI generator: the
CLI and loopback preview adapt calls into an application-owned state machine,
the core validates and records reversible changes, and authorization remains
an explicit route concern rather than an identity inferred from the caller.

## Runtime shape

```text
external generator / authorized actor
              |
        CLI or loopback preview
              |
       application use cases
       + governed projection
              |
      domain state + invariants
              |
   file store + HTML artifact store
```

There is no embedded model, model API key, or in-process agent loop. Generation
is external and the resulting HTML crosses a deterministic admission seam.
The loopback browser server is a local adapter, not a release service.

## Layers and ownership

| Layer | Current responsibility |
| --- | --- |
| `interface/` | CLI and HTTP/preview adapters. They map inputs and display evidence; they do not own readiness or admission truth. |
| `application/` | Use cases, current-head projection, two-gate apply, handoff predicates, ports, and orchestration. |
| `domain/` | Session states, invariant-bearing models, honest diff types, and deterministic rules. No I/O dependency. |
| `infrastructure/` | Lock-aware file persistence and content-addressed HTML artifacts behind ports. |
| external generator | Produces variants and candidate HTML. It has no authority merely because it generated content. |

Dependencies point inward. Adapters must call the same application gates; a
browser or HTTP path is not allowed to invent a weaker rule.

## Governed loop

```text
open → prompt → variants → baseline → comments → synthesize → approve
     → propose candidate → validate/stage → acknowledge Accept or Revert
     → append revision → confirm handoff
```

The implemented subset has two distinct admission moments:

1. Approval binds intent and the batch checksum.
2. Accept binds the exact staged `candidateHtmlHash` after validation and
   inspection. Revert appends another revision; it does not rewrite history.

The browser acknowledgment is actor-neutral. It binds a live candidate or
revision identity, intended action, target state, and visible diff recap. It
records inspection intent; it does not establish actor identity or grant
authority. Export likewise requires explicit confirmation in the application
use case, but confirmation alone does not establish readiness.

## Current-head projection

`application/governed-state-projection.ts` is the read-model boundary for the
preview. It derives the primary document from current persisted head state,
uses that same document identity for annotation, labels older variants as
history, and carries staged/current revision evidence. The file-backed store
reloads persisted bytes on reads and serializes writes, so a long-lived
preview observes state written by another process.

## Honest visible-change evidence

`DiffSummaryHonest` cannot represent a CSS-only change as an empty structural
diff. It contains:

- per-`data-od-id` structural fragments;
- a style/global-unattributed lane;
- an unattributed structural lane; and
- a derived `visibleChangeCount`.

Preview, revision, state, and handoff consumers preserve those lanes. This is
evidence about visible change, not proof of complete CSS cascade semantics.

## Persistence and replay boundary

Session JSON and content-addressed HTML artifacts are local durable state.
Reads are fresh, writes are lock-serialized, and session-file replacement is
atomic. The admission verdict and recorded hashes are replayable evidence; an
external model proposal is not assumed reproducible.

The current implementation does not prove multi-host coordination, complete
crash compensation across every artifact operation, or a production-grade
node-identity/cascade model.

## Handoff predicates

The handoff bundle separates four facts:

| Predicate | Meaning |
| --- | --- |
| `exportConfirmed` | An explicit confirmer requested the irreversible export action. |
| `evidenceComplete` | Exactly `missingRefs.length === 0`. |
| `integrationReady` | Evidence is complete and the accepted head has a content hash plus honest diff evidence. |
| `implementationReady` | Integration-ready, with applied tasks and no unresolved comments. |

No predicate is release authorization. Confirmation is deliberately not an
input to the other three predicates.

## Browser boundary

The no-build preview is a governed local view with reversible actions:

- the current head is primary and history is labeled;
- click-to-annotate is unavailable until a real `data-od-id` target is
  selected;
- Accept/Revert is disabled until the live action context is acknowledged;
- the server rejects missing acknowledgment and stale identity/state;
- at 390px, before/after evidence stacks without document overflow; and
- handoff export remains outside the browser.

These receipts cover the named interactions. They do not constitute a full
accessibility audit or human ergonomics study.

## Remaining boundaries

- Full accessibility evidence, including a broad axe/keyboard/focus audit, is
  not established.
- Human trust and control ergonomics require study evidence.
- Release ownership, publication, deployment, and release authorization are
  unbound.
- Production-grade DOM identity, CSS cascade attribution, and crash
  compensation remain deeper hardening work.
- L4–L6 identity, conformance, learning, and human-evidence ambitions remain
  research-gated rather than implied by this L0 implementation.

## Decision pointers

Craft authority lives in [.craft/ledger.yml](.craft/ledger.yml), with the
human projection in [CRAFT.md](CRAFT.md). Important lineage includes the
generator seam, deterministic admission, append-only reversibility, and
actor-neutral operation decisions. Dated proposal detail remains under
`development/deep-spec-dispatch/` and `development/refinement-runs/`.
