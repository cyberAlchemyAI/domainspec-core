export type ModuleInterface = {
    source_sha256: string;
    source_text: string;
    input: string;
    output: string;
    schemas: Record<string, any>;
    statuses: Record<string, number>;
};
export declare function moduleImports(source: string): {
    alias: string;
    file: string;
    line: number;
}[];
export declare function linkModuleTypes(source: string, modules: Record<string, ModuleInterface>): {
    source: string;
    origins: Record<string, number>;
};
