import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  buildVisualization,
  loadVisualizationData
} from "../scripts/build-visualization.mjs";

const PACKAGE_ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const OUTPUT_PATH = path.join(PACKAGE_ROOT, "ontology-visualization.html");
const EXPLANATION_FIELDS = [
  "plain_meaning",
  "state_view",
  "process_view",
  "boundary"
];

test("generated visualization is current and self-contained", async () => {
  const [expected, current] = await Promise.all([
    buildVisualization(),
    readFile(OUTPUT_PATH, "utf8")
  ]);

  assert.equal(current, expected);
  assert.match(current, /<script id="ontology-data" type="application\/json">/);
  assert.doesNotMatch(current, /<script\s+[^>]*src=/i);
  const linkTags = [...current.matchAll(/<link\s+[^>]*href=[^>]*>/gi)].map(([tag]) => tag);
  assert.ok(linkTags.every((tag) => /rel="icon"/i.test(tag) && /href="data:,"/i.test(tag)));
  assert.doesNotMatch(current, /<(?:img|iframe)\s+[^>]*src=/i);
});

test("visualization preserves package boundary and exact totals", async () => {
  const data = await loadVisualizationData();

  assert.equal(data.visualization_contract.ontology_type, "authority-governance");
  assert.equal(data.visualization_contract.authority_effect, "none");
  assert.equal(data.visualization_contract.output_kind, "interpretive-read-model");
  assert.equal(data.profile.status, "candidate-local");
  assert.equal(data.profile.release_admission, "not-granted");
  assert.match(data.profile.claim_ceiling, /no working routing/);
  assert.equal(data.nodes.length, 22);
  assert.equal(data.relations.length, 28);
  assert.equal(data.views.length, 5);
  assert.equal(data.residue.length, 7);
});

test("branch views expose their declared node and relation sets", async () => {
  const data = await loadVisualizationData();
  const counts = Object.fromEntries(
    data.views.map(({ descriptor, document }) => [
      descriptor.id,
      [document.node_refs.length, document.relation_refs.length]
    ])
  );

  assert.deepEqual(counts, {
    "augmentor-experience": [11, 9],
    "augmentor-runtime": [12, 13],
    "augmentor-knowledge": [7, 7],
    "augmentor-authority-bridge": [9, 7],
    "augmentor-intent-route": [13, 14]
  });
});

test("beginner explanations cover every node and lane through all six lenses", async () => {
  const data = await loadVisualizationData();
  const explanations = data.beginner_explanations;
  const expectedNodeIds = data.nodes.map((node) => node.concept_id).sort();

  assert.equal(explanations.transport, "interactive_ontology_explainer");
  assert.equal(explanations.status, "candidate-local");
  assert.equal(explanations.authority_effect, "none");
  assert.deepEqual(Object.keys(explanations.nodes).sort(), expectedNodeIds);
  assert.deepEqual(Object.keys(explanations.lanes).sort(), [
    "authority",
    "experience",
    "knowledge",
    "runtime"
  ]);
  assert.deepEqual(
    explanations.proposed_explanation_modes.slice(6).map((mode) => mode.mode),
    ["owner_map", "failure_story", "compare", "guided_walkthrough"]
  );

  for (const [conceptId, explanation] of Object.entries(explanations.nodes)) {
    assert.equal(typeof explanation.friendly_name, "string", `${conceptId}.friendly_name`);
    assert.ok(explanation.friendly_name.trim().length >= 3, `${conceptId}.friendly_name is too thin`);
    assert.ok(explanation.friendly_name.length <= 48, `${conceptId}.friendly_name is too long`);
  }

  for (const [subjectId, explanation] of Object.entries({
    ...explanations.nodes,
    ...explanations.lanes
  })) {
    for (const field of EXPLANATION_FIELDS) {
      assert.equal(typeof explanation[field], "string", `${subjectId}.${field}`);
      assert.ok(explanation[field].trim().length >= 24, `${subjectId}.${field} is too thin`);
      const maximumLength = field === "plain_meaning" ? 220 : 320;
      assert.ok(explanation[field].length <= maximumLength, `${subjectId}.${field} is too dense`);
    }
    assert.equal(explanation.concrete_example.kind, "illustrative", `${subjectId}.concrete_example.kind`);
    assert.ok(explanation.concrete_example.text.trim().length >= 24, `${subjectId}.concrete_example.text is too thin`);
    assert.ok(explanation.concrete_example.text.length <= 320, `${subjectId}.concrete_example.text is too dense`);
    assert.ok(explanation.analogy.text.trim().length >= 24, `${subjectId}.analogy.text is too thin`);
    assert.ok(explanation.analogy.text.length <= 320, `${subjectId}.analogy.text is too dense`);
    assert.ok(explanation.analogy.limitation.trim().length >= 24, `${subjectId}.analogy.limitation is too thin`);
    assert.ok(explanation.analogy.limitation.length <= 320, `${subjectId}.analogy.limitation is too dense`);
    assert.ok(explanation.glossary_refs.length >= 2 && explanation.glossary_refs.length <= 5, `${subjectId}.glossary_refs`);
    const directExplanation = [
      explanation.plain_meaning,
      explanation.state_view,
      explanation.process_view,
      explanation.boundary
    ].join(" ");
    assert.doesNotMatch(
      directExplanation,
      /\b(?:bounded|projection|disposition|lifecycle|receipt|canonical|ontology|digest|adapter|registrar|immutable|artifact|residue)\b/i,
      `${subjectId} leaks avoidable jargon into the direct explanation`
    );
  }
});

test("all visualized relations and sequence steps resolve", async () => {
  const data = await loadVisualizationData();
  const nodeIds = new Set(data.nodes.map((node) => node.concept_id));
  const relationIds = new Set(data.relations.map((relation) => relation.relation_id));

  for (const relation of data.relations) {
    assert.equal(relation.direction, "directed", relation.relation_id);
    assert.ok(relation.predicate, relation.relation_id);
    assert.ok(nodeIds.has(relation.source_concept), relation.source_concept);
    assert.ok(nodeIds.has(relation.target_concept), relation.target_concept);
  }

  for (const { document } of data.views) {
    for (const nodeRef of document.node_refs) assert.ok(nodeIds.has(nodeRef), nodeRef);
    for (const relationRef of document.relation_refs) {
      assert.ok(relationIds.has(relationRef), relationRef);
    }
    for (const sequence of document.sequences ?? []) {
      for (const step of sequence.steps) assert.ok(nodeIds.has(step), step);
    }
  }
});

test("the HTML exposes the primary exploration and accessibility surfaces", async () => {
  const html = await readFile(OUTPUT_PATH, "utf8");

  for (const marker of [
    "ontology-search",
    "posture-filter",
    "view-tabs",
    "ontology-graph",
    "sequence-list",
    "ontology-inspector",
    "beginner-guide",
    "explanation-lenses",
    "lane-explanations",
    "proposed-explanation-modes",
    "residue-grid",
    "linear-list",
    "claim-ceiling",
    "page-navigation",
    "ontology-page",
    "agent-api-page",
    "agent-api-form",
    "agent-api-question",
    "agent-api-profile",
    "agent-api-submit",
    "agent-api-status",
    "agent-api-result",
    "agent-api-raw"
  ]) {
    assert.match(html, new RegExp(`(?:id|data-testid)=["']${marker}["']`), marker);
  }
  assert.match(html, /prefers-reduced-motion:\s*reduce/);
  assert.match(html, /event\.key === "Enter" \|\| event\.key === " "/);
  assert.match(html, /event\.key === "Escape"/);
  assert.match(html, /window\.augmentorConsultationPage = Object\.freeze/);
  assert.match(html, /credentials: "same-origin"/);
  assert.match(html, /fetch\(agentContract\.endpoint/);
  assert.match(html, /augmentor:consultation-complete/);
  assert.doesNotMatch(html, /headers:\s*\{[^}]*Authorization/i);
});

test("the page agent contract is closed around the read-only consultation route", async () => {
  const html = await readFile(OUTPUT_PATH, "utf8");
  const encoded = html.match(/<script id="augmentor-agent-contract" type="application\/json">([^<]+)<\/script>/)?.[1];
  assert.ok(encoded, "agent contract is embedded");
  const contract = JSON.parse(encoded);

  assert.equal(contract.schemaVersion, "augmentor.page-agent-contract@1.1.0");
  assert.equal(contract.endpoint, "/augmentor/consultation");
  assert.equal(contract.method, "POST");
  assert.equal(contract.authorityEffect, "none");
  assert.equal(contract.followRetrievedInstructions, false);
  assert.equal(contract.defaultExplanationProfile, "guided");
  assert.equal(contract.selectors.support, "[data-testid=agent-api-support]");
  assert.deepEqual(contract.answerActions, ["answer", "qualify", "clarify", "abstain"]);
  assert.equal(contract.events.start, "augmentor:consultation-start");
  assert.equal(contract.events.complete, "augmentor:consultation-complete");
  assert.equal(contract.events.error, "augmentor:consultation-error");
});
