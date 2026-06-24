# Invoke · Design — `UIIdentityIndex` (Component Registry)

- Mode: `design` · Owner: `invoke` (parent-coordinator receipt under the `goal` loop)
- Goal node: **A1** — closes `GAP-COMPONENT-REGISTRY-002` ("persistence/index entity unspecified, R-1"); feeds `BLK-IDENTITY-TYPES-002` closure.
- Source design: refine run `2026-06-23-component-system-architecture/RESULT.md`; deep-spec `SYNTHESIZED-DEEP-DESIGN.md §2.3/2.4/3.x`.
- Status: **draft** (converges into the deep-spec final design; not promoted).
- Boundary: design artifact only — **no `models.ts` mutation, no ledger mutation** in this step (both staged for approval).

## 1. What this closes

`GAP-COMPONENT-REGISTRY-002` left one thing unspecified: *how `UIElementIdentity` nodes are stored, queried, and matched across sessions and `BaselineGenealogyFamily` lineages.* This design specifies that entity — **`UIIdentityIndex`** — and the identity/DNA value objects it indexes (the `BLK-IDENTITY-TYPES-002` types), entirely inside the existing domainspec UI vocabulary (no new durable entity).

## 2. `UIIdentityIndex` — the registry, as a derived read-model

**Decision: a repo-scoped, derived, regenerable projection over the append-only event log. Not a new canonical store.**

- **Nature.** `UIIdentityIndex` is a *read-model*, not a durable entity. The single source of truth stays the append-only event stream (`CommentEvent`, `UIDecisionRecord`, the revision manifest). The index is a **rebuildable cache** keyed by `UIElementIdentity`.
- **Scope.** **Repo-scoped**, not session-scoped: it aggregates over *all* session event logs in the repo so cross-session recognition and `BaselineGenealogyFamily` lineages resolve (recognition-over-recall, the registry's design goal per §2.4).
- **Anti-canonical guard.** The cache file is stamped `derived; regenerable; do not edit` and ships with a `rebuild` path. Any drift between cache and events is resolved by trusting the events — the index is **never a write target**.
- **Vocabulary fit (A1-invariant).** No new entity *name*: `UIIdentityIndex` is specified as a projection over existing types. It deepens, it does not invent.

### 2.1 Shape (TypeScript-leaning, for `models.ts` convergence)

```
UIIdentityIndex = {
  identityIndexVersion: string          // canonicalizer-style identity, e.g. "ups-identity-index v0.1.0"
  scope: "repo"                          // repo-scoped projection
  builtFrom: TypedReference[]            // the event-log sources this projection was rebuilt from
  identities: UIElementIdentity[]        // the concept nodes
  instancesByIdentity: Map<IdentityId, UIElementInstance[]>   // versioned realizations
  edges: UIIdentityRelation[]            // typed version edges between instances
}
```

It is **always reconstructable** from `builtFrom`; persisting it is an optimization, never a commitment.

## 3. The indexed types (closes `BLK-IDENTITY-TYPES-002`)

These are the L4 identity/DNA types absent from `models.ts` today. Specified here for convergence; **implementation is a separate gated node (A2).**

- **`UIElementIdentity`** — the stable concept node. `{ identityId, conceptLabel, firstSeenRevision }`. ("primary button", "filter chip".)
- **`UIElementInstance`** — a versioned realization within a `PrototypeVariant`. `{ instanceId, identityRef: TypedReference→UIElementIdentity, variantRef, odId | structuralHandle, signature: UIVisualSignature }`.
- **`UIIdentityRelationType`** — the typed version edge (unchanged value set): `replaced-by | reshaped | same-concept | new | split-from | merged-into`.
- **`UIIdentityRelation`** — `{ from: instanceId, to: instanceId, relation: UIIdentityRelationType }`.
- **`UIVisualSignature`** — the 24 owned DNA enums (the visual genome). **No raw values** (shape-only proof obligation). The R-7 underfilled dimensions (Motion / Interaction / State / Feedback / Numeric) are filled with **resonant token namespace-NAMES as enum members** (`MOTION_EMPHASIZED`, `STATE_HOVER`, `NUMERIC_STEP_3`) — never literal values, tagged `external_context`, `confidence < 1.0`, provenance recorded; **no vendoring, no canonical promotion** (gate g1).
- **`DiffSummary`** (refined — today it is only `{added,changed,removed}` counts) — an ordered list of per-field deltas over two `UIVisualSignature`s, each `{ dimension, fromValue, toValue, preference, confidence }`, surfaced as `FitnessSignal(source=governance)`. **This is the `BLK-IDENTITY-TYPES-002` + `DEC-R2-CSS-ATTRIBUTION-017` upgrade** that makes confirm-identity and honest theme-diffing possible.

## 4. Matching (instance → identity)

Two-phase, so reuse is detected without false auto-promotion:

1. **Phase 1 (ships first) — `data-od-id` equality.** Exact, deterministic instance→identity resolution. Covers all tagged components today.
2. **Phase 2 (deferred, node A-next) — DNA-signature similarity.** Where od-id misses, `DiffSummary` over `UIVisualSignature`s emits a `FitnessSignal` that **proposes** an identity edge → **human confirms** (`confidence=1.0` only on confirm, A4). Never auto-binds.

## 5. The components page falls out for free

Once `UIIdentityIndex` exists, the **components page is a read-model projection** of it (node A4) — render the identities + their instances + DNA. No parallel catalog, no drift. This is the honest answer to "then we could have a page for components": the page is the cheap projection; the index is the architecture.

## 6. Convergence into the final design

This artifact is the `GAP-COMPONENT-REGISTRY-002` closure to merge into `SYNTHESIZED-DEEP-DESIGN.md §2.4` (moving R-1 from RESIDUE → specified) and to seed the `BLK-IDENTITY-TYPES-002` `models.ts` types. It does **not** rewrite the deep-spec here — it stages the delta for the final-design merge.

## 7. Residue / deferred (named)

- **A2** implement `UIIdentityIndex` + the types in `models.ts` (gated; needs L4 build).
- **Phase-2 similarity matching** (after phase-1 proves out).
- **resonant license/provenance** `bounded-research` — only if vendoring beyond names-only is ever wanted.
- **`GAP-CONFLICT-ALGEBRA-003`** (R-2) is *adjacent* but out of this node's scope.
