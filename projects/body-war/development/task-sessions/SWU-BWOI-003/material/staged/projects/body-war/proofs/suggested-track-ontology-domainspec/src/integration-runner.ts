import { createHash } from "node:crypto";
import {
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";

import {
  buildBridgeAdmissionReceipt,
  renderBridgeJson,
  sha256BridgeCanonical,
  sha256Bytes,
  validateBridge,
  withBridgeDigest,
  type BridgeDiagnosticCode,
  type BridgeManifest,
  type BridgeProfile,
  type BridgeValidationInput,
} from "./bridge-validator.js";

type JsonRecord = Record<string, unknown>;

export interface IntegrationReceipt {
  readonly schema_version: "body-war-ontology-domainspec-integration/v1";
  readonly test_id: "T-INTEGRATION-001";
  readonly status: "pass";
  readonly authority_effect: "none";
  readonly release_admission: "not-granted";
  readonly parent_receipts: {
    readonly ontology: { readonly path: string; readonly sha256: string };
    readonly domainspec: { readonly path: string; readonly sha256: string };
  };
  readonly bridge: {
    readonly manifest_digest: string;
    readonly profile_digest: string;
    readonly admission_receipt_digest: string;
    readonly admission_receipt_sha256: string;
  };
  readonly domainspec_case: {
    readonly case_id: string;
    readonly case_digest: string;
    readonly expected_digest: string;
    readonly proof_receipt_digest: string;
    readonly backend_target_digest: string;
    readonly reused_exact_case: true;
  };
  readonly negative_controls: readonly {
    readonly mutation:
      | "stale-ontology-digest"
      | "promoted-required-candidate-observed"
      | "executable-bridge-duplication";
    readonly result: "rejected";
    readonly diagnostic: BridgeDiagnosticCode;
  }[];
  readonly receipt_digest: string;
}

export interface IntegrationRun {
  readonly receipt: IntegrationReceipt;
  readonly receipt_bytes: string;
  readonly bridge_receipt_bytes: string;
}

const sourceDir = dirname(fileURLToPath(import.meta.url));
const defaultProofRoot = resolve(sourceDir, "..");
const proofRoot = resolve(
  process.env.BWOI_PROOF_ROOT ?? defaultProofRoot,
);
const bridgeRoot = resolve(
  process.env.BWOI_BRIDGE_ROOT ?? join(proofRoot, "bridge"),
);
const outputRoot = resolve(
  process.env.BWOI_OUTPUT_ROOT ?? proofRoot,
);
const ontologyReceiptPath = join(proofRoot, "receipts/ontology-receipt.json");
const domainspecReceiptPath = join(proofRoot, "receipts/domainspec-receipt.json");
const integrationReceiptPath = join(
  outputRoot,
  "receipts/integration-receipt.json",
);
const bridgeReceiptPath = join(
  outputRoot,
  "bridge/receipts/bridge-admission-receipt.json",
);

function json<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function writeExact(path: string, bytes: string): void {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, bytes);
}

function fileDigest(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function assertCondition(
  condition: unknown,
  message: string,
): asserts condition {
  if (!condition) throw new Error(message);
}

async function ontologyEntryDigests(): Promise<Record<string, string>> {
  const modulePath = pathToFileURL(
    join(proofRoot, "src/ontology-validator.ts"),
  ).href;
  const imported = (await import(modulePath)) as {
    default?: { sha256Canonical(value: unknown): string };
    sha256Canonical(value: unknown): string;
  };
  const sha256Canonical =
    imported.sha256Canonical ?? imported.default?.sha256Canonical;
  assertCondition(
    typeof sha256Canonical === "function",
    "ontology canonical digest function is unavailable",
  );
  const entriesRoot = join(proofRoot, "ontology/entries");
  return Object.fromEntries(
    readdirSync(entriesRoot)
      .filter((name) => name.endsWith(".json"))
      .sort()
      .map((name) => {
        const entry = json<{ id: string }>(join(entriesRoot, name));
        return [entry.id, sha256Canonical(entry)];
      }),
  );
}

async function bridgeRuntimeInput(
  manifest: BridgeManifest,
): Promise<BridgeValidationInput> {
  const ontologyReceiptBytes = readFileSync(ontologyReceiptPath);
  const domainspecReceiptBytes = readFileSync(domainspecReceiptPath);
  return {
    manifest,
    profile: json<BridgeProfile>(join(bridgeRoot, "profile.json")),
    ontologyReceipt: JSON.parse(
      ontologyReceiptBytes.toString("utf8"),
    ) as JsonRecord,
    domainspecReceipt: JSON.parse(
      domainspecReceiptBytes.toString("utf8"),
    ) as JsonRecord,
    ontologyReceiptDigest: sha256Bytes(ontologyReceiptBytes),
    domainspecReceiptDigest: sha256Bytes(domainspecReceiptBytes),
    ontologyEntryDigests: await ontologyEntryDigests(),
  };
}

function firstDiagnostic(
  input: BridgeValidationInput,
): BridgeDiagnosticCode {
  const result = validateBridge(input);
  assertCondition(result.status === "fail", "negative bridge unexpectedly passed");
  const diagnostic = result.diagnostics[0];
  assertCondition(diagnostic !== undefined, "negative bridge has no diagnostic");
  return diagnostic.code;
}

export async function runBridgeNegativeControls(): Promise<
  IntegrationReceipt["negative_controls"]
> {
  const canonical = json<BridgeManifest>(join(bridgeRoot, "bridge.json"));
  const staleFixture = json<{
    entry_index: number;
    replacement_digest: string;
  }>(join(bridgeRoot, "fixtures/stale-ontology-digest.json"));
  const stateFixture = json<{
    binding_index: number;
    required_ontology_state: "promoted";
  }>(join(bridgeRoot, "fixtures/promoted-required.json"));
  const executableFixture = json<{
    binding_index: number;
    field: string;
    value: unknown;
  }>(join(bridgeRoot, "fixtures/executable-duplication.json"));

  const stale = structuredClone(canonical);
  const staleEntry = stale.ontology_context.entries[staleFixture.entry_index];
  assertCondition(staleEntry !== undefined, "stale fixture entry is absent");
  (staleEntry as { entry_digest: string }).entry_digest =
    staleFixture.replacement_digest;
  const staleManifest = withBridgeDigest(stale);

  const state = structuredClone(canonical);
  const stateBinding = state.bindings[stateFixture.binding_index];
  assertCondition(stateBinding !== undefined, "state fixture binding is absent");
  (stateBinding as { required_ontology_state: "candidate" | "promoted" })
    .required_ontology_state = stateFixture.required_ontology_state;
  const stateManifest = withBridgeDigest(state);

  const executable = structuredClone(canonical) as unknown as JsonRecord;
  const bindings = executable.bindings as JsonRecord[];
  const executableBinding = bindings[executableFixture.binding_index];
  assertCondition(
    executableBinding !== undefined,
    "executable fixture binding is absent",
  );
  executableBinding[executableFixture.field] = executableFixture.value;
  const executableManifest = withBridgeDigest(
    executable as unknown as BridgeManifest,
  );

  const staleCode = firstDiagnostic(
    await bridgeRuntimeInput(staleManifest),
  );
  const stateCode = firstDiagnostic(
    await bridgeRuntimeInput(stateManifest),
  );
  const executableCode = firstDiagnostic(
    await bridgeRuntimeInput(executableManifest),
  );
  assertCondition(
    staleCode === "BRIDGE_STALE_ONTOLOGY_DIGEST",
    `unexpected stale digest diagnostic: ${staleCode}`,
  );
  assertCondition(
    stateCode === "BRIDGE_ONTOLOGY_STATE_INSUFFICIENT",
    `unexpected ontology state diagnostic: ${stateCode}`,
  );
  assertCondition(
    executableCode === "BRIDGE_EXECUTABLE_LOGIC_FORBIDDEN",
    `unexpected executable bridge diagnostic: ${executableCode}`,
  );
  return [
    {
      mutation: "stale-ontology-digest",
      result: "rejected",
      diagnostic: staleCode,
    },
    {
      mutation: "promoted-required-candidate-observed",
      result: "rejected",
      diagnostic: stateCode,
    },
    {
      mutation: "executable-bridge-duplication",
      result: "rejected",
      diagnostic: executableCode,
    },
  ];
}

export async function runIntegrationProof(): Promise<IntegrationRun> {
  const manifest = json<BridgeManifest>(join(bridgeRoot, "bridge.json"));
  const runtimeInput = await bridgeRuntimeInput(manifest);
  const bridgeValidation = validateBridge(runtimeInput);
  assertCondition(
    bridgeValidation.status === "pass",
    `bridge admission failed: ${JSON.stringify(bridgeValidation.diagnostics)}`,
  );

  const generatedCase = runtimeInput.domainspecReceipt.generated_case;
  assertCondition(
    typeof generatedCase === "object" && generatedCase !== null,
    "DomainSpec generated case is absent",
  );
  const caseRecord = generatedCase as JsonRecord;
  const caseId = caseRecord.case_id;
  assertCondition(typeof caseId === "string", "DomainSpec case id is absent");

  const bridgeReceipt = buildBridgeAdmissionReceipt({
    validation: bridgeValidation,
    manifest,
    profile: runtimeInput.profile,
    ontologyReceiptDigest: runtimeInput.ontologyReceiptDigest,
    domainspecReceiptDigest: runtimeInput.domainspecReceiptDigest,
    domainspecCaseId: caseId,
  });
  const bridgeReceiptBytes = renderBridgeJson(bridgeReceipt);

  const parentBytesBefore = readFileSync(domainspecReceiptPath, "utf8");
  const runnerPath = pathToFileURL(
    join(proofRoot, "src/domainspec-ct2-runner.ts"),
  ).href;
  const importedRunner = (await import(runnerPath)) as {
    default?: {
      runDomainspecCt2Proof(): Promise<{
        receipt: JsonRecord;
        receipt_bytes: string;
      }>;
    };
    runDomainspecCt2Proof(): Promise<{
      receipt: JsonRecord;
      receipt_bytes: string;
    }>;
  };
  const runDomainspecCt2Proof =
    importedRunner.runDomainspecCt2Proof ??
    importedRunner.default?.runDomainspecCt2Proof;
  assertCondition(
    typeof runDomainspecCt2Proof === "function",
    "DomainSpec CT-2 runner is unavailable",
  );
  const rerun = await runDomainspecCt2Proof();
  assertCondition(
    rerun.receipt_bytes === parentBytesBefore,
    "reused DomainSpec case changed the standalone receipt bytes",
  );
  assertCondition(
    readFileSync(domainspecReceiptPath, "utf8") === parentBytesBefore,
    "reused DomainSpec runner changed the checked-in standalone receipt",
  );
  const rerunCase = rerun.receipt.generated_case as JsonRecord;
  assertCondition(
    rerunCase.case_id === caseId,
    "integration reran a different DomainSpec case",
  );

  const negativeControls = await runBridgeNegativeControls();
  const source = runtimeInput.domainspecReceipt.source as JsonRecord;
  const proof = runtimeInput.domainspecReceipt.proof as JsonRecord;
  const adapter = runtimeInput.domainspecReceipt.backend_adapter as JsonRecord;
  const unsigned = {
    schema_version: "body-war-ontology-domainspec-integration/v1" as const,
    test_id: "T-INTEGRATION-001" as const,
    status: "pass" as const,
    authority_effect: "none" as const,
    release_admission: "not-granted" as const,
    parent_receipts: {
      ontology: {
        path: "projects/body-war/proofs/suggested-track-ontology-domainspec/receipts/ontology-receipt.json",
        sha256: runtimeInput.ontologyReceiptDigest,
      },
      domainspec: {
        path: "projects/body-war/proofs/suggested-track-ontology-domainspec/receipts/domainspec-receipt.json",
        sha256: runtimeInput.domainspecReceiptDigest,
      },
    },
    bridge: {
      manifest_digest: manifest.bridge_digest,
      profile_digest: sha256BridgeCanonical(runtimeInput.profile),
      admission_receipt_digest: bridgeReceipt.receipt_digest,
      admission_receipt_sha256: sha256Bytes(bridgeReceiptBytes),
    },
    domainspec_case: {
      case_id: caseId,
      case_digest: String(caseRecord.case_digest),
      expected_digest: String(caseRecord.expected_digest),
      proof_receipt_digest: String(proof.receipt_digest),
      backend_target_digest: String(adapter.target_digest),
      reused_exact_case: true as const,
    },
    canonical_handles: {
      node_id: String(source.node_id),
      module_id: String(source.module_id),
      clause_id: String(source.clause_id),
    },
    negative_controls: negativeControls,
  };
  const receipt: IntegrationReceipt = {
    ...unsigned,
    receipt_digest: sha256BridgeCanonical(unsigned),
  };
  const receiptBytes = renderBridgeJson(receipt);
  writeExact(bridgeReceiptPath, bridgeReceiptBytes);
  writeExact(integrationReceiptPath, receiptBytes);
  return { receipt, receipt_bytes: receiptBytes, bridge_receipt_bytes: bridgeReceiptBytes };
}
