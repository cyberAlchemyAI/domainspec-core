# Experiment Report: SWU-WFE-007B

- Verdict: `PASS`
- Primary harness: `test-strategy-runtime-composition.cjs`
- Composition fixtures: 13/13
- Appender regression fixtures: 102/102

## Negative controls

- public lifecycle removal: rejected in Codex and Claude;
- undeclared public lifecycle addition: rejected in Codex and Claude;
- private owner removal: rejected;
- private research-output rule removal: rejected;
- private public/private boundary removal: rejected;
- undeclared private authority addition: rejected;
- private overlay sync to undeclared Codex target: rejected;
- missing overlay source: rejected.

## Positive controls

- checked-in public base projections: pass;
- generated private Claude adapter: pass;
- formatting-only private adapter changes: pass;
- declared provenance and Claude tool-name mapping: pass;
- appender evidence-binding regressions: pass.

## Interpretation

The harness proves semantic projection parity for the declared sources and
targets. It does not promote the public sigil or authorize a new private runtime
target.
