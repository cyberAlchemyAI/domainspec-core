import type { Expression } from './declarative-profile.js';
type Row = {
    text: string;
    line: number;
};
export type DerivedDeclaration = {
    name: string;
    kind: string;
    key: string;
    ontology: string;
    identity_origin: 'authored' | 'derived';
    meaning: string;
    meaning_origin: 'authored' | 'derived-structural';
    meaning_line: number;
    key_origin: 'authored' | 'derived';
    line: number;
    rows: Row[];
    identity?: {
        field: string;
        origin: 'authored' | 'derived-single-identifier';
    };
    properties: {
        name: string;
        ontology: string;
        type: string;
        required: boolean;
        meaning: string;
        meaning_origin: 'authored' | 'derived-structural';
        meaning_line: number;
        line: number;
    }[];
};
/** Elaborates missing bindings for the existing compiler; generated descriptions assert structure only. */
export declare function elaborateOntology(source: string): {
    source: string;
    domain: string;
    source_sha256: string;
    declarations: DerivedDeclaration[];
};
type Parsed = {
    ontologySource: ReturnType<typeof elaborateOntology>;
    contract: any;
    coreContracts: Record<string, unknown>;
    model: any;
    boundaryBindings: {
        name: string;
        integration: string;
        condition?: Expression;
        input?: {
            mapping: string;
            type: string;
        };
    }[];
};
export declare function deriveOntology(parsed: Parsed, trace: any, sourcePath: string): {
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
            condition?: Expression;
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
};
export declare function explainOntology(ontology: ReturnType<typeof deriveOntology>, selector: string): {
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
            condition?: Expression;
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
};
export {};
