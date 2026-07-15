---
task: SWU-RDL-004
mode: lean-strict
status: pass
createdAt: 2026-07-14T22:26:10Z
session_evidence: true
source_count: 7
obligation_coverage: 100%
---

# Context Pack: SWU-RDL-004 Fingerprint And Projection Manifest

This is Task Session evidence, not a reusable source-of-truth document.

## Objective

Make the Roadmap Lab projection traceable to deterministic build inputs and
rendered target bindings: hash a normalized input manifest, include manifest,
Craft, presentation-copy, and declared source-reference digests, embed rendered
node/field/source selectors, regenerate outputs, and prove material input
changes alter the fingerprint.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| F1 | Compute `read_model.input_fingerprint` from a versioned normalized build-input manifest, not ad hoc raw bytes. | `IMPLEMENTATION-PLAN.md#Deterministic fingerprint`; current `_fingerprint` | covered |
| F2 | Include roadmap manifest, Craft ledger, presentation copy, and declared source-reference digests. | SWU-RDL-004 rules; current source list and `roadmap-copy.json` | covered |
| F3 | Embed schema versions, rendered node IDs, copy field IDs, source refs, and coverage metadata without absolute paths or timestamps. | SWU-RDL-004 done criteria; current generated payload | covered |
| F4 | Prove manifest, Craft, copy, and declared source mutations change the fingerprint; unchanged builds remain byte-identical. | task validation requirements and test suite idioms | covered |
| F5 | Keep generated outputs builder-owned and synchronized after regeneration. | builder `generate`, `check_outputs`, SWU-RDL-003 result | covered |
| F6 | Avoid pulling UI proposal behavior or IDE route work forward. | W1 order and SWU write scope | covered |

## Selected Sources

| Source selector | Why included | Obligations |
| --- | --- | --- |
| `WORK-PACK.md` SWU-RDL-004 row | exact write scope/status/validation | F1-F6 |
| `TASK-RDL-BUILDER.md#SWU-RDL-004` | done criteria, edge cases, handoff | F1-F6 |
| `work-pack/waves/W1.md` | W1 entry/stop state after SWU-RDL-003 | F5-F6 |
| `IMPLEMENTATION-PLAN.md#Deterministic fingerprint`, `#Build metadata` | normalized manifest and metadata algorithm | F1-F4 |
| `SWU-RDL-003/TASK-SESSION-RESULT.md` and `COPY-MIGRATION-REPORT.md` | current copy model, generated baseline, next dependency | F2-F5 |
| `visibility/tools/build-roadmap.py` | current builder functions and fingerprint gap | F1-F5 |
| `visibility/tests/test_build_roadmap.py` | existing deterministic, stale, and negative validation style | F3-F5 |

Selected excerpt budget: 118 lines across 7 files.

## Contract Decisions

### D-SWU004-01 - Fingerprint a normalized manifest of input digests

- Selected: create a build manifest containing a version, relative input paths,
  SHA-256 digests, source roles, schema versions, rendered target IDs, and copy
  field IDs; hash its deterministic JSON bytes for `input_fingerprint`.
- Reason: this captures logical build inputs while excluding timestamps,
  absolute paths, and generated outputs.

### D-SWU004-02 - Keep proposal behavior deferred

- Selected: embed enough selectors for SWU-RDL-005 to bind proposals, but do not
  add event-producing UI or focused IDE routing here.
- Reason: SWU-RDL-004 proves projection identity. Proposal admission begins in
  SWU-RDL-005 after this metadata exists.

No blocker-level decision exists. Decision Gate is not required.

## Write Scope And Dirty Gate

Allowed:

- `visibility/tools/build-roadmap.py`;
- `visibility/roadmap.template.html` only if selector display needs a local
  template hook;
- `visibility/tests/test_build_roadmap.py`;
- regenerated `visibility/roadmap-data.json` and `visibility/roadmap.html`;
- this session's result/report and planning synchronization.

Read-only: roadmap manifest, Craft ledger, copy/event schemas, IDE runtime, and
public Arcanum.

Dirty-scope review: selected product files are the same untracked visibility
package files mutated by SWU-RDL-003. Continue treating them as the current
baseline; do not clean or rewrite unrelated repository changes.

## Validation

```bash
python3 -m unittest discover \
  -s projects/domainspec-v2/development/first-production-release/visibility/tests \
  -p 'test_build_roadmap.py'

python3 projects/domainspec-v2/development/first-production-release/visibility/tools/build-roadmap.py
python3 projects/domainspec-v2/development/first-production-release/visibility/tools/build-roadmap.py --check
python3 -m unittest discover \
  -s projects/domainspec-v2/development/first-production-release/visibility/tests
```

Also run two unchanged build generations and compare SHA-256, JSON parsing,
no-absolute-path scan, and focused mutation checks for manifest, Craft, copy,
and declared source file input changes.

## Context Builder Result

- Mode: lean, strict.
- Files selected: 7.
- Obligations: 6/6 covered.
- Noise ratio: low.
- Handoff pack: none; local execution.
- Strict coverage: pass.
- Blockers: 0.
