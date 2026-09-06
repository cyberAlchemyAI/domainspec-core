export declare const EVENT_STAGES: readonly ["outbox-committed", "provider-accepted", "consumer-received", "consumer-committed", "consumer-duplicate", "consumer-failed", "transport-unknown"];
export type EventStage = typeof EVENT_STAGES[number];
export interface EventObservationProfile {
    id: string;
    transport: string;
    stages: EventStage[];
    attributes: string[];
    cardinalityBudget: number;
    mode: "simulation";
}
/** This profile delegates business syntax to the existing Alch parser and delivery semantics to DomainSpec. */
export declare function compileEventProfile(source: string): Promise<{
    profile: string;
    domain_id: string;
    bindingSet: {
        schema_version: string;
        binding_set_id: string;
        profile_id: string;
        subject_ref: string;
        authority_effect: string;
        message_channels: {
            channel_id: string;
            purpose: string;
            allowed_event_refs: string[];
            publisher_operation_refs: string[];
            consumer_operation_refs: string[];
            evidence_boundary: string;
        }[];
        delivery_policies: {
            policy_id: string;
            semantics: string;
            acknowledgement_boundary: string;
            ordering_scope: string;
            visibility_timeout_seconds: number;
            retention_seconds: number;
            max_receive_count: number;
            dead_letter_channel_ref: string;
            deduplication_owner_ref: string;
            evidence_boundary: string;
        }[];
        transport_failure_policies: {
            policy_id: string;
            retry_eligibility: string;
            max_attempts: number;
            backoff: string;
            unknown_outcome: string;
            terminal_action: string;
            evidence_boundary: string;
        }[];
        transport_bindings: {
            binding_id: string;
            mode: string;
            direction: string;
            operation_ref: string;
            event_ref: string;
            channel_ref: string;
            delivery_policy_ref: string;
            failure_policy_ref: string;
            envelope_profile_ref: string;
            evidence_boundary: string;
        }[];
    };
    observations: EventObservationProfile[];
    targets: {
        [k: string]: {
            manifest: unknown;
            source: string;
        };
    };
    business: import("./model.js").CompilationResult;
    source_sha256: string;
    compiler: {
        package: typeof import("./domainspec-cli.js").DOMAINSPEC_PACKAGE;
        version: typeof import("./domainspec-cli.js").DOMAINSPEC_VERSION;
        package_root: string;
        package_sha256: string;
        entry_sha256: string;
    };
    authority_effect: string;
}>;
export declare function buildEventProfile(file: string, output: string): Promise<{
    status: string;
    output: string;
    profile: string;
    authority_effect: string;
}>;
