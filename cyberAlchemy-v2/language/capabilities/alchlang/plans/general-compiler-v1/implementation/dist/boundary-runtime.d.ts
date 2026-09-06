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
export declare function portableTimestamp(value: string): boolean;
export declare function validateSchema(model: FunctionModel, name: string, value: any, depth?: number): any;
export declare function prepareIntegrationRequest(b: any, scope: any, env: Record<string, string | undefined>): {
    url: string;
    method: string;
    headers: Record<string, string>;
    redirect: string;
    timeout_ms: any;
    max_bytes: any;
};
export type ModuleIo = {
    fetch?: typeof fetch;
    observeRequest?: (request: any) => void;
    localOnly?: boolean;
    signal?: AbortSignal;
};
export declare function createBoundary(model: FunctionModel, bindings: {
    name: string;
    integration: string;
    condition?: unknown;
    input?: {
        mapping: string;
        type: string;
    };
}[], compute: (scope: Record<string, any>) => any, precheck?: (scope: Record<string, any>) => void, modules?: Record<string, (input: any, env: any, io: ModuleIo, observe?: any) => Promise<any>>, observe?: (event: any) => void, guard?: (scope: Record<string, any>, binding: string) => boolean, mapInput?: (scope: Record<string, any>, binding: string) => any): {
    invoke: (input: any, env?: Record<string, string | undefined>, io?: ModuleIo) => Promise<any>;
    handler: (request: Request, env?: Record<string, string | undefined>, io?: ModuleIo) => Promise<Response>;
};
