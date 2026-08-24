export const predicatePhrases = {
  awards: "awards",
  becomes: "becomes after the required transition",
  changes_state_of: "changes the state of",
  consumes: "uses as input",
  contains: "contains as a step or responsibility",
  contests: "contests",
  controls: "controls under the declared basis",
  defends: "may defend",
  depends_on: "depends on",
  does_not_promote: "does not promote",
  exposes: "exposes",
  governed_by: "is constrained by",
  maps_to: "maps to",
  owns: "owns this business responsibility",
  participates_in: "participates in",
  produces: "creates or emits",
  projects: "projects as a read model",
  provides: "provides source data for",
  reads: "reads without changing",
  records: "records",
  supports: "supports without promoting",
  transitions_to: "may transition to",
  validates: "reviews or validates",
};

export const relationPhraseOverrides = Object.fromEntries([
  ...[
    1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18,
  ].map((id) => [
    `body-war.relation.context-${id}`,
    "groups as its responsibility",
  ]),
  ...Array.from({ length: 8 }, (_, index) => index + 9).map((id) => [
    `body-war.relation.capability-dependency-${id}`,
    "needs",
  ]),
  ["body-war.relation.visitor-authenticates", "takes part in"],
  ["body-war.relation.workflow-13", "includes"],
  ["body-war.relation.authenticate-contains-callback", "includes"],
  ["body-war.relation.runner-becomes-connected", "becomes after authentication"],
  ["body-war.relation.connected-proposes-track", "proposes"],
  ["body-war.relation.connected-confirms", "records an explicit"],
  ["body-war.relation.confirmation-governed-consent", "must obey"],
  ["body-war.relation.confirmation-produces-candidate", "creates candidate evidence"],
  ["body-war.relation.candidate-supports-geometry", "supports as evidence"],
  ["body-war.relation.fetch-geometry-consumes-confirmation", "uses"],
  ["body-war.relation.fetch-geometry-produces-sample", "supplies candidate input"],
  ["body-war.relation.derive-consumes-sample", "uses"],
  ["body-war.relation.derive-produces-geometry", "creates candidate geometry"],
  ["body-war.relation.geometry-governed-privacy", "must obey"],
  ["body-war.relation.snapshot-consumes-geometry", "uses"],
  ["body-war.relation.snapshot-consumes-policy", "must use the exact"],
  ["body-war.relation.snapshot-produces-snapshot", "creates canonical input"],
  ["body-war.relation.calculate-preview-consumes-snapshot", "uses"],
  ["body-war.relation.calculate-preview-consumes-policy", "must obey"],
  ["body-war.relation.calculate-preview-produces-preview", "creates a preliminary"],
  ["body-war.relation.project-preview-reads-preview", "reads without changing"],
  ["body-war.relation.geometry-does-not-promote", "does not establish"],
  ["body-war.relation.preview-does-not-promote", "does not establish"],
  ["body-war.relation.score-preview-projects-zone-score", "shows a limited view of"],
]);

export const featuredRelationExamples = [
  {
    example_id: "import-activities",
    title: "Import Activities relation sentences",
    question:
      "What does the Import Activities operation use, and what does it create?",
    represents:
      "A compact reading aid for two typed relations already present in the business ontology.",
    forbidden_claim:
      "This projection does not prove that provider authorization, activity import, persistence, or live Strava data works.",
    relation_ids: [
      "body-war.relation.operation-7",
      "body-war.relation.operation-8",
    ],
  },
];

export const journeyStories = [
  {
    story_id: "login-to-score-preview",
    eyebrow: "Prototype meaning path",
    title: "From login to a score preview",
    question:
      "What business meaning connects a visitor, a suggested track, consented evidence, candidate geometry, and a preliminary score?",
    summary:
      "Follow the candidate journey in five review chapters. Each arrow is backed by an existing typed relation.",
    forbidden_claim:
      "Chapter order is an explanatory review path. It does not prove UI order, live Strava activity retrieval, persistence, numeric score correctness, or runtime completion.",
    chapters: [
      {
        chapter_id: "connect",
        short_label: "Connect",
        title: "Connect a runner",
        summary:
          "These relations show authentication participation, workflow membership, callback containment, provider connection, and the connected-runner state transition.",
        relation_ids: [
          "body-war.relation.visitor-authenticates",
          "body-war.relation.workflow-13",
          "body-war.relation.authenticate-contains-callback",
          "body-war.relation.operation-5",
          "body-war.relation.runner-becomes-connected",
        ],
      },
      {
        chapter_id: "choose-confirm",
        short_label: "Choose",
        title: "Choose and confirm one SuggestedTrack",
        summary:
          "These relations associate a connected runner with track proposal, selection, one activity binding, explicit confirmation, and consent governance.",
        relation_ids: [
          "body-war.relation.connected-proposes-track",
          "body-war.relation.workflow-14",
          "body-war.relation.select-reads-track",
          "body-war.relation.workflow-15",
          "body-war.relation.confirm-consumes-track",
          "body-war.relation.confirm-consumes-activity",
          "body-war.relation.confirm-operation-governed-consent",
          "body-war.relation.confirm-produces-confirmation",
          "body-war.relation.connected-confirms",
          "body-war.relation.confirmation-governed-consent",
          "body-war.relation.confirmation-produces-candidate",
        ],
      },
      {
        chapter_id: "geometry",
        short_label: "Geometry",
        title: "Form private candidate geometry",
        summary:
          "Displayed relations connect confirmed candidate evidence, geometry sampling, geometry derivation, and the required privacy-policy constraint.",
        relation_ids: [
          "body-war.relation.candidate-supports-geometry",
          "body-war.relation.fetch-geometry-consumes-confirmation",
          "body-war.relation.fetch-geometry-produces-sample",
          "body-war.relation.derive-consumes-sample",
          "body-war.relation.derive-produces-geometry",
          "body-war.relation.geometry-governed-privacy",
        ],
      },
      {
        chapter_id: "score-preview",
        short_label: "Preview",
        title: "Build and explain a ScorePreview",
        summary:
          "Displayed relations connect candidate geometry, a score input snapshot, the score policy, a preliminary ScorePreview, and its limited Zone Score projection.",
        relation_ids: [
          "body-war.relation.snapshot-consumes-geometry",
          "body-war.relation.snapshot-consumes-policy",
          "body-war.relation.snapshot-produces-snapshot",
          "body-war.relation.calculate-preview-consumes-snapshot",
          "body-war.relation.calculate-preview-consumes-policy",
          "body-war.relation.calculate-preview-produces-preview",
          "body-war.relation.project-preview-reads-preview",
          "body-war.relation.score-preview-projects-zone-score",
        ],
      },
      {
        chapter_id: "limits",
        short_label: "Limits",
        title: "Keep the claim boundary visible",
        summary:
          "Candidate geometry and a score preview remain useful without becoming source-backed track authority.",
        relation_ids: [
          "body-war.relation.geometry-does-not-promote",
          "body-war.relation.preview-does-not-promote",
        ],
      },
    ],
  },
  {
    story_id: "activity-to-territory-preview",
    eyebrow: "Evidence meaning path",
    title: "From an imported activity to a territory preview",
    question:
      "Which typed relations place provider activity data, submitted evidence, preview acceptance, and a controller projection in this view?",
    summary:
      "See where ProviderAccount, RunActivity, evidence submission, preview acceptance, and controller projection meet.",
    reading_note:
      "EvidenceSubmission is a shared endpoint for sibling meaning branches A and B. Neither branch feeds the other in this view.",
    forbidden_claim:
      "This path does not prove live provider import, verified evidence, verified controller selection, or territory ownership.",
    chapters: [
      {
        chapter_id: "import",
        short_label: "Import",
        title: "Import activity summaries",
        summary:
          "The import operation uses a ProviderAccount and creates or emits RunActivity records.",
        relation_ids: [
          "body-war.relation.operation-7",
          "body-war.relation.operation-8",
        ],
      },
      {
        chapter_id: "submit",
        short_label: "Submit",
        title: "Submit activity evidence",
        summary:
          "Displayed relations show Submit Evidence using a run and a territory, and producing an EvidenceSubmission plus an Evidence Submitted event.",
        relation_ids: [
          "body-war.relation.operation-12",
          "body-war.relation.operation-13",
          "body-war.relation.operation-14",
          "body-war.relation.operation-15",
        ],
      },
      {
        chapter_id: "preview-evidence",
        short_label: "Review",
        review_label: "Sibling branch A",
        marker: "A",
        title: "Apply the preview evidence policy",
        summary:
          "Preview acceptance consumes the submission, emits a candidate event, and remains constrained by policy.",
        relation_ids: [
          "body-war.relation.operation-16",
          "body-war.relation.operation-17",
          "body-war.relation.preview-policy-governs-autoaccept",
        ],
      },
      {
        chapter_id: "controller-preview",
        short_label: "Project",
        review_label: "Sibling branch B",
        marker: "B",
        title: "Project a candidate controller",
        summary:
          "The controller computation consumes evidence and creates a state, event, basis, and territory projection.",
        relation_ids: [
          "body-war.relation.operation-21",
          "body-war.relation.operation-22",
          "body-war.relation.operation-23",
          "body-war.relation.controller-governed-selection",
          "body-war.relation.controller-records-basis",
          "body-war.relation.controller-projects-territory",
        ],
      },
    ],
  },
];

export const graphViews = [
  {
    view_id: "business-capability-map",
    title: "Business capability branches",
    question: "Which business contexts own which capabilities, and what must exist before the prototype score path can work?",
    represents:
      "A business-responsibility map. Contexts own capabilities; dependency arrows state prerequisite meaning, not module imports or runtime calls.",
    forbidden_claim:
      "This view does not prove that a capability is implemented, tested, deployed, or promoted.",
    relation_ids: [
      "body-war.relation.context-1",
      "body-war.relation.context-2",
      "body-war.relation.context-3",
      "body-war.relation.context-14",
      "body-war.relation.context-15",
      "body-war.relation.context-16",
      "body-war.relation.context-17",
      "body-war.relation.context-18",
      "body-war.relation.context-4",
      "body-war.relation.context-5",
      "body-war.relation.context-6",
      "body-war.relation.context-7",
      "body-war.relation.context-8",
      "body-war.relation.context-9",
      "body-war.relation.capability-dependency-9",
      "body-war.relation.capability-dependency-10",
      "body-war.relation.capability-dependency-11",
      "body-war.relation.capability-dependency-12",
      "body-war.relation.capability-dependency-13",
      "body-war.relation.capability-dependency-14",
      "body-war.relation.capability-dependency-15",
      "body-war.relation.capability-dependency-16"
    ]
  },
  {
    view_id: "runner-intent-to-candidate-evidence",
    title: "Runner intent: login to candidate evidence",
    question: "How does an anonymous visit become one exact track, activity, consent, and evidence binding?",
    represents:
      "The runner-intent half of the candidate journey. It shows authentication meaning, the connected-runner role, SuggestedTrack proposal, and explicit consented evidence.",
    forbidden_claim:
      "These arrows are typed business statements, not an operation sequence or proof that OAuth, ownership validation, consent UI, or persistence works.",
    relation_ids: [
      "body-war.relation.visitor-authenticates",
      "body-war.relation.workflow-13",
      "body-war.relation.authenticate-contains-callback",
      "body-war.relation.operation-5",
      "body-war.relation.runner-becomes-connected",
      "body-war.relation.connected-proposes-track",
      "body-war.relation.connected-confirms",
      "body-war.relation.confirmation-governed-consent",
      "body-war.relation.confirmation-produces-candidate"
    ]
  },
  {
    view_id: "candidate-geometry-to-score-preview",
    title: "Candidate calculation: geometry to ScorePreview",
    question: "How does confirmed evidence support private geometry, canonical score input, and an explained preliminary score?",
    represents:
      "A relation-local geometry and calculation view. Operations point to declared inputs and candidate outputs; residue annotations expose unresolved owner routes.",
    forbidden_claim:
      "The graph is not a completed runtime sequence. Candidate geometry and ScorePreview remain non-promoting; displayed score and privacy residue remains unresolved.",
    relation_ids: [
      "body-war.relation.candidate-supports-geometry",
      "body-war.relation.fetch-geometry-consumes-confirmation",
      "body-war.relation.fetch-geometry-produces-sample",
      "body-war.relation.derive-consumes-sample",
      "body-war.relation.derive-produces-geometry",
      "body-war.relation.geometry-governed-privacy",
      "body-war.relation.snapshot-consumes-geometry",
      "body-war.relation.snapshot-consumes-policy",
      "body-war.relation.snapshot-produces-snapshot",
      "body-war.relation.calculate-preview-consumes-snapshot",
      "body-war.relation.calculate-preview-consumes-policy",
      "body-war.relation.calculate-preview-produces-preview",
      "body-war.relation.project-preview-reads-preview",
      "body-war.relation.score-preview-projects-zone-score",
      "body-war.relation.geometry-does-not-promote",
      "body-war.relation.preview-does-not-promote"
    ]
  },
  {
    view_id: "activity-evidence-to-controller",
    title: "Activity evidence to controller projection",
    question: "Which relations connect one runner activity, preview evidence, and a controller read model?",
    represents:
      "A relation-local evidence-submission and preview-controller view. Operations point to declared inputs and the evidence, events, or projections they produce.",
    forbidden_claim:
      "Preview-accepted evidence and preview-controlled state are not verified evidence or verified territory control.",
    relation_ids: [
      "body-war.relation.operation-7",
      "body-war.relation.operation-8",
      "body-war.relation.operation-12",
      "body-war.relation.operation-13",
      "body-war.relation.operation-14",
      "body-war.relation.operation-15",
      "body-war.relation.operation-16",
      "body-war.relation.operation-17",
      "body-war.relation.preview-policy-governs-autoaccept",
      "body-war.relation.operation-21",
      "body-war.relation.operation-22",
      "body-war.relation.operation-23",
      "body-war.relation.controller-governed-selection",
      "body-war.relation.controller-records-basis",
      "body-war.relation.controller-projects-territory"
    ]
  },
  {
    view_id: "territory-competition-loop",
    title: "Territory competition loop",
    question: "What does controlling, invading, defending, and expiring territory mean?",
    represents:
      "The business loop around territory control. It separates actors, the invasion episode, owner eligibility, defense time, controller projection, and ownership evidence.",
    forbidden_claim:
      "The loop does not choose the controller metric, anti-cheat strictness, caducity interval, or clan eligibility policy.",
    relation_ids: [
      "body-war.relation.owner-controls-territory",
      "body-war.relation.invader-contests-territory",
      "body-war.relation.clan-member-defends",
      "body-war.relation.operation-24",
      "body-war.relation.operation-25",
      "body-war.relation.operation-26",
      "body-war.relation.invasion-contests-ownership",
      "body-war.relation.invasion-governed-defense-window",
      "body-war.relation.invasion-governed-eligibility",
      "body-war.relation.operation-27",
      "body-war.relation.operation-28",
      "body-war.relation.ownership-governed-caducity",
      "body-war.relation.controller-governed-metric"
    ]
  },
  {
    view_id: "community-progression-loop",
    title: "Community and progression loop",
    question: "How do challenges, clans, XP, seasons, and rankings relate?",
    represents:
      "The declared social and progression meanings: challenges can award profile XP, the ledger records XP, clans contain members, and seasons contain ranking projections.",
    forbidden_claim:
      "These relations do not prove retention, fairness, reward correctness, or implemented seasonal behavior; related premises remain hypotheses.",
    relation_ids: [
      "body-war.relation.challenge-awards-xp",
      "body-war.relation.xp-ledger-records-xp",
      "body-war.relation.clan-contains-member",
      "body-war.relation.season-contains-ranking",
      "body-war.relation.workflow-9",
      "body-war.relation.workflow-10",
      "body-war.relation.operation-31",
      "body-war.relation.operation-32",
      "body-war.relation.operation-33",
      "body-war.relation.operation-34",
      "body-war.relation.operation-35",
      "body-war.relation.operation-36",
      "body-war.relation.operation-37",
      "body-war.relation.operation-38"
    ]
  }
];

export const lifecycleViewPolicyIds = [
  "body-war.lifecycle.suggested-track",
  "body-war.lifecycle.geometry-candidate",
  "body-war.lifecycle.score-preview",
  "body-war.lifecycle.submission",
  "body-war.lifecycle.controller"
];
