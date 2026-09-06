import { DurableOutboxWorker } from "./durable-outbox-runtime.js";
/** ORODI observation/v1 shape. Records are local simulation observations, never admitted runtime evidence. */
export class EventObservationCollector {
    profile;
    runId;
    bindingDigest;
    observations = [];
    offered = 0;
    rejected = 0;
    sequence = 0;
    cardinalities = new Set();
    constructor(profile, runId, bindingDigest) {
        this.profile = profile;
        this.runId = runId;
        this.bindingDigest = bindingDigest;
        if (!runId || !/^[a-f0-9]{64}$/.test(bindingDigest))
            throw Error("EVENT_OBSERVATION_BINDING");
    }
    record(stage, message, at) {
        if (!this.profile.stages.includes(stage))
            return;
        if (!message.messageId || !message.eventType || !Number.isFinite(Date.parse(at)))
            throw Error("EVENT_OBSERVATION_INPUT");
        this.offered++;
        const key = JSON.stringify([message.messageId, message.eventType, stage]);
        if (!this.cardinalities.has(key) && this.cardinalities.size >= this.profile.cardinalityBudget) {
            this.rejected++;
            return;
        }
        this.cardinalities.add(key);
        this.observations.push({ schema_version: "domainspec.orodi.observation/v1", observation_id: `${this.runId}:${this.profile.id}:${++this.sequence}`, plane: "product", kind: "log", mode: "simulation", correlation_id: message.messageId, attributes: { "message-id": message.messageId, "event-type": message.eventType, stage }, attribute_allowlist: [...this.profile.attributes], cardinality: { observed: this.cardinalities.size, budget: this.profile.cardinalityBudget }, telemetry: { offered: 1, queued: 1, exported: 0, rejected: 0, dropped: 0, pending: 1, partial_success: 0 }, deployment_effect: false, independently_observed: false, observed_at: at, invalidation_key_digest: this.bindingDigest });
    }
    accounting() { return { offered: this.offered, queued: this.observations.length, rejected: this.rejected, exported: 0, dropped: 0, pending: this.observations.length, partial_success: 0 }; }
}
/** Local prototype harness: reuses durable runtime transactions, with policy from the compiled Alch binding. */
export class LocalEventFlow {
    store;
    inbox;
    observer;
    clock;
    worker;
    eventType;
    maxAttempts;
    constructor(compilation, transportId, store, inbox, transport, observer, clock) {
        this.store = store;
        this.inbox = inbox;
        this.observer = observer;
        this.clock = clock;
        const binding = compilation.bindingSet.transport_bindings.find(b => b.binding_id === transportId);
        if (!binding || observer.profile.transport !== transportId)
            throw Error("EVENT_FLOW_BINDING");
        const policy = compilation.bindingSet.transport_failure_policies.find(p => p.policy_id === binding.failure_policy_ref);
        const delivery = compilation.bindingSet.delivery_policies.find(p => p.policy_id === binding.delivery_policy_ref);
        this.eventType = binding.event_ref.split(":")[1];
        this.maxAttempts = policy.max_attempts;
        this.worker = new DurableOutboxWorker(store, { publish: async (message) => {
                if (message.eventType !== this.eventType)
                    throw Error("EVENT_FLOW_EVENT");
                try {
                    await transport.publish(message);
                }
                catch (error) {
                    this.observer.record("transport-unknown", message, this.clock());
                    throw error;
                }
                this.observer.record("provider-accepted", message, this.clock());
            } }, { workerId: transportId, clock, leaseMs: delivery.visibility_timeout_seconds * 1000 });
    }
    commit(request, failpoint = false) {
        if (request.messages.some(m => m.eventType !== this.eventType || m.maxAttempts !== undefined && m.maxAttempts !== this.maxAttempts))
            throw Error("EVENT_FLOW_EVENT_OR_POLICY");
        const result = this.store.commit({ ...request, messages: request.messages.map(m => ({ ...m, maxAttempts: this.maxAttempts })) }, failpoint ? "after-state-write" : undefined);
        if (result.status === "committed")
            for (const message of request.messages)
                this.observer.record("outbox-committed", message, this.clock());
        return result;
    }
    dispatch() { return this.worker.dispatch(); }
    consume(message, handler) {
        if (message.eventType !== this.eventType)
            throw Error("EVENT_FLOW_EVENT");
        this.observer.record("consumer-received", message, this.clock());
        let result;
        try {
            result = this.inbox.consume(message, this.clock(), handler);
        }
        catch (error) {
            this.observer.record("consumer-failed", message, this.clock());
            throw error;
        }
        this.observer.record(result === "processed" ? "consumer-committed" : "consumer-duplicate", message, this.clock());
        return result;
    }
}
