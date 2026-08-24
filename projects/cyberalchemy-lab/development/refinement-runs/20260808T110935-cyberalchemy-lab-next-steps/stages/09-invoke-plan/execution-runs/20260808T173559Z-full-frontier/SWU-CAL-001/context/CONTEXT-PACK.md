# Runtime Handoff Pack — SWU-CAL-001

## Identity

- Task/SWU: `TASK-CAL-CONTRACTS / SWU-CAL-001`
- Source work pack: `stages/09-invoke-plan/WORK-PACK.md`
- Run id: `CAL-L0-FULL-FRONTIER-20260808T173559Z`
- Runtime handoff: `local Task Session`
- Repository revision: `8126a2f740f0ef5e924988908847dc2d5d84b48e`
- Evidence date: `2026-08-08`
- Fast-entry guard: `TASK_READY`; receipt `feg-0b7b6f4fd9a0438058fb190b`

## Obligation Coverage

| Obligation | Status | Selected evidence | Resolution |
| --- | --- | --- | --- |
| `CAL001-O1` closed value profile | covered | `08-distill-repair.md#Repair 1` | accept JSON null/boolean/string/array/object and safe integers only |
| `CAL001-O2` pre-materialization rejection | covered | `TASK-CAL-CONTRACTS.md#SWU-CAL-001` | scan duplicate keys and forbidden number forms before `JSON.parse` |
| `CAL001-O3` deterministic bytes | covered | `08-distill-repair.md#Repair 1` | ASCII-byte key order, preserved arrays, ECMAScript string escaping, UTF-8, no whitespace |
| `CAL001-O4` digest domain separation | covered | `08-distill-repair.md#Repair 1` | every digest preimage binds profile ID and schema version |
| `CAL001-O5` pure boundary | covered | `TASK-CAL-CONTRACTS.md#SWU-CAL-001` | pure exported functions; no filesystem, network, package root, or downstream scaffold |
| `CAL001-O6` exact write partition | covered | `L0-EXECUTION-CONTRACTS.json#/units/0` | three material files plus one validation-owned terminal receipt |
| `CAL001-O7` acceptance proof | covered | `TASK-CAL-CONTRACTS.md#SWU-CAL-001` | Node test, valid/invalid vectors, and two fixed byte/digest golden vectors |
| `CAL001-O8` closeout availability | covered | `WORK-PACK.md#Task Session closeout synchronization contract` | exact Invoke Refresh owner route and unique successor `SWU-CAL-002` |

Strict coverage: `pass`.

## Selected Sources

- `stages/08-distill-repair.md`
  - Selector: `Repair 1 — Closed canonical JSON profile`
  - Controls: domain, key order, number restrictions, duplicate-key timing, encoding, and digest tagging.
- `stages/09-invoke-plan/work-pack/tasks/TASK-CAL-CONTRACTS.md`
  - Selector: `SWU-CAL-001 — Canonical JSON and digest primitive`
  - Controls: behavior, algorithm, failure cases, done criteria, and non-goals.
- `stages/09-invoke-plan/work-pack/admission/L0-EXECUTION-CONTRACTS.json`
  - Selector: `/units/0`
  - Controls: exact owner, write partitions, command, runtime, receipt, successor, and stop classes.
- `stages/09-invoke-plan/WORK-PACK.md`
  - Selectors: `Objective summary`, `SWU manifest and navigation`, `Task Session closeout synchronization contract`
  - Controls: L0 ceiling, order, closeout inventory, and successor.
- `stages/06-invoke-design/ARCHITECTURE.md`
  - Selector: `Package self-binding rule`
  - Context only: establishes a downstream consumer of canonical bytes; self-binding is not implemented by this SWU.
- `SWU-CAL-001/fast-execution-entry-receipt.json`
  - Selector: complete typed receipt
  - Controls: permits Context Builder entry only for the exact selected unit, semantic digest, binding, and route fingerprint.

## Constraints And Non-Goals

- The candidate is private, synthetic, and has `authority_effect: none`.
- Do not add a package root or external dependency.
- Do not create Research Tower, fixture, projection, IDE, server, browser, publication, promotion, or external-effect files.
- Do not broaden canonical JSON beyond `cal-canonical-json-v1` without a new decision and profile version.
- Preserve the exact declared Node runtime command.

## Write Scope

- `projects/cyberalchemy-lab/research/tower-evidence-navigator/schemas/canonical-json-profile.json`
- `projects/cyberalchemy-lab/research/tower-evidence-navigator/tools/canonical-json.mjs`
- `projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/canonical-json.test.mjs`
- `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-001.json`

## Validation Surface

- `/home/vrondelli/.nvm/versions/node/v22.13.0/bin/node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/canonical-json.test.mjs`

## Gaps And Blockers

- None. Product mutation remains separately gated by material-package validation and single-use mutation admission.

## Authority Precedence

1. Frozen `L0-EXECUTION-CONTRACTS.json#/units/0` machine contract.
2. `TASK-CAL-CONTRACTS.md#SWU-CAL-001` task semantics.
3. `08-distill-repair.md#Repair 1` repaired canonical profile.
4. `WORK-PACK.md` delivery and closeout boundary.
5. Stage 06 downstream self-binding context.

## Fallback Exploration Rule

No broad exploration is authorized. Stop and route semantic contradictions or scope expansion through the declared stop policy.

## Output Paths

- Markdown: this file.
- JSON/index: `context-index.json` beside this file.
