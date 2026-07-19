import assert from "node:assert/strict";
import { cpSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  MintedProjectCompilerError,
  compileMintedProject,
  type MintedProjectCompileOptions,
} from "../minted-project/compiler";
import { mintMintedProject } from "../minted-project/minter";
import { buildMintedProjectViews, verifyMintedProjectBuild } from "../minted-project/views";

type JsonObject = Record<string, any>;

const thisDir = dirname(fileURLToPath(import.meta.url));
const implRoot = resolve(thisDir, "../..");
const projectRoot = resolve(implRoot, "spec/features/ui-profile-create-player");
const registryPath = resolve(implRoot, "spec/ui-profile/minted-project-profile.json");
const generatedRoot = resolve(projectRoot, "generated");
const options: MintedProjectCompileOptions = {
  developmentProfileRegistry: {
    path: registryPath,
    handle: "ui-development-explicit-v0.1",
  },
};

function json(path: string): JsonObject {
  return JSON.parse(readFileSync(path, "utf8")) as JsonObject;
}

function writeJson(path: string, value: unknown): void {
  writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`);
}

function expectCompilerCode(action: () => unknown, code: string): void {
  assert.throws(action, (error: unknown) => {
    assert.ok(error instanceof MintedProjectCompilerError);
    assert.equal(error.code, code);
    return true;
  });
}

function temporaryProject(): { root: string; cleanup: () => void } {
  const root = mkdtempSync(resolve(tmpdir(), "domainspec-ui-engine-"));
  cpSync(projectRoot, root, { recursive: true });
  return { root, cleanup: () => rmSync(root, { recursive: true, force: true }) };
}

test("development profile fails closed without its explicit handle", () => {
  expectCompilerCode(
    () => compileMintedProject(projectRoot),
    "DEVELOPMENT_PROFILE_HANDLE_REQUIRED",
  );
  expectCompilerCode(
    () =>
      compileMintedProject(projectRoot, {
        developmentProfileRegistry: { path: registryPath, handle: "wrong-handle" },
      }),
    "DEVELOPMENT_PROFILE_HANDLE_INVALID",
  );
});

test("explicit development compile is byte-stable and preserves all source handles", () => {
  const first = compileMintedProject(projectRoot, options);
  const second = compileMintedProject(projectRoot, options);
  assert.equal(first.graphBytes, second.graphBytes);
  assert.equal(first.sourceManifestBytes, second.sourceManifestBytes);
  assert.equal(first.graph.nodes.length, 17);
  assert.equal(first.graph.edges.length, 20);
  assert.equal(first.sourceManifest.inputs.length, 19);
  assert.equal(first.sourceManifest.records.length, 37);
  assert.equal(first.graph.language.profile_digest, json(resolve(projectRoot, "project.json")).language.profile.digest);
  assert.deepEqual(
    first.sourceManifest.records.map((record) => record.graph_id).sort(),
    [
      ...first.graph.nodes.map((node) => node.node_id),
      ...first.graph.edges.map((edge) => edge.edge_id),
    ].sort(),
  );
});

test("existing view builder emits deterministic verified human and machine views", () => {
  const first = buildMintedProjectViews(projectRoot, options);
  const second = buildMintedProjectViews(projectRoot, options);
  assert.equal(first.graphBytes, second.graphBytes);
  assert.equal(first.markdownBytes, second.markdownBytes);
  assert.equal(first.buildReceiptBytes, second.buildReceiptBytes);
  assert.deepEqual(verifyMintedProjectBuild(projectRoot, first), { status: "pass", codes: [] });
  assert.match(first.markdownBytes, /CreatePlayerPage/);
  assert.match(first.markdownBytes, /CreatePlayerAdapter/);
  assert.equal((first.markdownBytes.match(/^\| `ui-profile-create-player\.(?!edge\.)[^`]+` \|/gm) ?? []).length, 17);
  assert.equal((first.markdownBytes.match(/^\| `ui-profile-create-player\.edge\..+` \|/gm) ?? []).length, 20);
});

test("development formation and endpoint mutants fail with existing compiler codes", () => {
  const formation = temporaryProject();
  try {
    const path = resolve(formation.root, "nodes/create-player-form.json");
    const node = json(path);
    node.body.typed_fields = "";
    writeJson(path, node);
    expectCompilerCode(() => compileMintedProject(formation.root, options), "FORMATION_INVALID");
  } finally {
    formation.cleanup();
  }

  const endpoint = temporaryProject();
  try {
    const path = resolve(endpoint.root, "nodes/create-player-page.json");
    const node = json(path);
    node.connections[0].to = "ui-profile-create-player.CreatePlayerForm";
    writeJson(path, node);
    expectCompilerCode(
      () => compileMintedProject(endpoint.root, options),
      "EDGE_ENDPOINT_KIND_MISMATCH",
    );
  } finally {
    endpoint.cleanup();
  }
});

test("generated traversal and per-node views cover every required representation", () => {
  const traversal = json(resolve(generatedRoot, "traversal.json"));
  const residue = json(resolve(generatedRoot, "residue.json"));
  const graph = json(resolve(generatedRoot, "graph.json"));
  assert.equal(graph.nodes.length, 17);
  assert.equal(graph.edges.length, 20);
  assert.equal(traversal.required_coverage.length, 11);
  assert.deepEqual(traversal.orphan_required_concepts, []);
  const page = traversal.roots.find((entry: JsonObject) => entry.kind === "Page");
  assert.equal(page.connected_reachable.length, 17);
  const state = traversal.required_coverage.find(
    (entry: JsonObject) => entry.concept_id === "DS-D1.25",
  );
  assert.equal(state.representation_handles.length, 2);
  assert.equal(readdirSync(resolve(generatedRoot, "nodes")).length, 17);
  assert.equal(residue.items.length, 5);
});

test("minter accepts the development profile only with explicit registry authority", () => {
  const parent = mkdtempSync(resolve(tmpdir(), "domainspec-ui-mint-"));
  try {
    const result = mintMintedProject({
      destination: resolve(parent, "ui-project"),
      projectId: "ui-project",
      profile: { id: "ui-development", version: "0.1" },
      developmentProfileRegistry: {
        path: registryPath,
        handle: "ui-development-explicit-v0.1",
      },
    });
    assert.equal(result.receipt.language.profile_id, "ui-development");
    assert.equal(json(resolve(result.projectRoot, "project.json")).features.length, 0);
    assert.equal(json(resolve(result.projectRoot, ".domainspec/generated/graph.json")).nodes.length, 0);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});
