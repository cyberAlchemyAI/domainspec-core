import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import path from "node:path";
const canonical = (value) => Array.isArray(value)
    ? `[${value.map(canonical).join(",")}]`
    : value && typeof value === "object"
        ? `{${Object.entries(value).sort(([a], [b]) => a.localeCompare(b)).map(([key, item]) => `${JSON.stringify(key)}:${canonical(item)}`).join(",")}}`
        : JSON.stringify(value);
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
function unique(rows, identity, label) {
    const result = new Map();
    for (const row of rows) {
        const id = identity(row);
        if (!id || result.has(id))
            throw new Error(`REGISTRY_DUPLICATE_OR_EMPTY_ID:${label}:${id}`);
        result.set(id, row);
    }
    return result;
}
export function compileOperationPatternRegistry(input) {
    const bindings = unique(input.integration_bindings, (row) => row.binding_id, "binding");
    const generators = unique(input.generators, (row) => row.generator_id, "generator");
    const conformance = unique(input.conformance, (row) => row.conformance_id, "conformance");
    unique(input.pattern_intents, (row) => row.pattern_id, "pattern-intent");
    const admitted = new Set(input.admitted_meta_types);
    const patterns = [...input.pattern_intents].sort((a, b) => a.pattern_id.localeCompare(b.pattern_id)).map((intent) => {
        const binding = bindings.get(intent.integration_binding_ref);
        const generator = generators.get(intent.generator_ref);
        const proof = conformance.get(intent.conformance_ref);
        const bindingDigest = input.resolved_binding_digests[intent.integration_binding_ref];
        const generatorDigest = input.resolved_generator_digests[intent.generator_ref];
        const blockers = [];
        const metaStatus = admitted.has(intent.meta_type_ref) ? "closed" : "missing";
        if (metaStatus !== "closed")
            blockers.push(`META_TYPE_NOT_ADMITTED:${intent.meta_type_ref}`);
        const bindingStatus = !binding ? "missing" : binding.status === "closed" && bindingDigest === binding.manifest_sha256 ? "closed" : "open";
        if (!binding)
            blockers.push(`BINDING_NOT_REGISTERED:${intent.integration_binding_ref}`);
        else if (binding.status !== "closed")
            blockers.push(`BINDING_NOT_CLOSED:${binding.binding_id}`);
        else if (bindingDigest !== binding.manifest_sha256)
            blockers.push(`BINDING_DIGEST_DRIFT:${binding.binding_id}`);
        const generatorStatus = !generator ? "missing" : generator.status === "closed" && generatorDigest === generator.source_tree_sha256 ? "closed" : "open";
        if (!generator)
            blockers.push(`GENERATOR_NOT_REGISTERED:${intent.generator_ref}`);
        else if (generator.status !== "closed")
            blockers.push(`GENERATOR_NOT_CLOSED:${generator.generator_id}`);
        else if (generatorDigest !== generator.source_tree_sha256)
            blockers.push(`GENERATOR_DIGEST_DRIFT:${generator.generator_id}`);
        const proofClosed = proof?.status === "PASS"
            && proof.generator_ref === intent.generator_ref
            && proof.binding_ref === intent.integration_binding_ref
            && proof.generator_sha256 === generatorDigest
            && proof.binding_sha256 === bindingDigest;
        const conformanceStatus = !proof ? "missing" : proofClosed ? "closed" : "open";
        if (!proof)
            blockers.push(`CONFORMANCE_NOT_REGISTERED:${intent.conformance_ref}`);
        else if (proof.status !== "PASS")
            blockers.push(`CONFORMANCE_NOT_PASSING:${proof.conformance_id}`);
        else if (!proofClosed)
            blockers.push(`CONFORMANCE_EVIDENCE_STALE:${proof.conformance_id}`);
        const availability = [metaStatus, bindingStatus, generatorStatus, conformanceStatus].every((status) => status === "closed") ? "available" : "blocked";
        return {
            pattern_id: intent.pattern_id,
            architecture_pattern_status: intent.architecture_pattern_status,
            meta_type: { id: intent.meta_type_ref, status: metaStatus },
            integration_binding: { id: intent.integration_binding_ref, status: bindingStatus },
            generator: { id: intent.generator_ref, status: generatorStatus },
            conformance: { id: intent.conformance_ref, status: conformanceStatus },
            availability,
            generated_artifacts: [...intent.generated_artifacts],
            blockers
        };
    });
    return { schema_version: "cav2.alchlang.operation-pattern-registry/v2-candidate", registry_id: "cav2.alchlang.operation-patterns", patterns, authority_effect: "none" };
}
function loadJson(file) { return JSON.parse(readFileSync(file, "utf8")); }
function resolveRef(configPath, ref) { return path.resolve(path.dirname(configPath), ref); }
function digestSourceTree(configPath, refs) {
    return sha256(`${[...refs].sort().map((ref) => `${ref}:${sha256(readFileSync(resolveRef(configPath, ref)))}`).join("\n")}\n`);
}
export function compileRegistryConfig(configPathInput) {
    const configPath = path.resolve(configPathInput);
    const config = loadJson(configPath);
    if (config.schema_version !== "cav2.alchlang.registry-compiler-config/v1-candidate")
        throw new Error(`REGISTRY_CONFIG_VERSION:${config.schema_version}`);
    const baselinePath = resolveRef(configPath, config.sources.meta_type_baseline.ref);
    const baselineBytes = readFileSync(baselinePath);
    if (sha256(baselineBytes) !== config.sources.meta_type_baseline.sha256)
        throw new Error("REGISTRY_SOURCE_DIGEST_DRIFT:meta-type-baseline");
    const baseline = JSON.parse(baselineBytes.toString("utf8"));
    const admittedMetaTypes = baseline.status === "owner-admitted-frozen" && baseline.operation_contract?.meta_type_id ? [baseline.operation_contract.meta_type_id] : [];
    const intents = loadJson(resolveRef(configPath, config.sources.pattern_intents.ref));
    const bindingRows = loadJson(resolveRef(configPath, config.sources.integration_bindings.ref));
    const generatorRows = loadJson(resolveRef(configPath, config.sources.generators.ref));
    const proofRows = loadJson(resolveRef(configPath, config.sources.conformance.ref));
    const bindingDigests = Object.fromEntries(bindingRows.bindings.map((row) => [row.binding_id, sha256(readFileSync(resolveRef(configPath, row.manifest_ref)))]));
    const generatorDigests = Object.fromEntries(generatorRows.generators.map((row) => [row.generator_id, digestSourceTree(configPath, row.source_refs)]));
    const registry = compileOperationPatternRegistry({ admitted_meta_types: admittedMetaTypes, pattern_intents: intents.patterns, integration_bindings: bindingRows.bindings, generators: generatorRows.generators, conformance: proofRows.conformance, resolved_binding_digests: bindingDigests, resolved_generator_digests: generatorDigests });
    const registryBytes = json(registry);
    const inputDigests = Object.fromEntries(Object.entries(config.sources).map(([id, source]) => [id, sha256(readFileSync(resolveRef(configPath, source.ref)))]));
    const receipt = {
        schema_version: "cav2.alchlang.registry-compilation-receipt/v1-candidate",
        inputs: inputDigests,
        resolved_binding_digests: bindingDigests,
        resolved_generator_digests: generatorDigests,
        output_registry_sha256: sha256(registryBytes),
        deterministic_replay: "PASS",
        authority_effect: "none",
        claim_ceiling: "Candidate registry compilation only; availability is technical closure, not stability, admission, release, deployment, or execution authority."
    };
    return { registry, receipt, typescript_projection: `import type { OperationPattern } from "../registry-compiler.js";\n\nexport const generatedOperationPatterns = ${JSON.stringify(registry.patterns, null, 2)} as const satisfies readonly OperationPattern[];\n` };
}
function writeAtomic(target, bytes) {
    mkdirSync(path.dirname(target), { recursive: true });
    const temporary = `${target}.tmp`;
    writeFileSync(temporary, bytes);
    renameSync(temporary, target);
}
export function writeRegistryCompilation(configPathInput) {
    const configPath = path.resolve(configPathInput);
    const config = loadJson(configPath);
    const result = compileRegistryConfig(configPath);
    writeAtomic(resolveRef(configPath, config.outputs.registry), json(result.registry));
    writeAtomic(resolveRef(configPath, config.outputs.receipt), json(result.receipt));
    writeAtomic(resolveRef(configPath, config.outputs.typescript_projection), result.typescript_projection);
    return result;
}
