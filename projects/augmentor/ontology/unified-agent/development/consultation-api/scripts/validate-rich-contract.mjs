import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validate } from "./validate-contract.mjs";

const ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const loadSchema = async (name) => JSON.parse(await readFile(path.join(ROOT, "schemas", name), "utf8"));

const exactKeys = (value, required, optional = []) => {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  const allowed = new Set([...required, ...optional]);
  return required.every((key) => Object.hasOwn(value, key)) && Object.keys(value).every((key) => allowed.has(key));
};

export async function validateRichGlossary(value) {
  const schema = await loadSchema("glossary.schema.json");
  const errors = validate(value, schema);
  if (Array.isArray(value?.terms)) {
    if (new Set(value.terms.map((term) => term.id)).size !== value.terms.length) errors.push("$.terms: duplicate ids");
    if (new Set(value.terms.map((term) => term.term.toLocaleLowerCase())).size !== value.terms.length) errors.push("$.terms: duplicate labels");
  }
  return errors;
}

export async function validateRichExplanationSupport(value) {
  const schema = await loadSchema("explanation-support.schema.json");
  const errors = validate(value, schema);
  const terms = new Map((value?.glossaryEntries ?? []).map((entry) => [entry.id, entry]));
  const used = new Set();
  for (const [index, pack] of (value?.packs ?? []).entries()) {
    for (const ref of pack.glossaryRefs ?? []) {
      used.add(ref);
      if (!terms.has(ref)) errors.push(`$.packs[${index}].glossaryRefs: unknown ref ${ref}`);
    }
    if (pack.illustrativeScenario?.kind === "source-derived" && !pack.illustrativeScenario.sourceHandles?.length) {
      errors.push(`$.packs[${index}].illustrativeScenario.sourceHandles: required for source-derived example`);
    }
  }
  for (const id of terms.keys()) if (!used.has(id)) errors.push(`$.glossaryEntries: unused term ${id}`);
  return errors;
}

export function validateRichQuery(value) {
  const errors = [];
  if (!exactKeys(value, ["schemaVersion", "requestId", "questionId", "operation", "query", "scope", "limits"], ["explanation"])) {
    return ["$: rich query is not closed"];
  }
  if (value.schemaVersion !== "augmentor.consultation.query@1.1.0") errors.push("$.schemaVersion: unsupported rich query version");
  if (value.explanation !== undefined && (!exactKeys(value.explanation, ["profile"]) || !["brief", "guided", "deep"].includes(value.explanation.profile))) {
    errors.push("$.explanation: invalid closed explanation selector");
  }
  return errors;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const schema = process.argv[2];
  const target = process.argv[3];
  if (!schema || !target) throw new Error("usage: validate-rich-contract.mjs glossary|explanation-support <json-path>");
  const value = JSON.parse(await readFile(path.resolve(target), "utf8"));
  const errors = schema === "glossary"
    ? await validateRichGlossary(value)
    : schema === "explanation-support" ? await validateRichExplanationSupport(value) : ["unknown schema"];
  process.stdout.write(`${JSON.stringify({ schema, status: errors.length ? "fail" : "pass", errors }, null, 2)}\n`);
  if (errors.length) process.exitCode = 1;
}
