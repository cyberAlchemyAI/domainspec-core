import { execFile } from "node:child_process";
import { access, readFile, realpath } from "node:fs/promises";
import { delimiter, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

import type { LockedFactoryToolV1 } from "../contracts/factory-run-lock-v1.js";
import { fail, sha256 } from "../shared/canonical.js";

const here = dirname(fileURLToPath(import.meta.url));
const implementationRoot = resolve(here, "../../..");
const execute = promisify(execFile);

export const resolveFactoryExecutablePath = async (toolId: string): Promise<string> => {
  const executableName = toolId === "python" ? "python3" : toolId;
  for (const directory of (process.env.PATH ?? "").split(delimiter)) {
    if (directory.length === 0) continue;
    const candidate = resolve(directory, executableName);
    try {
      await access(candidate);
      return candidate;
    } catch {
      // Continue through the explicit PATH search.
    }
  }
  return fail("FACTORY_TOOL_MISSING", toolId);
};

const executableTool = async (toolId: "python" | "cargo" | "rustc") => {
  const executable = await resolveFactoryExecutablePath(toolId);
  const { stdout, stderr } = await execute(executable, ["--version"], {
    env: {},
    timeout: 10_000,
  }).catch(() => fail("FACTORY_TOOL_INVALID", toolId));
  const version = `${stdout}${stderr}`.trim();
  if (version.length === 0) fail("FACTORY_TOOL_INVALID", toolId);
  return Object.freeze({
    tool_id: toolId,
    version,
    executable_sha256: sha256(await readFile(await realpath(executable))),
  });
};

const packageTool = async (toolId: "tsx" | "typescript"): Promise<LockedFactoryToolV1> => {
  const path = resolve(implementationRoot, `node_modules/${toolId}/package.json`);
  let bytes: Buffer;
  try {
    bytes = await readFile(await realpath(path));
  } catch {
    return fail("FACTORY_TOOL_MISSING", toolId);
  }
  const parsed = JSON.parse(bytes.toString("utf8")) as { version?: unknown };
  const version = typeof parsed.version === "string"
    ? parsed.version : fail("FACTORY_TOOL_INVALID", toolId);
  return Object.freeze({
    tool_id: toolId,
    version,
    executable_sha256: sha256(bytes),
  });
};

export const resolveFactoryToolV1 = async (toolId: string): Promise<LockedFactoryToolV1> => {
  if (toolId === "node") {
    const executable = await realpath(process.execPath);
    return Object.freeze({
      tool_id: "node",
      version: process.version,
      executable_sha256: sha256(await readFile(executable)),
    });
  }
  if (toolId === "tsx" || toolId === "typescript") return packageTool(toolId);
  if (toolId === "python" || toolId === "cargo" || toolId === "rustc") {
    return executableTool(toolId);
  }
  return fail("FACTORY_TOOL_UNKNOWN", toolId);
};
