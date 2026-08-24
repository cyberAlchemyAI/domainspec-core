import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const targets = [
  "fixtures/generated/projection.json",
  "fixtures/generated/projection-manifest.json",
  "generated/consumer/projection.json",
  "generated/consumer/glossary.json",
  "generated/consumer/projection-manifest.json",
  "generated/consumer/schemas/projection.schema.json",
  "generated/consumer/schemas/projection-manifest.schema.json",
  "generated/consumer/schemas/glossary.schema.json",
  "generated/consumer/schemas/explanation-support.schema.json",
];
const forbidden = [
  /\/home\//i,
  /workspace-resonant/i,
  /cyberalchemy/i,
  /authority_effect/i,
  /internal_note/i,
  /private_id/i,
  /secret|password|bearer\s+/i
];

export const findLeakage = async () => {
  const hits = [];
  for (const target of targets) {
    const text = await readFile(path.join(ROOT, target), "utf8");
    for (const pattern of forbidden) if (pattern.test(text)) hits.push({ target, pattern: String(pattern) });
  }
  return hits;
};

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const hits = await findLeakage();
  console.log(JSON.stringify({ status: hits.length ? "fail" : "pass", hits }, null, 2));
  if (hits.length) process.exitCode = 1;
}
