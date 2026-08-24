# Lucifer's Lights Project Bootstrap Validation

Date: 2026-08-09

Route: `craft`

Scope: `projects/lucifers-lights/`, current Chapter 1, and the existing Chapter 1
graphic/audio derivative inventory

Structural result: `pass`

Project gate: `flag` — author editorial acceptance remains pending

## Validated baseline

| Artifact | SHA-256 |
| --- | --- |
| `.craft/ledger.yml` | `0dcc5f616f713cc22e5dab7292ffebf627a69ad1eb59a9c58497a9dc72b8710f` |
| `CRAFT.md` | `26e892cf93d4d4f9f5858f9b1470cc0bb58f66fc10a71f169e33b7b31a9894d8` |
| `[repo-root] drafts/chapter-01.md` | `ee57d5c8ef0ccd927d0ed267d6cc75ca38da8a71f93683bf68b9864352d2a64e` |
| `.craft/artifacts/chapter-01-before-project-revision.md` | `7719ad12d2e8e0635cdfaca4af555e0aada15ce67568204495ac6b566378feb5` |

The hashes identify the bytes checked in this bootstrap. A later edit makes this
receipt historical evidence rather than current validation.

## Craft structural validation

Result: `pass`

- Parsed the YAML ledger against the field, reference, enum, path, and embedded-index
  contracts in Craft schema version `0.3.0`.
- Resolved `schema_ref` to
  `[repo-root] arcanum/arcana/craft/templates/ledger.schema.yml`.
- Checked 52 stable rows: 5 contexts, 18 artifacts, 5 descriptions, 5 local
  definitions, 3 typed items, 5 decisions, 6 gaps, and 5 relations.
- Confirmed every `by_id` selector against the row arrays.
- Confirmed `open_decisions`, `blocking_decisions`, `active_blockers`, `active_gaps`,
  `next_moves`, and `artifacts_by_path` are fresh.
- Confirmed every registered artifact path exists.
- Confirmed the human view exposes the tracked contexts, decisions, gaps, pending
  work by node, and claim boundary.

This proves ledger structure and reference integrity. It does not prove that open
creative gaps are resolved.

## Chapter 1 mechanical validation

Result: `pass`

- Current candidate: 715 lines, 3,142 whitespace-delimited words, 19,648 UTF-8
  bytes.
- Preserved snapshot: 703 lines, 3,155 whitespace-delimited words, 19,666 UTF-8
  bytes.
- Candidate versus snapshot: 33 added/replacement lines and 21
  removed/replacement lines by sequence comparison.
- Confirmed Vesper is identified as the city at first mention.
- Confirmed sunrise is fixed at 5:38 and the amended request retains
  `DEADLINE: SUNRISE`.
- Confirmed clock arithmetic: 2:13→5:38 is 205 minutes, 2:43→5:38 is 175
  minutes, and 2:51→5:38 is 167 minutes.
- Confirmed the matching prose countdowns and the removal of the duplicated final
  timestamp.
- Confirmed `Of course she did.` replaced `Good girl.`
- Confirmed no trailing whitespace in the current chapter.

These checks prove presence and arithmetic, not felt pace, voice quality, or author
acceptance.

## Derivative inventory validation

Result: `pass` at inventory level

- Parsed sixteen selected image paths from the shot-manifest table and confirmed all
  exist.
- Confirmed one preserved, unselected first KF13 candidate exists for comparison.
- Read PNG headers for all seventeen files and confirmed 1672 × 941 dimensions.
- Parsed 112 rows and five speakers in the ElevenLabs CSV.
- Did not synthesize, audition, time, letter, animate, or render media.
- Did not close the known prose/visual bracelet mismatch or synchronize the audio
  script to the current prose.

## Scoped whitespace validation

Result: `pass`

Thirteen Markdown/YAML files were checked: the current chapter plus the project
documents then present. No trailing spaces or tabs were found.

## Background helper receipt

One bounded read-only helper, `/root/lucifers_lights_craft_audit`, audited the Craft
shape and current evidence. It made no file or Git changes. Its material findings
were incorporated as follows:

- corrected the ledger schema path to be relative to `.craft/ledger.yml`;
- preserved the human editorial gate instead of treating candidate edits as closed;
- refreshed the chapter before ledger materialization because the file changed during
  the helper's read;
- kept visual completion bounded to manifest-selected keyframes and audio work bounded
  to prepared, unrendered inputs.

The helper is closed. Its advisory row-minimization proposal was not adopted wholesale:
the author asked for a durable project, so the ledger also retains separate manuscript,
story-bible, graphic-novel, and audio contexts, plus local definitions and traceable
relations. Those extra rows passed the same structural checks.

## Corrected test assumptions

The first content-check draft raised two false flags:

1. It expected different English phrasing for the 2:13 and 2:43 countdowns. The
   check was corrected to the actual prose, then the arithmetic was validated
   separately.
2. It inferred the retained KF13 candidate from the word `variant` in its filename.
   The manifest instead selects `kf13-locker-dead-drop-v2.png` and explicitly preserves
   `kf13-locker-dead-drop.png` for comparison. The inventory check was corrected to
   parse selected paths from the manifest.

No story bytes were changed to satisfy either mistaken test.

## Residue and next gate

- Human read of the revised Chapter 1 remains required.
- The voice, sunrise urgency, and Vesper clarity gaps remain active until that read.
- The graphic and audio derivatives still require comparison with accepted prose.
- The physical home of existing draft/media assets remains an open, non-blocking
  author decision.
- No commit, move, publication, release, deployment, or external generation occurred.
