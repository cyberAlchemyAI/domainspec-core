# TASK-WFE-005 — Verify Routed Mutation Readiness

- Change: TS-2 / WFE-R02
- Layer/slice/wave: L1 / S1 / W1
- Lifecycle owner: `sigil-development` for Task Session
- Status: complete; see `../session-evidence/SWU-WFE-005/receipt.json`

## Objective

Make Task Session verify the current INV-1 readiness receipt before the first
write on routed or reusable mutation, without imposing the receipt on ordinary
standalone analysis/non-mutating sessions or replacing live validation.

## Sources

- TASK-WFE-003 material receipt schema and closure receipt
- `arcanum/arcana/task-session/SKILL.md`: Context Builder, dependencies,
  handoff, first mutation, live validation, closeout
- accepted findings TS-2
- `../../DESIGN.md`: INV-1→TS-2 interface

## SWU-WFE-005

- Primary behavior: one routed mutation admission decision verifies task/SWU,
  source identities/digests, dependency frontier, allowed writes, validation
  surface, and authority/publication class.
- Acceptance boundary: absent, stale, mismatched task, changed dependency,
  expanded write scope, and missing authority class fixtures block or rebuild
  before mutation; current exact receipt admits; standalone non-mutating use is
  unchanged; live post-mutation validation still runs.
- Split analysis: receipt fields are conjuncts of one admission decision and
  partial verification would create an unsafe fast path.

## Implementation rules

1. Trigger only when a route claims reusable/mutation readiness from Invoke or
   another declared producer.
2. Parse and validate the producer-owned schema; do not duplicate package
   validity logic in Task Session.
3. Compare live controlling inputs immediately before first write.
4. Rebuild bounded context or block on mismatch/residue; never reuse a stale
   pass because approval exists.
5. Preserve Context Builder strict coverage, live drift detection, validation,
   recovery, and closeout.

## Scope and validation

- Canonical: `arcanum/arcana/task-session/` contract, receipt consumer, fixtures.
- Generated: declared Task Session runtimes from canonical source.
- Forbidden: Invoke producer validator, universal receipt expiry, application work.

```bash
bash arcanum/arcana/task-session/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/task-session .agents/skills/task-session .claude/skills/task-session
```

- Dependencies: SWU-WFE-003B and TASK-WFE-004 closure/program-order receipt.
- Execution owner: `sigil-development`.
- Handoff: include the exact current material-receipt schema and a valid fixture,
  never a prose reconstruction.
- Receipt: consumer fixture matrix and proof that live validation remains.

## Done

The routed fast path is bound and fail-closed; non-routed use is compatible; no
validation or lifecycle authority moved from its owner.
