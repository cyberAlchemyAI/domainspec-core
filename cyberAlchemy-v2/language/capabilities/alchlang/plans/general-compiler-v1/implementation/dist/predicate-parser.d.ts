import { type Expression, type ScalarType } from "./model.js";
export declare function parsePredicate(source: string, facts: ReadonlyMap<string, ScalarType>): Expression;
export type LegacyPredicateRegistry = Readonly<Record<string, Expression>>;
export declare function translateLegacyPredicate(predicateId: string, registry: LegacyPredicateRegistry): Expression;
