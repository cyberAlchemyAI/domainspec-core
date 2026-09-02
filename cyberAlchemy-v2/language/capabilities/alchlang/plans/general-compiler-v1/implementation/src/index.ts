import { createHash } from "node:crypto";
import type { CompilationResult } from "./model.js";
import { validateAndNormalize } from "./validate.js";
import { lower } from "./lower.js";
import { renderTypeScript } from "./render-typescript.js";

function canonical(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") return `{${Object.entries(value as Record<string, unknown>).sort(([a], [b]) => a.localeCompare(b)).map(([key, item]) => `${JSON.stringify(key)}:${canonical(item)}`).join(",")}}`;
  return JSON.stringify(value);
}

const digest = (value: unknown): string => createHash("sha256").update(canonical(value)).digest("hex");

export function compileCarrier(input: unknown): CompilationResult {
  const model = validateAndNormalize(input);
  const plan = lower(model);
  return { plan, files: renderTypeScript(plan), source_digest: digest(input), plan_digest: digest(plan), authority_effect: "none" };
}

export { CompilationRejected } from "./model.js";
export { parseDomainSource } from "./parser.js";
export { parsePredicate, translateLegacyPredicate } from "./predicate-parser.js";
export { evaluateExpression, evaluateRule, executeAction } from "./runtime.js";
export { FetchHttpTransport, HttpActionAdapter, MemoryActionAdapter, SqliteActionAdapter } from "./adapters.js";
export { writeCompilation } from "./writer.js";
export { deriveAvailability, listOperationPatterns, operationPatterns, requireGeneratablePattern } from "./pattern-registry.js";
export { renderSqliteTransactionalOutbox } from "./sqlite-outbox-generator.js";
export { compileOperationPatternRegistry, compileRegistryConfig, writeRegistryCompilation } from "./registry-compiler.js";
export type { CompilationPlan, CompilationResult, CompilerIssue, NormalizedDomain } from "./model.js";
export type { ActionAdapter, ActionAdapterRegistry, ActionExecutionResult, ActionRequest } from "./runtime.js";
export type { OperationPattern, PatternAvailability, PrerequisiteStatus } from "./pattern-registry.js";
