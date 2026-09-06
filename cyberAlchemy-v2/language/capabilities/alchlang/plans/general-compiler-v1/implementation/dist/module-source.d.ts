import { parseDeclarativeSource } from './declarative-profile.js';
export type ModuleTree = {
    path: string;
    source: string;
    parsed: ReturnType<typeof parseDeclarativeSource>;
    children: Record<string, ModuleTree>;
};
export declare function loadModuleTree(sourcePath: string): ModuleTree;
export declare function assertModuleSources(tree: ModuleTree): void;
export declare function moduleEnvironment(tree: ModuleTree, includeAuth?: boolean): string[];
export declare function moduleSourceDigests(tree: ModuleTree, prefix?: string): Record<string, string>;
export declare function assertModuleBundle(tree: ModuleTree, directory: string, paths: Readonly<Record<string, string>>): void;
