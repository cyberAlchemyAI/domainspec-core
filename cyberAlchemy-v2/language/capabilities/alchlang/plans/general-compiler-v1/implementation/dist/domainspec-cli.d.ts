export declare const DOMAINSPEC_PACKAGE: "@domainspec-v2/cli";
export declare const DOMAINSPEC_VERSION: "1.0.0";
export interface DomainSpecGraph {
    project_root: string;
    project_id: string;
    nodes: Array<{
        selector: string;
        kind: string;
        meta_type_id: string;
        body: unknown;
    }>;
    relationships: Array<{
        edge_id: string;
        relationship: string;
        source: {
            feature_id: string;
            node_id: string;
        };
        target: {
            feature_id: string;
            node_id: string;
        };
    }>;
    source_manifest: {
        manifest_sha256: string;
    };
    authority_effect: "none";
}
export interface DomainSpecIo {
    stdout(value: string): void;
    stderr(value: string): void;
}
export interface DomainSpecCompiler {
    compileEventBindings(value: unknown, language: "typescript" | "rust"): {
        manifest: unknown;
        source: string;
    };
    supportsExactUInt64: boolean;
    applicationPaths: Readonly<Record<string, string>>;
    outputImport(from: string, to: string): string;
    applicationLayoutId: string;
    compileDeclarativeFunction(value: unknown): {
        source: string;
        contract: unknown;
        trace: unknown;
    };
    binding: {
        package: typeof DOMAINSPEC_PACKAGE;
        version: typeof DOMAINSPEC_VERSION;
        package_root: string;
        package_sha256: string;
        entry_sha256: string;
    };
    compileProject(sourceRoot: string): {
        graph: DomainSpecGraph;
        certificate: {
            compiler: {
                package: string;
                version: string;
            };
            authority_effect: "none";
        };
    };
    runCli(args: readonly string[], io?: DomainSpecIo): number;
}
export declare function defaultDomainSpecPackageRoot(): string;
export declare function loadDomainSpecCompiler(packageRoot?: string): Promise<DomainSpecCompiler>;
export declare function runDomainSpecCli(args: readonly string[], io?: DomainSpecIo, packageRoot?: string): Promise<number>;
