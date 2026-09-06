export declare function normalizeEvents(events: any[]): {
    [k: string]: any;
}[];
export declare function normalizeRequest(request: any): any;
export declare function compareExecutions(node: any, rust: any, expected: any): {
    output: boolean;
    oracle: boolean;
    requests: boolean;
    decisions: boolean;
    complete: any;
    consumed: boolean;
};
export declare function runConformance(sourcePath: string, fixturePath: string, outPath: string): Promise<{
    schema_version: string;
    status: string;
    profile: string;
    source_sha256: string;
    dependency_sources: Record<string, string>;
    fixtures_sha256: string;
    builds: {
        node: string;
        rust: string;
    };
    count: number;
    cases: {
        name: any;
        status: string;
        checks: {
            output: boolean;
            oracle: boolean;
            requests: boolean;
            decisions: boolean;
            complete: any;
            consumed: boolean;
        };
        node: {
            outcome: {
                status: string;
                result: any;
                code?: undefined;
            } | {
                result?: undefined;
                status: string;
                code: any;
            };
            requests: any[];
            decisions: {
                [k: string]: any;
            }[];
        };
        rust: {
            outcome: any;
            requests: any;
            decisions: {
                [k: string]: any;
            }[];
        };
    }[];
    execution: string;
    claim: string;
    authority_effect: string;
}>;
