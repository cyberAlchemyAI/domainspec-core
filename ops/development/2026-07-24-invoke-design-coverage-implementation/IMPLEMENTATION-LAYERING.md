# Implementation Layering: Invoke Design Coverage

## Boundary heuristic

After each layer, state the decision unlocked by evidence. Later layers preserve
earlier fixture expectations and evidence-state separation.

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion rule |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | Can an implementation-independent fixture denominator expose omissions and bounded-selection false positives? | SWU-DVC-001 frozen fixture matrix and expected dispositions | positive, negative, bounded, UX, stale/self-issued, and mutation cases | schemas, extractor, validator | immutable fixture IDs, sources, expected selections, diagnostic codes, and corpus digest | enter L1 only when Spellcraft accepts the independent denominator |
| L1 | Can deterministic contracts reproduce the frozen expectations and reject every causal negative? | SWU-DVC-002A/B/C, 003, 004, 005 | schemas, canonicalization, extraction, precedence, ownership, four states, two passes, runner | mode/template integration | schema, unit, mutation, stale/self-issued, and bounded-selection suites pass | enter L2 only when fixtures pass without changing their expectations |
| L2 | Can Invoke Design, architecture, and UX contracts consume the validated result without collapsing evidence or selecting universal families? | SWU-DVC-006A/B/C | Design mode, root evidence contract, architecture extensions, UX trigger and content | generated surfaces, live examples | contract fixtures and exact expected outputs pass | enter L3 only when canonical sources validate and public/private scan passes |
| L3 | Do generated runtimes and a generic Define → Design → Plan run preserve the canonical behavior? | SWU-DVC-007 and 008 plus VERIFY | generated synchronization, parity, live example, observability, final audit | promotion/publication | parity receipt, live run, recomposition, leakage scan, lifecycle audit | promotion remains a separate Spellcraft/human decision |

## Non-regression guardrails

- Frozen fixture expectations may change only through a separate reviewed
  evidence decision, never to make an implementation pass.
- Six views remain mandatory and non-sufficient.
- Only `required` selects a companion or extension.
- `not-applicable-with-rationale` requires detector-negative evidence.
- `design-validator-pass` never implies `plan-evidence-pass`.
- Existing dirty Invoke edits are neither reverted nor absorbed.
- Generated surfaces are synchronized only after canonical validation.

## Recommended next layer

- Next layer: L0.
- Selected unit: SWU-DVC-001.
- Decision unlocked: whether the independent denominator and bounded controls
  are concrete enough to constrain implementation.

