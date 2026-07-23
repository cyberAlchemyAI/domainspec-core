# Context Pack: SWU-WFE-004A

Status: strict coverage pass

Mode: standard

Lifecycle route: repository-local Inventory sync and validation; no canonical
Inventory sigil mutation

## Task boundary

Normalize exactly 15 unsupported `kind` aliases in
`.arcanum/inventory/index.json`. Map `strategy-result` rows under `entries/` to
`entry`, and `query-file`, `research-findings`, or `research-transcript` rows
under `queries/` to `query`. Preserve IDs, paths, types, all other entry fields,
entry order, derived indexes, top-level fields, and existing unrelated dirty
Inventory changes.

## Obligation matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| INT1A-O1 | Current invalid count is exactly 15. | machine-index-first `jq` query | covered |
| INT1A-O2 | Mapping is closed to four aliases and path-qualified. | task algorithm and before projection | covered |
| INT1A-O3 | Every non-kind field remains identical. | per-entry canonical non-kind SHA-256 | covered |
| INT1A-O4 | Entry order and complete derived indexes remain identical. | baseline order and indexes SHA-256 | covered |
| INT1A-O5 | Invalid count becomes zero and the canonical validator passes. | declared validation surface | covered |
| INT1A-O6 | Current unrelated Inventory changes are preserved. | scoped dirty diff and exact-ID mutation | covered |
| INT1A-O7 | Human index remains synchronized. | `index.md` rows do not project `kind`; no content delta required | resolved |
| INT1A-O8 | Record the Inventory sync without rewriting prior log entries. | append-only `log.md` convention | covered |
| INT1A-O9 | Do not change the enum, updater, entry source files, or authority. | 004A forbidden scope | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `WORK-PACK.md` | selected SWU and current action | live execution authority | `bb1d76427ffe981077741e10bc856ab523bbd32cdd950b4c748fdd6664257775` |
| `work-pack/swu-manifest.json` | SWU-WFE-004A | exact write scope and acceptance | `050d8ad13cc75155a4e1fa6a90f10b6c63d41d782f2ff0ea645e876d1dc2661c` |
| `work-pack/tasks/TASK-WFE-004-INVENTORY-KIND-CONTRACT.md` | 004A algorithm, boundary, validation | task contract | `0db776b9c107da26a366bdebec27889f007dbaa0e956e038a8edc1a94aedfa66` |
| `.arcanum/inventory/index.json` | 15 unsupported-kind entries and derived indexes | primary machine read model | `c608ebf6bc6384a44295d2f614a0821da76802ea552d01a26854c9bfd5ef6ebe` |
| `.arcanum/inventory/index.md` | Entries and Query Files tables | human projection; `kind` is not rendered | `d1c6439209ea801254203ad7c2c219a4f44087d4919c49a46ad97e556ebc1dca` |
| `.arcanum/inventory/log.md` | append-only sync convention | required durable maintenance record | `04bb63f84886f3b6c0f4e8e2cd4385fc5b2cd9b184480f8713e7e081cebf53ff` |
| `arcanum/arcana/inventory/scripts/validate-index-json.sh` | supported `kind` enum and structural checks | acceptance validator | `b9306a877bd0df3fb8ec704f7dfcc68897e515f64172ecdc194471b74823360a` |
| `.agents/skills/inventory/SKILL.md` | machine-index and sync contracts | runtime owner guidance | `04670077db949dfe76c01f299bd9f93ed71fff854ad45d0dc0004e2d4499191f` |

## Dirty-worktree assessment

- `index.json`, `index.md`, and `log.md` already contain unrelated Inventory
  additions that must remain.
- Fourteen invalid rows already exist at `HEAD` and are semantically identical
  in the current file.
- One invalid row,
  `iolm-workable-example-research-strategy-result-synthesis`, is part of the
  current uncommitted Inventory additions.
- No historical invalid row is missing or semantically changed.
- The mutation is restricted to the 15 exact `kind` fields. Existing additions,
  timestamps, ordering, indexes, human rows, and log history remain intact.

## Write scope

- `.arcanum/inventory/index.json`
- `.arcanum/inventory/log.md`
- this SWU's session evidence

`index.md` is validation-only because it does not render `kind`.

## Validation surface

```bash
bash arcanum/arcana/inventory/scripts/validate-index-json.sh .arcanum/inventory/index.json
jq -e '[.entries[] | select(.kind | IN("page","entry","query","lint","raw-manifest","evidence-card-bundle","evidence-set-bundle") | not)] | length == 0' .arcanum/inventory/index.json
python3 work-pack/session-evidence/SWU-WFE-004A/validate-migration.py
git diff --check -- .arcanum/inventory/index.json .arcanum/inventory/log.md
```

## Context Builder result

- Files selected: 8
- Obligation coverage: 9/9
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none
