export declare function compileLocalHost(source: string): Promise<{
    normalized: string;
    deployment: {
        profile: string;
        id: string;
        runtime: string;
        provisioner: string;
        events: string;
        isolation: string;
        consumer: {
            operation: string;
            actors: string[];
            boundary: string;
        };
        transport: string;
        listen: string;
        operation: string;
        actors: string[];
        boundary: string;
        timeout_ms: number;
        max_request_bytes: number;
        endpoint: string;
        source_sha256: string;
        authority_effect: string;
    };
}>;
export declare function buildLocalHost(file: string, output: string): Promise<{
    status: string;
    output: string;
    profile: string;
    endpoint: string;
    authority_effect: string;
}>;
