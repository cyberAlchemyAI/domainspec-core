# Work Pack Readiness Audit

- Canonical ID: `work-pack-readiness-audit`
- Verdict: `block`
- Snapshot: `d383ca91b3b00834dd36b017eda908af4222c3974e383c2b628338d9ef6d1992`; drift `false`
- Plan contract: `block`
- Runtime admission: `block`
- Receipt semantics: `block`
- Ready frontier: `SWU-OFSP-001`
- Selected unit: `none`
- Authority effect: `none`
- Mutation ready: `false`
- Next owner: `invoke:refresh`

## Finding Counts

- `attempt`: 5
- `closeout`: 4
- `command`: 24
- `path`: 2
- `receipt-semantics`: 1
- `runtime-admission`: 29
- `write-algebra`: 4

## Unit Results

| Unit | Plan | Runtime | Blockers |
| --- | --- | --- | --- |
| `SWU-OFSP-001` | `pass` | `block` | WPA-040 |
| `SWU-OFSP-002` | `block` | `block` | WPA-033, WPA-034, WPA-040, WPA-041 |
| `SWU-OFSP-003` | `block` | `block` | WPA-033, WPA-034, WPA-040, WPA-041, WPA-042 |
| `SWU-OFSP-004` | `block` | `block` | WPA-033, WPA-034, WPA-040, WPA-041, WPA-042, WPA-043 |
| `SWU-OFSP-005` | `block` | `block` | WPA-004, WPA-033, WPA-034, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044 |
| `SWU-OFSP-006` | `block` | `block` | WPA-004, WPA-005, WPA-033, WPA-034, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045 |
| `SWU-OFSP-007` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046 |
| `SWU-OFSP-008` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047 |
| `SWU-OFSP-009` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048 |
| `SWU-OFSP-010` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049 |
| `SWU-OFSP-011` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050 |
| `SWU-OFSP-012` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051 |
| `SWU-OFSP-013` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052 |
| `SWU-OFSP-014` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053 |
| `SWU-OFSP-015` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054 |
| `SWU-OFSP-016` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-033, WPA-034, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055 |
| `SWU-OFSP-017` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056 |
| `SWU-OFSP-018` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057 |
| `SWU-OFSP-019` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058 |
| `SWU-OFSP-020` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059 |
| `SWU-OFSP-021` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060 |
| `SWU-OFSP-022` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-022, WPA-023, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060, WPA-061 |
| `SWU-OFSP-023` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-022, WPA-023, WPA-024, WPA-025, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060, WPA-061, WPA-062 |
| `SWU-OFSP-024` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-022, WPA-023, WPA-024, WPA-025, WPA-026, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060, WPA-061, WPA-062, WPA-063 |
| `SWU-OFSP-025` | `block` | `block` | WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-022, WPA-023, WPA-024, WPA-025, WPA-026, WPA-027, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060, WPA-061, WPA-062, WPA-063, WPA-064 |
| `TASK-VERIFY` | `block` | `block` | WPA-001, WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-022, WPA-023, WPA-024, WPA-025, WPA-026, WPA-027, WPA-028, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060, WPA-061, WPA-062, WPA-063, WPA-064, WPA-065 |
| `TASK-AUDIT-ALIGNMENT` | `block` | `block` | WPA-001, WPA-002, WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-022, WPA-023, WPA-024, WPA-025, WPA-026, WPA-027, WPA-028, WPA-029, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060, WPA-061, WPA-062, WPA-063, WPA-064, WPA-065, WPA-066 |
| `TASK-AUDIT-LAYERING` | `block` | `block` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-022, WPA-023, WPA-024, WPA-025, WPA-026, WPA-027, WPA-028, WPA-029, WPA-030, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060, WPA-061, WPA-062, WPA-063, WPA-064, WPA-065, WPA-066, WPA-067 |
| `SWU-OFSP-026` | `block` | `block` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009, WPA-010, WPA-011, WPA-012, WPA-013, WPA-014, WPA-015, WPA-016, WPA-017, WPA-018, WPA-019, WPA-020, WPA-021, WPA-022, WPA-023, WPA-024, WPA-025, WPA-026, WPA-027, WPA-028, WPA-029, WPA-030, WPA-031, WPA-032, WPA-033, WPA-034, WPA-035, WPA-036, WPA-040, WPA-041, WPA-042, WPA-043, WPA-044, WPA-045, WPA-046, WPA-047, WPA-048, WPA-049, WPA-050, WPA-051, WPA-052, WPA-053, WPA-054, WPA-055, WPA-056, WPA-057, WPA-058, WPA-059, WPA-060, WPA-061, WPA-062, WPA-063, WPA-064, WPA-065, WPA-066, WPA-067, WPA-068 |

## Findings

### WPA-001 — unit has no full task contract

- Category: `closeout`
- Scope: `TASK-VERIFY`
- Evidence: contract_kind=row-only; contract=projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`

### WPA-002 — unit has no full task contract

- Category: `closeout`
- Scope: `TASK-AUDIT-ALIGNMENT`
- Evidence: contract_kind=row-only; contract=projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`

### WPA-003 — unit has no full task contract

- Category: `closeout`
- Scope: `TASK-AUDIT-LAYERING`
- Evidence: contract_kind=row-only; contract=projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`

### WPA-004 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-005`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`

### WPA-005 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-006`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`

### WPA-006 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-007`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`

### WPA-007 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-008`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`

### WPA-008 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-009`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-009 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-010`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-010 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-011`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-011 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-012`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-012 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-013`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-013 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-014`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-014 — attempt lifecycle is incomplete

- Category: `attempt`
- Scope: `SWU-OFSP-014`
- Evidence: attempt ID algorithm is empty; success teardown is empty; failure teardown is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-015 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-016`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-016 — attempt lifecycle is incomplete

- Category: `attempt`
- Scope: `SWU-OFSP-016`
- Evidence: attempt ID algorithm is empty; success teardown is empty; failure teardown is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-017 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-017`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`

### WPA-018 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-018`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`

### WPA-019 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-019`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`

### WPA-020 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-020`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-021 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-021`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-022 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-022`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-023 — attempt lifecycle is incomplete

- Category: `attempt`
- Scope: `SWU-OFSP-022`
- Evidence: attempt ID algorithm is empty; success teardown is empty; failure teardown is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-024 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-023`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-025 — attempt lifecycle is incomplete

- Category: `attempt`
- Scope: `SWU-OFSP-023`
- Evidence: attempt ID algorithm is empty; success teardown is empty; failure teardown is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-026 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-024`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`

### WPA-027 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-025`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`

### WPA-028 — unit has no exact validation argv contract

- Category: `command`
- Scope: `TASK-VERIFY`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`

### WPA-029 — unit has no exact validation argv contract

- Category: `command`
- Scope: `TASK-AUDIT-ALIGNMENT`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`

### WPA-030 — unit has no exact validation argv contract

- Category: `command`
- Scope: `TASK-AUDIT-LAYERING`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`

### WPA-031 — unit has no exact validation argv contract

- Category: `command`
- Scope: `SWU-OFSP-026`
- Evidence: validation_commands is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-032 — attempt lifecycle is incomplete

- Category: `attempt`
- Scope: `SWU-OFSP-026`
- Evidence: attempt ID algorithm is empty; success teardown is empty; failure teardown is empty
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-033 — cross-unit write overlap has no exact shared owner contract

- Category: `write-algebra`
- Scope: `work-pack`
- Evidence: cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json: SWU-OFSP-002, SWU-OFSP-005, SWU-OFSP-006, SWU-OFSP-017, SWU-OFSP-024, SWU-OFSP-025
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/WORK-PACK.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CONTEXT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/TASK-SESSION-RECEIPT.schema.json`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-034 — cross-unit write overlap has no exact shared owner contract

- Category: `write-algebra`
- Scope: `work-pack`
- Evidence: cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json: SWU-OFSP-002, SWU-OFSP-005, SWU-OFSP-006, SWU-OFSP-017, SWU-OFSP-024, SWU-OFSP-025
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/WORK-PACK.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CONTEXT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/TASK-SESSION-RECEIPT.schema.json`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-035 — cross-unit write overlap has no exact shared owner contract

- Category: `write-algebra`
- Scope: `work-pack`
- Evidence: cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/projectScene.ts: SWU-OFSP-017, SWU-OFSP-024
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/WORK-PACK.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CONTEXT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/TASK-SESSION-RECEIPT.schema.json`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-036 — cross-unit write overlap has no exact shared owner contract

- Category: `write-algebra`
- Scope: `work-pack`
- Evidence: cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/serializeSemanticState.ts: SWU-OFSP-007, SWU-OFSP-008
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/WORK-PACK.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CONTEXT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/TASK-SESSION-RECEIPT.schema.json`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-037 — source selector is ambiguous, missing, or escapes the repository

- Category: `path`
- Scope: `source-selector`
- Evidence: missing path: findings.md
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/WORK-PACK.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CONTEXT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/TASK-SESSION-RECEIPT.schema.json`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-038 — source selector is ambiguous, missing, or escapes the repository

- Category: `path`
- Scope: `source-selector`
- Evidence: missing path: synthesis.md
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/WORK-PACK.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CONTEXT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/TASK-SESSION-RECEIPT.schema.json`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-039 — closeout directory is absent and has no atomic creation contract

- Category: `closeout`
- Scope: `work-pack`
- Evidence: projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/closeout
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/WORK-PACK.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CONTEXT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/TASK-SESSION-RECEIPT.schema.json`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`, `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-040 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-001`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`

### WPA-041 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-002`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`

### WPA-042 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-003`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`

### WPA-043 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-004`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-FOUNDATION.md`

### WPA-044 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-005`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`

### WPA-045 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-006`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`

### WPA-046 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-007`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`

### WPA-047 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-008`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`

### WPA-048 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-009`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-049 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-010`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-050 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-011`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-051 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-012`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-052 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-013`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-053 — live routed mutation requires material writes for a non-material task

- Category: `runtime-admission`
- Scope: `SWU-OFSP-014`
- Evidence: task_class=output-only; execution_outputs=1; no placeholder material write may be invented
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`

### WPA-054 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-015`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`

### WPA-055 — live routed mutation requires material writes for a non-material task

- Category: `runtime-admission`
- Scope: `SWU-OFSP-016`
- Evidence: task_class=output-only; execution_outputs=1; no placeholder material write may be invented
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`

### WPA-056 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-017`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PROJECTION.md`

### WPA-057 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-018`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`

### WPA-058 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-019`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-STATE.md`

### WPA-059 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-020`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-060 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-021`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-NATIVE-UI.md`

### WPA-061 — live routed mutation requires material writes for a non-material task

- Category: `runtime-admission`
- Scope: `SWU-OFSP-022`
- Evidence: task_class=output-only; execution_outputs=1; no placeholder material write may be invented
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`

### WPA-062 — live routed mutation requires material writes for a non-material task

- Category: `runtime-admission`
- Scope: `SWU-OFSP-023`
- Evidence: task_class=output-only; execution_outputs=1; no placeholder material write may be invented
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-ACCEPTANCE.md`, `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`

### WPA-063 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-024`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`

### WPA-064 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-025`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-RELIABILITY.md`

### WPA-065 — live routed mutation requires material writes for a non-material task

- Category: `runtime-admission`
- Scope: `TASK-VERIFY`
- Evidence: task_class=audit-only; execution_outputs=1; no placeholder material write may be invented
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`

### WPA-066 — live routed mutation requires material writes for a non-material task

- Category: `runtime-admission`
- Scope: `TASK-AUDIT-ALIGNMENT`
- Evidence: task_class=audit-only; execution_outputs=1; no placeholder material write may be invented
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`

### WPA-067 — live routed mutation requires material writes for a non-material task

- Category: `runtime-admission`
- Scope: `TASK-AUDIT-LAYERING`
- Evidence: task_class=audit-only; execution_outputs=1; no placeholder material write may be invented
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/shared/CLOSEOUT-CONTRACT.md`, `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`

### WPA-068 — material mutation lacks current material-package admission evidence

- Category: `runtime-admission`
- Scope: `SWU-OFSP-026`
- Evidence: material_package is null
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/work-pack/tasks/TASK-PACKAGE.md`

### WPA-069 — terminal receipt contract is fail-open

- Category: `receipt-semantics`
- Scope: `terminal-receipt`
- Evidence: unit_id is not explicitly type string; artifacts may be empty; validation may be empty; artifact entries allow unowned fields; validation entries allow unowned fields; artifact sha256 is not explicitly type string; pass status is not conditionally bound to passing validation and no blockers; no semantic validator binds unit/step/work-pack/successor
- Targets: `projects/body-war/development/invoke-runs/20260730T050022Z-ontology-focus-scene-pivot/TASK-SESSION-RECEIPT.schema.json`

## Claim Ceiling

This report is an audit-only preflight. It selects and executes no unit, authorizes no mutation, and applies no refresh.
