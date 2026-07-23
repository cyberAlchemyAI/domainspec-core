# Context Pack: SWU-WFE-005

Status: strict coverage pass

Mode: standard

Lifecycle route: Sigil Development revision with Experiment Harness validation
and declared Task Session runtime regeneration

## Task boundary

Make Task Session admit routed or reusable mutation only after it verifies a
current Invoke material-package receipt and binds that package to the live
selected task/SWU, controlling artifacts, dependency frontier, allowed writes,
validation surface, and authority/publication class. Standalone non-mutating
use remains unchanged, and post-mutation validation remains mandatory.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| TS2-O1 | Trigger the admission check only for routed or reusable mutation. | task acceptance; accepted TS-2 narrowing | covered |
| TS2-O2 | Validate the producer receipt with the exact producer-owned schema without copying Invoke package-validity logic. | task implementation rule 2; INV-1 schema | covered |
| TS2-O3 | Bind the producer package digest to the live selected task/SWU and controlling artifact identities/digests. | accepted TS-2 finding; Design interface | covered |
| TS2-O4 | Compare the live dependency frontier, allowed writes, validation surface, owner, authority, and publication class immediately before first write. | task primary behavior and implementation rule 3 | covered |
| TS2-O5 | Missing, stale, mismatched, expanded, or unclassified inputs block or rebuild before mutation. | task acceptance boundary | covered |
| TS2-O6 | A current exact receipt admits the routed mutation path. | task acceptance boundary | covered |
| TS2-O7 | Standalone non-mutating Task Session does not require an Invoke receipt. | accepted TS-2 narrowing | covered |
| TS2-O8 | Admission never replaces live post-mutation validation or lifecycle authority. | WFE-R02; task Done | covered |
| TS2-O9 | Add causal fixtures and retain all existing Task Session validation groups. | task receipt requirement; Experiment Harness | covered |
| TS2-O10 | Regenerate only declared Codex and Claude Task Session runtimes from canonical source. | task scope; public/generated boundary | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-005-TS-READINESS-RECEIPT.md` | objective, acceptance, rules, scope | complete SWU contract | `df720baf248886b2f68e0039d1e3268ef1dfbb92e1caf98a69a5710a0d5eed33` |
| `DESIGN.md` | routed readiness component and INV-1 to TS-2 interface | architecture boundary | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | TS-2 accepted finding and narrowing | source requirement | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `arcanum/arcana/task-session/SKILL.md` | scope, context, gates, first mutation, validation | canonical consumer contract | `e468531848bc54859f828418c74b029c33373c031fa49f189e3770e0fc7f8a72` |
| `arcanum/spells/invoke/schemas/material-package-receipt.schema.json` | complete schema | producer-owned receipt contract | `2c4ef7c0529f419278a3af530783383d05ccf8e144a40e895f26c2c2d6b77b6b` |
| `arcanum/spells/invoke/schemas/material-package.schema.json` | source, changes, targets, dependencies, validation | package fields bound by receipt digest | `f52810a2b08507f487cfc63e7b8619761a2803613098e6eb7cc46911288dc628` |
| `arcanum/spells/invoke/scripts/material_package_validator.py` | canonical digest and receipt production | producer behavior, not consumer code | `5012c5767f6dc0e76a0e34a63f4b65342883c7969b52e9b86e910c4c63ee1426` |
| `work-pack/session-evidence/SWU-WFE-003B/receipt.json` | INV-1 closure and residue | technical dependency receipt | `7ca01a7ae7ac3368aa58a00b3db2f0cf0721ef230807dd2f0faf36161a5d31c4` |
| `work-pack/session-evidence/SWU-WFE-004B/receipt.json` | W0 closure and unique successor | program-order dependency | `1c2398e45fcb88e631e8164163a086e1bc83f13954cb4dc7599a00fb2d4e8d35` |

## Resolved design

- The Invoke receipt remains the sole proof that the material package passed
  producer validation. Task Session reads that receipt through the exact Invoke
  schema path and does not copy the material-package validator.
- The full material package remains available behind `packageDigest`. Task
  Session recomputes that canonical digest, then performs only consumer-owned
  live binding checks over its declared sources, dependencies, targets,
  validation commands, and boundary classes.
- A Task Session admission request binds `taskId`, `swuId`, exact controlling
  artifact references, the dependency frontier, allowed writes, validation
  commands, lifecycle owner, authority class, and publication class.
- The resulting admission receipt conjunctively binds the live Task Session
  selection and the producer package. It is separate from the Invoke receipt;
  neither receipt gains lifecycle or mutation authority by itself.
- The check runs after scope/context/gate/runtime resolution and immediately
  before any local write or mutating runtime handoff.
- A standalone non-mutating request returns `not-applicable` without demanding
  material evidence.

## Validation surface

```bash
bash arcanum/arcana/task-session/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/task-session .agents/skills/task-session .claude/skills/task-session
```

The focused fixture matrix must include current exact admission plus absent
receipt, invalid receipt schema, stale source, mismatched task/SWU control,
changed dependency, expanded write scope, missing authority class, and
standalone non-mutating compatibility.

## Context Builder result

- Files selected: 9
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; implementation is local and bounded
