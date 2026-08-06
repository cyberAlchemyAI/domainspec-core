import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));

const load = async (relative) => JSON.parse(await readFile(path.join(ROOT, relative), "utf8"));

const typeMatches = (value, type) => {
  if (Array.isArray(type)) return type.some((candidate) => typeMatches(value, candidate));
  if (type === "null") return value === null;
  if (type === "array") return Array.isArray(value);
  if (type === "object") return value !== null && typeof value === "object" && !Array.isArray(value);
  if (type === "integer") return Number.isInteger(value);
  return typeof value === type;
};

export const validate = (value, schema, at = "$", rootSchema = schema) => {
  const errors = [];
  if (schema.$ref) {
    if (!schema.$ref.startsWith("#/$defs/")) return [`${at}: unsupported ref ${schema.$ref}`];
    const target = rootSchema.$defs?.[schema.$ref.slice("#/$defs/".length)];
    return target ? validate(value, target, at, rootSchema) : [`${at}: missing ref ${schema.$ref}`];
  }
  if (schema.const !== undefined && value !== schema.const) errors.push(`${at}: must equal ${JSON.stringify(schema.const)}`);
  if (schema.enum && !schema.enum.includes(value)) errors.push(`${at}: must be one of ${schema.enum.join(", ")}`);
  if (schema.type && !typeMatches(value, schema.type)) return [...errors, `${at}: wrong type`];
  if (schema.oneOf) {
    const branches = schema.oneOf.map((branch) => validate(value, branch, at, rootSchema));
    if (branches.filter((branch) => branch.length === 0).length !== 1) errors.push(`${at}: must match exactly one variant`);
  }
  if (schema.anyOf && !schema.anyOf.some((branch) => validate(value, branch, at, rootSchema).length === 0)) errors.push(`${at}: must match at least one variant`);
  if (value !== null && typeof value === "object" && !Array.isArray(value)) {
    for (const required of schema.required ?? []) if (!(required in value)) errors.push(`${at}.${required}: required`);
    if (schema.additionalProperties === false) {
      const allowed = new Set(Object.keys(schema.properties ?? {}));
      for (const key of Object.keys(value)) if (!allowed.has(key)) errors.push(`${at}.${key}: undeclared`);
    }
    for (const [key, child] of Object.entries(schema.properties ?? {})) if (key in value) errors.push(...validate(value[key], child, `${at}.${key}`, rootSchema));
  }
  if (Array.isArray(value)) {
    if (schema.minItems !== undefined && value.length < schema.minItems) errors.push(`${at}: too few items`);
    if (schema.maxItems !== undefined && value.length > schema.maxItems) errors.push(`${at}: too many items`);
    if (schema.uniqueItems && new Set(value.map((item) => JSON.stringify(item))).size !== value.length) errors.push(`${at}: duplicate items`);
    if (schema.items) value.forEach((item, index) => errors.push(...validate(item, schema.items, `${at}[${index}]`, rootSchema)));
  }
  if (typeof value === "string") {
    if (schema.minLength !== undefined && value.length < schema.minLength) errors.push(`${at}: too short`);
    if (schema.maxLength !== undefined && value.length > schema.maxLength) errors.push(`${at}: too long`);
    if (schema.pattern && !new RegExp(schema.pattern).test(value)) errors.push(`${at}: pattern mismatch`);
  }
  if (typeof value === "number") {
    if (schema.minimum !== undefined && value < schema.minimum) errors.push(`${at}: below minimum`);
    if (schema.maximum !== undefined && value > schema.maximum) errors.push(`${at}: above maximum`);
    if (schema.minimum !== undefined && !Number.isFinite(value)) errors.push(`${at}: not finite`);
  }
  return errors;
};

const validateCases = async (scope, schemaPath, casesPath) => {
  const schema = await load(schemaPath);
  const cases = await load(casesPath);
  const failures = [];
  for (const [index, value] of cases.valid.entries()) {
    const errors = validate(value, schema);
    if (errors.length) failures.push(`${scope} valid[${index}] rejected: ${errors.join("; ")}`);
  }
  for (const [index, testCase] of cases.invalid.entries()) {
    const errors = validate(testCase.value, schema);
    if (!errors.length) failures.push(`${scope} invalid[${index}] ${testCase.name} accepted`);
  }
  return { scope, valid: cases.valid.length, invalid: cases.invalid.length, failures };
};

export const validateScope = async (scope) => {
  const contracts = {
    query: ["schemas/query.schema.json", "fixtures/query-cases.json"],
    result: ["schemas/result.schema.json", "fixtures/result-cases.json"],
    projection: ["schemas/projection.schema.json", "fixtures/projection-cases.json"]
  };
  if (!contracts[scope]) throw new Error(`unknown scope ${scope}`);
  return validateCases(scope, ...contracts[scope]);
};

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const scopeIndex = process.argv.indexOf("--scope");
  const scope = scopeIndex >= 0 ? process.argv[scopeIndex + 1] : null;
  if (!scope) throw new Error("usage: validate-contract.mjs --scope query|result|projection");
  const receipt = await validateScope(scope);
  console.log(JSON.stringify(receipt, null, 2));
  if (receipt.failures.length) process.exitCode = 1;
}
