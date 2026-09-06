import { type NormalizedDomain, type NormalizedFact, type SfolUInt64Term, type SfolFormula } from "./model.js";
export declare const DOMAINSPEC_PROFILE = "domainspec-1.0.0";
export declare const EXACT_PROFILE = "domainspec-1.0.0-exact-uint64-v1";
export declare const EXACT_REALIZATION = "domainspec.typescript-exact-uint64/v1";
export interface DeclarationBinding {
    ontology: string;
    meaning: string;
    identity?: string;
    invariants?: string[];
    properties?: Record<string, {
        ontology: string;
        meaning: string;
    }>;
}
export interface DomainSpecBindings {
    schema_version: "alchlang.domainspec-bindings/v1";
    profile: string;
    source_sha256: string;
    owner: string;
    declarations: Record<string, DeclarationBinding>;
}
export declare const digest: (bytes: string | Buffer) => string;
export declare const json: (value: unknown) => string;
export declare function reject(code: string, where: string, message: string): never;
export declare function symbol(id: string, separator?: string): string;
export declare function fields(model: NormalizedDomain, id: string): NormalizedFact[];
export declare const scalar: (type: string, exact?: boolean) => "String" | "Bool" | "UInt64";
export declare function references(e: SfolFormula): string[];
export declare function predicate(e: SfolFormula, facts: Map<string, NormalizedFact>, rule?: boolean, exact?: boolean, rowFields?: Set<string>): any;
export declare function validateProfile(model: NormalizedDomain, raw: unknown, source: string): DomainSpecBindings;
export declare function numericExpression(e: SfolUInt64Term): any;
