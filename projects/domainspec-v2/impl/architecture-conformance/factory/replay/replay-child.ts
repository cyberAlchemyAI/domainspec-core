import { lstat, readFile, realpath, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";

import type {
  FactoryNodeSemanticResultV1,
  FactoryUpstreamResultV1,
} from "../contracts/factory-node-provider-v1.js";
import {
  canonicalJson,
  exactKeys,
  fail,
  isRecord,
  safeRelativePath,
  sha256,
} from "../shared/canonical.js";
import { resolveFactoryComponentClosure } from
  "../resolution/resolve-component-closure.js";

type LockedComponentIdentityV1 = Readonly<{
  path: string;
  sha256: string;
  byte_length: number;
}>;

type ReplayPayload = Readonly<{
  schema_version: "FactoryReplayChildRequest/v1";
  node_id: string;
  provider_id: string;
  provider_version: string;
  repository_root: string;
  raw_inputs: Readonly<Record<string, string>>;
  upstream: Readonly<Record<string, FactoryUpstreamResultV1>>;
  locked_components: readonly LockedComponentIdentityV1[];
  locked_component_set_sha256: string;
  replay_mode: "same-oracle-deterministic";
  authority_effect: "none";
}>;

const compareUtf8 = (left: string, right: string): number =>
  Buffer.from(left).compare(Buffer.from(right));

const normalizeComponents = (
  refs: readonly LockedComponentIdentityV1[],
): readonly LockedComponentIdentityV1[] => Object.freeze([...refs]
  .map((ref) => Object.freeze({ ...ref }))
  .sort((left, right) => compareUtf8(left.path, right.path)));

const componentSetSha256 = (refs: readonly LockedComponentIdentityV1[]): string =>
  sha256(canonicalJson(normalizeComponents(refs)));

const decodePayload = (value: unknown): ReplayPayload => {
  if (!isRecord(value)) return fail("FACTORY_REPLAY_PAYLOAD_INVALID");
  exactKeys(value, [
    "schema_version",
    "node_id",
    "provider_id",
    "provider_version",
    "repository_root",
    "raw_inputs",
    "upstream",
    "locked_components",
    "locked_component_set_sha256",
    "replay_mode",
    "authority_effect",
  ], "FACTORY_REPLAY_PAYLOAD_INVALID");
  if (value.schema_version !== "FactoryReplayChildRequest/v1" ||
      typeof value.node_id !== "string" || value.node_id.length === 0 ||
      typeof value.provider_id !== "string" || value.provider_id.length === 0 ||
      typeof value.provider_version !== "string" || value.provider_version.length === 0 ||
      typeof value.repository_root !== "string" || value.repository_root.length === 0 ||
      !isRecord(value.raw_inputs) || !isRecord(value.upstream) ||
      !Array.isArray(value.locked_components) ||
      typeof value.locked_component_set_sha256 !== "string" ||
      value.replay_mode !== "same-oracle-deterministic" ||
      value.authority_effect !== "none") {
    return fail("FACTORY_REPLAY_PAYLOAD_INVALID");
  }
  const components = value.locked_components.map((candidate) => {
    if (!isRecord(candidate)) {
      return fail("FACTORY_REPLAY_PAYLOAD_INVALID", "component");
    }
    exactKeys(candidate, ["path", "sha256", "byte_length"],
      "FACTORY_REPLAY_PAYLOAD_INVALID");
    if (typeof candidate.path !== "string" || !safeRelativePath(candidate.path) ||
        typeof candidate.sha256 !== "string" ||
        !/^[a-f0-9]{64}$/u.test(candidate.sha256) ||
        !Number.isInteger(candidate.byte_length) ||
        (candidate.byte_length as number) < 0) {
      return fail("FACTORY_REPLAY_PAYLOAD_INVALID", "component");
    }
    return Object.freeze({
      path: candidate.path,
      sha256: candidate.sha256,
      byte_length: candidate.byte_length as number,
    });
  });
  const paths = components.map(({ path }) => path);
  if (new Set(paths).size !== paths.length ||
      componentSetSha256(components) !== value.locked_component_set_sha256) {
    return fail("FACTORY_REPLAY_PAYLOAD_INVALID", "component-set");
  }
  if (Object.values(value.raw_inputs).some((raw) => typeof raw !== "string")) {
    return fail("FACTORY_REPLAY_PAYLOAD_INVALID", "raw-inputs");
  }
  return Object.freeze({
    schema_version: "FactoryReplayChildRequest/v1",
    node_id: value.node_id,
    provider_id: value.provider_id,
    provider_version: value.provider_version,
    repository_root: value.repository_root,
    raw_inputs: Object.freeze(value.raw_inputs as Record<string, string>),
    upstream: Object.freeze(value.upstream as Record<string, FactoryUpstreamResultV1>),
    locked_components: normalizeComponents(components),
    locked_component_set_sha256: value.locked_component_set_sha256,
    replay_mode: "same-oracle-deterministic",
    authority_effect: "none",
  });
};

const verifyComponents = async (
  rootInput: string,
  refs: readonly LockedComponentIdentityV1[],
): Promise<string> => {
  const root = await realpath(rootInput);
  await Promise.all(refs.map(async (ref) => {
    const target = resolve(root, ref.path);
    if (!target.startsWith(`${root}/`)) fail("FACTORY_REPLAY_COMPONENT_INVALID", ref.path);
    const stat = await lstat(target).catch(() =>
      fail("FACTORY_REPLAY_COMPONENT_MISSING", ref.path));
    if (!stat.isFile() || stat.isSymbolicLink()) {
      fail("FACTORY_REPLAY_COMPONENT_INVALID", ref.path);
    }
    const owned = await realpath(target);
    if (!owned.startsWith(`${root}/`)) fail("FACTORY_REPLAY_COMPONENT_INVALID", ref.path);
    const bytes = await readFile(owned);
    if (bytes.byteLength !== ref.byte_length || sha256(bytes) !== ref.sha256) {
      fail("FACTORY_REPLAY_COMPONENT_TAMPERED", ref.path);
    }
  }));
  return componentSetSha256(refs);
};

const payloadPath = process.argv[2];
if (payloadPath === undefined) fail("FACTORY_REPLAY_PAYLOAD_MISSING");

const payload = decodePayload(JSON.parse(await readFile(payloadPath, "utf8")));
const preLoadSha256 = await verifyComponents(
  payload.repository_root,
  payload.locked_components,
);
const moduleRuntime = await import("node:module") as unknown as {
  enableCompileCache?: () => unknown;
};
moduleRuntime.enableCompileCache?.();
const { getFactoryNodeProviderV1 } = await import(
  "../registry/factory-node-registry-v1.js"
);
const provider = getFactoryNodeProviderV1(payload.provider_id);
const providerPaths = await resolveFactoryComponentClosure({
  repositoryRoot: payload.repository_root,
  rootPaths: provider.component_paths,
});
const lockedPaths = payload.locked_components.map(({ path }) => path).sort(compareUtf8);
if (provider.provider_id !== payload.provider_id ||
    provider.provider_version !== payload.provider_version ||
    JSON.stringify(providerPaths) !== JSON.stringify(lockedPaths)) {
  fail("FACTORY_REPLAY_PROVIDER_IDENTITY_MISMATCH", payload.provider_id);
}
const result = await provider.execute({
  raw_inputs: payload.raw_inputs,
  upstream: payload.upstream,
});
const postExecuteSha256 = await verifyComponents(
  payload.repository_root,
  payload.locked_components,
);
const semanticResult = result as FactoryNodeSemanticResultV1;
const envelope = Object.freeze({
  schema_version: "FactoryReplayChildResult/v1",
  result: "pass",
  replay_mode: "same-oracle-deterministic",
  node_id: payload.node_id,
  provider_id: payload.provider_id,
  provider_version: payload.provider_version,
  component_identity: Object.freeze({
    algorithm: "sha256",
    locked_set_sha256: payload.locked_component_set_sha256,
    pre_load_sha256: preLoadSha256,
    post_execute_sha256: postExecuteSha256,
  }),
  semantic_result: semanticResult,
  semantic_result_sha256: sha256(canonicalJson(semanticResult)),
  authority_effect: "none",
});
await writeFile(resolve(dirname(payloadPath), "result.json"),
  `${JSON.stringify(envelope)}\n`, { encoding: "utf8", flag: "wx" });
