# Runtime Handoff Pack — SWU-OAVA-001

## Identity

- Task/SWU: `TASK-OAVA-CONTRACTS` / `SWU-OAVA-001`
- Source Work Pack: `research/2026-08-04-ontology-video-voice-provider-research/development/refinement-runs/20260805-autoresearch-animejs-animation/WORK-PACK.md`
- Run: `oava001-ts-20260806-001`
- Runtime handoff: `runtime`
- Evidence date: `2026-08-06`

## Obligation coverage

| Obligation | Status | Selected evidence | Resolution |
| --- | --- | --- | --- |
| closed schema | covered | candidate schema `$` | unknown fields fail before semantics |
| frozen source | covered | execution contract `/source_snapshot` | aggregate, candidate bindings, and live bytes must match |
| proof ceiling | covered | design proof ledger | maximum is `planned_motion` |
| contradiction | covered | task algorithm | missing object is `SCHEMA_INVALID` |
| reduced motion | covered | validation contract | final semantic state equals standard |
| causal fixtures | covered | task edge cases | five one-cause mutants have exact codes |
| governance | covered | plan manifest and selection receipt | current epoch, unit digest, one attempt |

Strict coverage: `pass`.

## Constraints and non-goals

- Write only the ten exact material paths in `runtime-handoff.json#/write_scope`.
- Do not modify source media, AutoAds, the canonical Anime.js vault, public Arcanum, Git, network state, deployment state, or successor work.
- Passing OAVA-001 proves a candidate validator and fixtures only; it is not animation, browser, visual, runtime, or owner proof.

## Validation surface

Run from the refinement-run root:

`node --test prototype/test/candidate.test.mjs`

## Gaps and blockers

B-001 is resolved and unused. B-002 and B-003 are deferred to later portfolio units. No current gap permits fallback exploration or scope expansion.

## Authority precedence

1. Current plan-semantic manifest and binding-backed selection receipt.
2. `WORK-PACK.md` and `work-pack/execution-contract.json`.
3. `work-pack/tasks/TASK-OAVA-CONTRACTS.md`.
4. Candidate schema and selected design/validation sections.

## Fallback exploration rule

No broad exploration is admitted. Any new obligation, contradiction, or target stops before mutation.

## Output paths

- Markdown: this file.
- JSON/index: `runtime-handoff.json`.
