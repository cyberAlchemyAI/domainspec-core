type Property = {
    id: string;
    name: string;
    type: string;
    required: boolean;
    owner: string;
    default?: unknown;
};
export type HostOntology = {
    schema_version: string;
    domain: string;
    source_sha256: string;
    status: string;
    authority_effect: string;
    records: Record<string, {
        id: string;
        properties: Property[];
    }>;
    operations: any[];
    mappings: any[];
};
/** The runtime facts and schema properties are projections of these same typed records. */
export declare function factsFromOntology(o: HostOntology): {
    id: string;
    subject_ref: string;
    type: string;
    required: boolean;
    owner: string;
}[];
export declare function schemasFromOntology(o: HostOntology): {
    schema_version: string;
    ontology_sha256: string;
    facts: {
        [k: string]: {
            $schema: string;
            type: string;
            properties: {
                [k: string]: any;
            };
            required: string[];
            additionalProperties: boolean;
        };
    };
    states: any;
    authority_effect: string;
};
export declare function compileOntologyHost(source: string): Promise<{
    normalized: string;
    ontology: HostOntology;
    schemas: {
        schema_version: string;
        ontology_sha256: string;
        facts: {
            [k: string]: {
                $schema: string;
                type: string;
                properties: {
                    [k: string]: any;
                };
                required: string[];
                additionalProperties: boolean;
            };
        };
        states: any;
        authority_effect: string;
    };
    generated: {
        directory: string;
        output: {
            source: string;
            contract: unknown;
            trace: unknown;
        };
        descriptor: {
            profile: string;
            id: string;
            subject: string;
            property_id: string;
            field: string;
            scalar: string;
            default: unknown;
            mapper: string;
            operations: any[];
            state_mappings: any[];
            mapper_sha256: string;
            compiler: {
                package: typeof import("./domainspec-cli.js").DOMAINSPEC_PACKAGE;
                version: typeof import("./domainspec-cli.js").DOMAINSPEC_VERSION;
                package_root: string;
                package_sha256: string;
                entry_sha256: string;
            };
            source_sha256: string;
            authority_effect: string;
        };
    }[];
}>;
export declare function buildOntologyHost(file: string, output: string): Promise<{
    status: string;
    profile: string;
    output: string;
    authority_effect: string;
}>;
export {};
