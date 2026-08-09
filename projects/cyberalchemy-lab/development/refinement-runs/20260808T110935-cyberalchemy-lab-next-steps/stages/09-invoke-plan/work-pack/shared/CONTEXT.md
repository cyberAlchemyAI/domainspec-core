# Shared Execution Context

## Approved inputs

- Strict evidence: `../../../01-context-builder/context-pack.md`
- Definition: `../../../02-invoke-define.md`
- Selected unit B: `../../../05-distill.md`
- Validated design: `../../../06-invoke-design/ARCHITECTURE.md`
- Design selection result: `../../../06-invoke-design/DESIGN-SELECTION-RESULT.json`
- Superseding repair rules: `../../../08-distill-repair.md`
- Layer governance: `../../IMPLEMENTATION-LAYERING.md`

## Global invariants

- Product root is `projects/cyberalchemy-lab/research/tower-evidence-navigator/`.
- Generated L0 output root is `projects/cyberalchemy-lab/development/witness-runs/l0-synthetic-001/`.
- No `projects/ide-extension/`, `arcanum/`, `.arcanum/inventory/`, external system, or Git history mutation is admitted.
- No new package root or dependency is added; use existing Node and `.mjs` entry points.
- All candidate/projection records carry `authority_effect: none`.
- All L0 evidence carries `fixture_class: synthetic-contract-fixture`.
- Stage 08 `cal-canonical-json-v1` supersedes the generic canonicalization wording in Stage 06.

## Expected execution result shape

```yaml
swu_id: SWU-CAL-NNN
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: <exact path or none>
files_touched: [<paths>]
validation: [<command and result>]
blockers: [<blocker or none>]
residue: [<unresolved evidence or none>]
reroute: <next owner or none>
handoff_note: <what closeout must synchronize>
```

