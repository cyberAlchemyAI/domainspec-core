#!/usr/bin/env node
import { readFileSync } from "node:fs";
import path from "node:path";
import { MemoryActionAdapter } from "./adapters.js";
import { SqliteTransactionalOutboxActionAdapter } from "./effect-adapters.js";
import { compileCarrier } from "./index.js";
import { loadAlchLangSource } from "./source-file.js";
import { executeAction } from "./runtime.js";
import { validateAtomicStateAndOutboxRequest } from "./sqlite-outbox-runtime.js";
import { DurableOutboxWorker, DurableSqliteTransactionalOutbox, type DurableOutboxRecord, type DurableOutboxTransport, type DurableOutboxStatus } from "./durable-outbox-runtime.js";
import { FetchOutboxHttpClient, HttpOutboxTransport } from "./outbox-integrations.js";
import { writeCompilation } from "./writer.js";
import { listOperationPatterns, requireGeneratablePattern } from "./pattern-registry.js";
import { writeRegistryCompilation } from "./registry-compiler.js";

function option(args: string[], name: string): string | undefined { const index = args.indexOf(name); return index === -1 ? undefined : args[index + 1]; }
function positiveInteger(value: string | undefined, fallback: number): number {
  if (value === undefined) return fallback;
  const parsed = Number(value);
  if (!Number.isSafeInteger(parsed) || parsed < 1) throw new Error(`INVALID_POSITIVE_INTEGER:${value}`);
  return parsed;
}
function usage(): never {
  console.error("Usage:\n  domainspec check <domain.alch>\n  domainspec build <domain.alch> [--out generated] [--force]\n  domainspec run <domain.alch> <action> --actor <actor> --facts '<json>' --grant <boundary> --adapter memory\n  domainspec run <domain.alch> <action> --actor <actor> --facts '<json>' --grant <boundary> --binding sqlite-transactional-outbox --database <path> --effect-request-file <json>\n  domainspec outbox pending|status --database <path> [--status pending|leased|published|dead]\n  domainspec outbox dispatch --database <path> --transport stdout --worker-id <id> [--now <ISO>]\n  domainspec outbox dispatch --database <path> --transport http --worker-id <id> --endpoint <url> --allow-origin <origin> --confirm-network-dispatch <origin>\n  domainspec outbox requeue-dead --database <path> --message-id <id> --now <ISO>\n  domainspec registry build --config <registry-compiler.config.json>\n  domainspec patterns [--available|--blocked]\n  domainspec pattern <pattern-id>\n\nCanonical source files use .alch. A fenced .md file is supported only for legacy compatibility.");
  process.exit(2);
}

async function main(): Promise<void> {
  const [, , command, ...args] = process.argv;
  if (command === "registry" && args[0] === "build") {
    const config = option(args, "--config"); if (!config) usage();
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
    const patternId = args[0]; if (!patternId) usage();
    console.log(JSON.stringify({ status: "generatable", pattern: requireGeneratablePattern(patternId), authority_effect: "none" }, null, 2));
    return;
  }
  if (command === "check") {
    const sourcePath = args[0]; if (!sourcePath || sourcePath.startsWith("--")) usage();
    const loaded = loadAlchLangSource(sourcePath);
    const result = compileCarrier(loaded.carrier);
    console.log(JSON.stringify({ status: "valid", source: loaded.source_path, file_format: loaded.file_format, domain_id: result.plan.model.domain_id, plan_digest: result.plan_digest, authority_effect: "none" }, null, 2));
    return;
  }
  if (command === "build") {
    const sourcePath = args[0]; if (!sourcePath || sourcePath.startsWith("--")) usage();
    const parsed = loadAlchLangSource(sourcePath);
    const result = compileCarrier(parsed.carrier);
    const receipt = writeCompilation(result, option(args, "--out") ?? path.resolve(process.cwd(), "generated"), { force: args.includes("--force"), carrier: parsed.carrier });
    console.log(JSON.stringify({ status: "built", source: path.resolve(sourcePath), ...receipt, authority_effect: "none" }, null, 2));
    return;
  }
  if (command === "outbox") {
    const operation = args[0];
    const databasePath = option(args, "--database");
    if (!databasePath || !["pending","status","dispatch","requeue-dead"].includes(operation ?? "")) usage();
    const limit = positiveInteger(option(args, "--limit"), 100);
    const outbox = new DurableSqliteTransactionalOutbox(databasePath);
    try {
      if (operation === "pending" || operation === "status") {
        const selected = option(args,"--status") as DurableOutboxStatus|undefined;
        if(selected && !["pending","leased","published","dead"].includes(selected)) throw new Error(`OUTBOX_STATUS_INVALID:${selected}`);
        console.log(JSON.stringify({ status: "inspected", database: path.resolve(databasePath), messages: outbox.records(selected??(operation==="pending"?"pending":undefined),limit), stats: outbox.stats(), schema_version:outbox.schemaVersion(), authority_effect: "none" }, null, 2));
        return;
      }
      if(operation === "requeue-dead"){const id=option(args,"--message-id"),now=option(args,"--now");if(!id||!now)usage();outbox.requeueDead(id,now);console.log(JSON.stringify({status:"requeued",message_id:id,stats:outbox.stats(),authority_effect:"local-sqlite-write"},null,2));return;}
      const transportId = option(args, "--transport");
      const workerId=option(args,"--worker-id");if(!workerId)usage();const now=option(args,"--now")??new Date().toISOString();
      const collected:DurableOutboxRecord[]=[];let transport:DurableOutboxTransport;let authorityEffect="local-stdout-only";
      if(transportId==="stdout")transport={async publish(message){collected.push(structuredClone(message));}};
      else if(transportId==="http"){const endpoint=option(args,"--endpoint"),origin=option(args,"--allow-origin"),confirmation=option(args,"--confirm-network-dispatch");if(!endpoint||!origin||confirmation!==origin||new URL(endpoint).origin!==origin)throw new Error("OUTBOX_HTTP_CONFIRMATION_REQUIRED");transport=new HttpOutboxTransport(endpoint,new FetchOutboxHttpClient([origin]));authorityEffect="explicit-confirmed-http-dispatch";}
      else throw new Error(`OUTBOX_TRANSPORT_UNSUPPORTED:${transportId??"missing"}`);
      const result = await new DurableOutboxWorker(outbox,transport,{workerId,clock:()=>now,leaseMs:positiveInteger(option(args,"--lease-ms"),30000),retryBaseMs:positiveInteger(option(args,"--retry-base-ms"),1000)}).dispatch(limit);
      console.log(JSON.stringify({ status: "dispatched", transport: transportId, messages: collected, result, stats: outbox.stats(), authority_effect: authorityEffect }, null, 2));
      return;
    } finally {
      outbox.close();
    }
  }
  if (command === "run") {
    const [sourcePath, actionId] = args; if (!sourcePath || !actionId) usage();
    const actor = option(args, "--actor"); const factsText = option(args, "--facts"); const grant = option(args, "--grant");
    if (!actor || !factsText || !grant) usage();
    const parsed = loadAlchLangSource(sourcePath); const compiled = compileCarrier(parsed.carrier);
    const action = compiled.plan.model.actions.find((item) => item.id === actionId); if (!action) throw new Error(`ACTION_NOT_FOUND:${actionId}`);
    const bindingId = option(args, "--binding");
    if (bindingId) {
      const databasePath = option(args, "--database"); const requestPath = option(args, "--effect-request-file");
      if (!databasePath || !requestPath) usage();
      const effectRequest: unknown = JSON.parse(readFileSync(requestPath, "utf8"));
      validateAtomicStateAndOutboxRequest(effectRequest);
      const failpointText = option(args, "--failpoint");
      if (failpointText && failpointText !== "after-state-write") throw new Error(`OUTBOX_FAILPOINT_UNSUPPORTED:${failpointText}`);
      const adapter = SqliteTransactionalOutboxActionAdapter.open({ model: compiled.plan.model, actionId, bindingId, databasePath, effectRequest, failpoint: failpointText as "after-state-write" | undefined });
      try {
        const result = await executeAction(compiled.plan.model, { action_id: actionId, actor_ref: actor, facts: JSON.parse(factsText), authority_grants: [grant] }, { [actionId]: adapter });
        console.log(JSON.stringify({ ...result, database: path.resolve(databasePath), outbox: adapter.outbox.stats(), authority_effect: "local-sqlite-write" }, null, 2));
      } finally {
        adapter.close();
      }
      return;
    }
    if (action.performs.length > 0) throw new Error(`EFFECT_BINDING_REQUIRED:${actionId}`);
    if (option(args, "--adapter") !== "memory") throw new Error(`ACTION_ADAPTER_REQUIRED:${actionId}`);
    const adapter = new MemoryActionAdapter({ outcome: "completed", emitted_events: action.outcome_refs });
    const result = await executeAction(compiled.plan.model, { action_id: actionId, actor_ref: actor, facts: JSON.parse(factsText), authority_grants: [grant] }, { [actionId]: adapter });
    console.log(JSON.stringify({ ...result, authority_effect: "none" }, null, 2));
    return;
  }
  usage();
}

main().catch((error: unknown) => { console.error(error instanceof Error ? error.message : String(error)); process.exit(1); });
