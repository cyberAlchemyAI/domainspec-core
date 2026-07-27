import { createHash } from "node:crypto";
import {
  mkdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { createMemoryBodyWarAuthRepository } from "../../../app/src/auth/memory-repository.js";
import type { CreateSuggestedTrackInput } from "../../../app/src/auth/body-war-repository.js";
import type { SuggestedTrack } from "../../../app/src/auth/types.js";
import {
  buildMintedProjectViews,
  verifyMintedProjectBuild,
} from "../../../../domainspec-v2/impl/tools/minted-project/views.js";
import {
  NODE_PROJECTION_ADMISSION_VERSION,
  NODE_PROOF_CONTEXT_VERSION,
  projectNodeLogic,
} from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/node-source/index.js";
import { decodeNodeLogicModule } from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/language/decoder.js";
import { typecheckLogicModule } from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/language/typecheck.js";
import {
  bindingSelectorForCase,
  derivePureCases,
  digestSfolValue,
  fixtureDigest,
  toPureInvocation,
  type DerivedPureCase,
  type PureFixture,
} from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/cases/index.js";
import { buildClauseDenominator } from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/denominator/index.js";
import {
  decodeLogicBindingRegistry,
  resolvePureBinding,
  SFOL_BINDING_SCHEMA_VERSION,
} from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/bindings/index.js";
import {
  runPureCase,
  type PureTargetHandle,
  type PureTargetResolver,
} from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/runners/pure/index.js";
import {
  buildPureProofReceipt,
  evaluatePureObservation,
} from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/proof/index.js";
import {
  integerValue,
  type SemanticValue,
} from "../../../../domainspec-v2/impl/test-derivation-engine/src/sfol/evaluator/index.js";

const PROFILE_DIGEST =
  "17384f4161df05461ac193ab6df369a20f189233a3f27fb111b437845b468918";
const ENVELOPE_SCHEMA_DIGEST =
  "f50d9978193bfaeca0b8005750e7f08686210d809bb8823af117c6248f49a5ea";
const NODE_ID = "body-war.CreateSuggestedTrack";
const MODULE_ID = "body-war.CreateSuggestedTrack.logic";
const CLAUSE_ID = "body-war.CT-2";
const RESULT_DECLARATION_ID = "body-war.CreateSuggestedTrackResult";
const TARGET_MODULE = "@body-war/memory-proof-adapter";
const TARGET_SYMBOL = "createSuggestedTrackNormalized";

const thisFile = fileURLToPath(import.meta.url);
const thisDir = dirname(thisFile);
const proofRoot = resolve(thisDir, "..");
const projectRoot = resolve(proofRoot, "domainspec");
const generatedRoot = resolve(projectRoot, "generated");
const receiptPath = resolve(proofRoot, "receipts/domainspec-receipt.json");
const implRoot = resolve(proofRoot, "../../../domainspec-v2/impl");
const profilePath = resolve(
  implRoot,
  "spec/sfol-profile/minted-project-profile.json",
);
const envelopeSchemaPath = resolve(
  implRoot,
  "spec/sfol-profile/node-logic-envelope.schema.json",
);
const fixturePath = resolve(projectRoot, "fixtures/ct2-input.json");
const adapterFiles = {
  memory_repository: resolve(
    proofRoot,
    "../../../body-war/app/src/auth/memory-repository.ts",
  ),
  repository_contract: resolve(
    proofRoot,
    "../../../body-war/app/src/auth/body-war-repository.ts",
  ),
  domain_types: resolve(
    proofRoot,
    "../../../body-war/app/src/auth/types.ts",
  ),
  consumer_adapter: thisFile,
} as const;

type JsonObject = Record<string, unknown>;

interface RawFixture {
  readonly schema_version: "body-war-ct2-input/v1";
  readonly fixture_id: string;
  readonly inputs: {
    readonly principalId: string;
    readonly name: string;
    readonly placeLabel: string;
    readonly city: string;
    readonly country: string;
    readonly distanceHintMeters: number;
    readonly publicNote: string;
  };
}

export interface DomainspecCt2Receipt {
  readonly schema_version: "body-war-domainspec-ct2-proof/v1";
  readonly status: "pass";
  readonly authority_effect: "none";
  readonly release_admission: "not-granted";
  readonly source: {
    readonly node_id: typeof NODE_ID;
    readonly module_id: typeof MODULE_ID;
    readonly clause_id: typeof CLAUSE_ID;
    readonly profile_digest: string;
    readonly envelope_schema_digest: string;
    readonly node_digest: string;
    readonly logic_digest: string;
    readonly clause_digest: string;
  };
  readonly build: {
    readonly deterministic: true;
    readonly verified: true;
    readonly graph_digest: string;
    readonly source_manifest_digest: string;
    readonly build_receipt_digest: string;
    readonly source_set_digest: string;
    readonly projection_digest: string;
  };
  readonly generated_case: {
    readonly case_id: string;
    readonly case_digest: string;
    readonly fixture_digest: string;
    readonly expected_digest: string;
  };
  readonly backend_adapter: {
    readonly target_digest: string;
    readonly runtime_digest: string;
    readonly source_digests: Readonly<Record<string, string>>;
    readonly normalized_fields: readonly [
      "status",
      "geometryAuthority",
      "sourceBacked",
      "pilotReady",
    ];
  };
  readonly proof: {
    readonly receipt_digest: string;
    readonly case_count: number;
    readonly stage_sets: readonly {
      readonly stage: string;
      readonly case_ids: readonly string[];
    }[];
  };
  readonly mutation_control: {
    readonly mutation: "stronger-backend-claims";
    readonly evaluation_status: "fail";
    readonly proof_status: "rejected";
    readonly diagnostic_code: string;
  };
  readonly receipt_digest: string;
}

export interface DomainspecCt2Run {
  readonly receipt: DomainspecCt2Receipt;
  readonly receipt_bytes: string;
}

function sha256(value: string | Buffer): string {
  return createHash("sha256").update(value).digest("hex");
}

function sha256File(path: string): string {
  return sha256(readFileSync(path));
}

function json<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function bytes(value: unknown): string {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function writeJson(path: string, value: unknown): void {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, bytes(value));
}

function assertCondition(
  condition: unknown,
  message: string,
): asserts condition {
  if (!condition) {
    throw new Error(message);
  }
}

function assertNoOracleFields(value: unknown, path = "$"): void {
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoOracleFields(item, `${path}[${index}]`));
    return;
  }
  if (typeof value !== "object" || value === null) {
    return;
  }
  for (const [key, child] of Object.entries(value)) {
    assertCondition(
      !/^(?:expected|oracle|acceptance|predicate|assert|verdict)(?:_|$)/i.test(
        key,
      ),
      `fixture oracle field is forbidden at ${path}.${key}`,
    );
    assertNoOracleFields(child, `${path}.${key}`);
  }
}

function stringValue(value: string): SemanticValue {
  return Object.freeze({ tag: "string", value });
}

function fixtureFromRaw(
  raw: RawFixture,
  coverageKey: string,
): PureFixture {
  assertCondition(
    raw.schema_version === "body-war-ct2-input/v1",
    "unsupported CT-2 input fixture version",
  );
  assertNoOracleFields(raw);
  assertCondition(
    Number.isSafeInteger(raw.inputs.distanceHintMeters),
    "distanceHintMeters must be a safe integer",
  );
  const unsigned = {
    fixture_id: raw.fixture_id,
    coverage_key: coverageKey,
    inputs: {
      principalId: stringValue(raw.inputs.principalId),
      name: stringValue(raw.inputs.name),
      placeLabel: stringValue(raw.inputs.placeLabel),
      city: stringValue(raw.inputs.city),
      country: stringValue(raw.inputs.country),
      distanceHintMeters: integerValue(
        raw.inputs.distanceHintMeters.toString(),
      ),
      publicNote: stringValue(raw.inputs.publicNote),
    },
    universes: {},
  };
  return Object.freeze({
    ...unsigned,
    fixture_digest: fixtureDigest(unsigned),
  });
}

function requireString(value: SemanticValue | undefined, name: string): string {
  assertCondition(value?.tag === "string", `${name} must be a semantic string`);
  return value.value;
}

function requireInteger(
  value: SemanticValue | undefined,
  name: string,
): number {
  assertCondition(
    value?.tag === "integer",
    `${name} must be a semantic integer`,
  );
  const converted = Number(BigInt(value.value));
  assertCondition(Number.isSafeInteger(converted), `${name} exceeds safe range`);
  return converted;
}

function normalizedResult(track: SuggestedTrack): SemanticValue {
  const sourceBacked =
    track.status === "source_backed" ||
    track.geometryAuthority === "source_backed";
  const pilotReady =
    (track as unknown as Readonly<Record<string, unknown>>).pilotReady === true;
  return Object.freeze({
    tag: "record",
    declaration_id: RESULT_DECLARATION_ID,
    fields: Object.freeze({
      status: stringValue(track.status),
      geometryAuthority: stringValue(track.geometryAuthority),
      sourceBacked: Object.freeze({
        tag: "boolean" as const,
        value: sourceBacked,
      }),
      pilotReady: Object.freeze({
        tag: "boolean" as const,
        value: pilotReady,
      }),
    }),
  });
}

async function observeMemoryRepository(
  arguments_: readonly SemanticValue[],
  inputNames: readonly string[],
): Promise<SemanticValue> {
  assertCondition(arguments_.length === 7, "CT-2 adapter requires seven inputs");
  assertCondition(
    arguments_.length === inputNames.length,
    "CT-2 adapter argument names are incomplete",
  );
  const inputByName = Object.fromEntries(
    inputNames.map((name, index) => [name, arguments_[index]]),
  );
  const input: CreateSuggestedTrackInput = {
    principalId: requireString(inputByName.principalId, "principalId"),
    name: requireString(inputByName.name, "name"),
    placeLabel: requireString(inputByName.placeLabel, "placeLabel"),
    city: requireString(inputByName.city, "city"),
    country: requireString(inputByName.country, "country"),
    distanceHintMeters: requireInteger(
      inputByName.distanceHintMeters,
      "distanceHintMeters",
    ),
    publicNote: requireString(inputByName.publicNote, "publicNote"),
  };
  const repository = createMemoryBodyWarAuthRepository();
  const created = await repository.createSuggestedTrack(input);
  return normalizedResult(created);
}

function strongerMutation(): SemanticValue {
  return Object.freeze({
    tag: "record",
    declaration_id: RESULT_DECLARATION_ID,
    fields: Object.freeze({
      status: stringValue("source_backed"),
      geometryAuthority: stringValue("source_backed"),
      sourceBacked: Object.freeze({ tag: "boolean" as const, value: true }),
      pilotReady: Object.freeze({ tag: "boolean" as const, value: true }),
    }),
  });
}

function targetResolver(
  handle: PureTargetHandle,
): PureTargetResolver {
  return {
    resolve(module, symbol) {
      return module === TARGET_MODULE && symbol === TARGET_SYMBOL
        ? handle
        : null;
    },
  };
}

function orderedArguments(
  derived: DerivedPureCase,
  inputNames: readonly string[],
): SemanticValue[] {
  return inputNames.map((name) => {
    const value = derived.inputs[name];
    assertCondition(value !== undefined, `derived input ${name} is absent`);
    return value;
  });
}

function preparedHandle(
  prepared: SemanticValue,
  expectedArguments: readonly SemanticValue[],
  targetDigest: string,
  runtimeDigest: string,
): PureTargetHandle {
  const expectedArgumentDigest = digestSfolValue(expectedArguments);
  return {
    target_digest: targetDigest,
    runtime_digest: runtimeDigest,
    invoke: (...arguments_: SemanticValue[]) => {
      assertCondition(
        digestSfolValue(arguments_) === expectedArgumentDigest,
        "generic runner arguments differ from the prepared backend call",
      );
      return prepared;
    },
  };
}

export async function runDomainspecCt2Proof(): Promise<DomainspecCt2Run> {
  assertCondition(
    sha256File(profilePath) === PROFILE_DIGEST,
    "DomainSpec development profile digest drifted",
  );
  assertCondition(
    sha256File(envelopeSchemaPath) === ENVELOPE_SCHEMA_DIGEST,
    "DomainSpec node logic envelope schema digest drifted",
  );

  const compileOptions = {
    developmentProfileRegistry: {
      path: profilePath,
      handle: "sfol-development-explicit-v0.1",
    },
  } as const;
  const first = buildMintedProjectViews(projectRoot, compileOptions);
  const second = buildMintedProjectViews(projectRoot, compileOptions);
  assertCondition(first.graphBytes === second.graphBytes, "graph bytes drifted");
  assertCondition(
    first.sourceManifestBytes === second.sourceManifestBytes,
    "source manifest bytes drifted",
  );
  assertCondition(
    first.buildReceiptBytes === second.buildReceiptBytes,
    "build receipt bytes drifted",
  );
  assertCondition(
    verifyMintedProjectBuild(projectRoot, first).status === "pass" &&
      verifyMintedProjectBuild(projectRoot, second).status === "pass",
    "compiled project verification failed",
  );

  const projected = projectNodeLogic(
    {
      schema_version: NODE_PROOF_CONTEXT_VERSION,
      route: "canonical-minted-project-build",
      graph_bytes: first.graphBytes,
      source_manifest_bytes: first.sourceManifestBytes,
      build_receipt_bytes: first.buildReceiptBytes,
    },
    {
      schema_version: NODE_PROJECTION_ADMISSION_VERSION,
      profile_id: "sfol-development",
      profile_version: "0.1",
      logic_schema_versions: ["domainspec-node-logic/v1"],
      admitted_node_ids: [NODE_ID],
    },
  );
  assertCondition(
    projected.ok,
    `canonical node projection failed: ${JSON.stringify(
      projected.ok ? [] : projected.diagnostics,
    )}`,
  );
  assertCondition(
    projected.value.length === 1,
    "projection must contain exactly one logic node",
  );
  const envelope = projected.value[0];
  assertCondition(envelope !== undefined, "CT-2 projection is absent");
  assertCondition(envelope.node.node_id === NODE_ID, "projected the wrong node");
  assertCondition(envelope.module_id === MODULE_ID, "projected the wrong module");

  const decoded = decodeNodeLogicModule(envelope.logic);
  assertCondition(
    decoded.ok,
    `CT-2 module decode failed: ${JSON.stringify(
      decoded.ok ? [] : decoded.diagnostics,
    )}`,
  );
  const typed = typecheckLogicModule(decoded.value);
  assertCondition(
    typed.ok,
    `CT-2 module typecheck failed: ${JSON.stringify(
      typed.ok ? [] : typed.diagnostics,
    )}`,
  );
  const clause = typed.value.source.clauses.find(
    (candidate) => candidate.clause_id === CLAUSE_ID,
  );
  assertCondition(clause !== undefined, "admitted CT-2 clause is absent");
  assertCondition(clause.kind === "function", "CT-2 must be a function clause");
  assertCondition(clause.status === "admitted", "CT-2 must be admitted");

  const moduleDigest = digestSfolValue(typed.value.source);
  const clauseDigest = digestSfolValue(clause);
  assertCondition(
    moduleDigest === envelope.logic_digest,
    "decoded module digest differs from canonical projection",
  );
  const proofContext = {
    graph_id: "body-war-ct2.graph",
    graph_digest: envelope.proof_context.graph_digest,
    manifest_id: "body-war-ct2.manifest",
    manifest_digest: envelope.proof_context.manifest_digest,
    build_id: "body-war-ct2.build",
    build_digest: envelope.proof_context.build_receipt_digest,
    source_set_digest: envelope.proof_context.source_set_digest,
    profile_id: envelope.proof_context.profile_id,
    profile_version: envelope.proof_context.profile_version,
    profile_digest: envelope.proof_context.profile_digest,
  };
  const denominator = buildClauseDenominator({
    schema_version: "domainspec-sfol-clause-admission-manifest/v1",
    source_form: "canonical-node-graph-manifest-build",
    unsupported_residue_policy: "reject",
    proof_context: proofContext,
    clause_membership: [CLAUSE_ID],
    clauses: [
      {
        clause_id: CLAUSE_ID,
        clause_digest: clauseDigest,
        node_id: NODE_ID,
        node_digest: envelope.node.node_digest,
        module_id: MODULE_ID,
        module_digest: moduleDigest,
        kind: "function",
        required_roles: ["return"],
        status: "admitted",
        proof_context: {
          graph_digest: proofContext.graph_digest,
          manifest_digest: proofContext.manifest_digest,
          build_digest: proofContext.build_digest,
          source_set_digest: proofContext.source_set_digest,
          profile_id: proofContext.profile_id,
          profile_version: proofContext.profile_version,
          profile_digest: proofContext.profile_digest,
        },
      },
    ],
  });
  const coverageKey = denominator.coverage_keys[0];
  assertCondition(coverageKey !== undefined, "CT-2 denominator is empty");
  const rawFixture = json<RawFixture>(fixturePath);
  const fixture = fixtureFromRaw(rawFixture, coverageKey);
  const cases = derivePureCases({
    typed: typed.value,
    typed_module_digest: moduleDigest,
    typed_clause_digests: { [CLAUSE_ID]: clauseDigest },
    denominator,
    fixtures: [fixture],
  });
  assertCondition(
    cases.ok,
    `CT-2 case derivation failed: ${JSON.stringify(
      cases.ok ? [] : cases.diagnostics,
    )}`,
  );
  assertCondition(cases.value.length === 1, "expected exactly one CT-2 case");
  const derived = cases.value[0];
  assertCondition(derived !== undefined, "derived CT-2 case is absent");

  const adapterSourceDigests = Object.fromEntries(
    Object.entries(adapterFiles).map(([name, path]) => [name, sha256File(path)]),
  );
  const targetDigest = adapterSourceDigests.consumer_adapter;
  assertCondition(targetDigest !== undefined, "consumer adapter digest is absent");
  const runtimeDigest = digestSfolValue(adapterSourceDigests);
  const bindingInput = {
    binding_id: "body-war.CreateSuggestedTrack.memory-binding",
    selector: bindingSelectorForCase(derived),
    target: {
      adapter_kind: "pure-function",
      module: TARGET_MODULE,
      symbol: TARGET_SYMBOL,
      target_digest: targetDigest,
      runtime_digest: runtimeDigest,
    },
    argument_map: [
      { parameter: "principalId", input_name: "principalId" },
      { parameter: "name", input_name: "name" },
      { parameter: "placeLabel", input_name: "placeLabel" },
      { parameter: "city", input_name: "city" },
      { parameter: "country", input_name: "country" },
      { parameter: "distanceHintMeters", input_name: "distanceHintMeters" },
      { parameter: "publicNote", input_name: "publicNote" },
    ],
    observation_map: { kind: "return" },
  };
  const bindingRegistry = decodeLogicBindingRegistry({
    schema_version: SFOL_BINDING_SCHEMA_VERSION,
    registry_id: "body-war.CT-2.bindings",
    bindings: [bindingInput],
  });
  assertCondition(
    bindingRegistry.ok,
    `CT-2 binding schema failed: ${JSON.stringify(
      bindingRegistry.ok ? [] : bindingRegistry.diagnostics,
    )}`,
  );
  const binding = resolvePureBinding(
    {
      selector: bindingSelectorForCase(derived),
      adapter_kind: "pure-function",
    },
    bindingRegistry.value,
  );
  assertCondition(
    binding.ok,
    `CT-2 binding resolution failed: ${JSON.stringify(
      binding.ok ? [] : binding.diagnostics,
    )}`,
  );

  const inputNames = binding.value.binding.argument_map.map(
    ({ input_name }) => input_name,
  );
  const arguments_ = orderedArguments(derived, inputNames);
  const normalizedBackend = await observeMemoryRepository(
    arguments_,
    inputNames,
  );
  const observation = runPureCase(
    toPureInvocation(derived),
    binding.value,
    targetResolver(
      preparedHandle(
        normalizedBackend,
        arguments_,
        targetDigest,
        runtimeDigest,
      ),
    ),
  );
  const evaluation = evaluatePureObservation(
    typed.value,
    derived,
    binding.value,
    observation,
  );
  assertCondition(
    evaluation.status === "pass",
    `memory repository differs from CT-2: ${evaluation.detail}`,
  );
  const stageCaseIds = [derived.case_id];
  const proofInput = {
    denominator,
    typed_artifact_digest: digestSfolValue(typed.value),
    upstream_case_sets: {
      C_spec: stageCaseIds,
      C_projected: stageCaseIds,
      C_validated: stageCaseIds,
      C_typed: stageCaseIds,
    },
    cases: [derived],
    bindings: [binding.value],
    observations: [observation],
    evaluations: [evaluation],
    tool_digest: targetDigest,
  };
  const proof = buildPureProofReceipt(proofInput);
  assertCondition(
    proof.ok,
    `CT-2 proof construction failed: ${JSON.stringify(
      proof.ok ? [] : proof.diagnostics,
    )}`,
  );

  const mutatedObservation = runPureCase(
    toPureInvocation(derived),
    binding.value,
    targetResolver(
      preparedHandle(
        strongerMutation(),
        arguments_,
        targetDigest,
        runtimeDigest,
      ),
    ),
  );
  const mutatedEvaluation = evaluatePureObservation(
    typed.value,
    derived,
    binding.value,
    mutatedObservation,
  );
  assertCondition(
    mutatedEvaluation.status === "fail",
    "stronger backend mutation was not rejected",
  );
  const mutatedProof = buildPureProofReceipt({
    ...proofInput,
    observations: [mutatedObservation],
    evaluations: [mutatedEvaluation],
  });
  assertCondition(!mutatedProof.ok, "mutated backend produced a proof receipt");
  const mutationDiagnostic = mutatedProof.diagnostics[0];
  assertCondition(
    mutationDiagnostic?.code === "SFOL_PROOF_NONPASS_STATE",
    "mutation failed for an unexpected reason",
  );

  mkdirSync(generatedRoot, { recursive: true });
  writeFileSync(resolve(generatedRoot, "graph.json"), first.graphBytes);
  writeFileSync(
    resolve(generatedRoot, "source-manifest.json"),
    first.sourceManifestBytes,
  );
  writeFileSync(
    resolve(generatedRoot, "build-receipt.json"),
    first.buildReceiptBytes,
  );
  writeJson(resolve(generatedRoot, "logic-projection.json"), envelope);

  const unsignedReceipt = {
    schema_version: "body-war-domainspec-ct2-proof/v1" as const,
    status: "pass" as const,
    authority_effect: "none" as const,
    release_admission: "not-granted" as const,
    source: {
      node_id: NODE_ID,
      module_id: MODULE_ID,
      clause_id: CLAUSE_ID,
      profile_digest: PROFILE_DIGEST,
      envelope_schema_digest: ENVELOPE_SCHEMA_DIGEST,
      node_digest: envelope.node.node_digest,
      logic_digest: envelope.logic_digest,
      clause_digest: clauseDigest,
    },
    build: {
      deterministic: true as const,
      verified: true as const,
      graph_digest: sha256(first.graphBytes),
      source_manifest_digest: sha256(first.sourceManifestBytes),
      build_receipt_digest: sha256(first.buildReceiptBytes),
      source_set_digest: first.graph.source_set_digest,
      projection_digest: digestSfolValue(envelope),
    },
    generated_case: {
      case_id: derived.case_id,
      case_digest: derived.case_digest,
      fixture_digest: derived.fixture_digest,
      expected_digest: derived.expected_digest,
    },
    backend_adapter: {
      target_digest: targetDigest,
      runtime_digest: runtimeDigest,
      source_digests: adapterSourceDigests,
      normalized_fields: [
        "status",
        "geometryAuthority",
        "sourceBacked",
        "pilotReady",
      ] as const,
    },
    proof: {
      receipt_digest: proof.value.receipt_digest,
      case_count: proof.value.case_count,
      stage_sets: proof.value.stage_sets,
    },
    mutation_control: {
      mutation: "stronger-backend-claims" as const,
      evaluation_status: "fail" as const,
      proof_status: "rejected" as const,
      diagnostic_code: mutationDiagnostic.code,
    },
  };
  const receipt: DomainspecCt2Receipt = Object.freeze({
    ...unsignedReceipt,
    receipt_digest: digestSfolValue(unsignedReceipt),
  });
  const receiptBytes = bytes(receipt);
  mkdirSync(dirname(receiptPath), { recursive: true });
  writeFileSync(receiptPath, receiptBytes);
  return Object.freeze({
    receipt,
    receipt_bytes: receiptBytes,
  });
}
