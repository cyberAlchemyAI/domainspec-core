import type { ActionAdapter, AdapterRequest, AdapterResult } from "./runtime.js";
export declare class MemoryActionAdapter implements ActionAdapter {
    private readonly result;
    readonly records: AdapterRequest[];
    constructor(result?: AdapterResult);
    execute(request: AdapterRequest): Promise<AdapterResult>;
}
export declare class SqliteActionAdapter implements ActionAdapter, Disposable {
    private readonly database;
    private readonly result;
    private constructor();
    static open(path: string, result?: AdapterResult): Promise<SqliteActionAdapter>;
    execute(request: AdapterRequest): Promise<AdapterResult>;
    records(): unknown[];
    close(): void;
    [Symbol.dispose](): void;
}
export interface HttpTransport {
    request(input: {
        url: string;
        method: "POST";
        headers: Readonly<Record<string, string>>;
        body: string;
    }): Promise<{
        status: number;
        body: string;
    }>;
}
export declare class FetchHttpTransport implements HttpTransport {
    private readonly allowedOrigins;
    constructor(allowedOrigins: readonly string[]);
    request(input: {
        url: string;
        method: "POST";
        headers: Readonly<Record<string, string>>;
        body: string;
    }): Promise<{
        status: number;
        body: string;
    }>;
}
export declare class HttpActionAdapter implements ActionAdapter {
    private readonly endpoint;
    private readonly transport;
    private readonly emittedEvents;
    constructor(endpoint: string, transport: HttpTransport, emittedEvents?: readonly string[]);
    execute(request: AdapterRequest): Promise<AdapterResult>;
}
