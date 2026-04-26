---
name: mars-research-definitions-governance
description: "Govern canonical definitions for MARS research projects: maintain formal semantics, colocated plain-language intuition, index sync, and downstream drift checks."
argument-hint: "<project-name> [--add <ID>] [--update <ID>] [--sync] [--audit]"
agent: mars-research-planner
allowed-tools: Read, Write, Bash, Glob, Grep
---

<objective>
Keep research definitions authoritative, interpretable, and traceable across MARS projects.

Use this skill when you need to add or revise gate-critical terms, formulas, notation, or definition families, and then propagate those changes safely into protocols, claims, and paper artifacts.
</objective>

<context>
Project contracts (target project):
- `research/projects/<project>/definitions/DEFINITIONS.md`
- `research/projects/<project>/definitions/DEFINITIONS-INDEX.md`
- `research/projects/<project>/papers/*.md`
- `research/projects/<project>/protocols/*.md`
- `research/projects/<project>/registry/TRACEABILITY-MATRIX.md`
- `research/projects/<project>/README.md`

MARS governance references:
- `implementation/mars/definitions/DEFINITIONS.md`
- `implementation/mars/definitions/DEFINITIONS-INDEX.md`
- `implementation/mars/definitions/MARS-PIPELINE.md`
- `research/projects/mars/protocols/MARS-PROTOCOL-CHECKLIST.md`
</context>

<authority-model>
1. For project `mars`, `implementation/mars/definitions/DEFINITIONS.md` is normative for reusable semantics.
2. For non-mars projects, `definitions/DEFINITIONS.md` is normative for project semantics.
3. `definitions/DEFINITIONS-INDEX.md` is lookup/traceability support.
4. Paper text is condensed synthesis and must not redefine canonical semantics.
</authority-model>

<process>
1. Resolve target project from argument; if omitted, infer from active files.
2. Read canonical definitions and definitions index first.
   - If target project is `mars`, edit `implementation/mars/definitions/*` first, then sync projection copies with `./tools/sync_mars_canonical_assets.sh`.
3. Add or update stable definition IDs with precise normative wording.
4. For mathematical constructs, keep these elements together in the same DS section:
   - formal expression,
   - symbol/variable meaning,
   - inline `Intuition` note (non-normative explanatory guidance).
5. If a global synthesis section exists, keep it consistent with inline intuition notes.
6. Sync definitions index anchors and artifact mappings.
7. Audit downstream drift:
   - protocol definition anchors,
   - traceability references,
   - paper wording conflicts.
8. Emit explicit remediation items for undefined, ambiguous, or conflicting terms.
9. Validate structure with:
   - `./tools/check_research_structure.sh`
</process>

<quality-bar>
- No new gate-critical term is normative unless present in `DEFINITIONS.md`.
- No formula without symbol meaning and plain-language intent.
- Intuition is colocated with each updated definition (not detached-only guidance).
- Plain-language notes must not contradict formal semantics.
- Definition IDs are unique, stable, and consistently referenced.
- Drift findings include exact file targets for remediation.
</quality-bar>

<output-contract>
Return a concise governance summary:

```markdown
## Definitions Governance Summary
- Project: <project-name>
- Definitions updated: <list IDs>
- Index synced: yes/no
- Paper drift found: yes/no
- Protocol anchor gaps: <count>
- Traceability gaps: <count>
- Validation: pass/fail

### Follow-ups
1. <action>
2. <action>
```
</output-contract>
