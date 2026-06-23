# Arcanum Journey — Design / Architecture

> Invoke **design** artifact. Converts the approved [SPEC.md](./SPEC.md) into a
> governed architecture. Honors closed decisions DEC-AJ-HOME/PACKAGE/ROUTING/SURFACE.

## 1. Context View (stakes & boundary)

- **Learner:** someone who may not know software or AI. Needs analogies, simplicity,
  a Veritasium-style explainer.
- **Surface:** a standalone, downloadable skill package. On run it offers to install
  Arcanum (whole repo or a picked slice) and teaches while installing.
- **Boundary:** ships in **public arcanum**. Zero private data. Composes existing
  capabilities; owns only curriculum + routing + preset + capstone wiring.

## 2. Component View

| Component | Responsibility | Composes |
| --- | --- | --- |
| `journey-skill` (entry) | Orchestrate onboarding → chapter loop → capstone | all below |
| `onboarder` | Goal interview + first-tool recommendation + map fallback | `interrogation` |
| `installer-bridge` | Install whole repo or a picked slice as lessons proceed | `arcanum-bootstrap` |
| `chapter-engine` | Sequence chapters; load authored content; track progress | route map, preset |
| `surface-renderer` | Produce per-chapter agent-generated HTML | `x-ray` |
| `preset-engine` | Apply explanation style; load neutral default; accept user tweaks | `goal/decision-profile.schema` pattern |
| `path-recommender` | After each chapter, offer coherent next chapters | route map |
| `tower-capstone` | Build the learner's own first tower | `research-tower` → `reading-learning-package` |
| `route-map` (data) | Nodes = sigils/spells; typed edges | inventory output |

## 3. Curriculum View — draft chapter arc (provisional)

> **GAP-AJ-CHAPTER-ORDER-001:** this arc is a *draft skeleton*. Final ordering is
> fixed only after GAP-AJ-SIGIL-MAP-001 produces the full inherit/build-on/
> integrate graph via the dispatch-spec fan-out + inventory.

| # | Chapter (tool) | Inherits from | Lets you build | Integrates with |
| --- | --- | --- | --- | --- |
| 0 | **What is Arcanum / Cyber Alchemy** (framing) | — | a mental model: Arcana / sigils / spells tiers | everything |
| 1 | **Craft** — the control surface | Ch0 | a durable project ledger | every later chapter returns here |
| 2 | **Refine** — vague idea → seed | Craft | a refined seed/design | feeds Invoke |
| 3 | **Invoke** — intent → define/design/plan | Refine | governed authoring artifacts | feeds task-session/spellcraft |
| 4a | **Whisper** (creative branch) | Invoke intent substrate | written artifacts, no code needed | research-tower |
| 4b | **Task-Session** (automation branch) | Invoke plan | one bounded executed unit | goal spell |
| 4c | **Inventory** (knowledge branch) | Craft | durable reusable knowledge | research-tower |
| 5 | **Goal spell** | Craft + task-session | an autonomous fail-closed work loop | decision-gate |
| 6 | **Dispatch-Spec** | Invoke | validated multi-sigil routes | research/review/experiment |
| 7 | **Decision-Gate** | Craft | resolved blocking decisions | goal, invoke |
| 8 | **X-Ray** | any artifact | a visual HTML explanation | the journey's own surfaces (self-referential) |
| 9 (capstone) | **Research-Tower → Reading-Learning-Package** | Inventory + Whisper | **the learner's own first tower** | the whole journey |

Branch selection at Ch4 follows the learner's interrogated goal; non-chosen
branches remain offered by the path-recommender.

## 4. Routing View (DEC-AJ-ROUTING-001)

```text
/interrogation (one question at a time) -> primary_goal in {creative, automation, knowledge, unsure}
  creative   -> recommend Whisper (Ch4a)
  automation -> recommend Craft+Task-Session/Goal (Ch1->4b->5)
  knowledge  -> recommend Inventory+Research-Tower (Ch4c->9)
  unsure     -> recommend Ch0->Ch1 (framing + Craft)
-> ALWAYS show full route-map; learner may override or probe any node
```

## 5. Preset View (GAP-AJ-PRESET-SCHEMA-001)

A public schema + neutral default, mirroring `goal/decision-profile.schema`
(public shape, no filled private data). Draft shape:

```yaml
profile: { id: neutral-default, version, mode: neutral-default | custom }
explanation:
  audience: novice            # novice | practitioner
  analogy_density: high       # low | medium | high
  simplicity: high            # plain language, short sentences
  style: veritasium           # curiosity-hook -> intuition -> mechanism -> recap
  persona_ref: anonymized-explainer   # from anonymized pool (GAP-AJ-PERSONA-001)
pacing: { one_concept_at_a_time: true, probe_prompts: true }
surface: { html: true, generator: x-ray }
language_tweaks: []           # user-supplied vocabulary so it speaks their language
```

- **Neutral default** ships in the public package; the learner's tweaks
  (`language_tweaks`, `audience`) are runtime/local, never committed to public.
- Persona is **anonymized** (GAP-AJ-PERSONA-001): copy the explainer *role-fit*
  from `agent-pool.yaml` without person names.

## 6. Surface View (DEC-AJ-SURFACE-001)

- Each chapter renders an **agent-generated HTML** page via `x-ray`, consistent
  with existing `arcanum/development/user-guide/*.html`.
- Standalone download → `arcanum-bootstrap` installs (whole or slice) → chapters
  teach while installing → learner probes live tools.

## 7. Decisions consumed (not reopened)

| Decision | Encoded as |
| --- | --- |
| DEC-AJ-HOME-001 (public) | §1 boundary, public-only authoring, anonymized persona |
| DEC-AJ-PACKAGE-MODE-001 (hybrid) | §3 authored chapters + §3/9 runtime capstone tower |
| DEC-AJ-ROUTING-001 (interrogate-then-pick) | §4 routing view |
| DEC-AJ-SURFACE-001 (install+HTML) | §6 surface view |

## 8. Glossary Consistency

Terms match [SPEC.md](./SPEC.md) Concept Registry: Chapter, LearningPreset,
RouteMap, StartingPoint, ExplanationSurface. No conflicting redefinitions. New
design terms (installer-bridge, path-recommender, tower-capstone) are component
names, not domain concepts — no registry collision. **Status: pass.**

## 9. Design gaps → plan

- GAP-AJ-SIGIL-MAP-001 (blocks final chapter order) — **highest leverage**; do first.
- GAP-AJ-PRESET-SCHEMA-001 — draft above; harden into a public schema file.
- GAP-AJ-PERSONA-001 — anonymize explainer persona.
- GAP-AJ-CYBERALCHEMY-001 — gather public-level Cyber Alchemy content for Ch0.
- GAP-AJ-CHAPTER-ORDER-001 — finalize after the map.
