import { type ParsedDomainSource } from "./parser.js";
export type AlchLangFileFormat = "canonical-alch" | "legacy-markdown";
export interface LoadedAlchLangSource extends ParsedDomainSource {
    source_path: string;
    file_format: AlchLangFileFormat;
}
export declare function loadAlchLangSource(sourcePath: string): LoadedAlchLangSource;
