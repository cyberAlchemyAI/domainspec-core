#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [beginner, glossary, ontology] = await Promise.all([
  readFile(path.join(ROOT, "explanations", "beginner.json"), "utf8").then(JSON.parse),
  readFile(path.join(ROOT, "explanations", "glossary.json"), "utf8").then(JSON.parse),
  readFile(path.join(ROOT, "nodes", "nodes.json"), "utf8").then(JSON.parse),
]);
const errors = [];
const terms = new Set(glossary.terms.map((term) => term.id));
if (terms.size !== glossary.terms.length) errors.push("glossary term IDs must be unique");
if (glossary.terms.some((term) => term.authority_effect !== undefined)) errors.push("source glossary must not override root authority_effect");
if (beginner.schema !== "augmentor.unified-agent.beginner-explanations@0.2.0") errors.push("unexpected beginner schema");
if (Object.keys(beginner.nodes).length !== ontology.nodes.length) errors.push("node coverage is not total");

function validateEntry(id, entry, posture = null) {
  if (!entry.concrete_example || !["illustrative", "source-derived"].includes(entry.concrete_example.kind) || !entry.concrete_example.text?.trim()) errors.push(`${id}: invalid example`);
  if (entry.concrete_example?.kind === "source-derived" && !entry.concrete_example.source_refs?.length) errors.push(`${id}: source-derived example lacks sources`);
  if (!entry.analogy?.text?.trim() || !entry.analogy?.limitation?.trim()) errors.push(`${id}: analogy and limitation are required together`);
  if (!Array.isArray(entry.glossary_refs) || entry.glossary_refs.length < 2 || entry.glossary_refs.length > 5 || new Set(entry.glossary_refs).size !== entry.glossary_refs.length) errors.push(`${id}: glossary refs must contain 2-5 unique terms`);
  for (const ref of entry.glossary_refs ?? []) if (!terms.has(ref)) errors.push(`${id}: unknown glossary ref ${ref}`);
  if (!Array.isArray(entry.keywords) || entry.keywords.length < 2 || entry.keywords.length > 12 || new Set(entry.keywords).size !== entry.keywords.length) errors.push(`${id}: keywords must contain 2-12 unique entries`);
  const prose = [entry.friendly_name, entry.plain_meaning, entry.state_view, entry.process_view, entry.concrete_example?.text, entry.analogy?.text, entry.analogy?.limitation, entry.boundary].filter(Boolean).join(" ");
  if (/\b(?:immutable|digest|selector|composed bytes|authority_effect)\b/i.test(prose)) errors.push(`${id}: unexplained implementation jargon`);
  if (["absent", "deferred"].includes(posture) && !/\b(?:not|no|still|later|planned|missing|blocked|saved)\b/i.test(entry.state_view)) errors.push(`${id}: non-current posture is not clear in state text`);
}

for (const [lane, entry] of Object.entries(beginner.lanes)) validateEntry(`lane:${lane}`, entry);
for (const node of ontology.nodes) validateEntry(node.concept_id, beginner.nodes[node.concept_id], node.runtime_posture);

process.stdout.write(`${JSON.stringify({ status: errors.length ? "fail" : "pass", nodes: ontology.nodes.length, lanes: Object.keys(beginner.lanes).length, terms: glossary.terms.length, errors }, null, 2)}\n`);
if (errors.length) process.exitCode = 1;
