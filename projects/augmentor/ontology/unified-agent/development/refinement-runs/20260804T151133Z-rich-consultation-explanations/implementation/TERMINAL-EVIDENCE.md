# Rich Consultation Explanations — Terminal Evidence

Status: **implemented and locally validated**  
Completed: `2026-08-04T16:40:43Z`  
Runtime: Node `22.13.0`

## Outcome

`SWU-RCE-000` through `SWU-RCE-008` are complete. The consultation route now accepts an optional `brief`, `guided`, or `deep` explanation profile and returns source-bound teaching support without returning final prose or changing the answer policy. The answering-agent adapter composes outside the API. The ontology page requests guided support by default, renders it as text, and exposes the same structured payload through `window.augmentorConsultationPage`.

This is local implementation evidence. It is not deployment, promotion, release, production proof, or proof of a working integrated reasoning engine.

## Measured Gates

| Gate | Result |
| --- | ---: |
| Installed compact bundle | 63,775 / 65,536 bytes |
| Records / glossary terms | 22 / 14 |
| Five questions × three profiles | 15 / 15 pass |
| Response bytes | 23,329–29,437 |
| Support bytes | 1,707–7,617 |
| Support estimated tokens | 427–1,905 |
| In-memory support assemblies | 3,000 |
| Assembly p50 / p95 | 0.058 ms / 0.725 ms |
| Evidence truth/status changes across profiles | 0 |
| Projection leakage hits | 0 |
| Browser page errors | 0 |

Bundle digest: `118ca29cbab34435235a065c654fa62232c3101a0e77cdee7cb9ed11c3933f1c`  
Projection digest: `ff1a3b2b4d79cc816dfbbac2711eaae19e43ef0b338d9a75812c7e98d753afdc`

## Validation

- Producer contract validation passed for query, result, and projection scopes.
- Producer consultation suite passed: 30 tests.
- Visualization suite passed: 7 tests.
- Targeted ResonantOS consultation/deployment/route suite passed: 11 tests.
- Browser acceptance passed twice at desktop and 320 px with reduced motion, keyboard flow, no horizontal overflow, no page errors, and expected console behavior.
- `test:module-ownership` passed: 2 tests.
- `docs:check` passed.
- `test:docs` passed: 224 tests.
- `verify:alpha` passed with exit 0, including hygiene, docs, build, 312 Vitest tests, browser-first tests, security certification, pre-release scan, and strict committed release-scope audit.

The build emitted the repository's non-failing large-chunk advisory. No acceptance gate failed.

## Boundaries And Residue

- No external research was run.
- No credentials were requested, printed, or stored.
- No deployment or external transport was changed.
- No Git commit or push was performed.
- Product bytes remain local and include pre-existing untracked/user-owned work; this report claims only the bounded work-pack changes and validations.
- The admission helper completed read-only with a flag about the live 1.1 family and untracked overlap; that finding was handled by explicit version reconciliation and scoped edits.
