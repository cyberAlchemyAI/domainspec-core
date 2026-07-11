# TASK-GSP-001 - Current-Head Projection

## Objective

Make the preview's primary artifact and annotation target project the current
governed head after Accept, Revert, and external CLI writes.

## Source Contracts

- `ARCHITECTURE-UPGRADE.md`
- `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md`
- `projects/ui-prototyping-studio/backend/src/cli/studio.ts`
- `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/current-html.ts`
- `projects/ui-prototyping-studio/backend/e2e/helpers.ts`

## Smallest Working Units

### SWU-GSP-001

- Goal: after a staged `Go -> Continue` change is accepted, the primary preview
  and annotation iframe render the accepted current head, not `/raw/variant/A`.
- Dependencies: none.
- Write scope:
  - `projects/ui-prototyping-studio/backend/src/cli/studio.ts`
  - optional new helper near `application/current-html.ts`
  - one focused Playwright e2e spec or addition to an existing preview spec
- Implementation detail:
  1. Add or inline a projection helper that resolves `currentHtml` once per
     render from `resolveCurrentHtml(session, store, artifactContentStore)`.
  2. In recorded states, render a primary "current accepted revision" iframe
     sourced from `/raw/baseline`.
  3. Keep original variant cards as reference/history, not the primary current
     artifact.
  4. Make annotation default to current head when a head exists; if the route
     needs a wrapper, add `/annotate/current` rather than reusing
     `/annotate/variant/<label>` as the only option.
  5. Ensure `/state` reload behavior observes external CLI writes while preview
     is running. If the current file-backed store keeps in-memory state, reload
     or version-check per request.
- Edge cases:
  - no baseline selected: annotation remains unavailable;
  - no real HTML artifact: show explicit unavailable state, not a blank iframe;
  - reverted head: current head shows restored content, history remains append-only.
- Done criteria:
  - current-head iframe is primary after Accept/Revert;
  - annotation source uses current head after a revision exists;
  - browser `/state` reflects external CLI apply/stage without server restart.
- Acceptance evidence:
  - failing-before/passing-after Playwright receipt;
  - screenshot or DOM assertion that current head contains `Continue` after Accept;
  - `/state` assertion for external write.
- Validation command:
  - `cd projects/ui-prototyping-studio/backend && ./node_modules/.bin/playwright test e2e/governed-state-projection.spec.ts --reporter=list`
- Execution owner: task-session.
- Expected result shape:

```yaml
swu_id: SWU-GSP-001
result: pass | flag | block
receipt_kind: task-session
files_touched: []
validation: []
blockers: []
residue: []
reroute: none
```

## Synchronization Notes

Do not start `SWU-GSP-002` or `SWU-GSP-003` until this SWU has at least a
passing focused witness or a clear blocker.
