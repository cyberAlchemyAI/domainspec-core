import { type NormalizedDomain, type NormalizedRule, type SfolFormula } from "./model.js";
import { type LegacyPredicateRegistry } from "./predicate-parser.js";
export interface ActionRequest {
    action_id: string;
    actor_ref: string;
    facts: Readonly<Record<string, unknown>>;
    authority_grants: readonly string[];
}
export interface AdapterRequest extends ActionRequest {
    domain_id: string;
    authority_boundary_ref: string;
}
export interface AdapterResult {
    outcome: string;
    emitted_events?: readonly string[];
    data?: unknown;
}
export interface ActionAdapter {
    execute(request: AdapterRequest): Promise<AdapterResult>;
}
export type ActionAdapterRegistry = Readonly<Record<string, ActionAdapter>>;
export interface ActionExecutionResult {
    status: "executed";
    action_id: string;
    outcome: string;
    emitted_events: readonly string[];
    rule_results: Readonly<Record<string, boolean>>;
    permission_results: Readonly<Record<string, boolean>>;
    adapter_data?: unknown;
}
export declare function evaluateSfolFormula(expression: SfolFormula, facts: Readonly<Record<string, unknown>>): boolean;
/** @deprecated Use evaluateSfolFormula. */
export declare const evaluateExpression: typeof evaluateSfolFormula;
export declare function evaluateRule(rule: NormalizedRule, facts: Readonly<Record<string, unknown>>, legacyRegistry?: LegacyPredicateRegistry): boolean;
export declare function executeAction(model: NormalizedDomain, request: ActionRequest, adapters: ActionAdapterRegistry, legacyRegistry?: LegacyPredicateRegistry): Promise<ActionExecutionResult>;
