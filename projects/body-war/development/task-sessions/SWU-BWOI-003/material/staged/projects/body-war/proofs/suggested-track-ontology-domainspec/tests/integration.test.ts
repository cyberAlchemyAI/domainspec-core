import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  runBridgeNegativeControls,
  runIntegrationProof,
} from "../src/integration-runner.js";

const proofRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

test("exact ontology and DomainSpec receipts admit the canonical CT-2 case", async () => {
  const result = await runIntegrationProof();

  assert.equal(result.receipt.status, "pass");
  assert.equal(result.receipt.test_id, "T-INTEGRATION-001");
  assert.equal(result.receipt.domainspec_case.reused_exact_case, true);
  assert.equal(
    result.receipt.domainspec_case.case_id,
    "body-war.CT-2#return@campinas-suggested-track",
  );
  assert.equal(result.receipt.authority_effect, "none");
  assert.equal(result.receipt.release_admission, "not-granted");
  assert.deepEqual(
    result.receipt.negative_controls.map(({ diagnostic }) => diagnostic),
    [
      "BRIDGE_STALE_ONTOLOGY_DIGEST",
      "BRIDGE_ONTOLOGY_STATE_INSUFFICIENT",
      "BRIDGE_EXECUTABLE_LOGIC_FORBIDDEN",
    ],
  );
});

test("the three mandatory bridge mutations fail closed", async () => {
  const controls = await runBridgeNegativeControls();
  assert.deepEqual(
    controls.map(({ result }) => result),
    ["rejected", "rejected", "rejected"],
  );
});

test("bridge mutation fixtures contain inputs rather than verdict oracles", () => {
  for (const name of [
    "stale-ontology-digest.json",
    "promoted-required.json",
    "executable-duplication.json",
  ]) {
    const fixture = JSON.parse(
      readFileSync(resolve(proofRoot, "bridge/fixtures", name), "utf8"),
    );
    assert.doesNotMatch(
      JSON.stringify(fixture),
      /"(?:expected|oracle|acceptance|predicate|assert|verdict)(?:_|")/i,
    );
  }
});

test("bridge and integration receipts are byte-stable", async () => {
  const first = await runIntegrationProof();
  const second = await runIntegrationProof();

  assert.equal(first.bridge_receipt_bytes, second.bridge_receipt_bytes);
  assert.equal(first.receipt_bytes, second.receipt_bytes);
  assert.equal(first.receipt.receipt_digest, second.receipt.receipt_digest);
  assert.equal(
    readFileSync(
      resolve(proofRoot, "bridge/receipts/bridge-admission-receipt.json"),
      "utf8",
    ),
    second.bridge_receipt_bytes,
  );
  assert.equal(
    readFileSync(
      resolve(proofRoot, "receipts/integration-receipt.json"),
      "utf8",
    ),
    second.receipt_bytes,
  );
});

