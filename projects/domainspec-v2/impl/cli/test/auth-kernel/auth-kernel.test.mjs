import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  AuthKernelContractError,
  checkAuthKernel,
  materializeAuthKernel,
  renderAuthKernel,
} from "../../tools/auth-kernel.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(here, "../../../../../..");
const projectRoot = path.join(repositoryRoot, "projects/auth-foundation/implementation/domainspec");

test("Auth kernel generation is deterministic and bound to the frozen Rust meta-type rows", () => {
  const first = renderAuthKernel({ repositoryRoot, projectRoot });
  const second = renderAuthKernel({ repositoryRoot, projectRoot });
  assert.deepEqual([...first.outputs], [...second.outputs]);
  assert.equal(first.model.instantiation.baseline_ref.id, "domainspec-meta-types-current-implemented@10");
  assert.deepEqual([...first.model.realizations.keys()], ["DS-D1.1", "DS-D1.7"]);
  const lib = first.outputs.get("src/lib.rs").toString("utf8");
  assert.match(lib, /pub fn authorize\(context: EvaluationContext/);
  assert.match(lib, /DOMAINSPEC_SOURCE_AGGREGATE_SHA256/);
});

test("Auth kernel check detects generated source drift", () => {
  const outputRoot = fs.mkdtempSync(path.join(os.tmpdir(), "domainspec-auth-kernel-"));
  try {
    materializeAuthKernel({ repositoryRoot, projectRoot, outputRoot });
    checkAuthKernel({ repositoryRoot, projectRoot, outputRoot });
    fs.appendFileSync(path.join(outputRoot, "src/lib.rs"), "// drift\n");
    assert.throws(
      () => checkAuthKernel({ repositoryRoot, projectRoot, outputRoot }),
      (error) => error instanceof AuthKernelContractError && error.code === "AKC_TARGET_DRIFT",
    );
  } finally {
    fs.rmSync(outputRoot, { recursive: true, force: true });
  }
});
