# TASK-AUDIT-ALIGNMENT: Semantic Alignment Audit

## Goal

Audit implementation fidelity against Sonar Loop DomainSpec contracts after mutation-capable stages.

## DomainSpec Coverage

All SPEC concept IDs, operation IDs, rule IDs, workflow IDs, interface IDs, and observability IDs listed in [../../SPEC.md](../../SPEC.md) and [../shared/04-traceability.md](../shared/04-traceability.md).

## Architecture References

- Semantic alignment findings must be reconciled before readiness closure.
- If implementation and DomainSpec docs diverge, DomainSpec docs remain authoritative unless explicitly updated through a spec-change task.

## Implementation Directives

- Run `domainspec-audit-alignment sonar-loop` after W1-W4 mutation-capable stages.
- Consolidate findings with layering audit results into one dependency-ordered remediation track.
- Require explicit evidence for any accepted deviation.

## Gaps and Questions

- None at planning time.

## Decision Lock

- D-001 and D-002 are expected behavior constraints during the audit.
