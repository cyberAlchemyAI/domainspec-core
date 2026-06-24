# Stage 06 — Invoke Redefine / Design

- Capability: `invoke` · Mode: `design` · Status: **pass** (forks resolved; g05)

## The component-system architecture (x-ray)

```
append-only event log  (CommentEvent, UIDecisionRecord — already canonical, L0/L4)
        │  (project, regenerable)
        ▼
UIIdentityIndex  ◄── derived read-model, per-repo cache, NOT source of truth  [closes Q4]
   ├─ UIElementIdentity        (concept node: "primary button")
   ├─ UIElementInstance        (versioned realization per PrototypeVariant)
   ├─ UIIdentityRelationType   (replaced-by / reshaped / same-concept / new / split-from / merged-into)
   ├─ TypedReference           (instance → identity)
   └─ UIVisualSignature        (24 owned DNA enums; canonical genome; NO raw values)
        │
        ├─ DiffSummary  (conformance-delta: per-field deltas → FitnessSignal(governance))
        │
        ▼
components page  ◄── read-model PROJECTION of UIIdentityIndex  [AF3 — free]
```

## Design decisions

- **DD-AF1 — `UIIdentityIndex` is a derived read-model.** Spec it inside the existing vocabulary (deepen, don't add an entity name): a regenerable projection over the append-only event log, keyed by `UIElementIdentity` via `TypedReference`. Per-repo cache file, **rebuildable from events**, never canonical. **Closes Q4.**
- **DD-AF2 — Owned canonical genome + resonant namespace-names fill.** The 24 `UIVisualSignature` enums are canonical (owned). The **R-7 underfilled dimensions** (Motion/Interaction/State/Feedback/Numeric) are filled with resonant **token namespace-NAMES as enum members** (`MOTION_EMPHASIZED`, `STATE_HOVER`, `NUMERIC_STEP_3`) — **never literal values** (A2), tagged `external_context`, `confidence<1.0` until both ends resolve (A4), **no vendoring, no promotion** (A3). Source: the **existing s1 mapping** (no new research).
- **DD-AF3 — Components page = projection of `UIIdentityIndex`.** Not a separate catalog. Rendering the index *is* the page; it inherits recognition-over-recall (A5) for free and cannot drift from source.
- **DD-AF4 — Two-phase matching.** Phase 1: `data-od-id` equality (exact, deterministic). Phase 2 (deferred): `DiffSummary` DNA-similarity emits a `FitnessSignal` that *proposes* an identity edge → **human confirms** (A4/A5). Phase 1 ships first.

## Preserved invariants

A1 (no new entity name — `UIIdentityIndex` is a read-model), A2 (names-only, no raw values), A3 (resonant stays external_context), A4 (confidence honesty), A5 (recognition-over-recall via projection).

## resonant decision

**Do NOT vendor.** The value (R-7 dimension names) is already captured in the s1 mapping; import names-only, doc-only. Vendoring is a **deferred, license-gated next-route** (bounded-research first).

## Open for s07 attack

1. A derived index "regenerable from events" — does it work for **cross-session** identity matching (`BaselineGenealogyFamily` lineages span session logs)? Is the event log complete/replayable enough?
2. Are resonant namespace-**names** themselves derived-from-their-values in a way that still needs attribution even doc-only?
3. Does the per-repo cache file risk becoming a de-facto source of truth?
