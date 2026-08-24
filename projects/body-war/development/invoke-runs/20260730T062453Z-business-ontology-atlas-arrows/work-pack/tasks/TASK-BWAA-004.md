# TASK-BWAA-004 — Execute Arrow Browser Acceptance

Layer: L3  
Dependencies: `SWU-BWAA-003` closeout  
SWU: `SWU-BWAA-004`  
Execution owner recommendation: `local-fallback` through one Task Session using
the shared Playwright runtime

## Task Objective

Observe the exact generated artifact across supported browser/static modes and
bind the arrow and reference-brief results without repairing source. This task
contains exactly one SWU.

## Smallest Working Units

- `SWU-BWAA-004`: execute and bind arrow-specific browser acceptance.

## Primary Behavior

Extend and execute the atlas browser validator so the new aggregate and exact
arrow representations and source-backed reference briefs have digest-bound
responsive/static evidence.

## Source Anchors

- `ARCHITECTURE.md#browser-evidence-contract`
- `UX-PLAN.md#responsive-and-static-modes`
- generated atlas from 003
- repository-global Playwright runtime defined by `AGENTS.md`

## Write Scope

- `projects/body-war/ontology/business/scripts/validate-view-atlas-browser.mjs`
- `projects/body-war/ontology/business/receipts/view-atlas-browser-receipt.json`
- `projects/body-war/ontology/business/receipts/view-atlas-arrow-overview.png`
- `projects/body-war/ontology/business/receipts/view-atlas-arrow-relation-mobile.png`

## Implementation Detail

Inputs are the 003-generated atlas, current projection/renderer/browser
validator bytes, shared Playwright/Chromium runtime discovery, and previous
coverage receipt. Outputs are a new browser receipt and two screenshots.

Execution algorithm:

```text
discover and record exact Playwright and Chromium runtime
start an ephemeral loopback-only server for the atlas directory
open the exact generated atlas bytes
run desktop overview and representative exact-arrow assertions
run keyboard and focus assertions
run hover, persistent keyboard, and touch/click reference-brief assertions
run mobile stacking and no-horizontal-loss assertions
run no-JS, reduced-motion, 200%-text, and print assertions, including briefs
collect page, console, request, and network failures
capture two declared screenshots
hash all bound inputs and outputs into a new receipt
close browser/server in finally
fail if any required assertion or zero-error invariant is false
```

External network is forbidden. Existing global runtime is convenience only and
must be re-discovered. Screenshots do not pass acceptance without the
machine-readable assertions and receipt.

Failure modes:

- runtime/version/executable cannot be resolved;
- server binds beyond loopback;
- current HTML digest differs from the selected 003 receipt;
- any arrow/count/responsive/static assertion fails;
- browser/page/request error or external network request;
- partial evidence or failed teardown.

All failures produce a blocked/failed attempt and no source repair.

## Acceptance

- exact runtime discovery records Playwright version, Chromium revision,
  executable path, and input digests;
- desktop proves six overview nodes, 13 directed lanes, and a representative
  55-count `behavior → business-objects` lane;
- exact relation focus proves source → predicate → target orientation;
- representative node, relation, lens, and predicate briefs expose exact
  source-backed content through hover, focus, and touch/click;
- blocked content, recorded questions, and explicit missing-question text
  remain visible;
- mobile preserves all semantic lanes and stacks exact arrows without
  horizontal content loss;
- keyboard, touch/click, no-JS, reduced-motion, 200% text, and print checks
  retain the same brief meaning;
- there are zero page errors, console errors, failed requests, or external
  network requests;
- screenshots and receipt are created by the validator, not hand-edited;
- the complete ontology regression remains green.

## Validation

```bash
command -v playwright
playwright --version
npm list -g --depth=0 playwright
playwright install --list
node projects/body-war/ontology/business/scripts/validate-view-atlas-browser.mjs
node --test projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs projects/body-war/ontology/business/tests/business-view-atlas-render.test.mjs projects/body-war/ontology/business/tests/business-views.test.mjs projects/body-war/ontology/business/tests/business-ontology.test.mjs
node projects/body-war/ontology/business/scripts/validate-view-atlas.mjs
git diff --check -- projects/body-war/ontology/business/scripts/validate-view-atlas-browser.mjs projects/body-war/ontology/business/receipts/view-atlas-browser-receipt.json projects/body-war/ontology/business/receipts/view-atlas-arrow-overview.png projects/body-war/ontology/business/receipts/view-atlas-arrow-relation-mobile.png
```

## Split And Done

Candidate children were validator changes and browser execution. They remain
one observation lifecycle because the new assertions have no accepted result
until executed against the selected bytes, while any product-code repair is
strictly excluded. Done requires a terminal receipt, browser receipt, two
screenshots, teardown evidence, and a candidate-local claim ceiling.

## Handoff And Closeout

Context Builder needs this task, the 003 receipt/digest, `AGENTS.md` shared
browser runtime section, the browser validator, the generated atlas, and
`../shared/EXECUTION-CONTROL.md`. Known blockers: failed 003 receipt, artifact
drift, or unavailable shared runtime.

Expected result:

```yaml
swu_id: SWU-BWAA-004
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: work-pack/closeout/SWU-BWAA-004.receipt.json | none
files_touched: [declared paths only]
validation: [command and result]
blockers: [blocker or none]
residue: [residue or none]
reroute: invoke-refresh | none
handoff_note: candidate-local arrow/brief evidence result and remaining claim ceilings
```
