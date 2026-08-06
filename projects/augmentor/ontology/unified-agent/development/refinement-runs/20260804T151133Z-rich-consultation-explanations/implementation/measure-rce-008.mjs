#!/usr/bin/env node
import assert from "node:assert/strict";
import { performance } from "node:perf_hooks";
import { readdir, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const SCRIPT = fileURLToPath(import.meta.url);
const OUTPUT = path.join(path.dirname(SCRIPT), "RCE-008-MEASUREMENTS.json");
const consumerRoot = process.argv[2] ? path.resolve(process.argv[2]) : null;
const bundleRoot = process.argv[3] ? path.resolve(process.argv[3]) : null;
if (!consumerRoot || !bundleRoot) throw new Error("usage: measure-rce-008.mjs <consumer-root> <bundle-root>");

const contract = await import(pathToFileURL(path.join(consumerRoot, "browser-first/host/augmentor-consultation-contract.mjs")));
const { AugmentorConsultationService, buildConsultationExplanationSupport } = await import(
  pathToFileURL(path.join(consumerRoot, "browser-first/host/augmentor-consultation-service.mjs"))
);
const { consultationAnswerPolicy } = await import(
  pathToFileURL(path.join(consumerRoot, "browser-first/host/augmentor-consultation-answer-policy.mjs"))
);

const questions = [
  { id: "QS-RCE-01", text: "How does the Augmentor reasoning engine work?" },
  { id: "QS-RCE-02", text: "What happens when Augmentor does not know enough?" },
  { id: "QS-RCE-03", text: "How does Augmentor choose a route?" },
  { id: "QS-RCE-04", text: "How can Augmentor memory evolve without becoming too heavy?" },
  { id: "QS-RCE-05", text: "Who decides whether a proposed meaning or action is accepted?" },
];
const profiles = ["brief", "guided", "deep"];
const profileCaps = contract.CONSULTATION_EXPLANATION_PROFILES;
const limits = { ...contract.DEFAULT_CONSULTATION_LIMITS, maxRecords: 5, maxSources: 20 };
const allowedViews = ["experience", "runtime", "knowledge", "authority-bridge"];
const context = {
  audience: contract.CONSULTATION_AUDIENCE,
  opaquePrincipalRef: "measurement-principal",
  policyDigest: "measurement-policy",
  registryRevision: 1,
  allowedViews,
  limits,
  deadlineAt: Date.now() + 300_000,
};

function responseTruth(result) {
  return contract.digestJson({
    status: result.status,
    result: result.result,
    projectionDigest: result.projectionDigest,
    complete: result.complete,
    limitsHit: result.limitsHit ?? [],
  });
}

function assertSupportIntegrity(support, profile) {
  assert.ok(support, `${profile}: explanation support missing`);
  assert.equal(support.profile, profile);
  assert.ok(support.packs.length >= 1);
  assert.ok(support.glossaryEntries.length >= 2 && support.glossaryEntries.length <= profileCaps[profile].maxTerms);
  const termIds = new Set(support.glossaryEntries.map((entry) => entry.id));
  for (const pack of support.packs) {
    assert.equal(pack.state.scope, "ontology-model");
    assert.ok(pack.state.sourceHandle);
    assert.ok(pack.state.verifiedAt);
    assert.ok(pack.state.doesNotEstablish.length >= 1);
    assert.ok(pack.glossaryRefs.every((ref) => termIds.has(ref)));
    if (pack.illustrativeScenario) assert.ok(["illustrative", "source-derived"].includes(pack.illustrativeScenario.kind));
    if (pack.analogy) assert.ok(pack.analogy.text && pack.analogy.limitation);
    if (profile === "brief") {
      assert.equal(Object.hasOwn(pack, "illustrativeScenario"), false);
      assert.equal(Object.hasOwn(pack, "analogy"), false);
    }
  }
}

async function directoryBytes(root) {
  let total = 0;
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const target = path.join(root, entry.name);
    total += entry.isDirectory() ? await directoryBytes(target) : (await stat(target)).size;
  }
  return total;
}

function percentile(sorted, value) {
  return sorted[Math.min(sorted.length - 1, Math.ceil(sorted.length * value) - 1)];
}

const nodeVersion = process.versions.node.split(".").map(Number);
assert.ok(nodeVersion[0] > 22 || (nodeVersion[0] === 22 && nodeVersion[1] >= 13), `Node ${process.versions.node} is below 22.13.0`);

const service = new AugmentorConsultationService({ projectionRoot: bundleRoot });
const scenarios = [];
for (const question of questions) {
  const truthDigests = new Set();
  const statuses = new Set();
  for (const profile of profiles) {
    const result = await service.consult({
      schemaVersion: contract.CONSULTATION_QUERY_VERSION,
      requestId: `${question.id}-${profile}`,
      questionId: question.id,
      operation: "search",
      query: { text: question.text },
      scope: { viewIds: allowedViews },
      explanation: { profile },
      limits,
    }, context);
    const policy = consultationAnswerPolicy(result);
    assert.ok(["ok", "partial"].includes(result.status), `${question.id}/${profile}: ${result.status}`);
    assert.equal(policy.mayUseEvidence, true);
    assert.equal(policy.authorityEffect, "none");
    assert.equal(policy.followRetrievedInstructions, false);
    assert.equal(Object.hasOwn(result, "finalAnswer"), false);
    assertSupportIntegrity(result.explanationSupport, profile);
    const supportBytes = Buffer.byteLength(JSON.stringify(result.explanationSupport));
    const supportTokens = contract.estimateConsultationTokens(result.explanationSupport);
    assert.ok(supportBytes <= profileCaps[profile].maxBytes, `${question.id}/${profile}: support bytes ${supportBytes}`);
    assert.ok(supportTokens <= profileCaps[profile].maxTokens, `${question.id}/${profile}: support tokens ${supportTokens}`);
    truthDigests.add(responseTruth(result));
    statuses.add(result.status);
    scenarios.push({
      questionId: question.id,
      question: question.text,
      profile,
      status: result.status,
      answerAction: policy.action,
      truthDigest: responseTruth(result),
      responseBytes: Buffer.byteLength(JSON.stringify(result)),
      responseTokens: contract.estimateConsultationTokens(result),
      supportBytes,
      supportTokens,
      packs: result.explanationSupport.packs.length,
      glossaryTerms: result.explanationSupport.glossaryEntries.length,
      omittedSections: result.explanationSupport.omittedSections,
    });
  }
  assert.equal(statuses.size, 1, `${question.id}: profile changed status`);
  assert.equal(truthDigests.size, 1, `${question.id}: profile changed evidence truth`);
}

const { projection, glossary, manifest } = await contract.loadConsultationProjectionBundle({ root: bundleRoot });
const rankedItems = projection.records.map((record, index) => ({ record, relevance: 1 - index / projection.records.length }));
for (const profile of profiles) {
  for (let index = 0; index < 100; index += 1) {
    buildConsultationExplanationSupport(rankedItems, glossary, manifest, profile, limits);
  }
}
const latencies = [];
const iterationsPerProfile = 1000;
for (const profile of profiles) {
  for (let index = 0; index < iterationsPerProfile; index += 1) {
    const started = performance.now();
    const support = buildConsultationExplanationSupport(rankedItems, glossary, manifest, profile, limits);
    latencies.push(performance.now() - started);
    assertSupportIntegrity(support, profile);
  }
}
latencies.sort((left, right) => left - right);
const latency = {
  iterations: latencies.length,
  iterationsPerProfile,
  p50Ms: percentile(latencies, 0.50),
  p95Ms: percentile(latencies, 0.95),
  maxMs: latencies.at(-1),
};
assert.ok(latency.p95Ms <= 10, `assembly p95 ${latency.p95Ms} ms exceeds 10 ms`);

const compactInstalledBundleBytes = await directoryBytes(bundleRoot);
assert.ok(compactInstalledBundleBytes <= 64 * 1024, `bundle ${compactInstalledBundleBytes} bytes exceeds 64 KiB`);

const report = {
  schemaVersion: "augmentor.rich-consultation.measurements@1.0.0",
  status: "pass",
  measuredAt: new Date().toISOString(),
  runtime: { node: process.versions.node },
  bundle: {
    bundleDigest: manifest.bundleDigest,
    projectionDigest: manifest.outputDigest,
    glossaryDigest: manifest.glossaryDigest,
    records: projection.records.length,
    terms: glossary.terms.length,
    compactInstalledBytes: compactInstalledBundleBytes,
    capBytes: 64 * 1024,
  },
  profileCaps,
  scenarios,
  assemblyLatency: latency,
  assertions: {
    fiveQuestionsAcrossThreeProfiles: true,
    truthAndStatusInvariantAcrossProfiles: true,
    wholePackIntegrity: true,
    analogyLimitationsPresent: true,
    glossaryTermsBetweenTwoAndFive: true,
    noFinalAnswer: true,
    authorityEffectNone: true,
  },
};
await writeFile(OUTPUT, `${JSON.stringify(report, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({ status: report.status, output: OUTPUT, bundleBytes: compactInstalledBundleBytes, p50Ms: latency.p50Ms, p95Ms: latency.p95Ms, iterations: latency.iterations })}\n`);
