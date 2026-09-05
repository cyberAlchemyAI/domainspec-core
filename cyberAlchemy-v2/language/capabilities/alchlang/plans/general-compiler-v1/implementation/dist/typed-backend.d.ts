import { type NormalizedCalculation, type NormalizedMapping, type NormalizedPolicy, type NormalizedQuery } from "./model.js";
export declare function evaluateCalculation(contract: NormalizedCalculation, inputs: Readonly<Record<string, unknown>>): bigint;
export declare function evaluateQuery(contract: NormalizedQuery, rows: readonly Readonly<Record<string, unknown>>[], inputs?: Readonly<Record<string, unknown>>): ReadonlyArray<Readonly<Record<string, unknown>>>;
export declare function evaluateMapping(contract: NormalizedMapping, source: Readonly<Record<string, unknown>>): Readonly<Record<string, unknown>>;
export declare function evaluatePolicy(contract: NormalizedPolicy, inputs: Readonly<Record<string, unknown>>): string;
