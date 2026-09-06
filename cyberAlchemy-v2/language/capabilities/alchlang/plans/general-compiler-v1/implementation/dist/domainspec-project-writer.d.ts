export interface DomainSpecBuildOptions {
    bindingsPath?: string;
    packageRoot?: string;
    generate?: boolean;
    profile?: string;
    composition?: Record<string, unknown>;
    language?: "typescript" | "rust";
    applicationLayout?: boolean;
}
export declare function buildDomainSpec(sourcePath: string, outputPath: string, options?: DomainSpecBuildOptions): Promise<{
    status: string;
    output_directory: string;
    nodes: number;
    source_sha256: string;
    authority_effect: string;
}>;
export declare function checkDomainSpec(sourcePath: string, options?: Omit<DomainSpecBuildOptions, "generate">): Promise<{
    status: string;
    profile: string;
    nodes: number;
    source_sha256: string;
    authority_effect: string;
}>;
