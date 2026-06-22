# Refine Result

- Status: `strategy-proposal-pending-confirmation`
- Target: `projects/body-war`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`
- Seed proposal: `REFINE-SEED-PROPOSAL.md`
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: `pass`
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Research mode: `research-if-gap-appears`
- Preset: `standard`

## Strategy Synthesis

The validated route should refine TROQAR into a production-ready first-page and
login UI before implementation. The likely direction is:

1. Use Strava as the only visible MVP login method.
2. Preserve backend/provider extensibility without exposing other login choices.
3. Redesign `/` as a login-first app entry screen for anonymous users.
4. Redesign the connected state as a runner home/profile screen with activity
   and preview evidence actions.
5. Use UI Prototyping Studio as the live review gate for the local page, then
   apply accepted changes into BodyWar source.
6. Keep static HTML/CSS/JS unless the refine loop proves a component package or
   bundler is needed now.

## Recommended Next Route

Confirm this strategy to run the Refine loop with the recommended subagent
strategy. After Refine produces the implementation plan, execute the selected
Task Session against BodyWar app/docs/tests.
