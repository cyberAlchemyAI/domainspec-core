import fs from "node:fs";

const outputPath = process.argv[2];
if (!outputPath) {
  throw new Error("output path required");
}

const receipt = (ref) => ({ kind: "receipt", ref });
const artifact = (ref) => ({ kind: "artifact", ref });
const decision = (ref) => ({ kind: "decision", ref });

const commonStop = [
  "stop after this exact SWU and complete owner closeout sync",
  "return to g-swu-reentry; a successor requires a new explicit operator selection",
  "do not synthesize a generic layer or selected-SWU receipt"
];

function swu({
  id,
  name,
  capability = "task-session",
  mode = "execute-selected-swu",
  pattern = "sequential",
  depends = [],
  inputs,
  output,
  techniques = ["scu_swu_reduction", "execution_receipt_handoff"],
  stop = []
}) {
  return {
    step_id: id,
    name,
    capability_ref: capability,
    ...(capability !== "task-session"
      ? {
          capability_status: "candidate",
          capability_metadata: {
            owner:
              capability === "arcanum-bootstrap"
                ? "Arcanum Bootstrap candidate"
                : "Arcanum decision-gate candidate",
            authority_ceiling:
              capability === "arcanum-bootstrap"
                ? "Bootstrap-owned compatibility or separately approved managed-package receipt only"
                : "decision receipt only"
          }
        }
      : {}),
    mode,
    pattern,
    ...(depends.length ? { depends_on_steps: depends } : {}),
    techniques,
    inputs,
    outputs: [receipt(output)],
    evidence_artifact: output,
    stop_conditions: [...commonStop, ...stop]
  };
}

function join({ id, name, depends, inputs, output, wave }) {
  return {
    step_id: id,
    name,
    capability_ref: "task-session",
    mode: "verify-complete-wave-receipt-set",
    pattern: "validation",
    depends_on_steps: depends,
    techniques: [
      "sequence",
      "recomposition_proof",
      "validation_loop",
      "execution_receipt_handoff"
    ],
    inputs: [...inputs.map(receipt), artifact(`development/arcanum-addon/plan/work-pack/waves/${wave}.md`)],
    outputs: [receipt(output)],
    evidence_artifact: output,
    stop_conditions: [
      `block unless every exact required ${wave} receipt is present, passing, and source-bound`,
      "block on any open execution agent/run, incomplete closeout sync, stale source binding, or hidden residue",
      "do not infer readiness, promotion, or release from wave completion"
    ]
  };
}

const steps = [
  swu({
    id: "s00-gov-001",
    name: "Bind governing issue, Project fields, owners, and retention disposition",
    capability: "decision-gate",
    mode: "resolve",
    pattern: "decision",
    inputs: [
      { kind: "intent", ref: "intent.raw" },
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md")
    ],
    output: "receipts/GOV-001.json",
    techniques: ["owner_boundary_check", "residue_ledger"],
    stop: [
      "stop until one complete owner-issued governance packet binds all required fields",
      "partial issue, Project, owner, or retention synchronization authorizes no successor"
    ]
  }),
  swu({
    id: "s01-boot-001",
    name: "Produce the no-write Bootstrap compatibility receipt",
    capability: "arcanum-bootstrap",
    mode: "dry-run",
    depends: ["s00-gov-001"],
    inputs: [
      receipt("receipts/GOV-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md")
    ],
    output: "receipts/BOOT-001.json",
    techniques: ["owner_boundary_check", "execution_receipt_handoff", "state_namespace_boundary"],
    stop: [
      "stop on missing or drifted generated operations",
      "do not apply a refresh without a separate exact approval"
    ]
  }),
  join({
    id: "s02-w0-join",
    name: "Join the required W0 governance and no-write compatibility receipts",
    depends: ["s00-gov-001", "s01-boot-001"],
    inputs: ["receipts/GOV-001.json", "receipts/BOOT-001.json"],
    output: "receipts/W0-COMPLETE.json",
    wave: "W0"
  }),
  swu({
    id: "s03-catalog-001",
    name: "Create the no-authority catalog candidate",
    depends: ["s02-w0-join"],
    inputs: [
      receipt("receipts/W0-COMPLETE.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-1-CATALOG-PREVIEW.md")
    ],
    output: "receipts/CATALOG-001.json",
    stop: ["stop if catalog presence installs, enables, grants, or executes the add-on"]
  }),
  swu({
    id: "s04-status-001",
    name: "Expose redacted read-only Arcanum status",
    depends: ["s03-catalog-001"],
    inputs: [
      receipt("receipts/CATALOG-001.json"),
      receipt("receipts/BOOT-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-1-CATALOG-PREVIEW.md")
    ],
    output: "receipts/STATUS-001.json",
    stop: ["stop on secret, raw-path, grant, install, refresh, or execution authority"]
  }),
  swu({
    id: "s05-proposal-001",
    name: "Create the pure canonical proposal resolver",
    depends: ["s04-status-001"],
    inputs: [
      receipt("receipts/STATUS-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-1-CATALOG-PREVIEW.md")
    ],
    output: "receipts/PROPOSAL-001.json",
    stop: ["stop unless repeated resolution is byte-identical and every effect counter is zero"]
  }),
  swu({
    id: "s06-proposal-ui-001",
    name: "Project the proposal through Augmentor without routing authority",
    depends: ["s05-proposal-001"],
    inputs: [
      receipt("receipts/PROPOSAL-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-1-CATALOG-PREVIEW.md")
    ],
    output: "receipts/PROPOSAL-UI-001.json",
    stop: ["stop if explicit commands lose precedence or either surface implies an action started"]
  }),
  swu({
    id: "s07-l0-decision-001",
    name: "Record the exact L0 continuation disposition",
    capability: "decision-gate",
    mode: "resolve",
    pattern: "decision",
    depends: ["s06-proposal-ui-001"],
    inputs: [
      receipt("receipts/CATALOG-001.json"),
      receipt("receipts/STATUS-001.json"),
      receipt("receipts/PROPOSAL-001.json"),
      receipt("receipts/PROPOSAL-UI-001.json")
    ],
    output: "receipts/L0-DECISION-001.json",
    techniques: ["owner_boundary_check", "execution_receipt_handoff", "residue_ledger"],
    stop: [
      "only an owner-issued current disposition of continue admits W2",
      "preview-only or stop authorizes no approval or run successor"
    ]
  }),
  join({
    id: "s08-w1-join",
    name: "Join the complete W1 catalog and preview receipt set",
    depends: [
      "s03-catalog-001",
      "s04-status-001",
      "s05-proposal-001",
      "s06-proposal-ui-001",
      "s07-l0-decision-001"
    ],
    inputs: [
      "receipts/CATALOG-001.json",
      "receipts/STATUS-001.json",
      "receipts/PROPOSAL-001.json",
      "receipts/PROPOSAL-UI-001.json",
      "receipts/L0-DECISION-001.json"
    ],
    output: "receipts/W1-COMPLETE.json",
    wave: "W1"
  }),
  swu({
    id: "s09-approval-001",
    name: "Persist exact current proposal approval",
    depends: ["s08-w1-join"],
    inputs: [
      receipt("receipts/W1-COMPLETE.json"),
      decision("receipts/L0-DECISION-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-2-APPROVAL-STATE.md")
    ],
    output: "receipts/APPROVAL-001.json",
    stop: ["stop on stale, edited, expired, replayed, grant-drifted, or provenance-drifted binding"]
  }),
  swu({
    id: "s10-run-001",
    name: "Create the at-most-once fake-owner run lifecycle",
    depends: ["s09-approval-001"],
    inputs: [
      receipt("receipts/APPROVAL-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-2-APPROVAL-STATE.md")
    ],
    output: "receipts/RUN-001.json",
    stop: ["stop if HTTP success is treated as owner terminal truth or a replay starts twice"]
  }),
  swu({
    id: "s11-run-ui-001",
    name: "Project owner-backed run state across both Augmentor surfaces",
    depends: ["s10-run-001"],
    inputs: [
      receipt("receipts/RUN-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-2-APPROVAL-STATE.md")
    ],
    output: "receipts/RUN-UI-001.json",
    stop: ["stop unless reload is exact or explicitly Unknown and parent chat remains usable"]
  }),
  join({
    id: "s12-w2-join",
    name: "Join the complete W2 approval and owner-state receipt set",
    depends: ["s09-approval-001", "s10-run-001", "s11-run-ui-001"],
    inputs: [
      "receipts/APPROVAL-001.json",
      "receipts/RUN-001.json",
      "receipts/RUN-UI-001.json"
    ],
    output: "receipts/W2-COMPLETE.json",
    wave: "W2"
  }),
  swu({
    id: "s13-boot-002",
    name: "Apply the separately approved selected-package Bootstrap refresh",
    capability: "arcanum-bootstrap",
    mode: "apply-approved",
    depends: ["s01-boot-001", "s12-w2-join"],
    inputs: [
      receipt("receipts/BOOT-001.json"),
      decision("receipts/BOOT-002-APPROVAL.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md")
    ],
    output: "receipts/BOOT-002.json",
    techniques: ["owner_boundary_check", "execution_receipt_handoff", "state_namespace_boundary"],
    stop: [
      "stop without a separate exact content-addressed Bootstrap approval",
      "stop unless staged validation and all-or-nothing apply or exact restoration pass"
    ]
  }),
  swu({
    id: "s14-boot-post-refresh",
    name: "Recheck Bootstrap compatibility after the approved refresh",
    capability: "arcanum-bootstrap",
    mode: "dry-run",
    depends: ["s13-boot-002"],
    inputs: [
      receipt("receipts/BOOT-002.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md")
    ],
    output: "receipts/BOOT-001-POST-REFRESH.json",
    techniques: ["owner_boundary_check", "execution_receipt_handoff", "state_namespace_boundary"],
    stop: ["stop unless stable public Strategy and Whisper owner operations are proven current"]
  }),
  swu({
    id: "s15-strategy-001",
    name: "Bind the stable public Strategy owner adapter",
    depends: ["s12-w2-join", "s14-boot-post-refresh"],
    inputs: [
      receipt("receipts/W2-COMPLETE.json"),
      receipt("receipts/BOOT-001-POST-REFRESH.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-3-ADAPTERS-RESULTS.md")
    ],
    output: "receipts/STRATEGY-001.json",
    stop: ["stop with zero attempts if the exact public owner is missing or incompatible; never substitute"]
  }),
  swu({
    id: "s16-whisper-001",
    name: "Bind the stable public Whisper owner adapter",
    depends: ["s15-strategy-001"],
    inputs: [
      receipt("receipts/W2-COMPLETE.json"),
      receipt("receipts/BOOT-001-POST-REFRESH.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-3-ADAPTERS-RESULTS.md")
    ],
    output: "receipts/WHISPER-001.json",
    stop: ["stop with zero attempts if the exact public owner is missing or incompatible; never substitute"]
  }),
  swu({
    id: "s17-clarify-001",
    name: "Deliver one child-scoped clarification",
    depends: ["s15-strategy-001", "s16-whisper-001"],
    inputs: [
      receipt("receipts/STRATEGY-001.json"),
      receipt("receipts/WHISPER-001.json"),
      receipt("receipts/RUN-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-3-ADAPTERS-RESULTS.md")
    ],
    output: "receipts/CLARIFY-001.json",
    stop: ["stop unless the addressed child receives exactly one message and parent/sibling receive zero"]
  }),
  swu({
    id: "s18-artifact-read-001",
    name: "Read one owner artifact by opaque handle",
    depends: ["s17-clarify-001"],
    inputs: [
      receipt("receipts/STRATEGY-001.json"),
      receipt("receipts/WHISPER-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-3-ADAPTERS-RESULTS.md")
    ],
    output: "receipts/ARTIFACT-READ-001.json",
    stop: ["stop if artifact read mutates chat, follow-up, memory, run, sibling, or owner state"]
  }),
  swu({
    id: "s19-attach-001",
    name: "Attach one artifact reference to the selected chat",
    depends: ["s18-artifact-read-001"],
    inputs: [
      receipt("receipts/ARTIFACT-READ-001.json"),
      receipt("receipts/RUN-UI-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-3-ADAPTERS-RESULTS.md")
    ],
    output: "receipts/ATTACH-001.json",
    stop: ["stop unless only the selected chat changes"]
  }),
  swu({
    id: "s20-consume-001",
    name: "Consume one artifact in an explicit follow-up",
    depends: ["s19-attach-001"],
    inputs: [
      receipt("receipts/ARTIFACT-READ-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-3-ADAPTERS-RESULTS.md")
    ],
    output: "receipts/CONSUME-001.json",
    stop: ["stop on sibling, run, memory, lifecycle, or implicit-follow-up mutation"]
  }),
  swu({
    id: "s21-intake-001",
    name: "Request provenance-preserving Living Archive intake",
    depends: ["s20-consume-001"],
    inputs: [
      receipt("receipts/ARTIFACT-READ-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-3-ADAPTERS-RESULTS.md")
    ],
    output: "receipts/INTAKE-001.json",
    stop: ["stop if intake writes trusted memory or bypasses archive review/promotion"]
  }),
  join({
    id: "s22-w3-join",
    name: "Join the complete W3 adapter and result receipt set",
    depends: [
      "s15-strategy-001",
      "s16-whisper-001",
      "s17-clarify-001",
      "s18-artifact-read-001",
      "s19-attach-001",
      "s20-consume-001",
      "s21-intake-001"
    ],
    inputs: [
      "receipts/BOOT-002.json",
      "receipts/BOOT-001-POST-REFRESH.json",
      "receipts/STRATEGY-001.json",
      "receipts/WHISPER-001.json",
      "receipts/CLARIFY-001.json",
      "receipts/ARTIFACT-READ-001.json",
      "receipts/ATTACH-001.json",
      "receipts/CONSUME-001.json",
      "receipts/INTAKE-001.json"
    ],
    output: "receipts/W3-COMPLETE.json",
    wave: "W3"
  }),
  swu({
    id: "s23-degrade-001",
    name: "Prove compatibility-drift and owner-loss degradation",
    depends: ["s22-w3-join"],
    inputs: [
      receipt("receipts/W3-COMPLETE.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md")
    ],
    output: "receipts/DEGRADE-001.json",
    techniques: ["scu_swu_reduction", "validation_loop", "execution_receipt_handoff"],
    stop: [
      "bind the accepted enabled or running candidate plus compatibility and owner baseline digests",
      "stop unless both stressors yield zero new starts, honest state, preserved history, and explicit recovery"
    ]
  }),
  swu({
    id: "s24-disable-001",
    name: "Disable the add-on and revoke launch authority",
    depends: ["s23-degrade-001"],
    inputs: [
      receipt("receipts/W3-COMPLETE.json"),
      receipt("receipts/DEGRADE-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md")
    ],
    output: "receipts/DISABLE-001.json",
    stop: ["stop unless cached and new launches are rejected and owner history remains intact"]
  }),
  swu({
    id: "s25-uninstall-001",
    name: "Run uninstall on one isolated accepted disabled snapshot",
    depends: ["s24-disable-001"],
    inputs: [
      receipt("receipts/DISABLE-001.json"),
      decision("receipts/RETENTION-001.json"),
      artifact("fixtures/W4/accepted-disabled-snapshot.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md")
    ],
    output: "receipts/UNINSTALL-001.json",
    stop: [
      "bind branch id uninstall and the accepted disabled snapshot digest",
      "stop on any Bootstrap inventory or retained owner-history mutation"
    ]
  }),
  swu({
    id: "s26-rollback-001",
    name: "Run rollback on a separate isolated copy of the accepted disabled snapshot",
    depends: ["s24-disable-001"],
    inputs: [
      receipt("receipts/DISABLE-001.json"),
      artifact("fixtures/W4/accepted-disabled-snapshot.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md")
    ],
    output: "receipts/ROLLBACK-001.json",
    stop: [
      "bind branch id rollback and the same accepted disabled snapshot digest without consuming uninstall state",
      "stop unless success and forced failure preserve Bootstrap inventory and owner history; failure remains disabled"
    ]
  }),
  join({
    id: "s27-w4-lifecycle-join",
    name: "Join degradation and both isolated disabled-lifecycle branches",
    depends: ["s23-degrade-001", "s25-uninstall-001", "s26-rollback-001"],
    inputs: [
      "receipts/DEGRADE-001.json",
      "receipts/DISABLE-001.json",
      "receipts/UNINSTALL-001.json",
      "receipts/ROLLBACK-001.json"
    ],
    output: "receipts/W4-LIFECYCLE-JOIN.json",
    wave: "W4"
  }),
  swu({
    id: "s28-security-001",
    name: "Close the complete security and repository gate",
    mode: "verify",
    pattern: "validation",
    depends: ["s27-w4-lifecycle-join"],
    inputs: [
      receipt("receipts/W3-COMPLETE.json"),
      receipt("receipts/DEGRADE-001.json"),
      receipt("receipts/UNINSTALL-001.json"),
      receipt("receipts/ROLLBACK-001.json"),
      receipt("receipts/W4-LIFECYCLE-JOIN.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md")
    ],
    output: "receipts/SECURITY-001.json",
    techniques: ["recomposition_proof", "validation_loop", "residue_ledger"],
    stop: [
      "require V-DEGRADATION-BASELINE and V-DISABLED-LIFECYCLE-BRANCHES to pass before V-SECURITY-LIFECYCLE-JOIN",
      "validation may open an owning SWU but must not repair runtime source"
    ]
  }),
  swu({
    id: "s29-browser-001",
    name: "Capture the literal two-child local Chrome witness",
    mode: "verify",
    pattern: "validation",
    depends: ["s28-security-001"],
    inputs: [
      receipt("receipts/SECURITY-001.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md")
    ],
    output: "receipts/BROWSER-001.json",
    techniques: ["validation_loop", "execution_receipt_handoff"],
    stop: [
      "do not start before every deterministic, security, and repository gate passes",
      "browser validation may capture evidence but must not patch runtime source"
    ]
  }),
  join({
    id: "s30-w4-join",
    name: "Join the complete W4 lifecycle, security, and browser receipt set",
    depends: [
      "s23-degrade-001",
      "s24-disable-001",
      "s25-uninstall-001",
      "s26-rollback-001",
      "s27-w4-lifecycle-join",
      "s28-security-001",
      "s29-browser-001"
    ],
    inputs: [
      "receipts/DEGRADE-001.json",
      "receipts/DISABLE-001.json",
      "receipts/UNINSTALL-001.json",
      "receipts/ROLLBACK-001.json",
      "receipts/W4-LIFECYCLE-JOIN.json",
      "receipts/SECURITY-001.json",
      "receipts/BROWSER-001.json"
    ],
    output: "receipts/W4-COMPLETE.json",
    wave: "W4"
  }),
  swu({
    id: "s31-verify-001",
    name: "Verify complete claim-to-evidence recomposition",
    mode: "verify",
    pattern: "validation",
    depends: ["s30-w4-join"],
    inputs: [
      receipt("receipts/W0-COMPLETE.json"),
      receipt("receipts/W1-COMPLETE.json"),
      receipt("receipts/W2-COMPLETE.json"),
      receipt("receipts/W3-COMPLETE.json"),
      receipt("receipts/W4-COMPLETE.json"),
      artifact("development/arcanum-addon/plan/work-pack/tasks/TASK-5-VERIFY-DECIDE.md")
    ],
    output: "receipts/VERIFY-001.json",
    techniques: ["recomposition_proof", "validation_loop", "residue_ledger"],
    stop: [
      "block if any planned witness is counted as executed",
      "block if any required receipt, negative witness, exact source binding, or closeout receipt is absent"
    ]
  }),
  {
    step_id: "s32-readiness",
    name: "Route the independent readiness decision",
    capability_ref: "decision-gate",
    capability_status: "candidate",
    capability_metadata: {
      owner: "Arcanum decision-gate candidate",
      authority_ceiling: "decision receipt only"
    },
    mode: "resolve",
    pattern: "handoff",
    depends_on_steps: ["s31-verify-001"],
    techniques: ["owner_boundary_check", "handle_handoff"],
    inputs: [receipt("receipts/VERIFY-001.json")],
    outputs: [{ kind: "handoff", ref: "product-acceptance-owner" }],
    stop_conditions: [
      "stop after routing readiness",
      "do not infer promotion or release from readiness"
    ]
  }
];

const exactSwuSteps = steps
  .filter((step) => !step.step_id.endsWith("-join") && step.step_id !== "s32-readiness")
  .map((step) => step.step_id);

const doc = {
  dispatch_id: "arcanum-addon-implementation-route-v2",
  intent: {
    raw: "Implement the approved Arcanum add-on work-pack one explicitly selected SWU at a time.",
    objective: "Preserve Bootstrap, ResonantOS, Augmentor, execution, state, artifact, memory, readiness, promotion, and release owners while requiring complete exact receipt sets at every W0-W4 boundary.",
    target_artifact: "development/arcanum-addon/plan/WORK-PACK.md",
    operator_sentence: "Resolve governance and compatibility first; select one exact SWU per Task Session; close it; re-enter selection; and cross a wave only through its complete receipt-set join."
  },
  mode: "sequence",
  techniques: [
    "sequence",
    "scu_swu_reduction",
    "recomposition_proof",
    "validation_loop",
    "owner_boundary_check",
    "handle_handoff",
    "residue_ledger",
    "execution_receipt_handoff",
    "state_namespace_boundary"
  ],
  subagent_strategy: {
    status: "none",
    trigger: "The default implementation route is sequential and admits exactly one explicitly selected SWU per Task Session.",
    explanation: "No parallel worker route is authorized. The uninstall and rollback nodes are dependency siblings over isolated snapshots, not permission for concurrent workers. Any later delegated execution requires its own validated and confirmed dispatch.",
    context: [
      "development/arcanum-addon/plan/WORK-PACK.md",
      "development/arcanum-addon/plan/EXECUTION-PACK.md"
    ],
    binding_mode: "descriptive",
    roles: [],
    parallelism: "none",
    join_policy: "none",
    authorization: "not_needed",
    receipt_requirements: []
  },
  subagent_lifecycle: { status: "none", agents: [] },
  steps,
  gates: [
    {
      gate_id: "g-governance",
      kind: "human_approval",
      owner: "product-maintainer",
      condition: "Governing issue, Project 2 item, owners, retention disposition, current source binding, and the one selected SWU are explicit.",
      on_fail: "block"
    },
    {
      gate_id: "g-bootstrap",
      kind: "policy",
      owner: "arcanum-bootstrap",
      condition: "Compatibility checks are no-write; BOOT-002 requires separate exact approval; product work cannot imply Bootstrap mutation.",
      on_fail: "block"
    },
    {
      gate_id: "g-swu-reentry",
      kind: "quality",
      owner: "task-session",
      condition: "Every exact SWU ends after one owner receipt and complete closeout sync; execution returns to explicit operator selection before any successor.",
      on_fail: "block"
    },
    {
      gate_id: "g-w0-complete",
      kind: "quality",
      owner: "task-session",
      condition: "W0-COMPLETE binds passing GOV-001 and BOOT-001 receipts.",
      on_fail: "block"
    },
    {
      gate_id: "g-w1-complete",
      kind: "quality",
      owner: "task-session",
      condition: "W1-COMPLETE binds CATALOG, STATUS, PROPOSAL, PROPOSAL-UI, and current L0-DECISION receipts; W2 additionally requires disposition continue.",
      on_fail: "block"
    },
    {
      gate_id: "g-w2-complete",
      kind: "quality",
      owner: "task-session",
      condition: "W2-COMPLETE binds APPROVAL, RUN, and RUN-UI receipts.",
      on_fail: "block"
    },
    {
      gate_id: "g-w3-complete",
      kind: "quality",
      owner: "task-session",
      condition: "W3-COMPLETE binds BOOT-002, post-refresh compatibility, both adapters, CLARIFY, ARTIFACT-READ, ATTACH, CONSUME, and INTAKE receipts.",
      on_fail: "block"
    },
    {
      gate_id: "g-w4-complete",
      kind: "validation",
      owner: "validation-owner",
      condition: "W4-COMPLETE binds DEGRADE, DISABLE, isolated UNINSTALL and ROLLBACK branches, their typed lifecycle join, SECURITY, and literal BROWSER receipts.",
      on_fail: "block"
    },
    {
      gate_id: "g-validation",
      kind: "validation",
      owner: "validation-owner",
      condition: "VERIFY-001 consumes W0-COMPLETE through W4-COMPLETE and proves deterministic, security, repository, and live-browser evidence against the exact candidate.",
      on_fail: "block"
    },
    {
      gate_id: "g-promotion",
      kind: "promotion_guardrail",
      owner: "product-acceptance-owner",
      condition: "Verification routes only readiness; promotion and release remain separate owner decisions.",
      on_fail: "block"
    }
  ],
  boundary_evidence: {
    boundaries: [
      {
        boundary_id: "b-bootstrap-product",
        kind: "capability_handoff",
        from_owner: "arcanum-bootstrap",
        to_owner: "resonantos-product",
        applies_to_steps: [
          "s01-boot-001",
          "s03-catalog-001",
          "s13-boot-002",
          "s14-boot-post-refresh",
          "s15-strategy-001",
          "s16-whisper-001"
        ],
        contract: "Product consumes admitted redacted compatibility receipts and never writes Bootstrap-managed generated packages.",
        on_violation: "block"
      },
      {
        boundary_id: "b-task-closeout",
        kind: "evidence_return",
        from_owner: "task-session",
        to_owner: "invoke-refresh",
        applies_to_steps: exactSwuSteps,
        contract: "Every exact SWU returns its named source-bound receipt, completes closeout sync, and re-enters explicit selection; generic layer receipts are forbidden.",
        on_violation: "block"
      },
      {
        boundary_id: "b-wave-completion",
        kind: "evidence_return",
        from_owner: "task-session",
        to_owner: "next-wave-owner",
        applies_to_steps: [
          "s02-w0-join",
          "s08-w1-join",
          "s12-w2-join",
          "s22-w3-join",
          "s27-w4-lifecycle-join",
          "s30-w4-join",
          "s31-verify-001"
        ],
        contract: "Only exact named wave-complete receipts admit a later wave; VERIFY-001 must consume the complete W4 bundle.",
        on_violation: "block"
      },
      {
        boundary_id: "b-readiness-promotion",
        kind: "human_approval",
        from_owner: "validation-owner",
        to_owner: "product-acceptance-owner",
        applies_to_steps: ["s31-verify-001", "s32-readiness"],
        contract: "Verification may inform readiness but cannot promote or release.",
        on_violation: "block"
      }
    ],
    authority: {
      lifecycle: "resonantos-product-owner and arcanum-bootstrap remain distinct",
      execution: "stable public Arcanum owner operation through ResonantOS mediation",
      validation: "independent validation owner",
      evidence: "operation and validation owners return separate exact receipts",
      memory: "Living Archive intake/review/promotion owners",
      promotion: "product promotion owner after readiness"
    },
    receipts: [
      {
        receipt_id: "r-exact-swu",
        producer: "task-session",
        required_fields: [
          "run_id",
          "session_id",
          "dispatch_id",
          "step_id",
          "capability_ref",
          "status",
          "artifacts",
          "validation",
          "blockers",
          "residue",
          "handoff_note"
        ],
        stores: ["development/arcanum-addon/plan/receipts/"],
        on_missing: "block"
      },
      {
        receipt_id: "r-wave-complete",
        producer: "task-session",
        required_fields: [
          "run_id",
          "session_id",
          "dispatch_id",
          "step_id",
          "capability_ref",
          "status",
          "artifacts",
          "validation",
          "blockers",
          "residue",
          "handoff_note"
        ],
        stores: ["development/arcanum-addon/plan/receipts/"],
        on_missing: "block"
      }
    ],
    state_namespaces: [
      {
        namespace: "consumer-generated-arcanum",
        owner: "arcanum-bootstrap",
        write_policy: "Bootstrap manifest-managed writes only"
      },
      {
        namespace: "resonantos-product-records",
        owner: "resonantos-addon-host",
        write_policy: "named authenticated capability-gated services only"
      },
      {
        namespace: "augmentor-session-projection",
        owner: "extension-chat-session-owner",
        write_policy: "opaque redacted references only"
      },
      {
        namespace: "living-archive-intake",
        owner: "living-archive-intake-owner",
        write_policy: "explicit intake request; no trusted write"
      }
    ],
    promotion_splits: [
      {
        source: "verified implementation evidence",
        target: "readiness decision",
        rule: "acceptance owner decides; verification cannot self-admit",
        on_violation: "block"
      },
      {
        source: "readiness decision",
        target: "promotion decision",
        rule: "promotion owner independently admits the exact candidate",
        on_violation: "block"
      },
      {
        source: "promotion decision",
        target: "release decision",
        rule: "release owner applies release-specific policy and packaging",
        on_violation: "block"
      }
    ]
  },
  promotion_guardrails: [
    "Plan evidence is not implementation evidence.",
    "A generated package is not an installed or granted product add-on.",
    "Augmentor projection is not approval or execution truth.",
    "Readiness, promotion, and release are independent owner decisions."
  ],
  observability: {
    dispatch_id_required: true,
    trace_events: [
      "governance_bound",
      "bootstrap_compatibility_observed",
      "swu_selected",
      "task_session_started",
      "task_session_closed",
      "owner_closeout_synchronized",
      "swu_selection_reentered",
      "wave_receipt_set_joined",
      "wave_gate_evaluated",
      "lifecycle_branch_joined",
      "verification_completed",
      "readiness_routed"
    ],
    signal_grouping: "dispatch_id"
  }
};

fs.writeFileSync(outputPath, `${JSON.stringify(doc, null, 2)}\n`);
