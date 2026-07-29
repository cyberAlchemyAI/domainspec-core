---
module: body-war-login-suggest-track-score-preview
version: current
status: candidate-local
updatedAt: 2026-07-28
docType: ontology-vault-candidate-map
authorityEffect: none
---

# Candidate Ontology Map: Login to Score Preview

## Branches

### Business branch

| ID | Kind | Meaning | Confidence |
| --- | --- | --- | --- |
| `bw.runner` | actor | Person using Body War to turn a run into track evidence and a visible result. | high |
| `bw.connected-runner` | role | Runner with an active Body War session and linked Strava account. | high |
| `bw.suggested-track` | entity | Proposed route awaiting evidence and, separately, source backing. | high |
| `bw.runner-confirmation` | event | Explicit consent binding one runner, one SuggestedTrack, one activity, and one geometry-use statement. | medium |
| `bw.activity-evidence-candidate` | evidence | Redacted activity facts retained for later review. | high |
| `bw.geometry-candidate` | evidence | Privacy-filtered route shape derived from consented activity data. | medium |
| `bw.score-policy` | rule | Versioned numeric calculation including all normalizers and caps. | low until decision gate |
| `bw.score-input-snapshot` | evidence | Canonical policy-window calculation inputs and provenance; never raw provider streams. | medium |
| `bw.score-preview` | read-model | Explained, non-authoritative score calculated from named candidate evidence. | medium |
| `bw.source-backed-track` | promoted-state | SuggestedTrack whose source or geometry evidence was accepted by an operator. | high |

### System branch

| ID | Kind | Realization | Confidence |
| --- | --- | --- | --- |
| `sys.browser-session` | component | Existing signed session and CSRF path. | high |
| `sys.strava-oauth-adapter` | component | Existing OAuth exchange and provider-account binding. | high |
| `sys.activity-list-gateway` | component | Existing interface; current implementation returns repository fixtures. | high |
| `sys.activity-geometry-gateway` | component | Proposed activity detail/stream fetch for one selected activity. | medium |
| `sys.geometry-normalizer` | component | Proposed stream alignment, validation, privacy filtering, simplification, digest, and metrics. | medium |
| `sys.score-input-assembler` | component | Proposed canonical window, eligibility, derived-metric, aggregation, and provenance builder. | low until policy decision |
| `sys.score-preview-calculator` | component | Proposed deterministic calculator over a ratified ScorePolicy. | low until policy decision |
| `sys.score-preview-projection` | interface | Proposed authenticated API and web card. | medium |
| `sys.prototype-receipt` | evidence | Records provider mode, policy version, selectors, input digests, result, and claim ceiling. | medium |

## Business Relationships

| From | Edge | To | Evidence or rule |
| --- | --- | --- | --- |
| `bw.runner` | becomes | `bw.connected-runner` | successful Strava OAuth callback and Body War session |
| `bw.connected-runner` | proposes | `bw.suggested-track` | existing `CreateSuggestedTrack` |
| `bw.connected-runner` | emits | `bw.runner-confirmation` | visible affirmative consent |
| `bw.runner-confirmation` | binds | `bw.activity-evidence-candidate` | exact track/activity/consent identity |
| `bw.activity-evidence-candidate` | supports | `bw.geometry-candidate` | selected activity geometry use was consented |
| `bw.geometry-candidate` | contributes_to | `bw.score-input-snapshot` | exact geometry digest |
| `bw.score-input-snapshot` | contributes_to | `bw.score-preview` | versioned canonical calculation input |
| `bw.score-policy` | governs | `bw.score-preview` | exact policy ID and digest |
| `bw.score-preview` | does_not_promote | `bw.source-backed-track` | authority ceiling |

## System Relationships

| From | Edge | To | Contract |
| --- | --- | --- | --- |
| `sys.browser-session` | authorizes | `sys.activity-list-gateway` | `body-war.activity.read` |
| `sys.activity-list-gateway` | selects_for | `sys.activity-geometry-gateway` | activity belongs to authenticated principal |
| `sys.activity-geometry-gateway` | feeds | `sys.geometry-normalizer` | aligned `latlng`, `distance`, and `time` streams |
| `sys.geometry-normalizer` | feeds | `sys.score-input-assembler` | validated `GeometryCandidate` plus digest |
| `sys.activity-geometry-gateway` | feeds | `sys.score-input-assembler` | privacy-safe derived qualifying metrics under the ratified window |
| `sys.score-input-assembler` | feeds | `sys.score-preview-calculator` | canonical `ScoreInputSnapshot` |
| `sys.score-preview-calculator` | feeds | `sys.score-preview-projection` | `ScorePreview` |
| `sys.score-preview-calculator` | observed_by | `sys.prototype-receipt` | input/output digests and policy version |

## Bridge Relationships

| Business node | Edge | System node | Alignment evidence | Drift |
| --- | --- | --- | --- | --- |
| `bw.connected-runner` | realized_by | `sys.browser-session` | current auth tests and callback path | real account witness still absent |
| `bw.activity-evidence-candidate` | realized_by | existing repository and evidence API | current local tests | consent UI currently manufactures affirmation |
| `bw.geometry-candidate` | realized_by | `sys.geometry-normalizer` | planned contract only | no geometry type, gateway, or storage yet |
| `bw.score-policy` | realized_by | `sys.score-preview-calculator` | planned contract only | weights exist; normalizers and caps do not |
| `bw.score-input-snapshot` | realized_by | `sys.score-input-assembler` | planned contract only | fixture and real history contracts are not implemented |
| `bw.score-preview` | realized_by | `sys.score-preview-projection` | planned API/UI witness | current API explicitly says scoring not claimed |
| `bw.runner-confirmation` | constrained_by | exact consent identity and CSRF rules | existing server validation plus LP-01 finding | track binding and affirmative control are open |
| `bw.geometry-candidate` | constrained_by | least privilege and private-by-default visibility | official Strava scope contract | private activities excluded in first prototype |
| `bw.score-preview` | tested_by | fake-provider and real-provider witness lanes | planned witnesses | lanes must retain separate verdicts |
| `bw.source-backed-track` | drifts_from | `bw.geometry-candidate` | existing lifecycle | automatic promotion would violate owner boundary |
| every bridge row | traced_to | exact source selectors and receipts | Design manifest and execution receipt; prior BWOI is immutable CT-2-only historical context | no bridge claim without selector/digest |

## Candidate State Machines

```text
Runner:
  anonymous -> oauth_pending -> connected

SuggestedTrack (existing):
  none -> needs_evidence -> evidence_submitted
  evidence_submitted -> operator_review -> source_backed   [not in prototype]

GeometryCandidate (new and separate):
  absent -> fetch_pending -> derived_candidate
  fetch_pending -> unavailable | rejected
  derived_candidate -> superseded

ScorePreview (new and separate):
  unavailable -> snapshot_pending -> calculation_pending -> available
  snapshot_pending -> incomplete_projection | blocked_policy | blocked_geometry
  calculation_pending -> failed
  available -> superseded
```

## Contradictions and Next Gates

| ID | Contradiction or gap | Disposition | Next gate |
| --- | --- | --- | --- |
| `ONT-GAP-001` | Current ActivitySummary omits geometry while the requested journey requires it. | Add a selected-activity geometry gateway; keep list response redacted. | implementation |
| `ONT-GAP-002` | Existing evidence consent excludes maps; the new journey needs explicit geometry-use consent. | Version the consent contract and bind displayed/affirmed/transmitted/persisted text. | decision + implementation |
| `ONT-GAP-003` | Score weights total 100% and cap at 550, but normalization is undefined. | Ratify ScorePolicy V0 before numeric score code. | decision-gate |
| `ONT-GAP-004` | A runner-derived route can be useful but is not official/source-backed. | Store and render it as a private candidate only. | operator-policy decision for later promotion |
| `ONT-GAP-005` | Real Strava adapter is synthetic despite successful OAuth structure. | Implement token read/decrypt/refresh and official API gateway. | implementation + supervised witness |
| `ONT-GAP-006` | No canonical complete-window score input exists; a single geometry-seeding activity is not a comparable 14-day score. | Add `ScoreInputSnapshot`; use complete-window fixtures in L0 and suppress comparable totals for incomplete real history. | decision + implementation |

## Vault Boundary

This map is a Body War candidate artifact. It has `authority_effect: none`,
does not mutate CyberAlchemy ontology, and does not promote any concept,
geometry, score policy, track, or release state.
