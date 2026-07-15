---
task: SWU-RDL-003
mode: lean-strict
status: pass
createdAt: 2026-07-14T22:17:18Z
session_evidence: true
source_count: 8
obligation_coverage: 100%
---

# Context Pack: SWU-RDL-003 Copy Extraction And Coverage

This is Task Session evidence, not a reusable source-of-truth document.

## Objective

Move the Roadmap Lab's current human-facing roadmap copy out of executable
template constants into `roadmap-copy.json`, validate complete current coverage
in the builder, remove hidden template fallbacks for migrated copy, regenerate
the read models, and prove the rendered roadmap remains behaviorally
equivalent for the current L0 surface.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| C1 | Externalize current node, frontier, critical-step, and status-label copy using the SWU-RDL-001 `field_id` contract. | `roadmap.template.html` constants and `roadmap-copy.schema.json` | covered |
| C2 | Reject missing, duplicate, unknown, and unused required copy fields with actionable errors. | `TASK-RDL-BUILDER.md` rules and current builder `ContractError` style | covered |
| C3 | Remove migrated literal fallback from template JavaScript. | Current `copyForNode`, `statusFor`, `FRONTIER_COPY`, `STEP_COPY` constants | covered |
| C4 | Preserve roadmap authority: copy never owns node identity, graph meaning, continuation state, proof, or release authorization. | copy schema description and builder manifest/Craft joins | covered |
| C5 | Regenerate only through the builder and keep generated data/HTML deterministic. | builder `generate`, `check_outputs`, current tests | covered |
| C6 | Stay inside dirty-scope boundary and avoid IDE runtime mutation. | scoped `git status --short -- visibility/...` | covered |

## Selected Sources

| Source selector | Why included | Obligations |
| --- | --- | --- |
| `WORK-PACK.md` SWU-RDL-003 row | exact write scope, status, validation | C1-C6 |
| `TASK-RDL-BUILDER.md#SWU-RDL-003` | done criteria and edge cases | C1-C6 |
| `work-pack/waves/W1.md` | W1 entry/exit and stop conditions | C5-C6 |
| `IMPLEMENTATION-PLAN.md#Presentation copy`, `#Build metadata`, `#Test Strategy` | copy contract and coverage/fallback requirements | C1-C5 |
| `visibility/schemas/roadmap-copy.schema.json` | legal target kinds, roles, and `field_id` shape | C1-C4 |
| `visibility/tools/build-roadmap.py` | current deterministic builder, source authority joins, output flow | C2-C5 |
| `visibility/roadmap.template.html:382-439`, `:597-617` | exact migrated copy constants and fallbacks | C1-C3 |
| `visibility/tests/test_build_roadmap.py` | current builder validation idioms and copy assertions | C2-C5 |

Selected excerpt budget: 129 lines across 8 files.

## Contract Decisions

### D-SWU003-01 - Extract current dynamic roadmap copy, not every static label

- Selected: migrate the current JS copy maps used for rendered roadmap nodes,
  frontier cards, critical-step labels, and status labels.
- Deferred: static page chrome such as section headings, command labels, and
  explanatory panels remains template-owned until SWU-RDL-005 reshapes the
  guided learning UI.
- Reason: SWU-RDL-003's equivalence target is the existing generated roadmap
  surface. Migrating only the dynamic copy maps removes the hidden fallback that
  proposal targets will depend on without pulling guided UI copy work forward.

### D-SWU003-02 - Coverage is builder-owned and live-manifest-derived

- Selected: the builder validates `roadmap-copy.json` against the live manifest
  and current node states, then emits a compact copy model in `roadmap-data.json`.
- Rejected: frozen enums inside copy data or permissive template fallback.
- Reason: live manifest ownership must remain authoritative; copy is
  presentation-only and should fail when it no longer matches rendered targets.

These are local implementation choices determined by the accepted SWU and live
contracts. Decision Gate is not required.

## Write Scope And Dirty Gate

Allowed:

- `projects/domainspec-v2/development/first-production-release/visibility/roadmap-copy.json`;
- `visibility/tools/build-roadmap.py`;
- `visibility/roadmap.template.html`;
- `visibility/tests/test_build_roadmap.py`;
- regenerated `visibility/roadmap-data.json` and `visibility/roadmap.html`;
- this session's result and planning synchronization.

Read-only: roadmap manifest, Craft ledger, copy/event schemas, IDE runtime,
public Arcanum, and Roadmap Lab design docs.

Dirty-scope review: all product files in the selected write scope are untracked
visibility package files. Treat them as the current baseline and mutate only
through the scoped extraction path; do not clean, revert, or rewrite unrelated
repository changes.

## Validation

```bash
python3 -m unittest discover \
  -s projects/domainspec-v2/development/first-production-release/visibility/tests \
  -p 'test_build_roadmap.py'

python3 projects/domainspec-v2/development/first-production-release/visibility/tools/build-roadmap.py

python3 projects/domainspec-v2/development/first-production-release/visibility/tools/build-roadmap.py --check
```

Also run JSON parsing for `roadmap-copy.json`, focused copy contract tests after
regeneration, no-absolute-path generated data checks, and a diff explanation for
generated outputs.

## Context Builder Result

- Mode: lean, strict.
- Files selected: 8.
- Obligations: 6/6 covered.
- Noise ratio: low.
- Handoff pack: none; local execution.
- Strict coverage: pass.
- Blockers: 0.
