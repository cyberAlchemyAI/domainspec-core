---
name: arcanum-journey
description: A standalone, downloadable learning course that teaches what Arcanum is by constructing it piece by piece — each sigil/spell is a chapter. It interrogates your goal, installs Arcanum (whole repo or a picked slice) while it teaches, renders each chapter as an HTML page, and ends by helping you build your own first research tower. Use when someone new wants to learn Arcanum hands-on, or wants to install it and be guided through what each tool does.
status: scaffold (L0 POC) — staged in the private parent; promotion to public arcanum is separately approved
---

# Arcanum Journey

> **Scaffold note.** This is the L0 proof-of-concept skill contract authored in the
> private-parent staging area. Decisions are locked (see the project DECISIONS.md):
> public home, hybrid chapters + runtime tower, interrogate-then-pick routing,
> standalone install-and-teach surface with agent-generated HTML.

## What this skill does

Teaches Arcanum by **building it up one chapter at a time**, while installing it, so
the learner can probe real tools as they learn.

## Flow

1. **Onboard (interrogate).** Ask the learner's primary goal (creative / automation /
   knowledge / unsure) — one question at a time. Config: [onboard/routing.yaml](onboard/routing.yaml).
   Composes `arcana/structured-interview-kits`.
2. **Install while teaching.** Offer to install Arcanum — the whole repo or just the
   slice the recommended path needs. Composes `spells/arcanum-bootstrap`.
3. **Chapter loop.** Teach one sigil/spell per chapter ([chapters/](chapters/)), in the
   order fixed by the route map. Each chapter:
   - applies the [learning preset](preset/learning-preset.schema.json) + the
     [anonymized explainer persona](preset/persona-explainer.md);
   - renders an HTML explanation surface ([surfaces/](surfaces/)) via `arcana/x-ray`;
   - ends with a hands-on probe against the real installed tool;
   - offers coherent next chapters (path-recommender, from the route-map edges).
4. **Capstone.** Help the learner produce **their own first research tower** in their
   own language. Composes `arcana/research-tower` → `spells/reading-learning-package`.
   *(Runtime per-learner step — not pre-authored.)*

## Composes (does not own)

`structured-interview-kits`, `arcanum-bootstrap`, `x-ray`, `craft`, `research-tower`,
`reading-learning-package`, plus every sigil/spell it teaches. Contracts are
referenced, never forked.

## Guardrails

- **Public boundary:** ships into public arcanum; no private data. Enforced by
  [lint/boundary-lint.py](lint/boundary-lint.py).
- **Persona is anonymized** (no real names).
- **Cyber Alchemy** is taught only at the level already public in arcanum
  (`framework/CYBERALCHEMY-METHOD.md`).

## Status / build state

| Piece | State |
| --- | --- |
| Route map (all sigils/spells, edges) | ✅ built |
| Onboarder routing | ✅ |
| Learning preset schema + neutral default | ✅ |
| Anonymized explainer persona | ✅ |
| Boundary lint | ✅ |
| Chapters 0–1 (exemplars) + template + outline | ✅ |
| Ch1 HTML surface (POC) | ✅ |
| Chapters 2–9 authoring | ⏳ Wave 1 |
| Install-while-teaching runtime wiring | ⏳ needs arcanum-bootstrap integration |
| Capstone tower run | ⏳ runtime, per-learner |
| Experiment-harness validation + promotion | ⏳ Wave 3 |
