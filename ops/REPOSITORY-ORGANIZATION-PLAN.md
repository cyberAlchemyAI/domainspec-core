# Repository Organization Plan

Goal: organize the repository so each research project is self-contained, and every cross-project dependency is explicit, versioned, and auditable.

Date: 2026-04-21
Scope: domainspec-core (implementation, research, validation orchestration)

## 1. Design Principles

1. Self-contained by default: each research project owns its protocol, data, sources, inventory, results, and paper artifacts.
2. Explicit dependencies only: projects cannot rely on implicit file-path coupling.
3. Published interfaces: cross-project reuse happens through declared export artifacts.
4. Immutable evidence: raw data stays append-only inside project boundaries.
5. Layer ownership remains intact: Type A in implementation, Type B in root orchestration, Type C in validation overlays.
6. Canonical paths only: no compatibility aliases or redirect layers unless explicitly requested.

## 2. Repository Zones

### Zone A: Implementation Source of Truth

Path: implementation/domainspec

Responsibilities:
- Canonical DomainSpec pack and framework content.
- Reusable Type A assets.

Consumption model:
- Research can reference released snapshots or pinned commits.
- No project should assume moving targets without pinning version.

### Zone B: Research Projects

Path: research/projects

Responsibilities:
- Self-contained experiment programs.
- Claim evidence pipelines.
- Project-local data, sources, inventory, results, and publication assets.

### Zone C: Validation Harness

Path: validation/poker-team

Responsibilities:
- Runtime and case-study evidence.
- Project-local overlays and operational validation.

## 3. Target Research Structure

```
research/
  projects/
    domainspec/
      PROJECT.yaml
      README.md
      definitions/
      claims/CLAIMS.md
      protocols/
      experiments/
      sources/
      inventory/
      data/
      results/
      papers/
      telemetry/
        SIGNAL-SCHEMA.md
        signals.jsonl
      registry/
        ARTIFACT-INDEX.md
        TRACEABILITY-MATRIX.md
      deps/DEPENDENCIES.yaml
      exports/
      runbooks/
    meta-meta/
      PROJECT.yaml
      README.md
      definitions/
      claims/CLAIMS.md
      protocols/
      experiments/
      sources/
      inventory/
      data/
      results/
      papers/
      telemetry/
        SIGNAL-SCHEMA.md
        signals.jsonl
      registry/
        ARTIFACT-INDEX.md
        TRACEABILITY-MATRIX.md
      deps/DEPENDENCIES.yaml
      exports/
      runbooks/
    mars/
      PROJECT.yaml
      README.md
      definitions/
      claims/CLAIMS.md
      protocols/
      experiments/
      sources/
      inventory/
      data/
      results/
      papers/
      telemetry/
        SIGNAL-SCHEMA.md
        signals.jsonl
      registry/
        ARTIFACT-INDEX.md
        TRACEABILITY-MATRIX.md
      deps/DEPENDENCIES.yaml
      exports/
      runbooks/
  shared/
    standards/
    templates/
  registry/
    PROJECT-INDEX.md
    DEPENDENCY-GRAPH.md
```

## 3.1 Artifact Lane Convention (borrowed from DomainSpec)

Each project uses four explicit artifact lanes:

1. Canonical definitions lane
- Inputs authored by humans and treated as source of truth.
- Examples: claims, protocols, experiment definitions, governance baselines.

2. Derived outputs lane
- Generated artifacts produced by execution and analysis workflows.
- Examples: integrity reports, pipeline reports, evidence updates, synthesis summaries.

3. Registry and traceability lane
- Indexes that aggregate and cross-reference project artifacts.
- Examples: artifact index, claim-to-experiment matrix, dependency graph pointers.

4. Telemetry lane
- Signal schema plus append-only signal stream for observability of research operations.
- Examples: SIGNAL-SCHEMA.md and signals.jsonl.

## 4. Project Contract (required for each project)

Each project must include:

1. PROJECT.yaml
- project_id
- project_name
- owner_agent
- status
- version
- dependencies_ref
- exports_ref

2. claims/CLAIMS.md
- claim IDs owned by project
- claim definitions
- claim-to-experiment map

3. deps/DEPENDENCIES.yaml
- explicit dependencies and expected artifact contracts

4. exports/
- published artifacts that other projects may consume
- each artifact includes version, producer, schema, and breaking-change notes

## 5. Explicit Cross-Dependency Model

Cross-project dependencies are allowed only through deps/DEPENDENCIES.yaml and exports manifests.

Dependency types:

1. data_dependency
- Consumes run/result artifacts from another project.

2. method_dependency
- Consumes protocol, schema, or analysis standards.

3. claim_dependency
- Uses evidence from another project for claim adjudication.

Required fields for each dependency:
- dependency_id
- provider_project
- provider_artifact
- provider_version_or_commit
- consumer_project
- consumer_purpose
- validation_gate
- fallback_plan

Example schema:

```
dependencies:
  - dependency_id: dep-mars-c2-baseline
    type: claim_dependency
    provider_project: domainspec
    provider_artifact: exports/claims/C2-baseline.md
    provider_version_or_commit: v0.1.0
    consumer_project: mars
    consumer_purpose: initialize MARS-C2 prior evidence
    validation_gate: G1
    fallback_plan: block until baseline is published
```

## 6. Allowed and Disallowed Coupling

Allowed:
1. project A reads project B exports path declared in dependency manifest.
2. project A references shared standards/templates in research/shared.
3. project A references pinned implementation version in implementation/domainspec.

Disallowed:
1. project A reading project B internal data/results directly.
2. project A reusing unpublished intermediate files from project B.
3. project A using implementation content without version pin.

## 7. Migration Map (current to target)

### Move DomainSpec research assets

From:
- research/experiments/*

To:
- research/projects/domainspec/*

### Move Meta-Meta assets

From:
- research/EXPERIMENTS-META.md and related docs

To:
- research/projects/meta-meta/*

### Move MARS assets

From:
- research/MARS-*.md and related files

To:
- research/projects/mars/*

### Keep shared standards

From:
- research root templates and common policy docs

To:
- research/shared/standards and research/shared/templates

## 8. Rollout Plan

### Phase 0: Freeze and inventory (1 day)

1. Freeze new path changes except critical fixes.
2. Generate complete file inventory by project ownership.
3. Tag baseline commit before migration.

### Phase 1: Scaffold project containers (1-2 days)

1. Create research/projects/domainspec, meta-meta, mars.
2. Add PROJECT.yaml, CLAIMS.md, DEPENDENCIES.yaml placeholders.
3. Create registry/PROJECT-INDEX.md.

### Phase 2: Move files without semantic edits (2-3 days)

1. Move existing docs/data/results/sources/inventory into project-local folders.
2. Preserve file history and add migration notes.
3. Remove old paths after move; do not add redirect pointers unless explicitly requested.

### Phase 3: Dependency declaration and export publication (1-2 days)

1. Define exports for each project.
2. Fill DEPENDENCIES.yaml for domainspec, meta-meta, mars.
3. Build registry/DEPENDENCY-GRAPH.md from manifests.

### Phase 4: Enforce with checks (1-2 days)

1. Add validation script to fail on undeclared cross-project reads.
2. Add check for missing provider version pin.
3. Add check that every dependency references an existing export.

## 9. Governance Checks to Add

1. project_containment_check
- Fails if project reads another project internal path.

2. dependency_manifest_check
- Fails if dependency fields are missing.

3. export_contract_check
- Fails if consumed export path/version does not exist.

4. claim_traceability_check
- Fails if claims reference non-existent experiments or results.

## 10. Immediate Next Actions

1. Approve target structure and dependency model.
2. Scaffold research/projects and registry directories.
3. Perform Phase 2 migration in one controlled batch.
4. Wire checks into existing governance scripts.

## 11. Success Criteria

1. Every research project can run independently from its own folder.
2. Every cross-project dependency is listed in DEPENDENCIES.yaml.
3. No direct internal cross-project file reads remain.
4. Dependency graph is generated and reviewed at each release checkpoint.
5. Existing governance drift checks remain green after migration.

## 12. DomainSpec Output Artifact Model Reuse

The research organization should reuse these DomainSpec patterns directly.

| DomainSpec Pattern | Existing DomainSpec Artifact | Research Reuse |
|---|---|---|
| Canonical concept spec as source of truth | docs/features/*/SPEC.md + aspect docs | claims + protocols + experiment definitions are canonical inputs |
| Explicit dependency declaration inside canonical spec | SPEC.md sections: Cross-Feature Dependencies and Produces For | each project must declare provider/consumer dependencies in DEPENDENCIES.yaml |
| Generated run report with frontmatter and verdict | templates/PIPELINE-REPORT.md | standardize project run reports with status PASS/FLAG/BLOCK |
| Generated alignment report comparing declared vs implemented obligations | templates/OBSERVABILITY-REPORT.md | add integrity/evidence alignment reports comparing protocol vs data/results |
| Signal schema and append-only stream | templates/SIGNAL-SCHEMA.md and docs/signals/pipeline-signals.jsonl | add per-project telemetry/SIGNAL-SCHEMA.md and telemetry/signals.jsonl |
| Global registry for searchable system view | docs/registry.md | add per-project registry plus root registry/PROJECT-INDEX.md and DEPENDENCY-GRAPH.md |
| Stable governance baseline for cross-cutting defaults | docs/shared/governance-baseline.md | add per-project definitions/governance-baseline.md for execution defaults |

## 13. Standard Research Output Artifacts

Each project should publish these generated outputs in a consistent format:

1. PIPELINE-REPORT.md
- one per run cycle; includes counters, verdict by stage, and reflection items.

2. INTEGRITY-REPORT.md
- validates protocol schema, metadata completeness, and row integrity before analysis.

3. EVIDENCE-REPORT.md
- maps experiment findings to claim status deltas and recommended next experiments.

4. TRACEABILITY-REPORT.md
- maps claim -> experiment -> data file -> result file -> paper section.

5. SESSION-RETROSPECTIVE.md
- records deviations, rework causes, and concrete process improvements.
