#!/usr/bin/env node
import {readFileSync} from "node:fs";
import {resolve} from "node:path";

import {loadBenchmark} from "../src/corpus.mjs";
import {packageRoot} from "../src/common.mjs";
import {createFixtureResearchProvider, runBenchmarkEvolutionCycle} from "../src/evolution-bridge.mjs";
import {diagnoseImprovement, loadImprovementReport, prepareIteration, runImprovementLoop, verifyCandidate} from "../src/improvement-loop.mjs";
import {writeImprovementReport} from "../src/improvement-report.mjs";

function parse(argv) {
  const value = {mode: "diagnose", target: null, baseline: null, output: null, max_attempts: null, fast: false, write: true, research_fixture: null};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--mode") value.mode = argv[++index];
    else if (arg === "--target") value.target = argv[++index];
    else if (arg === "--baseline") value.baseline = argv[++index];
    else if (arg === "--output") value.output = argv[++index];
    else if (arg === "--max-attempts") value.max_attempts = Number(argv[++index]);
    else if (arg === "--fast") value.fast = true;
    else if (arg === "--stdout-only") value.write = false;
    else if (arg === "--research-fixture") value.research_fixture = argv[++index];
    else if (arg === "--help") value.help = true;
    else throw new Error(`Unknown option: ${arg}`);
  }
  if (!["diagnose", "iterate", "verify-candidate", "loop", "evolution-cycle"].includes(value.mode)) throw new Error(`Unsupported mode: ${value.mode}`);
  if (value.max_attempts !== null && (!Number.isSafeInteger(value.max_attempts) || value.max_attempts < 1)) throw new Error("--max-attempts must be a positive integer");
  if (["verify-candidate", "loop"].includes(value.mode) && !value.baseline) throw new Error(`${value.mode} requires --baseline`);
  return value;
}

const options = parse(process.argv.slice(2));
if (options.help) {
  process.stdout.write("Usage: improve.mjs --mode diagnose|iterate|verify-candidate|loop|evolution-cycle [--target ID] [--baseline REPORT] [--research-fixture FILE] [--max-attempts N] [--fast] [--output PATH] [--stdout-only]\n");
  process.exit(0);
}

const benchmark = loadBenchmark(packageRoot);
const baseline = options.baseline ? loadImprovementReport(options.baseline) : null;
const target = options.target ?? baseline?.target_id ?? null;
let result;
if (options.mode === "diagnose") result = await diagnoseImprovement(benchmark, options);
else if (options.mode === "iterate") result = await prepareIteration(benchmark, target, {...options, baseline});
else if (options.mode === "verify-candidate") result = await verifyCandidate(benchmark, baseline, target, options);
else if (options.mode === "loop") result = await runImprovementLoop(benchmark, baseline, target, options);
else {
  const evolutionProfile = JSON.parse(readFileSync(new URL("../../../packages/evolution-runtime/profiles/default-v1.json", import.meta.url), "utf8"));
  const researchProviders = options.research_fixture ? [createFixtureResearchProvider(resolve(options.research_fixture))] : [];
  if (researchProviders.length > 0) evolutionProfile.research.enabled = true;
  result = await runBenchmarkEvolutionCycle(benchmark, {evolution_profile: evolutionProfile, research_providers: researchProviders, fast: options.fast});
}

const reportPath = options.write ? writeImprovementReport(result, options.output) : null;
process.stdout.write(`${JSON.stringify({...result, report_path: reportPath}, null, 2)}\n`);
process.exitCode = ["REJECT", "BLOCKED"].includes(result.status) ? 1 : 0;
