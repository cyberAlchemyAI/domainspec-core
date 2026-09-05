#!/usr/bin/env node
import {spawn} from "node:child_process";
import {resolve} from "node:path";

import {inspectProduct, materializeProductClosure, productRoot} from "../src/product.mjs";
import {inspectFrozenProductCandidate} from "../src/product-candidate.mjs";

function usage() {
  process.stderr.write("Usage: are doctor [--json] | closure [--json] | candidate freeze | candidate inspect [--json] | test | gateway <gateway-options> | benchmark <benchmark-options> | improve inspect --report <file> | improve run-canary [--output <file>] | define <define-options> | coding-agent demo [--approve] [--keep] [--fault-after-effect] | coding-agent live-demo [--codex-command <path>] [--model <id>] [--approve] [--keep]\n");
}

function run(script, args) {
  const child = spawn(process.execPath, [script, ...args], {stdio: "inherit"});
  for (const signal of ["SIGINT", "SIGTERM"]) process.once(signal, () => child.kill(signal));
  child.once("exit", (code, signal) => process.exit(signal ? 1 : (code ?? 1)));
}

const [command, ...args] = process.argv.slice(2);
if (command === "doctor") {
  const health = inspectProduct({require_exact_runtime: true});
  if (args.includes("--json")) process.stdout.write(`${JSON.stringify(health, null, 2)}\n`);
  else process.stdout.write(`ARE ${health.product_version}: ${health.status}\n${health.reason_codes.join("\n")}\n`);
  process.exitCode = health.status === "PASS" ? 0 : 1;
} else if (command === "closure") {
  const closure = materializeProductClosure();
  process.stdout.write(args.includes("--json") ? `${JSON.stringify(closure, null, 2)}\n` : `${closure.closure_digest}  ${closure.files.length} files\n`);
} else if (command === "test") {
  run(resolve(productRoot, "scripts/test-all.mjs"), args);
} else if (command === "candidate" && args[0] === "freeze") {
  run(resolve(productRoot, "scripts/freeze-tested-product-candidate.mjs"), args.slice(1));
} else if (command === "candidate" && args[0] === "inspect") {
  const inspection = inspectFrozenProductCandidate();
  if (args.includes("--json")) process.stdout.write(`${JSON.stringify(inspection, null, 2)}\n`);
  else process.stdout.write(`ARE ${inspection.candidate?.candidate_id ?? "candidate"}: ${inspection.status}\n${inspection.reason_codes.join("\n")}\n`);
  process.exitCode = inspection.status === "PASS" ? 0 : 1;
} else if (command === "gateway") {
  run(resolve(productRoot, "packages/codex-app-server-wrapper/bin/are-codex-gateway.mjs"), args);
} else if (command === "benchmark") {
  run(resolve(productRoot, "benchmarks/real-reasoning-v1/bin/benchmark.mjs"), args);
} else if (command === "improve") {
  run(resolve(productRoot, "benchmarks/real-reasoning-v1/bin/improve.mjs"), args);
} else if (command === "define") {
  run(resolve(productRoot, "../define-cli/bin/define.mjs"), args);
} else if (command === "coding-agent" && args[0] === "demo") {
  run(resolve(productRoot, "packages/coding-agent-runtime/bin/demo.mjs"), args.slice(1));
} else if (command === "coding-agent" && args[0] === "live-demo") {
  run(resolve(productRoot, "packages/coding-agent-runtime/bin/live-demo.mjs"), args.slice(1));
} else {
  usage();
  process.exitCode = 2;
}
