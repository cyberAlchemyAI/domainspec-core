import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const arg = (name) => { const index = process.argv.indexOf(name); return index >= 0 ? process.argv[index + 1] : null; };
const unit = arg("--swu");
const repositoryRoot = path.resolve(arg("--repository-root") ?? path.resolve(ONE_GO, "../../../../../../../.."));
if (!unit) throw new Error("--swu is required");
const packageDoc = JSON.parse(await readFile(path.join(ONE_GO, "generated", unit, "material-package.json"), "utf8"));

for (const change of packageDoc.changes) {
  const target = path.join(repositoryRoot, change.target_path);
  let output;
  if (change.operation === "create_text") {
    try { await readFile(target); throw new Error(`create target already exists: ${change.target_path}`); }
    catch (error) { if (error.code !== "ENOENT") throw error; }
    output = change.content;
  } else if (change.operation === "replace_text") {
    const before = await readFile(target, "utf8");
    if (sha(before) !== change.before_sha256) throw new Error(`baseline mismatch: ${change.target_path}`);
    output = before;
    for (const replacement of change.replacements) {
      const count = output.split(replacement.find).length - 1;
      if (count !== 1) throw new Error(`replacement match count ${count}: ${change.target_path}`);
      output = output.replace(replacement.find, replacement.replace);
    }
  } else throw new Error(`unsupported operation ${change.operation}`);
  if (sha(output) !== change.after_sha256) throw new Error(`result digest mismatch: ${change.target_path}`);
  await mkdir(path.dirname(target), { recursive: true });
  await writeFile(target, output);
}
console.log(`MATERIAL_APPLY=pass swu=${unit} files=${packageDoc.changes.length}`);
