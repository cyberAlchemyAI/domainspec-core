# TASK-WFE-001 — Enforce Subagents Admission Invariants

- Change: DSS-1 / WFE-R05
- Layer/slice/wave: L0 / S0 / W0
- Lifecycle owner: private DomainSpec tooling with `sigil-development`
- Status: complete
- Closure receipt: `../session-evidence/SWU-WFE-001/receipt.json`

## Objective

Make the existing registration boundary reject new states the strategy already
forbids, without changing historical rows, record fields, or duplicate-close
idempotence.

## Sources

- `../../DESIGN.md#canonicalized-destination-containment`
- `../../../2026-07-22-most-used-skills-efficiency-review/findings.md#domainspec-subagents-strategy--fix`
- `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs`: `LIVE_TYPES`, `validateDispatch`, folder check, close append, RESERVED note
- `implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs`: sections 10–12
- `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md`: LIVE/RESERVED table and closeout rules

## Dependencies and scope

- Technical dependencies: none.
- Entry gate: Dispatch Spec and Distill pass; lifecycle owner accepts this SWU.
- Write scope:
  - `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs`
  - `implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs`
- Forbidden: ledger history, public `arcanum/`, strategy semantics, record schema fields.

## SWU-WFE-001

- Primary behavior: one new-record admission decision rejects RESERVED dispatch,
  orphan close, working-agent final approver, and escaped destination.
- Acceptance boundary: focused appender suite proves the four rejections plus a
  non-existing in-root folder, existing symlink escape, historical-row parse,
  and duplicate-close no-op.
- Split analysis: type, close, approver, and path checks are candidate children,
  but independently deploying any subset leaves the same admission function
  capable of accepting a contract-forbidden row. Tests are the acceptance
  boundary, not a separate behavior.

### Implementation algorithm

1. Keep the broad structural enum readable for historical records, but reject a
   submitted dispatch whose type is not in `LIVE_TYPES` before append.
2. Before appending a close, require a matching dispatch row; retain duplicate
   close as a successful no-op.
3. Flatten all submitted group agent names and reject equality with
   `final_approver` after the same whitespace normalization used for identity;
   do not invent fuzzy identity matching.
4. For `working_folder`, reject absolute paths and `..`; resolve beneath the
   repository root; realpath the nearest existing parent and any existing leaf;
   reject a symlink/realpath escape; then apply the normalized `vault` rule.
5. Emit stable errors and do not change the ledger on failure.

### Done criteria

- Current 83-test baseline remains green after expected fixture updates.
- New tests prove every accepted DSS-1 negative and positive case.
- Historical ledger passes structural self-check unchanged.
- No extra approval or record field is added.

### Validation

```bash
node implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs
git diff --check -- implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs
```

- Execution owner: `sigil-development` with local fallback only if that owner
  explicitly routes implementation.
- Handoff: build execution-time Context Builder evidence from the exact symbols
  above; preserve unrelated dispatch-spec/runtime worktree changes.
- Expected receipt: standard closure receipt with test counts, rejected fixture
  names, files touched, and no ledger-history mutation.

## Synchronization

On pass, update `WORK-PACK.md` and `work-pack/swu-manifest.json`, append the
receipt under session evidence, and stop before selecting SWU-WFE-002.

Completed with 93 focused tests passing. The continuing user instruction to
execute the serial stream until a blocker explicitly selects SWU-WFE-002 after
this receipt; no second SWU was executed inside this session.
