export class MemoryActionAdapter {
    result;
    records = [];
    constructor(result = { outcome: "completed" }) {
        this.result = result;
    }
    async execute(request) { this.records.push(structuredClone(request)); return structuredClone(this.result); }
}
export class SqliteActionAdapter {
    database;
    result;
    constructor(database, result) {
        this.database = database;
        this.result = result;
        this.database.exec("CREATE TABLE IF NOT EXISTS domainspec_actions (id INTEGER PRIMARY KEY AUTOINCREMENT, domain_id TEXT NOT NULL, action_id TEXT NOT NULL, actor_ref TEXT NOT NULL, authority_boundary_ref TEXT NOT NULL, facts_json TEXT NOT NULL)");
    }
    static async open(path, result = { outcome: "persisted" }) {
        const { DatabaseSync } = await import("node:sqlite");
        return new SqliteActionAdapter(new DatabaseSync(path), result);
    }
    async execute(request) {
        this.database.prepare("INSERT INTO domainspec_actions (domain_id, action_id, actor_ref, authority_boundary_ref, facts_json) VALUES (?, ?, ?, ?, ?)").run(request.domain_id, request.action_id, request.actor_ref, request.authority_boundary_ref, JSON.stringify(request.facts));
        return structuredClone(this.result);
    }
    records() { return this.database.prepare("SELECT domain_id, action_id, actor_ref, authority_boundary_ref, facts_json FROM domainspec_actions ORDER BY id").all(); }
    close() { this.database.close(); }
    [Symbol.dispose]() { this.close(); }
}
export class FetchHttpTransport {
    allowedOrigins;
    constructor(allowedOrigins) {
        this.allowedOrigins = allowedOrigins;
    }
    async request(input) {
        const url = new URL(input.url);
        if (!this.allowedOrigins.includes(url.origin))
            throw new Error(`HTTP_ORIGIN_DENIED:${url.origin}`);
        const response = await fetch(url, { method: input.method, headers: input.headers, body: input.body, redirect: "error" });
        return { status: response.status, body: await response.text() };
    }
}
export class HttpActionAdapter {
    endpoint;
    transport;
    emittedEvents;
    constructor(endpoint, transport, emittedEvents = []) {
        this.endpoint = endpoint;
        this.transport = transport;
        this.emittedEvents = emittedEvents;
    }
    async execute(request) {
        const response = await this.transport.request({ url: this.endpoint, method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(request) });
        if (response.status < 200 || response.status >= 300)
            throw new Error(`HTTP_ADAPTER_FAILED:${response.status}`);
        return { outcome: "http-accepted", emitted_events: this.emittedEvents, data: response.body ? JSON.parse(response.body) : null };
    }
}
