export type PrerequisiteStatus = "closed" | "open" | "missing";
export type PatternAvailability = "available" | "blocked";
export interface OperationPattern {
    readonly pattern_id: string;
    readonly architecture_pattern_status: "candidate" | "stable";
    readonly meta_type: {
        readonly id: string;
        readonly status: PrerequisiteStatus;
    };
    readonly integration_binding: {
        readonly id: string;
        readonly status: PrerequisiteStatus;
    };
    readonly generator: {
        readonly id: string;
        readonly status: PrerequisiteStatus;
    };
    readonly conformance: {
        readonly id: string;
        readonly status: PrerequisiteStatus;
    };
    readonly availability: PatternAvailability;
    readonly generated_artifacts: readonly string[];
    readonly blockers: readonly string[];
}
type PatternIntent = {
    pattern_id: string;
    architecture_pattern_status: "candidate" | "stable";
    meta_type_ref: string;
    integration_binding_ref: string;
    generator_ref: string;
    conformance_ref: string;
    generated_artifacts: string[];
};
type BindingRegistration = {
    binding_id: string;
    status: "closed" | "open";
    manifest_ref: string;
    manifest_sha256: string;
};
type GeneratorRegistration = {
    generator_id: string;
    status: "closed" | "open";
    source_refs: string[];
    source_tree_sha256: string;
};
type ConformanceRegistration = {
    conformance_id: string;
    status: "PASS" | "FAIL" | "pending";
    generator_ref: string;
    generator_sha256: string;
    binding_ref: string;
    binding_sha256: string;
};
export interface RegistryCompilation {
    registry: {
        schema_version: string;
        registry_id: string;
        patterns: OperationPattern[];
        authority_effect: "none";
    };
    receipt: Record<string, unknown>;
    typescript_projection: string;
}
export declare function compileOperationPatternRegistry(input: {
    admitted_meta_types: readonly string[];
    pattern_intents: readonly PatternIntent[];
    integration_bindings: readonly BindingRegistration[];
    generators: readonly GeneratorRegistration[];
    conformance: readonly ConformanceRegistration[];
    resolved_binding_digests: Readonly<Record<string, string>>;
    resolved_generator_digests: Readonly<Record<string, string>>;
}): RegistryCompilation["registry"];
export declare function compileRegistryConfig(configPathInput: string): RegistryCompilation;
export declare function writeRegistryCompilation(configPathInput: string): RegistryCompilation;
export {};
