import { DatabaseSync } from "node:sqlite";
import type { DurableOutboxRecord, DurableOutboxTransport } from "./durable-outbox-runtime.js";
export interface OutboxHttpClient {
    send(input: {
        url: string;
        headers: Readonly<Record<string, string>>;
        body: string;
    }): Promise<{
        status: number;
    }>;
}
export declare class FetchOutboxHttpClient implements OutboxHttpClient {
    private readonly allowedOrigins;
    constructor(allowedOrigins: readonly string[]);
    send(input: {
        url: string;
        headers: Readonly<Record<string, string>>;
        body: string;
    }): Promise<{
        status: number;
    }>;
}
export declare class HttpOutboxTransport implements DurableOutboxTransport {
    private readonly endpoint;
    private readonly client;
    constructor(endpoint: string, client: OutboxHttpClient);
    publish(message: DurableOutboxRecord): Promise<void>;
}
export declare class SqliteIdempotentInbox implements Disposable {
    readonly database: DatabaseSync;
    constructor(path: string);
    consume(message: {
        messageId: string;
        eventType: string;
    }, processedAt: string, handler: (database: DatabaseSync) => void): "processed" | "duplicate";
    close(): void;
    [Symbol.dispose](): void;
}
