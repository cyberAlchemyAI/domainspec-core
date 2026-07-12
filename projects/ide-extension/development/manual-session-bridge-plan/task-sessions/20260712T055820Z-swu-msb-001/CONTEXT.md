# Context Pack: SWU-MSB-001

## Selection

- Work-pack: `projects/ide-extension/development/manual-session-bridge-plan/WORK-PACK.md`
- Task: `TASK-CONTRACT-MIGRATION`
- SWU: `SWU-MSB-001`
- Runtime: local Codex / Task Session
- Strict runtime handoff: not requested

## Controlling Sources

1. `work-pack/tasks/TASK-CONTRACT-MIGRATION.md` defines the exact write scope,
   done criteria, and no-route boundary.
2. `work-pack/shared/cross-task-decisions.md` requires immutable v1 history,
   discriminated v2 receipts, terminal-result authorization consumption, and
   a separate one-shot session protocol later.
3. `manual-session-bridge-design/DECISIONS.md` fixes read/preview effects,
   separate receipts, operator recovery, unattested sessions, and one ready target.
4. `manual-session-bridge-design/ARCHITECTURE-BUNDLE.md` defines the five request
   contract families, bridge states, receipt bindings, and late-disclosure rule.
5. Current spec, schemas, grant normalization, schema registry, fixtures, and
   focused tests define the accepted legacy contract.

## Brownfield Baseline

- Seven explicit schemas, six module manifests, and 22 schema fixtures validate.
- Six schema tests and eight grant/disposition tests pass.
- Legacy dry-run defaults are `dry-run.noop` plus `preview.read`.
- Legacy envelopes and receipts have no version discriminator and must remain valid.

## Execution Decision

- Keep legacy envelope/receipt branches structurally unchanged.
- Require `schema_version: "2"` on v2 envelopes and bridge request records.
- Require `receipt_kind` on v2 authorization/execution receipts so all three
  receipt branches are deterministic under `oneOf`.
- Keep the legacy default grant profile; add a separate exact bridge profile of
  `skill.invoke` plus `preview.read`.
- Register five request schemas: target, claim, result, interrupt, and release.

## Gates

- Dependencies: pass.
- Approved decisions: pass; no unresolved choice.
- Write scope: complete and bounded.
- Validation surface: baseline and post-change schema/grant commands available.
- Server/projector behavior: read-only in this SWU.
- Gate verdict: PASS.

## Done Evidence Required

- Legacy fixtures still pass.
- Valid v2 envelope, authorization receipt, execution receipt, and all five
  request fixtures pass.
- Hostile blank/path-like skill, grant-profile, receipt-overlap/status, and
  missing-binding fixtures fail.
- Registry and focused tests pass with no server/projector diff.
