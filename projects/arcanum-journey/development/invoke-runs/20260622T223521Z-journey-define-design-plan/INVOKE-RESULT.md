## Invoke Result

- Mode: define → design → plan (composed)
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: flag
- Mode contract: define.md, design.md, plan.md
- Outputs:
  - define: [SPEC.md](./SPEC.md)
  - design: [ARCHITECTURE.md](./ARCHITECTURE.md)
  - plan: [IMPLEMENTATION-LAYERING.md](./IMPLEMENTATION-LAYERING.md), [WORK-PACK.md](./WORK-PACK.md)
- Design views: context, component, curriculum (draft arc), routing, preset, surface, glossary-consistency — covered
- Glossary consistency: pass (Concept Registry consistent; component names introduce no domain-term collision)
- Dispatch techniques: see trace below; no full dispatch JSON required (single-owner authoring, no protected mutation, no subagent delegation in this run)
- Distill validation: flag (gaps named with owners below)
- Implementation layering: [IMPLEMENTATION-LAYERING.md](./IMPLEMENTATION-LAYERING.md) (L0–L3 with promotion decisions)
- Work-pack: [WORK-PACK.md](./WORK-PACK.md) (split, W0–W3)
- Complexity: high
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task-level SWUs with write scope, done criteria, validation, exec owner — complete at planning altitude; execution-pack deferred to task-session
- Smallest working units: complete (SWU manifest with 10 SWUs, write scope + done + validation + owner)
- Refresh: n/a
- Target artifact: arcanum-journey (public arcanum learning skill; owner = spellcraft lifecycle once authoring begins)
- Template or recipe selection: domainspec-spec (SPEC), architecture (design), implementation-layering + work-pack (plan)
- Decisions: all four scoping decisions consumed from DECISIONS.md, not reopened
- Unresolved gaps:
  - invoke gaps: none (authoring complete at plan altitude)
  - target-artifact gaps: GAP-AJ-SIGIL-MAP-001 (blocks chapter order; Wave 0), GAP-AJ-PRESET-SCHEMA-001 (drafted, harden in W1), GAP-AJ-PERSONA-001 (W2), GAP-AJ-CYBERALCHEMY-001 (W0 public-level), GAP-AJ-CHAPTER-ORDER-001 (finalize after map)
- Next route: task-session (execute W0 S-000 / SWU-AJ-MAP-1 via dispatch-spec fan-out → inventory); spellcraft owns later spell/skill lifecycle

## Dispatch Technique Trace

| Technique | Activation trigger | Affected phase/artifact | Validation expectation |
| --- | --- | --- | --- |
| `sequence` | Multi-stage build with ordered waves | WORK-PACK waves W0→W3 | Each wave gates the next; W0 map before chapters |
| `frame_handoff` | Plan prepares downstream execution | WORK-PACK "Next Move" → task-session/dispatch-spec | Named handle, expected receipt, write scope present |
| `owner_boundary_check` | Journey composes but must not own composed sigils | SPEC §Constraints, ARCHITECTURE §2 | No forking/mutating composed contracts |
| `authority_split_gate` | Public/private boundary is load-bearing | LAYERING guardrails, WORK-PACK GATE-AJ-BOUNDARY | Boundary lint (S-006) added L2, holds through L3 |
| `residue_ledger` | Five gaps carried, not resolved here | SPEC/ARCHITECTURE gap tables, ledger | Each gap has owner route + wave |

Skipped (considered, rejected): `recomposition_proof` (no child-context recompose in
this authoring run); full dispatch JSON (no protected mutation, no subagent strategy,
no reusable route artifact produced this run).

## Distill Validation

- **Small enough to execute?** Yes — W0 reduces to SWU-AJ-MAP-1 (a bounded fan-out)
  then SWU-AJ-POC-1 (one chapter). Not a monolith.
- **Large enough to preserve meaning?** Yes — the POC proves the whole thesis
  (teach-while-install + HTML surface) on one chapter.
- **Recomposes into the design?** Yes — waves map 1:1 to layers L0–L3 and to the
  SPEC capabilities.
- **Hidden gaps exposed?** Yes — the sigil map is correctly surfaced as a *prerequisite*
  (Wave 0), not assumed.
- **Overbuilt/vague?** Flag: chapter content (S-002) and the preset schema (S-004)
  are placeholders until the map and persona land; their SWUs name owners and gates,
  so they route as flag, not block.

**Verdict: flag** — routes to task-session because every Distill gap has a named
owner and repair path (the gap table). Not block: nothing mutation-critical is
unresolved at planning altitude.
