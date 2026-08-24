export const comprehensionTask = {
  schema_version: "body-war-business-comprehension-task/v1",
  task_id: "body-war.business-view-reading.v1",
  title: "Read the Body War business journey",
  audience: "first-time Body War business-ontology reader",
  stimulus: {
    label: "Body War journey ontology experiment",
    path: "BUSINESS-JOURNEY-EXPERIMENT.html",
    story_ids: [
      "login-to-score-preview",
      "activity-to-territory-preview",
    ],
  },
  prompt:
    "Use only the labeled relation arrows and visible boundary notes in the journey. Do not infer an operation order or a connection between sibling branches unless an arrow states it.",
  response_note:
    "Short plain-language answers are enough. You may quote visible relation IDs when useful.",
  loci: [
    {
      locus_id: "locate",
      label: "Locate",
      prompt:
        "Find the arrow where Confirm Suggested Track with Activity uses one RunActivity. Record the visible relation ID.",
    },
    {
      locus_id: "trace",
      label: "Trace",
      prompt:
        "Using only displayed arrows, list the relations that connect an Activity Evidence Candidate to a GeometryCandidate.",
    },
    {
      locus_id: "retell",
      label: "Retell",
      prompt:
        "Retell the Import Activities and ProviderAccount arrow as one plain-language sentence.",
    },
    {
      locus_id: "distinguish",
      label: "Distinguish",
      prompt:
        "Explain how sibling branch A differs from sibling branch B, and say whether either branch feeds the other in this view.",
    },
    {
      locus_id: "boundary",
      label: "Boundary",
      prompt:
        "Name one explicit non-promotion relation and one blocked owner decision, including the visible owner and next gate.",
    },
    {
      locus_id: "vocabulary",
      label: "Vocabulary",
      prompt:
        "In this view, what is the difference between a candidate meaning, a projection, and an explicit non-promotion boundary?",
    },
  ],
  submission:
    "Keep the six answers together with the exact task and stimulus digests supplied by the reviewer.",
  evidence_ceiling:
    "This task can reveal reading behavior. It cannot prove comprehension, ontology authority, runtime behavior, release, or production readiness.",
};

