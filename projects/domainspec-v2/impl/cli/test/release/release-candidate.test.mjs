import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

import { buildReleaseCandidate } from "../../tools/build-release-candidate.mjs";
import { canonicalJson, verifyReleaseCandidate } from "../../tools/verify-release-candidate.mjs";

function run(command, args, cwd) {
  const result = spawnSync(command, args, {
    cwd,
    encoding: "utf8",
    env: { ...process.env, npm_config_audit: "false", npm_config_fund: "false", npm_config_update_notifier: "false", npm_config_cache: path.join(os.tmpdir(), "domainspec-release-test-npm-cache") },
  });
  if (result.status !== 0) throw new Error(`${command} ${args.join(" ")} failed (${result.status})\n${result.stdout}\n${result.stderr}`);
  return result.stdout.trim();
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function createSource(root, fakeGit) {
  writeJson(path.join(root, "package.json"), {
    name: "@domainspec-v2/cli",
    version: "1.0.0",
    private: false,
    type: "module",
    bin: { "domainspec-v2": "./dist/cli/main.js" },
    exports: { ".": "./dist/index.js" },
    files: ["dist", "README.md"],
    engines: { node: "26.8.1", npm: "11.19.0" },
    packageManager: "npm@11.19.0",
    scripts: { build: "node synthetic-build.mjs" },
  });
  writeJson(path.join(root, "package-lock.json"), {
    name: "@domainspec-v2/cli",
    version: "1.0.0",
    lockfileVersion: 3,
    requires: true,
    packages: {
      "": {
        name: "@domainspec-v2/cli",
        version: "1.0.0",
        bin: { "domainspec-v2": "dist/cli/main.js" },
        engines: { node: "26.8.1", npm: "11.19.0" },
      },
    },
  });
  fs.writeFileSync(path.join(root, "README.md"), "# Synthetic DomainSpec release candidate\n");
  fs.writeFileSync(path.join(root, "product-value.txt"), "one\n");
  fs.writeFileSync(path.join(root, "synthetic-build.mjs"), "import fs from 'node:fs';\nimport path from 'node:path';\nconst value = fs.readFileSync('product-value.txt', 'utf8').trim();\nfs.mkdirSync(path.join('dist', 'cli'), { recursive: true });\nfs.writeFileSync(path.join('dist', 'index.js'), `export const releaseCandidateFixture = '${value}';\\n`);\nfs.writeFileSync(path.join('dist', 'cli', 'main.js'), `#!/usr/bin/env node\\nprocess.stdout.write('1.0.0\\\\n');\\n`, { mode: 0o755 });\n");
  fs.writeFileSync(path.join(root, "pnpm-lock.yaml"), "lockfileVersion: '9.0'\n");
  const commit = "1".repeat(40);
  fs.writeFileSync(path.join(root, ".release-commit"), `${commit}\n`);
  fs.writeFileSync(path.join(root, ".release-status"), "");
  fs.writeFileSync(fakeGit, `#!/bin/sh\ncase "$1 $2" in\n  "rev-parse HEAD") cat .release-commit ;;\n  "status --porcelain=v1") cat .release-status ;;\n  "config --get") printf '%s\\n' 'https://example.invalid/domainspec-core.git' ;;\n  *) exit 64 ;;\nesac\n`, { mode: 0o755 });
  return commit;
}

function createQualification(root) {
  const certificate = {
    schema_version: "domainspec.recipe-qualification-certificate/v1",
    result: "pass",
    certificate_sha256: "a".repeat(64),
    authority_effect: "none",
  };
  writeJson(path.join(root, "qualification-profile.json"), { schema_version: "domainspec.recipe-qualification-profile/v1", authority_effect: "none" });
  writeJson(path.join(root, "run-1", "qualification-certificate.json"), certificate);
  writeJson(path.join(root, "run-2", "qualification-certificate.json"), certificate);
  writeJson(path.join(root, "equivalence.json"), {
    schema_version: "domainspec.recipe-qualification-l1-equivalence/v1",
    result: "pass",
    checks: [{ id: "certificate-byte-equivalence", result: "pass" }],
    observed: { certificate_sha256: certificate.certificate_sha256 },
    evidence_root: root,
    authority_effect: "none",
  });
}

function byteInventory(root) {
  const rows = [];
  function visit(relative) {
    for (const entry of fs.readdirSync(path.join(root, relative), { withFileTypes: true }).sort((left, right) => left.name < right.name ? -1 : left.name > right.name ? 1 : 0)) {
      const child = relative ? `${relative}/${entry.name}` : entry.name;
      if (entry.isDirectory()) visit(child);
      else {
        const bytes = fs.readFileSync(path.join(root, child));
        rows.push({ path: child, size: bytes.length, sha256: crypto.createHash("sha256").update(bytes).digest("hex") });
      }
    }
  }
  visit("");
  return rows;
}

function installAndObserve(tarball, consumer) {
  fs.mkdirSync(consumer);
  writeJson(path.join(consumer, "package.json"), { private: true, type: "module" });
  run("npm", ["install", "--ignore-scripts", "--no-audit", "--no-fund", tarball], consumer);
  const imported = run(process.execPath, ["--input-type=module", "-e", "const value = await import('@domainspec-v2/cli'); process.stdout.write(value.releaseCandidateFixture);"], consumer);
  const version = run(path.join(consumer, "node_modules", ".bin", "domainspec-v2"), [], consumer);
  return { imported, version };
}

test("release candidate is deterministic, independently verifiable, installable, hostile-sensitive, and source-sensitive", () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "domainspec-release-candidate-test-"));
  try {
    const source = path.join(temporary, "source");
    const qualification = path.join(temporary, "qualification");
    fs.mkdirSync(source);
    fs.mkdirSync(qualification);
    const fakeGit = path.join(temporary, "fake-git");
    const firstCommit = createSource(source, fakeGit);
    createQualification(qualification);
    const first = path.join(temporary, "candidate-one");
    const second = path.join(temporary, "candidate-two");
    const firstBuild = buildReleaseCandidate({ repositoryRoot: source, packageRoot: source, qualificationEvidenceRoot: qualification, outputRoot: first, sourceCommit: firstCommit, gitExecutable: fakeGit, sourceSnapshotRoot: source });
    const secondBuild = buildReleaseCandidate({ repositoryRoot: source, packageRoot: source, qualificationEvidenceRoot: qualification, outputRoot: second, sourceCommit: firstCommit, gitExecutable: fakeGit, sourceSnapshotRoot: source });
    assert.equal(firstBuild.result, "pass");
    assert.equal(firstBuild.authority_effect, "none");
    assert.deepEqual(byteInventory(first), byteInventory(second));
    const firstVerification = verifyReleaseCandidate(first, firstCommit);
    assert.equal(firstVerification.result, "pass", JSON.stringify(firstVerification, null, 2));
    const command = spawnSync(process.execPath, [path.join(first, "verify-release-candidate.mjs"), "--bundle-root", first, "--expected-source-commit", firstCommit], { encoding: "utf8" });
    assert.equal(command.status, 0, command.stderr);
    assert.equal(JSON.parse(command.stdout).result, "pass");

    const tarball = path.join(first, "package", "domainspec-v2-cli-1.0.0.tgz");
    assert.deepEqual(installAndObserve(tarball, path.join(temporary, "consumer-one")), { imported: "one", version: "1.0.0" });
    assert.deepEqual(installAndObserve(tarball, path.join(temporary, "consumer-two")), { imported: "one", version: "1.0.0" });

    const tamperedPackage = path.join(temporary, "tampered-package");
    fs.cpSync(first, tamperedPackage, { recursive: true });
    fs.appendFileSync(path.join(tamperedPackage, "package", "domainspec-v2-cli-1.0.0.tgz"), "tamper");
    assert.equal(verifyReleaseCandidate(tamperedPackage, firstCommit).result, "fail");
    const missingEvidence = path.join(temporary, "missing-evidence");
    fs.cpSync(first, missingEvidence, { recursive: true });
    fs.rmSync(path.join(missingEvidence, "qualification", "run-2", "qualification-certificate.json"));
    assert.equal(verifyReleaseCandidate(missingEvidence, firstCommit).result, "fail");

    fs.writeFileSync(path.join(source, "product-value.txt"), "two\n");
    fs.writeFileSync(path.join(source, ".release-status"), " M product-value.txt\n");
    assert.throws(() => buildReleaseCandidate({ repositoryRoot: source, packageRoot: source, qualificationEvidenceRoot: qualification, outputRoot: path.join(temporary, "dirty-candidate"), sourceCommit: firstCommit, gitExecutable: fakeGit, sourceSnapshotRoot: source }), /clean source tree/);
    const secondCommit = "2".repeat(40);
    fs.writeFileSync(path.join(source, ".release-commit"), `${secondCommit}\n`);
    fs.writeFileSync(path.join(source, ".release-status"), "");
    const changed = path.join(temporary, "candidate-changed");
    const changedBuild = buildReleaseCandidate({ repositoryRoot: source, packageRoot: source, qualificationEvidenceRoot: qualification, outputRoot: changed, sourceCommit: secondCommit, gitExecutable: fakeGit, sourceSnapshotRoot: source });
    assert.notEqual(changedBuild.package_sha256, firstBuild.package_sha256);
    assert.notEqual(changedBuild.manifest_sha256, firstBuild.manifest_sha256);
    assert.notEqual(canonicalJson(JSON.parse(fs.readFileSync(path.join(changed, "candidate.json")))), canonicalJson(JSON.parse(fs.readFileSync(path.join(first, "candidate.json")))));
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
});
