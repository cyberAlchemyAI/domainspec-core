# Stage 10 - Final Interrogation And Synthesis

Status: pass
Capability handle: `interrogation + refine`
Mode: `refine-final`
Receipt kind: parent-native-stage-artifact

## Final Verdict

Proceed to a Task Session for the `TROQAR production login-first shell`, after
using Studio as the visual handoff gate.

The route is coherent, bounded, and implementation-ready. It should not grow
into full gameplay, full auth management, provider expansion, deployment, or
framework migration.

## Final Decisions

| Decision | Result |
| --- | --- |
| Visible MVP login method | Strava only. |
| Provider architecture | Keep backend/domain extensibility hidden from MVP UI. |
| UI implementation route | Plain static HTML/CSS/JS hardening. |
| Component/package route | No UI framework now; no icon package unless a concrete need appears. |
| Studio usage | Capture live page baselines, annotate selectors, export handoff, then mutate source in Task Session. |
| Production acceptance | Requires Playwright falsification and screenshot/Studio evidence. |

## Implementation Must Include

- Anonymous login-first page with `Continue with Strava`.
- Connected runner home/profile after fake or real Strava callback.
- User-safe auth success/error/retry states.
- Provider disconnected/reconnect state.
- Activity loading/empty/error states.
- Submit pending/success/error states.
- Preview-evidence and geometry-status language.
- Dynamic escaping/hardening for tracks and submissions rendered via template
  strings.
- Stable accepted Studio selectors plus the new production-state anchors.

## Recommended Next Route

Run a bounded Task Session for SWUs `SWU-PUI-001` through `SWU-PUI-005` from
`stages/09-plan.md`.

Suggested task-session objective:

```text
Execute the TROQAR production login-first shell plan from projects/body-war/development/refinement-runs/20260622T083402Z-troqar-production-ui-login-refine/stages/09-plan.md. Keep visible MVP login Strava-only, keep implementation static HTML/CSS/JS, use Studio handoff evidence, and validate with BodyWar build/check/test:ui plus diff hygiene.
```

## Residue

- Decide whether the final CTA copy is `Connect Strava` or
  `Continue with Strava`; the refined recommendation is `Continue with Strava`.
- Decide whether L0 server submissions should return `preview-accepted` now or
  whether the UI maps `submitted/hybrid` into preview language.
- Decide whether `/profile/privacy` remains deferred or gets a small static
  section in the connected shell.
