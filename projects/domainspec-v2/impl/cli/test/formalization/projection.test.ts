import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { runCli } from "../../src/cli/main.ts";
import { createMetaTypeFormalizationProjection, renderLeanMetaTypeFormalization } from "../../src/formalization/projection.ts";
import { loadCompiledProjectGraph } from "../../src/input/project-model.ts";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const fixtureRoot = path.resolve(testDir, "../../fixtures/input-roots/canonical-project");

function createRoot(): { readonly parent: string; readonly source: string; readonly target: string } {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "mtcli-formalize-"));
  const source = path.join(parent, "source");
  fs.cpSync(fixtureRoot, source, { recursive: true });
  return { parent, source, target: path.join(parent, "generated", "Current.lean") };
}

function writeJson(filePath: string, value: unknown): void {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function mutateJson(filePath: string, mutation: (value: Record<string, unknown>) => void): void {
  const value = JSON.parse(fs.readFileSync(filePath, "utf8")) as Record<string, unknown>;
  mutation(value);
  writeJson(filePath, value);
}

function formalizeFailure(source: string, target: string): Readonly<Record<string, unknown>> {
  const output: string[] = [];
  assert.equal(runCli(["formalize", source, "--target", target], { stdout: () => undefined, stderr: (value) => output.push(value) }), 22);
  return JSON.parse(output.at(-1)!);
}

test("formalization projects the compiled graph, all 45 DS-D8 obligations, and applicable witnesses", () => {
  const projection = createMetaTypeFormalizationProjection(loadCompiledProjectGraph(fixtureRoot));
  assert.equal(projection.meta_types.length, 24);
  assert.equal(projection.relationships.length, 31);
  assert.equal(projection.obligation_catalog.length, 45);
  assert.deepEqual(new Set(projection.obligation_catalog.map(({ family }) => family)), new Set(["endpoint", "scope", "multiplicity", "generated-projection", "inverse-collapse", "deprecation"]));
  assert.equal(projection.project_graph.nodes.length, 7);
  assert.equal(projection.project_graph.edges.length, 7);
  assert.equal(projection.applicable_witnesses.length, projection.project_graph.edges.reduce((total, edge) => total + edge.obligation_ids.length, 0));
  const familyByObligation = new Map(projection.obligation_catalog.map(({ obligation_id, family }) => [obligation_id, family]));
  assert.deepEqual(
    new Set(projection.applicable_witnesses.map(({ obligation_id }) => familyByObligation.get(obligation_id))),
    new Set(["endpoint", "scope", "multiplicity", "generated-projection", "inverse-collapse", "deprecation"]),
  );
  const lean = renderLeanMetaTypeFormalization(projection);
  assert.match(lean, /theorem allObligationIds_count : allObligationIds\.length = 45/);
  assert.match(lean, /def obligationHolds/);
  assert.match(lean, /theorem allApplicableWitnessesHold/);
  assert.match(lean, /def stateMachineHolds/);
  assert.match(lean, /theorem allProjectStateMachinesHold/);
  assert.match(lean, /theorem invalidCurrentStateRejected/);
  assert.match(lean, /theorem undeclaredTransitionRejected/);
  assert.match(lean, /theorem sourceMismatchRejected/);
  assert.match(lean, /theorem guardFailureRejected/);
  const stateMachine = projection.project_graph.nodes.find(({ selector }) => selector === "beta:settlement-status");
  assert.deepEqual(stateMachine?.state_machine_states, ["pending", "settled", "failed"]);
  assert.equal(stateMachine?.state_machine_initial, "pending");
  assert.deepEqual(stateMachine?.state_machine_transitions.map(({ transition_id }) => transition_id), ["complete-settlement", "fail-settlement"]);
});

test("formalize materializes compilable Lean once and formalize-check detects byte drift", () => {
  const { parent, source, target } = createRoot();
  const output: string[] = [];
  const errors: string[] = [];
  const io = { stdout: (value: string) => output.push(value), stderr: (value: string) => errors.push(value) };
  try {
    assert.equal(runCli(["formalize", source, "--target", target], io), 0);
    const materialized = JSON.parse(output.pop()!);
    assert.equal(materialized.result, "pass");
    assert.match(materialized.project_graph_sha256, /^[a-f0-9]{64}$/);
    assert.equal(runCli(["formalize-check", source, "--target", target], io), 0);
    assert.equal(JSON.parse(output.pop()!).result, "pass");
    fs.appendFileSync(target, "-- drift\n");
    assert.equal(runCli(["formalize-check", source, "--target", target], io), 1);
    assert.equal(JSON.parse(output.pop()!).result, "fail");
    assert.deepEqual(errors, []);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("generated Lean compiles when a Lean provider is available", (context) => {
  const available = spawnSync("lean", ["--version"], { encoding: "utf8" });
  if (available.error && (available.error as NodeJS.ErrnoException).code === "ENOENT") {
    context.skip("Lean provider is not installed in this Node package environment");
    return;
  }
  assert.equal(available.status, 0, `${available.stdout}${available.stderr}`);
  const { parent, source, target } = createRoot();
  try {
    assert.equal(runCli(["formalize", source, "--target", target], { stdout: () => undefined, stderr: () => undefined }), 0);
    const lean = spawnSync("lean", [target], { encoding: "utf8" });
    assert.equal(lean.status, 0, `${lean.stdout}${lean.stderr}`);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("authored graph changes causally change projection and Lean bytes", () => {
  const { parent, source } = createRoot();
  try {
    const before = createMetaTypeFormalizationProjection(loadCompiledProjectGraph(source));
    mutateJson(path.join(source, "specs/alpha/feature.json"), (feature) => (feature.edges as string[]).push("customer-performs-settle-again"));
    writeJson(path.join(source, "specs/alpha/edges/customer-performs-settle-again.json"), {
      schema_version: "domainspec.edge/v1", edge_id: "customer-performs-settle-again", feature_id: "alpha", relationship: "performs",
      source_node_id: "customer", target_node_id: "settle", scope: "feature",
    });
    const after = createMetaTypeFormalizationProjection(loadCompiledProjectGraph(source));
    assert.notEqual(after.project_graph.source_manifest_sha256, before.project_graph.source_manifest_sha256);
    assert.notEqual(after.project_graph.graph_sha256, before.project_graph.graph_sha256);
    assert.notEqual(renderLeanMetaTypeFormalization(after), renderLeanMetaTypeFormalization(before));
    assert.equal(after.project_graph.edges.length, before.project_graph.edges.length + 1);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("State Machine source changes causally change the compiled projection and Lean predicates", () => {
  const { parent, source } = createRoot();
  try {
    const before = createMetaTypeFormalizationProjection(loadCompiledProjectGraph(source));
    mutateJson(path.join(source, "specs/beta/nodes/settlement-status.json"), (node) => {
      const transitions = (node.body as { transitions: Array<Record<string, unknown>> }).transitions;
      transitions[0]!.guard_ref = null;
    });
    const after = createMetaTypeFormalizationProjection(loadCompiledProjectGraph(source));
    assert.notEqual(after.project_graph.source_manifest_sha256, before.project_graph.source_manifest_sha256);
    assert.notEqual(after.project_graph.graph_sha256, before.project_graph.graph_sha256);
    assert.notEqual(renderLeanMetaTypeFormalization(after), renderLeanMetaTypeFormalization(before));
    assert.equal(after.project_graph.nodes.find(({ selector }) => selector === "beta:settlement-status")?.state_machine_transitions[0]?.guard_ref, "");
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("hostile relationship and State Machine graphs fail causally", () => {
  const cases: Array<{ readonly code: string; readonly mutate: (source: string) => void }> = [
    { code: "MTCLI_RELATIONSHIP_ENDPOINT", mutate: (source) => mutateJson(path.join(source, "specs/beta/edges/audit-owns-settled.json"), (edge) => { edge.relationship = "produces"; }) },
    { code: "MTCLI_RELATIONSHIP_SCOPE", mutate: (source) => mutateJson(path.join(source, "edges/alpha-to-beta.json"), (edge) => { edge.source_feature_id = "alpha"; edge.source_node_id = "settle"; edge.target_feature_id = "beta"; edge.target_node_id = "audit"; edge.relationship = "creates"; }) },
    { code: "MTCLI_INPUT_BODY", mutate: (source) => mutateJson(path.join(source, "specs/alpha/nodes/settle.json"), (node) => { (node.body as Record<string, unknown>).creation_targets = ["alpha:customer"]; }) },
    { code: "MTCLI_RELATIONSHIP_GENERATED_VIEW", mutate: (source) => mutateJson(path.join(source, "specs/beta/edges/audit-owns-settled.json"), (edge) => { edge.relationship = "owned-by"; }) },
    { code: "MTCLI_RELATIONSHIP_DEPRECATED", mutate: (source) => mutateJson(path.join(source, "specs/beta/edges/audit-owns-settled.json"), (edge) => { edge.relationship = "queries"; }) },
    { code: "MTCLI_RELATIONSHIP_INVERSE_COLLAPSE", mutate: (source) => {
      mutateJson(path.join(source, "specs/beta/feature.json"), (feature) => (feature.edges as string[]).push("settled-belongs-to-audit"));
      writeJson(path.join(source, "specs/beta/edges/settled-belongs-to-audit.json"), { schema_version: "domainspec.edge/v1", edge_id: "settled-belongs-to-audit", feature_id: "beta", relationship: "belongs-to", source_node_id: "settled", target_node_id: "audit", scope: "feature" });
    } },
    { code: "MTCLI_RELATIONSHIP_MULTIPLICITY", mutate: (source) => {
      mutateJson(path.join(source, "specs/alpha/feature.json"), (feature) => { (feature.nodes as string[]).push("account"); (feature.edges as string[]).push("settle-creates-account"); });
      writeJson(path.join(source, "specs/alpha/nodes/account.json"), { schema_version: "domainspec.node/v1", node_id: "account", feature_id: "alpha", kind: "Entity", body: { description: "A second entity.", fields: [] } });
      writeJson(path.join(source, "specs/alpha/edges/settle-creates-account.json"), { schema_version: "domainspec.edge/v1", edge_id: "settle-creates-account", feature_id: "alpha", relationship: "creates", source_node_id: "settle", target_node_id: "account", scope: "feature" });
    } },
    { code: "MTCLI_STATE_MACHINE_STATE", mutate: (source) => mutateJson(path.join(source, "specs/beta/nodes/settlement-status.json"), (node) => { ((node.body as { transitions: Array<Record<string, unknown>> }).transitions[0]!).source_state = "unknown"; }) },
    { code: "MTCLI_STATE_MACHINE_DUPLICATE_TRANSITION", mutate: (source) => mutateJson(path.join(source, "specs/beta/nodes/settlement-status.json"), (node) => { ((node.body as { transitions: Array<Record<string, unknown>> }).transitions[1]!).transition_id = "complete-settlement"; }) },
    { code: "MTCLI_STATE_MACHINE_GUARD_REFERENCE", mutate: (source) => mutateJson(path.join(source, "specs/beta/nodes/settlement-status.json"), (node) => { ((node.body as { transitions: Array<Record<string, unknown>> }).transitions[0]!).guard_ref = "beta:settled"; }) },
    { code: "MTCLI_STATE_MACHINE_EVENT_RELATIONSHIP_MISSING", mutate: (source) => {
      mutateJson(path.join(source, "specs/beta/feature.json"), (feature) => { feature.edges = (feature.edges as string[]).filter((edge) => edge !== "settlement-completed-transitions-settlement-status"); });
      fs.rmSync(path.join(source, "specs/beta/edges/settlement-completed-transitions-settlement-status.json"));
    } },
  ];
  for (const hostile of cases) {
    const { parent, source, target } = createRoot();
    try {
      hostile.mutate(source);
      assert.equal(formalizeFailure(source, target).code, hostile.code);
      assert.equal(fs.existsSync(target), false);
    } finally {
      fs.rmSync(parent, { recursive: true, force: true });
    }
  }
});
