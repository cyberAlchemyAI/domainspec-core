import fs from "node:fs";
import path from "node:path";

import { metaTypeIdForLabel } from "../meta-types/catalog.js";
import {
  RELATIONSHIP_AUTHORITY_SHA256,
  RELATIONSHIP_SIGNATURES,
  deprecatedRelationship,
  generatedRelationshipView,
  relationshipSignature,
} from "../relationships/authority.js";
import { resolveProjectRoot } from "./project-root.js";
import { sha256, type SourceManifestV1 } from "./source-manifest.js";
import {
  decodeTypedOperationContract,
  decodeTypedRecordContract,
  decodeTypedRuleContract,
  decodeTypedSumContract,
} from "../typed-operation/contracts.js";
import { compileTypedOperationClosure, type TypedClosureSourceNode, type TypedOperationClosureV1 } from "../typed-operation/closure.js";

export { RELATIONSHIP_AUTHORITY_SHA256, RELATIONSHIP_SIGNATURES } from "../relationships/authority.js";

const SELECTOR_PATTERN = /^([a-z][a-z0-9]*(?:-[a-z0-9]+)*):([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$/;
const NODE_ID_PATTERN = /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;
const COMPENSATION_DEPENDENCY_PATTERN = /^([a-z][a-z0-9]*(?:-[a-z0-9]+)*):depends-on:([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$/;

type BodyFieldKind = "string" | "string-array" | "record-fields" | "field-spec" | "field-spec-array" | "interface-operation-array" | "state-transition-array" | "typed-record" | "typed-sum" | "typed-rule" | "typed-operation";

interface BodyContract {
  readonly required: readonly string[];
  readonly optional: readonly string[];
  readonly fields: Readonly<Record<string, BodyFieldKind>>;
  readonly nonemptyArrays?: readonly string[];
}

export const BODY_CONTRACTS: Readonly<Record<string, BodyContract>> = Object.freeze({
  Entity: { required: ["description", "fields"], optional: ["identity_field", "typed_contract"], fields: { description: "string", identity_field: "string", fields: "record-fields", typed_contract: "typed-record" }, nonemptyArrays: ["fields"] },
  "Value Object": { required: ["description", "fields"], optional: ["invariant_refs", "typed_contract"], fields: { description: "string", fields: "record-fields", invariant_refs: "string-array", typed_contract: "typed-record" }, nonemptyArrays: ["fields", "invariant_refs"] },
  Enum: { required: ["description", "values"], optional: ["typed_contract"], fields: { description: "string", values: "string-array", typed_contract: "typed-sum" }, nonemptyArrays: ["values"] },
  Operation: {
    required: ["description", "reads", "writes", "effects", "guard", "failure_continuation"],
    optional: ["typed_contract"],
    fields: { description: "string", reads: "string-array", writes: "string-array", effects: "string-array", guard: "string", failure_continuation: "string", typed_contract: "typed-operation" },
  },
  Query: { required: ["description", "reads"], optional: [], fields: { description: "string", reads: "string-array" } },
  Calculation: { required: ["description", "inputs"], optional: [], fields: { description: "string", inputs: "string-array" } },
  Rule: { required: ["description", "predicate"], optional: ["typed_contract"], fields: { description: "string", predicate: "string", typed_contract: "typed-rule" } },
  Policy: { required: ["description", "strategies"], optional: [], fields: { description: "string", strategies: "string-array" }, nonemptyArrays: ["strategies"] },
  Workflow: {
    required: ["description", "steps", "compensations"],
    optional: ["compensation_dependencies"],
    fields: { description: "string", steps: "string-array", compensations: "string-array", compensation_dependencies: "string-array" },
    nonemptyArrays: ["steps"],
  },
  Interface: { required: ["description", "boundary_kind", "version", "compatibility", "operations"], optional: [], fields: { description: "string", boundary_kind: "string", version: "string", compatibility: "string", operations: "interface-operation-array" }, nonemptyArrays: ["operations"] },
  Event: { required: ["description", "event_type", "version", "occurrence_id", "occurred_at_policy", "payload"], optional: [], fields: { description: "string", event_type: "string", version: "string", occurrence_id: "field-spec", occurred_at_policy: "string", payload: "field-spec-array" } },
  Mapping: { required: ["description", "source", "target"], optional: [], fields: { description: "string", source: "string", target: "string" } },
  "State Machine": { required: ["description", "states", "initial", "transitions"], optional: [], fields: { description: "string", states: "string-array", initial: "string", transitions: "state-transition-array" }, nonemptyArrays: ["states", "transitions"] },
});

export interface StateTransitionSpec {
  readonly transition_id: string;
  readonly source_state: string;
  readonly target_state: string;
  readonly guard_ref: string | null;
  readonly effect_event_ref: string | null;
}

export type PrimitiveTypeName = "string" | "boolean" | "integer" | "decimal" | "timestamp" | "uuid";

export type TypeRef =
  | Readonly<{ kind: "primitive"; name: PrimitiveTypeName }>
  | Readonly<{ kind: "reference"; selector: string }>;

export interface FieldSpec {
  readonly field_id: string;
  readonly type_ref: TypeRef;
  readonly required: boolean;
}

export interface InterfaceOperationSpec {
  readonly operation_id: string;
  readonly operation_ref: string;
  readonly request: readonly FieldSpec[];
  readonly result: readonly FieldSpec[];
}

export type DecodedBodyValue = string | readonly string[] | FieldSpec | readonly FieldSpec[] | readonly InterfaceOperationSpec[] | readonly StateTransitionSpec[];

export interface DecodedBody {
  readonly [key: string]: unknown;
}

export interface DecodedEndpoint {
  readonly feature_id: string;
  readonly node_id: string;
  readonly kind: string;
}

export interface DecodedRelationship {
  readonly edge_id: string;
  readonly relationship: string;
  readonly scope: "feature" | "project";
  readonly source: DecodedEndpoint;
  readonly target: DecodedEndpoint;
}

export interface DecodedProjectNode {
  readonly project_root: string;
  readonly project_id: string;
  readonly feature_id: string;
  readonly node_id: string;
  readonly kind: string;
  readonly meta_type_id: string;
  readonly body: DecodedBody;
  readonly relationships: readonly DecodedRelationship[];
  readonly source_manifest: SourceManifestV1;
  readonly typed_closure: TypedOperationClosureV1 | null;
}

export interface CompiledProjectGraphNode {
  readonly feature_id: string;
  readonly node_id: string;
  readonly selector: string;
  readonly kind: string;
  readonly meta_type_id: string;
  readonly body: DecodedBody;
  readonly generated_relationship_projections: Readonly<Record<string, readonly string[]>>;
  readonly authored_forbidden_projection_attributes: readonly string[];
}

export interface CompiledProjectGraph {
  readonly schema_version: "domainspec.compiled-project-graph/v1-candidate";
  readonly project_root: string;
  readonly project_id: string;
  readonly source_manifest: SourceManifestV1;
  readonly nodes: readonly CompiledProjectGraphNode[];
  readonly relationships: readonly DecodedRelationship[];
  readonly authority_effect: "none";
}

export class ProjectModelError extends Error {
  readonly exitCode = 22;

  constructor(readonly code: string, readonly pointer: string, message: string) {
    super(message);
    this.name = "ProjectModelError";
  }
}

function fail(code: string, pointer: string, message: string): never {
  throw new ProjectModelError(code, pointer, message);
}

function isObject(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function exactKeys(value: unknown, expected: readonly string[], pointer: string): asserts value is Record<string, unknown> {
  if (!isObject(value)) fail("MTCLI_INPUT_SCHEMA", pointer, "expected object");
  if (JSON.stringify(Object.keys(value).sort()) !== JSON.stringify([...expected].sort())) fail("MTCLI_INPUT_SCHEMA", pointer, "unexpected or missing member");
}

function readBoundJson(projectRoot: string, manifest: SourceManifestV1, relativePath: string): Record<string, unknown> {
  const ref = manifest.sources.find((source) => source.relative_path === relativePath);
  if (!ref) fail("MTCLI_INPUT_MISSING", `/${relativePath}`, "source is absent from the project manifest");
  const bytes = fs.readFileSync(path.join(projectRoot, relativePath));
  if (bytes.length !== ref.size_bytes || sha256(bytes) !== ref.sha256) fail("MTCLI_INPUT_DRIFT", `/${relativePath}`, "source changed after project-root validation");
  let value: unknown;
  try {
    value = JSON.parse(bytes.toString("utf8"));
  } catch {
    fail("MTCLI_INPUT_JSON", `/${relativePath}`, "source is not valid JSON");
  }
  if (!isObject(value)) fail("MTCLI_INPUT_SCHEMA", `/${relativePath}`, "source must be an object");
  return value;
}

function requireString(value: unknown, pointer: string): string {
  if (typeof value !== "string" || value.length === 0) fail("MTCLI_INPUT_BODY", pointer, "expected nonempty string");
  return value;
}

function requireStringArray(value: unknown, pointer: string, nonempty: boolean): readonly string[] {
  if (!Array.isArray(value) || (nonempty && value.length === 0)) fail("MTCLI_INPUT_BODY", pointer, "expected string array");
  const result = value.map((entry, index) => requireString(entry, `${pointer}/${index}`));
  if (new Set(result).size !== result.length) fail("MTCLI_INPUT_BODY", pointer, "duplicate array member");
  return Object.freeze(result);
}

const PRIMITIVE_TYPES = new Set<PrimitiveTypeName>(["string", "boolean", "integer", "decimal", "timestamp", "uuid"]);

function requireSelector(value: unknown, pointer: string, code = "MTCLI_TYPE_REFERENCE"): string {
  const selector = requireString(value, pointer);
  if (!SELECTOR_PATTERN.test(selector)) fail(code, pointer, "reference must be a feature-id:node-id selector");
  return selector;
}

function requireTypeRef(value: unknown, pointer: string): TypeRef {
  if (!isObject(value) || typeof value.kind !== "string") fail("MTCLI_TYPE_REF", pointer, "type_ref must be an object with a closed kind");
  if (value.kind === "primitive") {
    exactKeys(value, ["kind", "name"], pointer);
    const name = requireString(value.name, `${pointer}/name`) as PrimitiveTypeName;
    if (!PRIMITIVE_TYPES.has(name)) fail("MTCLI_TYPE_REF", `${pointer}/name`, "unknown primitive type");
    return Object.freeze({ kind: "primitive", name });
  }
  if (value.kind === "reference") {
    exactKeys(value, ["kind", "selector"], pointer);
    return Object.freeze({ kind: "reference", selector: requireSelector(value.selector, `${pointer}/selector`) });
  }
  return fail("MTCLI_TYPE_REF", `${pointer}/kind`, "type_ref kind must be primitive or reference");
}

function requireFieldSpec(value: unknown, pointer: string): FieldSpec {
  exactKeys(value, ["field_id", "type_ref", "required"], pointer);
  const fieldId = requireString(value.field_id, `${pointer}/field_id`);
  if (!NODE_ID_PATTERN.test(fieldId)) fail("MTCLI_FIELD_ID", `${pointer}/field_id`, "field identity must be canonical kebab-case");
  if (typeof value.required !== "boolean") fail("MTCLI_FIELD_REQUIRED", `${pointer}/required`, "required must be boolean");
  return Object.freeze({ field_id: fieldId, type_ref: requireTypeRef(value.type_ref, `${pointer}/type_ref`), required: value.required });
}

function requireFieldSpecArray(value: unknown, pointer: string, nonempty: boolean): readonly FieldSpec[] {
  if (!Array.isArray(value) || (nonempty && value.length === 0)) fail("MTCLI_INPUT_BODY", pointer, "expected typed field array");
  const fields = value.map((entry, index) => requireFieldSpec(entry, `${pointer}/${index}`));
  const fieldIds = fields.map(({ field_id }) => field_id);
  if (new Set(fieldIds).size !== fieldIds.length) fail("MTCLI_FIELD_DUPLICATE", pointer, "field identities must be unique");
  return Object.freeze(fields);
}

function requireInterfaceOperationArray(value: unknown, pointer: string, nonempty: boolean): readonly InterfaceOperationSpec[] {
  if (!Array.isArray(value) || (nonempty && value.length === 0)) fail("MTCLI_INPUT_BODY", pointer, "expected interface operation array");
  const operations = value.map((entry, index): InterfaceOperationSpec => {
    const entryPointer = `${pointer}/${index}`;
    exactKeys(entry, ["operation_id", "operation_ref", "request", "result"], entryPointer);
    const operationId = requireString(entry.operation_id, `${entryPointer}/operation_id`);
    if (!NODE_ID_PATTERN.test(operationId)) fail("MTCLI_INTERFACE_OPERATION_ID", `${entryPointer}/operation_id`, "operation identity must be canonical kebab-case");
    return Object.freeze({
      operation_id: operationId,
      operation_ref: requireSelector(entry.operation_ref, `${entryPointer}/operation_ref`, "MTCLI_INTERFACE_OPERATION_REFERENCE"),
      request: requireFieldSpecArray(entry.request, `${entryPointer}/request`, false),
      result: requireFieldSpecArray(entry.result, `${entryPointer}/result`, false),
    });
  });
  const operationIds = operations.map(({ operation_id }) => operation_id);
  const operationRefs = operations.map(({ operation_ref }) => operation_ref);
  if (new Set(operationIds).size !== operationIds.length || new Set(operationRefs).size !== operationRefs.length) {
    fail("MTCLI_INTERFACE_OPERATION_DUPLICATE", pointer, "operation identities and references must be unique");
  }
  return Object.freeze(operations);
}

function requireNullableSelector(value: unknown, pointer: string): string | null {
  if (value === null) return null;
  const selector = requireString(value, pointer);
  if (!SELECTOR_PATTERN.test(selector)) fail("MTCLI_STATE_MACHINE_REFERENCE", pointer, "reference must be a feature-id:node-id selector or null");
  return selector;
}

function requireStateTransitionArray(value: unknown, pointer: string, nonempty: boolean): readonly StateTransitionSpec[] {
  if (!Array.isArray(value) || (nonempty && value.length === 0)) fail("MTCLI_INPUT_BODY", pointer, "expected nonempty state transition array");
  const transitions = value.map((entry, index): StateTransitionSpec => {
    const entryPointer = `${pointer}/${index}`;
    if (!isObject(entry)) fail("MTCLI_INPUT_BODY", entryPointer, "transition must be an object");
    const expected = ["transition_id", "source_state", "target_state", "guard_ref", "effect_event_ref"];
    if (JSON.stringify(Object.keys(entry).sort()) !== JSON.stringify(expected.sort())) {
      fail("MTCLI_INPUT_BODY", entryPointer, "transition must contain exactly transition_id, source_state, target_state, guard_ref, and effect_event_ref");
    }
    const transitionId = requireString(entry.transition_id, `${entryPointer}/transition_id`);
    if (!NODE_ID_PATTERN.test(transitionId)) fail("MTCLI_STATE_MACHINE_TRANSITION_ID", `${entryPointer}/transition_id`, "transition identity must be canonical kebab-case");
    return Object.freeze({
      transition_id: transitionId,
      source_state: requireString(entry.source_state, `${entryPointer}/source_state`),
      target_state: requireString(entry.target_state, `${entryPointer}/target_state`),
      guard_ref: requireNullableSelector(entry.guard_ref, `${entryPointer}/guard_ref`),
      effect_event_ref: requireNullableSelector(entry.effect_event_ref, `${entryPointer}/effect_event_ref`),
    });
  });
  const transitionIds = transitions.map(({ transition_id }) => transition_id);
  if (new Set(transitionIds).size !== transitionIds.length) fail("MTCLI_STATE_MACHINE_DUPLICATE_TRANSITION", pointer, "transition identities must be unique");
  return Object.freeze(transitions);
}

export function decodeBody(kind: string, value: unknown, pointer = "/body"): DecodedBody {
  const contract = BODY_CONTRACTS[kind];
  if (!contract) fail("MTCLI_INPUT_META_TYPE", pointer, `unsupported backend meta-type:${kind}`);
  if (!isObject(value)) fail("MTCLI_INPUT_BODY", pointer, "body must be an object");
  const allowed = [...contract.required, ...contract.optional];
  const actual = Object.keys(value);
  if (actual.some((key) => !allowed.includes(key)) || contract.required.some((key) => !actual.includes(key))) {
    fail("MTCLI_INPUT_BODY", pointer, `closed ${kind} body has unexpected or missing fields`);
  }
  const decoded: Record<string, unknown> = {};
  for (const key of allowed) {
    const fieldKind = contract.fields[key];
    if (!fieldKind) fail("MTCLI_INPUT_BODY", `${pointer}/${key}`, "body contract is incomplete");
    const raw = value[key];
    if (raw === undefined && contract.optional.includes(key)) {
      if (fieldKind === "string-array") decoded[key] = Object.freeze([]);
      else if (fieldKind === "string") decoded[key] = "";
      else continue;
    } else if (fieldKind === "string") {
      decoded[key] = requireString(raw, `${pointer}/${key}`);
    } else if (fieldKind === "string-array") {
      decoded[key] = requireStringArray(raw, `${pointer}/${key}`, contract.nonemptyArrays?.includes(key) ?? false);
    } else if (fieldKind === "record-fields") {
      decoded[key] = Array.isArray(raw) && raw.every((entry) => typeof entry === "string")
        ? requireStringArray(raw, `${pointer}/${key}`, contract.nonemptyArrays?.includes(key) ?? false)
        : requireFieldSpecArray(raw, `${pointer}/${key}`, contract.nonemptyArrays?.includes(key) ?? false);
    } else if (fieldKind === "typed-record") {
      decoded[key] = decodeTypedRecordContract(raw, `${pointer}/${key}`);
    } else if (fieldKind === "typed-sum") {
      decoded[key] = decodeTypedSumContract(raw, `${pointer}/${key}`);
    } else if (fieldKind === "typed-rule") {
      decoded[key] = decodeTypedRuleContract(raw, `${pointer}/${key}`);
    } else if (fieldKind === "typed-operation") {
      decoded[key] = decodeTypedOperationContract(raw, `${pointer}/${key}`);
    } else if (fieldKind === "field-spec") {
      decoded[key] = requireFieldSpec(raw, `${pointer}/${key}`);
    } else if (fieldKind === "field-spec-array") {
      decoded[key] = requireFieldSpecArray(raw, `${pointer}/${key}`, contract.nonemptyArrays?.includes(key) ?? false);
    } else if (fieldKind === "interface-operation-array") {
      decoded[key] = requireInterfaceOperationArray(raw, `${pointer}/${key}`, contract.nonemptyArrays?.includes(key) ?? false);
    } else {
      decoded[key] = requireStateTransitionArray(raw, `${pointer}/${key}`, contract.nonemptyArrays?.includes(key) ?? false);
    }
  }
  if ((kind === "Entity" || kind === "Value Object") && decoded.typed_contract) {
    const names = (decoded.typed_contract as ReturnType<typeof decodeTypedRecordContract>).properties.map(({ name }) => name);
    if (JSON.stringify(names) !== JSON.stringify(decoded.fields)) fail("MTCLI_TYPED_FIELD_PARITY", `${pointer}/fields`, "typed property names must exactly match fields");
  }
  if (kind === "Enum" && decoded.typed_contract) {
    const names = (decoded.typed_contract as ReturnType<typeof decodeTypedSumContract>).variants.map(({ name }) => name);
    if (JSON.stringify(names) !== JSON.stringify(decoded.values)) fail("MTCLI_TYPED_VARIANT_PARITY", `${pointer}/values`, "typed variant names must exactly match values");
  }
  if (kind === "Entity" && decoded.typed_contract === undefined) {
    if (!(decoded.identity_field as string)) fail("MTCLI_ENTITY_IDENTITY", `${pointer}/identity_field`, "identity_field is required for an L1 Entity");
    const fields = decoded.fields as readonly FieldSpec[];
    const identityField = decoded.identity_field as string;
    const identity = fields.find(({ field_id }) => field_id === identityField);
    if (!identity) fail("MTCLI_ENTITY_IDENTITY", `${pointer}/identity_field`, "identity_field must name one declared field");
    if (!identity.required) fail("MTCLI_ENTITY_IDENTITY", `${pointer}/fields`, "the identity field must be required");
  }
  if (kind === "Value Object" && decoded.typed_contract === undefined) {
    if (!(decoded.invariant_refs as readonly string[]).length) fail("MTCLI_VALUE_OBJECT_COMPLETE", `${pointer}/invariant_refs`, "invariant_refs are required for an L1 Value Object");
    const fields = decoded.fields as readonly FieldSpec[];
    if (fields.some(({ required }) => !required)) fail("MTCLI_VALUE_OBJECT_COMPLETE", `${pointer}/fields`, "every Value Object field must be required");
    for (const [index, invariantRef] of (decoded.invariant_refs as readonly string[]).entries()) {
      requireSelector(invariantRef, `${pointer}/invariant_refs/${index}`, "MTCLI_VALUE_OBJECT_INVARIANT_REFERENCE");
    }
  }
  if (kind === "Event") {
    if (!NODE_ID_PATTERN.test(decoded.event_type as string)) fail("MTCLI_EVENT_TYPE", `${pointer}/event_type`, "event_type must be canonical kebab-case");
    if (!/^[1-9][0-9]*$/.test(decoded.version as string)) fail("MTCLI_EVENT_VERSION", `${pointer}/version`, "Event version must be a positive integer string");
    if (!["required", "generated"].includes(decoded.occurred_at_policy as string)) fail("MTCLI_EVENT_OCCURRED_AT", `${pointer}/occurred_at_policy`, "occurred_at_policy must be required or generated");
    if (!(decoded.occurrence_id as FieldSpec).required) fail("MTCLI_EVENT_OCCURRENCE_ID", `${pointer}/occurrence_id`, "occurrence identity must be required");
  }
  if (kind === "Interface") {
    if (!["external", "internal"].includes(decoded.boundary_kind as string)) fail("MTCLI_INTERFACE_BOUNDARY", `${pointer}/boundary_kind`, "boundary_kind must be external or internal");
    if (!/^[1-9][0-9]*$/.test(decoded.version as string)) fail("MTCLI_INTERFACE_VERSION", `${pointer}/version`, "Interface version must be a positive integer string");
    if (!["exact", "backward"].includes(decoded.compatibility as string)) fail("MTCLI_INTERFACE_COMPATIBILITY", `${pointer}/compatibility`, "compatibility must be exact or backward");
  }
  if (kind === "State Machine") {
    const states = decoded.states as readonly string[];
    for (const [index, state] of states.entries()) if (!NODE_ID_PATTERN.test(state)) {
      fail("MTCLI_STATE_MACHINE_STATE", `${pointer}/states/${index}`, "state identity must be canonical kebab-case");
    }
    if (!states.includes(decoded.initial as string)) fail("MTCLI_INPUT_BODY", `${pointer}/initial`, "initial state is not declared");
    for (const [index, transition] of (decoded.transitions as readonly StateTransitionSpec[]).entries()) {
      if (!states.includes(transition.source_state)) fail("MTCLI_STATE_MACHINE_STATE", `${pointer}/transitions/${index}/source_state`, "transition source state is not declared");
      if (!states.includes(transition.target_state)) fail("MTCLI_STATE_MACHINE_STATE", `${pointer}/transitions/${index}/target_state`, "transition target state is not declared");
    }
  }
  if (kind === "Workflow") {
    const steps = decoded.steps as readonly string[];
    const compensations = decoded.compensations as readonly string[];
    if (compensations.length !== 0 && compensations.length !== steps.length) fail("MTCLI_INPUT_BODY", `${pointer}/compensations`, "compensations must be empty or align one-to-one with steps");
    const declaredCompensations = compensations.filter((operationId) => operationId !== "none");
    for (const [index, operationId] of declaredCompensations.entries()) {
      if (!NODE_ID_PATTERN.test(operationId)) fail("MTCLI_WORKFLOW_COMPENSATION_ID", `${pointer}/compensations/${index}`, "compensation must be an Operation node ID or none");
    }
    const dependencies = decoded.compensation_dependencies as readonly string[];
    const graph = new Map(declaredCompensations.map((operationId) => [operationId, new Set<string>()]));
    for (const [index, dependency] of dependencies.entries()) {
      const match = COMPENSATION_DEPENDENCY_PATTERN.exec(dependency);
      if (!match) fail("MTCLI_WORKFLOW_COMPENSATION_DEPENDENCY", `${pointer}/compensation_dependencies/${index}`, "dependency must use operation:depends-on:operation");
      const operationId = match[1] as string;
      const prerequisiteId = match[2] as string;
      if (operationId === prerequisiteId || !graph.has(operationId) || !graph.has(prerequisiteId)) {
        fail("MTCLI_WORKFLOW_COMPENSATION_DEPENDENCY", `${pointer}/compensation_dependencies/${index}`, "dependency endpoints must be distinct declared compensation Operations");
      }
      graph.get(operationId)?.add(prerequisiteId);
    }
    const emitted = new Set<string>();
    while (emitted.size < graph.size) {
      const ready = [...graph].find(([operationId, prerequisites]) => !emitted.has(operationId) && [...prerequisites].every((entry) => emitted.has(entry)));
      if (!ready) fail("MTCLI_WORKFLOW_COMPENSATION_DEPENDENCY_CYCLE", `${pointer}/compensation_dependencies`, "compensation dependency graph is cyclic");
      emitted.add(ready[0]);
    }
  }
  return Object.freeze(decoded);
}

export function validateSelectedNodeRelationships(node: DecodedProjectNode): void {
  const selector = `${node.feature_id}:${node.node_id}`;
  if (node.kind === "Interface") {
    const requiredRefs = new Set((node.body.operations as readonly InterfaceOperationSpec[]).map(({ operation_ref }) => operation_ref));
    const observedRefs = new Set(node.relationships
      .filter((relationship) => relationship.relationship === "exposes" && `${relationship.source.feature_id}:${relationship.source.node_id}` === selector)
      .map(({ target }) => `${target.feature_id}:${target.node_id}`));
    for (const operationRef of requiredRefs) if (!observedRefs.has(operationRef)) {
      fail("MTCLI_INTERFACE_EXPOSES_MISSING", "/relationships", `Interface operation lacks an exposes relationship:${operationRef}`);
    }
    for (const operationRef of observedRefs) if (!requiredRefs.has(operationRef)) {
      fail("MTCLI_INTERFACE_EXPOSES_UNDECLARED", "/relationships", `exposed Operation or Query is absent from Interface signatures:${operationRef}`);
    }
    return;
  }
  if (node.kind === "State Machine") {
    const transitions = node.body.transitions as readonly StateTransitionSpec[];
    const requiredEvents = new Set(transitions.flatMap(({ effect_event_ref }) => effect_event_ref === null ? [] : [effect_event_ref]));
    const observedEvents = new Set(node.relationships
      .filter((relationship) => relationship.relationship === "transitions" && `${relationship.target.feature_id}:${relationship.target.node_id}` === selector)
      .map(({ source }) => `${source.feature_id}:${source.node_id}`));
    for (const eventRef of requiredEvents) if (!observedEvents.has(eventRef)) {
      fail("MTCLI_STATE_MACHINE_EVENT_RELATIONSHIP_MISSING", "/relationships", `State Machine effect Event lacks an incoming transitions relationship:${eventRef}`);
    }
    for (const eventRef of observedEvents) if (!requiredEvents.has(eventRef)) {
      fail("MTCLI_STATE_MACHINE_EVENT_RELATIONSHIP_UNDECLARED", "/relationships", `incoming transitions Event is absent from State Machine effect intents:${eventRef}`);
    }
    return;
  }
  if (node.kind !== "Workflow") return;
  const orchestrated = node.relationships.filter((relationship) =>
    relationship.relationship === "orchestrates" &&
    `${relationship.source.feature_id}:${relationship.source.node_id}` === selector
  );
  const targetIds = orchestrated.map(({ target }) => target.node_id);
  if (new Set(targetIds).size !== targetIds.length) {
    fail("MTCLI_WORKFLOW_OPERATION_ID_AMBIGUOUS", "/relationships", "Workflow Operation node IDs must be unique across selected orchestrates edges");
  }
  const steps = node.body.steps as readonly string[];
  const compensations = (node.body.compensations as readonly string[]).filter((operationId) => operationId !== "none");
  const required = new Set([...steps, ...compensations]);
  const observed = new Set(targetIds);
  for (const operationId of required) {
    if (!observed.has(operationId)) {
      fail("MTCLI_WORKFLOW_OPERATION_RELATIONSHIP_MISSING", "/relationships", `Workflow must orchestrate declared Operation:${operationId}`);
    }
  }
  for (const operationId of observed) {
    if (!required.has(operationId)) {
      fail("MTCLI_WORKFLOW_OPERATION_RELATIONSHIP_UNDECLARED", "/relationships", `orchestrated Operation is absent from Workflow steps and compensations:${operationId}`);
    }
  }
}

interface NodeRecord extends DecodedEndpoint {
  readonly body: Record<string, unknown>;
  readonly decoded_body: DecodedBody | null;
  readonly relative_path: string;
}

function readNodes(projectRoot: string, manifest: SourceManifestV1): Map<string, NodeRecord> {
  const nodes = new Map<string, NodeRecord>();
  for (const source of manifest.sources.filter((entry) => entry.source_type === "node")) {
    const value = readBoundJson(projectRoot, manifest, source.relative_path);
    exactKeys(value, ["schema_version", "node_id", "feature_id", "kind", "body"], `/${source.relative_path}`);
    if (typeof value.feature_id !== "string" || typeof value.node_id !== "string" || typeof value.kind !== "string" || !isObject(value.body)) {
      fail("MTCLI_INPUT_SCHEMA", `/${source.relative_path}`, "invalid node source");
    }
    const decodedBody = BODY_CONTRACTS[value.kind]
      ? decodeBody(value.kind, value.body, `/${source.relative_path}/body`)
      : null;
    nodes.set(`${value.feature_id}:${value.node_id}`, {
      feature_id: value.feature_id,
      node_id: value.node_id,
      kind: value.kind,
      body: value.body,
      decoded_body: decodedBody,
      relative_path: source.relative_path,
    });
  }
  return nodes;
}

function endpoint(nodes: Map<string, NodeRecord>, featureId: unknown, nodeId: unknown, pointer: string): NodeRecord {
  if (typeof featureId !== "string" || typeof nodeId !== "string") fail("MTCLI_RELATIONSHIP_ENDPOINT", pointer, "invalid endpoint identity");
  const result = nodes.get(`${featureId}:${nodeId}`);
  if (!result) fail("MTCLI_RELATIONSHIP_ENDPOINT", pointer, "endpoint node is missing");
  return result;
}

const DUPLICATE_REJECTING_RELATIONSHIPS = new Set(["creates", "orchestrates", "produces", "emits"]);

function validateRelationshipGraph(edges: readonly DecodedRelationship[]): void {
  const propositions = new Map<string, DecodedRelationship>();
  for (const edge of edges) {
    if (!DUPLICATE_REJECTING_RELATIONSHIPS.has(edge.relationship)) continue;
    const key = `${edge.scope}\u0000${edge.relationship}\u0000${edge.source.feature_id}:${edge.source.node_id}\u0000${edge.target.feature_id}:${edge.target.node_id}`;
    const prior = propositions.get(key);
    if (prior) fail("MTCLI_RELATIONSHIP_DUPLICATE", `/relationships/${edge.edge_id}`, `duplicate ${edge.relationship} proposition conflicts with ${prior.edge_id}`);
    propositions.set(key, edge);
  }

  const creates = edges.filter((edge) => edge.relationship === "creates");
  const outgoing = new Map<string, DecodedRelationship>();
  const incoming = new Map<string, DecodedRelationship>();
  for (const edge of creates) {
    const sourceKey = `${edge.source.feature_id}:${edge.source.node_id}`;
    const targetKey = `${edge.target.feature_id}:${edge.target.node_id}`;
    const priorOutgoing = outgoing.get(sourceKey);
    if (priorOutgoing) fail("MTCLI_RELATIONSHIP_MULTIPLICITY", `/relationships/${edge.edge_id}`, `creates source already targets ${priorOutgoing.target.feature_id}:${priorOutgoing.target.node_id}`);
    const priorIncoming = incoming.get(targetKey);
    if (priorIncoming) fail("MTCLI_RELATIONSHIP_MULTIPLICITY", `/relationships/${edge.edge_id}`, `creates target already has source ${priorIncoming.source.feature_id}:${priorIncoming.source.node_id}`);
    outgoing.set(sourceKey, edge);
    incoming.set(targetKey, edge);
  }

  const owns = new Map<string, DecodedRelationship>();
  for (const edge of edges.filter((candidate) => candidate.relationship === "owns")) {
    const sourceKey = `${edge.source.feature_id}:${edge.source.node_id}`;
    const targetKey = `${edge.target.feature_id}:${edge.target.node_id}`;
    owns.set(`${sourceKey}\u0000${targetKey}`, edge);
  }
  for (const edge of edges.filter((candidate) => candidate.relationship === "belongs-to")) {
    const sourceKey = `${edge.source.feature_id}:${edge.source.node_id}`;
    const targetKey = `${edge.target.feature_id}:${edge.target.node_id}`;
    const collapsed = owns.get(`${targetKey}\u0000${sourceKey}`);
    if (collapsed) {
      fail(
        "MTCLI_RELATIONSHIP_INVERSE_COLLAPSE",
        `/relationships/${edge.edge_id}`,
        `belongs-to cannot restate owns inverse:${collapsed.edge_id}`,
      );
    }
  }
}

function decodeProjectEdges(projectRoot: string, manifest: SourceManifestV1, nodes: Map<string, NodeRecord>): readonly DecodedRelationship[] {
  const result: DecodedRelationship[] = [];
  for (const source of manifest.sources.filter((entry) => entry.source_type === "feature-edge" || entry.source_type === "project-edge")) {
    const value = readBoundJson(projectRoot, manifest, source.relative_path);
    const isFeature = source.source_type === "feature-edge";
    const sourceEndpoint = isFeature
      ? endpoint(nodes, value.feature_id, value.source_node_id, `/${source.relative_path}/source`)
      : endpoint(nodes, value.source_feature_id, value.source_node_id, `/${source.relative_path}/source`);
    const targetEndpoint = isFeature
      ? endpoint(nodes, value.feature_id, value.target_node_id, `/${source.relative_path}/target`)
      : endpoint(nodes, value.target_feature_id, value.target_node_id, `/${source.relative_path}/target`);
    if (typeof value.relationship !== "string" || typeof value.edge_id !== "string") fail("MTCLI_RELATIONSHIP_SCHEMA", `/${source.relative_path}`, "invalid relationship source");
    const deprecated = deprecatedRelationship(value.relationship);
    if (deprecated) fail("MTCLI_RELATIONSHIP_DEPRECATED", `/${source.relative_path}/relationship`, `deprecated relationship:${value.relationship}; use ${deprecated.replacement}`);
    const generatedView = generatedRelationshipView(value.relationship);
    if (generatedView) fail("MTCLI_RELATIONSHIP_GENERATED_VIEW", `/${source.relative_path}/relationship`, `generated view ${value.relationship} cannot be authored; author ${generatedView.from_signature}`);
    const signature = relationshipSignature(value.relationship);
    if (!signature) fail("MTCLI_RELATIONSHIP_UNKNOWN", `/${source.relative_path}/relationship`, `unknown relationship:${value.relationship}`);
    if (!signature.source_types.includes(sourceEndpoint.kind) || !signature.target_types.includes(targetEndpoint.kind)) {
      fail("MTCLI_RELATIONSHIP_ENDPOINT", `/${source.relative_path}`, `${value.relationship} rejects ${sourceEndpoint.kind}->${targetEndpoint.kind}`);
    }
    const admittedScope = isFeature
      ? signature.feature_scope.some((scope) => scope === "same-feature" || scope === "ui" || scope === "ui-backend")
      : signature.feature_scope.includes("cross-feature");
    if (!admittedScope) fail("MTCLI_RELATIONSHIP_SCOPE", `/${source.relative_path}`, `${value.relationship} rejects ${isFeature ? "same-feature" : "cross-feature"} scope`);
    result.push(Object.freeze({
      edge_id: value.edge_id,
      relationship: value.relationship,
      scope: isFeature ? "feature" : "project",
      source: Object.freeze({ feature_id: sourceEndpoint.feature_id, node_id: sourceEndpoint.node_id, kind: sourceEndpoint.kind }),
      target: Object.freeze({ feature_id: targetEndpoint.feature_id, node_id: targetEndpoint.node_id, kind: targetEndpoint.kind }),
    }));
  }
  const sorted = Object.freeze(result.sort((left, right) => left.edge_id.localeCompare(right.edge_id)));
  validateRelationshipGraph(sorted);
  return sorted;
}

function relationshipsFor(selector: string, relationships: readonly DecodedRelationship[]): readonly DecodedRelationship[] {
  return Object.freeze(relationships.filter((relationship) =>
    `${relationship.source.feature_id}:${relationship.source.node_id}` === selector ||
    `${relationship.target.feature_id}:${relationship.target.node_id}` === selector
  ));
}

function validateBackendRelationshipClosures(
  projectRoot: string,
  projectId: string,
  manifest: SourceManifestV1,
  nodes: Map<string, NodeRecord>,
  relationships: readonly DecodedRelationship[],
): void {
  for (const [selector, node] of nodes) {
    if (!["Entity", "Value Object", "Enum", "Event", "Interface", "Workflow", "State Machine"].includes(node.kind)) continue;
    if (node.decoded_body === null) fail("MTCLI_INPUT_BODY", `/${node.relative_path}/body`, `${node.kind} body was not decoded`);
    const body = node.decoded_body;
    const hasTypedContract = body.typed_contract !== undefined;
    const fieldSets: readonly (readonly FieldSpec[])[] = hasTypedContract
      ? []
      : node.kind === "Entity" || node.kind === "Value Object"
      ? [body.fields as readonly FieldSpec[]]
      : node.kind === "Event"
        ? [[body.occurrence_id as FieldSpec], body.payload as readonly FieldSpec[]]
        : node.kind === "Interface"
          ? (body.operations as readonly InterfaceOperationSpec[]).flatMap(({ request, result }) => [request, result])
          : [];
    for (const fields of fieldSets) for (const [index, field] of fields.entries()) {
      if (field.type_ref.kind !== "reference") continue;
      const target = nodes.get(field.type_ref.selector);
      if (!target || !["Entity", "Value Object", "Enum", "Event"].includes(target.kind)) {
        fail("MTCLI_TYPE_REFERENCE", `/${node.relative_path}/body/fields/${index}/type_ref`, "typed reference must resolve to an Entity, Value Object, Enum, or Event node");
      }
    }
    if (node.kind === "Value Object" && !hasTypedContract) for (const [index, invariantRef] of (body.invariant_refs as readonly string[]).entries()) {
      const invariant = nodes.get(invariantRef);
      if (!invariant || invariant.kind !== "Rule") fail("MTCLI_VALUE_OBJECT_INVARIANT_REFERENCE", `/${node.relative_path}/body/invariant_refs/${index}`, "invariant reference must resolve to a Rule node");
    }
    if (node.kind === "Event" && body.event_type !== node.node_id) {
      fail("MTCLI_EVENT_TYPE", `/${node.relative_path}/body/event_type`, "event_type must equal the Event node identity");
    }
    if (node.kind === "Interface") for (const [index, operation] of (body.operations as readonly InterfaceOperationSpec[]).entries()) {
      const target = nodes.get(operation.operation_ref);
      if (!target || !["Operation", "Query"].includes(target.kind)) {
        fail("MTCLI_INTERFACE_OPERATION_REFERENCE", `/${node.relative_path}/body/operations/${index}/operation_ref`, "Interface operation reference must resolve to an Operation or Query node");
      }
    }
    if (node.kind === "State Machine") {
      for (const [index, transition] of (node.decoded_body.transitions as readonly StateTransitionSpec[]).entries()) {
        if (transition.guard_ref !== null) {
          const guard = nodes.get(transition.guard_ref);
          if (!guard || guard.kind !== "Rule") fail("MTCLI_STATE_MACHINE_GUARD_REFERENCE", `/${node.relative_path}/body/transitions/${index}/guard_ref`, "guard reference must resolve to a Rule node");
        }
        if (transition.effect_event_ref !== null) {
          const event = nodes.get(transition.effect_event_ref);
          if (!event || event.kind !== "Event") fail("MTCLI_STATE_MACHINE_EVENT_REFERENCE", `/${node.relative_path}/body/transitions/${index}/effect_event_ref`, "effect reference must resolve to an Event node");
        }
      }
    }
    if (!["Workflow", "State Machine", "Interface"].includes(node.kind)) continue;
    validateSelectedNodeRelationships(Object.freeze({
      project_root: projectRoot,
      project_id: projectId,
      feature_id: node.feature_id,
      node_id: node.node_id,
      kind: node.kind,
      meta_type_id: metaTypeIdForLabel(node.kind),
      body,
      relationships: relationshipsFor(selector, relationships),
      source_manifest: manifest,
      typed_closure: null,
    }));
  }
}

interface DecodedProjectModel {
  readonly project_root: string;
  readonly source_manifest: SourceManifestV1;
  readonly nodes: Map<string, NodeRecord>;
  readonly relationships: readonly DecodedRelationship[];
}

function decodeProjectModel(projectRoot: unknown): DecodedProjectModel {
  const manifest = resolveProjectRoot(projectRoot);
  const root = fs.realpathSync(String(projectRoot));
  const nodes = readNodes(root, manifest);
  const relationships = decodeProjectEdges(root, manifest, nodes);
  validateBackendRelationshipClosures(root, manifest.project_id, manifest, nodes, relationships);
  return Object.freeze({ project_root: root, source_manifest: manifest, nodes, relationships });
}

export function validateProjectRoot(projectRoot: unknown): SourceManifestV1 {
  return decodeProjectModel(projectRoot).source_manifest;
}

export function loadCompiledProjectGraph(projectRoot: unknown): CompiledProjectGraph {
  const model = decodeProjectModel(projectRoot);
  const nodes = [...model.nodes.values()]
    .map((node): CompiledProjectGraphNode => {
      const selector = `${node.feature_id}:${node.node_id}`;
      const generatedRelationshipProjections: Record<string, readonly string[]> = {};
      const authoredForbiddenProjectionAttributes: string[] = [];
      for (const signature of RELATIONSHIP_SIGNATURES) {
        const projection = signature.generated_source_projection;
        if (!projection || !signature.source_types.includes(node.kind)) continue;
        if (Object.hasOwn(node.body, projection.attribute)) authoredForbiddenProjectionAttributes.push(projection.attribute);
        const targets = model.relationships
          .filter((relationship) =>
            relationship.relationship === signature.id &&
            `${relationship.source.feature_id}:${relationship.source.node_id}` === selector
          )
          .map(({ target }) => `${target.feature_id}:${target.node_id}`)
          .sort();
        generatedRelationshipProjections[projection.attribute] = Object.freeze(targets);
      }
      return Object.freeze({
        feature_id: node.feature_id,
        node_id: node.node_id,
        selector,
        kind: node.kind,
        meta_type_id: metaTypeIdForLabel(node.kind),
        body: withGeneratedRelationshipProjections(
          node.kind,
          node.feature_id,
          node.node_id,
          node.decoded_body ?? Object.freeze(node.body as DecodedBody),
          model.relationships,
        ),
        generated_relationship_projections: Object.freeze(generatedRelationshipProjections),
        authored_forbidden_projection_attributes: Object.freeze(authoredForbiddenProjectionAttributes.sort()),
      });
    })
    .sort((left, right) => left.selector.localeCompare(right.selector));
  return Object.freeze({
    schema_version: "domainspec.compiled-project-graph/v1-candidate",
    project_root: model.project_root,
    project_id: model.source_manifest.project_id,
    source_manifest: model.source_manifest,
    nodes: Object.freeze(nodes),
    relationships: model.relationships,
    authority_effect: "none",
  });
}

export function withGeneratedRelationshipProjections(
  kind: string,
  featureId: string,
  nodeId: string,
  body: DecodedBody,
  relationships: readonly DecodedRelationship[],
): DecodedBody {
  const compiled: Record<string, unknown> = { ...body };
  const selector = `${featureId}:${nodeId}`;
  for (const signature of RELATIONSHIP_SIGNATURES) {
    const projection = signature.generated_source_projection;
    if (!projection || !signature.source_types.includes(kind)) continue;
    const targets = relationships
      .filter((relationship) =>
        relationship.relationship === signature.id &&
        `${relationship.source.feature_id}:${relationship.source.node_id}` === selector
      )
      .map(({ target }) => `${target.feature_id}.${target.node_id}`)
      .sort();
    if (targets.length > 0) compiled[projection.attribute] = Object.freeze(targets);
  }
  return Object.freeze(compiled);
}

export function loadProjectNode(projectRoot: unknown, selector: unknown): DecodedProjectNode {
  if (typeof selector !== "string") fail("MTCLI_INPUT_SELECTOR", "/node", "node selector must be feature-id:node-id");
  const match = SELECTOR_PATTERN.exec(selector);
  if (!match) fail("MTCLI_INPUT_SELECTOR", "/node", "node selector must be feature-id:node-id");
  const model = decodeProjectModel(projectRoot);
  const manifest = model.source_manifest;
  const root = model.project_root;
  const nodes = model.nodes;
  const selected = nodes.get(selector);
  if (!selected) fail("MTCLI_INPUT_MISSING", "/node", `selected node is missing:${selector}`);
  const metaTypeId = metaTypeIdForLabel(selected.kind);
  const body = selected.decoded_body ?? decodeBody(selected.kind, selected.body, `/${selected.relative_path}/body`);
  const projectRelationships = model.relationships;
  const selectedTypedContract = body.typed_contract;
  const closureSources: TypedClosureSourceNode[] = [];
  if (selectedTypedContract !== undefined) {
    for (const candidate of nodes.values()) {
      const candidateBody = candidate.decoded_body ?? decodeBody(candidate.kind, candidate.body, `/${candidate.relative_path}/body`);
      closureSources.push(Object.freeze({
        feature_id: candidate.feature_id,
        node_id: candidate.node_id,
        kind: candidate.kind,
        typed_contract: (candidateBody.typed_contract ?? null) as TypedClosureSourceNode["typed_contract"],
      }));
    }
  }
  const typedClosure = selectedTypedContract === undefined ? null : compileTypedOperationClosure(selector, closureSources, projectRelationships);
  const node = Object.freeze({
    project_root: root,
    project_id: manifest.project_id,
    feature_id: match[1] as string,
    node_id: match[2] as string,
    kind: selected.kind,
    meta_type_id: metaTypeId,
    body,
    relationships: relationshipsFor(selector, projectRelationships),
    source_manifest: manifest,
    typed_closure: typedClosure,
  });
  validateSelectedNodeRelationships(node);
  return node;
}
