import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

import { comprehensionTask } from "../authoring/comprehension-task-catalog.mjs";

const execFileAsync = promisify(execFile);
const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

test("learner comprehension task is current", async () => {
  const { stdout } = await execFileAsync(
    process.execPath,
    [
      path.join(packageRoot, "scripts/generate-comprehension-task.mjs"),
      "--check",
    ],
  );
  assert.match(stdout, /6 learner loci/);
});

test("learner generator has a single learner-only authoring dependency", async () => {
  const generator = await readFile(
    path.join(packageRoot, "scripts/generate-comprehension-task.mjs"),
    "utf8",
  );
  const imports = generator.match(/^import .+;$/gm) ?? [];
  assert.equal(
    imports.filter((line) => line.includes("../authoring/")).length,
    1,
  );
  assert.match(generator, /comprehension-task-catalog\.mjs/);
  assert.doesNotMatch(generator, /review\/|comprehension-protocol|answer_key/);
});

test("six preregistered loci are unique and learner-visible", async () => {
  const expected = [
    "locate",
    "trace",
    "retell",
    "distinguish",
    "boundary",
    "vocabulary",
  ];
  assert.deepEqual(
    comprehensionTask.loci.map((locus) => locus.locus_id),
    expected,
  );
  const html = await readFile(
    path.join(packageRoot, "BUSINESS-COMPREHENSION-TASK.html"),
    "utf8",
  );
  for (const locus of expected) {
    assert.equal(
      (html.match(new RegExp(`data-locus="${locus}"`, "g")) ?? []).length,
      1,
    );
  }
  assert.match(html, /BUSINESS-JOURNEY-EXPERIMENT\.html/);
});

test("reviewer protocol is complete and cannot leak into learner bytes", async () => {
  const protocol = JSON.parse(
    await readFile(
      path.join(packageRoot, "review/comprehension-protocol.json"),
      "utf8",
    ),
  );
  const html = await readFile(
    path.join(packageRoot, "BUSINESS-COMPREHENSION-TASK.html"),
    "utf8",
  );
  const leakageFixture = (
    await readFile(
      path.join(
        packageRoot,
        "tests/fixtures/comprehension-reviewer-leakage.txt",
      ),
      "utf8",
    )
  )
    .trim()
    .split("\n");

  assert.deepEqual(protocol.matched_arms.fields, [
    "task",
    "loci",
    "prompt",
    "stimulus",
  ]);
  assert.equal(protocol.matched_arms.identity_rule, "byte-identical");
  assert.equal(protocol.stall_contract.zero_stalls_valid, true);
  assert.equal(protocol.stall_contract.correctness_is_separate, true);
  assert.deepEqual(
    Object.keys(protocol.answer_key),
    comprehensionTask.loci.map((locus) => locus.locus_id),
  );
  for (const marker of [
    ...protocol.learner_deny_markers,
    ...leakageFixture,
  ]) {
    assert.doesNotMatch(html, new RegExp(marker));
  }
});

test("reviewer key covers edge, branch, boundary, and invented-sequence checks", async () => {
  const protocol = JSON.parse(
    await readFile(
      path.join(packageRoot, "review/comprehension-protocol.json"),
      "utf8",
    ),
  );
  assert.deepEqual(protocol.answer_key.locate.expected_relation_ids, [
    "body-war.relation.confirm-consumes-activity",
  ]);
  assert.deepEqual(protocol.answer_key.distinguish.expected_branches, [
    "preview-evidence",
    "controller-preview",
  ]);
  assert.equal(
    protocol.answer_key.distinguish.must_reject_invented_sequence,
    true,
  );
  assert.equal(protocol.answer_key.boundary.requires_owner_and_gate, true);
  assert.equal(protocol.scoring.unit, "edge-local");
});

