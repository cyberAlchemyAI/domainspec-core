# Domain: Tilth Runtime Build — Grant-Cycle Council Pipeline

Structural concepts for the council pipeline slice. Entities link to their state machines and to the council-seat operations that act on them.

## Entities

### GrantCycle

A single end-to-end run of the council pipeline for one organization's pursuit of one opportunity. One PROJECT_CONTEXT per cycle (Law 3 — Org Isolation); the cycle's `orgSlug` is structural and never crosses into another org's data.

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| id | CycleId | yes | Unique cycle identifier |
| orgSlug | string | yes | Owning org slug; Law-3 structural boundary |
| opportunityId | CandidateId | yes | The verified opportunity driving the cycle |
| gear | [OperatingGear](#operatinggear) | yes | Active seat gear (default co_pilot) |
| status | [GrantCycleStatus](states.md#grantcyclestatus) | yes | Current cycle phase |

**Lifecycle:** See [GrantCycleStatus](states.md#grantcyclestatus)
**Operations:** [LogicianGate](operations.md#logiciangate)

---

### Draft

A proposal in progress, composed section by section by Scribe and refined by Editor. Every section claim must trace to the RFA or PROJECT_CONTEXT (Law 1); the draft carries provenance and embedded rubric scores.

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| id | DraftId | yes | Unique draft identifier |
| cycleId | CycleId | yes | Owning [GrantCycle](#grantcycle) |
| sections | Section[] | yes | Ordered proposal sections |
| provenance | [SectionProvenance](#sectionprovenance)[] | yes | Source ref per section claim |
| scores | [RubricScore](#rubricscore)[] | no | Populated after JudgeScore |
| status | [DraftLifecycle](states.md#draftlifecycle) | yes | Current draft state |

**Lifecycle:** See [DraftLifecycle](states.md#draftlifecycle)
**Operations:** [ScribeDraft](operations.md#scribedraft), [EditorPass](operations.md#editorpass), [JudgeScore](operations.md#judgescore), [RedTeamChallenge](operations.md#redteamchallenge)
**Source of event:** [DraftScored](events.md#draftscored)

---

### OpportunityCandidate

A funding opportunity surfaced by Scout. A candidate cannot be elevated to CRITICAL-fit without a passed live-synopsis VERIFY stage. The applicant CIC never pre-binds a CLC subset (orthogonal axes; matching is opportunity-driven runtime).

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| id | CandidateId | yes | Unique candidate identifier |
| sourceChannel | string | yes | One of six channel families A–F |
| verdict | [VerificationVerdict](#verificationverdict) | yes | VERIFY-stage outcome |
| synopsisFetchedAt | DateTime | no | Live-synopsis fetch timestamp |

**Lifecycle:** See [OpportunityState](states.md#opportunitystate)
**Operations:** [ScoutDiscovery](operations.md#scoutdiscovery)
**Source of event:** [OpportunityVerified](events.md#opportunityverified)

---

## Value Objects

### RubricScore

A per-dimension score produced by Judge against the funder rubric. Each score's evidence string must appear verbatim in the draft (Rule 2 — the magic step).

| Field | Type | Constraint |
| ----- | ---- | ---------- |
| dimension | string | Rubric criterion name |
| points | int | 0 ≤ points ≤ dimensionMax |
| evidenceString | string | Must occur in [Draft](#draft).sections |

**Equality:** Two RubricScores are equal iff `dimension`, `points`, and `evidenceString` match.

---

### SectionProvenance

A traceability record binding one section claim to its authoritative source (Law 1 — RFA Is the Source of Truth).

| Field | Type | Constraint |
| ----- | ---- | ---------- |
| sectionId | string | Section the claim belongs to |
| sourceKind | string | `rfa` or `project_context` |
| sourceRef | string | Locator into RFA or PROJECT_CONTEXT |

**Equality:** Equal iff all three fields match.

---

## Enums

### CouncilSeat

| Value | Description |
| ----- | ----------- |
| scout | Two-stage discovery (DISCOVER/VERIFY/REVIEW) |
| scribe | Section-by-section drafting |
| editor | Clarity pass with replacement options |
| judge | Rubric scoring; cross-family vs scribe |
| red_team | Adversarial challenge; cross-family vs scribe + judge |
| logician | Deterministic Python + Cedar gate; fail-closed |

### OperatingGear

| Value | Description |
| ----- | ----------- |
| sparring_partner | Seat generates options; human decides |
| co_pilot | Human directs, seat executes/refines (DEFAULT) |
| synthesizer | Full delegation; human reviews final only |

### VerificationVerdict

| Value | Description |
| ----- | ----------- |
| VERIFIED_FIT | Live synopsis confirms fit |
| VERIFIED_NOT_FIT | Live synopsis confirms not a fit |
| UNVERIFIED | No live endpoint available |
| VERIFICATION_FAILED | Verify attempt errored |
