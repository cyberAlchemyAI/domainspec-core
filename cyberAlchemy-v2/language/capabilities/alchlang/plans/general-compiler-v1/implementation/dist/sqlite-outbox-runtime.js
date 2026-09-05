import { DatabaseSync } from "node:sqlite";
export const sqliteOutboxMigrationSql = `CREATE TABLE IF NOT EXISTS domainspec_aggregate_state (
  aggregate_type TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  state_json TEXT NOT NULL,
  version INTEGER NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (aggregate_type, aggregate_id)
);
CREATE TABLE IF NOT EXISTS domainspec_outbox (
  message_id TEXT PRIMARY KEY,
  aggregate_type TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'published')),
  attempts INTEGER NOT NULL DEFAULT 0,
  last_error TEXT
);
CREATE INDEX IF NOT EXISTS domainspec_outbox_pending_idx ON domainspec_outbox(status, occurred_at, message_id);
`;
function nonEmpty(value, code) {
    if (typeof value !== "string" || value.length === 0)
        throw new Error(code);
}
export function validateAtomicStateAndOutboxRequest(value) {
    if (!value || typeof value !== "object" || Array.isArray(value))
        throw new Error("OUTBOX_REQUEST_INVALID");
    const request = value;
    nonEmpty(request.aggregateType, "OUTBOX_AGGREGATE_TYPE_REQUIRED");
    nonEmpty(request.aggregateId, "OUTBOX_AGGREGATE_ID_REQUIRED");
    if (!request.state || typeof request.state !== "object" || Array.isArray(request.state))
        throw new Error("OUTBOX_STATE_REQUIRED");
    if (!Number.isSafeInteger(request.expectedVersion) || Number(request.expectedVersion) < 0)
        throw new Error("OUTBOX_EXPECTED_VERSION_INVALID");
    if (!Array.isArray(request.messages) || request.messages.length === 0)
        throw new Error("OUTBOX_MESSAGE_REQUIRED");
    const ids = new Set();
    for (const raw of request.messages) {
        if (!raw || typeof raw !== "object" || Array.isArray(raw))
            throw new Error("OUTBOX_MESSAGE_INVALID");
        const message = raw;
        nonEmpty(message.messageId, "OUTBOX_MESSAGE_ID_REQUIRED");
        nonEmpty(message.eventType, "OUTBOX_EVENT_TYPE_REQUIRED");
        nonEmpty(message.occurredAt, "OUTBOX_OCCURRED_AT_REQUIRED");
        if (Number.isNaN(Date.parse(message.occurredAt)))
            throw new Error("OUTBOX_OCCURRED_AT_INVALID");
        if (!message.payload || typeof message.payload !== "object" || Array.isArray(message.payload))
            throw new Error("OUTBOX_PAYLOAD_REQUIRED");
        if (ids.has(message.messageId))
            throw new Error("OUTBOX_DUPLICATE_MESSAGE_ID");
        ids.add(message.messageId);
    }
}
export class SqliteTransactionalOutbox {
    database;
    constructor(path) {
        nonEmpty(path, "OUTBOX_DATABASE_PATH_REQUIRED");
        this.database = new DatabaseSync(path);
        this.database.exec(sqliteOutboxMigrationSql);
    }
    commit(request, failpoint) {
        validateAtomicStateAndOutboxRequest(request);
        this.database.exec("BEGIN IMMEDIATE");
        try {
            const existing = this.database.prepare("SELECT version FROM domainspec_aggregate_state WHERE aggregate_type = ? AND aggregate_id = ?").get(request.aggregateType, request.aggregateId);
            if ((existing?.version ?? 0) !== request.expectedVersion)
                throw new Error("OUTBOX_VERSION_CONFLICT");
            this.database.prepare("INSERT INTO domainspec_aggregate_state (aggregate_type, aggregate_id, state_json, version, updated_at) VALUES (?, ?, ?, ?, ?) ON CONFLICT(aggregate_type, aggregate_id) DO UPDATE SET state_json = excluded.state_json, version = excluded.version, updated_at = excluded.updated_at").run(request.aggregateType, request.aggregateId, JSON.stringify(request.state), request.expectedVersion + 1, request.messages[0].occurredAt);
            if (failpoint === "after-state-write")
                throw new Error("OUTBOX_FAILPOINT_AFTER_STATE_WRITE");
            const insert = this.database.prepare("INSERT INTO domainspec_outbox (message_id, aggregate_type, aggregate_id, event_type, payload_json, occurred_at) VALUES (?, ?, ?, ?, ?, ?)");
            for (const message of request.messages)
                insert.run(message.messageId, request.aggregateType, request.aggregateId, message.eventType, JSON.stringify(message.payload), message.occurredAt);
            this.database.exec("COMMIT");
        }
        catch (error) {
            this.database.exec("ROLLBACK");
            throw error;
        }
    }
    state(aggregateType, aggregateId) {
        const row = this.database.prepare("SELECT state_json, version FROM domainspec_aggregate_state WHERE aggregate_type = ? AND aggregate_id = ?").get(aggregateType, aggregateId);
        return row ? { state: JSON.parse(row.state_json), version: row.version } : null;
    }
    pending(limit = 100) {
        if (!Number.isSafeInteger(limit) || limit < 1)
            throw new Error("OUTBOX_LIMIT_INVALID");
        const rows = this.database.prepare("SELECT message_id, aggregate_type, aggregate_id, event_type, payload_json, occurred_at, attempts, last_error FROM domainspec_outbox WHERE status = 'pending' ORDER BY occurred_at, message_id LIMIT ?").all(limit);
        return rows.map((row) => ({ messageId: row.message_id, aggregateType: row.aggregate_type, aggregateId: row.aggregate_id, eventType: row.event_type, payload: JSON.parse(row.payload_json), occurredAt: row.occurred_at, attempts: row.attempts, lastError: row.last_error }));
    }
    markPublished(messageId) {
        const result = this.database.prepare("UPDATE domainspec_outbox SET status = 'published', attempts = attempts + 1, last_error = NULL WHERE message_id = ? AND status = 'pending'").run(messageId);
        if (result.changes !== 1)
            throw new Error(`OUTBOX_PENDING_MESSAGE_NOT_FOUND:${messageId}`);
    }
    markFailed(messageId, error) {
        const result = this.database.prepare("UPDATE domainspec_outbox SET attempts = attempts + 1, last_error = ? WHERE message_id = ? AND status = 'pending'").run(error, messageId);
        if (result.changes !== 1)
            throw new Error(`OUTBOX_PENDING_MESSAGE_NOT_FOUND:${messageId}`);
    }
    stats() {
        const rows = this.database.prepare("SELECT status, COUNT(*) AS count FROM domainspec_outbox GROUP BY status").all();
        const result = { pending: 0, published: 0 };
        for (const row of rows)
            result[row.status] = row.count;
        return result;
    }
    close() { this.database.close(); }
    [Symbol.dispose]() { this.close(); }
}
export class TransactionalOutboxWorker {
    outbox;
    transport;
    constructor(outbox, transport) {
        this.outbox = outbox;
        this.transport = transport;
    }
    async dispatchPending(limit = 100) {
        let published = 0;
        let failed = 0;
        for (const message of this.outbox.pending(limit)) {
            try {
                await this.transport.publish(message);
                this.outbox.markPublished(message.messageId);
                published += 1;
            }
            catch (error) {
                this.outbox.markFailed(message.messageId, error instanceof Error ? error.message : String(error));
                failed += 1;
            }
        }
        return { published, failed };
    }
}
export class CollectingStdoutOutboxTransport {
    messages = [];
    async publish(message) { this.messages.push(structuredClone(message)); }
}
