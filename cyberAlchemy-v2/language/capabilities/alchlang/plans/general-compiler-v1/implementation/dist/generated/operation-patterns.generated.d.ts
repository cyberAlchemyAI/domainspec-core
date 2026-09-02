export declare const generatedOperationPatterns: readonly [{
    readonly pattern_id: "operation-port";
    readonly architecture_pattern_status: "candidate";
    readonly meta_type: {
        readonly id: "DS-D1.4";
        readonly status: "closed";
    };
    readonly integration_binding: {
        readonly id: "target-neutral-port";
        readonly status: "closed";
    };
    readonly generator: {
        readonly id: "typescript-operation-port-v1";
        readonly status: "closed";
    };
    readonly conformance: {
        readonly id: "general-compiler-v1-action-port-tests";
        readonly status: "closed";
    };
    readonly availability: "available";
    readonly generated_artifacts: readonly ["domain.tools.ts"];
    readonly blockers: readonly [];
}, {
    readonly pattern_id: "transactional-outbox";
    readonly architecture_pattern_status: "candidate";
    readonly meta_type: {
        readonly id: "DS-D1.4";
        readonly status: "closed";
    };
    readonly integration_binding: {
        readonly id: "sqlite-transactional-outbox";
        readonly status: "closed";
    };
    readonly generator: {
        readonly id: "typescript-sqlite-transactional-outbox-v1";
        readonly status: "closed";
    };
    readonly conformance: {
        readonly id: "transactional-outbox-executable-tests";
        readonly status: "closed";
    };
    readonly availability: "available";
    readonly generated_artifacts: readonly ["domain.outbox.port.ts", "domain.outbox.sqlite.ts", "domain.outbox.migration.sql", "domain.outbox.worker.ts", "domain.outbox.test.ts", "domain.generation-manifest.json"];
    readonly blockers: readonly [];
}];
