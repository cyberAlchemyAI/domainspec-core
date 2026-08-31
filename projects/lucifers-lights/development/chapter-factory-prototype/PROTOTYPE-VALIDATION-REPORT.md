# Lucifer's Lights Chapter Factory MVP — Prototype Validation Report

## Outcome

The candidate-local Chapter Factory MVP and its local Voice Production seam are
implemented and validated. Chapter 1 is the pilot and is correctly stopped at
`review_pending`; the author decision remains `pending`, so the new voice
handoff is correctly `withheld`.

This result is not canonical manuscript acceptance, publication readiness,
deployment, or production readiness.

## Implemented workflow

1. Bind the exact manuscript and creative sources by path, size, and SHA-256.
2. Generate a chapter brief and a story-safe context manifest.
3. Import a candidate manuscript without changing it.
4. Run deterministic title, digest, length, marker, and clock checks.
5. Generate an editorial review and commentable HTML with stable paragraph IDs.
6. Stop for an explicit author decision against one exact manuscript digest.
7. Bind the chapter-owned motion-comic voice script to an explicit,
   chapter-neutral Voice Production compiler config.
8. Emit a ChapterRun-bound `voice-handoff.json` while withholding its admission,
   revision, export, derivatives, and the next chapter until the author gate is
   resolved.

The reusable entry point is `projects/lucifers-lights/chapter_pipeline/factory.py`.
The Chapter 1 configuration is `projects/lucifers-lights/factory/chapter-01.json`.
The operating guide is `projects/lucifers-lights/CHAPTER-FACTORY.md`.

## Chapter 1 pilot

- Run: `LL-CF-CH01-PILOT`
- Manuscript: `projects/lucifers-lights/drafts/chapter-01.md`
- Manuscript SHA-256: `ee57d5c8ef0ccd927d0ed267d6cc75ca38da8a71f93683bf68b9864352d2a64e`
- Manuscript mutation: none
- ChapterRun digest: `b062d4dc49c035c4940b3e8c37fb330819a7151854a5ad3d2fb9ce8cff1d79b9`
- Context sources: 11 exact bindings; manuscript prose omitted from the context manifest
- Mechanical checks: 14 pass
- Review blocks: 357 stable and unique IDs
- Factory result: `review_pending`
- Human gate: `pending`
- Generated review HTML SHA-256: `b396c162b70e0866014350a78dda2a8e3ecba77248cb9d1c2bdd494e1ddeab7c`
- Factory receipt SHA-256: `fa941655a6b9828b977f69f3f214d205f21c99a035c9ac7fb01c905ec19cd934`
- Voice handoff SHA-256: `e20742c81ea837df8307524b9aad5200cc0ab1090e8993d3f955b809018335dc`
- Voice admission: `withheld` / `author_acceptance_pending`

## Voice Production compatibility

- The compiler now requires a closed immutable config and contains no Chapter 1
  path, digest, speaker, count, or production defaults.
- Chapter 1 reproduces the prior manifest exactly: digest
  `2f7066e3ef1a1a2268f7bf6a374af8c6a44fcb86af6519ca6e1ed682b5e8940a`,
  canonical-byte SHA-256
  `916be43c6c4dcc9ead5f71ac170de181fe4c153db42c0407e121b33430807d37`,
  and 33,372 bytes.
- A materially different five-row synthetic source selects rows 1, 3, and 5
  into three segments with speakers `NARRATOR`, `ORACLE`, `NARRATOR`; its
  manifest digest is
  `43f8d3ce413f24a9f05b0742725df32cfe1717a9bcd0aaad55cc9f2302878e7d`.
- The complete local workflow digest is
  `51d4e782be00a6632575ae94b8d01c87930917d79bdaff74cc4ad4935ba4a2a8`,
  with every effect counter equal to zero.

## Validation

| Check | Result | Evidence |
|---|---|---|
| Focused factory tests | pass | 8 of 8 |
| Complete chapter-pipeline tests | pass | 28 of 28 |
| Complete Voice Production tests | pass | 89 of 89 |
| Chapter 1 voice-manifest parity | pass | exact digest, canonical-byte hash, and size |
| Synthetic voice reuse fixture | pass | different production, speakers, row selection, and manifest digest |
| Python compilation | pass | `python3 -m compileall -q projects/lucifers-lights/chapter_pipeline` |
| ChapterRun structural validation | pass | canonical digest matches the pilot receipt |
| Output inventory | pass | all 9 receipt-bound outputs match size and SHA-256 |
| Source binding | pass | 11 of 11 exact project-local sources |
| Synthetic reuse fixture | pass | a materially different synthetic Chapter 2 uses the same runtime |
| Drift behavior | pass | wrong manuscript digest blocks before output creation |
| Effect boundary | pass | runtime imports no network, provider, or subprocess client; external effects remain false |
| Scoped whitespace scan | pass | no unexpected trailing spaces or tabs in prototype text surfaces |
| Managed HTTP preview | pass | loopback-only HTTP 200 and exact served bytes |
| Chromium acceptance | pass | Playwright 1.59.1, Chromium revision 1217, ten stages at desktop and 390 px |
| Review interaction | pass | comment persisted at `p001`, entered the agent payload, then was removed |
| Browser isolation | pass | zero external requests, console errors, or page errors |
| Manuscript preservation | pass | final SHA-256 equals the admitted Chapter 1 digest |

The browser gate initially exposed an implicit favicon 404 and a narrow-layout
status card placed after the manuscript. Both defects were repaired in the
project-local generator and the final browser suite passed. Detailed evidence is
in `evidence/BROWSER-ACCEPTANCE.json` and the two inspected screenshots beside it.

## Deferred lifecycle work

Handoff Notice `HN-1DD250B3274B` records the original Chapter Factory deferred
bookkeeping. Handoff Notice `HN-1B6600771CA1` extends that local-only record to
the Voice Compatibility fast lane. Both are communication evidence only and
grant no additional authority.

The machine-readable consolidated result is
`evidence/VOICE-COMPAT-VALIDATION.json`.

## Voice continuation changed-byte inventory

- Voice implementation: `voice_production/compiler.py`,
  `voice_production/compiler_config.py`, and `voice_workflow.py`.
- Voice contracts and proof fixtures: `factory/voice/chapter-01.json`, the two
  `tests/fixtures/chapter-02-*` files, six migrated Voice test modules, and
  `projects/voice-production/README.md`.
- Factory integration: `chapter_pipeline/factory.py`, `factory/chapter-01.json`,
  `tests/chapter_pipeline/test_factory.py`, and `CHAPTER-FACTORY.md`.
- Regenerated pilot: the eight original managed outputs plus
  `voice-handoff.json` and `factory-receipt.json` under
  `development/chapter-factory-runs/chapter-01-pilot/`.
- Acceptance evidence: `BROWSER-ACCEPTANCE.json`, both review screenshots,
  `VOICE-COMPAT-VALIDATION.json`, the Voice fast-lane Handoff Notice input, and
  notice `HN-1B6600771CA1`.

## Explicit boundary

- Network/provider calls: none
- Secret access: none
- Media generation: none
- Publication/deployment: none
- Commit/push: none
- Canonical manuscript acceptance: not inferred

The next product decision belongs to the author: accept the exact Chapter 1 digest
above or submit paragraph-located corrections through the review page. A correction
creates a separate revision candidate; it does not rewrite the admitted manuscript
in place.
