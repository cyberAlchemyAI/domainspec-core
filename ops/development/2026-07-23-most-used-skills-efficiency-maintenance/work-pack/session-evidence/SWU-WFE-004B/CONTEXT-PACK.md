# Context Pack: SWU-WFE-004B

Status: strict coverage pass

Mode: lean

Lifecycle route: repository-local Inventory producer hardening; canonical sigil
contract unchanged

## Task boundary

Reject unsupported `kind` values in the deterministic Inventory updater before
any write. Preserve all seven existing structural kinds, current deterministic
serialization, supported `entry` and `query` behavior, and idempotent no-op
semantics.

## Obligation matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| INT1B-O1 | Admission uses the same closed seven-value enum as the canonical validator. | validator and task contract | covered |
| INT1B-O2 | Unsupported input rejects before JSON or Markdown write. | CLI write order and new negative control | covered |
| INT1B-O3 | Pure updater input remains unmutated on rejection. | `addRecord` pure contract | covered |
| INT1B-O4 | Supported `entry` and `query` inputs remain accepted and idempotent. | existing fixture pattern plus new positive controls | covered |
| INT1B-O5 | Existing six deterministic regression groups remain green. | current focused suite baseline | covered |
| INT1B-O6 | No enum extension, index migration, source-entry change, or canonical sigil mutation. | 004B forbidden scope | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `WORK-PACK.md` | selected SWU and current action | live execution authority | `a89e3b424d6b1d3e043b2f0a38602d612f0d5df43d33f570b88234d4238487d7` |
| `work-pack/swu-manifest.json` | SWU-WFE-004B | exact scope and acceptance | `dc6d23732938f7fe18652e195a24d2754169ff82a032662514c1fea65c3fdf40` |
| `work-pack/tasks/TASK-WFE-004-INVENTORY-KIND-CONTRACT.md` | 004B boundary and validation | task contract | `72c370e7b705cbf345fb494b02e69b49df02d5f6cec7e0faaf31cae7531392be` |
| `.arcanum/inventory/tools/inventory-update.cjs` | `normalizeEntry`, `addRecord`, pre-write validation, CLI write order | implementation target | `df8a25d9b46b811a777fc0bd52fa4cb29d38cde348bd0ff500256fa8c90d8a50` |
| `.arcanum/inventory/tools/test/test-inventory-update.cjs` | six baseline groups | existing focused harness | `a70bcff491922df58cb5fc3fa8e90ea6d7d860c7076f455479939ed71deca55e` |
| `arcanum/arcana/inventory/scripts/validate-index-json.sh` | supported kind enum | canonical compatibility surface | `b9306a877bd0df3fb8ec704f7dfcc68897e515f64172ecdc194471b74823360a` |

## Constraints

- Add the guard in `normalizeEntry`, before an entry can reach indexes or
  filesystem writes.
- Use the exact canonical set: `page`, `entry`, `query`, `lint`,
  `raw-manifest`, `evidence-card-bundle`, `evidence-set-bundle`.
- Add a stable CLI error path so rejection exits non-zero without a stack trace
  or writes.
- Test both the pure function and the real CLI over temporary files.
- Do not touch current Inventory data, canonical Arcanum sources, generated
  runtime packages, or the supported-kind enum.

## Write scope

- `.arcanum/inventory/tools/inventory-update.cjs`
- `.arcanum/inventory/tools/test/test-inventory-update.cjs`
- this SWU's session evidence

## Validation surface

```bash
node .arcanum/inventory/tools/test/test-inventory-update.cjs
node .arcanum/inventory/tools/test/test-index-md.cjs
git diff --check -- .arcanum/inventory/tools
```

## Context Builder result

- Files selected: 6
- Obligation coverage: 6/6
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none
