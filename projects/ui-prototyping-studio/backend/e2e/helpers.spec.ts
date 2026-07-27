import { expect, test } from "@playwright/test";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { cli, newDataDir, startPreview } from "./helpers";

test("CLI failures retain local command and separate process diagnostics", () => {
  const result = cli(["state", "missing-session"], newDataDir());

  expect(result.code).not.toBe(0);
  expect(result.command).toContain(join("node_modules", ".bin", "tsx"));
  expect(result.args.at(-2)).toBe("state");
  expect(result.args.at(-1)).toBe("missing-session");
  expect(result.signal).toBeNull();
  expect(typeof result.rawStdout).toBe("string");
  expect(typeof result.stderr).toBe("string");
  expect(`${result.stdout}\n${result.stderr}`).toMatch(/SESSION_NOT_FOUND|not found/i);
});

test("preview rejects promptly when its child exits before readiness", async () => {
  const missingEntry = join(
    dirname(fileURLToPath(import.meta.url)),
    "fixtures",
    "missing-preview-entry.ts",
  );
  const startedAt = Date.now();

  await expect(startPreview(
    "session-for-exit-witness",
    newDataDir(),
    { cliPath: missingEntry, startupTimeoutMs: 5_000 },
  )).rejects.toThrow(/preview exited before readiness[\s\S]*command:[\s\S]*exit code:/);
  expect(Date.now() - startedAt).toBeLessThan(5_000);
});
