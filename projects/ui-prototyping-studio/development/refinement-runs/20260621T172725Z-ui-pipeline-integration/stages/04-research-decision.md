# Research Decision

Status: `pass`
Capability: `refine`
Mode: `no-research`

## Decision

Use **no external research** for this refine run.

## Rationale

The integration question is not "which external prototyping tool is best?" It
is how the local `ui-prototyping-studio` project should compose with the local
DomainSpec UI pipeline and current BodyWar/TROQAR UI artifacts.

Local evidence already establishes:

- Studio has a CLI-driven loop for variants, baseline, comments, preview,
  accept/revert, revisions, and handoff export.
- Studio has its own Playwright e2e suite.
- BodyWar has `UI-SPEC.md`, `TEST-SPEC.md`, and a Playwright scaffold.
- BodyWar target-app Playwright wiring is explicitly deferred to `SWU-TUI-002`.
- Owner boundaries are architectural, not market-research dependent.

## Trigger For Future Bounded Research

Bounded research would become useful only if a later task asks for one of these:

- comparison against external design/prototyping tools;
- accessibility research beyond existing WCAG/Playwright obligations;
- production hosting or preview collaboration patterns;
- browser security model changes around previewing untrusted HTML.

None of those are required for this integration plan.

## Receipt

```json
{
  "stage": "04-research-decision",
  "status": "pass",
  "artifacts": [
    "stages/04-research-decision.md"
  ],
  "validation_result": "pass",
  "blockers": [],
  "residue": []
}
```
