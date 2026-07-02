import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

// Black-box CLI test (build-from-owned: governance/tags/tools/tests/). Spawns the real validator
// over temp fixtures and asserts exit code + stdout. Schemas resolve from spec/meta-types (default).
const thisDir = dirname(fileURLToPath(import.meta.url));
const implRoot = resolve(thisDir, "../../");
const validator = "tools/validate-content.ts";

function runValidator(args: string[]) {
  return spawnSync(process.execPath, ["--import", "tsx", validator, ...args], {
    cwd: implRoot,
    encoding: "utf-8",
  });
}

function withFixture(body: string, run: (file: string) => void): void {
  const dir = mkdtempSync(join(tmpdir(), "dsv2-mt-"));
  try {
    const file = join(dir, "aspect.md");
    writeFileSync(file, body, "utf-8");
    run(file);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

function aspect(concept: string, type: string, rows: string[]): string {
  return [
    "# fixture",
    "",
    "## Concept Registry",
    "| Concept | Type |",
    "| --- | --- |",
    `| ${concept} | ${type} |`,
    "",
    `## ${concept}`,
    "| Field | Type | Required | Identity | Description |",
    "| --- | --- | --- | --- | --- |",
    ...rows,
    "",
  ].join("\n");
}

const ENTITY_OK = aspect("PaymentTransaction", "Entity", [
  "| id | UUID | yes | yes | identity |",
  "| amount | Money | yes |  | amount |",
]);

const ENTITY_NO_IDENTITY = aspect("Money", "Entity", [
  "| amount | Decimal | yes |  | amount |",
  "| currency | Currency | yes |  | code |",
]);

const ENTITY_UNTYPED = aspect("Widget", "Entity", [
  "| id | UUID | yes | yes | identity |",
  "| label |  | yes |  | untyped field |",
]);

test("Entity positive fixture passes (exit 0)", () => {
  withFixture(ENTITY_OK, (file) => {
    const r = runValidator(["--file", file]);
    assert.equal(r.status, 0, r.stdout + r.stderr);
    assert.match(r.stdout, /PASS/);
  });
});

test("Entity without identity is rejected as Entity (exit 1, identity violation)", () => {
  withFixture(ENTITY_NO_IDENTITY, (file) => {
    const r = runValidator(["--file", file]);
    assert.equal(r.status, 1, r.stdout + r.stderr);
    assert.match(r.stdout, /identity/);
  });
});

test("Entity with an untyped field is rejected (exit 1, typedness violation)", () => {
  withFixture(ENTITY_UNTYPED, (file) => {
    const r = runValidator(["--file", file]);
    assert.equal(r.status, 1, r.stdout + r.stderr);
    assert.match(r.stdout, /typedness/);
  });
});

test("committed Entity fixtures behave (ok passes, bad rejected)", () => {
  const ok = runValidator(["--file", "spec/__fixtures__/mt/entity-ok.md"]);
  assert.equal(ok.status, 0, ok.stdout + ok.stderr);
  const bad = runValidator(["--file", "spec/__fixtures__/mt/entity-bad.md"]);
  assert.equal(bad.status, 1, bad.stdout + bad.stderr);
});

test("Value Object fixtures behave (ok passes, bad rejected as VO)", () => {
  const ok = runValidator(["--file", "spec/__fixtures__/mt/value-object-ok.md"]);
  assert.equal(ok.status, 0, ok.stdout + ok.stderr);
  const bad = runValidator(["--file", "spec/__fixtures__/mt/value-object-bad.md"]);
  assert.equal(bad.status, 1, bad.stdout + bad.stderr);
  assert.match(bad.stdout, /no_identity/);
});

test("Enum fixtures behave (ok passes, bad rejected as Enum)", () => {
  const ok = runValidator(["--file", "spec/__fixtures__/mt/enum-ok.md"]);
  assert.equal(ok.status, 0, ok.stdout + ok.stderr);
  const bad = runValidator(["--file", "spec/__fixtures__/mt/enum-bad.md"]);
  assert.equal(bad.status, 1, bad.stdout + bad.stderr);
  assert.match(bad.stdout, /value_table/);
});

test("cross-discrimination: identity-bearing concept rejected as Value Object", () => {
  const body =
    aspect("Thing", "Value Object", [
      "| id | UUID | yes | yes | identity |",
      "| name | String | yes |  | label |",
    ]) + "\n**Equality:** two Thing are equal by id.\n";
  withFixture(body, (file) => {
    const r = runValidator(["--file", file]);
    assert.equal(r.status, 1, r.stdout + r.stderr);
    assert.match(r.stdout, /no_identity/);
  });
});
