import { DatabaseSync } from "node:sqlite";
export class FetchOutboxHttpClient {
    allowedOrigins;
    constructor(allowedOrigins) {
        this.allowedOrigins = allowedOrigins;
    }
    async send(input) { const origin = new URL(input.url).origin; if (!this.allowedOrigins.includes(origin))
        throw new Error(`OUTBOX_HTTP_ORIGIN_DENIED:${origin}`); const response = await fetch(input.url, { method: "POST", headers: input.headers, body: input.body, redirect: "error" }); return { status: response.status }; }
}
export class HttpOutboxTransport {
    endpoint;
    client;
    constructor(endpoint, client) {
        this.endpoint = endpoint;
        this.client = client;
    }
    async publish(message) { const response = await this.client.send({ url: this.endpoint, headers: { "content-type": "application/json", "idempotency-key": message.messageId }, body: JSON.stringify({ messageId: message.messageId, eventType: message.eventType, payload: message.payload, occurredAt: message.occurredAt, aggregateType: message.aggregateType, aggregateId: message.aggregateId }) }); if (response.status < 200 || response.status >= 300)
        throw new Error(`OUTBOX_HTTP_FAILED:${response.status}`); }
}
export class SqliteIdempotentInbox {
    database;
    constructor(path) { this.database = new DatabaseSync(path); this.database.exec("CREATE TABLE IF NOT EXISTS domainspec_inbox(message_id TEXT PRIMARY KEY,event_type TEXT NOT NULL,processed_at TEXT NOT NULL)"); }
    consume(message, processedAt, handler) { this.database.exec("BEGIN IMMEDIATE"); try {
        const existing = this.database.prepare("SELECT 1 FROM domainspec_inbox WHERE message_id=?").get(message.messageId);
        if (existing) {
            this.database.exec("COMMIT");
            return "duplicate";
        }
        handler(this.database);
        this.database.prepare("INSERT INTO domainspec_inbox VALUES(?,?,?)").run(message.messageId, message.eventType, processedAt);
        this.database.exec("COMMIT");
        return "processed";
    }
    catch (e) {
        this.database.exec("ROLLBACK");
        throw e;
    } }
    close() { this.database.close(); }
    [Symbol.dispose]() { this.close(); }
}
