# TASK-WFE-003 — Validate Invoke Material Packages

- Change: INV-1 / WFE-R03
- Layer/slice/wave: L0 / S0 / W0
- Lifecycle owner: `spellcraft` for Invoke
- Status: complete — [SWU-WFE-003A receipt](../session-evidence/SWU-WFE-003A/receipt.json),
  [Option 1 relocation refresh](../session-evidence/SWU-WFE-003A/RELOCATION-REFRESH.md),
  and [SWU-WFE-003B receipt](../session-evidence/SWU-WFE-003B/receipt.json)

## Objective

Make mutation-capable Invoke handoff depend on a deterministic verdict over the
actual material package, not only a narrative report or approval field.

## Sources

- `arcanum/spells/invoke/refresh.md`: apply-approved contract, report shape,
  gates, phase/handoff separation
- `arcanum/spells/invoke/schemas/` material-package schemas
- `arcanum/spells/invoke/scripts/` runtime validator and handoff resolver
- `arcanum/spells/invoke/development/` fixtures, reports, and runners
- `../../DESIGN.md`: material-package validator and INV-1→TS-2 interface
- accepted findings INV-1

## Dependencies and scope

- Program-order dependency: TASK-WFE-002 closure.
- Write scope: canonical Invoke Refresh contract, top-level runtime validator
  support and schemas, focused development fixtures/runners, and declared
  generated Invoke mirrors.
- Forbidden: requiring a material mutation package for proposal-only phase pass;
  Task Session consumer changes; target application mutation.

## SWU-WFE-003A — Material validator

- Primary behavior: deterministic validator returns pass/reject for one actual
  mutation package.
- Acceptance boundary: missing output, empty declared change, stale digest,
  path/owner escape, missing dependency, publication boundary violation, and
  approval-scope mismatch reject; valid authorized and valid proposal-only
  non-mutation controls classify correctly.
- Split analysis: schema, validator, and red/green fixtures are one executable
  proof; any one without the others cannot establish package validity.

Inputs: changed paths/content, target inventory, source/output digests,
dependency frontier, canonical/generated mirrors, lifecycle owner,
authority/publication class, approval class/scope, validation commands, and
mutation state.

Output:

```yaml
patchVerdict: pass | reject | not-applicable
mutationHandoff: ready | gated | deferred | blocked
packageDigest: string | null
validatedPaths: []
dependencyResult: pass | reject | not-applicable
ownerBoundaryResult: pass | reject
publicationBoundaryResult: pass | reject
validationCommands: []
reasons: []
```

Validation: focused validator suite plus `arcanum/spells/invoke/development/run-validation-fixtures.sh`.

## SWU-WFE-003B — Refresh handoff integration

- Dependency: SWU-WFE-003A pass receipt.
- Primary behavior: `apply-approved` and other mutation-capable handoffs emit a
  readiness receipt only when the material validator passes.
- Acceptance boundary: approved-invalid package cannot emit readiness; valid
  package does; proposal-only complete output remains `phase=pass` with
  `handoff=gated|deferred` and no material mutation claim.
- Split analysis: integration is independently reviewable after the validator
  exists and changes one transition, not validator semantics.

### Write scope

- `arcanum/spells/invoke/refresh.md`
- runtime validator/resolver under `arcanum/spells/invoke/scripts/`
- material schemas under `arcanum/spells/invoke/schemas/`
- fixtures, reports, and runners under `arcanum/spells/invoke/development/`
- declared generated Invoke runtime surfaces only

### Validation

```bash
bash arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- arcanum/spells/invoke .agents/skills/invoke .claude/skills/invoke
```

- Execution owner: `spellcraft`.
- Handoff: public submodule first; verify actual generated targets before sync.
- Receipt: material validator result, package digest, integration fixture matrix,
  generated parity, and proposal-only compatibility result.

## Done

Both SWUs pass, the receipt schema is stable enough for TASK-WFE-005, and no
proposal-only route gains or loses mutation authority accidentally.
