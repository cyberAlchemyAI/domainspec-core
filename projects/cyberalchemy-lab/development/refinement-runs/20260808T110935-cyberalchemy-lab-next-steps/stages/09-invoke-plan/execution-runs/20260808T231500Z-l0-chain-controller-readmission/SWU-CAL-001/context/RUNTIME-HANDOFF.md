# Runtime Handoff Pack — SWU-CAL-001

## Identity

- Task/SWU: `TASK-CAL-CONTRACTS` / `SWU-CAL-001`
- Source task/work-pack: `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/WORK-PACK.md`
- Session/run id: `task-session-4f3bb4a4d9f21f2e1c8c`
- Session evidence path: `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/execution-runs/20260808T231500Z-l0-chain-controller-readmission/SWU-CAL-001/context/`
- Runtime handoff: `runtime`
- Repository revision: `8126a2f740f0ef5e924988908847dc2d5d84b48e`
- Evidence date: `2026-08-08`

## Obligation Coverage

| Obligation | Status | Selected Evidence | Resolution |
| --- | --- | --- | --- |
| `O1-profile` | covered | `08-distill-repair.md#Repair 1` | Implement only `cal-canonical-json-v1`: null, booleans, strings, arrays, objects, and JavaScript-safe integers. |
| `O2-rejection` | covered | `TASK-CAL-CONTRACTS.md#SWU-CAL-001`; `08-distill-repair.md#Repair 1` | Reject duplicate keys before materialization and reject float/exponent, `-0`, unsafe integer, and non-ASCII-key cases before hashing. |
| `O3-serialization` | covered | `TASK-CAL-CONTRACTS.md#Algorithm`; `08-distill-repair.md#Repair 1` | ASCII-sort object keys, preserve arrays, use ECMAScript string escaping, produce compact UTF-8 bytes, and SHA-256 them. |
| `O4-digest-binding` | covered | `08-distill-repair.md#Repair 1`; `ARCHITECTURE.md#Package self-binding rule` | Return profile/schema-tagged digest data; do not claim package-snapshot self-binding is implemented in this SWU. |
| `O5-scope` | covered | `L0-EXECUTION-CONTRACTS.json#/units/0`; `TASK-CAL-CONTRACTS.md#Write scope` | Create only the profile, pure `.mjs` module, and Node test; terminal evidence is an execution output. |
| `O6-validation` | covered | `TASK-CAL-CONTRACTS.md#Acceptance evidence`; `L0-EXECUTION-CONTRACTS.json#/units/0/validation_contracts/0` | Run the declared Node test; include two fixed byte/digest vectors and all stated rejection cases. |
| `O7-boundaries` | covered | `CONTEXT.md#Global invariants`; `TASK-CAL-CONTRACTS.md#Handoff note` | Do not create a package root, scaffold, other schema, dependency, network/file-system behavior, IDE change, Git operation, authority, promotion, or publication claim. |
| `O8-test-vector-choice` | resolved | `TASK-CAL-CONTRACTS.md#Acceptance evidence` | The contract leaves golden-vector contents open. Select reversible test-only values that prove key-order equivalence and UTF-8/escaping; record exact expected bytes and digests in the test. |

Strict coverage: `pass`

## Selected Sources

- `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/work-pack/tasks/TASK-CAL-CONTRACTS.md`
  - Selectors: `SWU-CAL-001`, especially Primary behavior through Handoff note.
  - Obligations: `O1-profile`, `O2-rejection`, `O3-serialization`, `O5-scope`, `O6-validation`, `O8-test-vector-choice`.
  - Evidence excerpt: declares the complete algorithm, exact three material paths, pure-function constraint, edge cases, and Node validation.
- `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/08-distill-repair.md`
  - Selectors: `Repair 1 — Closed canonical JSON profile`.
  - Obligations: `O1-profile`, `O2-rejection`, `O3-serialization`, `O4-digest-binding`.
  - Evidence excerpt: closes the value vocabulary and rules that supersede generic canonicalization.
- `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/work-pack/admission/L0-EXECUTION-CONTRACTS.json`
  - Selectors: `units[0]` for `SWU-CAL-001`.
  - Obligations: `O5-scope`, `O6-validation`, `O7-boundaries`.
  - Evidence excerpt: gives the exact material/execution-write partition, Node v22.13.0 test command, attempt receipt root, successor, and stop classes.
- `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/work-pack/shared/CONTEXT.md`
  - Selectors: `Global invariants` and `Expected execution result shape`.
  - Obligations: `O7-boundaries`.
  - Evidence excerpt: forbids package-root, dependency, IDE, Arcanum, network, and Git effects and fixes `authority_effect: none`.
- `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/06-invoke-design/ARCHITECTURE.md`
  - Selectors: `Package self-binding rule`.
  - Obligations: `O4-digest-binding`.
  - Evidence excerpt: reserves package self-binding for the later snapshot contract; this primitive may only supply the deterministic canonical bytes/digest it needs.
- `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/WORK-PACK.md`
  - Selectors: `SWU manifest and navigation`, `First-unit narrowness`, and closeout row `001`.
  - Obligations: `O5-scope`, `O7-boundaries`.
  - Evidence excerpt: keeps SWU-CAL-001 as a three-file trust primitive and names Invoke Refresh as a later owner-only closeout.

## Architecture Guidance

Use a dependency-free Node `.mjs` pure-function module. This unit establishes only the canonical JSON/digest primitive; package snapshots, compiler behavior, records, projection, fixtures, and workbench behavior belong to later SWUs.

## Related Feature Context

CyberAlchemy Lab remains a private, synthetic-contract-fixture candidate. The future IDE seam is explicitly deferred and cannot be touched by this unit.

## Constraints And Non-Goals

- Do not use a general RFC 8785 library or add any dependency/package root.
- Do not accept numeric values outside the JavaScript safe-integer profile.
- Do not perform filesystem or network I/O from the exported module.
- Do not write outside the three declared material paths before the Task Session terminal receipt.
- Do not infer source authority, promotion, publication, deployment, or production readiness.

## Write Scope

- `projects/cyberalchemy-lab/research/tower-evidence-navigator/schemas/canonical-json-profile.json`
- `projects/cyberalchemy-lab/research/tower-evidence-navigator/tools/canonical-json.mjs`
- `projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/canonical-json.test.mjs`

## Validation Surface

- `/home/vrondelli/.nvm/versions/node/v22.13.0/bin/node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/canonical-json.test.mjs`
- Acceptance-critical: both fixed golden byte/digest vectors and every declared rejection case must pass.

## Gaps And Blockers

- None. The only open implementation detail—test vector values—is resolved as a reversible test-only choice under `O8-test-vector-choice`.

## Authority Precedence

1. `L0-EXECUTION-CONTRACTS.json` exact write, runtime, validation, receipt, successor, and stop contract.
2. `TASK-CAL-CONTRACTS.md` SWU-CAL-001 behavior and done criteria.
3. `08-distill-repair.md` Repair 1 canonical profile.
4. `CONTEXT.md` global scope/effect ceilings and `ARCHITECTURE.md` downstream-only self-binding boundary.

## Fallback Exploration Rule

No broad exploration is authorized. Consult only a named missing obligation; record any additional source before using it. No fallback source is currently needed.

## Provenance

- Builder mode: `standard`, strict runtime handoff.
- Source hashes: `WORK-PACK.md=d8c5993deb19a431971b86ecd035ae842ac3a7f15fb042b34ab9018c1612a71a`; `TASK-CAL-CONTRACTS.md=42e4d751b0e130780f31bff0256f6c59f954af9c5cab5b4676b59e107e938d3f`; `CONTEXT.md=2ff29684e396576e1329333ffabae414c27deb3d8039c2480ddf2e3bb909778a`; `ARCHITECTURE.md=7e548375372b2cc8953587b61dab667509ed3d732a9080b565a292bcc11efd39`; `08-distill-repair.md=60ae6f32fb6561c0582b92f26b61fcc161fee2b764865cc438b4f5bfb0981f1d`; `L0-EXECUTION-CONTRACTS.json=adc7aadbf7bc0443645d45967d03c24a38d532832eb13bdab98ce2a19eeef982`.

## Output Paths

- Markdown: `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/execution-runs/20260808T231500Z-l0-chain-controller-readmission/SWU-CAL-001/context/RUNTIME-HANDOFF.md`
- JSON/index: `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/execution-runs/20260808T231500Z-l0-chain-controller-readmission/SWU-CAL-001/context/runtime-handoff-index.json`
