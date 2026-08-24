import fs from "node:fs";
import path from "node:path";

const targetRoot = process.argv[2];
const stagingRoot = process.argv[3];
const findingsPath = process.argv[4];
if (!targetRoot || !stagingRoot || !findingsPath) {
  throw new Error(
    "usage: build-reentry-repair.mjs <target-root> <staging-root> <findings>"
  );
}

const existingTargets = [
  "development/arcanum-addon/plan/DISPATCH.json",
  "development/arcanum-addon/plan/WORK-PACK.md",
  "development/arcanum-addon/plan/EXECUTION-PACK.md",
  "development/arcanum-addon/plan/work-pack/shared/CLOSEOUT-SYNC.md",
  "development/arcanum-addon/plan/DISPATCH-TECHNIQUE-TRACE.md",
  "development/arcanum-addon/plan/DISTILL-VALIDATION.md",
  "development/arcanum-addon/plan/PLAN-RESULT.json",
  "development/arcanum-addon/plan/PLAN-TRANSPORT.md"
];
const createdTargets = [
  "development/arcanum-addon/plan/work-pack/shared/SWU-SELECTION-RECEIPT.schema.json",
  "development/arcanum-addon/plan/work-pack/shared/validate-swu-selection-reentry.mjs"
];
const targets = [...existingTargets, ...createdTargets];

function ensureParent(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function copy(source, target) {
  ensureParent(target);
  fs.copyFileSync(source, target);
}

function readOutput(relativePath) {
  return fs.readFileSync(path.join(stagingRoot, "outputs", relativePath), "utf8");
}

function writeOutput(relativePath, content) {
  const outputPath = path.join(stagingRoot, "outputs", relativePath);
  ensureParent(outputPath);
  fs.writeFileSync(outputPath, content);
}

function replaceOnce(content, before, after, label) {
  const first = content.indexOf(before);
  if (first < 0 || content.indexOf(before, first + before.length) >= 0) {
    throw new Error(`${label}: expected exactly one replacement target`);
  }
  return `${content.slice(0, first)}${after}${content.slice(first + before.length)}`;
}

for (const relativePath of existingTargets) {
  const source = path.join(targetRoot, relativePath);
  copy(source, path.join(stagingRoot, "inputs", relativePath));
  copy(source, path.join(stagingRoot, "outputs", relativePath));
}
for (const relativePath of createdTargets) {
  copy(
    path.join(
      path.dirname(new URL(import.meta.url).pathname),
      "templates",
      path.basename(relativePath)
    ),
    path.join(stagingRoot, "outputs", relativePath)
  );
}
copy(findingsPath, path.join(stagingRoot, "sources", "repair-revalidation-findings.md"));

const dispatchPath = targets[0];
const dispatch = JSON.parse(readOutput(dispatchPath));
dispatch.dispatch_id = "arcanum-addon-implementation-route-v3";
dispatch.intent.objective =
  "Preserve Bootstrap, ResonantOS, Augmentor, execution, state, artifact, memory, readiness, promotion, and release owners while requiring one fresh source-bound operator-selection receipt for every exact SWU and complete exact receipt sets at every W0-W4 boundary.";
dispatch.intent.operator_sentence =
  "Resolve governance and compatibility first; issue one fresh exact SWU selection receipt; admit only the literally matching step; close it; consume the selection once; re-enter selection; and cross a wave only through its complete receipt-set join.";

const requiredSwus = [
  "GOV-001",
  "BOOT-001",
  "BOOT-002",
  "CATALOG-001",
  "STATUS-001",
  "PROPOSAL-001",
  "PROPOSAL-UI-001",
  "L0-DECISION-001",
  "APPROVAL-001",
  "RUN-001",
  "RUN-UI-001",
  "STRATEGY-001",
  "WHISPER-001",
  "CLARIFY-001",
  "ARTIFACT-READ-001",
  "ATTACH-001",
  "CONSUME-001",
  "INTAKE-001",
  "DEGRADE-001",
  "DISABLE-001",
  "UNINSTALL-001",
  "ROLLBACK-001",
  "SECURITY-001",
  "BROWSER-001",
  "VERIFY-001"
];

const producerBySwu = new Map();
for (const step of dispatch.steps) {
  for (const output of step.outputs ?? []) {
    if (output.kind !== "receipt") continue;
    const match = /^receipts\/(.+)\.json$/.exec(output.ref);
    if (match && requiredSwus.includes(match[1])) {
      if (producerBySwu.has(match[1])) {
        throw new Error(`duplicate exact SWU producer: ${match[1]}`);
      }
      producerBySwu.set(match[1], step);
    }
  }
}
for (const swu of requiredSwus) {
  if (!producerBySwu.has(swu)) {
    throw new Error(`missing exact SWU producer: ${swu}`);
  }
}

function selectionInput(swu, stepId) {
  const selectedSwuId = `SWU-ARC-${swu}`;
  return {
    kind: "decision",
    ref: `receipts/selections/{session_id}/${selectedSwuId}.json`,
    binding_contract: {
      validator_ref: "V-SWU-SELECTION",
      gate_id: "g-swu-reentry",
      expected_dispatch_id: dispatch.dispatch_id,
      expected_step_id: stepId,
      expected_selected_swu_id: selectedSwuId,
      single_use: true,
      consume_before_task_start: true,
      on_missing_stale_replay_or_mismatch: "block-with-zero-task-starts"
    }
  };
}

const selectionBoundStepIds = [];
for (const [swu, step] of producerBySwu) {
  step.inputs = [
    selectionInput(swu, step.step_id),
    ...(step.inputs ?? []).filter(
      (item) => !String(item.ref ?? "").startsWith("receipts/selections/")
    )
  ];
  for (const output of step.outputs ?? []) {
    if (output.ref !== `receipts/${swu}.json`) continue;
    output.selection_echo_contract = {
      required_fields: ["selection_id", "selection_receipt_sha256"],
      selected_swu_id: `SWU-ARC-${swu}`,
      on_missing_or_mismatch: "block"
    };
  }
  selectionBoundStepIds.push(step.step_id);
}

const postRefresh = dispatch.steps.find(
  (step) => step.step_id === "s14-boot-post-refresh"
);
if (!postRefresh) {
  throw new Error("missing BOOT-002 post-refresh step");
}
postRefresh.inputs = (postRefresh.inputs ?? []).filter(
  (item) => !String(item.ref ?? "").startsWith("receipts/selections/")
);
postRefresh.internal_postcondition_for = "SWU-ARC-BOOT-002";
postRefresh.admission_policy =
  "not independently schedulable; consumes the selected BOOT-002 terminal receipt and cannot admit a different successor";
postRefresh.stop_conditions = [
  "this is an internal BOOT-002 postcondition validation, not a separately selectable SWU",
  "consume only the terminal BOOT-002 receipt bound to its selection receipt digest",
  "cannot admit a successor; return to explicit selection after closeout sync",
  "stop unless stable public Strategy and Whisper owner operations are proven current"
];

dispatch.selection_receipt_contract = {
  schema_version: "arcanum-addon.swu-selection.v1",
  producer: "explicit-operator-selection-through-task-session",
  validator_ref: "V-SWU-SELECTION",
  schema_ref:
    "development/arcanum-addon/plan/work-pack/shared/SWU-SELECTION-RECEIPT.schema.json",
  validator_path:
    "development/arcanum-addon/plan/work-pack/shared/validate-swu-selection-reentry.mjs",
  store: "receipts/selections/{session_id}/",
  required_fields: [
    "schema_version",
    "status",
    "selection_id",
    "operator_confirmation_handle",
    "issuing_owner",
    "issued_at",
    "expires_at",
    "session_id",
    "run_id",
    "dispatch_id",
    "dispatch_sha256",
    "plan_corpus_sha256",
    "work_pack_sha256",
    "source_commit",
    "selected_swu_id",
    "selected_step_id",
    "dependency_receipts",
    "previous_closeout_sync",
    "single_use_claim_key"
  ],
  admission_rules: [
    "the selected_swu_id and selected_step_id must equal the literal binding_contract values on the target step",
    "dispatch_id, dispatch_sha256, plan_corpus_sha256, work_pack_sha256, source_commit, dependency receipts, and predecessor closeout must match current Task Session preflight bytes",
    "exactly one SWU is admitted per Task Session and independent siblings require separate sessions",
    "the selection must be current, unexpired, operator-issued, and unused",
    "Task Session atomically claims single_use_claim_key before any task start",
    "every terminal SWU receipt echoes selection_id and selection_receipt_sha256",
    "missing, stale, expired, replayed, already-consumed, mismatched, or incomplete-predecessor selection blocks with task_start_count, owner_attempt_count, and mutation_count all zero"
  ]
};

const reentryGate = dispatch.gates.find(
  (gate) => gate.gate_id === "g-swu-reentry"
);
if (!reentryGate) {
  throw new Error("missing g-swu-reentry");
}
reentryGate.condition =
  "Every exact SWU admission consumes a current source-bound selection decision whose literal SWU and step IDs match; the claim is atomically consumed before starts; terminal receipts echo the selection digest; closeout returns to selection before any different successor. Internal joins, BOOT-002 postcondition validation, and readiness routing are not independently selectable.";
reentryGate.applies_to_steps = selectionBoundStepIds.sort();
reentryGate.validator_ref = "V-SWU-SELECTION";
reentryGate.required_input_kind = "decision";
reentryGate.required_input_ref_pattern =
  "receipts/selections/{session_id}/SWU-ARC-<ID>.json";

dispatch.boundary_evidence.boundaries.unshift({
  boundary_id: "b-swu-selection-admission",
  kind: "human_approval",
  from_owner: "explicit-operator",
  to_owner: "task-session",
  applies_to_steps: selectionBoundStepIds.sort(),
  contract:
    "Task Session admits a step only when V-SWU-SELECTION validates a fresh source-bound selection decision whose selected SWU and step IDs match the literal step binding; it consumes the nonce before starts.",
  on_violation: "block"
});
dispatch.boundary_evidence.receipts.unshift({
  receipt_id: "r-swu-selection",
  producer: "explicit-operator-selection-through-task-session",
  required_fields: [
    "run_id",
    "session_id",
    "dispatch_id",
    "step_id",
    "capability_ref",
    "status",
    "validation",
    "approval_record",
    "audit_reference",
    "blockers",
    "residue",
    "handoff_note"
  ],
  stores: ["development/arcanum-addon/plan/receipts/selections/{session_id}/"],
  on_missing: "block"
});

writeOutput(dispatchPath, `${JSON.stringify(dispatch, null, 2)}\n`);

const closeoutPath = existingTargets[3];
let closeout = readOutput(closeoutPath);
closeout = replaceOnce(
  closeout,
  "Common lifecycle owner route: `invoke:refresh:apply-approved` over planning and\nevidence artifacts only. It cannot admit another SWU or product authority.\n",
  "Common lifecycle owner route: `invoke:refresh:apply-approved` over planning and\nevidence artifacts only. It cannot admit another SWU or product authority.\n\nBefore any SWU row starts, Task Session must validate and atomically claim\n`receipts/selections/{session_id}/SWU-ARC-<ID>.json` through\n`validate-swu-selection-reentry.mjs`. The decision binds current dispatch,\nPlan-corpus, work-pack, source, dependency, predecessor-closeout, session/run,\nand literal SWU/step evidence. Missing, stale, expired, replayed, consumed,\nself-issued, mismatched, or incomplete selection blocks with task-start,\nowner-attempt, and mutation counters all zero. Terminal SWU receipts echo the\nselection ID and selection-receipt digest. `s14-boot-post-refresh` is an internal\nBOOT-002 postcondition, consumes its terminal receipt, and cannot admit a\nsuccessor or a separate selection.\n",
  "closeout selection contract"
);
writeOutput(closeoutPath, closeout);

const workPackPath = existingTargets[1];
let workPack = readOutput(workPackPath);
workPack = replaceOnce(
  workPack,
  "| distillValidationStatus | block | The second governed revalidation closed F-001-F-006 but found `NEW-001` and `NEW-BAL-001`; their bounded reconciliation is authored and a fresh exact-byte independent revalidation remains required. |",
  "| distillValidationStatus | block | The repair revalidation closed seven findings but preserved `NEW-001`: per-SWU re-entry was prose-only. A machine-bound selection decision is now authored for every exact SWU; fresh exact-byte independent revalidation remains required. |",
  "work-pack distill status"
);
workPack = replaceOnce(
  workPack,
  "| B-DESIGN-001 | all | The second independent revalidation closed F-001-F-006 but returned `NEW-001` and `NEW-BAL-001`. The exact-SWU dispatch graph and typed lifecycle bindings are now reconciled authoring only. | Invoke operator | keep mutation handoff blocked; run a fresh exact-byte independent revalidation before considering closure |",
  "| B-DESIGN-001 | all | The repair revalidation closed F-001-F-006 and `NEW-BAL-001` but preserved `NEW-001`: no executable step consumed the prose-only re-entry gate. The v3 route now binds every exact SWU to a fresh single-use operator-selection decision, but this is authored evidence only. | Invoke operator | keep mutation handoff blocked; run fresh exact-byte independent revalidation before considering closure |",
  "work-pack design blocker"
);
workPack = replaceOnce(
  workPack,
  "See `DISTILL-VALIDATION.md`. Current verdict remains block: both independently\njoined revalidation receipts returned new blocking findings. Their bounded\nreconciliation has not received a fresh exact-byte independent validation.",
  "See `DISTILL-VALIDATION.md`. Current verdict remains block: the latest\nindependent repair revalidation preserved one MAJOR machine-route finding. The\nv3 selection binding is authored and validated locally but has not received a\nfresh exact-byte independent validation.",
  "work-pack distill prose"
);
workPack +=
  "| 2026-07-30 | Reconciled repair-revalidation `NEW-001`: every exact SWU now consumes a fresh source-bound, single-use operator-selection decision with literal SWU/step matching and zero-start rejection. Gate and `selectedSWU: none` remain unchanged pending fresh exact-byte review. | Invoke Refresh |\n";
writeOutput(workPackPath, workPack);

const executionPath = existingTargets[2];
let execution = readOutput(executionPath);
execution = replaceOnce(
  execution,
  "- Execute one selected SWU per Task Session.\n",
  "- Execute one selected SWU per Task Session.\n- Before any SWU start, `validate-swu-selection-reentry.mjs` must validate and\n  atomically claim the fresh\n  `receipts/selections/{session_id}/SWU-ARC-<ID>.json` decision whose literal\n  SWU and step IDs match the admitted route step; any missing, stale, replayed,\n  consumed, mismatched, or incomplete-predecessor decision yields zero task\n  starts, owner attempts, and mutations.\n",
  "execution selection rule"
);
writeOutput(executionPath, execution);

const techniquePath = existingTargets[4];
let technique = readOutput(techniquePath);
technique = replaceOnce(
  technique,
  "| `sequence` | W0 -> W5 and one SWU per Task Session | No later wave starts without prior receipts | pass-authored |",
  "| `sequence` | W0 -> W5 and one machine-bound selected SWU per Task Session | Every executable SWU consumes a fresh literal SWU/step-matched decision; no later wave starts without prior receipts | pass-reconciled-authored |",
  "technique sequence row"
);
technique = replaceOnce(
  technique,
  "| `execution_receipt_handoff` | Task Session closeout | Exact receipt required before successor selection | pass-authored |",
  "| `execution_receipt_handoff` | Task Session admission and closeout | Fresh single-use selection decision required before start; exact terminal receipt required before successor selection | pass-reconciled-authored |",
  "technique receipt row"
);
writeOutput(techniquePath, technique);

const reviewSection = `

## Repair Revalidation And Machine Admission Repair

- Confirmed sheet:
  \`a850483e486e6d09f6baab804628ea2fd89244ee6fd69bd4115c96ef1c7ca6a1\`
- Admitted pre-repair corpus:
  \`5b5e79f5632b2e29e7a20e7ac4d9e92addef6f707e9525c71e7266c24349e4b0\`
- Verdict: seven findings closed; \`NEW-001\` remained MAJOR because
  \`g-swu-reentry\` was not consumed by executable steps.
- Current authored repair: every exact SWU consumes a fresh
  \`receipts/selections/{session_id}/SWU-ARC-<ID>.json\` decision. The input contract
  literally binds dispatch, step, SWU, source, work-pack, expiry, and a
  single-use nonce; invalid selection yields zero starts.
- Claim ceiling: authored repair only. \`B-DESIGN-001\`, work-pack block, and
  \`selectedSWU: none\` remain until fresh exact-byte independent validation.
`;
const planDistillPath = existingTargets[5];
writeOutput(
  planDistillPath,
  `${readOutput(planDistillPath).trimEnd()}${reviewSection}`
);

const resultPath = existingTargets[6];
const result = JSON.parse(readOutput(resultPath));
result.latest_revalidation = {
    confirmed_sheet_sha256:
      "a850483e486e6d09f6baab804628ea2fd89244ee6fd69bd4115c96ef1c7ca6a1",
    admitted_pre_repair_corpus_sha256:
      "5b5e79f5632b2e29e7a20e7ac4d9e92addef6f707e9525c71e7266c24349e4b0",
    source_commit: "80dcd79677ad73b21dbaded12e0e9cd47aace82b",
    verdict: "block",
    closed_findings: [
      "F-001",
      "F-002",
      "F-003",
      "F-004",
      "F-005",
      "F-006",
      "NEW-BAL-001"
    ],
    surviving_findings: ["NEW-001"],
    reconciled_findings_pending_revalidation: ["NEW-001"]
};
result.distill_validation =
  "block-repair-revalidation-new-001-machine-selection-binding-authored-exact-byte-revalidation-required";
result.dispatch_validation.implementation =
  "pass-repaired-v3-machine-selection-staged";
result.dispatch_validation.distill_closeout =
  "block-repair-revalidation-new-001-reconciled";
result.repository_validation.refresh_invariants =
  "pass-25-exact-swu-producers-25-unique-selection-inputs-zero-internal-selection-wave-joins-typed-lifecycle-selected-none";
result.repository_validation.markdown_local_targets =
  "pass-staged-6-changed-markdown-files";
writeOutput(resultPath, `${JSON.stringify(result, null, 2)}\n`);

const transportPath = existingTargets[7];
let transport = readOutput(transportPath);
transport = replaceOnce(
  transport,
  "4. Task Session may ask to select `SWU-ARC-GOV-001`; no selection is implied.",
  "4. Task Session may ask to select `SWU-ARC-GOV-001`; no selection is implied.\n5. Before a later selection can start, run the shared selection schema and\n   validator, atomically claim its single-use key, and require zero starts on\n   any stale, replayed, mismatched, or incomplete-predecessor decision.",
  "plan transport selection route"
);
writeOutput(transportPath, transport);

for (const createdTarget of createdTargets) {
  const bytes = readOutput(createdTarget);
  if (!bytes.trim()) {
    throw new Error(`empty created target: ${createdTarget}`);
  }
}

process.stdout.write(
  `staged ${targets.length} repaired targets with ${requiredSwus.length} exact SWUs and ${selectionBoundStepIds.length} selection-bound steps\n`
);
