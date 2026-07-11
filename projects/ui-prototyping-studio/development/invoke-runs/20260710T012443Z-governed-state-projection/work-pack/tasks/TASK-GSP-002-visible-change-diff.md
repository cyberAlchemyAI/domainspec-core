# TASK-GSP-002 - Visible-Change Diff Integrity

## Objective

Prevent visible CSS/theme/global/layout changes from being represented as zero
diff confidence.

## Source Contracts

- `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/admission.ts`
- `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md`

## Smallest Working Units

### SWU-GSP-002

- Goal: add a global/style/unattributed visible-change lane to diff evidence, or
  explicitly mark style changes as not component-attributable.
- Dependencies: `SWU-GSP-001`.
- Write scope:
  - `application/admission.ts`
  - domain diff model/types if needed
  - apply/preview/handoff display tests
- Implementation detail:
  1. Extend `diffByOdId` to compare `<style>` raw text and CSS rules.
  2. Preserve existing per-od-id fragments.
  3. Add a separate lane for global/style changes rather than pretending they
     are component fragments.
  4. Display the lane in pending review and handoff diff evidence.
- Edge cases:
  - selector maps to multiple od-ids;
  - selector maps to no od-id;
  - raw style changed but parsed rules equal;
  - external CSS unsupported by current HTML-only artifact.
- Done criteria:
  - TROQAR-style desaturation/theme fixture does not return empty evidence;
  - zero structural fragments with style change is visibly marked.
- Acceptance evidence:
  - unit fixture for CSS-only change;
  - e2e pending panel assertion when practical.
- Validation command:
  - `cd projects/ui-prototyping-studio/backend && ./node_modules/.bin/tsx --test "src/**/*.test.ts"`
- Execution owner: task-session.
