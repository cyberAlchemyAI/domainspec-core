import { lstat, readFile, realpath } from "node:fs/promises";
import { resolve } from "node:path";

import type { LockedFactoryNodeV1, LockedFactoryRefV1 } from "../contracts/factory-run-lock-v1.js";
import type { FactoryRunPlanV1 } from "../contracts/factory-run-plan-v1.js";
import type { FactoryRunRequestV1 } from "../contracts/factory-run-request-v1.js";
import { getFactoryNodeProviderV1 } from "../registry/factory-node-registry-v1.js";
import { resolveFactoryComponentClosure } from "../resolution/resolve-component-closure.js";
import { resolveFactoryToolV1 } from "../resolution/resolve-toolchain.js";
import { canonicalJson, fail, sha256 } from "../shared/canonical.js";

const compareUtf8 = (left: string, right: string): number =>
  Buffer.from(left).compare(Buffer.from(right));

const topologicalOrder = (request: FactoryRunRequestV1): readonly string[] => {
  const nodes = new Map(request.nodes.map((node) => [node.node_id, node]));
  for (const node of request.nodes) {
    if (new Set(node.depends_on).size !== node.depends_on.length ||
        node.depends_on.includes(node.node_id) ||
        node.depends_on.some((dependency) => !nodes.has(dependency))) {
      fail("FACTORY_GRAPH_INVALID", node.node_id);
    }
  }
  const indegree = new Map(request.nodes.map((node) => [node.node_id, node.depends_on.length]));
  const ready = request.nodes.filter(({ node_id: id }) => indegree.get(id) === 0)
    .map(({ node_id: id }) => id).sort(compareUtf8);
  const ordered: string[] = [];
  while (ready.length > 0) {
    const id = ready.shift()!;
    ordered.push(id);
    for (const candidate of request.nodes) {
      if (!candidate.depends_on.includes(id)) continue;
      const remaining = (indegree.get(candidate.node_id) ?? 0) - 1;
      indegree.set(candidate.node_id, remaining);
      if (remaining === 0) {
        ready.push(candidate.node_id);
        ready.sort(compareUtf8);
      }
    }
  }
  if (ordered.length !== request.nodes.length) fail("FACTORY_GRAPH_INVALID", "cycle");
  return Object.freeze(ordered);
};

const resolveRef = async (
  repositoryRoot: string,
  role: string,
  path: string,
  expectedSha256?: string,
): Promise<LockedFactoryRefV1> => {
  const root = await realpath(repositoryRoot);
  const target = resolve(root, path);
  if (!target.startsWith(`${root}/`)) fail("FACTORY_REQUEST_INVALID", "path-escape");
  let owned: string;
  try {
    const stat = await lstat(target);
    if (!stat.isFile() || stat.isSymbolicLink()) fail("FACTORY_INPUT_INVALID", path);
    owned = await realpath(target);
  } catch (error) {
    if ((error as { code?: string }).code?.startsWith("FACTORY_")) throw error;
    return fail("FACTORY_INPUT_MISSING", path);
  }
  if (!owned.startsWith(`${root}/`)) fail("FACTORY_REQUEST_INVALID", "symlink-escape");
  const bytes = await readFile(owned);
  const observed = sha256(bytes);
  if (expectedSha256 !== undefined && observed !== expectedSha256) {
    fail("FACTORY_INPUT_TAMPERED", path);
  }
  return Object.freeze({ role, path, sha256: observed, byte_length: bytes.byteLength });
};

export const planFactoryRun = async (input: Readonly<{
  repositoryRoot: string;
  request: FactoryRunRequestV1;
}>): Promise<FactoryRunPlanV1> => {
  const orderedNodeIds = topologicalOrder(input.request);
  const requestSha256 = sha256(canonicalJson(input.request));
  const lockedNodes: LockedFactoryNodeV1[] = [];
  for (const nodeId of orderedNodeIds) {
    const node = input.request.nodes.find(({ node_id: id }) => id === nodeId)!;
    const provider = getFactoryNodeProviderV1(node.provider_id);
    if (!provider.compatible_kinds.includes(node.kind)) {
      fail("FACTORY_PROVIDER_INCOMPATIBLE", node.provider_id);
    }
    const roles = node.input_refs.map(({ role }) => role);
    if (new Set(roles).size !== roles.length ||
        JSON.stringify([...roles].sort(compareUtf8)) !==
          JSON.stringify([...provider.required_input_roles].sort(compareUtf8))) {
      fail("FACTORY_PROVIDER_INPUTS_INCOMPLETE", node.node_id);
    }
    const inputs = await Promise.all(node.input_refs.map(({ role, ref }) =>
      resolveRef(input.repositoryRoot, role, ref.path, ref.sha256)));
    const componentPaths = await resolveFactoryComponentClosure({
      repositoryRoot: input.repositoryRoot,
      rootPaths: provider.component_paths,
    });
    const components = await Promise.all(componentPaths.map((path) =>
      resolveRef(input.repositoryRoot, "component", path)));
    const tools = await Promise.all(provider.tool_ids.map(resolveFactoryToolV1));
    lockedNodes.push(Object.freeze({
      node_id: node.node_id,
      kind: node.kind,
      provider_id: provider.provider_id,
      provider_version: provider.provider_version,
      depends_on: Object.freeze([...node.depends_on]),
      inputs: Object.freeze(inputs),
      components: Object.freeze(components),
      tools: Object.freeze(tools),
      claim_ceiling: node.claim_ceiling,
    }));
  }
  const replayPolicy = Object.freeze({
    timeout_ms: 70_000,
    output_limit_bytes: 1_048_576,
    termination_grace_ms: 1_000,
    environment_keys: Object.freeze(["PATH", "TMPDIR", "HOME", "CARGO_HOME", "RUSTUP_HOME"]),
  });
  const lockBody = Object.freeze({
    schema_version: "FactoryRunLock/v1" as const,
    request_id: input.request.request_id,
    suite_id: input.request.suite_id,
    purpose: input.request.purpose,
    request_sha256: requestSha256,
    ordered_node_ids: orderedNodeIds,
    nodes: Object.freeze(lockedNodes),
    replay_policy: replayPolicy,
    claim_ceiling: input.request.claim_ceiling,
    authority_effect: "none" as const,
  });
  const lockSha256 = sha256(canonicalJson(lockBody));
  const lock = Object.freeze({ ...lockBody, lock_sha256: lockSha256 });
  return Object.freeze({
    schema_version: "FactoryRunPlan/v1",
    request: input.request,
    lock,
    run_id: `factory-${lockSha256.slice(0, 24)}`,
    authority_effect: "none",
  });
};
