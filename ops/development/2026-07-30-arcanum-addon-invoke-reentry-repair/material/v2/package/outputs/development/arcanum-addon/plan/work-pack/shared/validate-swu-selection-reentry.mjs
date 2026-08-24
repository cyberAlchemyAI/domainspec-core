import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const SWU_STEP_MAP = {
  "SWU-ARC-GOV-001": "s00-gov-001",
  "SWU-ARC-BOOT-001": "s01-boot-001",
  "SWU-ARC-CATALOG-001": "s03-catalog-001",
  "SWU-ARC-STATUS-001": "s04-status-001",
  "SWU-ARC-PROPOSAL-001": "s05-proposal-001",
  "SWU-ARC-PROPOSAL-UI-001": "s06-proposal-ui-001",
  "SWU-ARC-L0-DECISION-001": "s07-l0-decision-001",
  "SWU-ARC-APPROVAL-001": "s09-approval-001",
  "SWU-ARC-RUN-001": "s10-run-001",
  "SWU-ARC-RUN-UI-001": "s11-run-ui-001",
  "SWU-ARC-BOOT-002": "s13-boot-002",
  "SWU-ARC-STRATEGY-001": "s15-strategy-001",
  "SWU-ARC-WHISPER-001": "s16-whisper-001",
  "SWU-ARC-CLARIFY-001": "s17-clarify-001",
  "SWU-ARC-ARTIFACT-READ-001": "s18-artifact-read-001",
  "SWU-ARC-ATTACH-001": "s19-attach-001",
  "SWU-ARC-CONSUME-001": "s20-consume-001",
  "SWU-ARC-INTAKE-001": "s21-intake-001",
  "SWU-ARC-DEGRADE-001": "s23-degrade-001",
  "SWU-ARC-DISABLE-001": "s24-disable-001",
  "SWU-ARC-UNINSTALL-001": "s25-uninstall-001",
  "SWU-ARC-ROLLBACK-001": "s26-rollback-001",
  "SWU-ARC-SECURITY-001": "s28-security-001",
  "SWU-ARC-BROWSER-001": "s29-browser-001",
  "SWU-ARC-VERIFY-001": "s31-verify-001"
};

const REQUIRED_SELECTION_FIELDS = [
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
];

const sha256 = (bytes) =>
  crypto.createHash("sha256").update(bytes).digest("hex");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function exactSelectionRef(selectedSwuId) {
  return `receipts/selections/{session_id}/${selectedSwuId}.json`;
}

function selectionInputs(step) {
  return (step.inputs ?? []).filter(
    (input) =>
      input.kind === "decision" &&
      String(input.ref ?? "").startsWith("receipts/selections/")
  );
}

function staticPlanFailures(planRoot) {
  const failures = [];
  const dispatch = readJson(path.join(planRoot, "DISPATCH.json"));
  const workPack = fs.readFileSync(path.join(planRoot, "WORK-PACK.md"), "utf8");
  const schema = readJson(
    path.join(
      planRoot,
      "work-pack/shared/SWU-SELECTION-RECEIPT.schema.json"
    )
  );
  const stepById = new Map(dispatch.steps.map((step) => [step.step_id, step]));

  if (Object.keys(SWU_STEP_MAP).length !== 25) {
    failures.push("static SWU mapping is not exactly 25");
  }

  for (const [selectedSwuId, stepId] of Object.entries(SWU_STEP_MAP)) {
    const step = stepById.get(stepId);
    if (!step) {
      failures.push(`${selectedSwuId} missing admission step ${stepId}`);
      continue;
    }
    const inputs = selectionInputs(step);
    if (
      inputs.length !== 1 ||
      inputs[0].ref !== exactSelectionRef(selectedSwuId)
    ) {
      failures.push(`${stepId} does not have one exact selection input`);
      continue;
    }
    const binding = inputs[0].binding_contract ?? {};
    if (
      binding.validator_ref !== "V-SWU-SELECTION" ||
      binding.gate_id !== "g-swu-reentry" ||
      binding.expected_dispatch_id !== dispatch.dispatch_id ||
      binding.expected_step_id !== stepId ||
      binding.expected_selected_swu_id !== selectedSwuId ||
      binding.single_use !== true ||
      binding.consume_before_task_start !== true ||
      binding.on_missing_stale_replay_or_mismatch !==
        "block-with-zero-task-starts"
    ) {
      failures.push(`${stepId} selection binding contract mismatch`);
    }

    const swuSuffix = selectedSwuId.slice("SWU-ARC-".length);
    const terminal = (step.outputs ?? []).find(
      (output) => output.ref === `receipts/${swuSuffix}.json`
    );
    const echo = terminal?.selection_echo_contract;
    if (
      !echo ||
      echo.selected_swu_id !== selectedSwuId ||
      !echo.required_fields?.includes("selection_id") ||
      !echo.required_fields?.includes("selection_receipt_sha256")
    ) {
      failures.push(`${stepId} terminal receipt lacks selection echo`);
    }
  }

  const admittedSteps = new Set(Object.values(SWU_STEP_MAP));
  for (const step of dispatch.steps) {
    if (!admittedSteps.has(step.step_id) && selectionInputs(step).length) {
      failures.push(`${step.step_id} is an internal node with a selection input`);
    }
  }

  const gate = dispatch.gates.find(
    (candidate) => candidate.gate_id === "g-swu-reentry"
  );
  const gateSteps = new Set(gate?.applies_to_steps ?? []);
  if (
    gate?.validator_ref !== "V-SWU-SELECTION" ||
    gate?.required_input_kind !== "decision" ||
    gate?.required_input_ref_pattern !==
      "receipts/selections/{session_id}/SWU-ARC-<ID>.json" ||
    gateSteps.size !== admittedSteps.size ||
    [...admittedSteps].some((stepId) => !gateSteps.has(stepId))
  ) {
    failures.push("g-swu-reentry is not attached to exactly 25 admissions");
  }

  const postRefresh = stepById.get("s14-boot-post-refresh");
  if (
    !postRefresh ||
    selectionInputs(postRefresh).length !== 0 ||
    postRefresh.internal_postcondition_for !== "SWU-ARC-BOOT-002" ||
    !(postRefresh.inputs ?? []).some(
      (input) => input.ref === "receipts/BOOT-002.json"
    )
  ) {
    failures.push("s14 is not a non-selectable BOOT-002 postcondition");
  }

  const joins = [
    "s02-w0-join",
    "s08-w1-join",
    "s12-w2-join",
    "s22-w3-join",
    "s27-w4-lifecycle-join",
    "s30-w4-join",
    "s32-readiness"
  ];
  for (const stepId of joins) {
    if (selectionInputs(stepById.get(stepId) ?? {}).length) {
      failures.push(`${stepId} must not be independently selectable`);
    }
  }

  const schemaRequired = new Set(schema.required ?? []);
  for (const field of REQUIRED_SELECTION_FIELDS) {
    if (!schemaRequired.has(field)) {
      failures.push(`selection schema missing ${field}`);
    }
  }

  for (const requiredOutput of [
    "W0-COMPLETE",
    "W1-COMPLETE",
    "W2-COMPLETE",
    "W3-COMPLETE",
    "W4-LIFECYCLE-JOIN",
    "W4-COMPLETE"
  ]) {
    const count = dispatch.steps.filter((step) =>
      (step.outputs ?? []).some(
        (output) => output.ref === `receipts/${requiredOutput}.json`
      )
    ).length;
    if (count !== 1) {
      failures.push(`${requiredOutput} producer count ${count}`);
    }
  }

  if (!workPack.includes("| workPackGateStatus | block |")) {
    failures.push("work-pack gate is not block");
  }
  if (!workPack.includes("| selectedSWU | none |")) {
    failures.push("selectedSWU is not none");
  }

  const designValidation = fs.readFileSync(
    path.resolve(planRoot, "../design/VALIDATION-CONTRACTS.md"),
    "utf8"
  );
  for (const validator of [
    "V-DEGRADATION-BASELINE",
    "V-DISABLED-LIFECYCLE-BRANCHES",
    "V-SECURITY-LIFECYCLE-JOIN"
  ]) {
    if (!designValidation.includes(validator)) {
      failures.push(`typed lifecycle validator missing: ${validator}`);
    }
  }

  return failures;
}

function receiptShapeFailures(receipt) {
  const failures = [];
  for (const field of REQUIRED_SELECTION_FIELDS) {
    if (!(field in receipt)) failures.push(`missing ${field}`);
  }
  if (receipt.schema_version !== "arcanum-addon.swu-selection.v1") {
    failures.push("unsupported schema_version");
  }
  if (receipt.status !== "selected") failures.push("status is not selected");
  for (const field of [
    "dispatch_sha256",
    "plan_corpus_sha256",
    "work_pack_sha256"
  ]) {
    if (!/^[a-f0-9]{64}$/.test(receipt[field] ?? "")) {
      failures.push(`${field} is not SHA-256`);
    }
  }
  if (!/^[a-f0-9]{40}$/.test(receipt.source_commit ?? "")) {
    failures.push("source_commit is not SHA-1");
  }
  if (!Array.isArray(receipt.dependency_receipts)) {
    failures.push("dependency_receipts is not an array");
  }
  return failures;
}

function validateExactRef(reference, receiptRoot) {
  if (
    !reference ||
    typeof reference.ref !== "string" ||
    !reference.ref.startsWith("receipts/") ||
    !/^[a-f0-9]{64}$/.test(reference.sha256 ?? "")
  ) {
    return "invalid exact receipt reference";
  }
  const root = path.resolve(receiptRoot);
  const target = path.resolve(root, reference.ref);
  if (!target.startsWith(`${root}${path.sep}`) || !fs.existsSync(target)) {
    return `missing or escaped receipt: ${reference.ref}`;
  }
  if (sha256(fs.readFileSync(target)) !== reference.sha256) {
    return `receipt digest mismatch: ${reference.ref}`;
  }
  return null;
}

function runtimeFailures(receipt, current) {
  const failures = receiptShapeFailures(receipt);
  const expectedStep = SWU_STEP_MAP[receipt.selected_swu_id];
  if (!expectedStep || expectedStep !== receipt.selected_step_id) {
    failures.push("selected SWU and admitted step do not literally match");
  }
  for (const field of [
    "session_id",
    "run_id",
    "dispatch_id",
    "dispatch_sha256",
    "plan_corpus_sha256",
    "work_pack_sha256",
    "source_commit"
  ]) {
    if (receipt[field] !== current[field]) failures.push(`${field} mismatch`);
  }
  if (receipt.selection_id !== receipt.session_id) {
    failures.push("selection_id must equal Task Session id");
  }
  const receiptRoot = path.resolve(current.receipt_root);
  const selectionPath = path.resolve(current.selection_path);
  const expectedSelectionPath = path.resolve(
    receiptRoot,
    `receipts/selections/${receipt.session_id}/${receipt.selected_swu_id}.json`
  );
  if (
    !selectionPath.startsWith(`${receiptRoot}${path.sep}`) ||
    selectionPath !== expectedSelectionPath
  ) {
    failures.push("selection receipt path does not match session and selected SWU");
  }
  if (!receipt.operator_confirmation_handle || !receipt.issuing_owner) {
    failures.push("operator confirmation or issuing owner missing");
  }
  const issued = Date.parse(receipt.issued_at);
  const expires = Date.parse(receipt.expires_at);
  if (!Number.isFinite(issued) || !Number.isFinite(expires)) {
    failures.push("selection timestamps invalid");
  } else if (issued > current.now || expires <= current.now || expires <= issued) {
    failures.push("selection is stale or expired");
  }

  const dependencies = receipt.dependency_receipts ?? [];
  const sortedRefs = dependencies.map((item) => item.ref).sort();
  if (
    new Set(sortedRefs).size !== sortedRefs.length ||
    JSON.stringify(dependencies.map((item) => item.ref)) !==
      JSON.stringify(sortedRefs)
  ) {
    failures.push("dependency receipts must be unique and sorted");
  }
  for (const dependency of dependencies) {
    const error = validateExactRef(dependency, current.receipt_root);
    if (error) failures.push(error);
  }

  const firstAdmission = receipt.selected_swu_id === "SWU-ARC-GOV-001";
  if (firstAdmission && receipt.previous_closeout_sync !== null) {
    failures.push("first admission must not claim a predecessor closeout");
  }
  if (!firstAdmission) {
    if (receipt.previous_closeout_sync === null) {
      failures.push("predecessor closeout is required");
    } else {
      const error = validateExactRef(
        receipt.previous_closeout_sync,
        current.receipt_root
      );
      if (error) failures.push(error);
    }
  }
  if (
    typeof receipt.single_use_claim_key !== "string" ||
    receipt.single_use_claim_key.length < 16
  ) {
    failures.push("single-use claim key invalid");
  }
  return failures;
}

function failReceipt(errors) {
  return {
    status: "block",
    errors,
    task_start_count: 0,
    owner_attempt_count: 0,
    mutation_count: 0
  };
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith("--")) {
      args._.push(item);
      continue;
    }
    if (item === "--self-test") {
      args.self_test = true;
      continue;
    }
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) throw new Error(`${item} needs a value`);
    args[item.slice(2).replaceAll("-", "_")] = value;
    index += 1;
  }
  return args;
}

function runSelfTest() {
  const digest = "a".repeat(64);
  const commit = "b".repeat(40);
  const base = {
    schema_version: "arcanum-addon.swu-selection.v1",
    status: "selected",
    selection_id: "session-1",
    operator_confirmation_handle: "chat-confirmation-1",
    issuing_owner: "operator",
    issued_at: "2026-07-30T12:00:00Z",
    expires_at: "2026-07-30T13:00:00Z",
    session_id: "session-1",
    run_id: "run-1",
    dispatch_id: "arcanum-addon-implementation-route-v3",
    dispatch_sha256: digest,
    plan_corpus_sha256: digest,
    work_pack_sha256: digest,
    source_commit: commit,
    selected_swu_id: "SWU-ARC-GOV-001",
    selected_step_id: "s00-gov-001",
    dependency_receipts: [],
    previous_closeout_sync: null,
    single_use_claim_key: "session-1:SWU-ARC-GOV-001"
  };
  const current = {
    session_id: "session-1",
    run_id: "run-1",
    dispatch_id: "arcanum-addon-implementation-route-v3",
    dispatch_sha256: digest,
    plan_corpus_sha256: digest,
    work_pack_sha256: digest,
    source_commit: commit,
    now: Date.parse("2026-07-30T12:30:00Z"),
    receipt_root: process.cwd(),
    selection_path: path.resolve(
      "receipts/selections/session-1/SWU-ARC-GOV-001.json"
    )
  };
  assert.deepEqual(runtimeFailures(base, current), []);
  assert(runtimeFailures({ ...base, selected_step_id: "s01-boot-001" }, current).length);
  assert(
    runtimeFailures(base, {
      ...current,
      selection_path: path.resolve(
        "receipts/selections/session-1/SWU-ARC-BOOT-001.json"
      )
    }).some((item) => item.includes("receipt path"))
  );
  assert(runtimeFailures({ ...base, dispatch_sha256: "c".repeat(64) }, current).length);
  assert(runtimeFailures({ ...base, expires_at: "2026-07-30T12:01:00Z" }, current).length);
  assert(
    runtimeFailures(
      {
        ...base,
        selected_swu_id: "SWU-ARC-VERIFY-001",
        selected_step_id: "s31-verify-001"
      },
      current
    ).some((item) => item.includes("predecessor closeout"))
  );
  assert.equal(SWU_STEP_MAP["SWU-ARC-L0-DECISION-001"], "s07-l0-decision-001");
  assert.equal(SWU_STEP_MAP["SWU-ARC-VERIFY-001"], "s31-verify-001");
  assert(!Object.values(SWU_STEP_MAP).includes("s14-boot-post-refresh"));
  const claimSet = new Set();
  assert(!claimSet.has(base.single_use_claim_key));
  claimSet.add(base.single_use_claim_key);
  assert(claimSet.has(base.single_use_claim_key));
  process.stdout.write(
    "PASS: selection validator self-test covers mismatch, drift, expiry, predecessor closeout, manual/verification SWUs, internal BOOT postcondition, and replay claim\n"
  );
}

const args = parseArgs(process.argv.slice(2));
if (args.self_test) {
  runSelfTest();
  process.exit(0);
}

const planRoot = args._[0];
if (!planRoot) {
  throw new Error(
    "usage: validate-swu-selection-reentry.mjs <plan-root> [--selection <receipt> --session-id <id> --run-id <id> --dispatch-sha256 <sha> --plan-corpus-sha256 <sha> --work-pack-sha256 <sha> --source-commit <sha> --receipt-root <dir> --claim-dir <dir>]"
  );
}

const staticFailures = staticPlanFailures(planRoot);
if (staticFailures.length) {
  process.stderr.write(`${JSON.stringify(failReceipt(staticFailures), null, 2)}\n`);
  process.exit(1);
}

if (!args.selection) {
  process.stdout.write(
    `PASS: ${Object.keys(SWU_STEP_MAP).length} exact SWU admissions, 25 unique selection inputs, zero internal-node selections, terminal selection echoes, wave joins, typed lifecycle bindings, work-pack block, selectedSWU none\n`
  );
  process.exit(0);
}

for (const requiredArg of [
  "session_id",
  "run_id",
  "dispatch_sha256",
  "plan_corpus_sha256",
  "work_pack_sha256",
  "source_commit",
  "receipt_root",
  "claim_dir"
]) {
  if (!args[requiredArg]) throw new Error(`--${requiredArg.replaceAll("_", "-")} required`);
}

const receipt = readJson(args.selection);
const dispatch = readJson(path.join(planRoot, "DISPATCH.json"));
const current = {
  session_id: args.session_id,
  run_id: args.run_id,
  dispatch_id: dispatch.dispatch_id,
  dispatch_sha256: args.dispatch_sha256,
  plan_corpus_sha256: args.plan_corpus_sha256,
  work_pack_sha256: args.work_pack_sha256,
  source_commit: args.source_commit,
  now: args.now ? Date.parse(args.now) : Date.now(),
  receipt_root: args.receipt_root,
  selection_path: args.selection
};
const runtimeErrors = runtimeFailures(receipt, current);
if (runtimeErrors.length) {
  process.stderr.write(`${JSON.stringify(failReceipt(runtimeErrors), null, 2)}\n`);
  process.exit(1);
}

fs.mkdirSync(args.claim_dir, { recursive: true });
const claimName = `${sha256(receipt.single_use_claim_key)}.claim`;
const claimPath = path.join(args.claim_dir, claimName);
let descriptor;
try {
  descriptor = fs.openSync(claimPath, "wx", 0o600);
  fs.writeFileSync(
    descriptor,
    `${JSON.stringify({
      selection_id: receipt.selection_id,
      selection_receipt_sha256: sha256(fs.readFileSync(args.selection)),
      claimed_at: new Date(current.now).toISOString()
    })}\n`
  );
  fs.closeSync(descriptor);
} catch (error) {
  if (descriptor !== undefined) fs.closeSync(descriptor);
  const reason =
    error && error.code === "EEXIST"
      ? "single-use claim already consumed"
      : `claim failed: ${error.message}`;
  process.stderr.write(`${JSON.stringify(failReceipt([reason]), null, 2)}\n`);
  process.exit(1);
}

process.stdout.write(
  `${JSON.stringify({
    status: "pass",
    selection_id: receipt.selection_id,
    selected_swu_id: receipt.selected_swu_id,
    selected_step_id: receipt.selected_step_id,
    selection_receipt_sha256: sha256(fs.readFileSync(args.selection)),
    claim_path: claimPath,
    task_start_count: 0,
    owner_attempt_count: 0,
    mutation_count: 0,
    admission: "ready-after-atomic-claim"
  })}\n`
);
