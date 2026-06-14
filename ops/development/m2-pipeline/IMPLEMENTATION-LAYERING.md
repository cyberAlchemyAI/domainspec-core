---
module: m2-pipeline
version: current
status: draft
updatedAt: 2026-06-14
docType: implementation-layering
---

# Implementation Layering: M2 Pipeline

## Layer Boundary Rule
`After this layer, we know whether {decision unlocked}.`

## Layer Decision Table
| Layer | Decision Question | Minimum Working Unit | Capabilities | Exit Evidence | Promotion |
| --- | --- | --- | --- | --- | --- |
| **L0** | After this layer, we know whether the frozen spec contract is *consumable* and the cleanest wedge ships. | C1 sync-registry reads the Concept Registry and aggregates a typed registry; C2 code-tag toolchain ships as a sigil. | C1, C2 | sync-registry produces a registry+edges from a real SPEC; code-tag suite green on a real repo. | continue / pivot |
| **L1** | After this layer, we know whether deterministic derivation from aspect docs works. | C3 derives ≥1 obligation type end-to-end (aspect clause → content-addressed TEST-SPEC row) with a round-trip oracle; C4 derives metric obligations from the same docs. | C3, C4 | one feature's aspect docs → byte-stable TEST-SPEC + metric-obligation inventory; round-trip PASS. | expand cardinalities / narrow |
| **L2** | After this layer, we know whether spec-driven coverage + audit close the loop. | C5 emits STORIES + coverage matrix flagging unmapped concepts; C6 classifies spec-vs-code compliant/partial/missing/extra. | C5, C6 | stories↔concepts coverage matrix; an alignment report on a real feature. | scale / remediate |
| **L3** | After this layer, we know whether the M2 sigils are promotion-ready. | validation suites + worked examples + R-IB framing for all 6. | all | each sigil passes its validation examples; public docs carry R-IB-1/3. | promote / defer |

## Non-Regression Guardrails
- Freeze the M1 aspect/registry contract before L1 (C3/C4/C5 depend on it).
- C3 stays deterministic + fresh-built (B3); no DS engine code crosses.
- C6 stays decoupled from the governance chain (no moat import).
- Promotion cites validation evidence, not preference.
