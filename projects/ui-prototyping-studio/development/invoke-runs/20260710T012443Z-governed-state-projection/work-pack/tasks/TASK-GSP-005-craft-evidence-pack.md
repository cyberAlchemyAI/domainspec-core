# TASK-GSP-005 - Minimal CraftEvidencePack

## Objective

Add the first Open Design-inspired evidence/profile slice without changing
Studio identity or bypassing Studio gates.

## Source Contracts

- `projects/ui-prototyping-studio/provenance/open-design-reference/`
- `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md`

## Smallest Working Units

### SWU-GSP-006

- Goal: create a minimal `CraftEvidencePack` for a candidate/revision with
  `required_gate`, `advisory`, and `subjective_review` buckets.
- Dependencies: `SWU-GSP-002`, `SWU-GSP-004`.
- Write scope:
  - new evidence/provenance type or schema;
  - candidate/revision provenance;
  - unit fixture.
- Implementation detail:
  1. Required bucket includes only machine-checkable facts already in scope:
     `data-od-id` coverage, visible-change diff evidence presence, required
     source refs present.
  2. Advisory bucket can record target-size/contrast/focus pending evidence only
     when the check exists.
  3. Subjective review is never a hard gate.
  4. Accepted revision records pack id/hash only through existing
     register/baseline/stage/accept flow.
- Done criteria:
  - missing required evidence marks pack incomplete;
  - subjective review cannot block acceptance;
  - no OD artifact output bypasses Studio gates.
- Validation command:
  - `cd projects/ui-prototyping-studio/backend && ./node_modules/.bin/tsx --test "src/**/*.test.ts"`
- Execution owner: task-session.
