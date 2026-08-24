import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";

const terminalPath =
  "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/work-pack/closeout/SWU-BWAA-001.receipt.json";
const ownerPath =
  "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T164538Z-swu-bwaa-001-closeout/CLOSEOUT-OWNER-RECEIPT.json";
const workPackPath =
  "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/WORK-PACK.md";
const continuationPath =
  "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/CONTINUATION.json";

const requiredTerminalFields = [
  "swu_id",
  "result",
  "capability_ref",
  "receipt_kind",
  "timestamp",
  "control_digests",
  "semantic_lock_results",
  "target_inventory",
  "files_touched",
  "validation",
  "blockers",
  "residue",
  "reroute",
  "handoff_note",
  "successor",
  "authority_effect",
  "release_admission",
];

const sha256 = (value) =>
  createHash("sha256").update(value).digest("hex");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const terminalBytes = await readFile(terminalPath);
const ownerBytes = await readFile(ownerPath);
const workPack = await readFile(workPackPath, "utf8");
const continuation = JSON.parse(await readFile(continuationPath, "utf8"));
const terminal = JSON.parse(terminalBytes);
const owner = JSON.parse(ownerBytes);
const terminalDigest = sha256(terminalBytes);

for (const field of requiredTerminalFields) {
  assert(Object.hasOwn(terminal, field), `terminal receipt missing ${field}`);
}
assert(terminal.swu_id === "SWU-BWAA-001", "terminal SWU mismatch");
assert(terminal.result === "pass", "terminal result is not pass");
assert(terminal.successor === "SWU-BWAA-002", "terminal successor mismatch");
assert(terminal.authority_effect === "none", "terminal changed authority");
assert(
  terminal.release_admission === "not-granted",
  "terminal granted release",
);

assert(
  owner.schema_version === "body-war.invoke-closeout-owner-receipt.v1",
  "owner receipt schema mismatch",
);
assert(owner.owner?.capability === "invoke", "owner capability mismatch");
assert(owner.owner?.mode === "refresh", "owner mode mismatch");
assert(
  owner.owner?.mutation_mode === "apply-approved",
  "owner mutation mode mismatch",
);
assert(owner.result === "pass", "owner receipt result is not pass");
assert(
  owner.source_terminal_receipt?.path === terminalPath,
  "owner source terminal path mismatch",
);
assert(
  owner.source_terminal_receipt?.sha256 === terminalDigest,
  "owner source terminal digest mismatch",
);
assert(
  owner.preserved_terminal_receipt?.path === terminalPath &&
    owner.preserved_terminal_receipt?.sha256 === terminalDigest,
  "terminal receipt was not preserved",
);
assert(
  owner.returned_successor === "SWU-BWAA-002",
  "owner successor mismatch",
);
assert(owner.authority_effect === "none", "owner changed authority");
assert(owner.release_admission === "not-granted", "owner granted release");

const appliedPaths = owner.applied_targets
  .map((item) => item.path)
  .sort();
assert(
  JSON.stringify(appliedPaths) ===
    JSON.stringify([continuationPath, workPackPath].sort()),
  "owner applied target inventory mismatch",
);
assert(
  owner.validation.every((item) => item.result === "pass"),
  "owner validation contains a failure",
);

assert(
  workPack.includes(
    "| [TASK-BWAA-001](work-pack/tasks/TASK-BWAA-001.md) | `SWU-BWAA-001` | L0 | completed |",
  ),
  "Work Pack did not mark SWU-BWAA-001 completed",
);
assert(
  workPack.includes(
    "| [TASK-BWAA-002](work-pack/tasks/TASK-BWAA-002.md) | `SWU-BWAA-002` | L1 | dependency-ready, unselected |",
  ),
  "Work Pack did not expose SWU-BWAA-002 as the unique ready successor",
);
assert(
  continuation.state === "series-continuation-ready",
  "Continuation state mismatch",
);
assert(
  continuation.selected_swu === null &&
    continuation.first_selectable_swu === "SWU-BWAA-002",
  "Continuation selected or lost the unique successor",
);
assert(
  continuation.last_completed_swu === "SWU-BWAA-001",
  "Continuation last completed SWU mismatch",
);
assert(
  continuation.next_route === "task-session:execute:SWU-BWAA-002",
  "Continuation next route mismatch",
);

process.stdout.write(
  "SWU-BWAA-001 closeout pass: terminal and Invoke owner receipts joined; successor SWU-BWAA-002 returned without execution\n",
);
