import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  mkdtempSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { createFileBackedStudioSessionStore } from "./file-studio-session-store.js";

const BACKEND_DIR = resolve(
  dirname(fileURLToPath(import.meta.url)),
  "../../../..",
);
const TSX_PATH = join(
  BACKEND_DIR,
  "node_modules",
  ".bin",
  process.platform === "win32" ? "tsx.cmd" : "tsx",
);
const CLI_PATH = join(BACKEND_DIR, "src", "cli", "studio.ts");

function runCli(args: string[], dataFile: string): unknown {
  const result = spawnSync(TSX_PATH, [CLI_PATH, ...args], {
    cwd: BACKEND_DIR,
    env: {
      ...process.env,
      STUDIO_DATA: dataFile,
      STUDIO_ACTOR: "agent:freshness-witness",
    },
    encoding: "utf8",
  });
  assert.equal(
    result.status,
    0,
    `CLI failed: ${JSON.stringify([TSX_PATH, CLI_PATH, ...args])}\nstdout:\n${result.stdout}\nstderr:\n${result.stderr}`,
  );
  return JSON.parse(result.stdout);
}

test("an existing reader observes child-process stage, Accept, and Revert", () => {
  const dir = mkdtempSync(join(tmpdir(), "ups-freshness-process-"));
  const file = join(dir, "studio.json");
  const reader = createFileBackedStudioSessionStore({ filePath: file });
  try {
    const opened = runCli(["session", "open", "--variants", "1"], file) as {
      sessionId: string;
    };
    const sid = opened.sessionId;
    assert.equal(reader.getSession(sid)?.state, "SessionInitialized");

    runCli(["prompt", "submit", sid, "freshness"], file);
    runCli([
      "variants",
      "register",
      sid,
      "--label",
      "A",
      "--file",
      "e2e/fixtures/base.html",
    ], file);
    runCli(["baseline", "select", sid, "A"], file);
    runCli([
      "comment",
      "add",
      sid,
      "--od-id",
      "cta.primary",
      "--selector",
      "[data-od-id=cta.primary]",
      "--label",
      "Primary button",
      "--intent",
      "reword",
      "--note",
      "say Continue",
    ], file);
    const synthesized = runCli(["synthesize", sid], file) as {
      batch: { batchId: string };
    };
    runCli(["batch", "approve", sid, synthesized.batch.batchId], file);
    runCli([
      "apply",
      sid,
      synthesized.batch.batchId,
      "--candidate-from",
      "e2e/fixtures/continue.html",
    ], file);

    assert.equal(reader.getSession(sid)?.state, "RevisionApplied");
    assert.ok(reader.getStagedCandidate(sid));

    runCli(["accept", sid], file);
    const acceptedHead = reader.getSession(sid)?.revisionHeadId;
    assert.equal(reader.getSession(sid)?.state, "RevisionRecorded");
    assert.equal(reader.getStagedCandidate(sid), null);
    assert.equal(reader.listRevisions(sid).length, 1);

    runCli(["revert", sid], file);
    assert.equal(reader.getSession(sid)?.state, "RevisionRecorded");
    assert.notEqual(reader.getSession(sid)?.revisionHeadId, acceptedHead);
    assert.equal(reader.listRevisions(sid).length, 2);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("two store instances allocate from fresh sequential counters", () => {
  const dir = mkdtempSync(join(tmpdir(), "ups-freshness-counters-"));
  const file = join(dir, "studio.json");
  try {
    const first = createFileBackedStudioSessionStore({ filePath: file });
    const second = createFileBackedStudioSessionStore({ filePath: file });
    assert.equal(first.allocateSessionId(), "ups-session-0001");
    assert.equal(second.allocateSessionId(), "ups-session-0002");
    assert.equal(first.allocateSessionId(), "ups-session-0003");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("post-construction corruption and concurrent lock both fail closed", () => {
  const dir = mkdtempSync(join(tmpdir(), "ups-freshness-fail-closed-"));
  const file = join(dir, "studio.json");
  try {
    const reader = createFileBackedStudioSessionStore({ filePath: file });
    reader.allocateSessionId();
    writeFileSync(file, "{ corrupt external bytes", "utf8");
    assert.throws(
      () => reader.getSession("any"),
      /not valid JSON|data-loss guard/i,
    );

    rmSync(file, { force: true });
    const writer = createFileBackedStudioSessionStore({ filePath: file });
    writeFileSync(`${file}.lock`, "external writer", "utf8");
    assert.throws(
      () => writer.allocateSessionId(),
      /locked by another writer|Refusing to overwrite concurrent state/i,
    );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
