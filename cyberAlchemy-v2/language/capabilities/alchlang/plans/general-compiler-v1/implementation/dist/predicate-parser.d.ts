import { type ScalarType, type SfolFormula } from "./model.js";
export declare function parseSfolFormula(source: string, facts: ReadonlyMap<string, ScalarType>): SfolFormula;
/** @deprecated Use parseSfolFormula. */
export declare const parsePredicate: typeof parseSfolFormula;
export type LegacyPredicateRegistry = Readonly<Record<string, SfolFormula>>;
export declare function translateLegacyPredicate(predicateId: string, registry: LegacyPredicateRegistry): SfolFormula;
