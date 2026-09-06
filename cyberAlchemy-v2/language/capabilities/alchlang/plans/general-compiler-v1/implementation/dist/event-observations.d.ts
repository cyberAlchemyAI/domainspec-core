import type { DatabaseSync } from "node:sqlite";
import { type DurableCommitRequest, type DurableOutboxRecord, type DurableOutboxTransport, type DurableSqliteTransactionalOutbox } from "./durable-outbox-runtime.js";
import type { SqliteIdempotentInbox } from "./outbox-integrations.js";
import type { EventObservationProfile, EventStage, compileEventProfile } from "./event-profile.js";
/** ORODI observation/v1 shape. Records are local simulation observations, never admitted runtime evidence. */
export declare class EventObservationCollector {
    readonly profile: EventObservationProfile;
    private readonly runId;
    private readonly bindingDigest;
    readonly observations: Array<{
        schema_version: "domainspec.orodi.observation/v1";
        observation_id: string;
        plane: "product";
        kind: "log";
        mode: "simulation";
        correlation_id: string;
        attributes: Record<string, string>;
        attribute_allowlist: string[];
        cardinality: {
            observed: number;
            budget: number;
        };
        telemetry: {
            offered: number;
            queued: number;
            exported: number;
            rejected: number;
            dropped: number;
            pending: number;
            partial_success: number;
        };
        deployment_effect: false;
        independently_observed: false;
        observed_at: string;
        invalidation_key_digest: string;
    }>;
    private offered;
    private rejected;
    private sequence;
    private readonly cardinalities;
    constructor(profile: EventObservationProfile, runId: string, bindingDigest: string);
    record(stage: EventStage, message: {
        messageId: string;
        eventType: string;
    }, at: string): void;
    accounting(): {
        offered: number;
        queued: number;
        rejected: number;
        exported: number;
        dropped: number;
        pending: number;
        partial_success: number;
    };
}
type EventCompilation = Awaited<ReturnType<typeof compileEventProfile>>;
/** Local prototype harness: reuses durable runtime transactions, with policy from the compiled Alch binding. */
export declare class LocalEventFlow {
    private readonly store;
    private readonly inbox;
    private readonly observer;
    private readonly clock;
    private readonly worker;
    private readonly eventType;
    private readonly maxAttempts;
    constructor(compilation: EventCompilation, transportId: string, store: DurableSqliteTransactionalOutbox, inbox: SqliteIdempotentInbox, transport: DurableOutboxTransport, observer: EventObservationCollector, clock: () => string);
    commit(request: DurableCommitRequest, failpoint?: boolean): {
        status: "committed" | "already-committed";
        version: number;
    };
    dispatch(): Promise<{
        published: number;
        failed: number;
        dead: number;
    }>;
    consume(message: Pick<DurableOutboxRecord, "messageId" | "eventType">, handler: (database: DatabaseSync) => void): "duplicate" | "processed";
}
export {};
