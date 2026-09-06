type TraceOptions = {
    maxEvents?: number;
    maxBytes?: number;
};
/** Local, provided-input diagnostic. No credentials or provider-fetch path is accepted. */
export declare function createTracedInvoker(model: any, bindings: any[], api: any, execute: any, validateInput: any, ontology: any, identity: any, createBoundary: any, modules?: any): (input: any, options?: TraceOptions) => Promise<{
    schema_version: string;
    binding: any;
    execution_mode: string;
    outcome: any;
    capture: {
        complete: boolean;
        truncated: boolean;
        dropped_events: number;
        recorded_bytes: number;
        max_events: number;
        max_bytes: number;
    };
    answer: string;
    selection_reason: {
        clause: any;
        rule_results: {
            name: any;
            value: any;
            source: any;
        }[];
    } | null;
    selected_case: any;
    queries: any;
    declarations: any;
    events: any[];
    authority_effect: string;
    claim: string;
}>;
export {};
