---
name: domainspec-spec-feature
description: Create or evolve a feature specification using DomainSpec templates and taxonomy.
argument-hint: "<feature-name> [--update]"
agent: domainspec-spec-writer
allowed-tools: Read, Write, Glob, Grep
---

<objective>
Produce complete and consistent DomainSpec documentation for one feature before implementation starts.
</objective>

<context>
Source references:
- domainspec/CHANGELOG.md
- domainspec/TAXONOMY.md
- domainspec/RELATIONSHIPS.md
- domainspec/templates/*.md
Target location:
- docs/features/{feature-name}/
</context>

<process>
1. Read domainspec/CHANGELOG.md and extract current-framework constraints.
2. Create or update SPEC.md and concept table.
3. Generate relevant aspect files from templates.
4. Add formal rules, formulas, transitions, and invariants where applicable.
5. When introducing or changing gate-critical terms, sync canonical definitions first via `.github/skills/domainspec-definitions-governance/SKILL.md`.
6. Validate cross-links, referenced field-name links, and concept ID naming.
7. Summarize what is ready and what remains undefined.
</process>
