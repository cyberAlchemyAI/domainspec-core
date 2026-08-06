#!/usr/bin/env node
import {createHash} from "node:crypto";
import {writeFile} from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {resolve} from "node:path";

const [packageRoot, runtime, outputPath] = process.argv.slice(2);
if (!packageRoot || !runtime || !outputPath) {
  throw new Error("usage: run-wrapper-matrix.mjs <package-root> <runtime> <output>");
}

const load = (path) => import(pathToFileURL(resolve(packageRoot, path)));
const {canonicalJson} = await load("src/canonical-json.mjs");
const {resolveJson, resolveJsonValue} = await load("src/json-port.mjs");
const {resolveIntentRoute} = await load("src/resolve.mjs");
const {makeCatalog, makeEnvelope, makeRequest} = await load("test/fixture-factory.mjs");

const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const observed = [];
const record = (caseId, result) => observed.push({
  case_id: caseId,
  exit_code: result.exit_code,
  stdout_sha256: sha256(result.stdout),
  stdout_bytes: Buffer.byteLength(result.stdout),
  stderr_bytes: Buffer.byteLength(result.stderr)
});

for (const [caseId, kind] of [["J01", "candidate"], ["J02", "ambiguous"], ["J03", "no-match"], ["J04", "invalid"]]) {
  record(caseId, resolveJsonValue(makeEnvelope(kind)));
}
record("J05", resolveJson("{"));
{
  const envelope = makeEnvelope("candidate");
  envelope.catalog = structuredClone(envelope.catalog);
  envelope.catalog.routes[0].dominates = ["missing-route"];
  record("J06", resolveJsonValue(envelope));
}
{
  const envelope = makeEnvelope();
  delete envelope.capability_token;
  record("J07", resolveJsonValue(envelope));
}
{
  const envelope = makeEnvelope();
  envelope.request.schema = "intent-route.request@2";
  record("J08", resolveJsonValue(envelope));
}
{
  const envelope = makeEnvelope();
  envelope.schema = "intent-route.runtime-port.request@2";
  record("J09", resolveJsonValue(envelope));
}
{
  const envelope = makeEnvelope();
  envelope.expected_core_version = "9.9.9";
  record("J10", resolveJsonValue(envelope));
}
{
  const envelope = makeEnvelope();
  envelope.expected_manifest_version = "9.9.9";
  record("J11", resolveJsonValue(envelope));
}
{
  const envelope = makeEnvelope();
  envelope.request.catalog_digest = "f".repeat(64);
  record("J12", resolveJsonValue(envelope));
}
{
  const envelope = makeEnvelope();
  envelope.expected_closure_digest = "f".repeat(64);
  record("J13", resolveJsonValue(envelope));
}
{
  const orders = [
    ["route.general", "route.image", "route.special"],
    ["route.image", "route.special", "route.general"],
    ["route.special", "route.general", "route.image"]
  ];
  const bytes = orders.map((order) => {
    const catalog = makeCatalog(order);
    return canonicalJson(resolveIntentRoute(makeRequest("candidate", catalog), catalog));
  });
  if (new Set(bytes).size !== 1) throw new Error("M14 permutation mismatch");
  record("M14", {exit_code: 0, stdout: `${bytes[0]}\n`, stderr: ""});
}
{
  const catalog = makeCatalog();
  const request = makeRequest("candidate", catalog);
  const candidate = resolveIntentRoute(request, catalog);
  request.intent.discriminators.audience = {posture: "unresolved", value: null};
  const ambiguous = resolveIntentRoute(request, catalog);
  if (candidate.kind !== "candidate" || ambiguous.kind !== "ambiguous") {
    throw new Error("M15 uncertainty monotonicity mismatch");
  }
  record("M15", {exit_code: 0, stdout: `${canonicalJson({candidate, ambiguous})}\n`, stderr: ""});
}

const report = {
  schema: "intent-route.wrapper-matrix@1",
  runtime,
  status: observed.length === 15 && observed.every((item) => item.stderr_bytes === 0) ? "pass" : "fail",
  case_count: observed.length,
  cases: observed,
  authority_effect: "none"
};
await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
process.stdout.write(`${canonicalJson({schema: report.schema, runtime, status: report.status, case_count: report.case_count})}\n`);
if (report.status !== "pass") process.exitCode = 1;
