# Events: Tilth Runtime Build — Grant-Cycle Council Pipeline

Past-tense announcements of council-pipeline state changes. Every event is written to the WP-11 hash-chained audit log with payload class and content hash.

## OpportunityVerified

Fired when Scout's VERIFY stage assigns a verdict to a candidate.

**Produced by:** [`tilth-runtime-build.ScoutDiscovery`](operations.md#scoutdiscovery)
**Triggers transition:** [`tilth-runtime-build.OpportunityState`](states.md#opportunitystate) (Discovered → Verified)

### Payload

| Field | Type | Description |
| ----- | ---- | ----------- |
| candidateId | CandidateId | The verified candidate |
| verdict | VerificationVerdict | VERIFY outcome |

### Consumed By

| Consumer | Action |
| -------- | ------ |
| GrantCyclePipeline | Open a cycle if VERIFIED_FIT and human-approved at REVIEW |
| WP-11 Audit log | Record fetch + verdict with hash |

---

## DraftScored

Fired when Judge has scored every rubric dimension.

**Produced by:** [`tilth-runtime-build.JudgeScore`](operations.md#judgescore)
**Triggers transition:** [`tilth-runtime-build.DraftLifecycle`](states.md#draftlifecycle) (Edited → Scored)

### Payload

| Field | Type | Description |
| ----- | ---- | ----------- |
| draftId | DraftId | The scored draft |
| scores | RubricScore[] | Per-dimension scores |

### Consumed By

| Consumer | Action |
| -------- | ------ |
| RedTeamChallenge | Compute Judge/Red-Team delta |
| WP-13 Evidence/Report | Accepted draft feeds evidence capture |

---

## CouncilSplitRaised

Fired when the Judge/Red-Team delta reaches the split threshold (≥10, inclusive).

**Produced by:** [`tilth-runtime-build.RedTeamChallenge`](operations.md#redteamchallenge)
**Triggers transition:** [`tilth-runtime-build.DraftLifecycle`](states.md#draftlifecycle) (Scored → Challenged)

### Payload

| Field | Type | Description |
| ----- | ---- | ----------- |
| draftId | DraftId | The disputed draft |
| delta | int | Absolute Judge/Red-Team gap |

### Consumed By

| Consumer | Action |
| -------- | ------ |
| GrantCyclePipeline | Route to the HumanGate (Law 4 tie-breaker) |
| WP-11 Audit log | Record the split |

---

## DraftRevisionRequested

Fired when the Logician fail-closes a gate or the human directs a revision.

**Produced by:** [`tilth-runtime-build.LogicianGate`](operations.md#logiciangate)
**Triggers transition:** [`tilth-runtime-build.DraftLifecycle`](states.md#draftlifecycle) (Scored/Challenged → Revising)

### Payload

| Field | Type | Description |
| ----- | ---- | ----------- |
| draftId | DraftId | The draft to revise |
| failedGate | string | The fail-closed gate code |

### Consumed By

| Consumer | Action |
| -------- | ------ |
| ScribeDraft | Recompose flagged sections (two-audit cycle, L-005) |
| WP-11 Audit log | Record the gate failure |
