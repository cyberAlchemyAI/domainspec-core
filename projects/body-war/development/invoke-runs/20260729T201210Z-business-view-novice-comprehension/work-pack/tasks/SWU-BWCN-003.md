# SWU-BWCN-003 — Pinned Browser Structural Evidence

Status: `blocked-by-dependency`

Depends on: `SWU-BWCN-002`

## Primary behavior

Validate the exact learner task and journey stimulus in the shared Chromium
runtime and emit a durable structural receipt.

## Material write scope

- `projects/body-war/ontology/business/scripts/validate-comprehension-browser.mjs`

## Execution output scope

- `projects/body-war/ontology/business/receipts/comprehension-browser-receipt.json`
- `projects/body-war/ontology/business/receipts/comprehension-browser-task.png`
- `projects/body-war/ontology/business/receipts/comprehension-browser-journey.png`

## Acceptance

The receipt pins task, stimulus, loci, prompt, catalog, generator, profile,
residue, Node, Playwright, browser revision, executable path/hash, viewport,
DPR, JavaScript/no-JavaScript/reduced-motion/print modes, isolation, assertions,
artifacts, timestamps, results, and claim ceiling.

Browser assertions cover stimulus-only loading, keyboard behavior, responsive
structure, native no-JS access, progressive enhancement, reduced motion, print,
owner/gate/tone visibility, and negative reviewer leakage.

## Validation

```text
node projects/body-war/ontology/business/scripts/validate-comprehension-browser.mjs
```

## Split analysis

The harness and its one run form one evidence behavior. The harness is the only
material write; receipts and screenshots are disjoint execution outputs.

