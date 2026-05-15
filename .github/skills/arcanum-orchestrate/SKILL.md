---
name: arcanum-orchestrate
description: Route Arcanum requests to the canonical sigil and spell registry from the workspace root.
argument-hint: "<natural-language-arcanum-request>"
allowed-tools: Read, Glob, Grep, AskQuestions, Task
---

# Arcanum Orchestrate

<objective>
Route a user request to the appropriate Arcanum sigil or spell by reading the canonical Arcanum registry in this workspace and following the selected artifact's instructions.
</objective>

<context>
The Arcanum repository lives at `arcanum/` in this workspace. Read `arcanum/registry/SIGILS.md`, `arcanum/registry/SPELLS.md`, `arcanum/registry/PACKS.md`, and relevant canonical files under `arcanum/formulae/`, `arcanum/transmutations/`, `arcanum/arcana/`, and `arcanum/spells/`.
</context>

<routing>
- install sigils into agent runtimes -> `arcanum/arcana/sigil-runtime-installer/SKILL.md`
- create, revise, observe, or reflect on a sigil -> `arcanum/arcana/sigil-development/SKILL.md`
- convert a coherent skill or workflow into a sigil -> `arcanum/arcana/skill-transcriptor/SKILL.md`
- decompose a broad or tangled source into a sigil candidate -> `arcanum/arcana/skill-decomposer/SKILL.md`
- compose multiple sigils into a workflow -> `arcanum/arcana/spellcraft/SKILL.md`
- setup repository-local telemetry -> `arcanum/formulae/observability-setup/SKILL.md`
- build compact task context -> `arcanum/transmutations/context-builder/SKILL.md`
- map repository architecture -> `arcanum/arcana/architecture-pattern-inventory/SKILL.md`
- govern vault-like knowledge -> `arcanum/arcana/ontology-vault/SKILL.md`
- route unknown requests -> read `arcanum/registry/SIGILS.md` and `arcanum/registry/SPELLS.md`, then ask one focused clarification if needed.
</routing>

<process>
1. Read the Arcanum registry files under `arcanum/registry/`.
2. Classify the request as sigil usage, spell usage, install/setup, authoring, validation, or help.
3. Select one canonical sigil or spell. If multiple routes are plausible, ask one focused clarification.
4. Read the selected artifact's `README.md` and `SKILL.md`, or the selected spell file.
5. Follow the selected artifact's process and preserve its Quality Bar, Anti-Patterns, output contract, and validation gates.
6. Return the selected route, files used, validation result, and next action.
</process>

<guardrails>
- Keep this skill as a thin runtime adapter.
- Do not copy full sigil internals into this wrapper.
- Treat `arcanum/registry/` and canonical Arcanum sigil files as authoritative.
- Do not install runtime adapters unless the user selects a target runtime or asks for a specific target.
</guardrails>
