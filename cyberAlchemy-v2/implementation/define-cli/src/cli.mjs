import {readFileSync, renameSync, writeFileSync} from "node:fs";
import {resolve} from "node:path";
import {createInterface} from "node:readline/promises";

import {canonicalJson, digest} from "./canonical.mjs";
import {createAppServerDefineAgent} from "./app-server-agent.mjs";
import {runDefineConversation} from "./conversation-runtime.mjs";
import {composeDefineContext} from "./context-adapter.mjs";
import {runDefineSession} from "./session-runtime.mjs";

export const HELP = `Usage:
  define [chat] [broad opening about a domain, subject, context, or project]
  define run --goal <text> --intent <text> --context <text> --consumer <id> [options]

Options:
  --model <id>         Optional Codex model override for conversational mode
  --input <path>       JSON with concepts and optional responses
  --concept <term>     Required concept; repeatable
  --output <path>      Atomically write the complete result JSON
  --json               Print canonical JSON only
  --help               Show this help

Conversation review actions:
  accept | discuss | edit | open/defer | quit

Advanced scripted responses:
  propose <meaning> | reuse <definition-ref> | specialize <ref> :: <scope>
  open [reason] | defer [reason] | refuse [reason]

The default flow uses the Codex app-server wrapper in an ephemeral read-only thread.
It starts broadly, confirms scope, and reviews candidate meaning options one at a time.
All state is in-memory and non-authorizing.`;

function parseArgs(argv) {
  const result = {mode: "chat", concepts: [], opening_parts: [], json: false};
  const args = [...argv];
  if (args[0] === "run") {
    result.mode = "run";
    args.shift();
  } else if (args[0] === "chat") {
    args.shift();
  }
  while (args.length > 0) {
    const flag = args.shift();
    if (flag === "--help" || flag === "-h") result.help = true;
    else if (flag === "--json") result.json = true;
    else if (["--goal", "--intent", "--context", "--consumer", "--input", "--output", "--concept", "--model"].includes(flag)) {
      const value = args.shift();
      if (value === undefined || value.startsWith("--")) throw new Error(`define-cli.value-required:${flag}`);
      if (flag === "--concept") result.concepts.push(value);
      else result[flag.slice(2)] = value;
    } else if (!flag.startsWith("-") && result.mode === "chat") result.opening_parts.push(flag);
    else throw new Error(`define-cli.unknown-option:${flag}`);
  }
  result.opening = result.opening_parts.join(" ").trim();
  return result;
}

function responseFromLine(conceptId, line) {
  const trimmed = line.trim();
  const [actionRaw, ...rest] = trimmed.split(/\s+/);
  const action = (actionRaw || "open").toLowerCase();
  const text = rest.join(" ").trim();
  if (action === "propose") return {concept_id: conceptId, action, payload: {definition: text}};
  if (action === "reuse") return {concept_id: conceptId, action, payload: {definition_ref: text}};
  if (action === "specialize") {
    const [base_definition_ref, scope] = text.split("::").map((part) => part.trim());
    return {concept_id: conceptId, action, payload: {base_definition_ref, scope}};
  }
  if (["open", "defer", "refuse"].includes(action)) return {concept_id: conceptId, action, payload: {reason: text || undefined}};
  throw new Error(`define-cli.unsupported-response:${action}`);
}

async function collectInteractive(options, input, output) {
  const terminal = Boolean(input.isTTY && output.isTTY);
  if (!terminal) throw new Error("define-cli.input-required-in-noninteractive-mode");
  const readline = createInterface({input, output});
  try {
    if (options.concepts.length === 0) {
      const value = await readline.question("Required concepts (comma-separated): ");
      options.concepts = value.split(",").map((item) => item.trim()).filter(Boolean);
    }
    const concepts = options.concepts.map((term) => ({term}));
    const normalizedIds = concepts.map((concept) => `concept:${digest(concept.term).slice(0, 16)}`);
    const responses = [];
    for (let index = 0; index < concepts.length; index += 1) {
      const line = await readline.question(`What should "${concepts[index].term}" mean? `);
      responses.push(responseFromLine(normalizedIds[index], line));
    }
    return {concepts, responses};
  } finally {
    readline.close();
  }
}

function atomicWrite(path, value) {
  const target = resolve(path);
  const temporary = `${target}.define-cli.tmp`;
  writeFileSync(temporary, `${canonicalJson(value)}\n`, {encoding: "utf8", mode: 0o600});
  renameSync(temporary, target);
  return target;
}

export async function runDefineCli(argv, environment = {}) {
  const stdout = environment.stdout ?? process.stdout;
  const stderr = environment.stderr ?? process.stderr;
  const stdin = environment.stdin ?? process.stdin;
  const repositoryRoot = environment.repositoryRoot ?? resolve(import.meta.dirname, "../../../..");
  let options;
  try {
    options = parseArgs(argv);
  } catch (error) {
    stderr.write(`${error.message}\n${HELP}\n`);
    return 2;
  }
  if (options.help) {
    stdout.write(`${HELP}\n`);
    return 0;
  }
  if (options.mode === "chat") {
    if (!options.opening && !stdin.isTTY && typeof environment.ask !== "function") {
      stderr.write(`define-cli.conversation-requires-opening-or-terminal\n${HELP}\n`);
      return 2;
    }
    const readline = typeof environment.ask === "function" ? null : createInterface({input: stdin, output: stdout});
    const ask = environment.ask ?? ((question) => readline.question(question));
    const write = environment.write ?? ((text) => stdout.write(text));
    let agent = environment.agent ?? null;
    let result;
    try {
      const opening = options.opening || String(await ask("What are you working on? You can begin with a domain, subject, context, or project.\n> ") ?? "").trim();
      if (!opening) {
        result = {ok: false, stopped: true, reason_codes: ["define-conversation.opening-required"], authority_effect: "none"};
      } else {
        const createAgent = environment.agent_factory ?? createAppServerDefineAgent;
        agent ??= createAgent({repository_root: repositoryRoot, model: options.model});
        result = await runDefineConversation({
          agent,
          ask,
          write,
          opening,
          consumer: options.consumer ?? "human:define-cli",
          repository_root: repositoryRoot,
        });
      }
    } catch (error) {
      stderr.write(`${error.message}\n`);
      return 3;
    } finally {
      readline?.close();
      await agent?.close?.();
    }
    if (!result.ok) {
      write(`\nDefine stopped: ${(result.reason_codes ?? ["unknown"]).join(", ")}\n`);
      if (options.json) stdout.write(`${canonicalJson(result)}\n`);
      return 4;
    }
    let outputPath = null;
    if (options.output) outputPath = atomicWrite(options.output, result);
    if (options.json) stdout.write(`${canonicalJson(result)}\n`);
    else {
      const pack = result.definition_pack;
      write([
        "\nCandidate Definition Pack created.",
        `  Pack: ${pack.pack_id}`,
        `  Reviewed concepts: ${pack.required_concepts.length}`,
        `  Open questions: ${pack.open_questions.length}`,
        `  Status: ${result.session.state}`,
        outputPath ? `  Saved: ${outputPath}` : "  Not saved; use --output <path> to retain the full JSON.",
        "  Authority effect: none",
        "",
      ].join("\n"));
    }
    return result.validation.handoff_ready ? 0 : 4;
  }
  const missing = ["goal", "intent", "context", "consumer"].filter((key) => !String(options[key] ?? "").trim());
  if (missing.length > 0) {
    stderr.write(`define-cli.required-options:${missing.join(",")}\n`);
    return 2;
  }
  let scripted = null;
  try {
    if (options.input) scripted = JSON.parse(readFileSync(resolve(options.input), "utf8"));
    else if (options.concepts.length === 0 || stdin.isTTY) scripted = await collectInteractive(options, stdin, stdout);
    else scripted = {concepts: options.concepts, responses: []};
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  const concepts = Array.isArray(scripted.concepts) && scripted.concepts.length > 0 ? scripted.concepts : options.concepts;
  const contextResult = composeDefineContext(options, repositoryRoot);
  if (!contextResult.ok) {
    stderr.write(`${canonicalJson(contextResult)}\n`);
    return 3;
  }
  const result = runDefineSession({...options, concepts, responses: scripted.responses, context_result: contextResult});
  if (!result.ok) {
    stderr.write(`${canonicalJson(result)}\n`);
    return 3;
  }
  if (options.output) result.output_path = atomicWrite(options.output, result);
  stdout.write(`${canonicalJson(result)}\n`);
  return result.validation.handoff_ready ? 0 : 4;
}
