#!/usr/bin/env node
import {readFileSync} from "node:fs";
import {resolve} from "node:path";
import {createEvolutionRuntime} from "../index.mjs";

function parse(argv) {
  const options = {operation: "status", input: null, profile: new URL("../profiles/default-v1.json", import.meta.url)};
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--operation") options.operation = argv[++index];
    else if (argv[index] === "--input") options.input = argv[++index];
    else if (argv[index] === "--profile") options.profile = resolve(argv[++index]);
    else if (argv[index] === "--help") options.help = true;
    else throw new Error(`Unknown option: ${argv[index]}`);
  }
  return options;
}

const options = parse(process.argv.slice(2));
if (options.help) {
  process.stdout.write("Usage: evolve.mjs --operation status|ingest [--input FILE] [--profile FILE]\n");
  process.exit(0);
}
const profile = JSON.parse(readFileSync(options.profile, "utf8"));
const runtime = createEvolutionRuntime({profile});
let result;
if (options.operation === "status") result = runtime.inspect();
else if (options.operation === "ingest") {
  if (!options.input) throw new Error("ingest requires --input");
  const signals = JSON.parse(readFileSync(resolve(options.input), "utf8"));
  result = signals.map((signal) => runtime.appendSignal(signal));
} else throw new Error(`Unsupported operation: ${options.operation}`);
process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
