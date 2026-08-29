import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const cliRoot = path.resolve(testDir, "../..");
const packageJson = JSON.parse(fs.readFileSync(path.join(cliRoot, "package.json"), "utf8"));
const tsconfig = JSON.parse(fs.readFileSync(path.join(cliRoot, "tsconfig.json"), "utf8"));
const source = fs.readFileSync(path.join(cliRoot, "src/index.ts"), "utf8");
const versionSource = fs.readFileSync(path.join(cliRoot, "src/version.ts"), "utf8");

test("package identity and supported bin are exact", () => {
  assert.equal(packageJson.name, "@domainspec-v2/cli");
  assert.equal(packageJson.version, "0.0.0-candidate.2");
  assert.equal(packageJson.private, true);
  assert.equal(packageJson.type, "module");
  assert.deepEqual(packageJson.bin, { "domainspec-v2": "./dist/cli/main.js" });
});

test("only the curated root entry is exported", () => {
  assert.deepEqual(packageJson.exports, {
    ".": { types: "./dist/index.d.ts", import: "./dist/index.js" }
  });
  assert.deepEqual(packageJson.files, ["dist", "README.md"]);
  assert.equal("workspaces" in packageJson, false);
  assert.equal("dependencies" in packageJson, false);
  assert.equal("devDependencies" in packageJson, false);
  assert.equal("scripts" in packageJson, false);
});

test("development and factory command surfaces are not re-exported", () => {
  for (const forbidden of ["roundtrip", "derive", "self-check", "emit-tests", "factory", "replay", "verify"]) {
    assert.equal(source.includes(forbidden), false, forbidden);
    assert.equal(JSON.stringify(packageJson.exports).includes(forbidden), false, forbidden);
  }
  assert.match(source, /from "\.\/version\.js"/);
});

test("runtime and platform declarations remain exact and non-authoritative", () => {
  assert.deepEqual(packageJson.engines, { node: "26.8.1", npm: "11.19.0" });
  assert.equal(packageJson.packageManager, "npm@11.19.0");
  assert.deepEqual(packageJson.os, ["linux"]);
  assert.deepEqual(packageJson.cpu, ["x64"]);
  assert.match(versionSource, /SUPPORTED_NODE_VERSION = "v26\.8\.1"/);
  assert.match(versionSource, /AUTHORITY_EFFECT = "none"/);
});

test("TypeScript boundary is strict NodeNext and source-only", () => {
  assert.equal(tsconfig.compilerOptions.module, "NodeNext");
  assert.equal(tsconfig.compilerOptions.moduleResolution, "NodeNext");
  assert.equal(tsconfig.compilerOptions.strict, true);
  assert.equal(tsconfig.compilerOptions.rootDir, "src");
  assert.equal(tsconfig.compilerOptions.outDir, "dist");
  assert.deepEqual(tsconfig.include, ["src/**/*.ts"]);
});
