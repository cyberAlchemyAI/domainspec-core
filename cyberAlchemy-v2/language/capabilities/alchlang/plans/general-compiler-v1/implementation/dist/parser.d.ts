export interface ParsedDomainSource {
    carrier: Record<string, unknown>;
    source_kind: "markdown-alchlang" | "plain-alchlang";
}
export declare function parseDomainSource(markdown: string): ParsedDomainSource;
