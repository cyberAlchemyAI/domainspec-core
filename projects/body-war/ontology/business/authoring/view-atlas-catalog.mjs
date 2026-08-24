export const viewAtlasLenses = [
  {
    lens_id: "participants-boundaries",
    title: "Participants and boundaries",
    question:
      "Who participates, and through which external or interface boundary?",
    description:
      "Actors, external systems, and interfaces grouped for navigation only.",
    business_kinds: ["actor", "external_system", "interface"],
  },
  {
    lens_id: "responsibilities",
    title: "Responsibilities",
    question: "Which contexts group which capabilities?",
    description:
      "Responsibility vocabulary; this lens does not declare runtime modules.",
    business_kinds: ["bounded_context", "capability"],
  },
  {
    lens_id: "behavior",
    title: "Behavior",
    question:
      "What can happen, be requested, be answered, or be observed?",
    description:
      "Workflow, operation, query, and event kinds remain literal source kinds.",
    business_kinds: ["workflow", "operation", "query", "event"],
  },
  {
    lens_id: "business-objects",
    title: "Business objects",
    question: "What information, records, values, and measures are carried?",
    description:
      "Entity, value, ledger, and metric vocabulary without changed ownership.",
    business_kinds: ["entity", "value_object", "ledger", "metric"],
  },
  {
    lens_id: "governance-lifecycle",
    title: "Governance and lifecycle",
    question: "What constrains behavior and names lifecycle postures?",
    description:
      "Policy and lifecycle membership remain distinct from relation incidence.",
    business_kinds: ["policy", "lifecycle_state"],
  },
  {
    lens_id: "hypotheses-outcomes",
    title: "Hypotheses and outcomes",
    question: "What is believed or sought?",
    description:
      "Premise source defects remain explicit and unresolved in this lens.",
    business_kinds: ["premise", "outcome"],
  },
];

const policyMembers = [
  "body-war.business.state.activity.empty",
  "body-war.business.state.activity.loading",
  "body-war.business.state.activity.not-loaded",
  "body-war.business.state.activity.provider-error",
  "body-war.business.state.activity.ready",
  "body-war.business.state.auth.error",
  "body-war.business.state.auth.unconfigured",
  "body-war.business.state.challenge.expired",
  "body-war.business.state.controller.expired",
  "body-war.business.state.evidence-candidate.accepted",
  "body-war.business.state.evidence-candidate.operator-review",
  "body-war.business.state.evidence-candidate.rejected",
  "body-war.business.state.evidence-candidate.submitted",
  "body-war.business.state.geometry-candidate.rejected",
  "body-war.business.state.geometry-candidate.superseded",
  "body-war.business.state.geometry.draft",
  "body-war.business.state.geometry.missing",
  "body-war.business.state.geometry.placeholder",
  "body-war.business.state.geometry.source-backed",
  "body-war.business.state.geometry.validated",
  "body-war.business.state.score-preview.blocked-geometry",
  "body-war.business.state.score-preview.blocked-policy",
  "body-war.business.state.score-preview.superseded",
  "body-war.business.state.suggested-track.retired",
];

const sourceDefects = Array.from(
  { length: 10 },
  (_, index) =>
    `body-war.business.premise.h-${String(index + 1).padStart(3, "0")}`,
);

const standaloneValues = [
  "body-war.business.value.activity-sport-type",
  "body-war.business.value.badge",
  "body-war.business.value.geometry-status",
  "body-war.business.value.league",
  "body-war.business.value.reference-time",
  "body-war.business.value.zone-type",
];

const dispositionRows = [
  ...policyMembers.map((concept_id) => [concept_id, "POLICY-MEMBER"]),
  ...sourceDefects.map((concept_id) => [concept_id, "SOURCE-DEFECT"]),
  ...standaloneValues.map((concept_id) => [concept_id, "STANDALONE"]),
  ["body-war.business.value.privacy-consent", "ASSOCIATION-REVIEW"],
  ["body-war.business.actor.city-community-operator", "DEFERRED"],
  ["body-war.business.actor.product-team", "OWNER-DECISION"],
  [
    "body-war.business.context.run-validation-anti-cheat",
    "OWNER-DECISION",
  ],
];

export const viewAtlasIsolateDispositions = dispositionRows.map(
  ([concept_id, disposition]) => ({ concept_id, disposition }),
);

export const viewAtlasDispositionLabels = {
  "POLICY-MEMBER": "Lifecycle-policy member — keep as-is",
  "SOURCE-DEFECT": "Source-definition defect — owner decision required",
  STANDALONE: "Standalone vocabulary — keep as-is",
  "ASSOCIATION-REVIEW": "Candidate association — predicate unresolved",
  DEFERRED: "Deferred vocabulary — keep as-is",
  "OWNER-DECISION": "Owner decision required",
};
export const viewAtlasBoundary = {
  authority_effect: "none",
  release_admission: "not-granted",
  lens_note:
    "Editorial lenses are removable navigation groupings, not semantic ontology branches or new business kinds.",
  isolate_note:
    "Research dispositions classify review state only. They are not current ontology admission policy.",
  zero_degree_note:
    "No admitted explicit relation means absent from current relation endpoints; it does not mean meaningless or unrelated in every sense.",
};
