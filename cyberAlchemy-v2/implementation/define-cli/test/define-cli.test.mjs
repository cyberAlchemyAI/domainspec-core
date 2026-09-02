import assert from "node:assert/strict";
import {EventEmitter} from "node:events";
import {mkdtempSync, readFileSync, rmSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";
import {PassThrough} from "node:stream";
import test from "node:test";

import {composeDefineContext, createAppServerDefineAgent, runDefineCli, runDefineConversation, runDefineSession, validateDefinitionPack} from "../index.mjs";

const repositoryRoot = resolve(import.meta.dirname, "../../../..");
const fixture = resolve(import.meta.dirname, "../fixtures/smoke-input.json");
const scope = {
  goal: "Define a release channel",
  intent: "Remove ambiguity for a local consumer",
  context: "A release channel names how candidate output reaches a consumer.",
  consumer: "define-cli-test",
};

function capture() {
  const stream = new PassThrough();
  let value = "";
  stream.on("data", (chunk) => { value += chunk.toString("utf8"); });
  return {stream, value: () => value};
}

function scopeReview(options) {
  return {
    schema_version: "cav2.define-conversation-turn/v1",
    phase: "scope-review",
    message: "I can now reflect the scope back before we examine its meaning.",
    question: null,
    scope_ready: true,
    scope: {
      domain: "knowledge systems",
      subject: "shared vocabulary",
      project: "Atlas",
      context: "Teams currently use overlapping terms.",
      desired_outcome: "Create a consistent bounded vocabulary",
      intent: "Reduce ambiguity between teams",
      consumer: "atlas-team",
    },
    options,
  };
}

function option(id, term, meaning) {
  return {option_id: id, term, question: `What should ${term} mean?`, why_it_matters: `${term} changes how teams communicate.`, candidate_definition: meaning, boundary: "Candidate meaning for Atlas only."};
}

function scriptedAnswers(values) {
  const queue = [...values];
  return async () => queue.shift() ?? "";
}

test("ARE composition selects Define and projects inline meaning", () => {
  const result = composeDefineContext(scope, repositoryRoot);
  assert.equal(result.ok, true);
  assert.equal(result.route_decision.selected.route_id, "CA2-ROUTE-DEFINE");
  assert.equal(result.context_envelope.authority_effect, "none");
  assert.ok(result.context_envelope.included_items.some((item) => item.context_item_id === "definition:CAV2-DEFINE-CAND-001" && item.content.text.includes("CyberAlchemy Define")));
  assert.ok(result.context_envelope.included_items.some((item) => item.context_item_id === "ontology-node:define-session-runtime.CliInterface" && item.content.intent));
  assert.ok(result.context_envelope.inline_bytes <= 32 * 1024);
});

test("same selected sources and request produce byte-stable context", () => {
  const first = composeDefineContext(scope, repositoryRoot);
  const second = composeDefineContext(scope, repositoryRoot);
  assert.deepEqual(second, first);
});

test("session produces exactly one candidate disposition per concept", () => {
  const contextResult = composeDefineContext(scope, repositoryRoot);
  const result = runDefineSession({
    ...scope,
    context_result: contextResult,
    concepts: [{concept_id: "concept:channel", term: "release channel"}],
    responses: [{concept_id: "concept:channel", action: "propose", payload: {definition: "A named candidate delivery path."}}],
  });
  assert.equal(result.ok, true);
  assert.equal(result.definition_pack.concept_dispositions.length, 1);
  assert.equal(result.definition_pack.concept_dispositions[0].disposition, "propose");
  assert.equal(result.validation.handoff_ready, true);
  assert.deepEqual(validateDefinitionPack(result.definition_pack), result.validation);
});

test("defer preserves an open question and never invents a definition", () => {
  const contextResult = composeDefineContext(scope, repositoryRoot);
  const result = runDefineSession({
    ...scope,
    context_result: contextResult,
    concepts: [{concept_id: "concept:channel", term: "release channel"}],
    responses: [{concept_id: "concept:channel", action: "defer", payload: {reason: "Owner unavailable"}}],
  });
  assert.equal(result.ok, true);
  assert.equal(result.definition_pack.concept_dispositions[0].disposition, "open");
  assert.equal(result.definition_pack.concept_dispositions[0].candidate_definition, undefined);
  assert.equal(result.validation.handoff_ready, false);
  assert.equal(result.session.state, "blocked-open-meaning");
});

test("CLI scripted canary writes deterministic result only when explicitly requested", async () => {
  const directory = mkdtempSync(join(tmpdir(), "define-cli-test-"));
  try {
    const outputPath = join(directory, "pack.json");
    const stdout = capture();
    const stderr = capture();
    const code = await runDefineCli([
      "run", "--goal", scope.goal, "--intent", scope.intent, "--context", scope.context,
      "--consumer", scope.consumer, "--input", fixture, "--output", outputPath, "--json",
    ], {repositoryRoot, stdin: new PassThrough(), stdout: stdout.stream, stderr: stderr.stream});
    assert.equal(code, 0, stderr.value());
    assert.equal(stderr.value(), "");
    const written = JSON.parse(readFileSync(outputPath, "utf8"));
    const displayed = JSON.parse(stdout.value());
    delete displayed.output_path;
    assert.deepEqual(displayed, written);
    assert.equal(written.route.route_id, "CA2-ROUTE-DEFINE");
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});

test("CLI preserves unresolved non-interactive concepts with exit code 4", async () => {
  const stdout = capture();
  const stderr = capture();
  const code = await runDefineCli([
    "run", "--goal", scope.goal, "--intent", scope.intent, "--context", scope.context,
    "--consumer", scope.consumer, "--concept", "release channel", "--json",
  ], {repositoryRoot, stdin: new PassThrough(), stdout: stdout.stream, stderr: stderr.stream});
  assert.equal(code, 4, stderr.value());
  const result = JSON.parse(stdout.value());
  assert.equal(result.validation.handoff_ready, false);
  assert.equal(result.definition_pack.open_questions.length, 1);
});

test("conversation starts broadly, confirms scope, and reviews options one at a time", async () => {
  const seen = [];
  const agent = {
    respond: async (request) => {
      seen.push(request);
      return scopeReview([
        option("option:vocabulary", "shared vocabulary", "The bounded set of terms used consistently by Atlas teams."),
        option("option:term-owner", "term owner", "The role responsible for answering challenges about one term."),
      ]);
    },
  };
  const output = [];
  const result = await runDefineConversation({
    agent,
    ask: scriptedAnswers(["yes", "accept", "open", "Owner is not identified", "yes"]),
    write: (text) => output.push(text),
    opening: "We are building Atlas, a knowledge system, and teams use inconsistent language.",
    consumer: "human:define-cli",
    repository_root: repositoryRoot,
  });
  assert.equal(seen[0].mode, "discovery");
  assert.equal(result.ok, true);
  assert.equal(result.definition_pack.required_concepts.length, 2);
  assert.equal(result.definition_pack.concept_dispositions[0].disposition === "propose" || result.definition_pack.concept_dispositions[1].disposition === "propose", true);
  assert.equal(result.definition_pack.open_questions.length, 1);
  assert.match(output.join(""), /Option 1 of 2/);
  assert.match(output.join(""), /Option 2 of 2/);
});

test("discussion lets the agent revise only the current option before acceptance", async () => {
  const original = option("option:vocabulary", "shared vocabulary", "An initial meaning.");
  const revised = option("option:vocabulary", "shared vocabulary", "A revised meaning bounded to the Atlas project.");
  let calls = 0;
  const agent = {
    respond: async (request) => {
      calls += 1;
      if (request.mode === "discuss-option") return {...scopeReview([revised]), phase: "option-discussion", message: "I narrowed the candidate to the project boundary."};
      return scopeReview([original]);
    },
  };
  const result = await runDefineConversation({
    agent,
    ask: scriptedAnswers(["y", "discuss", "It is too broad", "accept", "y"]),
    write: () => {},
    opening: "Atlas needs a shared vocabulary.",
    repository_root: repositoryRoot,
  });
  assert.equal(calls, 2);
  assert.equal(result.definition_pack.concept_dispositions[0].candidate_definition.normative_voice, revised.candidate_definition);
});

test("CLI defaults to conversational mode and keeps agent inference candidate", async () => {
  const agent = {
    respond: async () => ({...scopeReview([option("option:vocabulary", "shared vocabulary", "A reviewed project vocabulary.")]), phase: "options-ready"}),
    close: async () => {},
  };
  const stdout = capture();
  const stderr = capture();
  const code = await runDefineCli(["Atlas", "needs", "consistent", "language"], {
    repositoryRoot,
    stdin: new PassThrough(),
    stdout: stdout.stream,
    stderr: stderr.stream,
    agent,
    ask: scriptedAnswers(["yes", "accept", "yes"]),
    write: (text) => stdout.stream.write(text),
  });
  assert.equal(code, 0, stderr.value());
  assert.match(stdout.value(), /Here is the scope I heard/);
  assert.match(stdout.value(), /Candidate Definition Pack created/);
  assert.match(stdout.value(), /Authority effect: none/);
});

test("CLI waits for the broad opening before creating the app-server agent", async () => {
  let agentCreated = false;
  const prompts = [];
  const agent = {
    respond: async () => ({...scopeReview([option("option:vocabulary", "shared vocabulary", "A reviewed project vocabulary.")]), phase: "options-ready"}),
    close: async () => {},
  };
  const stdout = capture();
  const stderr = capture();
  const answers = scriptedAnswers(["how can I build an escape room game", "yes", "accept", "yes"]);
  const code = await runDefineCli([], {
    repositoryRoot,
    stdin: new PassThrough(),
    stdout: stdout.stream,
    stderr: stderr.stream,
    ask: async (prompt) => {
      prompts.push(prompt);
      if (prompts.length === 1) assert.equal(agentCreated, false);
      return answers();
    },
    agent_factory: () => {
      agentCreated = true;
      return agent;
    },
    write: (text) => stdout.stream.write(text),
  });
  assert.equal(code, 0, stderr.value());
  assert.equal(agentCreated, true);
  assert.match(prompts[0], /domain, subject, context, or project/);
});

test("agent preserves an app-server exit reason that occurs before initialize", async () => {
  const child = new EventEmitter();
  child.stdin = new PassThrough();
  child.stdout = new PassThrough();
  child.stderr = new PassThrough();
  child.kill = () => true;
  const agent = createAppServerDefineAgent({
    repository_root: repositoryRoot,
    spawn_impl: () => child,
  });
  child.stderr.write("profile failed to load");
  child.emit("exit", 3, null);
  await assert.rejects(
    agent.respond({mode: "discovery", user_input: "escape room", scope_confirmed: false}),
    /define-agent\.app-server-exited:3:profile failed to load/,
  );
  assert.match(agent.inspect().close_error, /app-server-exited:3/);
});
