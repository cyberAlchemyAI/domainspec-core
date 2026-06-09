# Lean Formalization Owner Handoff: Proof-Domain Skill And Agent Lane

Date: 2026-06-01
Source task: `SWU-AGENTARCH-010`
Status: handoff; no Lean-owned files edited

## Purpose

This handoff preserves the Lean formalization lane while the root
Claude/Codex architecture removes GitHub as a target runtime.

Root scope produced:

- `ops/development/skill-agent-canonical-map.json`
- `ops/development/CLAUDE-CODEX-SURFACE-DRIFT-REPORT.md`
- `ops/development/GITHUB-SURFACE-DELETION-CANDIDATES.md`

## Lean-Owned Surfaces

The Lean lane remains canonical under:

- `domainspec-lean-formalization/.agents/skills/*`
- `domainspec-lean-formalization/.agents/agent-prompts/*`
- `domainspec-lean-formalization/CLAUDE.md`

Root task-session did not edit any of those paths.

## Guardrails To Preserve

Any Lean-owned promotion or cleanup must preserve:

- Claim text must remain a subset of Lean proof, theorem, audit, or cited literature evidence.
- Novelty and publication-bound claims require precedent/literature search before promotion.
- Lean completion requires foreground build evidence, sorry count, and axiom audit.
- Lean proof/build/PR mechanics route through dedicated Lean skills rather than generic DomainSpec workflow skills.
- Mathlib PR descriptions must strip DomainSpec/framework taxonomy and remain a subset of proved theorem content.
- Non-trivial math/Lean sessions close through `/close-session-math` as proof-trail evidence.

## Current Findings

From `ops/development/lean-formalization-skill-agent-candidate-ledger.md`:

- Lean records: 47.
- Lean proof-domain skills: 13.
- Lean proof-domain agent prompts: 3.
- Lean router: 1.
- Shared utility and imported utility residue remains present.

The canonical map keeps Lean proof-domain and theorem-governance materials as
separate canonical candidates. It does not merge them into generic DomainSpec
runtime skills.

## Residue Requiring Active-Use Proof

Do not promote or preserve these as canonical proof-domain capabilities without
active-use evidence:

- `domainspec-lean-formalization/.agents/skills/custom/*`
- `domainspec-lean-formalization/.agents/skills/gitnexus/*`
- `domainspec-lean-formalization/.agents/skills/implement-filter/SKILL.md`

These may still be useful locally, but the current root map treats them as
residue candidates rather than theorem-formalization canonical units.

## Recommended Lean Task

Create a Lean-owned task to split the lane into two capability packages:

1. Proof mechanics: Lean imports, simp hygiene, declaration naming, PR preparation/review, build verification, and proof writing.
2. Theorem research governance: discovery writing, ontology research, robot dialogue, precedent search, and Mathlib PR description writing.

The task should decide whether any shared utility belongs in either package or
should remain local residue.

## Suggested Validation

Before promoting Lean lane changes:

```bash
rg -n "sorry|axiom|admit" domainspec-lean-formalization
```

Then run the appropriate Lean build command from the Lean repository context and
record foreground build evidence, sorry count, and axiom audit in the Lean task.
