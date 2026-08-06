import { execFileSync } from "node:child_process";
import { cp, mkdir, mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const PACKAGE_ROOT = path.resolve(ONE_GO, "../../../..");
const REPO = path.resolve(ONE_GO, "../../../../../../../..");
const map = JSON.parse(await readFile(path.join(ONE_GO, "material-map.json"), "utf8"));
const sources = JSON.parse(await readFile(path.join(PACKAGE_ROOT, "sources.json"), "utf8"));
const container = await mkdtemp(path.join(os.tmpdir(), "augmentor-consultation-l0-"));
const tempRepo = path.join(container, "domainspec-core");
const tempPackage = path.join(tempRepo, "projects/augmentor/ontology/unified-agent");

try {
  await mkdir(path.dirname(tempPackage), { recursive: true });
  await cp(PACKAGE_ROOT, tempPackage, { recursive: true, preserveTimestamps: true });
  for (const source of sources.sources) {
    const repository = sources.repository_roots[source.repository];
    if (!repository) throw new Error(`unknown repository ${source.repository}`);
    const original = path.resolve(REPO, repository.path, source.path);
    const target = path.resolve(tempRepo, repository.path, source.path);
    if (!target.startsWith(container + path.sep)) throw new Error(`temporary source escapes test container: ${source.path}`);
    await mkdir(path.dirname(target), { recursive: true });
    await cp(original, target, { preserveTimestamps: true });
  }
  const runUnit = path.join(tempPackage, "development/refinement-runs/20260803T180648Z-agent-consultation-api/one-go/scripts/run-unit.mjs");
  for (const unit of map.frontier) {
    execFileSync(process.execPath, [runUnit, "--swu", unit, "--repository-root", tempRepo], { cwd: tempRepo, stdio: "inherit", timeout: 60000, env: { ...process.env, NODE_ENV: "test" } });
  }
  console.log(JSON.stringify({ schema_version: "augmentor.consultation.staged-validation@0.1.0", status: "pass", frontier: map.frontier, units_executed: map.frontier.length, target: "isolated-temporary-repository", product_writes: false }, null, 2));
} finally {
  await rm(container, { recursive: true, force: true });
}
