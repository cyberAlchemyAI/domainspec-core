export type Expr = {
    kind: string;
    value?: any;
    name?: string;
    args?: Expr[];
    fields?: [string, Expr][];
    body?: Expr;
};
export type FunctionModel = {
    portability?: string;
    modules?: Record<string, any>;
    schemas: Record<string, Record<string, any>>;
    integrations: Record<string, any>;
    flows: Record<string, any[]>;
    endpoint: any;
};
export declare class FunctionFault extends Error {
    code: string;
    constructor(code: string);
}
export declare function validateSchema(model: FunctionModel, name: string, value: any, depth?: number): any;
export declare function evaluate(expr: Expr, scope: Record<string, any>, api: any): any;
export declare function createFunction(model: FunctionModel, api: any): {
    invoke: (input: any, env?: Record<string, string | undefined>, io?: {
        fetch?: typeof fetch;
    }) => Promise<any>;
    handler: (request: Request, env?: Record<string, string | undefined>, io?: {
        fetch?: typeof fetch;
    }) => Promise<Response>;
};
