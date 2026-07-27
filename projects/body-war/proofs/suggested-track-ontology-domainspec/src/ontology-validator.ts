import { createHash } from "node:crypto";

export const ONTOLOGY_DIAGNOSTIC_CODES = [
  "ONTOLOGY_DUPLICATE_ID",
  "ONTOLOGY_EDGE_TARGET_MISSING",
  "ONTOLOGY_ENTRY_INVALID",
  "ONTOLOGY_EVIDENCE_DIGEST_MISMATCH",
  "ONTOLOGY_EVIDENCE_SOURCE_MISSING",
  "ONTOLOGY_EXECUTABLE_LOGIC_FORBIDDEN",
  "ONTOLOGY_GOVERNANCE_METADATA_MISSING",
  "ONTOLOGY_REQUIRED_ENTRY_MISSING",
  "ONTOLOGY_REQUIRED_RELATION_MISSING",
  "ONTOLOGY_TRANSITION_FORBIDDEN",
] as const;

export type OntologyDiagnosticCode =
  (typeof ONTOLOGY_DIAGNOSTIC_CODES)[number];

export interface OntologyDiagnostic {
  code: OntologyDiagnosticCode;
  path: string;
  message: string;
}

export interface OntologyEvidence {
  source: string;
  selector: string;
  sha256: string;
}

export interface OntologyEntry {
  schema_version: "1.0.0";
  id: string;
  kind: "entity" | "operation" | "state";
  label: string;
  definition: string;
  status: "candidate-local";
  evidence: OntologyEvidence[];
  confidence: {
    level: "low" | "medium" | "high";
    basis: string;
  };
  next_gate: string;
  contradiction_path: string;
  relations: Array<{
    type: "produces" | "establishes";
    target: string;
  }>;
}

export interface OntologyTransition {
  from: string;
  to: string;
  trigger?: string;
}

export interface OntologyTransitionPolicy {
  schema_version: "1.0.0";
  source: string;
  source_sha256: string;
  allowed_transitions: Array<Pick<OntologyTransition, "from" | "to">>;
}

export interface OntologyValidationResult {
  status: "pass" | "fail";
  diagnostics: OntologyDiagnostic[];
  entry_digests: Array<{ id: string; sha256: string }>;
  entry_set_digest: string;
}

export interface OntologyReceipt {
  schema_version: "1.0.0";
  test_id: "T-ONTOLOGY-001";
  status: "pass";
  ontology_status: "candidate-local";
  authority_effect: "none";
  release_admission: "not-granted";
  entry_digests: Array<{ id: string; sha256: string }>;
  entry_set_digest: string;
  legal_transition: {
    from: string;
    to: string;
    result: "accepted";
  };
  negative_control: {
    from: string;
    to: string;
    result: "rejected";
    diagnostic: "ONTOLOGY_TRANSITION_FORBIDDEN";
  };
  diagnostic_contract: readonly OntologyDiagnosticCode[];
  source_bindings: Array<{ path: string; sha256: string }>;
}

const ENTRY_KEYS = new Set([
  "schema_version",
  "id",
  "kind",
  "label",
  "definition",
  "status",
  "evidence",
  "confidence",
  "next_gate",
  "contradiction_path",
  "relations",
]);

const GOVERNANCE_KEYS = [
  "status",
  "evidence",
  "confidence",
  "next_gate",
  "contradiction_path",
] as const;

const REQUIRED_ENTRY_IDS = [
  "body-war.ontology.CreateSuggestedTrack",
  "body-war.ontology.SuggestedTrack",
  "body-war.ontology.SuggestedTrackStatus.needs_evidence",
] as const;

const FORBIDDEN_LOGIC_KEYS = new Set([
  "body.logic",
  "bodyLogic",
  "clauses",
  "expression",
  "predicate",
  "quantifier",
]);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function hasNonEmptyString(
  value: Record<string, unknown>,
  key: string,
): boolean {
  return typeof value[key] === "string" && value[key]!.length > 0;
}

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value
      .map(canonicalize)
      .sort((left, right) =>
        JSON.stringify(left).localeCompare(JSON.stringify(right)),
      );
  }
  if (isRecord(value)) {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalize(value[key])]),
    );
  }
  return value;
}

export function renderDeterministicJson(value: unknown): string {
  return `${JSON.stringify(canonicalize(value), null, 2)}\n`;
}

export function sha256Canonical(value: unknown): string {
  return createHash("sha256")
    .update(JSON.stringify(canonicalize(value)))
    .digest("hex");
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

function validateGovernanceMetadata(
  entry: Record<string, unknown>,
  path: string,
): OntologyDiagnostic[] {
  const diagnostics: OntologyDiagnostic[] = [];
  for (const key of GOVERNANCE_KEYS) {
    if (!(key in entry)) {
      diagnostics.push({
        code: "ONTOLOGY_GOVERNANCE_METADATA_MISSING",
        path: `${path}.${key}`,
        message: `Required governance metadata is missing: ${key}`,
      });
    }
  }
  if (entry.status !== "candidate-local") {
    diagnostics.push({
      code: "ONTOLOGY_GOVERNANCE_METADATA_MISSING",
      path: `${path}.status`,
      message: "Local ontology entries must expose status=candidate-local.",
    });
  }
  if (!Array.isArray(entry.evidence) || entry.evidence.length === 0) {
    diagnostics.push({
      code: "ONTOLOGY_GOVERNANCE_METADATA_MISSING",
      path: `${path}.evidence`,
      message: "At least one evidence binding is required.",
    });
  }
  if (
    !isRecord(entry.confidence) ||
    !["low", "medium", "high"].includes(String(entry.confidence.level)) ||
    !hasNonEmptyString(entry.confidence, "basis")
  ) {
    diagnostics.push({
      code: "ONTOLOGY_GOVERNANCE_METADATA_MISSING",
      path: `${path}.confidence`,
      message: "Confidence requires a level and non-empty basis.",
    });
  }
  for (const key of ["next_gate", "contradiction_path"]) {
    if (!hasNonEmptyString(entry, key)) {
      diagnostics.push({
        code: "ONTOLOGY_GOVERNANCE_METADATA_MISSING",
        path: `${path}.${key}`,
        message: `${key} must be a non-empty string.`,
      });
    }
  }
  return diagnostics;
}

function validateEntryShape(
  entry: unknown,
  index: number,
): OntologyDiagnostic[] {
  const path = `entries[${index}]`;
  if (!isRecord(entry)) {
    return [
      {
        code: "ONTOLOGY_ENTRY_INVALID",
        path,
        message: "Entry must be an object.",
      },
    ];
  }

  const diagnostics = validateGovernanceMetadata(entry, path);
  const unknownKeys = Object.keys(entry).filter((key) => !ENTRY_KEYS.has(key));
  if (unknownKeys.length > 0) {
    diagnostics.push({
      code: "ONTOLOGY_ENTRY_INVALID",
      path,
      message: `Closed entry schema rejected keys: ${unknownKeys.sort().join(", ")}`,
    });
  }

  const scalarValid =
    entry.schema_version === "1.0.0" &&
    hasNonEmptyString(entry, "id") &&
    /^body-war\.ontology\.[A-Za-z0-9._-]+$/.test(String(entry.id)) &&
    ["entity", "operation", "state"].includes(String(entry.kind)) &&
    hasNonEmptyString(entry, "label") &&
    hasNonEmptyString(entry, "definition") &&
    Array.isArray(entry.relations);
  if (!scalarValid) {
    diagnostics.push({
      code: "ONTOLOGY_ENTRY_INVALID",
      path,
      message: "Entry scalar fields or relations do not match schema v1.",
    });
  }

  if (Array.isArray(entry.evidence)) {
    for (const [evidenceIndex, evidence] of entry.evidence.entries()) {
      if (
        !isRecord(evidence) ||
        Object.keys(evidence).some(
          (key) => !["source", "selector", "sha256"].includes(key),
        ) ||
        !hasNonEmptyString(evidence, "source") ||
        !hasNonEmptyString(evidence, "selector") ||
        !/^[a-f0-9]{64}$/.test(String(evidence.sha256))
      ) {
        diagnostics.push({
          code: "ONTOLOGY_ENTRY_INVALID",
          path: `${path}.evidence[${evidenceIndex}]`,
          message: "Evidence must bind source, selector, and sha256.",
        });
      }
    }
  }

  if (Array.isArray(entry.relations)) {
    for (const [relationIndex, relation] of entry.relations.entries()) {
      if (
        !isRecord(relation) ||
        Object.keys(relation).some(
          (key) => !["type", "target"].includes(key),
        ) ||
        !["produces", "establishes"].includes(String(relation.type)) ||
        !hasNonEmptyString(relation, "target")
      ) {
        diagnostics.push({
          code: "ONTOLOGY_ENTRY_INVALID",
          path: `${path}.relations[${relationIndex}]`,
          message: "Relation must have one admitted type and a target.",
        });
      }
    }
  }

  const forbiddenPath = findForbiddenLogicPath(entry);
  if (forbiddenPath) {
    diagnostics.push({
      code: "ONTOLOGY_EXECUTABLE_LOGIC_FORBIDDEN",
      path: `${path}${forbiddenPath.slice(1)}`,
      message: "Ontology entries cannot contain body.logic or executable logic AST fields.",
    });
  }
  return diagnostics;
}

export function validateTransition(
  transition: OntologyTransition,
  policy: OntologyTransitionPolicy,
): OntologyDiagnostic[] {
  const accepted = policy.allowed_transitions.some(
    (allowed) =>
      allowed.from === transition.from && allowed.to === transition.to,
  );
  if (accepted) return [];
  return [
    {
      code: "ONTOLOGY_TRANSITION_FORBIDDEN",
      path: `transition:${transition.from}->${transition.to}`,
      message: `Transition ${transition.from} -> ${transition.to} is not admitted by the local policy.`,
    },
  ];
}

function relationExists(
  entry: OntologyEntry | undefined,
  type: "produces" | "establishes",
  target: string,
): boolean {
  return (
    entry?.relations.some(
      (relation) => relation.type === type && relation.target === target,
    ) ?? false
  );
}

export function validateOntology(input: {
  entries: unknown[];
  transition_policy: OntologyTransitionPolicy;
  declared_transitions: OntologyTransition[];
  source_digests: Readonly<Record<string, string>>;
}): OntologyValidationResult {
  const diagnostics = input.entries.flatMap(validateEntryShape);
  const indexed = new Map<string, OntologyEntry>();

  for (const [index, candidate] of input.entries.entries()) {
    if (!isRecord(candidate) || typeof candidate.id !== "string") continue;
    if (indexed.has(candidate.id)) {
      diagnostics.push({
        code: "ONTOLOGY_DUPLICATE_ID",
        path: `entries[${index}].id`,
        message: `Duplicate ontology entry id: ${candidate.id}`,
      });
      continue;
    }
    indexed.set(candidate.id, candidate as unknown as OntologyEntry);
  }

  for (const id of REQUIRED_ENTRY_IDS) {
    if (!indexed.has(id)) {
      diagnostics.push({
        code: "ONTOLOGY_REQUIRED_ENTRY_MISSING",
        path: "entries",
        message: `Required ontology entry is missing: ${id}`,
      });
    }
  }

  for (const [id, entry] of indexed) {
    if (!Array.isArray(entry.relations)) continue;
    for (const [relationIndex, relation] of entry.relations.entries()) {
      if (isRecord(relation) && typeof relation.target === "string") {
        if (!indexed.has(relation.target)) {
          diagnostics.push({
            code: "ONTOLOGY_EDGE_TARGET_MISSING",
            path: `${id}.relations[${relationIndex}].target`,
            message: `Relation target does not resolve: ${relation.target}`,
          });
        }
      }
    }
    if (!Array.isArray(entry.evidence)) continue;
    for (const [evidenceIndex, evidence] of entry.evidence.entries()) {
      if (!isRecord(evidence) || typeof evidence.source !== "string") continue;
      const actual = input.source_digests[evidence.source];
      if (!actual) {
        diagnostics.push({
          code: "ONTOLOGY_EVIDENCE_SOURCE_MISSING",
          path: `${id}.evidence[${evidenceIndex}]`,
          message: `Evidence source was not supplied: ${evidence.source}`,
        });
      } else if (actual !== evidence.sha256) {
        diagnostics.push({
          code: "ONTOLOGY_EVIDENCE_DIGEST_MISMATCH",
          path: `${id}.evidence[${evidenceIndex}].sha256`,
          message: `Evidence digest is stale for ${evidence.source}`,
        });
      }
    }
  }

  const operation = indexed.get("body-war.ontology.CreateSuggestedTrack");
  const requiredRelations = [
    {
      type: "produces" as const,
      target: "body-war.ontology.SuggestedTrack",
    },
    {
      type: "establishes" as const,
      target: "body-war.ontology.SuggestedTrackStatus.needs_evidence",
    },
  ];
  for (const relation of requiredRelations) {
    if (!relationExists(operation, relation.type, relation.target)) {
      diagnostics.push({
        code: "ONTOLOGY_REQUIRED_RELATION_MISSING",
        path: "body-war.ontology.CreateSuggestedTrack.relations",
        message: `Required relation is missing: ${relation.type} -> ${relation.target}`,
      });
    }
  }

  if (
    input.source_digests[input.transition_policy.source] !==
    input.transition_policy.source_sha256
  ) {
    diagnostics.push({
      code: "ONTOLOGY_EVIDENCE_DIGEST_MISMATCH",
      path: "transition_policy.source_sha256",
      message: `Transition policy source digest is stale for ${input.transition_policy.source}`,
    });
  }

  for (const transition of input.declared_transitions) {
    diagnostics.push(...validateTransition(transition, input.transition_policy));
  }

  const sortableEntries = [...indexed.values()];
  const entryDigests = sortableEntries
    .map((entry) => ({ id: entry.id, sha256: sha256Canonical(entry) }))
    .sort((left, right) => left.id.localeCompare(right.id));
  const entrySetDigest = sha256Canonical(sortableEntries);
  const sortedDiagnostics = diagnostics.sort((left, right) =>
    `${left.code}:${left.path}:${left.message}`.localeCompare(
      `${right.code}:${right.path}:${right.message}`,
    ),
  );
  return {
    status: sortedDiagnostics.length === 0 ? "pass" : "fail",
    diagnostics: sortedDiagnostics,
    entry_digests: entryDigests,
    entry_set_digest: entrySetDigest,
  };
}

export function buildOntologyReceipt(input: {
  validation: OntologyValidationResult;
  legal_transition: OntologyTransition;
  negative_transition: OntologyTransition;
  negative_diagnostics: OntologyDiagnostic[];
  source_bindings: Array<{ path: string; sha256: string }>;
}): OntologyReceipt {
  if (input.validation.status !== "pass") {
    throw new Error("Cannot emit a passing receipt from failed ontology validation.");
  }
  const transitionDiagnostic = input.negative_diagnostics.find(
    (diagnostic) => diagnostic.code === "ONTOLOGY_TRANSITION_FORBIDDEN",
  );
  if (!transitionDiagnostic) {
    throw new Error("Negative transition did not produce ONTOLOGY_TRANSITION_FORBIDDEN.");
  }
  return {
    schema_version: "1.0.0",
    test_id: "T-ONTOLOGY-001",
    status: "pass",
    ontology_status: "candidate-local",
    authority_effect: "none",
    release_admission: "not-granted",
    entry_digests: input.validation.entry_digests,
    entry_set_digest: input.validation.entry_set_digest,
    legal_transition: {
      from: input.legal_transition.from,
      to: input.legal_transition.to,
      result: "accepted",
    },
    negative_control: {
      from: input.negative_transition.from,
      to: input.negative_transition.to,
      result: "rejected",
      diagnostic: "ONTOLOGY_TRANSITION_FORBIDDEN",
    },
    diagnostic_contract: [...ONTOLOGY_DIAGNOSTIC_CODES],
    source_bindings: [...input.source_bindings].sort((left, right) =>
      left.path.localeCompare(right.path),
    ),
  };
}

