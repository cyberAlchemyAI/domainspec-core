# Source Map

This file describes ownership and derivation. Project state itself is owned by [.craft/ledger.yml](.craft/ledger.yml).

| Surface | Path | Role | Current status |
|---|---|---|---|
| Project ledger | `.craft/ledger.yml` | Authoritative project state | Active |
| Human status | `CRAFT.md` | Derived linked view | Active |
| Project brief | `PROJECT.md` | Creative intent and boundary | Active |
| Chapter 1 manuscript | `[repo-root] drafts/chapter-01.md` | Canonical current prose | Editorial candidate; human review pending |
| Pre-revision Chapter 1 | `.craft/artifacts/chapter-01-before-project-revision.md` | Immutable recovery snapshot | Historical evidence |
| Chapter 1 editorial review | `.craft/artifacts/chapter-01-editorial-review-2026-08-09.md` | Review evidence and approved repair scope | Pass as review evidence |
| Story bible | `story-bible/*.md` | Current Chapter 1 facts and unresolved continuity | Active-local reference |
| Voice guide | `editorial/VOICE-GUIDE.md` | Editorial constraint | Active-local reference |
| Revision log | `editorial/REVISION-LOG.md` | Append-only human change history | Active |
| Whisper intent | `ontology/WHISPER-INTENT.md` | Derived composition substrate | Candidate; author review pending |
| Whisper ontology | `ontology/whisper-story-ontology.json` | Candidate-local story knowledge graph and source registry | Mechanical policy pass; author review pending |
| Ontology map | `ontology/ONTOLOGY-MAP.md` | Human-readable Ontology Vault map | Active derived view |
| Ontology runtime profile | `ontology/runtime-profile.json` | Inline read/output/gate boundary | Candidate-local |
| Ontology validation | `ontology/scripts/validate.py`, `ontology/fixtures/`, `ontology/receipts/` | Closed-world policy checks, negative fixtures, and evidence | Mechanical pass; authority effect none |
| Graphic shot manifest | `[repo-root] drafts/graphic-novel/chapter-01/shot-manifest.md` | Image-sequence derivative | Needs post-revision drift check |
| Keyframes | `[repo-root] drafts/graphic-novel/chapter-01/keyframes/` | Generated visual derivatives | Sixteen selected plus one retained variant |
| Visual anchor | `[repo-root] drafts/graphic-novel/chapter-01/visual-bible/halo-meeting-anchor.png` | Character/style reference | Approved visual anchor |
| ElevenLabs CSV | `[repo-root] drafts/graphic-novel/chapter-01/audio/elevenlabs-voiceover-studio.csv` | Audio-script derivative | Needs post-revision sync |
| ElevenLabs guide | `[repo-root] drafts/graphic-novel/chapter-01/audio/elevenlabs-production-guide.md` | Voice and timing guidance | Needs post-revision sync |

## Authority rule

The manuscript owns prose. The story bible records established facts but cannot silently override the manuscript. The Whisper ontology owns only its candidate-local graph, knowledge records, and validation conventions; it cannot accept prose, settle mysteries, or promote canon. Graphic and audio artifacts derive from the manuscript; their existence does not make a prose change canonical. The Craft ledger owns issue, decision, gap, gate, and next-move status.

## Asset-location decision

Existing untracked manuscript and media files remain at their current repository-root paths during this first project bootstrap. This avoids risky movement and duplicated creative authority. Whether to consolidate them physically under `projects/lucifers-lights/` remains an explicit non-blocking decision in the Craft ledger.
