import { spawnSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const arg = (name) => { const index = process.argv.indexOf(name); return index >= 0 ? process.argv[index + 1] : null; };
const unit = arg("--swu");
const repositoryRoot = path.resolve(arg("--repository-root") ?? path.resolve(ONE_GO, "../../../../../../../.."));
if (!unit) throw new Error("--swu is required");
const apply = spawnSync(process.execPath, [path.join(ONE_GO, "scripts/apply-material.mjs"), "--swu", unit, "--repository-root", repositoryRoot], { cwd: repositoryRoot, encoding: "utf8", stdio: "inherit", timeout: 30000 });
if (apply.status !== 0) process.exit(apply.status ?? 1);
const packageDoc = JSON.parse(await readFile(path.join(ONE_GO, "generated", unit, "material-package.json"), "utf8"));
for (const command of packageDoc.validation_commands) {
  const argv = JSON.parse(command);
  const result = spawnSync(argv[0], argv.slice(1), { cwd: repositoryRoot, encoding: "utf8", stdio: "inherit", timeout: 30000, env: { ...process.env, NODE_ENV: "test" } });
  if (result.status !== 0) process.exit(result.status ?? 1);
}
console.log(`UNIT_VALIDATION=pass swu=${unit}`);
