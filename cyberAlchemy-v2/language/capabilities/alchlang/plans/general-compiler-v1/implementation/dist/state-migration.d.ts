/** A structural extension: existing record bytes are opaque to the generated default Mapping. */
export declare function compileStateMigration(source: string): Promise<{
    normalized: string;
    generated: {
        source: string;
        contract: unknown;
        trace: unknown;
    };
    manifest: {
        profile: string;
        id: string;
        from_contract: string;
        subject: string;
        field: string;
        scalar: string;
        default: unknown;
        mapper: string;
        operations: string[];
        state_mappings: string[];
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
}>;
export declare function buildStateMigration(file: string, output: string): Promise<{
    status: string;
    profile: string;
    output: string;
    authority_effect: string;
}>;
