# Experiment Bundle Migration Plan

Objective: migrate all current experiment artifacts from flat/shared locations to per-experiment bundle directories.

Status: completed
Owner: mars-research-planner
Completed on: 2026-04-22

## Target Structure

Each experiment will use:

- `experiments/<experiment-key>/protocol.md`
- `experiments/<experiment-key>/sources.md`
- `experiments/<experiment-key>/data/*.jsonl`
- `experiments/<experiment-key>/results/*.md`

No new writes should be made to legacy flat experiment files after migration starts.

## Scope

This plan covers all current experiments discovered in:

- `research/projects/domainspec/experiments/`
- `research/projects/mars/experiments/`
- related data and results files in shared project directories

## Migration Inventory (Pre-Migration Snapshot)

| Experiment | Pre-Migration Protocol | Pre-Migration Data Files | Pre-Migration Result Files | Target Bundle Directory |
|---|---|---|---|---|
| E1 | `research/projects/domainspec/experiments/E1-derivation-determinism.md` | none | none | `research/projects/domainspec/experiments/E1-derivation-determinism/` |
| E2 | `research/projects/domainspec/experiments/E2-derivation-vs-manual.md` | none | none | `research/projects/domainspec/experiments/E2-derivation-vs-manual/` |
| E3 | `research/projects/domainspec/experiments/E3-mutation-testing.md` | none | none | `research/projects/domainspec/experiments/E3-mutation-testing/` |
| E4 | `research/projects/domainspec/experiments/E4-governance-attenuation-curve.md` | none | none | `research/projects/domainspec/experiments/E4-governance-attenuation-curve/` |
| E5 | `research/projects/domainspec/experiments/E5-observer-executor-separation.md` | none | none | `research/projects/domainspec/experiments/E5-observer-executor-separation/` |
| E6 | `research/projects/domainspec/experiments/E6-vocabulary-sufficiency.md` | `research/projects/domainspec/data/E6-run-2026-04-20.jsonl` | `research/projects/domainspec/results/E6-results.md` | `research/projects/domainspec/experiments/E6-vocabulary-sufficiency/` |
| E7 | `research/projects/domainspec/experiments/E7-signal-emission-rate.md` | none | none | `research/projects/domainspec/experiments/E7-signal-emission-rate/` |
| E8 | `research/projects/domainspec/experiments/E8-meta-health-convergence.md` | none | none | `research/projects/domainspec/experiments/E8-meta-health-convergence/` |
| E9 | `research/projects/domainspec/experiments/E9-cross-feature-composition.md` | `research/projects/domainspec/data/E9-run-2026-04-20.jsonl`, `research/projects/domainspec/data/E9-run2-2026-04-20.jsonl`, `research/projects/domainspec/data/E9-run2-rerun-2026-04-20.jsonl` | `research/projects/domainspec/results/E9-results.md`, `research/projects/domainspec/results/E9-run2-rerun-results.md` | `research/projects/domainspec/experiments/E9-cross-feature-composition/` |
| E10 | `research/projects/domainspec/experiments/E10-developer-productivity.md` | none | none | `research/projects/domainspec/experiments/E10-developer-productivity/` |
| MARS-DRY-RUN-E1-foundation | `research/projects/mars/experiments/MARS-DRY-RUN-E1-foundation.md` | none | none | `research/projects/mars/experiments/MARS-DRY-RUN-E1-foundation/` |

Migration outcome:

- All listed target bundle directories were created.
- Protocol files were moved to `protocol.md` inside each bundle.
- Existing JSONL and result files were moved into bundle `data/` and `results/` directories.
- Bundle-local `sources.md` files were created.

## Execution Plan

### Wave 1: Directory and Protocol Migration (completed)

1. Create bundle directories for each experiment listed above.
2. Move each protocol file to `protocol.md` under its bundle directory.
3. Create `sources.md` placeholders for experiments that do not yet have source-selection files.

### Wave 2: Data and Results Migration (completed)

1. Move existing JSONL files into each experiment `data/` directory.
2. Move existing result markdown files into each experiment `results/` directory.
3. Keep filenames unchanged during first pass to preserve run traceability.

### Wave 3: Reference and Registry Updates (completed)

1. Update `research/projects/domainspec/experiments/EXPERIMENTS.md` links to bundle `protocol.md` paths.
2. Update DomainSpec artifact index and constitution experiment-link policy to directory-based protocol paths.
3. Update any residual references in MARS runbooks/results/traceability files.

### Wave 4: Governance Enforcement (completed)

1. Re-run governance checks and docs checks.
2. Verify no new writes target legacy flat experiment files.
3. Mark legacy flat files as deprecated and remove after successful verification.

## Verification Checklist

- [x] All protocol links resolve to `experiments/<experiment-key>/protocol.md`.
- [x] All run JSONL files are under bundle `data/` directories.
- [x] All result markdown files are under bundle `results/` directories.
- [x] MARS and DomainSpec artifact indexes reflect bundle paths.
- [x] No canonical docs depend on legacy flat experiment paths.
