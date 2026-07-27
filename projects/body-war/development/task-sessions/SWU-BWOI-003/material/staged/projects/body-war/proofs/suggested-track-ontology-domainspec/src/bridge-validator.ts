import { createHash } from "node:crypto";

export const BRIDGE_DIAGNOSTIC_CODES = [
  "BRIDGE_SCHEMA_INVALID",
  "BRIDGE_DIGEST_MISMATCH",
  "BRIDGE_PARENT_RECEIPT_INVALID",
  "BRIDGE_STALE_ONTOLOGY_RECEIPT",
  "BRIDGE_STALE_DOMAINSPEC_RECEIPT",
  "BRIDGE_UNKNOWN_ONTOLOGY_ENTRY",
  "BRIDGE_STALE_ONTOLOGY_DIGEST",
  "BRIDGE_STALE_DOMAINSPEC_DIGEST",
  "BRIDGE_UNKNOWN_DOMAINSPEC_HANDLE",
  "BRIDGE_ONTOLOGY_STATE_INSUFFICIENT",
  "BRIDGE_EXECUTABLE_LOGIC_FORBIDDEN",
  "BRIDGE_CLAIM_CEILING_VIOLATION",
] as const;

export type BridgeDiagnosticCode =
  (typeof BRIDGE_DIAGNOSTIC_CODES)[number];

export interface BridgeDiagnostic {
  readonly code: BridgeDiagnosticCode;
  readonly path: string;
  readonly message: string;
}

export interface BridgeManifest {
  readonly schema_version: "body-war-ontology-bridge/v1";
  readonly feature_id: "body-war-suggested-track";
  readonly ontology_context: {
    readonly validation_receipt_digest: string;
    readonly entries: readonly {
      readonly entry_id: string;
      readonly entry_digest: string;
      readonly observed_state: "candidate" | "promoted";
    }[];
  };
  readonly domainspec_context: {
    readonly validation_receipt_digest: string;
    readonly profile_digest: string;
    readonly graph_digest: string;
    readonly source_manifest_digest: string;
    readonly build_receipt_digest: string;
  };
  readonly bindings: readonly {
    readonly node_id: string;
    readonly node_digest: string;
    readonly module_id: string;
    readonly module_digest: string;
    readonly clause_id: string;
    readonly clause_digest: string;
    readonly interprets: readonly string[];
    readonly required_ontology_state: "candidate" | "promoted";
  }[];
  readonly authority_effect: "none";
  readonly release_admission: "not-granted";
  readonly bridge_digest: string;
}

export interface BridgeProfile {
  readonly schema_version: "body-war-ontology-bridge-profile/v1";
  readonly profile_id: string;
  readonly state_order: readonly ["candidate", "promoted"];
  readonly ontology_status_map: Readonly<Record<string, "candidate" | "promoted">>;
  readonly authority_effect: "none";
  readonly release_admission: "not-granted";
}

type JsonRecord = Record<string, unknown>;

export interface BridgeValidationInput {
  readonly manifest: BridgeManifest;
  readonly profile: BridgeProfile;
  readonly ontologyReceipt: JsonRecord;
  readonly domainspecReceipt: JsonRecord;
  readonly ontologyReceiptDigest: string;
  readonly domainspecReceiptDigest: string;
  readonly ontologyEntryDigests: Readonly<Record<string, string>>;
}

export interface BridgeValidationResult {
  readonly status: "pass" | "fail";
  readonly diagnostics: readonly BridgeDiagnostic[];
  readonly observed_state?: "candidate" | "promoted";
}

export interface BridgeAdmissionReceipt {
  readonly schema_version: "body-war-bridge-admission/v1";
  readonly status: "pass";
  readonly authority_effect: "none";
  readonly release_admission: "not-granted";
  readonly bridge_digest: string;
  readonly profile_digest: string;
  readonly parent_receipts: {
    readonly ontology: string;
    readonly domainspec: string;
  };
  readonly resolved_handles: {
    readonly ontology_entries: readonly string[];
    readonly node_id: string;
    readonly module_id: string;
    readonly clause_id: string;
  };
  readonly observed_ontology_state: "candidate" | "promoted";
  readonly required_ontology_state: "candidate" | "promoted";
  readonly domainspec_case_id: string;
  readonly diagnostics: readonly [];
  readonly receipt_digest: string;
}

const TOP_LEVEL_KEYS = new Set([
  "schema_version",
  "feature_id",
  "ontology_context",
  "domainspec_context",
  "bindings",
  "authority_effect",
  "release_admission",
  "bridge_digest",
]);

const FORBIDDEN_LOGIC_KEYS = new Set([
  "body.logic",
  "bodyLogic",
  "clauses",
  "expression",
  "predicate",
  "quantifier",
]);

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (!isRecord(value)) return value;
  return Object.fromEntries(
    Object.keys(value)
      .sort()
      .map((key) => [key, canonicalize(value[key])]),
  );
}

export function renderBridgeJson(value: unknown): string {
  return `${JSON.stringify(canonicalize(value), null, 2)}\n`;
}

export function sha256Bytes(value: string | Buffer): string {
  return createHash("sha256").update(value).digest("hex");
}

export function sha256BridgeCanonical(value: unknown): string {
  return sha256Bytes(JSON.stringify(canonicalize(value)));
}

export function withBridgeDigest(
  manifest: Omit<BridgeManifest, "bridge_digest"> | BridgeManifest,
): BridgeManifest {
  const unsigned = structuredClone(manifest) as JsonRecord;
  delete unsigned.bridge_digest;
  return {
    ...(unsigned as Omit<BridgeManifest, "bridge_digest">),
    bridge_digest: sha256BridgeCanonical(unsigned),
  };
}

function failure(
  code: BridgeDiagnosticCode,
  path: string,
  message: string,
): BridgeValidationResult {
  return { status: "fail", diagnostics: [{ code, path, message }] };
}

function findForbiddenLogicPath(
  value: unknown,
  path = "$",
): string | undefined {
  if (Array.isArray(value)) {
    for (const [index, child] of value.entries()) {
      const found = findForbiddenLogicPath(child, `${path}[${index}]`);
      if (found) return found;
    }
    return undefined;
  }
  if (!isRecord(value)) return undefined;
  for (const [key, child] of Object.entries(value)) {
    if (FORBIDDEN_LOGIC_KEYS.has(key)) return `${path}.${key}`;
    const found = findForbiddenLogicPath(child, `${path}.${key}`);
    if (found) return found;
  }
  return undefined;
}

function validateShape(manifest: unknown): BridgeValidationResult | undefined {
  if (!isRecord(manifest)) {
    return failure("BRIDGE_SCHEMA_INVALID", "$", "bridge must be an object");
  }
  const keys = Object.keys(manifest);
  if (
    keys.length !== TOP_LEVEL_KEYS.size ||
    keys.some((key) => !TOP_LEVEL_KEYS.has(key))
  ) {
    return failure(
      "BRIDGE_SCHEMA_INVALID",
      "$",
      "bridge top-level fields differ from the closed schema",
    );
  }
  if (
    manifest.schema_version !== "body-war-ontology-bridge/v1" ||
    manifest.feature_id !== "body-war-suggested-track" ||
    !isRecord(manifest.ontology_context) ||
    !isRecord(manifest.domainspec_context) ||
    !Array.isArray(manifest.bindings) ||
    manifest.bindings.length !== 1
  ) {
    return failure(
      "BRIDGE_SCHEMA_INVALID",
      "$",
      "bridge identity or required components are invalid",
    );
  }
  return undefined;
}

function receiptRecord(
  receipt: JsonRecord,
  key: string,
): JsonRecord | undefined {
  const value = receipt[key];
  return isRecord(value) ? value : undefined;
}

export function validateBridge(
  input: BridgeValidationInput,
): BridgeValidationResult {
  const forbiddenPath = findForbiddenLogicPath(input.manifest);
  if (forbiddenPath) {
    return failure(
      "BRIDGE_EXECUTABLE_LOGIC_FORBIDDEN",
      forbiddenPath,
      "bridge may reference canonical logic but cannot copy executable logic",
    );
  }
  const shapeFailure = validateShape(input.manifest);
  if (shapeFailure) return shapeFailure;

  const expectedBridge = withBridgeDigest(input.manifest);
  if (expectedBridge.bridge_digest !== input.manifest.bridge_digest) {
    return failure(
      "BRIDGE_DIGEST_MISMATCH",
      "$.bridge_digest",
      "bridge digest does not match the unsigned manifest",
    );
  }

  if (
    input.manifest.authority_effect !== "none" ||
    input.manifest.release_admission !== "not-granted" ||
    input.profile.authority_effect !== "none" ||
    input.profile.release_admission !== "not-granted"
  ) {
    return failure(
      "BRIDGE_CLAIM_CEILING_VIOLATION",
      "$",
      "bridge or profile exceeds the experimental claim ceiling",
    );
  }

  if (
    input.ontologyReceipt.status !== "pass" ||
    input.domainspecReceipt.status !== "pass" ||
    input.ontologyReceipt.authority_effect !== "none" ||
    input.domainspecReceipt.authority_effect !== "none" ||
    input.ontologyReceipt.release_admission !== "not-granted" ||
    input.domainspecReceipt.release_admission !== "not-granted"
  ) {
    return failure(
      "BRIDGE_PARENT_RECEIPT_INVALID",
      "$",
      "both parent receipts must pass inside the same claim ceiling",
    );
  }

  if (
    input.manifest.ontology_context.validation_receipt_digest !==
    input.ontologyReceiptDigest
  ) {
    return failure(
      "BRIDGE_STALE_ONTOLOGY_RECEIPT",
      "$.ontology_context.validation_receipt_digest",
      "ontology receipt digest is stale",
    );
  }
  if (
    input.manifest.domainspec_context.validation_receipt_digest !==
    input.domainspecReceiptDigest
  ) {
    return failure(
      "BRIDGE_STALE_DOMAINSPEC_RECEIPT",
      "$.domainspec_context.validation_receipt_digest",
      "DomainSpec receipt digest is stale",
    );
  }

  const ontologyDigestRows = input.ontologyReceipt.entry_digests;
  if (!Array.isArray(ontologyDigestRows)) {
    return failure(
      "BRIDGE_PARENT_RECEIPT_INVALID",
      "$.ontology_receipt.entry_digests",
      "ontology entry digest table is absent",
    );
  }
  for (const [index, entry] of input.manifest.ontology_context.entries.entries()) {
    const receiptRow = ontologyDigestRows.find(
      (candidate) =>
        isRecord(candidate) && candidate.id === entry.entry_id,
    ) as JsonRecord | undefined;
    if (!receiptRow || !(entry.entry_id in input.ontologyEntryDigests)) {
      return failure(
        "BRIDGE_UNKNOWN_ONTOLOGY_ENTRY",
        `$.ontology_context.entries[${index}]`,
        `ontology entry is unresolved: ${entry.entry_id}`,
      );
    }
    if (
      receiptRow.sha256 !== entry.entry_digest ||
      input.ontologyEntryDigests[entry.entry_id] !== entry.entry_digest
    ) {
      return failure(
        "BRIDGE_STALE_ONTOLOGY_DIGEST",
        `$.ontology_context.entries[${index}].entry_digest`,
        `ontology entry digest is stale: ${entry.entry_id}`,
      );
    }
  }

  const source = receiptRecord(input.domainspecReceipt, "source");
  const build = receiptRecord(input.domainspecReceipt, "build");
  const generatedCase = receiptRecord(input.domainspecReceipt, "generated_case");
  if (!source || !build || !generatedCase) {
    return failure(
      "BRIDGE_PARENT_RECEIPT_INVALID",
      "$.domainspec_receipt",
      "DomainSpec receipt lacks source, build, or case evidence",
    );
  }
  const contextPairs: Array<[string, unknown, string]> = [
    ["profile_digest", source.profile_digest, input.manifest.domainspec_context.profile_digest],
    ["graph_digest", build.graph_digest, input.manifest.domainspec_context.graph_digest],
    [
      "source_manifest_digest",
      build.source_manifest_digest,
      input.manifest.domainspec_context.source_manifest_digest,
    ],
    [
      "build_receipt_digest",
      build.build_receipt_digest,
      input.manifest.domainspec_context.build_receipt_digest,
    ],
  ];
  const staleContext = contextPairs.find(([, actual, declared]) => actual !== declared);
  if (staleContext) {
    return failure(
      "BRIDGE_STALE_DOMAINSPEC_DIGEST",
      `$.domainspec_context.${staleContext[0]}`,
      `DomainSpec ${staleContext[0]} is stale`,
    );
  }

  const binding = input.manifest.bindings[0];
  if (
    !binding ||
    binding.node_id !== source.node_id ||
    binding.module_id !== source.module_id ||
    binding.clause_id !== source.clause_id
  ) {
    return failure(
      "BRIDGE_UNKNOWN_DOMAINSPEC_HANDLE",
      "$.bindings[0]",
      "node, module, or clause handle differs from the canonical receipt",
    );
  }
  if (
    binding.node_digest !== source.node_digest ||
    binding.module_digest !== source.logic_digest ||
    binding.clause_digest !== source.clause_digest
  ) {
    return failure(
      "BRIDGE_STALE_DOMAINSPEC_DIGEST",
      "$.bindings[0]",
      "node, module, or clause digest is stale",
    );
  }

  const observedStatus = input.ontologyReceipt.ontology_status;
  const observedState =
    typeof observedStatus === "string"
      ? input.profile.ontology_status_map[observedStatus]
      : undefined;
  const declaredState = input.manifest.ontology_context.entries[0]?.observed_state;
  if (!observedState || observedState !== declaredState) {
    return failure(
      "BRIDGE_PARENT_RECEIPT_INVALID",
      "$.ontology_context.entries[0].observed_state",
      "observed ontology state differs from the parent receipt",
    );
  }
  const observedRank = input.profile.state_order.indexOf(observedState);
  const requiredRank = input.profile.state_order.indexOf(
    binding.required_ontology_state,
  );
  if (observedRank < requiredRank) {
    return failure(
      "BRIDGE_ONTOLOGY_STATE_INSUFFICIENT",
      "$.bindings[0].required_ontology_state",
      `${observedState} does not satisfy ${binding.required_ontology_state}`,
    );
  }

  return { status: "pass", diagnostics: [], observed_state: observedState };
}

export function buildBridgeAdmissionReceipt(input: {
  readonly validation: BridgeValidationResult;
  readonly manifest: BridgeManifest;
  readonly profile: BridgeProfile;
  readonly ontologyReceiptDigest: string;
  readonly domainspecReceiptDigest: string;
  readonly domainspecCaseId: string;
}): BridgeAdmissionReceipt {
  if (input.validation.status !== "pass" || !input.validation.observed_state) {
    throw new Error("Cannot build a passing admission receipt from failed validation.");
  }
  const binding = input.manifest.bindings[0];
  if (!binding) throw new Error("Bridge binding is absent.");
  const unsigned = {
    schema_version: "body-war-bridge-admission/v1" as const,
    status: "pass" as const,
    authority_effect: "none" as const,
    release_admission: "not-granted" as const,
    bridge_digest: input.manifest.bridge_digest,
    profile_digest: sha256BridgeCanonical(input.profile),
    parent_receipts: {
      ontology: input.ontologyReceiptDigest,
      domainspec: input.domainspecReceiptDigest,
    },
    resolved_handles: {
      ontology_entries: input.manifest.ontology_context.entries.map(
        ({ entry_id }) => entry_id,
      ),
      node_id: binding.node_id,
      module_id: binding.module_id,
      clause_id: binding.clause_id,
    },
    observed_ontology_state: input.validation.observed_state,
    required_ontology_state: binding.required_ontology_state,
    domainspec_case_id: input.domainspecCaseId,
    diagnostics: [] as const,
  };
  return {
    ...unsigned,
    receipt_digest: sha256BridgeCanonical(unsigned),
  };
}

