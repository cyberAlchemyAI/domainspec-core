# Work Pack Readiness Audit

- Canonical ID: `work-pack-readiness-audit`
- Verdict: `block`
- Snapshot: `4b033a415458b9136f51de39566f2403c978a3462d69e0a10c5b86b4cd829c9f`; drift `false`
- Plan contract: `block`
- Runtime admission: `block`
- Receipt semantics: `block`
- Ready frontier: `SWU-AKV-QRY-001`
- Selected unit: `none`
- Authority effect: `none`
- Mutation ready: `false`
- Next owner: `invoke:refresh`

## Finding Counts

- `command`: 5
- `path`: 3
- `receipt-semantics`: 1
- `runtime-admission`: 5

## Unit Results

| Unit | Plan | Runtime | Blockers |
| --- | --- | --- | --- |
| `SWU-AKV-QRY-001` | `block` | `block` | WPA-001, WPA-009 |
| `SWU-AKV-QRY-002` | `block` | `block` | WPA-001, WPA-002, WPA-009, WPA-010 |
| `SWU-AKV-QRY-003` | `block` | `block` | WPA-001, WPA-002, WPA-003, WPA-009, WPA-010, WPA-011 |
| `SWU-AKV-QRY-004` | `block` | `block` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-009, WPA-010, WPA-011, WPA-012 |
| `SWU-AKV-QRY-005` | `block` | `block` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-005, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013 |

## Findings

### WPA-001 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-AKV-QRY-001`
- Evidence: invalid relative path: .
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-POLICY.md`

### WPA-002 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-AKV-QRY-002`
- Evidence: invalid relative path: .
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-SCHEMA.md`

### WPA-003 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-AKV-QRY-003`
- Evidence: invalid relative path: .
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-MIGRATION.md`

### WPA-004 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-AKV-QRY-004`
- Evidence: invalid relative path: .
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-VALIDATOR.md`

### WPA-005 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-AKV-QRY-005`
- Evidence: invalid relative path: .
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-REPLAY.md`

### WPA-006 — source selector is ambiguous, missing, or escapes the repository

- Category: `path`
- Scope: `source-selector`
- Evidence: missing path: projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-query-contract-matrix.json#closed_abstention_vocabulary
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/WORK-PACK.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-POLICY.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-SCHEMA.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-MIGRATION.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-VALIDATOR.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-REPLAY.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/PLAN-TRANSPORT.json`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/HANDOFF-STATE.json`

### WPA-007 — source selector is ambiguous, missing, or escapes the repository

- Category: `path`
- Scope: `source-selector`
- Evidence: missing path: projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-query-contract-matrix.json#planned_fixtures
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/WORK-PACK.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-POLICY.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-SCHEMA.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-MIGRATION.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-VALIDATOR.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-REPLAY.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/PLAN-TRANSPORT.json`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/HANDOFF-STATE.json`

### WPA-008 — source selector is ambiguous, missing, or escapes the repository

- Category: `path`
- Scope: `source-selector`
- Evidence: missing path: projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/task-sessions/20260803T191537Z-SWU-AKV-NV-001/CLOSEOUT-PREFLIGHT.json#blockers
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/WORK-PACK.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-POLICY.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-SCHEMA.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-MIGRATION.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-VALIDATOR.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-REPLAY.md`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/PLAN-TRANSPORT.json`, `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/HANDOFF-STATE.json`

### WPA-009 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-AKV-QRY-001`
- Evidence: material_package is null
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-POLICY.md`

### WPA-010 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-AKV-QRY-002`
- Evidence: material_package is null
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-SCHEMA.md`

### WPA-011 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-AKV-QRY-003`
- Evidence: material_package is null
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-MIGRATION.md`

### WPA-012 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-AKV-QRY-004`
- Evidence: material_package is null
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-VALIDATOR.md`

### WPA-013 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-AKV-QRY-005`
- Evidence: material_package is null
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/work-pack/tasks/TASK-AKV-QRY-REPLAY.md`

### WPA-014 — terminal receipt contract is fail-open

- Category: `receipt-semantics`
- Scope: `terminal-receipt`
- Evidence: unit_id is not explicitly type string
- Targets: `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/TASK-SESSION-TERMINAL-RECEIPT.schema.json`

## Claim Ceiling

This report is an audit-only preflight. It selects and executes no unit, authorizes no mutation, and applies no refresh.
