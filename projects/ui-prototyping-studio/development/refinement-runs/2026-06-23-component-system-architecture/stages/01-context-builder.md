# Stage 01 — Context Builder evidence baseline

- Capability: `context-builder` · Mode: `standard` · Receipt: parent coordinator · Status: **pass**

## The component-system architecture as it stands (design-time)

**Designed (deep-spec, not yet code):**
- **`UIElementIdentity`** — the stable concept node ("primary button", "filter chip"). Recognition-over-recall is its *design goal*.
- **`UIElementInstance`** — a versioned realization of an identity within a `PrototypeVariant`.
- **`UIIdentityRelationType`** — the typed version edge: `replaced-by` / `reshaped` / `same-concept` / `new` / `split-from` / `merged-into`.
- **`TypedReference`** — indexes `UIElementInstance` → `UIElementIdentity` (and proof evidence).
- **24 `UIVisualSignature` DNA enums** — the visual genome; value sets fixed; **no raw values** allowed (shape-only proof obligation).
- **`DiffSummary`** — the conformance-delta: ordered per-field deltas over two `UIVisualSignature`s, each `{dimension, fromValue, toValue, preference, confidence}`, surfaced as `FitnessSignal(source=governance)`.
- **`PrototypeGenome`** — folds positive (`constrain`-locked) and negative (`reject`) constraints into the next `GenerateVariants`.

**Built (code, L0):** the 10-state session machine, governance gates, the `data-od-id` component model, the honest per-component diff (`canonicalize.ts`). The identity/DNA/registry layer above is **designed, deferred, not implemented**.

## The load-bearing gap (Q4 RESIDUE)

§2.4 is explicit: the typed edges land, but **the registry persistence/index entity itself is unspecified** — "how identities are stored, queried, and matched across sessions and `BaselineGenealogyFamily` lineages." A components page (or per-element composition) **cannot enumerate components without this entity.** This is the architecture's open center.

## The external source (resonant)

s1 research mapped **resonant-os-design-tokens onto the 24 DNA enums** as `external_context`, **gate g1 (no canonical promotion)**. Residue R-7: the DNA enums are *underfilled* (Motion/Interaction/State/Feedback/Numeric pending); resonant tokens are a candidate fill source. **resonant is NOT vendored** (only voltagent MIT + nexu-io Apache-2.0 are).

## Constraints the architecture must honor

- Express in the **existing** domainspec UI vocabulary (deep-spec: no new entity names; deepen via additive enum states / field specs).
- **No raw values** in `UIVisualSignature` (proof obligation; shape-only).
- External tokens stay `external_context`; **never auto-promote to canonical** (gate g1).
- `confidence=1.0` only when both ends resolve to a confirmed enum/token (D-S2 honesty).

## Frame → Define

The architecture question is: **what is the registry entity (Q4) that stores/queries/matches `UIElementIdentity`, and where do its DNA values come from — owned, resonant-external, or hybrid?**
