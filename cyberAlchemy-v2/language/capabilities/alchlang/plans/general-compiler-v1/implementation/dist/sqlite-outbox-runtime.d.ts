import { DatabaseSync } from "node:sqlite";
export interface OutboxMessage {
    readonly messageId: string;
    readonly eventType: string;
    readonly payload: Readonly<Record<string, unknown>>;
    readonly occurredAt: string;
}
export interface AtomicStateAndOutboxRequest {
    readonly aggregateType: string;
    readonly aggregateId: string;
    readonly state: Readonly<Record<string, unknown>>;
    readonly expectedVersion: number;
    readonly messages: readonly OutboxMessage[];
}
export interface PendingOutboxMessage extends OutboxMessage {
    readonly aggregateType: string;
    readonly aggregateId: string;
    readonly attempts: number;
    readonly lastError: string | null;
}
export interface OutboxTransport {
    publish(message: PendingOutboxMessage): Promise<void>;
}
export declare const sqliteOutboxMigrationSql = "CREATE TABLE IF NOT EXISTS domainspec_aggregate_state (\n  aggregate_type TEXT NOT NULL,\n  aggregate_id TEXT NOT NULL,\n  state_json TEXT NOT NULL,\n  version INTEGER NOT NULL,\n  updated_at TEXT NOT NULL,\n  PRIMARY KEY (aggregate_type, aggregate_id)\n);\nCREATE TABLE IF NOT EXISTS domainspec_outbox (\n  message_id TEXT PRIMARY KEY,\n  aggregate_type TEXT NOT NULL,\n  aggregate_id TEXT NOT NULL,\n  event_type TEXT NOT NULL,\n  payload_json TEXT NOT NULL,\n  occurred_at TEXT NOT NULL,\n  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'published')),\n  attempts INTEGER NOT NULL DEFAULT 0,\n  last_error TEXT\n);\nCREATE INDEX IF NOT EXISTS domainspec_outbox_pending_idx ON domainspec_outbox(status, occurred_at, message_id);\n";
export declare function validateAtomicStateAndOutboxRequest(value: unknown): asserts value is AtomicStateAndOutboxRequest;
export declare class SqliteTransactionalOutbox implements Disposable {
    readonly database: DatabaseSync;
    constructor(path: string);
    commit(request: AtomicStateAndOutboxRequest, failpoint?: "after-state-write"): void;
    state(aggregateType: string, aggregateId: string): {
        state: Readonly<Record<string, unknown>>;
        version: number;
    } | null;
    pending(limit?: number): readonly PendingOutboxMessage[];
    markPublished(messageId: string): void;
    markFailed(messageId: string, error: string): void;
    stats(): Readonly<{
        pending: number;
        published: number;
    }>;
    close(): void;
    [Symbol.dispose](): void;
}
export declare class TransactionalOutboxWorker {
    private readonly outbox;
    private readonly transport;
    constructor(outbox: SqliteTransactionalOutbox, transport: OutboxTransport);
    dispatchPending(limit?: number): Promise<{
        published: number;
        failed: number;
    }>;
}
export declare class CollectingStdoutOutboxTransport implements OutboxTransport {
    readonly messages: PendingOutboxMessage[];
    publish(message: PendingOutboxMessage): Promise<void>;
}
