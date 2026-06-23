---
module: arcanum-journey
version: current
status: draft
updatedAt: 2026-06-22
docType: work-pack
---

# WORK-PACK: arcanum-journey

## Purpose

Canonical executable plan for building the Arcanum Journey learning skill, derived
from [SPEC.md](./SPEC.md), [ARCHITECTURE.md](./ARCHITECTURE.md), and
[IMPLEMENTATION-LAYERING.md](./IMPLEMENTATION-LAYERING.md). Source of truth for the
Craft ledger at `projects/arcanum-journey/.craft/`.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block | Wave 0 (sigil map) must complete before chapter authoring is execution-ready. |
| complexity | high | Multi-capability composition, public boundary, runtime capstone. |
| outputMode | split | Waves W0–W3 map to layers L0–L3. |
| executionPackRef | n/a (to be authored at task-session time) | |
| layeringArtifactRef | ./IMPLEMENTATION-LAYERING.md | |
| dispatchTechniqueTrace | see INVOKE-RESULT.md §Dispatch Technique Trace | sequence, frame_handoff, owner_boundary_check, authority_split_gate, residue_ledger |
| distillValidationStatus | flag | Gaps named with owners below; see INVOKE-RESULT.md §Distill. |
| activeLayerWindow | L0 | First executable slice = single-chapter POC after the map. |
| lastUpdatedAt | 2026-06-22T22:35:21Z | |
| readinessProfile | pilot | First public pilot of the journey. |

## Objective Summary

- **Objective:** ship a public arcanum standalone skill that teaches Arcanum chapter
  by chapter while installing it, routes learners by goal, and ends with the learner
  building their own first research tower.
- **Primary inputs:** approved SPEC/ARCHITECTURE/LAYERING; the Craft ledger; the
  five open gaps.
- **Success condition:** a novice completes a branch, gets coherent next-path offers,
  stays inside the public boundary, and produces a tower in their own language —
  validated by experiment-harness before promotion.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-000 | Sigil/spell route map with inherit/build-on/integrate edges | L0-input | W0 | — | map covers every installed sigil+spell; edges typed |
| S-001 | Single-chapter POC (Craft) install+teach+HTML | L0 | W0 | S-000 | novice runs it end to end; 1 HTML page |
| S-002 | Draft chapter arc Ch0–9 authored + finalized order | L1 | W1 | S-000 | every chapter declares inherits/builds/integrates |
| S-003 | `/interrogation` goal routing + full-map fallback | L1 | W1 | S-000 | each goal yields a recommended first tool + override |
| S-004 | Learning preset public schema + neutral default | L1 | W1 | — | schema validates; default present; no private data |
| S-005 | Path-recommender (next-chapter offers) | L1 | W1 | S-000, S-002 | offers are reachable map edges |
| S-006 | Public-boundary lint (no private data leak) | L2 | W2 | S-002 | lint flags any private path/persona-name |
| S-007 | Anonymized explainer persona | L2 | W2 | S-004 | persona has no person names |
| S-008 | Preset user-tweak (local, uncommitted) | L2 | W2 | S-004 | tweaks load at runtime, never committed public |
| S-009 | Capstone: research-tower → reading-learning-package | L2 | W2 | S-002 | sample learner tower produced |
| S-010 | Standalone package + whole-repo install path | L3 | W3 | S-001..S-009 | downloadable; installs whole or slice |
| S-011 | Experiment-harness validation + promotion readiness | L3 | W3 | S-010 | harness pass; spellcraft validate; registry-ready |

## SWU Manifest (Smallest Working Units)

| SWU | Parent Slice | Write Scope | Done Criteria | Validation | Exec Owner |
| --- | --- | --- | --- | --- | --- |
| SWU-AJ-MAP-1 | S-000 | private parent map artifact | dispatch-spec fan-out gathers every sigil/spell + Cyber Alchemy (public-level) | route shapes validate | dispatch-spec → research |
| SWU-AJ-MAP-2 | S-000 | inventory entries | findings made durable as inventory; edges tagged | inventory lint pass | inventory |
| SWU-AJ-POC-1 | S-001 | journey-skill stub | onboard→install Craft slice→teach Ch1→1 x-ray HTML | manual run by a novice proxy | task-session |
| SWU-AJ-ARC-1 | S-002 | chapter content files | Ch0–9 authored; order fixed against map | each chapter peer-readable | task-session |
| SWU-AJ-ROUTE-1 | S-003 | onboarder config | interrogation script + goal→tool table | dry-run each goal | task-session |
| SWU-AJ-PRESET-1 | S-004 | preset schema file | public JSON-schema + neutral default (goal-profile pattern) | schema self-validates | task-session |
| SWU-AJ-PERSONA-1 | S-007 | persona ref | anonymized explainer extracted from agent-pool | no person names present | task-session |
| SWU-AJ-BOUNDARY-1 | S-006 | lint script | fails on private path/name in public package | run against draft package | task-session |
| SWU-AJ-CAP-1 | S-009 | capstone wiring | research-tower→reading-learning-package run on a sample | sample tower exists | task-session |
| SWU-AJ-PROMO-1 | S-011 | experiment-harness fixtures | harness validates reusable behavior | harness pass | experiment-harness → spellcraft |

## Waves

- **W0 (L0):** S-000 (map) → S-001 (POC). *Gate: map complete before POC; POC proves
  teach-while-install.*
- **W1 (L1):** S-002–S-005. *Gate: full arc + routing + preset + offers repeatable.*
- **W2 (L2):** S-006–S-009. *Gate: boundary lint passes; capstone tower produced.*
- **W3 (L3):** S-010–S-011. *Gate: experiment-harness pass; promotion-ready.*

## Blockers & Gates

| ID | Blocker | Resolution path |
| --- | --- | --- |
| BLK-AJ-MAP | Chapter order can't finalize without the sigil map | Run W0 S-000 first (dispatch-spec + inventory) |
| GATE-AJ-BOUNDARY | No private data may ship public | S-006 lint must pass through W2–W3 |
| GATE-AJ-PROMOTION | Public promotion needs reusable-behavior evidence | S-011 experiment-harness, then spellcraft validate |

## Validation Strategy

Every slice carries a validation column above. Cross-cutting: boundary lint (W2+),
experiment-harness + spellcraft validate (W3). The journey reuses the goal spell's
promotion discipline (harness evidence before registry).

## Current State / Next Move

W0 is the entry. The next executable step is **S-000 / SWU-AJ-MAP-1** — the
dispatch-spec fan-out exploration (with Cyber Alchemy at public level) feeding the
inventory. This matches the downstream route already recorded in the ledger.
