import type { NormalizedDomain } from "./model.js";
import { type DomainSpecBindings } from "./domainspec-profile.js";
export interface DomainSpecLowering {
    model: NormalizedDomain;
    bindings: DomainSpecBindings;
    files: Record<string, string>;
    trace: Record<string, unknown>;
    source_sha256: string;
    bindings_sha256: string;
    feature: string;
    symbols: Record<string, string>;
}
export declare function lowerDomainSpec(carrier: unknown, bindingInput: unknown, source: string): DomainSpecLowering;
