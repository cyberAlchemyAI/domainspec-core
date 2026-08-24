import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";

const targetRoot = process.argv[2];
if (!targetRoot) {
  throw new Error("usage: test-runtime-selection.mjs <target-root>");
}

const planRoot = path.join(
  targetRoot,
  "development/arcanum-addon/plan"
);
const validator = path.join(
  planRoot,
  "work-pack/shared/validate-swu-selection-reentry.mjs"
);
const digest = (bytes) =>
  crypto.createHash("sha256").update(bytes).digest("hex");

function walk(root) {
  const files = [];
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const candidate = path.join(root, entry.name);
    if (entry.isDirectory()) files.push(...walk(candidate));
    if (entry.isFile()) files.push(candidate);
  }
  return files;
}

const addonRoot = path.join(targetRoot, "development/arcanum-addon");
const corpusFiles = ["define", "design", "plan"]
  .flatMap((segment) => walk(path.join(addonRoot, segment)))
  .sort();
const checksumStream = corpusFiles
  .map((file) => `${digest(fs.readFileSync(file))}  ${file}\n`)
  .join("");
const current = {
  dispatch_sha256: digest(fs.readFileSync(path.join(planRoot, "DISPATCH.json"))),
  plan_corpus_sha256: digest(checksumStream),
  work_pack_sha256: digest(
    fs.readFileSync(path.join(planRoot, "WORK-PACK.md"))
  ),
  source_commit: execFileSync("git", ["-C", targetRoot, "rev-parse", "HEAD"], {
    encoding: "utf8"
  }).trim()
};

const temporary = fs.mkdtempSync(
  path.join(os.tmpdir(), "arcanum-selection-runtime-")
);
try {
  const receiptRoot = temporary;
  const sessionId = "runtime-selection-test-session";
  const runId = "runtime-selection-test-run";
  const selectionPath = path.join(
    receiptRoot,
    `receipts/selections/${sessionId}/SWU-ARC-GOV-001.json`
  );
  fs.mkdirSync(path.dirname(selectionPath), { recursive: true });
  const receipt = {
    schema_version: "arcanum-addon.swu-selection.v1",
    status: "selected",
    selection_id: sessionId,
    operator_confirmation_handle: "test-confirmation",
    issuing_owner: "runtime-test",
    issued_at: "2026-07-30T12:00:00Z",
    expires_at: "2026-07-30T14:00:00Z",
    session_id: sessionId,
    run_id: runId,
    dispatch_id: "arcanum-addon-implementation-route-v3",
    ...current,
    selected_swu_id: "SWU-ARC-GOV-001",
    selected_step_id: "s00-gov-001",
    dependency_receipts: [],
    previous_closeout_sync: null,
    single_use_claim_key: `${sessionId}:SWU-ARC-GOV-001`
  };
  fs.writeFileSync(selectionPath, `${JSON.stringify(receipt, null, 2)}\n`);

  const commonArgs = [
    validator,
    planRoot,
    "--selection",
    selectionPath,
    "--session-id",
    sessionId,
    "--run-id",
    runId,
    "--dispatch-sha256",
    current.dispatch_sha256,
    "--plan-corpus-sha256",
    current.plan_corpus_sha256,
    "--work-pack-sha256",
    current.work_pack_sha256,
    "--source-commit",
    current.source_commit,
    "--receipt-root",
    receiptRoot,
    "--claim-dir",
    path.join(temporary, "claims"),
    "--now",
    "2026-07-30T13:00:00Z"
  ];

  const first = spawnSync(process.execPath, commonArgs, { encoding: "utf8" });
  assert.equal(first.status, 0, first.stderr);
  assert.equal(JSON.parse(first.stdout).admission, "ready-after-atomic-claim");

  const replay = spawnSync(process.execPath, commonArgs, { encoding: "utf8" });
  assert.equal(replay.status, 1, replay.stdout);
  assert(
    JSON.parse(replay.stderr).errors.includes(
      "single-use claim already consumed"
    )
  );

  const mismatchPath = path.join(
    receiptRoot,
    `receipts/selections/${sessionId}/SWU-ARC-BOOT-001.json`
  );
  fs.writeFileSync(mismatchPath, `${JSON.stringify(receipt, null, 2)}\n`);
  const mismatchArgs = [...commonArgs];
  mismatchArgs[mismatchArgs.indexOf(selectionPath)] = mismatchPath;
  mismatchArgs[mismatchArgs.indexOf(path.join(temporary, "claims"))] =
    path.join(temporary, "mismatch-claims");
  const mismatch = spawnSync(process.execPath, mismatchArgs, {
    encoding: "utf8"
  });
  assert.equal(mismatch.status, 1, mismatch.stdout);
  assert(
    JSON.parse(mismatch.stderr).errors.some((item) =>
      item.includes("receipt path")
    )
  );

  process.stdout.write(
    `PASS: live validator accepted one exact selection, atomically blocked replay, and rejected path/content mismatch over corpus ${current.plan_corpus_sha256}\n`
  );
} finally {
  fs.rmSync(temporary, { recursive: true, force: true });
}
