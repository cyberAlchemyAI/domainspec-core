import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

// Round-trip: generate canonical example instances from the schemas, then validate them (DEF-D3 source B).
const thisDir = dirname(fileURLToPath(import.meta.url));
const implRoot = resolve(thisDir, "../../");
const tool = "tools/instances.ts";

function run(args: string[]) {
  return spawnSync(process.execPath, ["--import", "tsx", tool, ...args], {
    cwd: implRoot,
    encoding: "utf-8",
  });
}

test("generate emits an example instance per schema; every generated instance validates", () => {
  const dir = mkdtempSync(join(tmpdir(), "dsv2-inst-"));
  try {
    const gen = run(["generate", "--out-dir", dir]);
    assert.equal(gen.status, 0, gen.stdout + gen.stderr);
    assert.match(gen.stdout, /generated \d+ example/);
    const val = run(["validate", "--dir", dir]);
    assert.equal(val.status, 0, val.stdout + val.stderr);
    assert.match(val.stdout, /PASS/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("a malformed instance is rejected (Entity example with the identity flag dropped)", () => {
  const dir = mkdtempSync(join(tmpdir(), "dsv2-inst-"));
  try {
    run(["generate", "--out-dir", dir]);
    const entity = readFileSync(join(dir, "entity.example.instance.yml"), "utf-8");
    const mutant = entity.replace(/field_identity: \[[^\]]*\]/, "field_identity: [no, no]");
    assert.notEqual(mutant, entity, "mutation should have changed the instance");
    const mfile = join(dir, "entity-mutant.instance.yml");
    writeFileSync(mfile, mutant, "utf-8");
    const val = run(["validate", "--file", mfile]);
    assert.equal(val.status, 1, val.stdout + val.stderr);
    assert.match(val.stdout, /identity/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
