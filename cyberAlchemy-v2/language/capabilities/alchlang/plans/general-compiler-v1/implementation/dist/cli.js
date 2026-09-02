#!/usr/bin/env node
import { readFileSync } from "node:fs";
import path from "node:path";
import { MemoryActionAdapter } from "./adapters.js";
import { compileCarrier } from "./index.js";
import { parseDomainSource } from "./parser.js";
import { executeAction } from "./runtime.js";
import { writeCompilation } from "./writer.js";
import { listOperationPatterns, requireGeneratablePattern } from "./pattern-registry.js";
import { writeRegistryCompilation } from "./registry-compiler.js";
function option(args, name) { const index = args.indexOf(name); return index === -1 ? undefined : args[index + 1]; }
function usage() {
    console.error("Usage:\n  domainspec build <domain.md> [--out generated] [--force]\n  domainspec run <domain.md> <action> --actor <actor> --facts '<json>' --grant <boundary>\n  domainspec registry build --config <registry-compiler.config.json>\n  domainspec patterns [--available|--blocked]\n  domainspec pattern <pattern-id>");
    process.exit(2);
}
async function main() {
    const [, , command, ...args] = process.argv;
    if (command === "registry" && args[0] === "build") {
        const config = option(args, "--config");
        if (!config)
            usage();
        const result = writeRegistryCompilation(config);
        console.log(JSON.stringify({ status: "built", patterns: result.registry.patterns.length, available: result.registry.patterns.filter((pattern) => pattern.availability === "available").length, authority_effect: "none" }, null, 2));
        return;
    }
    if (command === "patterns") {
        const filter = args.includes("--available") ? "available" : args.includes("--blocked") ? "blocked" : "all";
        console.log(JSON.stringify({ schema_version: "cav2.alchlang.operation-pattern-list/v1-candidate", patterns: listOperationPatterns(filter), authority_effect: "none" }, null, 2));
        return;
    }
    if (command === "pattern") {
        const patternId = args[0];
        if (!patternId)
            usage();
        console.log(JSON.stringify({ status: "generatable", pattern: requireGeneratablePattern(patternId), authority_effect: "none" }, null, 2));
        return;
    }
    if (command === "build") {
        const sourcePath = args[0];
        if (!sourcePath || sourcePath.startsWith("--"))
            usage();
        const parsed = parseDomainSource(readFileSync(sourcePath, "utf8"));
        const result = compileCarrier(parsed.carrier);
        const receipt = writeCompilation(result, option(args, "--out") ?? path.resolve(process.cwd(), "generated"), { force: args.includes("--force"), carrier: parsed.carrier });
        console.log(JSON.stringify({ status: "built", source: path.resolve(sourcePath), ...receipt, authority_effect: "none" }, null, 2));
        return;
    }
    if (command === "run") {
        const [sourcePath, actionId] = args;
        if (!sourcePath || !actionId)
            usage();
        const actor = option(args, "--actor");
        const factsText = option(args, "--facts");
        const grant = option(args, "--grant");
        if (!actor || !factsText || !grant)
            usage();
        const parsed = parseDomainSource(readFileSync(sourcePath, "utf8"));
        const compiled = compileCarrier(parsed.carrier);
        const action = compiled.plan.model.actions.find((item) => item.id === actionId);
        if (!action)
            throw new Error(`ACTION_NOT_FOUND:${actionId}`);
        const adapter = new MemoryActionAdapter({ outcome: "completed", emitted_events: action.outcome_refs });
        const result = await executeAction(compiled.plan.model, { action_id: actionId, actor_ref: actor, facts: JSON.parse(factsText), authority_grants: [grant] }, { [actionId]: adapter });
        console.log(JSON.stringify(result, null, 2));
        return;
    }
    usage();
}
main().catch((error) => { console.error(error instanceof Error ? error.message : String(error)); process.exit(1); });
