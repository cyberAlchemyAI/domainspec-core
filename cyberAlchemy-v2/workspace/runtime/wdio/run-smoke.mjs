import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const testDirectory = mkdtempSync(join(tmpdir(), "cav2-essays-wdio-"));
const database = join(testDirectory, "essays.sqlite");
const artifactDirectory = process.env.WORKSPACE_WDIO_OUTPUT ?? join(testDirectory, "artifacts");
const wdio = resolve("node_modules/.bin/wdio");
mkdirSync(artifactDirectory, { recursive: true });

try {
  const result = spawnSync(wdio, ["run", "./wdio/wdio.conf.mjs"], {
    cwd: process.cwd(),
    env: {
      ...process.env,
      ESSAYS_DATABASE: database,
      WORKSPACE_WDIO_OUTPUT: artifactDirectory,
      WDIO_USE_NATIVE_FETCH: "1",
    },
    stdio: "inherit",
  });

  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    process.stderr.write(
      `${JSON.stringify({
        status: "FAIL",
        check: "unified-workspace-tauri-wdio-smoke",
        code: "WDIO_SMOKE_FAILED",
        exitCode: result.status,
        authorityEffect: "none",
      })}\n`,
    );
    process.exitCode = result.status ?? 1;
  } else {
    process.stdout.write(
      `${JSON.stringify({
        status: "PASS",
        check: "unified-workspace-tauri-wdio-smoke",
        databasePosture: "temporary-and-removed",
        authorityEffect: "none",
        claimCeiling: "Local candidate desktop smoke evidence only.",
      })}\n`,
    );
  }
} finally {
  rmSync(testDirectory, { recursive: true, force: true });
}
