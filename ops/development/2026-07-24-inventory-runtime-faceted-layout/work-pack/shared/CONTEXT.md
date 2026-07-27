# Shared Execution Context

## Approved Sources

- [SPEC.md](../../SPEC.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)
- `ops/development/2026-07-24-inventory-runtime-research/findings.md`
- `arcanum/arcana/inventory/SKILL.md`

## Global Constraints

- Patch public canonical source first.
- Keep all public code, fixtures, and docs generic.
- Execute one SWU at a time.
- Preserve consumer-owned mutable state.
- Do not claim atomicity or currentness.
- Do not migrate legacy entries.
- Stop on baseline, candidate, helper, digest, or owner mismatch.

## Expected SWU Result

```yaml
swu_id: SWU-IFR-NNN
result: pass | flag | block | interrupted
capability_ref: sigil-development
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: path-or-none
files_touched: []
validation: []
blockers: []
residue: []
reroute: sigil-development | none
handoff_note: summary
```

