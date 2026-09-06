import { type ModuleInterface } from './module-types.js';
export type Expression = {
    op: 'literal';
    value: string | number | boolean | null;
} | {
    op: 'path';
    path: string[];
} | {
    op: 'call';
    name: string;
    args: Expression[];
} | {
    op: 'exists' | 'forall' | 'exactly_one';
    binding: string;
    collection: Expression;
    where: Expression;
};
export declare function parseDeclarativeExpression(source: string): Expression;
export declare function parseDeclarativeSource(source: string, modules?: Record<string, ModuleInterface>): {
    model: import("./function-runtime.js").FunctionModel;
    coreSource: string;
    bindings: any;
    contract: {
        schema_version: string;
        portability?: string | undefined;
        records: Record<string, Record<string, string>>;
        roots: Record<string, string>;
        calculations: {
            [k: string]: string[];
        };
        nodes: any[];
        bindings?: {
            name: string;
            condition?: Expression | undefined;
            input?: {
                mapping: string;
                type: string;
            } | undefined;
        }[] | undefined;
        assertions: any[];
        results: any[];
        output: any;
    };
    coreContracts: {
        [k: string]: any;
    };
    ontologySource: {
        source: string;
        domain: string;
        source_sha256: string;
        declarations: import("./derived-ontology.js").DerivedDeclaration[];
    };
    boundaryBindings: {
        name: string;
        integration: string;
        condition?: Expression;
        input?: {
            mapping: string;
            type: string;
        };
    }[];
    profile: string;
};
