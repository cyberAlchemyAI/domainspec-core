# Context Pack: Invoke Public-Hygiene Repair

- Mode: lean
- Strict coverage: pass
- Task: `TASK.md`
- Files selected: 5
- Obligation coverage: 100%
- Runtime handoff: none; local execution
- Subagents: none

## Obligation map

| Obligation | Controlling evidence | Selector |
| --- | --- | --- |
| PH-01 remove four exact findings | prior leakage report | `repo_wide_diagnostic.hits` |
| PH-02 preserve lifecycle truth | prior final audit | `residue`, `authority` |
| PH-03 preserve source claim bounds | Distill evidence README/context | provenance and claim-bound paragraphs |
| PH-04 keep executable example portable | template example runbook | `CODEX_BIN` example |
| PH-05 avoid silent scope expansion | repository scan | `projects/ide-extension` bindings classified separately |

## Baselines

- Distill evidence README:
  `dbc03d32f3afbff0a9c6c95435c4cdaf718bc19ad5a8c0a802fb05afab5b61fe`
- Template example runbook:
  `8154f7a8a3196f13a1247d1f452e519ff0f32ed5d32f4fb1ce9876b5a4d68a92`
- Shared context:
  `0ea1cb4c1f04f08017270eedb844a8fe2073264feb4abbd3a6db366eff89502f`

The pack is session evidence, not a new public authority source.
