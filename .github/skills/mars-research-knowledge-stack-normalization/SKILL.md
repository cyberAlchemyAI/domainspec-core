---
name: mars-research-knowledge-stack-normalization
description: "Normalize a brownfield research project to the MARS knowledge-stack contract using dependency-ordered waves across definitions, references, context bundles, inventory, and experiment artifacts."
argument-hint: "<project-key> [--audit|--execute] [--wave <W1..W8>] [--dry-run]"
agent: mars-research-planner
allowed-tools: Read, Write, Bash, Glob, Grep, AskQuestions
---

<objective>
Convert fragmented brownfield research artifacts into a consistent MARS execution stack.

This skill is for projects with scattered definitions/references/context assets that block reliable protocol execution and evidence adjudication.
</objective>

<context>
Target project contracts:
- `research/projects/<project-key>/PROJECT.yaml`
- `research/projects/<project-key>/definitions/*`
- `research/projects/<project-key>/protocols/*`
- `research/projects/<project-key>/sources/*`
- `research/projects/<project-key>/inventory/*`
- `research/projects/<project-key>/experiments/*`
- `research/projects/<project-key>/registry/*`
- `research/projects/<project-key>/results/*`

MARS references:
- `implementation/mars/definitions/RESEARCH-KNOWLEDGE-STACK-CONTRACT.md`
- `implementation/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md`
- `implementation/mars/definitions/MARS-PIPELINE.md`
</context>

<waves>
W1. Candidate extraction
- enumerate definition, reference, context, and resource candidate artifacts

W2. Taxonomy and ID policy
- finalize definition-ID and reference-status vocabularies

W3. Definitions/protocol coupling
- align definition index and protocol checklist anchor requirements

W4. Source authority normalization
- normalize ledger statuses, authority sources, and waivers

W5. Inventory linkage normalization
- ensure source-to-inventory linkage and index coverage

W6. Experiment source backfill
- ensure every scheduled experiment has source-selection artifact with pins

W7. Context bundle backfill
- ensure every scheduled experiment has context bundle minimum contract

W8. Compliance sweep and closure
- run structure checks, publish residual risks, and capture follow-up backlog
</waves>

<process>
1. Run `--audit` first to classify current artifact completeness by wave.
2. Ask decision-gate questions when policy choices have multiple viable options.
3. Execute waves in order unless a specific `--wave` is requested.
4. Stop on blockers and publish exact remediation obligations with file targets.
5. After wave execution:
   - refresh experiment navigation artifacts (`./tools/update_project_experiments_index.sh <project-key>`),
   - run structural validation (`./tools/check_research_structure.sh`).
6. Publish execution summary and residual risk list.
</process>

<quality-bar>
- No wave can be marked complete without artifact evidence.
- Reference authority normalization must preserve waiver auditability.
- Context bundles must include source-role matrix, terminology map, metric map, conflict log, and open risks.
- Backfill actions must be deterministic and reproducible.
</quality-bar>

<output-contract>
Return:

```markdown
## Knowledge Stack Normalization Summary
- Project: <project-key>
- Mode: audit | execute
- Waves completed: <list>
- Waves blocked: <list>
- Critical blockers: <n>

### Artifacts Updated
- <path>

### Residual Risks
1. <risk>

### Next Actions
1. <action>
2. <action>
```
</output-contract>
