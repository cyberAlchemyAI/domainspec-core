import assert from "node:assert/strict";
import { resolve } from "node:path";
import { loadCompiledProjectGraph } from "../../../../../../../../projects/domainspec-v2/impl/cli/src/input/project-model.ts";

const root = resolve(import.meta.dirname, "../..", "domainspec");
const graph = loadCompiledProjectGraph(root);
assert.equal(graph.project_id, "alchlang-general-compiler");
assert.equal(graph.nodes.length, 27);
assert.equal(graph.relationships.length, 22);
assert.equal(graph.authority_effect, "none");
const selectors = new Set(graph.nodes.map((node) => node.selector));
for (const edge of graph.relationships) {
  assert(selectors.has(`${edge.source.feature_id}:${edge.source.node_id}`));
  assert(selectors.has(`${edge.target.feature_id}:${edge.target.node_id}`));
}
const kinds = new Set(graph.nodes.map((node) => node.kind));
for (const required of ["Entity", "Value Object", "Operation", "Event", "State Machine", "Rule"]) assert(kinds.has(required));
console.log(JSON.stringify({ status: "PASS", project_id: graph.project_id, nodes: graph.nodes.length, relationships: graph.relationships.length, authority_effect: "none" }, null, 2));
