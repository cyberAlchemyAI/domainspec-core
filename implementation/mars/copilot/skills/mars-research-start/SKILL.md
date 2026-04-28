---
name: mars-research-start
description: "Unified MARS startpoint. Detect greenfield or brownfield scope, run discovery, scaffold a repository-valid research project baseline when needed, and enforce structural readiness before protocol design or execution."
argument-hint: "[greenfield|brownfield|auto] [project-or-research-scope] [--audit-only]"
agent: mars-research-interviewer
allowed-tools: Read, Write, Bash, Glob, Grep, AskQuestions
---

<objective>
Create a stable MARS research-project baseline before `mars-research-planner`, `mars-research-protocol-designer`, or experiment execution mutate project artifacts.

This skill is the dedicated startpoint for new-project initialization and brownfield baseline audits.
</objective>

<context>
Read first:
- `research/projects/mars/README.md`
- `implementation/mars/definitions/MARS-PIPELINE.md`
- `research/shared/templates/PROJECT-README.md`
- `research/registry/PROJECT-INDEX.md`
- `research/registry/DEPENDENCY-GRAPH.md`

Uses:

- `mars-research-interview`
- `mars-research-foundations`
- `mars-research-emit-signals`
- `implementation/mars/templates/domain-context-template.md`
- `implementation/mars/templates/methodology-theory-baseline-template.md`
- `implementation/mars/templates/project-overview-template.md`
- `implementation/mars/templates/initial-definitions-template.md`
- `implementation/mars/templates/hypotheses-template.md`
- `implementation/mars/templates/experiment-candidates-template.md`
- `implementation/mars/templates/telemetry-signal-schema-template.md`
- `tools/update_project_experiments_index.sh`
- `tools/check_research_structure.sh`
  </context>

<process>
1. Read framework references and detect mode (`greenfield`, `brownfield`, `auto`).
2. Delegate scoped discovery to `mars-research-interview`.
   - `auto` must inspect the repository and choose mode.
   - If `--audit-only`, stop after discovery and startpoint gate verdict.
3. Enforce startpoint artifacts.
   - Repository project contract:
     - `README.md`
     - `PROJECT.yaml`
     - `claims/CLAIMS.md`
     - `deps/DEPENDENCIES.yaml`
     - `registry/ARTIFACT-INDEX.md`
     - `registry/TRACEABILITY-MATRIX.md`
       - `telemetry/SIGNAL-SCHEMA.md` from `implementation/mars/templates/telemetry-signal-schema-template.md`
     - `exports/README.md`
    - Project foundations baseline:
       - `foundations/DOMAIN-CONTEXT.md` from `implementation/mars/templates/domain-context-template.md`
       - `foundations/METHODOLOGY-AND-THEORY.md` from `implementation/mars/templates/methodology-theory-baseline-template.md`
   - Research scope baseline:
     - `PROJECT-OVERVIEW.md`
     - `definitions/DEFINITIONS.md`
     - `definitions/DEFINITIONS-INDEX.md`
     - `definitions/INITIAL-DEFINITIONS.md`
     - `claims/HYPOTHESES.md`
     - `experiments/EXPERIMENT-CANDIDATES.md`
   - First-wave execution baseline:
     - `experiments/EXPERIMENTS.md`
     - `experiments/README.md`
     - `sources/REFERENCE-LEDGER.md`
     - `inventory/INVENTORY-INDEX.md`
     - `results/<project>-EVIDENCE-STATUS.md`
    - Protocol design remains blocked while the foundations baseline is missing or while primary authorities are not yet library-inventoried.
4. Register project integration.
   - Ensure the project is present in `research/registry/PROJECT-INDEX.md`.
   - If upstream exported artifacts are declared in `deps/DEPENDENCIES.yaml`, ensure matching edges exist in `research/registry/DEPENDENCY-GRAPH.md`.
5. Run startpoint gates.
   - Gate A - Project contract completeness.
   - Gate B - Project foundations and scope baseline completeness.
   - Gate C - Registry integration completeness.
   - Gate D - Validation pass via `./tools/update_project_experiments_index.sh <project-key>` and `./tools/check_research_structure.sh`.
   - If any gate fails, return BLOCK and stop before protocol-design or execution guidance.
6. Recommend or run project foundations baseline.
   - If the foundations artifacts are still placeholders or authority coverage is missing, route next to `mars-research-foundations <project-key>`.
7. Emit startpoint telemetry.
   - Use `mars-research-emit-signals` to record startpoint outcomes, especially `workflow-gap`, `contract-gap`, `decision-friction`, `overhead`, and `proposal` when applicable.
8. Return startpoint summary with mode, gate results, artifacts, and next recommended command.
</process>

<output-contract>
Return:

```markdown
## MARS Startpoint Summary

- Mode selected: greenfield | brownfield
- Gate verdict: PASS | BLOCK
- Discovery status: completed | blocked
- New project initialized: yes | no

### Artifacts

- Project README: <path>
- Project manifest: <path>
- Project overview: <path>
- Canonical definitions: <path>
- Definitions index: <path>
- Hypotheses: <path>
- Experiment candidates: <path>

### Startpoint Gates

| Gate | Verdict | Notes |
| ---- | ------- | ----- |

### Recommended Next Command

- <exact command with arguments>
```

</output-contract>

<authority-rule>
- No protocol-design or execution-stage workflow should proceed while the MARS startpoint gate verdict is BLOCK.
- When the operator asks to create or initialize a new project, completion requires structural validation, not discovery-only artifacts.
</authority-rule>

<examples>
- `/mars-research-start auto`
- `/mars-research-start greenfield multi objective decision research`
- `/mars-research-start brownfield research/projects/mars --audit-only`
</examples>
