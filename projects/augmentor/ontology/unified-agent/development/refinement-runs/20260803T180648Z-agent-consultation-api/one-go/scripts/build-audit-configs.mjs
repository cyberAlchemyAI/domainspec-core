import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const REPO = path.resolve(ONE_GO, "../../../../../../../..");
const RUN = path.dirname(ONE_GO);
const GENERATED = path.join(ONE_GO, "generated");
const AUDIT = path.join(ONE_GO, "audit");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const rel = (absolute) => path.relative(REPO, absolute).replaceAll(path.sep, "/");
const readJson = async (target) => JSON.parse(await readFile(target, "utf8"));
const exact = async (relative) => { const bytes = await readFile(path.join(REPO, relative)); return { path: relative, sha256: sha(bytes), size_bytes: bytes.length }; };
const binding = async (id, owner, relative, selector = "") => ({ binding_id: id, owner_ref: owner, artifact_ref: await exact(relative), selector });
const writeJson = async (target, value) => { await mkdir(path.dirname(target), { recursive: true }); await writeFile(target, `${JSON.stringify(value, null, 2)}\n`); };
const PACKAGE_ROOT = "projects/augmentor/ontology/unified-agent";
const packageArgv = (argv) => argv.map((value) => value.startsWith(`${PACKAGE_ROOT}/`) ? value.slice(PACKAGE_ROOT.length + 1) : value);
const command = (argv, risk = "bounded-write") => ({ cwd: PACKAGE_ROOT, argv: packageArgv(argv), expected_exit_code: 0, timeout_seconds: 30, environment: { NODE_ENV: "test" }, runtime_identity: { executable: argv[0], version_policy: "Node v22.x captured at Task Session preflight", hash_policy: "resolve and hash executable at Task Session preflight" }, risk_class: risk });
const attempt = { required: false, id_algorithm: "", collision_policy: "append-only", retention_policy: "retain-receipt-only", teardown_on_success: [], teardown_on_failure: [] };

const build = async () => {
  const [map, summary] = await Promise.all([readJson(path.join(ONE_GO, "material-map.json")), readJson(path.join(GENERATED, "material-summary.json"))]);
  const byUnit = new Map(summary.units.map((unit) => [unit.unit_id, unit]));
  const admissionItems = [];
  for (const unitId of map.frontier) {
    const receiptPath = rel(path.join(GENERATED, unitId, "mutation-admission-receipt.json"));
    const receipt = await readJson(path.join(REPO, receiptPath));
    if (receipt.admissionVerdict !== "admit" || receipt.mutationReady !== true) throw new Error(`${unitId}: admission not ready`);
    admissionItems.push({ unit_id: unitId, admission_verdict: receipt.admissionVerdict, mutation_ready: receipt.mutationReady, receipt_ref: await exact(receiptPath) });
  }
  const admissionSummaryPath = path.join(GENERATED, "task-session-admission-summary.json");
  await writeJson(admissionSummaryPath, { schema_version: "augmentor.consultation.admission-summary@0.1.0", status: "pass", units: admissionItems });
  const expectedReceiptsPath = path.join(GENERATED, "expected-terminal-receipts.json");
  await writeJson(expectedReceiptsPath, { schema_version: "augmentor.consultation.expected-receipts@0.1.0", receipts: map.frontier.map((unitId, index) => ({ unit_id: unitId, step_id: `l0-${unitId.slice(-3)}`, status: "pass", path: rel(path.join(ONE_GO, "execution/receipts", `${unitId}.json`)), successor: index + 1 < map.frontier.length ? map.frontier[index + 1] : null })) });
  const workPackPath = rel(path.join(RUN, "WORK-PACK.md"));
  const taskPaths = [...new Set(map.units.map((unit) => unit.task_contract))];
  const terminalSchemaPath = rel(path.join(ONE_GO, "contracts/terminal-receipt.schema.json"));
  const terminalValidatorPath = rel(path.join(ONE_GO, "scripts/validate-terminal-receipt.mjs"));
  const transitionGatePath = rel(path.join(ONE_GO, "scripts/run-transition-gate.mjs"));
  const transitionGateTestPath = rel(path.join(ONE_GO, "tests/transition-gate.test.mjs"));
  const approvalReceiptSchemaPath = rel(path.join(ONE_GO, "contracts/decision-gate-approval-receipt.schema.json"));
  const approvedChainBuilderPath = rel(path.join(ONE_GO, "scripts/build-approved-chain.mjs"));
  const approvedChainBuilderTestPath = rel(path.join(ONE_GO, "tests/approved-chain-builder.test.mjs"));
  const chainRunnerPath = ".agents/skills/task-session-until-blocker/scripts/run_chain.py";
  const chainConfigSchemaPath = ".agents/skills/task-session-until-blocker/schemas/chain-config.schema.json";
  const chainTransitionSchemaPath = ".agents/skills/task-session-until-blocker/schemas/chain-transition.schema.json";
  const closeoutNoOpSchemaPath = ".agents/skills/task-session-until-blocker/schemas/closeout-no-op-proof.schema.json";
  const requestSchemaPath = ".agents/skills/task-session/schemas/mutation-admission-request.schema.json";
  const v1Units = await Promise.all(map.units.map(async (unit) => {
    const item = byUnit.get(unit.unit_id);
    const packagePath = item.package_path;
    const producerReceiptPath = rel(path.join(GENERATED, unit.unit_id, "producer-receipt.json"));
    const commands = unit.validation_commands.map((argv) => command(argv, "read-only"));
    return {
      unit_id: unit.unit_id,
      task_class: "material-mutation",
      state: "planned",
      requested_execution_mode: "reusable-mutation",
      contract_kind: "full-task",
      contract_ref: await exact(unit.task_contract),
      dependencies: unit.dependencies,
      dependency_receipts: [],
      successor: unit.successor === "__complete__" ? null : unit.successor,
      dispatch_step: `l0-${unit.unit_id.slice(-3)}`,
      material_writes: item.material_writes,
      execution_outputs: item.execution_outputs,
      allowed_writes: [...item.material_writes, ...item.execution_outputs].sort(),
      validation_commands: commands,
      attempt,
      material_package: { package_ref: await exact(packagePath), receipt_ref: await exact(producerReceiptPath) },
      terminal_receipt: rel(path.join(ONE_GO, "execution/receipts", `${unit.unit_id}.json`)),
      closeout_receipt: rel(path.join(ONE_GO, "execution/no-op", `${unit.unit_id}.json`))
    };
  }));
  const v1 = {
    schema_version: "1.0.0",
    audit_id: "augmentor-consultation-l0-v1",
    repository_root: ".",
    authority_class: "private",
    publication_class: "private",
    work_pack: await exact(workPackPath),
    control_artifacts: await Promise.all([...taskPaths, rel(path.join(ONE_GO, "material-map.json")), rel(path.join(ONE_GO, "contracts/authority-bindings.json")), terminalValidatorPath, transitionGateTestPath, approvalReceiptSchemaPath, approvedChainBuilderPath, approvedChainBuilderTestPath, chainRunnerPath, chainConfigSchemaPath, chainTransitionSchemaPath, closeoutNoOpSchemaPath].map(exact)),
    task_session_request_schema: await exact(requestSchemaPath),
    terminal_receipt_schema: await exact(terminalSchemaPath),
    terminal_receipt_semantic_validator: await exact(transitionGatePath),
    units: v1Units,
    immutable_paths: [workPackPath, ...taskPaths, rel(path.join(ONE_GO, "material-map.json"))],
    shared_write_owners: [],
    source_selectors: taskPaths,
    closeout_directory: { path: rel(path.join(ONE_GO, "execution/no-op")), create_if_missing: true },
    handoff_state: { artifact_ref: await exact(rel(path.join(ONE_GO, "handoff-state.json"))), expected_fields: { state: "audit-ready", selected_unit: null, selection_allowed: false } },
    refresh_targets: [workPackPath, ...taskPaths],
    next_owner: "invoke:refresh"
  };
  await writeJson(path.join(AUDIT, "audit-config-v1.json"), v1);

  const capsulePath = rel(path.join(ONE_GO, "contracts/authority-bindings.json"));
  const materialSchemaPath = rel(path.join(ONE_GO, "contracts/material-receipt.schema.json"));
  const closeoutContractPath = rel(path.join(ONE_GO, "contracts/closeout-owner-receipt-contract.json"));
  const expectedPath = rel(expectedReceiptsPath);
  const v2Units = await Promise.all(map.units.map(async (unit) => {
    const item = byUnit.get(unit.unit_id);
    const packagePath = item.package_path;
    const producerReceiptPath = rel(path.join(GENERATED, unit.unit_id, "producer-receipt.json"));
    const targetInventoryPath = rel(path.join(GENERATED, unit.unit_id, "target-inventory.json"));
    const baselinePath = rel(path.join(GENERATED, unit.unit_id, "byte-baseline.json"));
    const baselineRef = await exact(baselinePath);
    return {
      unit_id: unit.unit_id,
      dependencies: unit.dependencies,
      canonical_successors: [unit.successor],
      command: { argv: ["node", rel(path.join(ONE_GO, "scripts/run-unit.mjs")).slice(PACKAGE_ROOT.length + 1), "--swu", unit.unit_id], cwd: PACKAGE_ROOT, risk_class: "bounded-write" },
      material_writes: item.material_writes,
      execution_outputs: item.execution_outputs,
      allowed_writes: [...item.material_writes, ...item.execution_outputs].sort(),
      material_package: {
        package_ref: await binding(`${unit.unit_id}:package`, "augmentor-consultation-material-producer", packagePath, "/package_id"),
        producer_owner_ref: "augmentor-consultation-material-producer",
        producer_receipt_ref: await binding(`${unit.unit_id}:producer-receipt`, "augmentor-consultation-material-producer", producerReceiptPath, "/patchVerdict"),
        schema_ref: await binding(`${unit.unit_id}:material-schema`, "task-session", materialSchemaPath, "/properties"),
        declared_sha256: item.package_digest,
        target_inventory_ref: await binding(`${unit.unit_id}:target-inventory`, "augmentor-consultation-material-producer", targetInventoryPath, "/targets")
      },
      byte_baselines: [{ path: baselinePath, sha256: baselineRef.sha256 }]
    };
  }));
  const status = async (id, value, selector) => ({ value, owner_ref: "implementation-readiness", receipt_ref: await binding(id, "implementation-readiness", capsulePath, selector) });
  const v2 = {
    schema_version: "2.0.0",
    audit_id: "augmentor-consultation-l0-v2",
    repository_root: ".",
    evidence_ceiling: "frozen-input-contractual-readiness",
    classifier_version: "wpra-projection-v1",
    objective_ref: await binding("objective", "invoke-plan", capsulePath, "/objective"),
    closure_receipt_refs: [await binding("plan-status", "invoke-plan", capsulePath, "/lifecycle/plan_artifact"), await binding("refine-status", "refine", capsulePath, "/statuses/artifact_authored")],
    authority_bindings: {
      canonical_authority_refs: [
        await binding("canonical-objective", "invoke-plan", capsulePath, "/objective"),
        await binding("risk-boundary", "human-decision-gate", capsulePath, "/risk"),
        await binding("terminal-validator-core", "task-session-chain-normalizer", terminalValidatorPath),
        await binding("transition-gate-test", "task-session-chain-normalizer", transitionGateTestPath),
        await binding("approval-receipt-schema", "human-decision-gate", approvalReceiptSchemaPath),
        await binding("approved-chain-builder", "task-session-until-blocker", approvedChainBuilderPath),
        await binding("approved-chain-builder-test", "task-session-until-blocker", approvedChainBuilderTestPath),
        await binding("canonical-chain-runner", "task-session-until-blocker", chainRunnerPath),
        await binding("chain-config-schema", "task-session-until-blocker", chainConfigSchemaPath),
        await binding("chain-transition-schema", "task-session-until-blocker", chainTransitionSchemaPath),
        await binding("closeout-no-op-schema", "task-session-until-blocker", closeoutNoOpSchemaPath)
      ],
      semantic_bindings: {
        owner: await binding("semantic-owner", "implementation-readiness", capsulePath, "/owner"),
        material: await binding("semantic-material", "augmentor-consultation-material-producer", capsulePath, "/material"),
        validation: await binding("semantic-validation", "task-session", capsulePath, "/validation"),
        receipt: await binding("semantic-receipt", "task-session", capsulePath, "/receipt"),
        closeout: await binding("semantic-closeout", "invoke-refresh", capsulePath, "/closeout")
      }
    },
    execution_bindings: v2Units,
    receipt_bindings: {
      terminal_schema_ref: await binding("terminal-schema", "task-session-chain-normalizer", terminalSchemaPath, "/properties"),
      semantic_validator_ref: await binding("transition-receipt-gate", "task-session-chain-normalizer", transitionGatePath),
      expected_receipt_refs: await Promise.all(map.frontier.map((unitId, index) => binding(`expected-${unitId}`, "task-session-chain-normalizer", expectedPath, `/receipts/${index}`)))
    },
    closeout_bindings: await Promise.all(map.units.map(async (unit) => ({ unit_id: unit.unit_id, allowed_delta_policy_ref: await binding(`${unit.unit_id}:delta-policy`, "invoke-refresh", capsulePath, "/closeout"), owner_receipt_contract_ref: await binding(`${unit.unit_id}:closeout-contract`, "invoke-refresh", closeoutContractPath, "/required_inputs"), compensation: { mode: "none", rationale: "Stop and preserve validated candidate-local bytes; no automatic rollback or external effect." } }))),
    runtime_binding: { requested_task_session_execution_mode: "reusable-mutation", task_session_admission_receipt_ref: await binding("admission-summary", "task-session", rel(admissionSummaryPath), "/status") },
    status_receipt_refs: {
      artifact_authored_status: await status("artifact-authored", "authored", "/statuses/artifact_authored"),
      registry_released_status: await status("registry-released", "unreleased", "/statuses/registry_released"),
      mutation_runtime_ready_status: await status("mutation-runtime", "candidate", "/statuses/mutation_runtime_ready"),
      audit_verdict: await status("audit-verdict", "pending", "/statuses/audit_verdict")
    },
    lifecycle_status_refs: {
      plan_artifact_status: await status("lifecycle-plan", "authored", "/lifecycle/plan_artifact"),
      audit_status: await status("lifecycle-audit", "pending", "/lifecycle/audit"),
      approval_status: await status("lifecycle-approval", "unapproved", "/lifecycle/approval"),
      chain_status: await status("lifecycle-chain", "not-started", "/lifecycle/chain")
    },
    approval_policy: { approval_owner_ref: "human-decision-gate", decision_gate_receipt_ref: await binding("decision-gate", "human-decision-gate", capsulePath, "/decision"), run_budget: { max_task_session_requests: 7 }, risk_policy_ref: await binding("risk-policy", "human-decision-gate", capsulePath, "/risk"), allowed_audit_verdicts: ["pass"], allowed_flag_classes: [] },
    continuity_projection: { cursor: "l0-root", completed_unit_receipt_refs: [], joined_closeout_receipt_refs: [], projected_next_successor: { unit_id: "SWU-ACAPI-000", canonical_successor_ref: await binding("canonical-successor-root", "invoke-plan", capsulePath, "/continuity/projected_next_successor"), projection_owner_ref: "work-pack-readiness-audit", equivalence_validator_ref: await binding("equivalence-validator", "task-session-chain-normalizer", transitionGatePath), continuation_router_verification_receipt_ref: await binding("router-verification-contract", "continuation-router", closeoutContractPath, "/required_inputs"), authority_effect: "none" } },
    expected_material_digests: Object.fromEntries(summary.units.map((unit) => [unit.unit_id, unit.package_digest]))
  };
  await writeJson(path.join(AUDIT, "audit-config-v2.json"), v2);
  console.log(`AUDIT_CONFIGS=prepared v1_units=${v1Units.length} v2_units=${v2Units.length}`);
};

await build();
