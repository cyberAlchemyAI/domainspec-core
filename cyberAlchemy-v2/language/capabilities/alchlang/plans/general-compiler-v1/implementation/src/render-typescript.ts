import type { CompilationPlan, NormalizedFact } from "./model.js";
import { requireGeneratablePattern } from "./pattern-registry.js";
import { renderSqliteTransactionalOutbox } from "./sqlite-outbox-generator.js";

const identifier = (value: string): string => value.replace(/[^A-Za-z0-9_$]/g, "_").replace(/^[^A-Za-z_$]/, "_$&");
const pascal = (value: string): string => identifier(value).split("_").filter(Boolean).map((part) => part[0].toUpperCase() + part.slice(1)).join("") || "Anonymous";
const tsType = (fact: NormalizedFact): string => ({ integer: "number", decimal: "number", boolean: "boolean", list: "readonly unknown[]", record: "Readonly<Record<string, unknown>>" } as Record<string, string>)[fact.type] ?? "string";
const json = (value: unknown): string => JSON.stringify(value, null, 2) + "\n";
const literal = (value: unknown): string => JSON.stringify(value, null, 2) + " as const;\n";

export function renderTypeScript(plan: CompilationPlan): Record<string, string> {
  const types = plan.type_model.map((type) => `export interface ${pascal(type.id)} {\n${type.fields.map((field) => `  ${JSON.stringify(field.id)}${field.required ? "" : "?"}: ${tsType(field)};`).join("\n")}\n}`).join("\n\n") + "\n";
  const ports = plan.action_ports.map((action) => {
    const name = pascal(action.id);
    return `export interface ${name}Request { readonly facts: Readonly<Record<string, unknown>>; }\nexport interface ${name}Result { readonly outcome: string; readonly emittedEvents: readonly string[]; }\nexport interface ${name}Port { execute(request: ${name}Request): Promise<${name}Result>; }`;
  }).join("\n\n") + "\n";
  const base = {
    "domain.types.ts": types,
    "domain.schema.ts": `export const factModel = ${literal(plan.type_model)}`,
    "domain.machine.ts": `export const stateMachines = ${literal(plan.state_machines)}`,
    "domain.events.ts": `export const eventContracts = ${literal(plan.event_contracts)}`,
    "domain.tools.ts": ports,
    "domain.test-obligations.json": json(plan.test_obligations),
    "domain.graph.json": json(plan.graph_model),
    "traceability.json": json(plan.trace_ledger),
    "unsupported-residue.json": json(plan.unsupported_residue),
  };
  if (!plan.effect_contracts.length) return base;
  const effectFiles: Record<string, string> = { "domain.effects.ts": `export const effectContracts = ${literal(plan.effect_contracts)}` };
  for (const effect of plan.effect_contracts) {
    const pattern = requireGeneratablePattern(effect.pattern_ref);
    if (pattern.integration_binding.id !== effect.integration_binding_ref) throw new Error(`EFFECT_BINDING_NOT_AVAILABLE:${effect.id}:${effect.integration_binding_ref}`);
    if (effect.pattern_ref === "transactional-outbox") Object.assign(effectFiles, renderSqliteTransactionalOutbox(effect));
    else throw new Error(`EFFECT_GENERATOR_NOT_IMPLEMENTED:${effect.pattern_ref}`);
  }
  return { ...base, ...effectFiles };
}
