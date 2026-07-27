# Context Pack — SWU-BWOI-003

## Selected Unit

- Work pack: `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/WORK-PACK.md`
- Task: `TASK-BWOI-INTEGRATION`
- SWU: `SWU-BWOI-003`
- Layer / wave: `L2` / `W2`
- Execution owner: `local-fallback`

## Objective

Admit integration only when the current ontology receipt, DomainSpec receipt,
bridge manifest, nested handles, and experimental ontology state all match.
After admission, reuse the existing canonical CT-2 runner and require its case
and receipt bytes to remain identical.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Bind both accepted standalone receipts by exact digest. | work pack, task, parent receipts | covered |
| O2 | Reject stale ontology-entry digests. | task algorithm and T-INTEGRATION-001 | covered |
| O3 | Reject candidate state when the profile requires promoted. | task algorithm and W2 exit gate | covered |
| O4 | Reject executable logic copied into the bridge. | architecture bridge rule | covered |
| O5 | Resolve exact node, module, and clause handles. | DomainSpec receipt | covered |
| O6 | Reuse the exact DomainSpec case and backend observation path. | DomainSpec receipt and runner | covered |
| O7 | Emit deterministic bridge and integration receipts. | task outputs and acceptance evidence | covered |
| O8 | Preserve authority and release claim ceilings. | task, SPEC acceptance boundary | covered |

## Selected Sources

| Source | Selectors | Obligations |
| --- | --- | --- |
| `WORK-PACK.md` | selected SWU, closeout row, blockers | O1, O7, O8 |
| `TASK-BWOI-INTEGRATION.md` | algorithm, write scope, done criteria, validation | O1-O8 |
| `W2.md` | entry and exit gates | O2-O4, O7 |
| `SPEC.md` | `T-INTEGRATION-001`, acceptance boundary | O1-O3, O6, O8 |
| `ARCHITECTURE.md` | Bridge Manifest, workflow steps 9-12 | O1-O6, O8 |
| `ontology-receipt.json` | entry digests, status, claim ceiling | O1-O3, O8 |
| `domainspec-receipt.json` | canonical handles, build digests, case identity | O1, O5-O8 |

## Resolved Tension

The Architecture example spells the module handle as
`body-war.create-suggested-track`; the completed canonical DomainSpec receipt
and runner use `body-war.CreateSuggestedTrack.logic`. Exact current canonical
evidence controls, so the bridge binds the latter. No source contract is
rewritten.

## Write Boundary

Implementation writes are restricted to the task’s declared bridge directory,
the two integration source files, the integration test, and the integration
receipt. Task Session evidence is restricted to this session directory.

`cyberAlchemy/ontology/`, `projects/domainspec-v2/`, the Body War application,
and both standalone proof packages remain read-only.

## Context Builder Result

- Mode: standard
- Files selected: 7
- Obligation coverage: 8/8, 100%
- Strict coverage: pass
- Runtime handoff: none
- Blockers: 0

