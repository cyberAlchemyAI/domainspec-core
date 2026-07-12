# Task Contract: Canvas Policy Coherence

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-CANVAS-POLICY` |
| Objective | Resolve approval and receipt contradictions without adding runtime ceremony. |
| Layer / slice / wave | L0 / VCR-S1 / W0 |
| Execution owner | Task Session on one SWU |

## Source Handles

- [Shared context](../shared/context.md)
- [Cross-task decisions](../shared/cross-task-decisions.md)
- Accepted findings: `../../../html-builder-architecture-review/findings.md`

## SWU-VCR-001: Trusted-Local Canvas Exception

**Goal:** make `SPEC.md` and `ARCHITECTURE.md` accurately describe current
canvas publication authority.

**Dependencies:** none.

**Exact write scope:** `projects/ide-extension/SPEC.md` and
`projects/ide-extension/ARCHITECTURE.md` only, plus Task Session evidence.

**Implementation rules:**

1. Narrow "approval and receipts on every effectful crossing" to protected
   effects.
2. Add an explicit trusted-local canvas preview/display exception.
3. State that canvas publication reads an operator-controlled workspace file
   and mutates local canvas projection/display state only.
4. State that `canvas.surface_published` is an audit event, not a receipt under
   the receipt contract.
5. Preserve approval for source writes, shell, network, provider, browser-act,
   domain effects, export, commit, push, and publication outside this local
   preview exception.
6. Clarify "one complete read" as bytes returned by one opened file read, not an
   atomic filesystem snapshot.
7. Do not change schemas, server routes, or tests in this SWU.

**Edge cases:** wording must not imply arbitrary local-file publication, remote
browser authority, source mutation, hostile HTML safety, or Craft completion.

**Done criteria:** G1-A, G1-R, G1-I, and K2/P2 each map to exact non-
contradictory prose; runtime diff is empty.

**Validation:** `rg` for approval/receipt/canvas clauses, review against
`findings.md`, and scoped `git diff --check`.

**Expected result:** pass with exact clause locations. **Handoff:**
`SWU-VCR-002` only after policy review passes.
