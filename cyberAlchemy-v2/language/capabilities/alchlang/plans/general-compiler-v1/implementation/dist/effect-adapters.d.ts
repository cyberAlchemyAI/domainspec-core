import { type NormalizedDomain, type NormalizedEffect } from "./model.js";
import type { ActionAdapter, AdapterRequest, AdapterResult } from "./runtime.js";
import { DurableSqliteTransactionalOutbox, type DurableCommitRequest } from "./durable-outbox-runtime.js";
export declare function resolveSqliteTransactionalOutboxEffect(model: NormalizedDomain, actionId: string, bindingId: string): NormalizedEffect;
export declare class SqliteTransactionalOutboxActionAdapter implements ActionAdapter, Disposable {
    private readonly effect;
    private readonly request;
    readonly outbox: DurableSqliteTransactionalOutbox;
    private readonly failpoint?;
    private constructor();
    static open(input: {
        model: NormalizedDomain;
        actionId: string;
        bindingId: string;
        databasePath: string;
        effectRequest: DurableCommitRequest;
        failpoint?: "after-state-write";
    }): SqliteTransactionalOutboxActionAdapter;
    execute(request: AdapterRequest): Promise<AdapterResult>;
    close(): void;
    [Symbol.dispose](): void;
}
