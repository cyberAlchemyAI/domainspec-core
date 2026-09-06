import { type ModuleTree } from './module-source.js';
export declare function buildRustFunction(sourcePath: string, output: string, loaded?: ModuleTree): Promise<{
    status: string;
    target: string;
    output: string;
    source_sha256: string;
    files: number;
    authority_effect: string;
}>;
export declare function traceRustFunction(sourcePath: string, inputPath: string): Promise<any>;
