import { DatabaseSync } from "node:sqlite";
export type DurableOutboxStatus = "pending" | "leased" | "published" | "dead";
export interface DurableOutboxMessage {
    readonly messageId: string;
    readonly eventType: string;
    readonly payload: Readonly<Record<string, unknown>>;
    readonly occurredAt: string;
    readonly maxAttempts?: number;
}
export interface DurableCommitRequest {
    readonly aggregateType: string;
    readonly aggregateId: string;
    readonly state: Readonly<Record<string, unknown>>;
    readonly expectedVersion: number;
    readonly messages: readonly DurableOutboxMessage[];
}
export interface DurableOutboxRecord extends DurableOutboxMessage {
    readonly aggregateType: string;
    readonly aggregateId: string;
    readonly status: DurableOutboxStatus;
    readonly attempts: number;
    readonly maxAttempts: number;
    readonly availableAt: string;
    readonly leaseOwner: string | null;
    readonly leaseUntil: string | null;
    readonly lastError: string | null;
    readonly publishedAt: string | null;
}
export interface DurableOutboxTransport {
    publish(message: DurableOutboxRecord): Promise<void>;
}
export interface OutboxTelemetryEvent {
    kind: "committed" | "replayed" | "claimed" | "published" | "retry-scheduled" | "dead-lettered" | "dead-requeued";
    messageId?: string;
    workerId?: string;
    at: string;
}
export interface OutboxTelemetrySink {
    record(event: OutboxTelemetryEvent): void;
}
export declare class CollectingOutboxTelemetry implements OutboxTelemetrySink {
    readonly events: OutboxTelemetryEvent[];
    record(event: OutboxTelemetryEvent): void;
}
export declare class DurableSqliteTransactionalOutbox implements Disposable {
    private readonly telemetry;
    readonly database: DatabaseSync;
    constructor(path: string, telemetry?: OutboxTelemetrySink);
    private migrate;
    schemaVersion(): number;
    commit(request: DurableCommitRequest, failpoint?: "after-state-write"): {
        status: "committed" | "already-committed";
        version: number;
    };
    private decode;
    state(type: string, id: string): {
        state: Readonly<Record<string, unknown>>;
        version: number;
    } | null;
    records(status?: DurableOutboxStatus, limit?: number): readonly DurableOutboxRecord[];
    pending(limit?: number): readonly DurableOutboxRecord[];
    claim(workerId: string, now: string, leaseMs: number, limit?: number): readonly DurableOutboxRecord[];
    markPublished(id: string, worker: string, at: string): void;
    markFailed(id: string, worker: string, error: string, at: string): "pending" | "dead";
    requeueDead(id: string, at: string): void;
    stats(): Record<DurableOutboxStatus, number>;
    close(): void;
    [Symbol.dispose](): void;
}
export interface DurableWorkerOptions {
    workerId: string;
    clock?: () => string;
    leaseMs?: number;
    retryBaseMs?: number;
    maxRetryMs?: number;
}
export declare class DurableOutboxWorker {
    private readonly store;
    private readonly transport;
    private readonly options;
    constructor(store: DurableSqliteTransactionalOutbox, transport: DurableOutboxTransport, options: DurableWorkerOptions);
    dispatch(limit?: number): Promise<{
        published: number;
        failed: number;
        dead: number;
    }>;
}
