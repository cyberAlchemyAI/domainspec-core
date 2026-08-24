# Body War Business Ontology Views

Status: `generated-projection`

This document instantiates the CyberAlchemy v2 branch-as-view pattern for the
Body War `business` meaning branch. It is generated from validated nodes,
relations, and lifecycle policies. It is navigation and explanation, not a
definition store, promotion decision, DomainSpec graph, or runtime proof.

## Which CAV2 view exists here?

| CAV2 view role | Body War state | What it can answer |
| --- | --- | --- |
| Ontology / meaning view | **Instantiated here** as the `business` branch. | What the business concepts mean, how they relate, their confidence/status, and which owner gate remains. |
| System view | **Not yet modeled.** | Would require typed components, services, endpoints, schemas, tests, telemetry, and runtime constraints with current evidence. |
| Business-system bridge view | **Not yet modeled.** | Would require evidence-backed `realized_by`, `tested_by`, `observed_by`, `constrained_by`, `drifts_from`, or `traced_to` edges on both sides. |

The absence of system and bridge views is deliberate. Existing application code
must not be inferred into ontology alignment without a separate source-bound map
and bridge validation.

## How to read the diagrams

- Boxes are candidate ontology nodes. The second line is `business_kind · candidate_status`.
- Solid arrows are admitted non-blocked relations.
- Dotted arrows are blocked, projection-only, or explicit `does_not_promote` relations.
- Green means `reviewed-candidate`; amber means `candidate`; red means `blocked`; gray means `deferred`; blue means `projected`.
- An arrow states business meaning only. It does not prove implementation or runtime behavior.

A [print-friendly HTML gallery](BUSINESS-VIEWS.html) contains the same relation
sentences as individually paginating rows.

For a progressive-disclosure review, open the
[interactive journey experiment](BUSINESS-JOURNEY-EXPERIMENT.html). It begins
with ordinary-language stories and reveals ontology metadata on request.

## Relation sentence example

The visible phrase makes the business meaning readable; the predicate under the
arrow preserves the exact typed relation.

![Import Activities relation sentences](generated/views/import-activities.svg)

- [Import Activities](nodes/operation.import-activities.json) **uses as input** [ProviderAccount](nodes/entity.provider-account.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-7`.
- [Import Activities](nodes/operation.import-activities.json) **creates or emits** [RunActivity](nodes/entity.run-activity.json). Typed predicate: `produces`; relation: `body-war.relation.operation-8`.

**Boundary:** This projection does not prove that provider authorization, activity import, persistence, or live Strava data works.

## Business view map

```mermaid
flowchart TB
  B["Body War business meaning branch"]
  B --> C["Capability branches<br/>who owns what"]
  B --> J["Runner journey<br/>login to ScorePreview"]
  B --> E["Evidence chain<br/>activity to controller"]
  B --> T["Territory loop<br/>control, invasion, defense"]
  B --> P["Progression loop<br/>challenges, XP, clans, seasons"]
  B --> L["Lifecycle views<br/>what may change state"]
  S["System branch<br/>not yet modeled"]
  G["Business-system bridge<br/>not yet modeled"]
  B -. requires later source-bound map .-> S
  B -. requires two-sided evidence .-> G
  S -. contributes system evidence .-> G
```

The business branch explains **what Body War means**. A future system branch
would explain **what software exists**. A future bridge would show **which
software realizes, constrains, observes, or tests which business meaning**.

## Business capability branches

**Question:** Which business contexts own which capabilities, and what must exist before the prototype score path can work?

**Represents:** A business-responsibility map. Contexts own capabilities; dependency arrows state prerequisite meaning, not module imports or runtime calls.

![Business capability branches: typed relation sentences](generated/views/business-capability-map.svg)

<details>
<summary>Open Mermaid network projection</summary>

```mermaid
flowchart LR
  N0["Selected Activity Geometry<br/>capability · blocked"]
  N1["Activity Import<br/>capability · reviewed-candidate"]
  N2["Authentication and Consent<br/>capability · reviewed-candidate"]
  N3["Challenges and Missions<br/>capability · reviewed-candidate"]
  N4["Community and Clans<br/>capability · reviewed-candidate"]
  N5["Control and Ownership<br/>capability · reviewed-candidate"]
  N6["Evidence Candidate Attachment<br/>capability · reviewed-candidate"]
  N7["Evidence Submission<br/>capability · reviewed-candidate"]
  N8["Rankings and Seasons<br/>capability · reviewed-candidate"]
  N9["Explained Score Preview<br/>capability · blocked"]
  N10["Score and XP<br/>capability · reviewed-candidate"]
  N11["Suggested Track Creation<br/>capability · reviewed-candidate"]
  N12["Suggested Track Discovery<br/>capability · reviewed-candidate"]
  N13["Track and Territory Catalog<br/>capability · reviewed-candidate"]
  N14["Activity Evidence<br/>bounded_context · reviewed-candidate"]
  N15["Community<br/>bounded_context · reviewed-candidate"]
  N16["Control and Competition<br/>bounded_context · reviewed-candidate"]
  N17["Candidate Geometry Evidence<br/>bounded_context · candidate"]
  N18["Identity and Consent<br/>bounded_context · reviewed-candidate"]
  N19["Progression<br/>bounded_context · reviewed-candidate"]
  N20["Suggested Track Route Expansion<br/>bounded_context · reviewed-candidate"]
  N21["Score Preview<br/>bounded_context · blocked"]
  N22["Territory Catalog<br/>bounded_context · reviewed-candidate"]
  N18 -->|"groups as its responsibility"| N2
  N14 -->|"groups as its responsibility"| N1
  N14 -->|"groups as its responsibility"| N7
  N20 -->|"groups as its responsibility"| N12
  N20 -->|"groups as its responsibility"| N11
  N20 -->|"groups as its responsibility"| N6
  N17 -->|"groups as its responsibility"| N0
  N21 -->|"groups as its responsibility"| N9
  N22 -->|"groups as its responsibility"| N13
  N16 -->|"groups as its responsibility"| N5
  N19 -->|"groups as its responsibility"| N10
  N19 -->|"groups as its responsibility"| N8
  N15 -->|"groups as its responsibility"| N3
  N15 -->|"groups as its responsibility"| N4
  N12 -->|"needs"| N2
  N11 -->|"needs"| N2
  N6 -->|"needs"| N12
  N6 -->|"needs"| N1
  N0 -->|"needs"| N6
  N0 -->|"needs"| N2
  N9 -->|"needs"| N0
  N9 -->|"needs"| N10
  classDef reviewed_candidate fill:#e8f5e9,stroke:#2e7d32,color:#16351b
  classDef candidate fill:#fff8e1,stroke:#f9a825,color:#4a3500
  classDef blocked fill:#ffebee,stroke:#c62828,color:#5a1010
  classDef deferred fill:#eceff1,stroke:#607d8b,color:#263238
  classDef projected fill:#e3f2fd,stroke:#1565c0,color:#0d315f
  class N0 blocked
  class N1 reviewed_candidate
  class N2 reviewed_candidate
  class N3 reviewed_candidate
  class N4 reviewed_candidate
  class N5 reviewed_candidate
  class N6 reviewed_candidate
  class N7 reviewed_candidate
  class N8 reviewed_candidate
  class N9 blocked
  class N10 reviewed_candidate
  class N11 reviewed_candidate
  class N12 reviewed_candidate
  class N13 reviewed_candidate
  class N14 reviewed_candidate
  class N15 reviewed_candidate
  class N16 reviewed_candidate
  class N17 candidate
  class N18 reviewed_candidate
  class N19 reviewed_candidate
  class N20 reviewed_candidate
  class N21 blocked
  class N22 reviewed_candidate
```

</details>

### Read the arrows as sentences

- [Identity and Consent](nodes/context.identity-consent.json) **groups as its responsibility** [Authentication and Consent](nodes/capability.auth-consent.json). Typed predicate: `owns`; relation: `body-war.relation.context-1`.
- [Activity Evidence](nodes/context.activity-evidence.json) **groups as its responsibility** [Activity Import](nodes/capability.activity-import.json). Typed predicate: `owns`; relation: `body-war.relation.context-2`.
- [Activity Evidence](nodes/context.activity-evidence.json) **groups as its responsibility** [Evidence Submission](nodes/capability.evidence-submission.json). Typed predicate: `owns`; relation: `body-war.relation.context-3`.
- [Suggested Track Route Expansion](nodes/context.route-expansion.json) **groups as its responsibility** [Suggested Track Discovery](nodes/capability.suggested-track-discovery.json). Typed predicate: `owns`; relation: `body-war.relation.context-14`.
- [Suggested Track Route Expansion](nodes/context.route-expansion.json) **groups as its responsibility** [Suggested Track Creation](nodes/capability.suggested-track-creation.json). Typed predicate: `owns`; relation: `body-war.relation.context-15`.
- [Suggested Track Route Expansion](nodes/context.route-expansion.json) **groups as its responsibility** [Evidence Candidate Attachment](nodes/capability.evidence-candidate-attach.json). Typed predicate: `owns`; relation: `body-war.relation.context-16`.
- [Candidate Geometry Evidence](nodes/context.geometry-evidence.json) **groups as its responsibility** [Selected Activity Geometry](nodes/capability.activity-geometry.json). Typed predicate: `owns`; relation: `body-war.relation.context-17`.
- [Score Preview](nodes/context.score-preview.json) **groups as its responsibility** [Explained Score Preview](nodes/capability.score-preview.json). Typed predicate: `owns`; relation: `body-war.relation.context-18`.
- [Territory Catalog](nodes/context.territory-catalog.json) **groups as its responsibility** [Track and Territory Catalog](nodes/capability.track-territory-catalog.json). Typed predicate: `owns`; relation: `body-war.relation.context-4`.
- [Control and Competition](nodes/context.control-competition.json) **groups as its responsibility** [Control and Ownership](nodes/capability.control-ownership.json). Typed predicate: `owns`; relation: `body-war.relation.context-5`.
- [Progression](nodes/context.progression.json) **groups as its responsibility** [Score and XP](nodes/capability.score-xp.json). Typed predicate: `owns`; relation: `body-war.relation.context-6`.
- [Progression](nodes/context.progression.json) **groups as its responsibility** [Rankings and Seasons](nodes/capability.rankings-seasons.json). Typed predicate: `owns`; relation: `body-war.relation.context-7`.
- [Community](nodes/context.community.json) **groups as its responsibility** [Challenges and Missions](nodes/capability.challenges-missions.json). Typed predicate: `owns`; relation: `body-war.relation.context-8`.
- [Community](nodes/context.community.json) **groups as its responsibility** [Community and Clans](nodes/capability.community-clans.json). Typed predicate: `owns`; relation: `body-war.relation.context-9`.
- [Suggested Track Discovery](nodes/capability.suggested-track-discovery.json) **needs** [Authentication and Consent](nodes/capability.auth-consent.json). Typed predicate: `depends_on`; relation: `body-war.relation.capability-dependency-9`.
- [Suggested Track Creation](nodes/capability.suggested-track-creation.json) **needs** [Authentication and Consent](nodes/capability.auth-consent.json). Typed predicate: `depends_on`; relation: `body-war.relation.capability-dependency-10`.
- [Evidence Candidate Attachment](nodes/capability.evidence-candidate-attach.json) **needs** [Suggested Track Discovery](nodes/capability.suggested-track-discovery.json). Typed predicate: `depends_on`; relation: `body-war.relation.capability-dependency-11`.
- [Evidence Candidate Attachment](nodes/capability.evidence-candidate-attach.json) **needs** [Activity Import](nodes/capability.activity-import.json). Typed predicate: `depends_on`; relation: `body-war.relation.capability-dependency-12`.
- [Selected Activity Geometry](nodes/capability.activity-geometry.json) **needs** [Evidence Candidate Attachment](nodes/capability.evidence-candidate-attach.json). Typed predicate: `depends_on`; relation: `body-war.relation.capability-dependency-13`.
- [Selected Activity Geometry](nodes/capability.activity-geometry.json) **needs** [Authentication and Consent](nodes/capability.auth-consent.json). Typed predicate: `depends_on`; relation: `body-war.relation.capability-dependency-14`.
- [Explained Score Preview](nodes/capability.score-preview.json) **needs** [Selected Activity Geometry](nodes/capability.activity-geometry.json). Typed predicate: `depends_on`; relation: `body-war.relation.capability-dependency-15`.
- [Explained Score Preview](nodes/capability.score-preview.json) **needs** [Score and XP](nodes/capability.score-xp.json). Typed predicate: `depends_on`; relation: `body-war.relation.capability-dependency-16`.

**Boundary:** This view does not prove that a capability is implemented, tested, deployed, or promoted.

## Runner intent: login to candidate evidence

**Question:** How does an anonymous visit become one exact track, activity, consent, and evidence binding?

**Represents:** The runner-intent half of the candidate journey. It shows authentication meaning, the connected-runner role, SuggestedTrack proposal, and explicit consented evidence.

![Runner intent: login to candidate evidence: typed relation sentences](generated/views/runner-intent-to-candidate-evidence.svg)

<details>
<summary>Open Mermaid network projection</summary>

```mermaid
flowchart LR
  N0["Anonymous Visitor<br/>actor · reviewed-candidate"]
  N1["Connected Runner<br/>actor · reviewed-candidate"]
  N2["Runner<br/>actor · reviewed-candidate"]
  N3["ActivityEvidenceCandidate<br/>entity · reviewed-candidate"]
  N4["RunnerConfirmation<br/>entity · candidate"]
  N5["SuggestedTrack<br/>entity · reviewed-candidate"]
  N6["Authenticate Via Strava<br/>operation · reviewed-candidate"]
  N7["Complete Strava OAuth<br/>operation · reviewed-candidate"]
  N8["Consent Contract<br/>policy · candidate"]
  N9["Auth Connected<br/>lifecycle_state · reviewed-candidate"]
  N10["Login To ScorePreview Workflow<br/>workflow · blocked"]
  N0 -->|"takes part in"| N10
  N10 -->|"includes"| N6
  N6 -->|"includes"| N7
  N7 -->|"changes the state of"| N9
  N2 -->|"becomes after authentication"| N1
  N1 -->|"proposes"| N5
  N1 -->|"records an explicit"| N4
  N4 -->|"must obey"| N8
  N4 -->|"creates candidate evidence"| N3
  classDef reviewed_candidate fill:#e8f5e9,stroke:#2e7d32,color:#16351b
  classDef candidate fill:#fff8e1,stroke:#f9a825,color:#4a3500
  classDef blocked fill:#ffebee,stroke:#c62828,color:#5a1010
  classDef deferred fill:#eceff1,stroke:#607d8b,color:#263238
  classDef projected fill:#e3f2fd,stroke:#1565c0,color:#0d315f
  class N0 reviewed_candidate
  class N1 reviewed_candidate
  class N2 reviewed_candidate
  class N3 reviewed_candidate
  class N4 candidate
  class N5 reviewed_candidate
  class N6 reviewed_candidate
  class N7 reviewed_candidate
  class N8 candidate
  class N9 reviewed_candidate
  class N10 blocked
```

</details>

### Read the arrows as sentences

- [Anonymous Visitor](nodes/actor.anonymous-visitor.json) **takes part in** [Login To ScorePreview Workflow](nodes/workflow.login-to-score-preview.json). Typed predicate: `participates_in`; relation: `body-war.relation.visitor-authenticates`.
- [Login To ScorePreview Workflow](nodes/workflow.login-to-score-preview.json) **includes** [Authenticate Via Strava](nodes/operation.authenticate-via-strava.json). Typed predicate: `contains`; relation: `body-war.relation.workflow-13`.
- [Authenticate Via Strava](nodes/operation.authenticate-via-strava.json) **includes** [Complete Strava OAuth](nodes/operation.complete-strava-oauth.json). Typed predicate: `contains`; relation: `body-war.relation.authenticate-contains-callback`.
- [Complete Strava OAuth](nodes/operation.complete-strava-oauth.json) **changes the state of** [Auth Connected](nodes/state.auth.connected.json). Typed predicate: `changes_state_of`; relation: `body-war.relation.operation-5`.
- [Runner](nodes/actor.runner.json) **becomes after authentication** [Connected Runner](nodes/actor.connected-runner.json). Typed predicate: `becomes`; relation: `body-war.relation.runner-becomes-connected`.
- [Connected Runner](nodes/actor.connected-runner.json) **proposes** [SuggestedTrack](nodes/entity.suggested-track.json). Typed predicate: `produces`; relation: `body-war.relation.connected-proposes-track`.
- [Connected Runner](nodes/actor.connected-runner.json) **records an explicit** [RunnerConfirmation](nodes/entity.runner-confirmation.json). Typed predicate: `produces`; relation: `body-war.relation.connected-confirms`.
- [RunnerConfirmation](nodes/entity.runner-confirmation.json) **must obey** [Consent Contract](nodes/policy.consent-contract.json). Typed predicate: `governed_by`; relation: `body-war.relation.confirmation-governed-consent`.
- [RunnerConfirmation](nodes/entity.runner-confirmation.json) **creates candidate evidence** [ActivityEvidenceCandidate](nodes/entity.activity-evidence-candidate.json). Typed predicate: `produces`; relation: `body-war.relation.confirmation-produces-candidate`.

**Boundary:** These arrows are typed business statements, not an operation sequence or proof that OAuth, ownership validation, consent UI, or persistence works.

## Candidate calculation: geometry to ScorePreview

**Question:** How does confirmed evidence support private geometry, canonical score input, and an explained preliminary score?

**Represents:** A relation-local geometry and calculation view. Operations point to declared inputs and candidate outputs; residue annotations expose unresolved owner routes.

![Candidate calculation: geometry to ScorePreview: typed relation sentences](generated/views/candidate-geometry-to-score-preview.svg)

<details>
<summary>Open Mermaid network projection</summary>

```mermaid
flowchart LR
  N0["ActivityEvidenceCandidate<br/>entity · reviewed-candidate"]
  N1["GeometryCandidate<br/>entity · blocked"]
  N2["RunnerConfirmation<br/>entity · candidate"]
  N3["Zone Score<br/>metric · blocked"]
  N4["Build ScoreInputSnapshot<br/>operation · blocked"]
  N5["Calculate ScorePreview<br/>operation · blocked"]
  N6["Derive GeometryCandidate<br/>operation · blocked"]
  N7["Fetch Selected Activity Geometry<br/>operation · blocked"]
  N8["Project ScorePreview<br/>operation · blocked"]
  N9["ScorePreview<br/>outcome · blocked"]
  N10["Source-Backed Track<br/>outcome · deferred"]
  N11["Geometry Privacy Policy<br/>policy · blocked"]
  N12["ScorePolicy<br/>policy · blocked"]
  N13["ActivityGeometrySample<br/>value_object · blocked"]
  N14["ScoreInputSnapshot<br/>value_object · blocked"]
  N0 -->|"supports as evidence"| N1
  N7 -. "uses" .-> N2
  N7 -. "supplies candidate input" .-> N13
  N6 -. "uses" .-> N13
  N6 -. "creates candidate geometry" .-> N1
  N6 -. "must obey" .-> N11
  N4 -. "uses" .-> N1
  N4 -. "must use the exact" .-> N12
  N4 -. "creates canonical input" .-> N14
  N5 -. "uses" .-> N14
  N5 -. "must obey" .-> N12
  N5 -. "creates a preliminary" .-> N9
  N8 -. "reads without changing" .-> N9
  N9 -. "shows a limited view of" .-> N3
  N1 -. "does not establish" .-> N10
  N9 -. "does not establish" .-> N10
  classDef reviewed_candidate fill:#e8f5e9,stroke:#2e7d32,color:#16351b
  classDef candidate fill:#fff8e1,stroke:#f9a825,color:#4a3500
  classDef blocked fill:#ffebee,stroke:#c62828,color:#5a1010
  classDef deferred fill:#eceff1,stroke:#607d8b,color:#263238
  classDef projected fill:#e3f2fd,stroke:#1565c0,color:#0d315f
  class N0 reviewed_candidate
  class N1 blocked
  class N2 candidate
  class N3 blocked
  class N4 blocked
  class N5 blocked
  class N6 blocked
  class N7 blocked
  class N8 blocked
  class N9 blocked
  class N10 deferred
  class N11 blocked
  class N12 blocked
  class N13 blocked
  class N14 blocked
```

</details>

### Read the arrows as sentences

- [ActivityEvidenceCandidate](nodes/entity.activity-evidence-candidate.json) **supports as evidence** [GeometryCandidate](nodes/entity.geometry-candidate.json). Typed predicate: `supports`; relation: `body-war.relation.candidate-supports-geometry`.
- [Fetch Selected Activity Geometry](nodes/operation.fetch-selected-activity-geometry.json) **uses** [RunnerConfirmation](nodes/entity.runner-confirmation.json). Typed predicate: `consumes`; relation: `body-war.relation.fetch-geometry-consumes-confirmation`.
- [Fetch Selected Activity Geometry](nodes/operation.fetch-selected-activity-geometry.json) **supplies candidate input** [ActivityGeometrySample](nodes/value.activity-geometry-sample.json). Typed predicate: `produces`; relation: `body-war.relation.fetch-geometry-produces-sample`.
- [Derive GeometryCandidate](nodes/operation.derive-geometry-candidate.json) **uses** [ActivityGeometrySample](nodes/value.activity-geometry-sample.json). Typed predicate: `consumes`; relation: `body-war.relation.derive-consumes-sample`.
- [Derive GeometryCandidate](nodes/operation.derive-geometry-candidate.json) **creates candidate geometry** [GeometryCandidate](nodes/entity.geometry-candidate.json). Typed predicate: `produces`; relation: `body-war.relation.derive-produces-geometry`.
- [Derive GeometryCandidate](nodes/operation.derive-geometry-candidate.json) **must obey** [Geometry Privacy Policy](nodes/policy.geometry-privacy.json). Typed predicate: `governed_by`; relation: `body-war.relation.geometry-governed-privacy`.
- [Build ScoreInputSnapshot](nodes/operation.build-score-input-snapshot.json) **uses** [GeometryCandidate](nodes/entity.geometry-candidate.json). Typed predicate: `consumes`; relation: `body-war.relation.snapshot-consumes-geometry`.
- [Build ScoreInputSnapshot](nodes/operation.build-score-input-snapshot.json) **must use the exact** [ScorePolicy](nodes/policy.score-policy.json). Typed predicate: `consumes`; relation: `body-war.relation.snapshot-consumes-policy`.
- [Build ScoreInputSnapshot](nodes/operation.build-score-input-snapshot.json) **creates canonical input** [ScoreInputSnapshot](nodes/value.score-input-snapshot.json). Typed predicate: `produces`; relation: `body-war.relation.snapshot-produces-snapshot`.
- [Calculate ScorePreview](nodes/operation.calculate-score-preview.json) **uses** [ScoreInputSnapshot](nodes/value.score-input-snapshot.json). Typed predicate: `consumes`; relation: `body-war.relation.calculate-preview-consumes-snapshot`.
- [Calculate ScorePreview](nodes/operation.calculate-score-preview.json) **must obey** [ScorePolicy](nodes/policy.score-policy.json). Typed predicate: `consumes`; relation: `body-war.relation.calculate-preview-consumes-policy`.
- [Calculate ScorePreview](nodes/operation.calculate-score-preview.json) **creates a preliminary** [ScorePreview](nodes/outcome.score-preview.json). Typed predicate: `produces`; relation: `body-war.relation.calculate-preview-produces-preview`.
- [Project ScorePreview](nodes/operation.project-score-preview.json) **reads without changing** [ScorePreview](nodes/outcome.score-preview.json). Typed predicate: `reads`; relation: `body-war.relation.project-preview-reads-preview`.
- [ScorePreview](nodes/outcome.score-preview.json) **shows a limited view of** [Zone Score](nodes/metric.zone-score.json). Typed predicate: `projects`; relation: `body-war.relation.score-preview-projects-zone-score`.
- [GeometryCandidate](nodes/entity.geometry-candidate.json) **does not establish** [Source-Backed Track](nodes/outcome.source-backed-track.json). Typed predicate: `does_not_promote`; relation: `body-war.relation.geometry-does-not-promote`.
- [ScorePreview](nodes/outcome.score-preview.json) **does not establish** [Source-Backed Track](nodes/outcome.source-backed-track.json). Typed predicate: `does_not_promote`; relation: `body-war.relation.preview-does-not-promote`.

**Boundary:** The graph is not a completed runtime sequence. Candidate geometry and ScorePreview remain non-promoting; displayed score and privacy residue remains unresolved.

## Activity evidence to controller projection

**Question:** Which relations connect one runner activity, preview evidence, and a controller read model?

**Represents:** A relation-local evidence-submission and preview-controller view. Operations point to declared inputs and the evidence, events, or projections they produce.

![Activity evidence to controller projection: typed relation sentences](generated/views/activity-evidence-to-controller.svg)

<details>
<summary>Open Mermaid network projection</summary>

```mermaid
flowchart LR
  N0["EvidenceSubmission<br/>entity · reviewed-candidate"]
  N1["ProviderAccount<br/>entity · reviewed-candidate"]
  N2["RunActivity<br/>entity · reviewed-candidate"]
  N3["TerritoryUnit<br/>entity · reviewed-candidate"]
  N4["ControllerUpdated<br/>event · reviewed-candidate"]
  N5["EvidencePreviewAccepted<br/>event · reviewed-candidate"]
  N6["EvidenceSubmitted<br/>event · reviewed-candidate"]
  N7["Auto-Accept Preview Evidence<br/>operation · reviewed-candidate"]
  N8["Compute Controller<br/>operation · reviewed-candidate"]
  N9["Import Activities<br/>operation · reviewed-candidate"]
  N10["Submit Evidence<br/>operation · reviewed-candidate"]
  N11["Controller Selection Policy<br/>policy · blocked"]
  N12["Preview Evidence Policy<br/>policy · reviewed-candidate"]
  N13["Control Basis<br/>value_object · reviewed-candidate"]
  N14["ControllerState<br/>value_object · reviewed-candidate"]
  N9 -->|"uses as input"| N1
  N9 -->|"creates or emits"| N2
  N10 -->|"uses as input"| N2
  N10 -->|"uses as input"| N3
  N10 -->|"creates or emits"| N0
  N10 -->|"creates or emits"| N6
  N7 -->|"uses as input"| N0
  N7 -->|"creates or emits"| N5
  N7 -->|"is constrained by"| N12
  N8 -->|"uses as input"| N0
  N8 -->|"creates or emits"| N14
  N8 -->|"creates or emits"| N4
  N8 -. "is constrained by" .-> N11
  N14 -->|"records"| N13
  N14 -->|"projects as a read model"| N3
  classDef reviewed_candidate fill:#e8f5e9,stroke:#2e7d32,color:#16351b
  classDef candidate fill:#fff8e1,stroke:#f9a825,color:#4a3500
  classDef blocked fill:#ffebee,stroke:#c62828,color:#5a1010
  classDef deferred fill:#eceff1,stroke:#607d8b,color:#263238
  classDef projected fill:#e3f2fd,stroke:#1565c0,color:#0d315f
  class N0 reviewed_candidate
  class N1 reviewed_candidate
  class N2 reviewed_candidate
  class N3 reviewed_candidate
  class N4 reviewed_candidate
  class N5 reviewed_candidate
  class N6 reviewed_candidate
  class N7 reviewed_candidate
  class N8 reviewed_candidate
  class N9 reviewed_candidate
  class N10 reviewed_candidate
  class N11 blocked
  class N12 reviewed_candidate
  class N13 reviewed_candidate
  class N14 reviewed_candidate
```

</details>

### Read the arrows as sentences

- [Import Activities](nodes/operation.import-activities.json) **uses as input** [ProviderAccount](nodes/entity.provider-account.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-7`.
- [Import Activities](nodes/operation.import-activities.json) **creates or emits** [RunActivity](nodes/entity.run-activity.json). Typed predicate: `produces`; relation: `body-war.relation.operation-8`.
- [Submit Evidence](nodes/operation.submit-evidence.json) **uses as input** [RunActivity](nodes/entity.run-activity.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-12`.
- [Submit Evidence](nodes/operation.submit-evidence.json) **uses as input** [TerritoryUnit](nodes/entity.territory-unit.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-13`.
- [Submit Evidence](nodes/operation.submit-evidence.json) **creates or emits** [EvidenceSubmission](nodes/entity.evidence-submission.json). Typed predicate: `produces`; relation: `body-war.relation.operation-14`.
- [Submit Evidence](nodes/operation.submit-evidence.json) **creates or emits** [EvidenceSubmitted](nodes/event.evidence-submitted.json). Typed predicate: `produces`; relation: `body-war.relation.operation-15`.
- [Auto-Accept Preview Evidence](nodes/operation.auto-accept-preview-evidence.json) **uses as input** [EvidenceSubmission](nodes/entity.evidence-submission.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-16`.
- [Auto-Accept Preview Evidence](nodes/operation.auto-accept-preview-evidence.json) **creates or emits** [EvidencePreviewAccepted](nodes/event.evidence-preview-accepted.json). Typed predicate: `produces`; relation: `body-war.relation.operation-17`.
- [Auto-Accept Preview Evidence](nodes/operation.auto-accept-preview-evidence.json) **is constrained by** [Preview Evidence Policy](nodes/policy.preview-evidence.json). Typed predicate: `governed_by`; relation: `body-war.relation.preview-policy-governs-autoaccept`.
- [Compute Controller](nodes/operation.compute-controller.json) **uses as input** [EvidenceSubmission](nodes/entity.evidence-submission.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-21`.
- [Compute Controller](nodes/operation.compute-controller.json) **creates or emits** [ControllerState](nodes/value.controller-state.json). Typed predicate: `produces`; relation: `body-war.relation.operation-22`.
- [Compute Controller](nodes/operation.compute-controller.json) **creates or emits** [ControllerUpdated](nodes/event.controller-updated.json). Typed predicate: `produces`; relation: `body-war.relation.operation-23`.
- [Compute Controller](nodes/operation.compute-controller.json) **is constrained by** [Controller Selection Policy](nodes/policy.controller-selection.json). Typed predicate: `governed_by`; relation: `body-war.relation.controller-governed-selection`.
- [ControllerState](nodes/value.controller-state.json) **records** [Control Basis](nodes/value.control-basis.json). Typed predicate: `records`; relation: `body-war.relation.controller-records-basis`.
- [ControllerState](nodes/value.controller-state.json) **projects as a read model** [TerritoryUnit](nodes/entity.territory-unit.json). Typed predicate: `projects`; relation: `body-war.relation.controller-projects-territory`.

**Boundary:** Preview-accepted evidence and preview-controlled state are not verified evidence or verified territory control.

## Territory competition loop

**Question:** What does controlling, invading, defending, and expiring territory mean?

**Represents:** The business loop around territory control. It separates actors, the invasion episode, owner eligibility, defense time, controller projection, and ownership evidence.

![Territory competition loop: typed relation sentences](generated/views/territory-competition-loop.svg)

<details>
<summary>Open Mermaid network projection</summary>

```mermaid
flowchart LR
  N0["Clan Member<br/>actor · reviewed-candidate"]
  N1["Invader<br/>actor · reviewed-candidate"]
  N2["Zone Owner<br/>actor · reviewed-candidate"]
  N3["Invasion<br/>entity · reviewed-candidate"]
  N4["Ownership Record<br/>entity · reviewed-candidate"]
  N5["TerritoryUnit<br/>entity · reviewed-candidate"]
  N6["DefenseSucceeded<br/>event · reviewed-candidate"]
  N7["InvasionOpened<br/>event · reviewed-candidate"]
  N8["Defend Territory<br/>operation · reviewed-candidate"]
  N9["Open Invasion<br/>operation · reviewed-candidate"]
  N10["Ownership Caducity Policy<br/>policy · blocked"]
  N11["Ownership Eligibility Policy<br/>policy · blocked"]
  N12["Controller Metric<br/>value_object · blocked"]
  N13["ControllerState<br/>value_object · reviewed-candidate"]
  N14["Defense Window<br/>value_object · reviewed-candidate"]
  N2 -->|"controls under the declared basis"| N5
  N1 -->|"contests"| N5
  N0 -->|"may defend"| N5
  N9 -->|"uses as input"| N4
  N9 -->|"creates or emits"| N3
  N9 -->|"creates or emits"| N7
  N3 -->|"contests"| N4
  N3 -->|"is constrained by"| N14
  N3 -. "is constrained by" .-> N11
  N8 -->|"uses as input"| N3
  N8 -->|"creates or emits"| N6
  N4 -. "is constrained by" .-> N10
  N13 -->|"is constrained by"| N12
  classDef reviewed_candidate fill:#e8f5e9,stroke:#2e7d32,color:#16351b
  classDef candidate fill:#fff8e1,stroke:#f9a825,color:#4a3500
  classDef blocked fill:#ffebee,stroke:#c62828,color:#5a1010
  classDef deferred fill:#eceff1,stroke:#607d8b,color:#263238
  classDef projected fill:#e3f2fd,stroke:#1565c0,color:#0d315f
  class N0 reviewed_candidate
  class N1 reviewed_candidate
  class N2 reviewed_candidate
  class N3 reviewed_candidate
  class N4 reviewed_candidate
  class N5 reviewed_candidate
  class N6 reviewed_candidate
  class N7 reviewed_candidate
  class N8 reviewed_candidate
  class N9 reviewed_candidate
  class N10 blocked
  class N11 blocked
  class N12 blocked
  class N13 reviewed_candidate
  class N14 reviewed_candidate
```

</details>

### Read the arrows as sentences

- [Zone Owner](nodes/actor.zone-owner.json) **controls under the declared basis** [TerritoryUnit](nodes/entity.territory-unit.json). Typed predicate: `controls`; relation: `body-war.relation.owner-controls-territory`.
- [Invader](nodes/actor.invader.json) **contests** [TerritoryUnit](nodes/entity.territory-unit.json). Typed predicate: `contests`; relation: `body-war.relation.invader-contests-territory`.
- [Clan Member](nodes/actor.clan-member.json) **may defend** [TerritoryUnit](nodes/entity.territory-unit.json). Typed predicate: `defends`; relation: `body-war.relation.clan-member-defends`.
- [Open Invasion](nodes/operation.open-invasion.json) **uses as input** [Ownership Record](nodes/entity.ownership-record.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-24`.
- [Open Invasion](nodes/operation.open-invasion.json) **creates or emits** [Invasion](nodes/entity.invasion.json). Typed predicate: `produces`; relation: `body-war.relation.operation-25`.
- [Open Invasion](nodes/operation.open-invasion.json) **creates or emits** [InvasionOpened](nodes/event.invasion-opened.json). Typed predicate: `produces`; relation: `body-war.relation.operation-26`.
- [Invasion](nodes/entity.invasion.json) **contests** [Ownership Record](nodes/entity.ownership-record.json). Typed predicate: `contests`; relation: `body-war.relation.invasion-contests-ownership`.
- [Invasion](nodes/entity.invasion.json) **is constrained by** [Defense Window](nodes/value.defense-window.json). Typed predicate: `governed_by`; relation: `body-war.relation.invasion-governed-defense-window`.
- [Invasion](nodes/entity.invasion.json) **is constrained by** [Ownership Eligibility Policy](nodes/policy.ownership-eligibility.json). Typed predicate: `governed_by`; relation: `body-war.relation.invasion-governed-eligibility`.
- [Defend Territory](nodes/operation.defend-territory.json) **uses as input** [Invasion](nodes/entity.invasion.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-27`.
- [Defend Territory](nodes/operation.defend-territory.json) **creates or emits** [DefenseSucceeded](nodes/event.defense-succeeded.json). Typed predicate: `produces`; relation: `body-war.relation.operation-28`.
- [Ownership Record](nodes/entity.ownership-record.json) **is constrained by** [Ownership Caducity Policy](nodes/policy.caducity.json). Typed predicate: `governed_by`; relation: `body-war.relation.ownership-governed-caducity`.
- [ControllerState](nodes/value.controller-state.json) **is constrained by** [Controller Metric](nodes/value.controller-metric.json). Typed predicate: `governed_by`; relation: `body-war.relation.controller-governed-metric`.

**Boundary:** The loop does not choose the controller metric, anti-cheat strictness, caducity interval, or clan eligibility policy.

## Community and progression loop

**Question:** How do challenges, clans, XP, seasons, and rankings relate?

**Represents:** The declared social and progression meanings: challenges can award profile XP, the ledger records XP, clans contain members, and seasons contain ranking projections.

![Community and progression loop: typed relation sentences](generated/views/community-progression-loop.svg)

<details>
<summary>Open Mermaid network projection</summary>

```mermaid
flowchart LR
  N0["Clan Member<br/>actor · reviewed-candidate"]
  N1["Challenge<br/>entity · reviewed-candidate"]
  N2["Clan<br/>entity · reviewed-candidate"]
  N3["Ranking Snapshot<br/>entity · reviewed-candidate"]
  N4["Season<br/>entity · reviewed-candidate"]
  N5["ChallengeCompleted<br/>event · reviewed-candidate"]
  N6["SeasonSnapshotClosed<br/>event · reviewed-candidate"]
  N7["XPAwarded<br/>event · reviewed-candidate"]
  N8["XP Ledger<br/>ledger · reviewed-candidate"]
  N9["Profile XP<br/>metric · reviewed-candidate"]
  N10["Seasonal Ranking<br/>metric · reviewed-candidate"]
  N11["Award XP<br/>operation · reviewed-candidate"]
  N12["Complete Challenge<br/>operation · reviewed-candidate"]
  N13["Create Clan<br/>operation · reviewed-candidate"]
  N14["Join Challenge<br/>operation · reviewed-candidate"]
  N15["Join Clan<br/>operation · reviewed-candidate"]
  N16["Snapshot Season<br/>operation · reviewed-candidate"]
  N17["Seasonal Progression Workflow<br/>workflow · reviewed-candidate"]
  N1 -->|"awards"| N9
  N8 -->|"records"| N9
  N2 -->|"contains as a step or responsibility"| N0
  N4 -->|"contains as a step or responsibility"| N10
  N17 -->|"contains as a step or responsibility"| N11
  N17 -->|"contains as a step or responsibility"| N16
  N11 -->|"creates or emits"| N7
  N11 -->|"records"| N8
  N14 -->|"uses as input"| N1
  N12 -->|"creates or emits"| N5
  N13 -->|"creates or emits"| N2
  N15 -->|"uses as input"| N2
  N16 -->|"creates or emits"| N3
  N16 -->|"creates or emits"| N6
  classDef reviewed_candidate fill:#e8f5e9,stroke:#2e7d32,color:#16351b
  classDef candidate fill:#fff8e1,stroke:#f9a825,color:#4a3500
  classDef blocked fill:#ffebee,stroke:#c62828,color:#5a1010
  classDef deferred fill:#eceff1,stroke:#607d8b,color:#263238
  classDef projected fill:#e3f2fd,stroke:#1565c0,color:#0d315f
  class N0 reviewed_candidate
  class N1 reviewed_candidate
  class N2 reviewed_candidate
  class N3 reviewed_candidate
  class N4 reviewed_candidate
  class N5 reviewed_candidate
  class N6 reviewed_candidate
  class N7 reviewed_candidate
  class N8 reviewed_candidate
  class N9 reviewed_candidate
  class N10 reviewed_candidate
  class N11 reviewed_candidate
  class N12 reviewed_candidate
  class N13 reviewed_candidate
  class N14 reviewed_candidate
  class N15 reviewed_candidate
  class N16 reviewed_candidate
  class N17 reviewed_candidate
```

</details>

### Read the arrows as sentences

- [Challenge](nodes/entity.challenge.json) **awards** [Profile XP](nodes/metric.profile-xp.json). Typed predicate: `awards`; relation: `body-war.relation.challenge-awards-xp`.
- [XP Ledger](nodes/ledger.xp-ledger.json) **records** [Profile XP](nodes/metric.profile-xp.json). Typed predicate: `records`; relation: `body-war.relation.xp-ledger-records-xp`.
- [Clan](nodes/entity.clan.json) **contains as a step or responsibility** [Clan Member](nodes/actor.clan-member.json). Typed predicate: `contains`; relation: `body-war.relation.clan-contains-member`.
- [Season](nodes/entity.season.json) **contains as a step or responsibility** [Seasonal Ranking](nodes/metric.seasonal-ranking.json). Typed predicate: `contains`; relation: `body-war.relation.season-contains-ranking`.
- [Seasonal Progression Workflow](nodes/workflow.seasonal-progression.json) **contains as a step or responsibility** [Award XP](nodes/operation.award-xp.json). Typed predicate: `contains`; relation: `body-war.relation.workflow-9`.
- [Seasonal Progression Workflow](nodes/workflow.seasonal-progression.json) **contains as a step or responsibility** [Snapshot Season](nodes/operation.snapshot-season.json). Typed predicate: `contains`; relation: `body-war.relation.workflow-10`.
- [Award XP](nodes/operation.award-xp.json) **creates or emits** [XPAwarded](nodes/event.xp-awarded.json). Typed predicate: `produces`; relation: `body-war.relation.operation-31`.
- [Award XP](nodes/operation.award-xp.json) **records** [XP Ledger](nodes/ledger.xp-ledger.json). Typed predicate: `records`; relation: `body-war.relation.operation-32`.
- [Join Challenge](nodes/operation.join-challenge.json) **uses as input** [Challenge](nodes/entity.challenge.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-33`.
- [Complete Challenge](nodes/operation.complete-challenge.json) **creates or emits** [ChallengeCompleted](nodes/event.challenge-completed.json). Typed predicate: `produces`; relation: `body-war.relation.operation-34`.
- [Create Clan](nodes/operation.create-clan.json) **creates or emits** [Clan](nodes/entity.clan.json). Typed predicate: `produces`; relation: `body-war.relation.operation-35`.
- [Join Clan](nodes/operation.join-clan.json) **uses as input** [Clan](nodes/entity.clan.json). Typed predicate: `consumes`; relation: `body-war.relation.operation-36`.
- [Snapshot Season](nodes/operation.snapshot-season.json) **creates or emits** [Ranking Snapshot](nodes/entity.ranking-snapshot.json). Typed predicate: `produces`; relation: `body-war.relation.operation-37`.
- [Snapshot Season](nodes/operation.snapshot-season.json) **creates or emits** [SeasonSnapshotClosed](nodes/event.season-snapshot-closed.json). Typed predicate: `produces`; relation: `body-war.relation.operation-38`.

**Boundary:** These relations do not prove retention, fairness, reward correctness, or implemented seasonal behavior; related premises remain hypotheses.

## Lifecycle views

Lifecycle status is independent from ontology `candidate_status`. These diagrams
show what a business object may transition through; they do not promote the node
record itself.

### SuggestedTrack

Owner route: `body-war.route-expansion-owner` · Authority effect: `none`

```mermaid
stateDiagram-v2
  state "SuggestedTrack Needs Evidence" as S0
  state "SuggestedTrack Evidence Submitted" as S1
  state "SuggestedTrack Operator Review" as S2
  state "SuggestedTrack Source-Backed" as S3
  state "SuggestedTrack Retired" as S4
  [*] --> S0: Seed or connected runner creates a suggestion. [available]
  S0 --> S1: Runner confirms and attaches a redacted activity evidence candidate. [available]
  S1 --> S2: Operator starts candidate review. [out-of-scope]
  S2 --> S3: Operator accepts source or geometry evidence under a future promotion policy. [out-of-scope]
  state "Any active state" as ACTIVE
  ACTIVE --> S4: Operator retires the suggestion. [out-of-scope]
```

Transition phrases:

- `none -> needs-evidence`: Seed or connected runner creates a suggestion. Availability: `available`.
- `needs-evidence -> evidence-submitted`: Runner confirms and attaches a redacted activity evidence candidate. Availability: `available`.
- `evidence-submitted -> operator-review`: Operator starts candidate review. Availability: `out-of-scope`.
- `operator-review -> source-backed`: Operator accepts source or geometry evidence under a future promotion policy. Availability: `out-of-scope`.
- `any-active-state -> retired`: Operator retires the suggestion. Availability: `out-of-scope`.

Boundary: Runner confirmation, candidate evidence, GeometryCandidate, or ScorePreview cannot skip operator-review and create source-backed state.

### GeometryCandidate

Owner route: `body-war.data-privacy-owner` · Authority effect: `none`

```mermaid
stateDiagram-v2
  state "Geometry Candidate Absent" as S0
  state "Geometry Fetch Pending" as S1
  state "Geometry Derived Candidate" as S2
  state "Geometry Unavailable" as S3
  state "Geometry Candidate Rejected" as S4
  state "Geometry Candidate Superseded" as S5
  S0 --> S1: Validated runner confirmation authorizes selected-activity geometry use. [fixture-only]
  S1 --> S2: Aligned streams pass validation and the ratified privacy filter. [fixture-only]
  S1 --> S3: Ownership, scope, provider, stream, or validation failure. [fixture-only]
  S2 --> S4: Candidate fails later validation or review. [out-of-scope]
  S2 --> S5: A newer candidate replaces it while retaining provenance. [blocked]
```

Transition phrases:

- `absent -> fetch-pending`: Validated runner confirmation authorizes selected-activity geometry use. Availability: `fixture-only`.
- `fetch-pending -> derived-candidate`: Aligned streams pass validation and the ratified privacy filter. Availability: `fixture-only`.
- `fetch-pending -> unavailable`: Ownership, scope, provider, stream, or validation failure. Availability: `fixture-only`.
- `derived-candidate -> rejected`: Candidate fails later validation or review. Availability: `out-of-scope`.
- `derived-candidate -> superseded`: A newer candidate replaces it while retaining provenance. Availability: `blocked`.

Boundary: derived-candidate is principal-private candidate evidence, not source-backed or public geometry.

### ScorePreview

Owner route: `body-war.score-policy-owner` · Authority effect: `none`

```mermaid
stateDiagram-v2
  state "Score Preview Unavailable" as S0
  state "Score Snapshot Pending" as S1
  state "Score Calculation Pending" as S2
  state "Score Preview Available" as S3
  state "Score Incomplete Projection" as S4
  state "Score Blocked By Policy" as S5
  state "Score Blocked By Geometry" as S6
  state "Score Calculation Failed" as S7
  state "Score Preview Superseded" as S8
  S0 --> S1: Admissible GeometryCandidate and exact policy become available. [fixture-only]
  S1 --> S2: Canonical complete-window snapshot is persisted. [fixture-only]
  S1 --> S4: Snapshot records single_activity_projection. [fixture-only]
  S1 --> S5: Policy is absent, incomplete, or stale. [available]
  S1 --> S6: No admissible GeometryCandidate is available. [available]
  S2 --> S3: Deterministic calculation succeeds under exact policy and snapshot. [fixture-only]
  S2 --> S7: Calculation invariant fails. [fixture-only]
  S3 --> S8: A newer policy, geometry, or snapshot result replaces it. [blocked]
```

Transition phrases:

- `unavailable -> snapshot-pending`: Admissible GeometryCandidate and exact policy become available. Availability: `fixture-only`.
- `snapshot-pending -> calculation-pending`: Canonical complete-window snapshot is persisted. Availability: `fixture-only`.
- `snapshot-pending -> incomplete-projection`: Snapshot records single_activity_projection. Availability: `fixture-only`.
- `snapshot-pending -> blocked-policy`: Policy is absent, incomplete, or stale. Availability: `available`.
- `snapshot-pending -> blocked-geometry`: No admissible GeometryCandidate is available. Availability: `available`.
- `calculation-pending -> available`: Deterministic calculation succeeds under exact policy and snapshot. Availability: `fixture-only`.
- `calculation-pending -> failed`: Calculation invariant fails. Availability: `fixture-only`.
- `available -> superseded`: A newer policy, geometry, or snapshot result replaces it. Availability: `blocked`.

Boundary: available means preview_only; it does not establish Zone Score, controller, conquest, source-backed route, or production authority.

### EvidenceSubmission

Owner route: `body-war.activity-evidence-owner` · Authority effect: `none`

```mermaid
stateDiagram-v2
  state "Submission Draft" as S0
  state "Submission Submitted" as S1
  state "Submission Preview-Accepted" as S2
  state "Submission Verified" as S3
  state "Submission Rejected" as S4
  S0 --> S1: Backend receives authenticated runner-owned evidence. [available]
  S1 --> S2: Preview evidence policy accepts the submission for preview display. [available]
  S1 --> S3: Operator or validation owner records accepted verification evidence. [out-of-scope]
  S1 --> S4: Operator or validation policy records rejection and reason. [out-of-scope]
  S2 --> S3: Later owner review accepts verification evidence. [out-of-scope]
  S2 --> S4: Later owner review rejects the evidence. [out-of-scope]
```

Transition phrases:

- `draft -> submitted`: Backend receives authenticated runner-owned evidence. Availability: `available`.
- `submitted -> preview-accepted`: Preview evidence policy accepts the submission for preview display. Availability: `available`.
- `submitted -> verified`: Operator or validation owner records accepted verification evidence. Availability: `out-of-scope`.
- `submitted -> rejected`: Operator or validation policy records rejection and reason. Availability: `out-of-scope`.
- `preview-accepted -> verified`: Later owner review accepts verification evidence. Availability: `out-of-scope`.
- `preview-accepted -> rejected`: Later owner review rejects the evidence. Availability: `out-of-scope`.

Boundary: preview-accepted must never be displayed or interpreted as verified.

### ControllerState

Owner route: `body-war.control-competition-owner` · Authority effect: `none`

```mermaid
stateDiagram-v2
  state "Controller Neutral" as S0
  state "Controller Preview-Controlled" as S1
  state "Controller Verified-Controlled" as S2
  state "Controller Contested" as S3
  state "Controller Expired" as S4
  S0 --> S1: Controller computation selects preview-accepted evidence under preview policy. [available]
  S0 --> S2: Controller computation selects verified evidence under adopted metric policy. [out-of-scope]
  S2 --> S3: Eligible invasion opens. [out-of-scope]
  S3 --> S2: Defense succeeds under adopted policy. [out-of-scope]
  S2 --> S4: Caducity policy expires ownership. [blocked]
```

Transition phrases:

- `neutral -> preview-controlled`: Controller computation selects preview-accepted evidence under preview policy. Availability: `available`.
- `neutral -> verified-controlled`: Controller computation selects verified evidence under adopted metric policy. Availability: `out-of-scope`.
- `verified-controlled -> contested`: Eligible invasion opens. Availability: `out-of-scope`.
- `contested -> verified-controlled`: Defense succeeds under adopted policy. Availability: `out-of-scope`.
- `verified-controlled -> expired`: Caducity policy expires ownership. Availability: `blocked`.

Boundary: A controller projection must retain basis and metric and must not convert preview evidence into verified control.

## Arrow phrase glossary

These phrases translate the project-local predicates into ordinary sentences.
They explain graph edges; they do not redefine the relation schema.

| Predicate | Read the arrow as | Example relation |
| --- | --- | --- |
| `awards` | awards | `body-war.relation.challenge-awards-xp` |
| `becomes` | becomes after the required transition | `body-war.relation.runner-becomes-connected` |
| `changes_state_of` | changes the state of | `body-war.relation.operation-5` |
| `consumes` | uses as input | `body-war.relation.attach-candidate-consumes-track` |
| `contains` | contains as a step or responsibility | `body-war.relation.authenticate-contains-callback` |
| `contests` | contests | `body-war.relation.invader-contests-territory` |
| `controls` | controls under the declared basis | `body-war.relation.owner-controls-territory` |
| `defends` | may defend | `body-war.relation.clan-member-defends` |
| `depends_on` | depends on | `body-war.relation.capability-dependency-1` |
| `does_not_promote` | does not promote | `body-war.relation.geometry-does-not-promote` |
| `exposes` | exposes | `body-war.relation.http-exposes-auth-query` |
| `governed_by` | is constrained by | `body-war.relation.confirm-operation-governed-consent` |
| `maps_to` | maps to | `body-war.relation.activity-maps-redacted` |
| `owns` | owns this business responsibility | `body-war.relation.context-1` |
| `participates_in` | participates in | `body-war.relation.operator-reviews-evidence` |
| `produces` | creates or emits | `body-war.relation.attach-candidate-produces-candidate` |
| `projects` | projects as a read model | `body-war.relation.controller-projects-territory` |
| `provides` | provides source data for | `body-war.relation.strava-provides-activity` |
| `reads` | reads without changing | `body-war.relation.detail-suggested-reads-candidate` |
| `records` | records | `body-war.relation.controller-records-basis` |
| `supports` | supports without promoting | `body-war.relation.candidate-supports-geometry` |
| `transitions_to` | may transition to | `body-war.relation.auth-anonymous-connected` |
| `validates` | reviews or validates | `body-war.relation.reviewer-validates-submission` |

## Authority and next-view boundary

```mermaid
flowchart LR
  SRC["Source documents + selectors"] --> CAND["Candidate business nodes + relations"]
  CAND --> REVIEW["Body War product ontology review"]
  REVIEW --> DECIDE{"Owner decision required?"}
  DECIDE -->|no| READY["Reviewed candidate meaning"]
  DECIDE -->|yes| BLOCKED["Blocked or deferred residue"]
  READY -. "later exact digest bridge" .-> DS["DomainSpec mapping<br/>not part of this package"]
  BLOCKED --> GATE["Decision gate / named owner route"]
  GATE -. "only after explicit decision" .-> READY
  GEO["GeometryCandidate"] -. "does not promote" .-> SOURCEBACKED["Source-backed track"]
  SCORE["ScorePreview"] -. "does not promote" .-> SOURCEBACKED
```

Next view work should be a separate system-branch inventory of the Body War app,
followed by a two-sided bridge validation. That future work must not be generated
from business intent alone.
