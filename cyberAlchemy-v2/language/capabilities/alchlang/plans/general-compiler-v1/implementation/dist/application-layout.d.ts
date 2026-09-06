export declare function writeApplicationFile(root: string, name: string, bytes: string | Buffer): void;
/** Move compiler output once; retain exact inputs and compiler evidence, not stale inventories. */
export declare function collectApplicationDomain(intermediate: string, root: string, paths: Readonly<Record<string, string>>): void;
