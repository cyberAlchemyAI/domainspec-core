import type { OperationPattern, PatternAvailability } from "./registry-compiler.js";
export type { OperationPattern, PatternAvailability, PrerequisiteStatus } from "./registry-compiler.js";
export declare const operationPatterns: readonly OperationPattern[];
export declare function deriveAvailability(pattern: OperationPattern): PatternAvailability;
export declare function listOperationPatterns(filter?: PatternAvailability | "all"): readonly OperationPattern[];
export declare function requireGeneratablePattern(patternId: string): OperationPattern;
