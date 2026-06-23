---
module: arcanum-journey
version: current
status: draft
updatedAt: 2026-06-22
docType: implementation-layering
---

# Implementation Layering: Arcanum Journey

## Target And Scope

- Target: arcanum-journey (public arcanum learning skill)
- Scope: workflow + product (curriculum, routing, install, capstone)
- Current state: greenfield (durable definition + design only)

## Layer Boundary Rule

`After this layer, we know whether {decision unlocked}.`

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| **L0 (POC)** | After this layer, we know whether **teach-while-install works at all** — can a skill install one slice and teach one chapter with an HTML surface? | Onboard → install Craft slice → teach **Chapter 1 (Craft)** → render one `x-ray` HTML page → one probe prompt | 1 chapter, 1 goal path, hardcoded preset default, manual map | routing breadth, full arc, tower, public packaging | a runnable single-chapter demo + 1 HTML page a novice can follow | continue / pivot / stop |
| **L1** | After this layer, we know whether the **curriculum is repeatable** across goals and chapters. | Sigil map (draft) + draft chapter arc (Ch0–9) + `/interrogation` routing + neutral preset + path-recommender | 4 branch paths, all chapters authored, preset default | user tweaks, anonymized persona, capstone tower, boundary hardening | learner can complete any branch and get coherent next-path offers | harden / narrow / stop |
| **L2** | After this layer, we know whether **the public boundary holds and a real learner tower is produced**. | Public-boundary lint (no private data) + preset user-tweak + anonymized persona + capstone `research-tower`→`reading-learning-package` | boundary enforcement, capstone, preset tweak, persona | scale, whole-repo install, registry promotion | passing boundary lint + a sample learner tower in the learner's own language | scale / remediate / stop |
| **L3** | After this layer, we know whether the **standalone public package is shippable**. | Standalone downloadable package + whole-repo install path + experiment-harness validation + spellcraft/registry promotion | packaging, whole-repo install, validation evidence, promotion | future chapters for new sigils | experiment-harness pass + spellcraft validation + registry-ready | pilot / package / defer |

## Non Regression Guardrails

- L0→L3 never weakens the public/private boundary (DEC-AJ-HOME-001). Boundary lint
  is added at L2 and must keep passing through L3.
- Authored chapters (L1) must not be replaced by runtime generation; the tower is
  capstone-only (DEC-AJ-PACKAGE-MODE-001).
- Promotion to public arcanum requires experiment-harness evidence (mirrors the
  goal spell's promotion gate).

## Prerequisite (cross-layer input)

GAP-AJ-SIGIL-MAP-001 is the spine. The sigil/spell route map is produced by the
named downstream routes — **dispatch-spec fan-out → inventory** — and feeds chapter
ordering (GAP-AJ-CHAPTER-ORDER-001). This is planned as Wave 0; the journey cannot
finalize its arc without it.
