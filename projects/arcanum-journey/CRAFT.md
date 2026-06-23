# Arcanum Journey — Craft View

> Human-readable view of [`.craft/ledger.yml`](.craft/ledger.yml). The ledger is
> the source of truth; this file is a linked summary only. Source authority for
> the intent: [`vision-brief.md`](.craft/artifacts/vision-brief.md).

- **Ledger:** `projects/arcanum-journey/.craft/ledger.yml`
- **Scope:** a learning course that teaches Arcanum by constructing it piece by
  piece — each sigil/spell is a chapter; Craft is presented as the control
  surface. Surface area: a standalone downloadable skill that installs the repo
  and teaches while installing.
- **Stage:** define · **Gate:** flag (scoping decisions closed; design not yet run)

## Quick links

- **Next move:** Run `/invoke` to **define → design → plan** the journey as a **public
  arcanum spell/skill**, consuming this ledger + the vision brief + [DECISIONS.md](.craft/artifacts/DECISIONS.md).
- **Blocking decision:** none — all four scoping decisions resolved 2026-06-22.
- **Decisions (closed):** see [DECISIONS.md](.craft/artifacts/DECISIONS.md):
  HOME = public arcanum · PACKAGE = hybrid chapters+tower · ROUTING = interrogate-then-pick ·
  SURFACE = standalone install-and-teach + agent-generated HTML.
- **Active gaps:** [GAP-AJ-SIGIL-MAP-001](#gap-gap-aj-sigil-map-001),
  [GAP-AJ-PRESET-SCHEMA-001](#gap-gap-aj-preset-schema-001),
  [GAP-AJ-PERSONA-001](#gap-gap-aj-persona-001),
  [GAP-AJ-CYBERALCHEMY-001](#gap-gap-aj-cyberalchemy-001),
  [GAP-AJ-CHAPTER-ORDER-001](#gap-gap-aj-chapter-order-001)
- **Active blockers:** none

## Context

### <a id="context-ctx-aj-root"></a>CTX-AJ-ROOT — Arcanum Journey
Build a learning course that explains what Arcanum is by constructing it piece by
piece. Each sigil/spell is a chapter; the course shows how concepts **inherit**,
**build on**, and **integrate**, presenting **Craft as the control surface**. The
ledger lives in the **private parent** because the planning content references
private material (domainspec persona, Cyber Alchemy, user-guide); the
**deliverable's** public/private home is the open blocker
[DEC-AJ-HOME-001](#decision-dec-aj-home-001).

## Planned route (recorded, not executed)

Craft records these downstream sigil routes as the work graph; this `/craft` run
does **not** run them.

| Step | Owner capability | Purpose |
| --- | --- | --- |
| 1 | `/invoke` (define→design→plan) | Author the journey definition/design/plan; resolve [DEC-AJ-HOME-001](#decision-dec-aj-home-001). |
| 2 | `/dispatch-spec` fan-out | Explore max info: definitions, lifecycles, **Cyber Alchemy** method/framework. |
| 3 | `/inventory` | Make the findings durable and reusable. |
| 4 | `/research-tower` | Produce the user's first tower in their own language. |
| 5 | `spells/reading-learning-package` | Base tool: build the learning package from the tower. |
| 6 | `/refine` | Shape the installer-companion approach. |
| 7 | `/interrogation` | Understand the user's primary goal → starting-point routing. |

## Decisions (closed 2026-06-22, via /decision-gate)

| ID | Question | Selected |
| --- | --- | --- |
| <a id="decision-dec-aj-home-001"></a>DEC-AJ-HOME-001 | Deliverable home? | **public-arcanum-only** (guardrail: Cyber Alchemy taught only at the level already public in arcanum) |
| <a id="decision-dec-aj-package-mode-001"></a>DEC-AJ-PACKAGE-MODE-001 | Package mode? | **hybrid** authored chapters + runtime tower |
| <a id="decision-dec-aj-routing-001"></a>DEC-AJ-ROUTING-001 | Starting-point routing? | **interrogate, then let user pick** |
| <a id="decision-dec-aj-surface-001"></a>DEC-AJ-SURFACE-001 | Surface area? | **standalone install-and-teach skill + agent-generated HTML surfaces** |

## Gaps (active)

| ID | Severity | Summary | Owner route |
| --- | --- | --- | --- |
| <a id="gap-gap-aj-sigil-map-001"></a>GAP-AJ-SIGIL-MAP-001 | flag | Map all sigils/spells with inherit/build-on/integrate edges. | dispatch-spec + inventory |
| <a id="gap-gap-aj-preset-schema-001"></a>GAP-AJ-PRESET-SCHEMA-001 | flag | Define the user-tweakable learning preset schema. | invoke-design |
| <a id="gap-gap-aj-persona-001"></a>GAP-AJ-PERSONA-001 | info | Extract Veritasium-style explainer persona from the agent pool. | invoke-design |
| <a id="gap-gap-aj-cyberalchemy-001"></a>GAP-AJ-CYBERALCHEMY-001 | flag | Include Cyber Alchemy method/framework in the fan-out. | dispatch-spec |
| <a id="gap-gap-aj-chapter-order-001"></a>GAP-AJ-CHAPTER-ORDER-001 | flag | Define chapter sequence (depends on the sigil map). | invoke-design |

## Candidate definitions

- **DEF-AJ-JOURNEY-001** — Arcanum Journey: course/installer-companion teaching Arcanum piece by piece.
- **DEF-AJ-CHAPTER-001** — chapter: one sigil/spell introduced as a tutorial step.
- **DEF-AJ-LEARNING-PRESET-001** — learning preset: novice explanation config, neutral defaults, user-tweakable.
- **DEF-AJ-ROUTE-MAP-001** — sigil/spell route map: inherit/build-on/integrate edges powering path offers.
- **DEF-AJ-STARTING-POINT-001** — starting-point routing: goal → first tool (creative → Whisper; automation → Craft/goal/task-session).
- **DEF-AJ-CRAFT-CONTROL-SURFACE-001** — Craft as control surface; refine/invoke as entry capabilities.
- **DEF-AJ-TEACH-WHILE-INSTALL-001** — teach-while-install standalone skill.

> Candidate definitions are local; they do not become canonical until routed
> through `definitions-governance`.

## Enablers

- **ENA-AJ-READING-PKG-001** → `arcanum/spells/reading-learning-package/` (base tool).
- **ENA-AJ-GOAL-PROFILE-001** → `arcanum/spells/goal/decision-profile.schema` + user-guide (preset precedent).
- **ENA-AJ-PERSONA-SRC-001** → `implementation/domainspec/telemetry/agents/agent-pool.yaml` (persona source).

## Pending by node

- **projects/arcanum-journey** (CTX-AJ-ROOT, gate flag):
  - Blocking decision: none (DEC-AJ-HOME-001 closed → public arcanum).
  - Open decisions: none (all four closed).
  - Active gaps: sigil map, preset schema, persona, Cyber Alchemy inclusion, chapter order.
  - Active blockers: none.
  - Next move: run `/invoke` define → design → plan as a public arcanum spell/skill.
