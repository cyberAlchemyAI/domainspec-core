# Lucifer's Lights — Craft View

> Human-readable projection only. The machine-readable source of truth is
> [`.craft/ledger.yml`](.craft/ledger.yml). If this view and the ledger disagree,
> the ledger wins.

## Project status

- Overall gate: `flag`
- Current stage: `review-audit`
- Manuscript state: Chapter 1 candidate revised; author acceptance pending
- Graphic-novel state: sixteen selected keyframes exist; prose-sync review pending
- Audio state: ElevenLabs script and production guide exist; render and revised-prose sync pending
- Ontology state: closed-world policy pass; author review pending
- Active blockers: none
- Open decisions: one non-blocking asset-location decision

The immediate next move is to read the revised
[Chapter 1](../../drafts/chapter-01.md) and either accept it as the project baseline
or record targeted corrections. Mechanical validation cannot make that creative
decision.

## Start here

- [Project brief](PROJECT.md)
- [Source and authority map](SOURCE-MAP.md)
- [Voice guide](editorial/VOICE-GUIDE.md)
- [Continuity register](story-bible/CONTINUITY.md)
- [Revision log](editorial/REVISION-LOG.md)
- [Chapter 1 editorial review](.craft/artifacts/chapter-01-editorial-review-2026-08-09.md)
- [Pre-revision Chapter 1 snapshot](.craft/artifacts/chapter-01-before-project-revision.md)
- [Bootstrap validation receipt](.craft/artifacts/bootstrap-validation-2026-08-09.md)
- [Whisper ontology](ontology/README.md)

## Contexts and next moves

### Context CTX-LL-ROOT

**Lucifer's Lights** — Track the manuscript, story continuity, editorial decisions,
graphic-novel assets, audio derivatives, gaps, gates, and next moves without
conflating them.

- Stage/gate: `review-audit` / `flag`
- Next move: read the revised Chapter 1 and either accept it as the project baseline
  or record targeted corrections.
- Child contexts: [manuscript](#context-ctx-ll-manuscript),
  [story bible](#context-ctx-ll-story-bible),
  [graphic novel](#context-ctx-ll-graphic-novel), and
  [audio and motion comic](#context-ctx-ll-audio), and
  [Whisper ontology](#context-ctx-ll-ontology).

### Context CTX-LL-MANUSCRIPT

Own prose development, chapter baselines, editorial review, voice discipline, and
revision history.

- Stage/gate: `review-audit` / `flag`
- Next move: run the human editorial read for Vesper clarity, tethered voice, and
  the sunrise clock.
- Pending: [voice continuity](#gap-gap-ll-voice-continuity-001) and
  [deadline continuity](#gap-gap-ll-deadline-continuity-001).

### Context CTX-LL-STORY-BIBLE

Record established characters, locations, rules, timelines, prop state, and
unresolved questions without inventing future canon.

- Stage/gate: `define` / `flag`
- Next move: update facts only after the Chapter 1 candidate is accepted or later
  chapters establish new evidence.
- Pending: [Vesper clarity](#gap-gap-ll-vesper-clarity-001) and
  [wider story-bible coverage](#gap-gap-ll-story-bible-001).

### Context CTX-LL-GRAPHIC-NOVEL

Own the visual bible, selected keyframes, shot mapping, lettering handoff, and later
motion-comic image timing.

- Stage/gate: `validate` / `flag`
- Next move: after prose acceptance, compare the shot manifest and selected
  keyframes against the revised chapter.
- Pending: [derivative synchronization](#gap-gap-ll-derivative-sync-001).

### Context CTX-LL-AUDIO

Own the ElevenLabs performance script, casting guide, voice auditions, narration
timing, and later motion-comic audio synchronization.

- Stage/gate: `plan` / `flag`
- Next move: after prose acceptance, synchronize the ElevenLabs script and generate
  the three voice auditions.
- Pending: [derivative synchronization](#gap-gap-ll-derivative-sync-001) and
  [audio rendering](#gap-gap-ll-audio-render-001).

### Context CTX-LL-ONTOLOGY

Govern the project-local authoring ontology for Whisper across intent, story
entities, evidence, commitment, mysteries, editorial rules, and derivative drift
without changing prose or canonical Arcanum vocabulary.

- Stage/gate: `validate` / `flag`
- Mechanical result: `policy-pass` for 12 sources, 21 nodes, 40 edges, 23 knowledge
  records, six edge policies, and six negative fixtures.
- Next move: review the Whisper intent, entity set, knowledge roles, edge policies,
  and deferred semantics, then accept or correct the candidate ontology.
- Pending: [ontology acceptance](#gap-gap-ll-ontology-acceptance-001) and
  [deferred semantics](#gap-gap-ll-ontology-deferred-semantics-001).

## Human gates

### Gate GATE-LL-CH01-EDITORIAL-001

- Status: `active`; human review required
- Source: [editorial review](.craft/artifacts/chapter-01-editorial-review-2026-08-09.md)
- Target: [current Chapter 1](../../drafts/chapter-01.md)
- Closure condition: the author reads the revised chapter and explicitly accepts
  Vesper clarity, the tethered interjections, and the carried sunrise deadline as
  the Chapter 1 baseline.
- Boundary: mechanical application and checks cannot replace authorial voice
  approval.

### Gate GATE-LL-ONTOLOGY-REVIEW-001

- Status: `active`; human review required
- Source: [ontology validation](ontology/receipts/validation-2026-08-09.json)
- Target: [candidate ontology](ontology/whisper-story-ontology.json)
- Closure condition: the author reviews and explicitly accepts the Whisper intent
  substrate, the three local story entity kinds, the knowledge roles and confidence
  states, the six edge policies, and the deferred semantics as the project's working
  authoring ontology.
- Boundary: a closed-world policy pass cannot approve author intent, canon
  commitment, or new semantic conventions.

## Decisions

### Decision DEC-LL-OPENING-ENGINE-001

- Status: `closed`
- Selection: `request-negotiation-terms-consequence`
- Result: the opening reveals Lucifer, the app, the Light economy, Mara's need, and
  the cost through a live transaction.

### Decision DEC-LL-VOICE-TETHER-001

- Status: `closed`
- Selection: `preserve-and-tether`
- Result: Lucifer's charismatic instability and direct address stay, while detached
  essays are compressed or relocated so each aside touches the scene.

### Decision DEC-LL-VESPER-CITY-001

- Status: `closed`
- Selection: `city-at-first-mention`
- Result: Vesper is established as the city at its first appearance.

### Decision DEC-LL-SUNRISE-CLOCK-001

- Status: `closed`
- Selection: `exact-clock-throughline`
- Result: the request, amendment, station sequence, and cliffhanger carry one exact
  5:38 sunrise deadline.

### Decision DEC-LL-ASSET-HOME-001

- Status: `active`, non-blocking
- Question: should the existing manuscript and generated media be moved physically
  under `projects/lucifers-lights/`?
- Current reversible behavior: reference the existing repository-root draft files in
  place.
- Default for later consideration: `move-after-chapter-baseline`
- Other options: keep references in place, or copy and archive the originals.
- Boundary: no files have been moved or duplicated during project bootstrap.

### Decision DEC-LL-ONTOLOGY-TYPE-001

- Status: `closed`
- Selection: `knowledge-vault`
- Local alias: `whisper-story-ontology`
- Result: the ontology governs narrative knowledge and its lifecycle; story-world
  modeling and authority routing remain supporting concerns.
- Boundary: the alias does not extend the reusable Ontology Vault catalog.

## Gaps

### Gap GAP-LL-VOICE-CONTINUITY-001

- Severity/status: `flag` / `active`
- Candidate edits tether the disconnected Lucifer interjections, but the author has
  not yet accepted the revised voice in a full read.
- Owner: `whisper-editorial`

### Gap GAP-LL-DEADLINE-CONTINUITY-001

- Severity/status: `flag` / `active`
- Candidate edits restore the sunrise deadline and countdown, but their felt urgency
  still requires author review.
- Owner: `whisper-editorial`

### Gap GAP-LL-VESPER-CLARITY-001

- Severity/status: `flag` / `active`
- Candidate prose defines Vesper as the city; clarity remains pending author
  confirmation in context.
- Owner: `whisper-editorial`

### Gap GAP-LL-STORY-BIBLE-001

- Severity/status: `info` / `active`
- The story bible covers Chapter 1 only. Wider city history, long-arc rules, and
  future-character continuity remain intentionally undefined.
- Owner: `author`

### Gap GAP-LL-DERIVATIVE-SYNC-001

- Severity/status: `flag` / `active`
- Graphic and ElevenLabs derivatives predate the current Chapter 1 revision and have
  not been checked or synchronized against it.
- Known example: the manuscript says Mara cuts the bracelet herself, while a visual
  derivative describes it being unclasped and opened with Lucifer's tool.
- Owner: `production`

### Gap GAP-LL-AUDIO-RENDER-001

- Severity/status: `deferred` / `active`
- No ElevenLabs voice audition, complete narration, measured timing, or synchronized
  motion-comic audio exists yet.
- Owner: `audio-production`

### Gap GAP-LL-ONTOLOGY-ACCEPTANCE-001

- Severity/status: `flag` / `active`
- Mechanical validation passes, but the author has not accepted the Whisper
  substrate, entity set, knowledge roles, edge policies, or deferred semantics.
- Owner: `author`

### Gap GAP-LL-ONTOLOGY-DEFERRED-SEMANTICS-001

- Severity/status: `info` / `active`
- Props, typed contracts and requests, organizations, temporal and causal relations,
  motivation, emotion, theme, place containment, and canonical namespace admission
  remain deliberately outside L0.
- Owner: `ontology-vault`

## Enablers

### Enabler ENA-LL-CH01-DRAFT-001

The complete Chapter 1 candidate provides a concrete editorial and derivative
baseline. Status: `pass` as an enabler, not as accepted prose.

### Enabler ENA-LL-VISUAL-SEQUENCE-001

The sixteen-frame selected sequence enables later lettering, timing, and motion work
after prose synchronization. Status: `pass` at the selected-keyframe level only.

## Local definitions

These definitions are project-local and do not claim broader canonical authority.

| ID | Term | Status | Working meaning |
| --- | --- | --- | --- |
| `DEF-LL-LIGHT-001` | Light | `active-local` | A bounded service governed by an explicit request, price, agreement, performance rule, and consequence. |
| `DEF-LL-OPEN-FAVOR-001` | open favor | `active-local` | Compensation whose future request is unspecified when the agreement is made. |
| `DEF-LL-VESPER-001` | Vesper | `active-local` | The renamed, rain-soaked city in which Chapter 1 takes place. |
| `DEF-LL-PRIOR-LIGHT-001` | prior Light | `active-local` | An older active agreement that takes precedence when a later request would violate it. |
| `DEF-LL-VOICE-TETHER-001` | voice tether | `candidate` | A Lucifer aside remains connected to a live person, rule, decision, danger, or clock. |

## Artifacts

| ID | Artifact | Status | Claim boundary |
| --- | --- | --- | --- |
| `ART-LL-LEDGER` | [Craft ledger](.craft/ledger.yml) | `active` | Machine-readable project-state authority. |
| `ART-LL-CRAFT-VIEW` | [This view](CRAFT.md) | `active` | Derived navigation only. |
| `ART-LL-PROJECT-BRIEF` | [Project brief](PROJECT.md) | `active` | Creative premise and working boundary. |
| `ART-LL-SOURCE-MAP` | [Source map](SOURCE-MAP.md) | `active` | Authority and derivation map. |
| `ART-LL-CHARACTERS` | [Characters](story-bible/CHARACTERS.md) | `active` | Chapter 1 facts and explicit unknowns. |
| `ART-LL-LOCATIONS` | [Locations](story-bible/LOCATIONS.md) | `active` | Chapter 1 location facts. |
| `ART-LL-CONTINUITY` | [Continuity](story-bible/CONTINUITY.md) | `active` | Timeline, contract chain, props, and questions. |
| `ART-LL-VOICE-GUIDE` | [Voice guide](editorial/VOICE-GUIDE.md) | `active` | Editorial tether rule. |
| `ART-LL-REVISION-LOG` | [Revision log](editorial/REVISION-LOG.md) | `active` | Append-only human history, not state authority. |
| `ART-LL-CH01-REVIEW` | [Editorial review](.craft/artifacts/chapter-01-editorial-review-2026-08-09.md) | `pass` | Approved repair scope; acceptance still pending. |
| `ART-LL-CH01-PRE-REVISION` | [Pre-revision snapshot](.craft/artifacts/chapter-01-before-project-revision.md) | `pass` | Recovery and comparison evidence. |
| `ART-LL-CH01-MANUSCRIPT` | [Current Chapter 1](../../drafts/chapter-01.md) | `flag` | Revised candidate awaiting author acceptance. |
| `ART-LL-CH01-SHOT-MANIFEST` | [Shot manifest](../../drafts/graphic-novel/chapter-01/shot-manifest.md) | `pass` | Sixteen selected beats; post-revision drift check pending. |
| `ART-LL-CH01-KEYFRAMES` | [Selected keyframes](../../drafts/graphic-novel/chapter-01/keyframes/) | `pass` | Selected image sequence, not a finished comic or video. |
| `ART-LL-CH01-VISUAL-ANCHOR` | [Halo meeting anchor](../../drafts/graphic-novel/chapter-01/visual-bible/halo-meeting-anchor.png) | `pass` | Visual identity/location reference. |
| `ART-LL-CH01-AUDIO-SCRIPT` | [ElevenLabs CSV](../../drafts/graphic-novel/chapter-01/audio/elevenlabs-voiceover-studio.csv) | `flag` | Predates the current revision; synchronization pending. |
| `ART-LL-CH01-AUDIO-GUIDE` | [Audio guide](../../drafts/graphic-novel/chapter-01/audio/elevenlabs-production-guide.md) | `flag` | Casting/timing plan; no render evidence. |
| `ART-LL-BOOTSTRAP-VALIDATION` | [Bootstrap validation](.craft/artifacts/bootstrap-validation-2026-08-09.md) | `pass` | Structural and inventory evidence only; not creative acceptance. |
| `ART-LL-ONTOLOGY-README` | [Ontology guide](ontology/README.md) | `active` | Entry point and update discipline. |
| `ART-LL-WHISPER-INTENT` | [Whisper intent](ontology/WHISPER-INTENT.md) | `flag` | Candidate authoring substrate; not audience prose. |
| `ART-LL-ONTOLOGY-GRAPH` | [Ontology graph](ontology/whisper-story-ontology.json) | `flag` | Mechanically valid candidate-local graph; author review pending. |
| `ART-LL-ONTOLOGY-MAP` | [Ontology map](ontology/ONTOLOGY-MAP.md) | `active` | Human map, not machine or canon authority. |
| `ART-LL-ONTOLOGY-PROFILE` | [Runtime profile](ontology/runtime-profile.json) | `active` | Inline source/output boundary; no production runtime. |
| `ART-LL-ONTOLOGY-VALIDATOR` | [Validator](ontology/scripts/validate.py) | `pass` | Closed-world mechanical checks only. |
| `ART-LL-ONTOLOGY-NEGATIVES` | [Negative fixtures](ontology/fixtures/closed-world-negatives.json) | `pass` | Six expected rejection witnesses. |
| `ART-LL-ONTOLOGY-VALIDATION` | [Validation receipt](ontology/receipts/validation-2026-08-09.json) | `pass` | Exact policy evidence with `authority_effect: none`. |

## Pending by node

- `CTX-LL-ROOT`: author editorial gate, asset-home decision, derivative
  synchronization; next read and accept or correct Chapter 1.
- `CTX-LL-MANUSCRIPT`: voice and deadline continuity; next perform the full human
  editorial read.
- `CTX-LL-STORY-BIBLE`: Vesper acceptance and intentionally partial coverage; next
  extend only from accepted or new prose evidence.
- `CTX-LL-GRAPHIC-NOVEL`: post-revision prose/visual comparison; next run after prose
  acceptance.
- `CTX-LL-AUDIO`: script synchronization and deferred rendering; next update the
  script, then create three auditions after prose acceptance.
- `CTX-LL-ONTOLOGY`: author acceptance and deliberately deferred semantics; next
  review the candidate ontology and either accept it as a working authoring aid or
  record corrections.

## Claim boundary

This project bootstrap records state; it does not publish, release, migrate, or freeze
the novel. The Chapter 1 repairs are candidate prose awaiting author review. Graphic
sequence completeness is limited to the selected-keyframe level. Lettering, prose
synchronization, synthesized audio, measured narration timing, motion, and final
video assembly remain pending. The Whisper ontology is a mechanically validated
candidate-local authoring aid; it does not accept the chapter, settle mysteries,
promote canon, implement a runtime, or extend canonical Arcanum vocabulary.
