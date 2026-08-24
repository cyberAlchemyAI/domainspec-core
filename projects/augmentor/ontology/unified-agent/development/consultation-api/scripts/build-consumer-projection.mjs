#!/usr/bin/env node
import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(import.meta.url);
const API_ROOT = path.resolve(path.dirname(SCRIPT), "..");
const ONTOLOGY_ROOT = path.resolve(API_ROOT, "..", "..");
const OUTPUT_ROOT = path.join(API_ROOT, "generated", "consumer");
const SOURCES = {
  nodes: path.join(ONTOLOGY_ROOT, "nodes", "nodes.json"),
  explanations: path.join(ONTOLOGY_ROOT, "explanations", "beginner.json"),
  glossary: path.join(ONTOLOGY_ROOT, "explanations", "glossary.json"),
  receipt: path.join(ONTOLOGY_ROOT, "receipts", "validation-receipt.json"),
};
const SCHEMAS = {
  projection: path.join(API_ROOT, "schemas", "consumer-projection.schema.json"),
  manifest: path.join(API_ROOT, "schemas", "consumer-bundle-manifest.schema.json"),
  glossary: path.join(API_ROOT, "schemas", "glossary.schema.json"),
  explanationSupport: path.join(API_ROOT, "schemas", "explanation-support.schema.json"),
};
const ALLOWLIST = [
  "id", "kind", "label", "summary", "viewIds", "fields.responsibility", "fields.boundary",
  "explanationSupport.state", "explanationSupport.process", "explanationSupport.illustrativeScenario",
  "explanationSupport.analogy", "explanationSupport.boundary", "explanationSupport.glossaryRefs",
  "explanationSupport.keywords", "fieldProvenance", "sourceHandles", "confidence",
  "glossary.terms", "structuredConflicts",
];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (!value || typeof value !== "object") return value;
  return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonicalize(value[key])]));
}

function digestJson(value) {
  return sha256(JSON.stringify(canonicalize(value)));
}

function opaque(prefix, value) {
  return `${prefix}-${sha256(value).slice(0, 12)}`;
}

function kind(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

export async function buildConsumerProjection({ outputRoot = OUTPUT_ROOT, check = false } = {}) {
  const [nodesText, explanationsText, glossaryText, receiptText, compilerText, ...schemaTexts] = await Promise.all([
    readFile(SOURCES.nodes, "utf8"),
    readFile(SOURCES.explanations, "utf8"),
    readFile(SOURCES.glossary, "utf8"),
    readFile(SOURCES.receipt, "utf8"),
    readFile(SCRIPT, "utf8"),
    ...Object.values(SCHEMAS).map((schemaPath) => readFile(schemaPath, "utf8")),
  ]);
  const nodes = JSON.parse(nodesText);
  const explanations = JSON.parse(explanationsText);
  const glossarySource = JSON.parse(glossaryText);
  const receipt = JSON.parse(receiptText);
  const reviewedDate = new Date(receipt.generated_at).toISOString().slice(0, 10);
  const schemaOutputs = schemaTexts.map((schemaText) => `${JSON.stringify(JSON.parse(schemaText))}\n`);
  if (receipt.status !== "pass" || receipt.counts.nodes !== nodes.nodes.length) throw new Error("Ontology validation receipt does not match the node source.");
  const nodeSource = opaque("src", "unified-agent-reviewed-nodes-v1");
  const explanationSource = opaque("src", "unified-agent-beginner-explanations-v1");
  const glossarySourceHandle = opaque("src", "unified-agent-explanation-glossary-v1");
  const termIds = new Map(glossarySource.terms.map((term) => [term.id, opaque("term", term.id)]));
  const glossary = {
    schemaVersion: "augmentor.consultation.glossary@1.1.0",
    terms: glossarySource.terms.map((term) => ({
      id: termIds.get(term.id),
      term: term.term,
      plainMeaning: term.plain_meaning,
      formalName: term.formal_name,
      whyItMatters: term.why_it_matters,
      sourceHandles: [glossarySourceHandle],
      authorityEffect: "none",
      forbiddenInferences: [...term.forbidden_inferences],
    })).sort((left, right) => left.id.localeCompare(right.id)),
  };
  const records = nodes.nodes.map((node) => {
    const explanation = explanations.nodes[node.concept_id];
    if (!explanation) throw new Error(`Missing reviewed explanation for ${node.concept_id}`);
    const confidence = node.confidence?.evidence_confidence === "high"
      ? "high"
      : node.confidence?.evidence_confidence === "medium" ? "medium" : "low";
    return {
      id: opaque("rec", node.concept_id),
      kind: kind(node.concept_role),
      label: explanation.friendly_name,
      summary: explanation.plain_meaning,
      viewIds: [...new Set(node.branches)].sort(),
      fields: { responsibility: explanation.process_view, boundary: explanation.boundary },
      explanationSupport: {
        recordId: opaque("rec", node.concept_id),
        state: {
          scope: "ontology-model",
          posture: node.runtime_posture,
          text: explanation.state_view,
          verifiedAt: reviewedDate,
          sourceHandle: explanationSource,
          doesNotEstablish: ["deployment"],
        },
        process: { text: explanation.process_view, sourceHandle: explanationSource },
        illustrativeScenario: {
          kind: explanation.concrete_example.kind,
          text: explanation.concrete_example.text,
          sourceHandles: explanation.concrete_example.kind === "source-derived" ? [explanationSource] : [],
        },
        analogy: { ...explanation.analogy, sourceHandle: explanationSource },
        boundary: { text: explanation.boundary, sourceHandle: explanationSource },
        glossaryRefs: explanation.glossary_refs.map((ref) => {
          if (!termIds.has(ref)) throw new Error(`Unknown glossary ref ${ref} for ${node.concept_id}`);
          return termIds.get(ref);
        }),
        keywords: [...explanation.keywords],
      },
      fieldProvenance: { sourceHandle: explanationSource },
      sourceHandles: [nodeSource],
      confidence: {
        level: confidence,
        ownerRef: opaque("own", node.owner_route),
        basis: "source_derived",
        assessedAt: reviewedDate,
        sourceHandle: nodeSource,
      },
    };
  }).sort((left, right) => left.id.localeCompare(right.id));
  const projection = {
    schemaVersion: "augmentor.consultation.projection@1.1.0",
    records,
    structuredConflicts: [],
  };
  const schemaVersions = {
    projection: "augmentor.consultation.projection@1.1.0",
    manifest: "augmentor.consultation.projection-manifest@1.1.0",
    glossary: "augmentor.consultation.glossary@1.1.0",
    explanationSupport: "augmentor.consultation.explanation-support@1.1.0",
  };
  const schemaDigests = Object.fromEntries(Object.keys(SCHEMAS).map((name, index) => [name, sha256(schemaOutputs[index])]));
  const outputDigest = digestJson(projection);
  const glossaryDigest = digestJson(glossary);
  const manifest = {
    schemaVersion: "augmentor.consultation.projection-manifest@1.1.0",
    compilerVersion: "augmentor-neutral-projection-compiler@1.1.0",
    compilerDigest: sha256(compilerText),
    allowlistDigest: digestJson(ALLOWLIST),
    opaqueIdMapVersion: "sha256-prefix@1.0.0",
    inputSources: [
      { sourceHandle: nodeSource, sha256: sha256(nodesText) },
      { sourceHandle: explanationSource, sha256: sha256(explanationsText) },
      { sourceHandle: glossarySourceHandle, sha256: sha256(glossaryText) },
    ],
    schemaVersions,
    schemaDigests,
    recordCounts: { records: records.length, structuredConflicts: 0, terms: glossary.terms.length },
    generatedAt: new Date(receipt.generated_at).toISOString(),
    outputDigest,
    glossaryDigest,
    bundleDigest: digestJson({ outputDigest, glossaryDigest, schemaVersions, schemaDigests }),
    ownerApprovalRef: opaque("approval", "APPROVE_EXACT_EPOCH:augmentor-consultation-l1-l2"),
  };
  const files = {
    "projection.json": `${JSON.stringify(projection)}\n`,
    "glossary.json": `${JSON.stringify(glossary)}\n`,
    "projection-manifest.json": `${JSON.stringify(manifest)}\n`,
    "schemas/projection.schema.json": schemaOutputs[0],
    "schemas/projection-manifest.schema.json": schemaOutputs[1],
    "schemas/glossary.schema.json": schemaOutputs[2],
    "schemas/explanation-support.schema.json": schemaOutputs[3],
  };
  if (check) {
    for (const [name, expected] of Object.entries(files)) {
      const actual = await readFile(path.join(outputRoot, name), "utf8");
      if (actual !== expected) throw new Error(`${name} is stale; rebuild the neutral consumer projection.`);
    }
  } else {
    await mkdir(outputRoot, { recursive: true });
    await Promise.all(Object.entries(files).map(async ([name, contents]) => {
      const destination = path.join(outputRoot, name);
      await mkdir(path.dirname(destination), { recursive: true });
      await writeFile(destination, contents);
    }));
  }
  return { outputRoot, manifest };
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT) {
  const result = await buildConsumerProjection({ check: process.argv.includes("--check") });
  process.stdout.write(`${JSON.stringify({ ok: true, outputRoot: result.outputRoot, outputDigest: result.manifest.outputDigest })}\n`);
}
