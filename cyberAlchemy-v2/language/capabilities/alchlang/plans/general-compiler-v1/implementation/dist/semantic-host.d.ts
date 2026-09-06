type Property = {
    id: string;
    type: string;
    required: boolean;
    default?: unknown;
};
type RecordType = {
    name: string;
    kind: string;
    properties: Property[];
    line: number;
    from?: string;
};
/** A single parsed representation owns schemas, ontology relationships and both execution plans. */
export declare function compileSemanticHost(source: string): Promise<{
    config: {
        schema_version: string;
        binding_digest: string;
        model: {
            domain_id: string;
            facts: {
                id: string;
                type: string;
                required: boolean;
                default?: unknown;
                subject_ref: string;
            }[];
            mappings: any[];
            actions: any[];
            rules: never[];
            permissions: never[];
            transitions: any[];
        };
        executions: any[];
        event: string;
        aggregate: string;
        transport: string;
        max_attempts: number;
        max_receives: number;
        retention_ms: number;
        dead_letter: string;
        lease_ms: number;
        observation: {
            stages: never[];
            attributes: never[];
            cardinalityBudget: number;
        };
        authority_effect: string;
    };
    ontology: {
        schema_version: string;
        domain: string;
        source_sha256: string;
        records: Record<string, RecordType>;
        nodes: any[];
        relations: {
            from: any;
            type: string;
            to: any;
        }[];
        status: string;
        authority_effect: string;
    };
    schemas: {
        [k: string]: {
            $defs: {
                portableObject: {
                    type: string;
                    additionalProperties: {
                        $ref: string;
                    };
                };
                portableValue: {
                    anyOf: ({
                        type: string[];
                        minimum?: undefined;
                        maximum?: undefined;
                        items?: undefined;
                        $ref?: undefined;
                    } | {
                        type: string;
                        minimum: number;
                        maximum: number;
                        items?: undefined;
                        $ref?: undefined;
                    } | {
                        minimum?: undefined;
                        maximum?: undefined;
                        type: string;
                        items: {
                            $ref: string;
                        };
                        $ref?: undefined;
                    } | {
                        minimum?: undefined;
                        maximum?: undefined;
                        type?: undefined;
                        items?: undefined;
                        $ref: string;
                    })[];
                };
            };
            $schema: string;
            type: string;
            properties: {
                [k: string]: any;
            };
            required: string[];
            additionalProperties: boolean;
        };
    };
    generated: {
        source: string;
        contract: unknown;
        trace: unknown;
        id: any;
    }[];
    backfills: any[];
    binding: any;
    bindingSet: any;
    targets: {
        [k: string]: {
            manifest: unknown;
            source: string;
        };
    };
    compiler: {
        package: typeof import("./domainspec-cli.js").DOMAINSPEC_PACKAGE;
        version: typeof import("./domainspec-cli.js").DOMAINSPEC_VERSION;
        package_root: string;
        package_sha256: string;
        entry_sha256: string;
    };
}>;
export declare function buildSemanticHost(file: string, output: string): Promise<{
    status: string;
    profile: string;
    output: string;
    authority_effect: string;
}>;
export {};
