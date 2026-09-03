#!/usr/bin/env node
import {loadBenchmark} from "../src/corpus.mjs";
import {packageRoot} from "../src/common.mjs";
import {runCoreBenchmark} from "../src/core.mjs";
import {runIntegrationBenchmark} from "../src/integration.mjs";
import {runLiveBenchmark, runLiveMultiTurnBenchmark} from "../src/live.mjs";
import {combineResults, writeReport} from "../src/report.mjs";

function options(argv) {
  const value = {mode: "core", output: null, gateway_socket: null, repetitions: null, include_live: false, write: true};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--mode") value.mode = argv[++index];
    else if (arg === "--output") value.output = argv[++index];
    else if (arg === "--gateway-socket") value.gateway_socket = argv[++index];
    else if (arg === "--repetitions") value.repetitions = Number(argv[++index]);
    else if (arg === "--include-live") value.include_live = true;
    else if (arg === "--stdout-only") value.write = false;
    else if (arg === "--help") value.help = true;
    else throw new Error(`Unknown option: ${arg}`);
  }
  if (!["core", "integration", "live", "live-multiturn", "all"].includes(value.mode)) throw new Error(`Unsupported mode: ${value.mode}`);
  if (value.repetitions !== null && (!Number.isSafeInteger(value.repetitions) || value.repetitions < 1)) throw new Error("--repetitions must be a positive integer");
  return value;
}

const selected = options(process.argv.slice(2));
if (selected.help) {
  process.stdout.write("Usage: benchmark.mjs --mode core|integration|live|live-multiturn|all [--include-live] [--gateway-socket PATH] [--repetitions N] [--output PATH] [--stdout-only]\n\n'live-multiturn' runs the opt-in persistent-conversation holdout. 'all' runs core and integration; add --include-live to invoke the original live A/B turns.\n");
  process.exit(0);
}
const benchmark = loadBenchmark(packageRoot);
let result;
if (selected.mode === "core") result = await runCoreBenchmark(benchmark);
else if (selected.mode === "integration") result = await runIntegrationBenchmark(benchmark);
else if (selected.mode === "live") result = await runLiveBenchmark(benchmark, selected);
else if (selected.mode === "live-multiturn") result = await runLiveMultiTurnBenchmark(benchmark, selected);
else {
  const results = [await runCoreBenchmark(benchmark), await runIntegrationBenchmark(benchmark)];
  if (selected.include_live) results.push(await runLiveBenchmark(benchmark, selected));
  result = combineResults(benchmark.profile, results);
}
const outputPath = selected.write ? writeReport(result, selected.output) : null;
process.stdout.write(`${JSON.stringify({...result, report_path: outputPath}, null, 2)}\n`);
process.exitCode = result.status === "FAIL" ? 1 : 0;
