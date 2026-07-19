---
id: ide-extension-workbench-ui-v1-layering
project: ide-extension
status: planned
updatedAt: 2026-07-17
---

# Implementation Layering

| Layer | Question | Included | Promotion Evidence |
| --- | --- | --- | --- |
| L0 | Can the new shell preserve every current capability? | Responsive regions, existing data mapper, no behavior loss. | Existing Node tests plus desktop/mobile shell assertions. |
| L1 | Can a user create the right request and understand its state? | Explicit modes, validation, run list, state action, timeline. | Dry-run/agent-task and lifecycle Playwright journeys. |
| L2 | Can the user operate around the produced artifact? | Canvas-first workspace, Craft source selection, evidence drawer. | Canvas interaction, Craft read-only, receipt linkage, responsive evidence. |
| L3 | Is V1 useful and ready to become the default screen? | Integrated regression, accessibility checks, human usefulness gate. | Full scoped suites, retained screenshots, explicit human verdict. |

## Deferrals

Background workers, OpenRouter, MV3 browser control, VSCodium chrome, hostile
HTML containment, collaboration, and region mutation are outside this layering.
