# Context Pack: SWU-WFE-006A

Status: strict coverage pass

Mode: lean

Lifecycle route: Sigil Development revision with Experiment Harness validation
and declared Decision Gate runtime regeneration

## Task boundary

Add one deterministic option-admissibility prefilter. It accepts typed
owner-supplied structural evidence, rejects inadmissible or unsafe-unowned
candidates before human presentation, and routes the remaining cardinality:
zero to `block`, one to `direct`, and two or more to `gate`. It does not choose
among viable options and does not implement override consumption.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| DG1A-O1 | Candidate options have typed identity, kind, structural status, reversibility, hazard, evidence, reasons, and owner gate. | task input contract | covered |
| DG1A-O2 | Structurally inadmissible options never reach a human gate. | accepted DG-1 finding | covered |
| DG1A-O3 | Protected or irreversible candidates without an owning gate are rejected before cardinality routing. | task owner-gate input; Design authority rule | covered |
| DG1A-O4 | Zero admissible options returns structural `block`. | task acceptance | covered |
| DG1A-O5 | One admissible option returns `direct` through its declared owner gate when present. | task acceptance and verifier correction | covered |
| DG1A-O6 | Two or more admissible options return `gate` without selecting one. | accepted DG-1 finding | covered |
| DG1A-O7 | Defer and stop remain legitimate candidate kinds. | task handoff note | covered |
| DG1A-O8 | Duplicate IDs and invalid evidence/status combinations fail closed. | deterministic structural boundary | covered |
| DG1A-O9 | Typed override validation remains isolated in SWU-WFE-006B. | task split | covered |
| DG1A-O10 | Canonical and declared generated runtimes synchronize and full fixtures pass. | task scope and lifecycle contract | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-006-DG-ADMISSIBILITY-OVERRIDE.md` | 006A behavior, inputs, acceptance, scope | complete SWU contract | `2b4d3885d5bcbb8e61373fbec2e5eb82c6f9ad5423e1bf744cf581d67c7d1d4a` |
| `DESIGN.md` | Decision Gate prefilter and decision flow | architecture boundary | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | DG-1 accepted finding and verifier correction | source requirement | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `arcanum/arcana/decision-gate/SKILL.md` | applicability, process, authority, output | canonical target | `0c86d26cacb5c7d6767476029a398eac2116e609111045aa58c48064568076ba` |
| `arcanum/arcana/decision-gate/README.md` | pass/block model and deterministic-rule exclusion | public explanation | `7a8f77b0c212d878663e45d5bf69f3f79d3582e699b9e23ba647edf8ca65ee98` |
| `work-pack/session-evidence/SWU-WFE-005/receipt.json` | dependency closure and successor | program-order proof | `88e2077eda8913ecaa39cd5eabbf611b56ab04b4178f85a593ec40d11aae04b5` |

## Resolved design

- Decision Gate consumes structural verdicts produced by the caller or owning
  validator; it does not infer application-specific validity.
- A candidate marked inadmissible must carry reasons. A candidate marked
  admissible must carry evidence and no rejection reason.
- Destructive, authority, promotion, publication, and spend hazards, plus any
  irreversible candidate, require a named owner gate. Missing ownership makes
  that candidate inadmissible before cardinality is counted.
- `direct` is routing, not execution or consent. The output names the one
  option and its owning gate; the caller still runs that owner.
- `gate` never selects an option. It returns only the admissible candidate IDs
  that may be presented.
- `block` reports rejected candidates and why no admissible route remains.

## Validation surface

```bash
bash arcanum/arcana/decision-gate/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/decision-gate .agents/skills/decision-gate .claude/skills/decision-gate
```

## Context Builder result

- Files selected: 6
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; implementation is local and bounded
