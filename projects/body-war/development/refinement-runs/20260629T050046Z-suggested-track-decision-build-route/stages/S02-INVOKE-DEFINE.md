---
stage_id: s02-invoke-define
capability_ref: invoke
mode: define
status: pass
---

# S02 Invoke Define

## Defined Feature Unit

`SuggestedTrack` is the product anchor for natural track expansion.

```text
SuggestedTrack -> EvidenceRequest -> ActivityEvidenceCandidate -> SourceBackedTrack
```

## Approved Decision Slate

| Decision | Selected value | Rationale |
| --- | --- | --- |
| Suggested track visibility | Connected runners only in L0. | Useful for connected users without public route overclaim. |
| Suggestion creation | Login required before submit. | Keeps ownership, audit, and abuse control simple. |
| Taquaral seed | Versioned idempotent seed after Drizzle migration. | Treats Taquaral as data without polluting generated migration semantics. |
| Promotion authority | Operator-only promotion to `source_backed` in L0. | Preserves geometry honesty and review control. |
| Storage path | Existing Body War Postgres/Drizzle. | Existing app stack already has Drizzle/Postgres wiring. |
| Geometry claim | `needs_evidence` until source-backed promotion. | Lets the feature ship without pilot-ready overclaim. |
| One-go build scope | Docs, schema, migration, seed, API, UI, tests. | Broad enough to be usable; bounded below source-backed/pilot-ready claims. |

## Candidate Vocabulary

| Term | Meaning | Status |
| --- | --- | --- |
| `SuggestedTrack` | A route/place users want TROQAR to support. | selected local term |
| `EvidenceRequest` | A visible prompt asking connected runners for supporting evidence. | selected local term |
| `ActivityEvidenceCandidate` | One consent-attached redacted activity summary supporting a suggestion. | selected local term |
| `SourceBackedTrack` | A promoted track whose geometry/source evidence has been accepted. | deferred promotion term |

## Define Verdict

`pass`: product definition and defaults are sufficiently explicit for design.
The definition does not promote any candidate vocabulary beyond the Body War
feature scope.

