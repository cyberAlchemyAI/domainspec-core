import { type ModuleTree } from './module-source.js';
export declare function inspectFunctionOntology(sourcePath: string, selector?: string): Promise<{
    module_imports?: {
        [k: string]: {
            source_sha256: any;
            input: any;
            output: any;
        };
    } | undefined;
    schema_version: string;
    domain: string;
    source: {
        path: string;
        sha256: string;
    };
    nodes: {
        id: string;
        name: string;
        kind: string;
        meta_type: string | null;
        stable_key: string;
        key_origin: "authored" | "derived";
        identity_origin: "authored" | "derived";
        meaning: {
            text: string;
            origin: "authored" | "derived-structural";
            source: {
                path: string;
                line: number;
                sha256: string;
            };
        };
        source: {
            path: string;
            line: number;
            sha256: string;
        };
        entity_identity?: {
            field: string;
            origin: 'authored' | 'derived-single-identifier';
        } | undefined;
        properties: {
            name: string;
            ontology: string;
            type: string;
            required: boolean;
            meaning: string;
            meaning_origin: 'authored' | 'derived-structural';
            meaning_line: number;
            line: number;
            source: {
                path: string;
                line: number;
                sha256: string;
            };
            meaning_source: {
                path: string;
                line: number;
                sha256: string;
            };
        }[];
        clauses: {
            text: string;
            source: {
                path: string;
                line: number;
                sha256: string;
            };
        }[];
        typed_contract: any;
        record_type: any;
        constraints?: any;
        binding?: any;
        assertions?: any;
        cases?: any;
        bindings?: {
            name: string;
            integration: string;
            condition?: import("./declarative-profile.js").Expression;
            input?: {
                mapping: string;
                type: string;
            };
        }[] | undefined;
        inputs?: any;
        result?: string | undefined;
    }[];
    references: {
        source: string;
        target: string;
        role: string;
        evidence: ReturnType<(line: number) => {
            path: string;
            line: number;
            sha256: string;
        }>;
    }[];
    composition_trace: any;
    status: string;
    reference_semantics: string;
    authority_effect: string;
    ontology_admitted: boolean;
} | {
    schema_version: string;
    subject: string;
    answer: string;
    meaning_origin: "authored" | "derived-structural";
    definition: {
        id: string;
        name: string;
        kind: string;
        meta_type: string | null;
        stable_key: string;
        key_origin: "authored" | "derived";
        identity_origin: "authored" | "derived";
        meaning: {
            text: string;
            origin: "authored" | "derived-structural";
            source: {
                path: string;
                line: number;
                sha256: string;
            };
        };
        source: {
            path: string;
            line: number;
            sha256: string;
        };
        entity_identity?: {
            field: string;
            origin: 'authored' | 'derived-single-identifier';
        } | undefined;
        properties: {
            name: string;
            ontology: string;
            type: string;
            required: boolean;
            meaning: string;
            meaning_origin: 'authored' | 'derived-structural';
            meaning_line: number;
            line: number;
            source: {
                path: string;
                line: number;
                sha256: string;
            };
            meaning_source: {
                path: string;
                line: number;
                sha256: string;
            };
        }[];
        clauses: {
            text: string;
            source: {
                path: string;
                line: number;
                sha256: string;
            };
        }[];
        typed_contract: any;
        record_type: any;
        constraints?: any;
        binding?: any;
        assertions?: any;
        cases?: any;
        bindings?: {
            name: string;
            integration: string;
            condition?: import("./declarative-profile.js").Expression;
            input?: {
                mapping: string;
                type: string;
            };
        }[] | undefined;
        inputs?: any;
        result?: string | undefined;
    };
    dependencies: {
        role: string;
        name: string;
        id: string;
        source: {
            path: string;
            line: number;
            sha256: string;
        };
    }[];
    claim: string;
    authority_effect: string;
}>;
export declare function checkFunction(sourcePath: string, target?: string): Promise<{
    status: string;
    profile: string;
    endpoint: any;
    authority_effect: string;
}>;
export declare function buildFunction(sourcePath: string, output: string, loaded?: ModuleTree): Promise<{
    status: string;
    target: string;
    output: string;
    source_sha256: string;
    files: number;
    authority_effect: string;
} | {
    status: string;
    profile: string;
    output: string;
    source_sha256: string;
    files: number;
    authority_effect: string;
}>;
