# Stage 02 — Invoke Define

- Capability: `invoke` · Mode: `define` · Receipt: parent coordinator · Status: **pass**

## Problem definition

The studio has a **designed but unbuilt** component vocabulary (identity / instance / typed-version-edge / 24 DNA enums / conformance-delta) whose **registry persistence/index entity is unspecified (Q4 residue)**. The operator asked whether resonant-os-design-system was vendored (it wasn't) and reframed to: **the component-system architecture is what matters**. So the unit to refine is the **component registry architecture + its DNA source**.

## The unit being refined

`ComponentRegistry = { store UIElementIdentity, version via UIIdentityRelationType, index via TypedReference, carry 24-enum UIVisualSignature DNA, compute DiffSummary conformance, source DNA values (owned | external | hybrid) }`.

## Invariants that must survive

- **A1** Express in existing domainspec UI vocabulary; no new entity names (deepen, don't invent).
- **A2** No raw values in `UIVisualSignature` (shape-only proof obligation).
- **A3** External tokens (resonant) stay `external_context`; no canonical promotion (gate g1).
- **A4** `confidence` honesty (D-S2): `1.0` only when both ends resolve to a confirmed enum/token.
- **A5** Recognition-over-recall: the registry must let the human *recognize* reused components, not re-learn them.

## Architecture forks (resolve before Design — g05)

- **AF1 — Registry entity (Q4).** Where/how are identities stored, queried, matched across sessions? In-session map | durable per-repo registry file | derived index over the append-only event log.
- **AF2 — DNA source.** Owned (author the 24 enum values by hand) | external (resonant tokens) | hybrid (owned enums, resonant-mapped values as `external_context`).
- **AF3 — Components page relation.** Is the page a *read-model projection* of the registry, or a separate catalog? (Determines whether the page is free once the registry exists.)
- **AF4 — Matching.** How is a `UIElementInstance` matched to an existing `UIElementIdentity` (so reuse is detected)? `data-od-id` equality | DNA-signature similarity | human confirm.

## Done criteria

A plan that picks AF1–AF4, preserves A1–A5, closes/scopes Q4, and states the resonant decision honestly (vendor / external-map / defer).

## Residue for interrogation

- Does a durable registry violate "session-scoped" assumptions, or is cross-session identity exactly the point (recognition-over-recall)?
- Is resonant worth a vendoring/license cost, or do the existing vendored refs (voltagent/open-design) already cover the DNA fill?
