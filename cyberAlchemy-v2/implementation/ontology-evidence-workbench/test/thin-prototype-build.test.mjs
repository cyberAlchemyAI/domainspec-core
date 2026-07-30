import assert from "node:assert/strict";
import { mkdir, mkdtemp, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  ThinBuildError,
  expectedTypedSourceDigest,
  normalizedRelativePath,
  parseBuildArgs,
  treeIdentity,
  validateOutputLogicalPath,
  validatePatchSpecs,
  validateTypedReceipt,
} from "../scripts/build-thin-prototype.mjs";

const issue = (expected) => (error) =>
  error instanceof ThinBuildError && error.issue === expected;

test("CLI accepts only the exact build contract", () => {
  assert.deepEqual(
    parseBuildArgs([
      "build",
      "--typed-receipt",
      "cyberAlchemy-v2/development/receipt.json",
      "--output",
      "generated/runs/SWU-OEWTP-002/20260729T184000Z/thin-prototype-build-handle.json",
    ]),
    {
      typedReceipt: "cyberAlchemy-v2/development/receipt.json",
      output:
        "generated/runs/SWU-OEWTP-002/20260729T184000Z/thin-prototype-build-handle.json",
    },
  );
  assert.throws(() => parseBuildArgs(["run"]), issue("COMMAND_INVALID"));
  assert.throws(
    () => parseBuildArgs(["build", "--output", "x"]),
    issue("ARGUMENT_COUNT_INVALID"),
  );
  assert.throws(
    () =>
      parseBuildArgs([
        "build",
        "--output",
        "x",
        "--output",
        "y",
      ]),
    issue("ARGUMENT_DUPLICATE"),
  );
});

test("paths reject absolute, traversal, normalization, and wrong output identity", () => {
  for (const path of ["/tmp/x", "../x", "a/../x", "a/./x", "a\\x"]) {
    assert.throws(() => normalizedRelativePath(path), issue("PATH_INVALID"));
  }
  assert.throws(
    () =>
      validateOutputLogicalPath(
        "generated/runs/SWU-OEWTP-003/20260729T184000Z/thin-prototype-build-handle.json",
      ),
    issue("OUTPUT_PATH_INVALID"),
  );
  assert.equal(
    validateOutputLogicalPath(
      "generated/runs/SWU-OEWTP-002/20260729T184000Z/thin-prototype-build-handle.json",
    ).attemptId,
    "20260729T184000Z",
  );
});

test("predecessor receipt rejects failure, partial inventory, and diagnostics", () => {
  const valid = {
    schema_version: "oewtp.task-session-receipt.v1",
    swu_id: "SWU-OEWTP-001",
    result: "pass",
    files_touched: ["1", "2", "3", "4", "5"],
    validation: {
      strict_typescript: { after_diagnostics: 0 },
      typed_oew_tests: { failed: 0 },
      package_manifest_inventory: { result: "pass" },
    },
  };
  assert.equal(validateTypedReceipt(valid), true);
  for (const changed of [
    { result: "block" },
    { files_touched: ["1"] },
    { validation: { ...valid.validation, strict_typescript: { after_diagnostics: 1 } } },
  ]) {
    assert.throws(
      () => validateTypedReceipt({ ...valid, ...changed }),
      issue("TYPED_RECEIPT_INVALID"),
    );
  }
});

test("patch bindings retain declared order and reject incomplete or duplicate rows", () => {
  const digest = "a".repeat(64);
  const secondDigest = "b".repeat(64);
  const patches = [
    {
      path: "upstream/patches/0001.patch",
      target: "src/App.tsx",
      sha256: digest,
      preimage_sha256: digest,
      postimage_sha256: secondDigest,
      apply_exactly_once: true,
    },
    {
      path: "upstream/patches/0002.patch",
      target: "src/View.tsx",
      sha256: secondDigest,
      preimage_sha256: digest,
      postimage_sha256: secondDigest,
      apply_exactly_once: true,
    },
  ];
  assert.deepEqual(
    validatePatchSpecs(patches).map(({path}) => path),
    ["upstream/patches/0001.patch", "upstream/patches/0002.patch"],
  );
  assert.throws(() => validatePatchSpecs([]), issue("PATCH_BINDINGS_MISSING"));
  assert.throws(
    () => validatePatchSpecs([patches[0], patches[0]]),
    issue("PATCH_BINDING_INVALID"),
  );
  assert.throws(
    () => validatePatchSpecs([{...patches[0], apply_exactly_once: false}]),
    issue("PATCH_BINDING_INVALID"),
  );
});

test("only the two typed manifests may rebind through the focus build lock", () => {
  const typed = "a".repeat(64);
  const overlay = "b".repeat(64);
  const first = "c".repeat(64);
  const lock = {
    feature_inputs: {
      swu_007: {overlay_manifest: {sha256: overlay}},
      swu_008f: {first_working_version_manifest: {sha256: first}},
    },
  };
  assert.equal(
    expectedTypedSourceDigest(
      "root/upstream/overlay/overlay-manifest.json",
      typed,
      lock,
    ),
    overlay,
  );
  assert.equal(
    expectedTypedSourceDigest(
      "root/upstream/overlay/first-working-version-manifest.json",
      typed,
      lock,
    ),
    first,
  );
  assert.equal(
    expectedTypedSourceDigest("root/upstream/overlay/src/oew/store.ts", typed, lock),
    typed,
  );
  assert.throws(
    () =>
      expectedTypedSourceDigest(
        "root/upstream/overlay/overlay-manifest.json",
        typed,
        {},
      ),
    issue("BUILD_LOCK_REBINDING_MISSING"),
  );
});

test("tree identity is stable and rejects symlinked outputs", async () => {
  const root = await mkdtemp(join(tmpdir(), "oewtp-build-test-"));
  try {
    await mkdir(join(root, "assets"));
    await writeFile(join(root, "index.html"), "ok\n");
    await writeFile(join(root, "assets/app.js"), "app\n");
    const first = await treeIdentity(root);
    const second = await treeIdentity(root);
    assert.deepEqual(first, second);
    assert.equal(first.file_count, 2);
    await symlink(join(root, "index.html"), join(root, "assets/link"));
    await assert.rejects(() => treeIdentity(root), issue("TREE_SYMLINK"));
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
