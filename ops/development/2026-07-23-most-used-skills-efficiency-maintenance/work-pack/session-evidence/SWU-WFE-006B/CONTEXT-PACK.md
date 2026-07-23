# Context Pack: SWU-WFE-006B

Status: strict coverage pass

Mode: lean

Lifecycle route: Sigil Development revision with Experiment Harness validation
and declared Decision Gate runtime regeneration

## Task boundary

Validate and consume one typed override for one exact target, scope, hazard, and
run. Reject ambient assent, malformed or stale overrides, target/scope/hazard
mismatch, and replay. Generic overrides never admit destructive, authority,
promotion, publication, or spend hazards; those remain routed to their owning
gate.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| DG1B-O1 | Override fields are typed and closed. | task required fields | covered |
| DG1B-O2 | Ambient assent and missing identity/target fail structurally. | accepted DG-1 finding | covered |
| DG1B-O3 | Live target, exact scope, and hazard must match. | task acceptance | covered |
| DG1B-O4 | Issued/expiry timestamps are parsed and stale/future-invalid evidence blocks. | task stale-receipt control | covered |
| DG1B-O5 | `consumed_by` must be null before admission and is persisted as the consuming run. | task one-use boundary | covered |
| DG1B-O6 | A second use blocks without changing the first consumer. | task replay matrix | covered |
| DG1B-O7 | Protected hazards remain with their owning gate and cannot be admitted by the generic override consumer. | task protected-gate rule; Design authority | covered |
| DG1B-O8 | Rejected inputs leave the override artifact byte-identical. | causal negative control | covered |
| DG1B-O9 | Exact reversible/non-protected override consumes once and emits a schema-valid receipt. | task positive control | covered |
| DG1B-O10 | SWU-WFE-006A prefilter behavior and canonical/generated parity remain passing. | dependency and lifecycle scope | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-006-DG-ADMISSIBILITY-OVERRIDE.md` | 006B behavior, fields, acceptance | complete SWU contract | `f08b22ef5310b1a34a5880e74f0a989b450229a82853260a5d47875c4fd10996` |
| `DESIGN.md` | override validator and authority rule | architecture boundary | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | DG-1 accepted finding | source requirement | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `arcanum/arcana/decision-gate/SKILL.md` | prefilter, process, authority rule | canonical target | `eaf4b9f000856ee409661e067c7387c4bff502962f38598c048099bd362bbfc5` |
| `work-pack/session-evidence/SWU-WFE-006A/receipt.json` | dependency closure | program-order proof | `2801ec8204bde90786c5dba99296a2100ef12e42d2db02c085376b27dd068a80` |

## Resolved design

- The mutable override artifact is the one-use state. Consumption occurs under
  an exclusive file lock, re-reads the current document, and persists the
  consuming run before returning `consumed`.
- Validation is exact equality over target, normalized scope set, and hazard.
- Rejected validation does not rewrite the override.
- The repository has no generic producer-owned schema that can prove arbitrary
  protected owner-gate receipts. Therefore a free-form receipt path cannot be
  treated as proof. Protected hazards always return `owner-gate-required` from
  the generic consumer. A future owner-specific adapter may consume its own
  typed receipt without weakening this rule.
- This narrowing preserves the accepted requirement: a generic override never
  bypasses destructive, authority, promotion, publication, or spend gates.

## Validation surface

```bash
bash arcanum/arcana/decision-gate/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/decision-gate .agents/skills/decision-gate .claude/skills/decision-gate
```

## Context Builder result

- Files selected: 5
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; implementation is local and bounded
