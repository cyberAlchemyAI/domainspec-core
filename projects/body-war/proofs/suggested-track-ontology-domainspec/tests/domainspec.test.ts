import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { runDomainspecCt2Proof } from "../src/domainspec-ct2-runner.js";

const thisDir = dirname(fileURLToPath(import.meta.url));
const proofRoot = resolve(thisDir, "..");

test("canonical CT-2 matches the Body War memory repository", async () => {
  const result = await runDomainspecCt2Proof();

  assert.equal(result.receipt.status, "pass");
  assert.equal(result.receipt.source.node_id, "body-war.CreateSuggestedTrack");
  assert.equal(result.receipt.source.clause_id, "body-war.CT-2");
  assert.equal(result.receipt.build.deterministic, true);
  assert.equal(result.receipt.build.verified, true);
  assert.equal(result.receipt.proof.case_count, 1);
  assert.equal(result.receipt.authority_effect, "none");
  assert.equal(result.receipt.release_admission, "not-granted");
  assert.deepEqual(
    result.receipt.proof.stage_sets.map(({ stage }) => stage),
    [
      "C_spec",
      "C_projected",
      "C_validated",
      "C_typed",
      "T_generated",
      "C_bound",
      "O_run",
      "R_evaluated",
    ],
  );
  assert.equal(
    new Set(
      result.receipt.proof.stage_sets.map(({ case_ids }) =>
        JSON.stringify(case_ids),
      ),
    ).size,
    1,
  );
});

test("the fixture is input-only and the stronger backend mutation is rejected", async () => {
  const fixture = JSON.parse(
    readFileSync(
      resolve(proofRoot, "domainspec/fixtures/ct2-input.json"),
      "utf8",
    ),
  ) as Record<string, unknown>;
  const serialized = JSON.stringify(fixture);
  assert.doesNotMatch(
    serialized,
    /"(?:expected|oracle|acceptance|predicate|assert|verdict)(?:_|")/i,
  );

  const result = await runDomainspecCt2Proof();
  assert.deepEqual(result.receipt.mutation_control, {
    mutation: "stronger-backend-claims",
    evaluation_status: "fail",
    proof_status: "rejected",
    diagnostic_code: "SFOL_PROOF_NONPASS_STATE",
  });
});

test("unchanged CT-2 proof artifacts are byte-stable", async () => {
  const first = await runDomainspecCt2Proof();
  const second = await runDomainspecCt2Proof();

  assert.equal(first.receipt_bytes, second.receipt_bytes);
  assert.equal(first.receipt.receipt_digest, second.receipt.receipt_digest);
  assert.equal(
    readFileSync(
      resolve(proofRoot, "receipts/domainspec-receipt.json"),
      "utf8",
    ),
    second.receipt_bytes,
  );
  assert.equal(
    readFileSync(resolve(proofRoot, "domainspec/generated/graph.json"), "utf8")
      .length > 0,
    true,
  );
  assert.equal(
    readFileSync(
      resolve(proofRoot, "domainspec/generated/source-manifest.json"),
      "utf8",
    ).length > 0,
    true,
  );
  assert.equal(
    readFileSync(
      resolve(proofRoot, "domainspec/generated/build-receipt.json"),
      "utf8",
    ).length > 0,
    true,
  );
  assert.equal(
    readFileSync(
      resolve(proofRoot, "domainspec/generated/logic-projection.json"),
      "utf8",
    ).length > 0,
    true,
  );
});
