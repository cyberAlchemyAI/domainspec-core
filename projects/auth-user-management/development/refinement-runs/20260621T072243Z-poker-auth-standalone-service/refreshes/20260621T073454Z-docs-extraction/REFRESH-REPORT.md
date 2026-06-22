# Invoke Refresh Report: Docs Extraction

## Mode Result

- Mode: invoke refresh
- Phase status: pass
- Mutation mode: apply-approved
- Evidence date: 2026-06-21
- Target workflow root: `projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service`
- Next route: task-session

## Source Signals

| ID | Type | Claim | Safety |
| --- | --- | --- | --- |
| SIG-AUM-DOCS-001 | evidence_added | Poker Team auth-access-control has source docs that must be extracted with the code. | safe |
| SIG-AUM-DOCS-002 | route_changed | The work-pack needs a dedicated docs extraction SWU before readiness audit. | safe |

## Evidence

- `validation/poker-team/docs/features/auth-access-control/`
- `validation/poker-team/docs/index/feature-map.md`
- `validation/poker-team/docs/slos.md`
- `validation/poker-team/infra/alerts/auth-access-control.rules.yml`

## Delta Summary

- Added docs extraction as a covered context obligation.
- Expanded define/design/distill artifacts so documentation is source
  authority, not only adoption output.
- Added `SWU-AUM-006` for extracting and normalizing docs.
- Renumbered readiness audit to `SWU-AUM-007`.
- Added stale path/link scans to the work-pack validation surface.
- Updated manifest, evidence index, result, synthesis, and runtime handoff.

## Applied Changes

- `REFINE-SEED-PROPOSAL.md`
- `REFINE-DISPATCH.json`
- `RUN-MANIFEST.md`
- `RUNTIME-HANDOFF.md`
- `RESULT.md`
- `evidence-index.json`
- `stages/01-context-builder/CONTEXT-PACK.md`
- `stages/01-context-builder/context-index.json`
- `stages/02-invoke-define/DEFINE.md`
- `stages/05-distill/COPY-UNIT.md`
- `stages/06-invoke-design/DESIGN.md`
- `stages/08-distill-repair/REPAIR.md`
- `stages/09-invoke-plan/IMPLEMENTATION-LAYERING.md`
- `stages/09-invoke-plan/WORK-PACK.md`
- `stages/10-final-synthesis/SYNTHESIS.md`

## Skipped Changes

- No target implementation code was changed.
- No Poker Team source file was changed.
- No public `arcanum` file was changed.

## Validation

```bash
python3 -m json.tool projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/stages/01-context-builder/context-index.json
python3 -m json.tool projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/evidence-index.json
python3 -m json.tool projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/refreshes/20260621T073454Z-docs-extraction/refresh-report.json
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/REFINE-DISPATCH.json
rg -n "SWU-AUM-006|SWU-AUM-007|docs/features/auth-access-control|Extract And Normalize Source Docs" projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service
git diff --check -- projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service
! rg -n '[[:blank:]]$' projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service
```

## Result

pass. The work-pack now routes docs extraction as first-class implementation
work and remains ready for Task Session execution.
