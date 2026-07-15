---
task: SWU-RDL-005
mode: lean-strict
status: pass
createdAt: 2026-07-14T22:33:45Z
session_evidence: true
source_count: 9
obligation_coverage: 100%
---

# Context Pack: SWU-RDL-005 FPR-01 Learning And Proposal Surface

This is Task Session evidence, not a reusable source-of-truth document.

## Objective

Extend the generated roadmap HTML with an FPR-01 Roadmap Lab panel that lets a
newcomer explicitly orient, learn FPR-01, restate it, request a source path, and
draft one reviewable improvement proposal using the exact semantic
`postMessage` envelope already admitted by Canvas. The surface must preserve
drafts on local/client failure and must not claim Canvas storage, owner review,
or source mutation.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| U1 | Implement orientation, learning packet, restatement, source request, proposal draft, owner preview, and local status/history. | `TASK-RDL-GUIDED-SURFACE.md`, `UX-PLAN.md#Primary Journey` | covered |
| U2 | Emit exact W0 semantic event messages inside `{type,eventName,payload}` only after explicit actions. | `roadmap-event.schema.json`, Canvas postMessage adapter | covered |
| U3 | Bind events to participant label, `FPR-01`, current input fingerprint, observed copy/source selectors, and FPR-01 copy fields. | SWU-RDL-004 build manifest and copy fields | covered |
| U4 | Enforce local validation, semantic payload size, unsupported class/evidence rules, and retry-preserved drafts without passive click events. | UX error principles and event schema bounds | covered |
| U5 | Keep browser authority honest: no direct mutation endpoint, no stored/applied claim without parent/owner evidence. | Architecture RDL-O02/RDL-O03 and existing Canvas adapter | covered |
| U6 | Prove browser behavior with focused Playwright plus visibility suite, without mutating IDE route files. | Playwright skill prerequisite and task validation | covered |

## Selected Sources

| Source selector | Why included | Obligations |
| --- | --- | --- |
| `WORK-PACK.md` SWU-RDL-005 row | exact scope/status/validation | U1-U6 |
| `TASK-RDL-GUIDED-SURFACE.md#SWU-RDL-005` | rules, edge cases, done criteria | U1-U6 |
| `UX-PLAN.md#Primary Journey`, `#Proposal Classes`, `#Accessibility And Error Principles` | journey and user-facing states | U1, U4-U5 |
| `ARCHITECTURE-BUNDLE.md#RDL-O02`, `#View 6` | exact event envelope and authority boundary | U2-U5 |
| `roadmap-event.schema.json` | semantic event fields, proposal class targets, bounds | U2-U4 |
| `l0.html:1390-1432` | current parent message admission and storage semantics | U2, U5 |
| `SWU-RDL-004/TASK-SESSION-RESULT.md` and `BUILD-FINGERPRINT-REPORT.md` | fingerprint version, FPR-01 field IDs, source roles | U3 |
| `visibility/roadmap.template.html` | generated UI insertion point and current DOM conventions | U1-U5 |
| `projects/ide-extension/package.json` and Playwright skill | browser validation route | U6 |

Selected excerpt budget: 137 lines across 9 files.

## Contract Decisions

### D-SWU005-01 - Emit semantic messages, do not claim storage

- Selected: the generated page emits exact semantic `postMessage` objects and
  displays "waiting for Canvas storage acknowledgment" until a parent sends an
  explicit result message.
- Reason: SWU-RDL-005 is not allowed to edit `l0.html` or call
  `/api/canvas/events`; storage proof belongs to SWU-RDL-006.

### D-SWU005-02 - Support all proposal classes with conservative defaults

- Selected: the form exposes all five proposal classes. Presentation-copy
  proposals target `copy.node.FPR-01.title` or `copy.node.FPR-01.summary`; other
  classes target `FPR-01` with class-specific schema shapes and owner preview.
- Reason: this proves class semantics without pretending non-copy classes have
  direct effects.

No blocker-level decision exists. Decision Gate is not required.

## Write Scope And Dirty Gate

Allowed:

- `visibility/roadmap.template.html`;
- `visibility/tests/test_build_roadmap.py` if static generated-surface checks
  are needed;
- new focused visibility browser spec/fixture under `visibility/tests/e2e/`;
- regenerated `visibility/roadmap-data.json` and `visibility/roadmap.html`;
- output screenshots under `output/playwright/`;
- this session's result/report and planning synchronization.

Read-only: IDE `l0.html`, `server.mjs`, Canvas tests, roadmap manifest, Craft
ledger, schemas except for validation reads, and public Arcanum.

Dirty-scope review: `l0.html`/`server.mjs` are dirty but out of this SWU's write
scope. Visibility package files are untracked current baseline and may be
mutated only through the guided-surface implementation and builder regeneration.

## Validation

```bash
python3 -m unittest discover \
  -s projects/domainspec-v2/development/first-production-release/visibility/tests

cd projects/ide-extension && npx playwright test \
  ../domainspec-v2/development/first-production-release/visibility/tests/e2e/roadmap-lab-surface.spec.mjs
```

Also run builder `--check`, JSON parsing, semantic event contract tests, exact
message capture in Playwright, draft-preservation failure test, keyboard/focus
checks, screenshots, and no IDE runtime mutation scan.

## Context Builder Result

- Mode: lean, strict.
- Files selected: 9.
- Obligations: 6/6 covered.
- Noise ratio: low.
- Handoff pack: none; local execution.
- Strict coverage: pass.
- Blockers: 0.
