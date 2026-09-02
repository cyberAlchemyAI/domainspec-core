import type { CompilationResult } from "./model.js";
export interface WriteOptions {
    force?: boolean;
    carrier?: unknown;
}
export interface WriteReceipt {
    output_directory: string;
    files: Readonly<Record<string, string>>;
    source_digest: string;
    plan_digest: string;
}
export declare function writeCompilation(result: CompilationResult, outputDirectory: string, options?: WriteOptions): WriteReceipt;
