# TASK-UPW-REGIONS — Six Independently Accepted Regions

Status: `not-started`

## Objective

Add the six selected workbench regions as separately reviewable keyed surfaces
without coarse rerender or authority changes.

- Layer/wave: L1 / W2
- Semantic baseline: SWU-UPW-007
- Scope authority: `SWU-SCOPE-INVENTORY.json` rows 008–013
- Acceptance authority: `SWU-ACCEPTANCE-MATRIX.json` assertions 008–013
- Closeout authority: `CLOSEOUT-SYNC-INVENTORY.json` rows 008–013

SWU-UPW-008 creates `backend/e2e/workbench-regions.spec.ts`; later region
SWUs may modify it. Each row has the same bounded application/projection/shell
files but all omitted paths remain unauthorized. Execution is serial because
those declared files overlap; after 008, each `serialization_after` edge is not
a semantic prerequisite.

## SWU Contracts

| SWU | Primary behavior | Semantic prerequisites | Serialization only | Exact focused check | Receipt |
| --- | --- | --- | --- | --- | --- |
| SWU-UPW-008 | lifecycle/next-action spine | 007 | none | `e2e/workbench-regions.spec.ts --grep "UPW-008 lifecycle spine"` | `validation.assertions.UPW_A_008_SPINE` |
| SWU-UPW-009 | current governed canvas | 007 | 008 | `e2e/workbench-regions.spec.ts --grep "UPW-009 current governed canvas"` | `validation.assertions.UPW_A_009_CANVAS` |
| SWU-UPW-010 | state-specific inspector | 007 | 009 | `e2e/workbench-regions.spec.ts --grep "UPW-010 contextual inspector"` | `validation.assertions.UPW_A_010_INSPECTOR` |
| SWU-UPW-011 | staged review and named frames | 007 | 010 | `e2e/workbench-regions.spec.ts --grep "UPW-011 staged review"` | `validation.assertions.UPW_A_011_REVIEW` |
| SWU-UPW-012 | governed actions and feedback | 005, 007 | 011 | `e2e/workbench-regions.spec.ts --grep "UPW-012 governed actions"` | `validation.assertions.UPW_A_012_ACTIONS` |
| SWU-UPW-013 | collapsed historical lineage | 007 | 012 | `e2e/workbench-regions.spec.ts --grep "UPW-013 historical lineage"` | `validation.assertions.UPW_A_013_HISTORY` |

All commands run from `projects/ui-prototyping-studio/backend` as:

`./node_modules/.bin/playwright test <exact-spec> --grep "<exact-name>" --reporter=list`.

## Implementation Detail

### SWU-UPW-008 — Lifecycle Spine

Build projection data and a `[data-region="spine"]` renderer for exact state,
current/staged identity, progress, connection state, and next valid action.
Derive values from the server projection only. Unknown prerequisites render a
reason rather than a fabricated action. The direct positive, state-collapse
mutant, selectors, and receipt are literal in assertion
`UPW-A-008-SPINE`.

Split analysis: identity and next action are one lifecycle summary decision;
canvas or action handlers can pass independently and remain separate.

### SWU-UPW-009 — Current Canvas

Render one `[data-region="canvas"] iframe[data-current-head]` from the current
head route/identity. Preserve its node/source while identity is unchanged;
present explicit unavailable/load-error behavior. Do not introduce annotation,
review, history, or route admission.

Split analysis: the canvas owns one current-head surface; frame security and
annotation behavior have different acceptance and remain later units.

### SWU-UPW-010 — Contextual Inspector

Select exactly one inspector model by lifecycle state: annotation, comment
queue, batch, staged context, or revision receipt. Gate each control on its
identity and render disabled reasons. Keep durable action POSTs in 012 and
ARIA/live semantics in 016.

Split analysis: inspector selection is one state-to-context mapping; canvas,
durable actions, and live semantics pass separately.

### SWU-UPW-011 — Staged Review

When a staged candidate exists, render candidate identity, diff recap, changed
components, and frames with distinct accessible names “Before — current” and
“After — candidate”. The region supplies acknowledgment context but not action
transport.

Split analysis: review evidence closes before its controls perform mutations;
transport remains 012.

### SWU-UPW-012 — Governed Actions

Wire Accept, Discard, and Revert to existing server handlers through the shared
refresh coordinator. Bind Accept/Revert to exact live identity and target
state, retain existing application validation, and direct response text only
to the state-owned feedback element. Do not add browser Export. ARIA roles,
keyboard parity, and focus policy remain 016.

Split analysis: action transport, gating, and state-owned feedback target form
one governed action result; visual placement/review evidence pass separately.

### SWU-UPW-013 — Historical Lineage

Render variants/revisions under `[data-region="history"]`, label them
non-current, collapse once a current head exists, place the region after active
work in DOM order, and key expansion context to the history region identity.

Split analysis: history is a single secondary-reference surface; responsive
layout is independently receiptable in 014.

## Shared Rules

- Region data comes only from the accepted server projection.
- Outer data uses `textContent`, explicit nodes, and allowlisted attributes.
- Prototype HTML stays inside route frames.
- Each renderer writes only its mount and has a stable identity/version.
- Unavailable regions explain the exact state; they do not create fake actions.
- Primary ownership is per assertion, not per fixture. Shared witnesses in
  `SWU-ACCEPTANCE-MATRIX.json` are regression/recomposition only.
- Each SWU owner recommendation is `subagent`; its handoff is the exact scope
  row, assertion row, dependency receipts, and source Design section.
