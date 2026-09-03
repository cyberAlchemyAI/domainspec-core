#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { addCalculation, addMapping, addOperation, addPolicy, addQuery, addRule, type AddCalculationInput, type AddMappingInput, type AddOperationInput, type AddPolicyInput, type AddQueryInput, type AddRuleInput } from "../authoring/add-operation.js";
import { decodeRuleExpression, decodeTypedOperationContract, decodeTypedRuleContract, type RuleExpression, type TypedParameter } from "../typed-operation/contracts.js";
import { observeTarget, observeTargetReceipt } from "../conformance/observe-target.js";
import { readInstantiationReceipt } from "../conformance/receipt.js";
import { planInstantiation } from "../generation/plan-instantiation.js";
import { publishInstantiation } from "../generation/publish-instantiation.js";
import { planProjectInstantiation } from "../generation/project-instantiation.js";
import { publishProjectInstantiation } from "../generation/publish-project.js";
import { checkLeanMetaTypeFormalization, materializeLeanMetaTypeFormalization } from "../formalization/projection.js";
import { loadCompiledProjectGraph, loadProjectNode, validateProjectRoot } from "../input/project-model.js";
import { normalizeLanguage } from "../meta-types/catalog.js";
import { loadSystemIntegrationSelection } from "../system-integration/compiler.js";
import { decodeCalculationSemantics, decodeMappingFields, decodePolicyDecisions } from "../static-semantics/contracts.js";
import { verifyProject } from "../verification/verify-project.js";

export interface CliIo {
  readonly stdout: (value: string) => void;
  readonly stderr: (value: string) => void;
}

class CliUsageError extends Error {
  readonly exitCode = 22;
  readonly code = "MTCLI_USAGE";
  readonly pointer = "/argv";
}

function usage(message: string): never {
  throw new CliUsageError(message);
}

function objectOutput(io: CliIo, value: unknown): void {
  io.stdout(`${JSON.stringify(value, null, 2)}\n`);
}

function exactlyOneRoot(args: readonly string[], command: string): string {
  if (args.length !== 1) usage(`${command} requires exactly one explicit root`);
  const root = args[0];
  if (!root || !path.isAbsolute(root)) usage(`${command} requires an absolute root`);
  return root;
}

function parseCsvSet(value: string | undefined, option: string): readonly string[] {
  if (value === undefined) return Object.freeze([]);
  const entries = value.split(",").map((entry) => entry.trim());
  if (entries.some((entry) => entry.length === 0)) usage(`${option} must be a comma-separated list without empty entries`);
  if (new Set(entries).size !== entries.length) usage(`${option} must not contain duplicate entries`);
  return Object.freeze(entries);
}

function addOperationArgs(args: readonly string[]): AddOperationInput {
  const sourceRoot = args[0];
  if (!sourceRoot || !path.isAbsolute(sourceRoot)) usage("add operation requires one absolute source project root");
  const values = new Map<string, string>();
  const allowedOptions = [
    "--feature",
    "--name",
    "--description",
    "--reads",
    "--writes",
    "--effects",
    "--guard",
    "--failure-continuation",
  ];
  for (let index = 1; index < args.length; index += 2) {
    const option = args[index];
    const value = args[index + 1];
    if (!option || !allowedOptions.includes(option) || !value || value.startsWith("--")) {
      usage("add operation received an unsupported or unvalued option");
    }
    if (values.has(option)) usage(`duplicate option:${option}`);
    values.set(option, value);
  }
  for (const required of ["--feature", "--name", "--description", "--guard", "--failure-continuation"]) {
    if (!values.has(required)) usage(`add operation requires ${required}`);
  }
  return Object.freeze({
    sourceRoot,
    featureId: values.get("--feature")!,
    nodeId: values.get("--name")!,
    description: values.get("--description")!,
    reads: parseCsvSet(values.get("--reads"), "--reads"),
    writes: parseCsvSet(values.get("--writes"), "--writes"),
    effects: parseCsvSet(values.get("--effects"), "--effects"),
    guard: values.get("--guard")!,
    failureContinuation: values.get("--failure-continuation")!,
  });
}

function parseJsonOption(value: string, option: string): unknown {
  try {
    return JSON.parse(value);
  } catch {
    usage(`${option} must contain valid JSON`);
  }
}

function addRuleArgs(args: readonly string[]): AddRuleInput {
  const sourceRoot = args[0];
  if (!sourceRoot || !path.isAbsolute(sourceRoot)) usage("add rule requires one absolute source project root");
  const values = new Map<string, string>();
  const allowedOptions = ["--feature", "--name", "--description", "--ontology-rule", "--parameters-json", "--expression-json"];
  for (let index = 1; index < args.length; index += 2) {
    const option = args[index];
    const value = args[index + 1];
    if (!option || !allowedOptions.includes(option) || value === undefined || value.startsWith("--")) usage("add rule received an unsupported or unvalued option");
    if (values.has(option)) usage(`duplicate option:${option}`);
    values.set(option, value);
  }
  for (const required of allowedOptions) if (!values.has(required)) usage(`add rule requires ${required}`);
  const candidate = decodeTypedRuleContract({
    schema_version: "domainspec.typed-rule/v1",
    ontology_rule: values.get("--ontology-rule"),
    parameters: parseJsonOption(values.get("--parameters-json")!, "--parameters-json"),
    expression: parseJsonOption(values.get("--expression-json")!, "--expression-json"),
  });
  return Object.freeze({
    sourceRoot,
    featureId: values.get("--feature")!,
    nodeId: values.get("--name")!,
    description: values.get("--description")!,
    ontologyRule: candidate.ontology_rule,
    parameters: candidate.parameters as readonly TypedParameter[],
    expression: decodeRuleExpression(candidate.expression) as RuleExpression,
  });
}

function addQueryArgs(args: readonly string[]): AddQueryInput {
  const sourceRoot = args[0];
  if (!sourceRoot || !path.isAbsolute(sourceRoot)) usage("add query requires one absolute source project root");
  const values = new Map<string, string>();
  const allowedOptions = ["--feature", "--name", "--description", "--reads", "--typed-contract-json"];
  for (let index = 1; index < args.length; index += 2) {
    const option = args[index];
    const value = args[index + 1];
    if (!option || !allowedOptions.includes(option) || value === undefined || value.startsWith("--")) usage("add query received an unsupported or unvalued option");
    if (values.has(option)) usage(`duplicate option:${option}`);
    values.set(option, value);
  }
  for (const required of allowedOptions) if (!values.has(required)) usage(`add query requires ${required}`);
  return Object.freeze({
    sourceRoot,
    featureId: values.get("--feature")!,
    nodeId: values.get("--name")!,
    description: values.get("--description")!,
    reads: parseCsvSet(values.get("--reads"), "--reads"),
    typedContract: decodeTypedOperationContract(parseJsonOption(values.get("--typed-contract-json")!, "--typed-contract-json")),
  });
}

function valuedOptions(args: readonly string[], command: string, allowed: readonly string[]): ReadonlyMap<string, string> {
  const values = new Map<string, string>();
  for (let index = 1; index < args.length; index += 2) {
    const option = args[index]; const value = args[index + 1];
    if (!option || !allowed.includes(option) || value === undefined || value.startsWith("--")) usage(`${command} received an unsupported or unvalued option`);
    if (values.has(option)) usage(`duplicate option:${option}`);
    values.set(option, value);
  }
  for (const required of allowed) if (!values.has(required)) usage(`${command} requires ${required}`);
  return values;
}

function staticSourceRoot(args: readonly string[], command: string): string {
  const root = args[0];
  if (!root || !path.isAbsolute(root)) usage(`${command} requires one absolute source project root`);
  return root;
}

function addCalculationArgs(args: readonly string[]): AddCalculationInput {
  const sourceRoot = staticSourceRoot(args, "add calculation");
  const values = valuedOptions(args, "add calculation", ["--feature", "--name", "--description", "--inputs", "--semantics-json", "--calculates"]);
  const inputs = parseCsvSet(values.get("--inputs"), "--inputs");
  return Object.freeze({ sourceRoot, featureId: values.get("--feature")!, nodeId: values.get("--name")!, description: values.get("--description")!, inputs, semantics: decodeCalculationSemantics(parseJsonOption(values.get("--semantics-json")!, "--semantics-json"), inputs), calculates: parseCsvSet(values.get("--calculates"), "--calculates") });
}

function addPolicyArgs(args: readonly string[]): AddPolicyInput {
  const sourceRoot = staticSourceRoot(args, "add policy");
  const values = valuedOptions(args, "add policy", ["--feature", "--name", "--description", "--strategies", "--decisions-json", "--default-strategy", "--applies"]);
  const strategies = parseCsvSet(values.get("--strategies"), "--strategies");
  return Object.freeze({ sourceRoot, featureId: values.get("--feature")!, nodeId: values.get("--name")!, description: values.get("--description")!, strategies, decisions: decodePolicyDecisions(parseJsonOption(values.get("--decisions-json")!, "--decisions-json"), strategies), defaultStrategy: values.get("--default-strategy")!, applies: parseCsvSet(values.get("--applies"), "--applies") });
}

function addMappingArgs(args: readonly string[]): AddMappingInput {
  const sourceRoot = staticSourceRoot(args, "add mapping");
  const values = valuedOptions(args, "add mapping", ["--feature", "--name", "--description", "--source", "--target", "--direction", "--totality", "--fields-json"]);
  const direction = values.get("--direction");
  if (direction !== "inbound" && direction !== "outbound" && direction !== "bidirectional") usage("--direction must be inbound, outbound, or bidirectional");
  const totality = values.get("--totality");
  if (totality !== "total" && totality !== "partial") usage("--totality must be total or partial");
  return Object.freeze({ sourceRoot, featureId: values.get("--feature")!, nodeId: values.get("--name")!, description: values.get("--description")!, sourceNodeId: values.get("--source")!, targetNodeId: values.get("--target")!, direction, totality, fields: decodeMappingFields(parseJsonOption(values.get("--fields-json")!, "--fields-json")) });
}

interface InstantiateArgs {
  readonly sourceRoot: string;
  readonly node: string;
  readonly language: "typescript" | "python" | "rust";
  readonly targetRoot: string;
  readonly integrationProfile: string | null;
  readonly integrationBindingSet: string | null;
}

function instantiateArgs(args: readonly string[]): InstantiateArgs {
  const sourceRoot = args[0];
  if (!sourceRoot || !path.isAbsolute(sourceRoot)) usage("instantiate requires one absolute source project root");
  const values = new Map<string, string>();
  const allowedOptions = ["--node", "--language", "--target-root", "--integration-profile", "--integration-binding-set"];
  for (let index = 1; index < args.length; index += 2) {
    const option = args[index];
    const value = args[index + 1];
    if (!option || !allowedOptions.includes(option) || !value || value.startsWith("--")) usage("instantiate requires valued --node, --language, --target-root, and optional system-integration profile options");
    if (values.has(option)) usage(`duplicate option:${option}`);
    values.set(option, value);
  }
  for (const required of ["--node", "--language", "--target-root"]) if (!values.has(required)) usage("instantiate requires --node, --language, and --target-root");
  const integrationProfile = values.get("--integration-profile") ?? null;
  const integrationBindingSet = values.get("--integration-binding-set") ?? null;
  if ((integrationProfile === null) !== (integrationBindingSet === null)) usage("--integration-profile and --integration-binding-set must be supplied together");
  if (values.size !== (integrationProfile === null ? 3 : 5)) usage("instantiate received an unsupported option set");
  const targetRoot = values.get("--target-root")!;
  if (!path.isAbsolute(targetRoot)) usage("--target-root must be absolute");
  return Object.freeze({
    sourceRoot,
    node: values.get("--node")!,
    language: normalizeLanguage(values.get("--language")),
    targetRoot,
    integrationProfile,
    integrationBindingSet,
  });
}

function instantiateProjectArgs(args: readonly string[]): { readonly sourceRoot: string; readonly languages: readonly ("typescript" | "python" | "rust")[]; readonly targetRoot: string } {
  const sourceRoot = args[0];
  if (!sourceRoot || !path.isAbsolute(sourceRoot)) usage("instantiate-project requires one absolute source project root");
  const values = valuedOptions(args, "instantiate-project", ["--languages", "--target-root"]);
  const languages = parseCsvSet(values.get("--languages"), "--languages").map((language) => normalizeLanguage(language));
  if (languages.length < 1 || languages.length > 3 || new Set(languages).size !== languages.length) usage("instantiate-project requires one or more unique supported languages");
  const targetRoot = values.get("--target-root")!;
  if (!path.isAbsolute(targetRoot)) usage("--target-root must be absolute");
  return Object.freeze({ sourceRoot, languages: Object.freeze(languages), targetRoot });
}

function formalizeArgs(args: readonly string[], command: "formalize" | "formalize-check"): { readonly sourceRoot: string; readonly targetPath: string } {
  const sourceRoot = args[0];
  if (!sourceRoot || !path.isAbsolute(sourceRoot) || args.length !== 3 || args[1] !== "--target" || !path.isAbsolute(args[2] ?? "")) {
    usage(`${command} requires one absolute source project root and --target <absolute-file>`);
  }
  return Object.freeze({ sourceRoot, targetPath: args[2]! });
}

function verifyProjectArgs(args: readonly string[]): { readonly sourceRoot: string; readonly targetRoot: string } {
  const sourceRoot = args[0];
  if (!sourceRoot || !path.isAbsolute(sourceRoot) || args.length !== 3 || args[1] !== "--target-root" || !path.isAbsolute(args[2] ?? "")) {
    usage("verify-project requires one absolute source project root and --target-root <absolute-directory>");
  }
  return Object.freeze({ sourceRoot, targetRoot: args[2]! });
}

function isInstantiationTarget(root: string): boolean {
  return fs.existsSync(path.join(root, ".domainspec", "instantiations"));
}

function errorEnvelope(error: unknown): Record<string, unknown> {
  const candidate = error as Partial<Error> & { code?: unknown; pointer?: unknown };
  return {
    result: "fail",
    code: typeof candidate.code === "string" ? candidate.code : "MTCLI_UNEXPECTED",
    pointer: typeof candidate.pointer === "string" ? candidate.pointer : "$",
    message: error instanceof Error ? error.message : "unexpected failure",
    authority_effect: "none",
  };
}

export function runCli(argv: readonly string[], io: CliIo = {
  stdout: (value) => process.stdout.write(value),
  stderr: (value) => process.stderr.write(value),
}): number {
  try {
    const [command, ...args] = argv;
    if (command === "add") {
      if (!args[0] || !["operation", "query", "calculation", "rule", "policy", "mapping"].includes(args[0])) usage("add requires a supported meta-type: operation, query, calculation, rule, policy, or mapping");
      const result = args[0] === "operation"
        ? addOperation(addOperationArgs(args.slice(1)))
        : args[0] === "query"
          ? addQuery(addQueryArgs(args.slice(1)))
          : args[0] === "calculation"
            ? addCalculation(addCalculationArgs(args.slice(1)))
            : args[0] === "rule"
              ? addRule(addRuleArgs(args.slice(1)))
              : args[0] === "policy"
                ? addPolicy(addPolicyArgs(args.slice(1)))
                : addMapping(addMappingArgs(args.slice(1)));
      objectOutput(io, {
        schema_version: `domainspec.add-${args[0]}-command-result/v1`,
        result: "pass",
        publication_protocol: result.publication_protocol,
        source_root: result.source_root,
        selector: result.selector,
        node_path: result.node_path,
        relationship_paths: result.relationship_paths,
        source_manifest_sha256: result.source_manifest.manifest_sha256,
        source_count: result.source_manifest.source_count,
        authority_effect: result.authority_effect,
      });
      return 0;
    }
    if (command === "instantiate") {
      const parsed = instantiateArgs(args);
      const node = loadProjectNode(parsed.sourceRoot, parsed.node);
      const systemIntegration = parsed.integrationProfile === null || parsed.integrationBindingSet === null
        ? null
        : loadSystemIntegrationSelection(node.project_root, parsed.integrationBindingSet, parsed.integrationProfile, `${node.feature_id}:${node.node_id}`, parsed.language);
      const plan = planInstantiation(node, parsed.language, systemIntegration);
      const publication = publishInstantiation(plan, parsed.targetRoot);
      const observation = observeTarget(publication.target_root);
      objectOutput(io, {
        schema_version: "domainspec.instantiate-command-result/v1",
        result: "pass",
        target_root: publication.target_root,
        receipt_path: publication.receipt_path,
        plan_sha256: plan.plan_sha256,
        receipt_sha256: publication.receipt.receipt_sha256,
        system_integration_binding_digest: plan.system_integration?.manifest.binding_digest ?? null,
        observation,
        authority_effect: "none",
      });
      return 0;
    }
    if (command === "instantiate-project") {
      const parsed = instantiateProjectArgs(args);
      const plan = planProjectInstantiation(parsed.sourceRoot, parsed.languages);
      const publication = publishProjectInstantiation(plan, parsed.targetRoot);
      objectOutput(io, { schema_version: "domainspec.instantiate-project-command-result/v1", result: "pass", target_root: publication.target_root, receipt_path: publication.receipt_path, project_plan_sha256: plan.project_plan_sha256, receipt_sha256: publication.receipt.receipt_sha256, graph_certificate: plan.graph_certificate, artifact_count: plan.artifacts.length, authority_effect: "none" });
      return 0;
    }
    if (command === "verify-project") {
      const parsed = verifyProjectArgs(args);
      objectOutput(io, verifyProject(parsed.sourceRoot, parsed.targetRoot));
      return 0;
    }
    if (command === "formalize" || command === "formalize-check") {
      const parsed = formalizeArgs(args, command);
      const projectGraph = loadCompiledProjectGraph(parsed.sourceRoot);
      const sourceManifest = projectGraph.source_manifest;
      if (command === "formalize") {
        const result = materializeLeanMetaTypeFormalization(projectGraph, parsed.targetPath);
        objectOutput(io, {
          schema_version: "domainspec.meta-type-formalization-command-result/v1-candidate",
          result: "pass",
          source_manifest_sha256: sourceManifest.manifest_sha256,
          ...result,
          authority_effect: "none",
        });
        return 0;
      }
      const result = checkLeanMetaTypeFormalization(projectGraph, parsed.targetPath);
      objectOutput(io, {
        schema_version: "domainspec.meta-type-formalization-command-result/v1-candidate",
        result: result.current ? "pass" : "fail",
        source_manifest_sha256: sourceManifest.manifest_sha256,
        ...result,
        authority_effect: "none",
      });
      return result.current ? 0 : 1;
    }
    if (command === "lint") {
      const root = exactlyOneRoot(args, "lint");
      if (isInstantiationTarget(root)) {
        const observation = observeTargetReceipt(root);
        objectOutput(io, observation);
        return observation.result === "pass" ? 0 : 1;
      }
      objectOutput(io, {
        schema_version: "domainspec.source-project-lint/v1",
        result: "pass",
        source_manifest: validateProjectRoot(root),
        authority_effect: "none",
      });
      return 0;
    }
    if (command === "receipt") {
      const root = exactlyOneRoot(args, "receipt");
      if (isInstantiationTarget(root)) {
        const observation = observeTargetReceipt(root);
        if (observation.result === "fail") {
          objectOutput(io, { observation });
          return 1;
        }
        objectOutput(io, { receipt: readInstantiationReceipt(root), observation });
      } else {
        objectOutput(io, validateProjectRoot(root));
      }
      return 0;
    }
    usage("expected command: add <meta-type>, instantiate, instantiate-project, verify-project, formalize, formalize-check, lint, or receipt");
  } catch (error) {
    objectOutput({ ...io, stdout: io.stderr }, errorEnvelope(error));
    const candidate = error as { exitCode?: unknown };
    return typeof candidate.exitCode === "number" ? candidate.exitCode : 1;
  }
}

if (process.argv[1] && fs.realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = runCli(process.argv.slice(2));
}
