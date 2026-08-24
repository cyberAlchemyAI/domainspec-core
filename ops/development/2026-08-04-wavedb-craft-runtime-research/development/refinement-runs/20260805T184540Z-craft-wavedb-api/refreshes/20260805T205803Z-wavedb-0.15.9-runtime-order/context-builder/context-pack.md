# Context Pack — Craft API WaveDB 0.15.9 runtime order refresh

Status: strict coverage pass. This is Invoke Refresh session evidence, not a
replacement authority for the selected Work Pack or its source receipts.

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Bind the new package identity and exact Node runtime without inferring source provenance. | covered |
| O2 | Preserve the existing 0.15.8 Craft import as a baseline, not a 0.15.9 snapshot. | covered |
| O3 | Order re-ingestion, fresh-process verification, API pinning, and read-only construction. | covered |
| O4 | Refresh every coupled runtime-plan projection and no unrelated artifact. | covered |
| O5 | Preserve owner, security, deployment, authority, and evidence-ceiling blockers. | covered |
| O6 | Require an exact apply-approved material package and live validation. | covered |

## Selected evidence

- `WORK-PACK.md` — control fields, SWU handoff, closeout table, blockers, and
  first-unit verdict. Covers O3-O6.
- `work-pack/tasks/TASK-RUNTIME.md` — exact runtime SWU behaviors,
  dependencies, scopes, and evidence. Covers O3-O6.
- `work-pack/waves/W1.md` and `EXECUTION-PACK.md` — coupled wave ordering.
  Covers O3-O4.
- `../../../../experiment/source-build/npm-diagnostic/execution/npm-node26-0.15.9/npm-diagnostic-receipt.json`
  — exact npm tarball identity, Node 26.6.0 canaries, and residue. Covers O1,
  O5.
- `../../../../experiment/source-build/npm-diagnostic/execution/task-sessions/SWU-WCND-002/terminal-receipt.json`
  — Task Session result and explicit denial of Craft/API integration. Covers
  O1, O5-O6.
- `../../../../experiment/craft-ledger-import/execution/wcli-20260805-node26-04/receipt.json`
  — 0.15.8, 27-ledger, 55-record sequential import baseline. Covers O2-O3.

## Exact target inventory

1. `WORK-PACK.md`
2. `work-pack/tasks/TASK-RUNTIME.md`
3. `work-pack/waves/W1.md`
4. `EXECUTION-PACK.md`

Historical Refine stages, design contracts, `RESULT.md`, `RUNTIME-HANDOFF.md`,
Craft ledgers, existing WaveDB attempts, and implementation paths are excluded.
Their bytes are not part of this refresh.

## Resolutions and residue

- Insert `SWU-CAPI-000`; do not renumber `SWU-CAPI-001` through `009`.
- The API dependency pin is a gate before `SWU-CAPI-002`, not evidence that the
  API dependency has already been updated.
- The new package passed isolated canaries, but a 0.15.9 Craft snapshot and a
  separately launched reader receipt do not exist.
- The exact reviewed source tree behind the npm tarball remains unbound; prior
  concurrency and compiler-warning residue remains live.
- The root-level catalog lookup typo (`formulae/...`) was corrected to the
  generated `.agents/skills/dispatch-spec/TECHNIQUE-CATALOG.md` path.
- Inventory lookup readiness passed with 146 tag warnings; Inventory contributed
  discovery only and no authority claim.

Distill is skipped: the change is one bounded dependency-order repair over four
coupled planning projections, with one stable new predecessor and no new product
behavior or implementation slice.
