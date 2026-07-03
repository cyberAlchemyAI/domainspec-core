---
module: architecture-pattern-enforcement
feature_code: APE
version: current
status: draft
updatedAt: 2026-07-02
docType: implementation-layering
---

# Implementation Layering: Architecture-Pattern Enforcement

Decision-first layering. L0 minimal; scope promotes only when evidence justifies it. The layer
boundaries are chosen so the **node plane** (owned, stable) leads and the **edge plane**
(now unblocked by R3A, still not implemented here) follows — the design's load-bearing split.

## Target And Scope

- Target: architecture-pattern-enforcement (APE)
- Scope: system (a cross-cutting validation discipline + its tooling)
- Current state: brownfield — substrate owned and installed; L0 is witnessed on the financial-settlement
  feature pack; L1 repeatability and dynamic edge-law enforcement remain.

## Layer Boundary Rule

`After this layer, we know whether {decision unlocked}.`

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| **L0 (POC)** | After this layer, we know whether the **spec→validate→enforce loop runs non-vacuously on one real domain**. | one hand-authored v2 feature pack (SPEC + aspect docs) that passes `validate-content` + `instances validate` + engine `lint`, and **fails on a deliberately broken concept**. | C-A uniformity on ONE feature pack; engine `lint` via explicit path; a red/green demonstration. | C-B edges, C-C layering, CI wiring, card triage, promotion, mint, drift. | green + red run transcripts committed under the feature pack; the validators are now *witnessed*, not vacuous. | continue → L1 · pivot if the schema criteria can't express a real domain. |
| **L1 (repeatable)** | After this layer, we know whether **uniformity enforcement is repeatable and the authoring layer is in place**. | node-plane gates wired into CI over ≥2 feature packs; v1 pattern-library triaged in as the card layer. | C-D card-layer triage (concept + relationship cards + IMPORT-MANIFEST rows); node gates in CI; **defect cleanup** (reset `code-tag-waivers.yaml`; fix `docs/features`→`spec/features` anchors). | edge-law binding, cav2 promotion, unconstructibility, cross-project. | 2nd feature pack green; CI blocks on a seeded violation; concept cards linked as Evidence for backend meta-type promotions. | harden → L2 · narrow if card triage balloons. |
| **L2 (governed)** | After this layer, we know whether **the edge plane and authority promotion hold**. | edge-law (composability) enforced from R3A root DS-D8 authority; node meta-types + validators promoted candidate→binding via cav2. | C-B composability (post-R3A): endpoint-signature checks; refactor `check-code-tag-composability` to read the edge-law dynamically; C-E promotion of L0/L1 handles through definitions/constitution-governance. | C-C unconstructibility, C-F mint, C-G drift-trend. | R3A landed + composability green on a real pack; ≥1 handle reaches `binding` state. | scale → L3 · remediate if DS-D8 endpoint signatures force schema changes. |
| **L3 (scale / package)** | After this layer, we know whether **the discipline replicates to another project and becomes unconstructible-by-construction**. | a second (minted) repo inherits the substrate and validates its own domain; C6 typed-catalog layer; C7 drift baseline series. | C-F inheritance via mint; C-C unconstructibility (typed catalog generalizing `containment.ts`); C-G drift baseline. | future domain classes; public/private mint boundary (blocked). | minted repo runs the same gates green on its own nodes; a forbidden edge is unbuildable, not flagged; drift series shows a trend. | pilot/package · defer unconstructibility if the meta-type formalism is still moving. |

## Non-Regression Guardrails

- Later layers preserve earlier guarantees: L2 edge checks must not weaken L0/L1 node checks.
- Deferred scope stays explicit — do **not** pull C-B/C-C/C-F forward into L0/L1 to look complete.
- Promotion decisions cite evidence, not preference (cav2 CAV2-D38, claim ≤ proof).
- The node plane must remain independently shippable while edge-plane enforcement is pending.

## Recommended Next Layer

- Next layer: **L1**
- Key decision unlocked: can the witnessed validator stack repeat across another pack, with card evidence and CI gating?
- Major deferred scope: the edge plane (C-B/C-C), promotion (C-E), and cross-project (C-F) — no longer gated on R3, but still gated on L1 repeatability, dynamic DS-D8 enforcement, and later formalism.
