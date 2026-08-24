#!/usr/bin/env node
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const TARGET = path.join(ROOT, "explanations", "beginner.json");
const NODES = path.join(ROOT, "nodes", "nodes.json");

const keywordMap = {
  augmentor_interface: ["interface", "conversation", "route", "memory"],
  conversation_thread: ["conversation", "thread", "session", "history"],
  interaction: ["topic", "goal", "interaction", "context"],
  source_record: ["source", "evidence", "owner", "version"],
  disposable_semantic_index: ["search", "index", "temporary", "knowledge"],
  context_snapshot: ["context", "snapshot", "starting information", "sources"],
  intent_route_request: ["intent", "routing", "request", "missing information"],
  route_catalog_projection: ["route", "catalog", "allowed routes", "routing"],
  resolver_invocation: ["route", "resolver", "routing", "lookup"],
  route_disposition: ["route", "result", "clarify", "no match"],
  route_decision: ["route", "decision", "answer", "clarify"],
  strategy_proposal: ["strategy", "plan", "helpers", "approval"],
  approval_record: ["approval", "plan", "version", "permission"],
  dispatch: ["dispatch", "helpers", "roles", "workflow"],
  run: ["run", "task", "status", "execution"],
  lifecycle_join: ["join", "results", "status", "workflow"],
  result_consumption: ["result", "conversation", "use", "memory"],
  memory_intake_request: ["memory", "request", "correction", "source"],
  ontology_candidate: ["ontology", "meaning", "proposal", "evidence"],
  authority_decision: ["authority", "owner", "decision", "meaning"],
  reasoning_request: ["reasoning", "evaluator", "request", "rules", "judgment"],
  judgment_receipt: ["reasoning", "judgment", "evaluator", "evidence", "authority"],
};

const glossaryMap = {
  augmentor_interface: ["term-consultation", "term-route", "term-authority"],
  conversation_thread: ["term-consultation", "term-evidence"],
  interaction: ["term-consultation", "term-route"],
  source_record: ["term-source-handle", "term-evidence", "term-authority"],
  disposable_semantic_index: ["term-neutral-projection", "term-evidence"],
  context_snapshot: ["term-evidence", "term-source-handle"],
  intent_route_request: ["term-route", "term-authority"],
  route_catalog_projection: ["term-route", "term-neutral-projection"],
  resolver_invocation: ["term-route", "term-evidence"],
  route_disposition: ["term-route", "term-answer-policy"],
  route_decision: ["term-route", "term-authority", "term-answer-policy"],
  strategy_proposal: ["term-route", "term-authority"],
  approval_record: ["term-authority", "term-evidence"],
  dispatch: ["term-route", "term-authority"],
  run: ["term-evidence", "term-authority"],
  lifecycle_join: ["term-evidence", "term-answer-policy"],
  result_consumption: ["term-evidence", "term-memory-request"],
  memory_intake_request: ["term-memory-request", "term-authority", "term-evidence"],
  ontology_candidate: ["term-evidence", "term-authority", "term-neutral-projection"],
  authority_decision: ["term-authority", "term-evidence"],
  reasoning_request: ["term-reasoning-request", "term-evidence", "term-authority"],
  judgment_receipt: ["term-judgment-receipt", "term-reasoning-request", "term-authority", "term-evidence"],
};

const laneGlossary = {
  experience: ["term-consultation", "term-route", "term-authority"],
  runtime: ["term-route", "term-evidence", "term-authority"],
  knowledge: ["term-evidence", "term-source-handle", "term-memory-request"],
  authority: ["term-authority", "term-reasoning-request", "term-judgment-receipt"],
};

function structure(entry, refs, keywords) {
  return {
    ...entry,
    concrete_example: typeof entry.concrete_example === "string"
      ? { kind: "illustrative", text: entry.concrete_example }
      : entry.concrete_example,
    analogy: typeof entry.analogy === "string"
      ? { text: entry.analogy, limitation: `This comparison explains only the main relationship. ${entry.boundary}` }
      : entry.analogy,
    glossary_refs: refs,
    keywords,
  };
}

const beginner = JSON.parse(await readFile(TARGET, "utf8"));
const ontology = JSON.parse(await readFile(NODES, "utf8"));
const known = new Set(ontology.nodes.map((node) => node.concept_id));
if (known.size !== Object.keys(beginner.nodes).length || Object.keys(beginner.nodes).some((id) => !known.has(id))) {
  throw new Error("beginner explanations do not match the ontology node set");
}
beginner.schema = "augmentor.unified-agent.beginner-explanations@0.2.0";
for (const [lane, entry] of Object.entries(beginner.lanes)) {
  beginner.lanes[lane] = structure(entry, laneGlossary[lane], [lane, "process", "boundary"]);
}
for (const [id, entry] of Object.entries(beginner.nodes)) {
  const short = id.split(".").at(-1);
  beginner.nodes[id] = structure(entry, glossaryMap[short], keywordMap[short]);
}
await writeFile(TARGET, `${JSON.stringify(beginner, null, 2)}\n`);
process.stdout.write(`RICH_EXPLANATION_MIGRATION=pass nodes=${Object.keys(beginner.nodes).length} lanes=${Object.keys(beginner.lanes).length}\n`);
