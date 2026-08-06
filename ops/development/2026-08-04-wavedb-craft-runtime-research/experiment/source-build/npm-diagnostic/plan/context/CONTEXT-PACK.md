# Planning context: pinned npm artifact diagnostic

- Mode: lean, strict.
- Files selected: 5.
- Obligation coverage: 7/7.
- Authority boundary: source files are evidence; this pack is not package,
  Craft, or lifecycle authority.

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| WCND-O1 | bind exact npm name/version/tarball integrity | provenance result and live registry metadata | covered |
| WCND-O2 | preserve stale `gitHead` contradiction | history reconstruction | covered |
| WCND-O3 | record direct risk/policy authorization | `DECISION.md` and admissibility receipt | covered |
| WCND-O4 | use exact Node 26/npm identities | prior Node 26 terminal receipt plus live NVM check | covered |
| WCND-O5 | distinguish compilation/load from runtime proof | Node 26 terminal receipt | covered |
| WCND-O6 | reproduce the concurrent-write public API pattern with an external timeout | source integration test selector | covered |
| WCND-O7 | exclude Craft, handoff, publication, deployment, and default-alias mutation | Decision and Work Pack boundaries | covered |

## Selected evidence

1. `experiment/execution/wp0-provenance/RESULT.md` — package identity,
   integrity pass, and exact provenance block.
2. `experiment/execution/wp0-provenance/HISTORY-RECONSTRUCTION.md` —
   content-equivalence interpretation and remaining metadata contradiction.
3. `experiment/source-build/execution/task-sessions/SWU-WCSB-003/terminal-receipt.json`
   — Node 26 build/load pass and concurrent-write runtime block.
4. `experiment/source-build/.work/wcsb-20260805-node26-01/source/bindings/nodejs/test/integration.test.js`
   — exact 100-write `Promise.all` behavior selector.
5. `experiment/source-build/npm-diagnostic/plan/DECISION.md` — direct user
   selection and exact claim boundary.

## Exclusions

- Whole README/API corpus: excluded; it does not close another run obligation.
- Craft source trees: excluded; neither is needed to test package behavior.
- Inventory projections: excluded; direct owner evidence is available.
- Other Node/platform variants: deferred beyond this single diagnostic.

Strict coverage: pass. No unresolved planning question remains.
