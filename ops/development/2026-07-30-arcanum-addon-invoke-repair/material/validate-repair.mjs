import fs from "node:fs";
import path from "node:path";

const root = process.argv[2];
if (!root) {
  throw new Error("artifact root required");
}

const failures = [];
const dispatchPath = path.join(
  root,
  "development/arcanum-addon/plan/DISPATCH.json"
);
const validationPath = path.join(
  root,
  "development/arcanum-addon/design/VALIDATION-CONTRACTS.md"
);
const task4Path = path.join(
  root,
  "development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md"
);
const closeoutPath = path.join(
  root,
  "development/arcanum-addon/plan/work-pack/shared/CLOSEOUT-SYNC.md"
);
const workPackPath = path.join(
  root,
  "development/arcanum-addon/plan/WORK-PACK.md"
);

const dispatchBytes = fs.readFileSync(dispatchPath, "utf8");
const dispatch = JSON.parse(dispatchBytes);
const validation = fs.readFileSync(validationPath, "utf8");
const task4 = fs.readFileSync(task4Path, "utf8");
const closeout = fs.readFileSync(closeoutPath, "utf8");
const workPack = fs.readFileSync(workPackPath, "utf8");

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

const produced = new Map();
for (const step of dispatch.steps) {
  for (const output of step.outputs ?? []) {
    if (output.kind !== "receipt") continue;
    const match = /^receipts\/(.+)\.json$/.exec(output.ref);
    if (!match) continue;
    const producers = produced.get(match[1]) ?? [];
    producers.push(step.step_id);
    produced.set(match[1], producers);
  }
}

for (const swu of requiredSwus) {
  const producers = produced.get(swu) ?? [];
  if (producers.length !== 1) {
    failures.push(`${swu} producer count ${producers.length}`);
  }
}

if (/L[0-3]-selected-swu/.test(dispatchBytes)) {
  failures.push("generic selected-SWU receipt survives");
}

const stepById = new Map(dispatch.steps.map((step) => [step.step_id, step]));
const uninstall = stepById.get("s25-uninstall-001");
const rollback = stepById.get("s26-rollback-001");
if (
  JSON.stringify(uninstall?.depends_on_steps) !==
    JSON.stringify(["s24-disable-001"]) ||
  JSON.stringify(rollback?.depends_on_steps) !==
    JSON.stringify(["s24-disable-001"])
) {
  failures.push("uninstall and rollback are not sibling dependencies of DISABLE");
}

const waveOutputs = [
  "W0-COMPLETE",
  "W1-COMPLETE",
  "W2-COMPLETE",
  "W3-COMPLETE",
  "W4-LIFECYCLE-JOIN",
  "W4-COMPLETE"
];
for (const id of waveOutputs) {
  if ((produced.get(id) ?? []).length !== 1) {
    failures.push(`${id} join producer missing or duplicated`);
  }
}

const verify = stepById.get("s31-verify-001");
const verifyInputs = new Set((verify?.inputs ?? []).map((item) => item.ref));
for (const wave of ["W0", "W1", "W2", "W3", "W4"]) {
  if (!verifyInputs.has(`receipts/${wave}-COMPLETE.json`)) {
    failures.push(`VERIFY-001 missing ${wave}-COMPLETE input`);
  }
}

const reentry = dispatch.gates.find(
  (gate) => gate.gate_id === "g-swu-reentry"
);
if (!reentry) {
  failures.push("g-swu-reentry missing");
}
for (const step of dispatch.steps) {
  const exactReceipt = (step.outputs ?? []).some(
    (output) =>
      output.kind === "receipt" &&
      requiredSwus.some((swu) => output.ref === `receipts/${swu}.json`)
  );
  if (
    exactReceipt &&
    !(step.stop_conditions ?? []).some((condition) =>
      condition.includes("g-swu-reentry")
    )
  ) {
    failures.push(`${step.step_id} missing explicit re-entry stop`);
  }
}

for (const id of [
  "V-DEGRADATION-BASELINE",
  "V-DISABLED-LIFECYCLE-BRANCHES",
  "V-SECURITY-LIFECYCLE-JOIN"
]) {
  for (const [label, content] of [
    ["validation", validation],
    ["task4", task4],
    ["closeout", closeout]
  ]) {
    if (!content.includes(id)) {
      failures.push(`${label} missing ${id}`);
    }
  }
}

if (!workPack.includes("| selectedSWU | none |")) {
  failures.push("selectedSWU is not none");
}
if (!workPack.includes("| workPackGateStatus | block |")) {
  failures.push("work pack gate is not block");
}

if (failures.length) {
  for (const failure of failures) {
    process.stderr.write(`FAIL: ${failure}\n`);
  }
  process.exit(1);
}

process.stdout.write(
  `PASS: ${requiredSwus.length} exact SWU producers, wave joins, typed lifecycle bindings, selectedSWU none\n`
);
