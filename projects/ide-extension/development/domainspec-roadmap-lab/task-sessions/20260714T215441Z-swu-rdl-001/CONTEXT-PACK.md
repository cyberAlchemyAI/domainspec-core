---
task: SWU-RDL-001
mode: lean-strict
status: pass
createdAt: 2026-07-14T21:54:41Z
session_evidence: true
source_count: 7
obligation_coverage: 100%
---

# Context Pack: SWU-RDL-001 Presentation-copy Oracle

This is Task Session evidence, not a reusable source-of-truth document.

## Objective And Output

Define a JSON Schema, valid/invalid fixtures, and a focused unittest that make
human-facing roadmap copy addressable without importing roadmap, graph, Craft,
or release authority into the copy document.

## Obligation Matrix

| ID | Obligation | Selected evidence | Status |
| --- | --- | --- | --- |
| O1 | Require versioned, presentation-only copy fields with stable identity, target association, role, and nonblank text. | Task contract SWU-001; design RDL-D04; architecture RDL-CN02 | covered |
| O2 | Reject duplicate field IDs even when the duplicated rows differ. | Task contract invalid-fixture rule | covered |
| O3 | Reject unknown roadmap node targets against the live manifest rather than a copied ID enumeration. | Builder `MANIFEST_PATH`; manifest `nodes`; task unknown-node rule | covered |
| O4 | Reject missing roles, blank text, extra fields, and authority-bearing fields. | Task rules; design owner boundary; manifest authority fields | covered |
| O5 | Keep behavior unchanged: no builder, template, generated output, IDE runtime, or authority source edits. | Work-pack scope; W0 exit; dirty-tree gate | covered |
| O6 | Produce focused, runnable schema/fixture evidence. | Existing unittest style and installed `jsonschema` 4.10.3 | covered |

## Selected Sources

| Source and selector | Use | Obligations | SHA-256 |
| --- | --- | --- | --- |
| `WORK-PACK.md#SWU Execution Manifest`, `#Gate Checks` | selection, scope, execution constraints | O1–O6 | `5343f993aefbb664799229a2622df6965d0af661cadd08a50aa981a47a00136d` |
| `work-pack/tasks/TASK-RDL-CONTRACTS.md#SWU-RDL-001` | exact objective, invalid cases, done/evidence/validation | O1–O6 | `88281bd92436a037ba301af6bfeeaa39f8e0c197d9bf4b6533f60c34849eeb67` |
| `ARCHITECTURE-BUNDLE.md#View 3`, `#View 6` | CopyField is presentation-owned and separate from graph authority | O1, O4, O5 | `cc579eaee51f0f929f73ccd8d5f299eff178d2cb0460dd960d78c551dca84e62` |
| `DESIGN-DECISIONS.md` RDL-D04/D05 | stable field IDs precede proposals; observed values bind later | O1, O4 | `b110951f53537bc32e3822a2bacf35fb3dfa9e3aefa5cb6e5334e4eefbb97dd7` |
| `visibility/roadmap.template.html:383-437` | current node/frontier/critical-step/status copy shapes | O1, O5 | `86c14e8aab70134e628e169a03785085c57074ca03e8c6e4c00fe3eff67cf3f9` |
| `visibility/tests/test_build_roadmap.py:35-71` | current unittest and copy-coverage conventions | O3, O5, O6 | `1f0192ab98e11bde933a451d1a4a85db2c66a0ac240865e631152a6910efdbb3` |
| `craft/expected-node-edge-manifest.yml:1-68,457-514` | live authority/target sets for nodes, frontiers, critical steps | O3, O4 | `0d24d1581da0faea3cc1a481ee7175083a922f10cc731fb5bd474ccd6320e64e` |

Selected excerpt budget: 128 lines across 7 files.

## Implementation Decision Pack

### D-SWU001-01 — General target shape

- Classification: non-blocking implementation decision.
- Selected: one generic `target` object with `kind` and `id`; node rows are
  validated against manifest nodes, while the same contract can later address
  frontiers, critical steps, status labels, and page copy.
- Rejected: node-only schema, because SWU-RDL-003 must immediately migrate
  frontier, step, heading, and explanatory copy and would force schema churn.
- Rejected: separate arrays per target kind, because it duplicates field
  identity/role/text rules without adding authority safety.
- Constraint: stable `field_id` must equal
  `copy.<target-kind>.<target-id>.<role>`; target validity is checked against
  live manifest sets rather than frozen schema enums.

This decision is local, reversible, and does not change product authority or
the accepted UX. No blocker-level choice requires Decision Gate.

## Write Scope

Allowed new files only:

- `visibility/schemas/roadmap-copy.schema.json`;
- `visibility/tests/fixtures/roadmap-copy/*.json`;
- `visibility/tests/test_roadmap_contracts.py`;
- this Task Session's evidence/result files;
- work-pack/task/wave/traceability status synchronization after validation.

Forbidden in this SWU: builder, template, manifest, Craft ledger, generated
roadmap outputs, IDE runtime, package scripts, and public `arcanum/`.

## Dirty-tree Gate

The first-production-release package and visibility directory are currently
untracked in the parent repository. The selected product paths do not yet exist,
so there is no overlapping file mutation. Existing untracked builder/template/
manifest files are read-only inputs and their hashes are recorded above.

## Validation Surface

```bash
python3 -m unittest discover \
  -s projects/domainspec-v2/development/first-production-release/visibility/tests \
  -p 'test_roadmap_contracts.py'
```

Additional checks: schema meta-validation, JSON parse, exact invalid-error
matrix, scoped status/diff, and confirmation that recorded read-only source
hashes remain unchanged.

## Context Builder Result

- Mode: lean, strict.
- Files selected: 7.
- Obligation coverage: 6/6 (100%).
- Noise ratio: low; every selector closes at least one obligation.
- Handoff pack: none; execution is local, not `--via runtime`.
- Strict coverage: pass.
- Blockers: 0.

