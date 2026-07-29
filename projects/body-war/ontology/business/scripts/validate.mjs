import { createHash } from "node:crypto";
import { readFile, readdir, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const DIAGNOSTIC_CODES = [
  "BWO_BRANCH_INVALID",
  "BWO_COVERAGE_MISSING",
  "BWO_DUPLICATE_CONCEPT_ID",
  "BWO_DUPLICATE_RELATION_ID",
  "BWO_EXECUTABLE_LOGIC_FORBIDDEN",
  "BWO_LIFECYCLE_INVALID",
  "BWO_NODE_INVALID",
  "BWO_NODE_MANIFEST_DRIFT",
  "BWO_PROFILE_INVALID",
  "BWO_RELATION_ENDPOINT_MISSING",
  "BWO_RELATION_INVALID",
  "BWO_RESIDUE_INVALID",
  "BWO_SOURCE_DIGEST_MISMATCH",
  "BWO_SOURCE_MISSING",
  "BWO_TRANSITION_FORBIDDEN",
  "BWO_VALUE_CYCLE_BLOCKED",
] ;

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const repositoryRoot = path.resolve(packageRoot, "../../../..");

const NODE_KEYS = [
  "branch_roles",
  "business_kind",
  "candidate_status",
  "challenge_contract",
  "concept_id",
  "concept_role",
  "confidence",
  "definition",
  "forbidden_collapse",
  "label",
  "owner_route",
  "residue",
  "schema_version",
  "source_refs",
];
const CONFIDENCE_KEYS = [
  "basis",
  "commitment_confidence",
  "evidence_confidence",
];
const CHALLENGE_KEYS = [
  "blocking_questions",
  "challenge_residue_route",
  "challenge_response",
  "contradiction_edges",
  "owner_route",
  "resolution_gate",
  "valid_challenge_modes",
  "validation_edges",
];
const RELATION_KEYS = [
  "authority_effect",
  "cycle_policy",
  "direction",
  "evidence_refs",
  "forbidden_collapse",
  "owner_route",
  "predicate",
  "relation_id",
  "schema_version",
  "source_concept",
  "target_concept",
  "value_effect",
];
const SOURCE_REF_KEYS = ["path", "selector", "sha256"];
const LIFECYCLE_KEYS = [
  "authority_effect",
  "forbidden_collapse",
  "owner_route",
  "policy_id",
  "schema_version",
  "source_refs",
  "state_concepts",
  "subject_concept",
  "transitions",
];
const TRANSITION_KEYS = [
  "from",
  "prototype_availability",
  "to",
  "trigger",
];

const CONCEPT_ROLES = new Set([
  "authority object",
  "evidence object",
  "workflow object",
  "projection object",
  "residue object",
]);
const BUSINESS_KINDS = new Set([
  "actor",
  "bounded_context",
  "capability",
  "entity",
  "value_object",
  "operation",
  "query",
  "event",
  "lifecycle_state",
  "policy",
  "metric",
  "ledger",
  "premise",
  "outcome",
  "external_system",
  "interface",
  "workflow",
]);
const CANDIDATE_STATUSES = new Set([
  "candidate",
  "reviewed-candidate",
  "deferred",
  "blocked",
  "projected",
]);
const CONFIDENCE_LEVELS = new Set(["low", "medium", "high"]);
const CHALLENGE_MODES = new Set([
  "evidence",
  "contradiction",
  "owner_review",
]);
const DIRECTIONS = new Set(["directed", "symmetric", "view-only"]);
const AUTHORITY_EFFECTS = new Set([
  "none",
  "staging",
  "projection",
  "owner-decision",
  "blocked",
]);
const VALUE_EFFECTS = new Set([
  "value-free",
  "value-constraining",
  "unknown",
]);
const CYCLE_POLICIES = new Set([
  "acyclic",
  "cycle-permitted",
  "unknown",
]);
const FORBIDDEN_LOGIC_KEYS = new Set([
  "body.logic",
  "bodyLogic",
  "clauses",
  "expression",
  "predicate_ast",
  "quantifier",
]);

function isRecord(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.length > 0;
}

function exactKeys(value, keys) {
  if (!isRecord(value)) return false;
  return (
    JSON.stringify(Object.keys(value).sort()) ===
    JSON.stringify([...keys].sort())
  );
}

function stringArray(value, { min = 0, allowed } = {}) {
  return (
    Array.isArray(value) &&
    value.length >= min &&
    value.every(
      (item) =>
        isNonEmptyString(item) && (!allowed || allowed.has(item)),
    )
  );
}

function canonicalize(value) {
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

export function renderDeterministicJson(value) {
  return `${JSON.stringify(canonicalize(value), null, 2)}\n`;
}

export function sha256Canonical(value) {
  return createHash("sha256")
    .update(JSON.stringify(canonicalize(value)))
    .digest("hex");
}

async function sha256File(absolutePath) {
  return createHash("sha256")
    .update(await readFile(absolutePath))
    .digest("hex");
}

function diagnostic(code, pathValue, message) {
  return { code, path: pathValue, message };
}

function findForbiddenLogic(value, currentPath = "$") {
  if (Array.isArray(value)) {
    for (const [index, item] of value.entries()) {
      const found = findForbiddenLogic(item, `${currentPath}[${index}]`);
      if (found) return found;
    }
    return undefined;
  }
  if (!isRecord(value)) return undefined;
  for (const [key, item] of Object.entries(value)) {
    if (FORBIDDEN_LOGIC_KEYS.has(key)) return `${currentPath}.${key}`;
    const found = findForbiddenLogic(item, `${currentPath}.${key}`);
    if (found) return found;
  }
  return undefined;
}

function validateSourceRefShape(ref) {
  return (
    exactKeys(ref, SOURCE_REF_KEYS) &&
    isNonEmptyString(ref.path) &&
    isNonEmptyString(ref.selector) &&
    /^[a-f0-9]{64}$/.test(ref.sha256)
  );
}

export function validateNodeShape(node, nodePath = "node") {
  const diagnostics = [];
  if (
    !exactKeys(node, NODE_KEYS) ||
    node.schema_version !== "body-war-business-node/v1" ||
    !/^body-war\.business\.[a-z0-9.-]+$/.test(node.concept_id ?? "") ||
    !isNonEmptyString(node.label) ||
    !isNonEmptyString(node.definition) ||
    !CONCEPT_ROLES.has(node.concept_role) ||
    !BUSINESS_KINDS.has(node.business_kind) ||
    !stringArray(node.branch_roles, { min: 1 }) ||
    node.branch_roles.some((role) => role !== "business") ||
    !Array.isArray(node.source_refs) ||
    node.source_refs.length === 0 ||
    !node.source_refs.every(validateSourceRefShape) ||
    !isNonEmptyString(node.owner_route) ||
    !CANDIDATE_STATUSES.has(node.candidate_status) ||
    !exactKeys(node.confidence, CONFIDENCE_KEYS) ||
    !CONFIDENCE_LEVELS.has(node.confidence?.evidence_confidence) ||
    !CONFIDENCE_LEVELS.has(node.confidence?.commitment_confidence) ||
    !isNonEmptyString(node.confidence?.basis) ||
    !exactKeys(node.challenge_contract, CHALLENGE_KEYS) ||
    !isNonEmptyString(node.challenge_contract?.challenge_response) ||
    !stringArray(node.challenge_contract?.valid_challenge_modes, {
      min: 1,
      allowed: CHALLENGE_MODES,
    }) ||
    !stringArray(node.challenge_contract?.contradiction_edges) ||
    !stringArray(node.challenge_contract?.validation_edges) ||
    !isNonEmptyString(node.challenge_contract?.owner_route) ||
    !isNonEmptyString(node.challenge_contract?.resolution_gate) ||
    !stringArray(node.challenge_contract?.blocking_questions) ||
    !isNonEmptyString(node.challenge_contract?.challenge_residue_route) ||
    !stringArray(node.residue) ||
    !stringArray(node.forbidden_collapse, { min: 1 })
  ) {
    diagnostics.push(
      diagnostic(
        "BWO_NODE_INVALID",
        nodePath,
        "Node does not match the closed Body War candidate node contract.",
      ),
    );
  }
  const forbidden = findForbiddenLogic(node);
  if (forbidden) {
    diagnostics.push(
      diagnostic(
        "BWO_EXECUTABLE_LOGIC_FORBIDDEN",
        `${nodePath}${forbidden.slice(1)}`,
        "Business ontology nodes cannot embed executable logic AST fields.",
      ),
    );
  }
  return diagnostics;
}

export function validateRelationShape(
  relation,
  conceptIds,
  relationPath = "relation",
) {
  const diagnostics = [];
  if (
    !exactKeys(relation, RELATION_KEYS) ||
    relation.schema_version !== "body-war-business-relation/v1" ||
    !/^body-war\.relation\.[a-z0-9.-]+$/.test(relation.relation_id ?? "") ||
    !isNonEmptyString(relation.predicate) ||
    !/^body-war\.business\.[a-z0-9.-]+$/.test(
      relation.source_concept ?? "",
    ) ||
    !/^body-war\.business\.[a-z0-9.-]+$/.test(
      relation.target_concept ?? "",
    ) ||
    !DIRECTIONS.has(relation.direction) ||
    !isNonEmptyString(relation.owner_route) ||
    !Array.isArray(relation.evidence_refs) ||
    relation.evidence_refs.length === 0 ||
    !relation.evidence_refs.every(validateSourceRefShape) ||
    !AUTHORITY_EFFECTS.has(relation.authority_effect) ||
    !VALUE_EFFECTS.has(relation.value_effect) ||
    !CYCLE_POLICIES.has(relation.cycle_policy) ||
    !stringArray(relation.forbidden_collapse, { min: 1 })
  ) {
    diagnostics.push(
      diagnostic(
        "BWO_RELATION_INVALID",
        relationPath,
        "Relation does not match the closed Body War candidate relation contract.",
      ),
    );
    return diagnostics;
  }
  for (const [field, endpoint] of [
    ["source_concept", relation.source_concept],
    ["target_concept", relation.target_concept],
  ]) {
    if (!conceptIds.has(endpoint)) {
      diagnostics.push(
        diagnostic(
          "BWO_RELATION_ENDPOINT_MISSING",
          `${relationPath}.${field}`,
          `Relation endpoint does not exist: ${endpoint}`,
        ),
      );
    }
  }
  if (
    relation.value_effect === "value-constraining" &&
    relation.cycle_policy === "cycle-permitted"
  ) {
    diagnostics.push(
      diagnostic(
        "BWO_VALUE_CYCLE_BLOCKED",
        relationPath,
        "Value-constraining cycle-permitted relation requires explicit schema-governance exception.",
      ),
    );
  }
  return diagnostics;
}

function localStateNames(policy) {
  const prefix = `body-war.business.state.${policy.policy_id
    .replace("body-war.lifecycle.", "")}.`;
  return new Set(
    policy.state_concepts
      .filter((state) => state.startsWith(prefix))
      .map((state) => state.slice(prefix.length)),
  );
}

export function validateTransition(transition, policy) {
  const accepted = policy.transitions.some(
    (allowed) =>
      allowed.from === transition.from && allowed.to === transition.to,
  );
  return accepted
    ? []
    : [
        diagnostic(
          "BWO_TRANSITION_FORBIDDEN",
          `transition:${transition.policy_id}:${transition.from}->${transition.to}`,
          "Transition is not admitted by the named lifecycle policy.",
        ),
      ];
}

function validateLifecycle(policy, conceptIds, policyPath) {
  const diagnostics = [];
  if (
    !exactKeys(policy, LIFECYCLE_KEYS) ||
    policy.schema_version !== "body-war-business-lifecycle-policy/v1" ||
    !/^body-war\.lifecycle\.[a-z0-9.-]+$/.test(policy.policy_id ?? "") ||
    !conceptIds.has(policy.subject_concept) ||
    !stringArray(policy.state_concepts, { min: 1 }) ||
    !policy.state_concepts.every((state) => conceptIds.has(state)) ||
    !Array.isArray(policy.transitions) ||
    policy.transitions.length === 0 ||
    !policy.transitions.every(
      (transition) =>
        exactKeys(transition, TRANSITION_KEYS) &&
        isNonEmptyString(transition.from) &&
        isNonEmptyString(transition.to) &&
        isNonEmptyString(transition.trigger) &&
        new Set([
          "available",
          "fixture-only",
          "blocked",
          "out-of-scope",
        ]).has(transition.prototype_availability),
    ) ||
    !Array.isArray(policy.source_refs) ||
    policy.source_refs.length === 0 ||
    !policy.source_refs.every(validateSourceRefShape) ||
    !isNonEmptyString(policy.owner_route) ||
    policy.authority_effect !== "none" ||
    !stringArray(policy.forbidden_collapse, { min: 1 })
  ) {
    diagnostics.push(
      diagnostic(
        "BWO_LIFECYCLE_INVALID",
        policyPath,
        "Lifecycle policy does not match its closed contract or references missing concepts.",
      ),
    );
    return diagnostics;
  }
  const stateNames = localStateNames(policy);
  for (const [index, transition] of policy.transitions.entries()) {
    if (
      !stateNames.has(transition.from) &&
      !["none", "any-active-state"].includes(transition.from)
    ) {
      diagnostics.push(
        diagnostic(
          "BWO_LIFECYCLE_INVALID",
          `${policyPath}.transitions[${index}].from`,
          `Unknown lifecycle state: ${transition.from}`,
        ),
      );
    }
    if (!stateNames.has(transition.to)) {
      diagnostics.push(
        diagnostic(
          "BWO_LIFECYCLE_INVALID",
          `${policyPath}.transitions[${index}].to`,
          `Unknown lifecycle state: ${transition.to}`,
        ),
      );
    }
  }
  return diagnostics;
}

async function readJson(absolutePath) {
  return JSON.parse(await readFile(absolutePath, "utf8"));
}

async function loadPackage() {
  const [
    profile,
    sources,
    nodeManifest,
    relationSet,
    branch,
    residue,
  ] = await Promise.all([
    readJson(path.join(packageRoot, "profile.json")),
    readJson(path.join(packageRoot, "sources.json")),
    readJson(path.join(packageRoot, "nodes/manifest.json")),
    readJson(path.join(packageRoot, "relations/relations.json")),
    readJson(path.join(packageRoot, "views/business.json")),
    readJson(path.join(packageRoot, "residue.json")),
  ]);

  const nodeNames = (await readdir(path.join(packageRoot, "nodes")))
    .filter((name) => name.endsWith(".json") && name !== "manifest.json")
    .sort();
  const nodes = await Promise.all(
    nodeNames.map((name) => readJson(path.join(packageRoot, "nodes", name))),
  );
  const lifecycleNames = (
    await readdir(path.join(packageRoot, "lifecycle-policies"))
  )
    .filter((name) => name.endsWith(".json"))
    .sort();
  const lifecyclePolicies = await Promise.all(
    lifecycleNames.map((name) =>
      readJson(path.join(packageRoot, "lifecycle-policies", name)),
    ),
  );
  return {
    profile,
    sources,
    nodeManifest,
    relationSet,
    branch,
    residue,
    nodes,
    nodeNames,
    lifecyclePolicies,
    lifecycleNames,
  };
}

async function validateSourceRefs(allRefs, declaredSources) {
  const diagnostics = [];
  const sourceMap = new Map(
    declaredSources.sources.map((source) => [source.path, source.sha256]),
  );
  const checked = new Map();
  for (const [index, ref] of allRefs.entries()) {
    const expected = sourceMap.get(ref.path);
    if (!expected) {
      diagnostics.push(
        diagnostic(
          "BWO_SOURCE_MISSING",
          `source_refs[${index}]`,
          `Source is not declared in sources.json: ${ref.path}`,
        ),
      );
      continue;
    }
    if (expected !== ref.sha256) {
      diagnostics.push(
        diagnostic(
          "BWO_SOURCE_DIGEST_MISMATCH",
          `source_refs[${index}].sha256`,
          `Reference digest disagrees with sources.json for ${ref.path}`,
        ),
      );
      continue;
    }
    if (!checked.has(ref.path)) {
      try {
        checked.set(
          ref.path,
          await sha256File(path.join(repositoryRoot, ref.path)),
        );
      } catch {
        diagnostics.push(
          diagnostic(
            "BWO_SOURCE_MISSING",
            `source_refs[${index}].path`,
            `Bound source does not exist: ${ref.path}`,
          ),
        );
        continue;
      }
    }
    if (checked.get(ref.path) !== ref.sha256) {
      diagnostics.push(
        diagnostic(
          "BWO_SOURCE_DIGEST_MISMATCH",
          `source_refs[${index}].sha256`,
          `Current source bytes do not match bound digest for ${ref.path}`,
        ),
      );
    }
  }
  return { diagnostics, checked };
}

function validateBranch(branch) {
  if (
    !exactKeys(branch, [
      "allowed_readings",
      "branch_id",
      "forbidden_authority_moves",
      "owner_route",
      "residue",
      "schema_version",
      "source_refs",
      "view_role",
    ]) ||
    branch.schema_version !== "body-war-business-branch-view/v1" ||
    branch.branch_id !== "body-war.branch.business" ||
    branch.view_role !== "meaning" ||
    !Array.isArray(branch.source_refs) ||
    branch.source_refs.length === 0 ||
    !branch.source_refs.every(validateSourceRefShape) ||
    !stringArray(branch.allowed_readings, { min: 1 }) ||
    !stringArray(branch.forbidden_authority_moves, { min: 1 }) ||
    !isNonEmptyString(branch.owner_route) ||
    !stringArray(branch.residue)
  ) {
    return [
      diagnostic(
        "BWO_BRANCH_INVALID",
        "views/business.json",
        "Business branch does not match the branch-as-view contract.",
      ),
    ];
  }
  return [];
}

function validateProfile(profile) {
  const valid =
    exactKeys(profile, [
      "authority_effect",
      "branch_id",
      "claim_ceiling",
      "classification_axes",
      "coverage_contract",
      "forbidden_claims",
      "label",
      "model_contracts",
      "model_source_refs",
      "owner_route",
      "package_id",
      "release_admission",
      "schema_version",
      "status",
    ]) &&
    profile.schema_version === "body-war-business-ontology-profile/v1" &&
    profile.package_id === "body-war.business-ontology" &&
    isNonEmptyString(profile.label) &&
    profile.status === "candidate-local" &&
    profile.authority_effect === "none" &&
    profile.release_admission === "not-granted" &&
    profile.branch_id === "body-war.branch.business" &&
    isNonEmptyString(profile.owner_route) &&
    isNonEmptyString(profile.claim_ceiling) &&
    stringArray(profile.model_contracts, { min: 1 }) &&
    Array.isArray(profile.model_source_refs) &&
    profile.model_source_refs.length > 0 &&
    profile.model_source_refs.every(validateSourceRefShape) &&
    isRecord(profile.classification_axes) &&
    isRecord(profile.coverage_contract) &&
    stringArray(profile.forbidden_claims, { min: 1 });
  return valid
    ? []
    : [
        diagnostic(
          "BWO_PROFILE_INVALID",
          "profile.json",
          "Profile does not match the closed candidate-local package boundary.",
        ),
      ];
}

function validateResidue(residue, conceptIds) {
  const valid =
    isRecord(residue) &&
    residue.schema_version === "body-war-business-ontology-residue/v1" &&
    residue.authority_effect === "none" &&
    residue.questions_are_nodes === false &&
    Array.isArray(residue.items) &&
    residue.items.length > 0 &&
    residue.items.every(
      (item) =>
        isRecord(item) &&
        isNonEmptyString(item.residue_id) &&
        ["blocked", "deferred"].includes(item.status) &&
        isNonEmptyString(item.owner_route) &&
        stringArray(item.blocking_questions, { min: 1 }) &&
        isNonEmptyString(item.next_gate) &&
        stringArray(item.affected_concepts, { min: 1 }) &&
        item.affected_concepts.every((id) => conceptIds.has(id)),
    );
  return valid
    ? []
    : [
        diagnostic(
          "BWO_RESIDUE_INVALID",
          "residue.json",
          "Residue must keep questions as fields and reference existing concepts.",
        ),
      ];
}

function validateCoverage(profile, nodes, relations, lifecycles) {
  const diagnostics = [];
  const conceptIds = new Set(nodes.map((node) => node.concept_id));
  const businessKinds = new Set(nodes.map((node) => node.business_kind));
  const predicates = new Set(relations.map((relation) => relation.predicate));
  const policyIds = new Set(lifecycles.map((policy) => policy.policy_id));
  const coverage = profile.coverage_contract;
  const missingKinds = coverage.required_business_kinds.filter(
    (kind) => !businessKinds.has(kind),
  );
  const missingConcepts = coverage.required_concepts.filter(
    (id) => !conceptIds.has(id),
  );
  const missingPredicates = coverage.required_relation_predicates.filter(
    (predicate) => !predicates.has(predicate),
  );
  const missingPolicies = coverage.required_lifecycle_policies.filter(
    (id) => !policyIds.has(id),
  );
  if (
    nodes.length < coverage.minimum_node_count ||
    relations.length < coverage.minimum_relation_count ||
    missingKinds.length ||
    missingConcepts.length ||
    missingPredicates.length ||
    missingPolicies.length
  ) {
    diagnostics.push(
      diagnostic(
        "BWO_COVERAGE_MISSING",
        "profile.json.coverage_contract",
        JSON.stringify({
          node_count: nodes.length,
          relation_count: relations.length,
          missingKinds,
          missingConcepts,
          missingPredicates,
          missingPolicies,
        }),
      ),
    );
  }
  return diagnostics;
}

export async function validateBusinessOntology() {
  const loaded = await loadPackage();
  const diagnostics = [];
  const conceptIds = new Set();
  const relationIds = new Set();

  for (const [index, node] of loaded.nodes.entries()) {
    diagnostics.push(
      ...validateNodeShape(node, `nodes/${loaded.nodeNames[index]}`),
    );
    if (conceptIds.has(node.concept_id)) {
      diagnostics.push(
        diagnostic(
          "BWO_DUPLICATE_CONCEPT_ID",
          `nodes/${loaded.nodeNames[index]}.concept_id`,
          `Duplicate concept ID: ${node.concept_id}`,
        ),
      );
    }
    conceptIds.add(node.concept_id);
  }

  const manifestIds = [...loaded.nodeManifest.concept_ids].sort();
  const actualIds = [...conceptIds].sort();
  if (
    loaded.nodeManifest.node_count !== loaded.nodes.length ||
    JSON.stringify(manifestIds) !== JSON.stringify(actualIds)
  ) {
    diagnostics.push(
      diagnostic(
        "BWO_NODE_MANIFEST_DRIFT",
        "nodes/manifest.json",
        "Node manifest does not match materialized node files.",
      ),
    );
  }

  const relations = loaded.relationSet.relations ?? [];
  if (loaded.relationSet.relation_count !== relations.length) {
    diagnostics.push(
      diagnostic(
        "BWO_RELATION_INVALID",
        "relations/relations.json.relation_count",
        "Declared relation count does not match relation records.",
      ),
    );
  }
  for (const [index, relation] of relations.entries()) {
    diagnostics.push(
      ...validateRelationShape(
        relation,
        conceptIds,
        `relations[${index}]`,
      ),
    );
    if (relationIds.has(relation.relation_id)) {
      diagnostics.push(
        diagnostic(
          "BWO_DUPLICATE_RELATION_ID",
          `relations[${index}].relation_id`,
          `Duplicate relation ID: ${relation.relation_id}`,
        ),
      );
    }
    relationIds.add(relation.relation_id);
  }

  for (const [index, policy] of loaded.lifecyclePolicies.entries()) {
    diagnostics.push(
      ...validateLifecycle(
        policy,
        conceptIds,
        `lifecycle-policies/${loaded.lifecycleNames[index]}`,
      ),
    );
  }
  diagnostics.push(...validateProfile(loaded.profile));
  diagnostics.push(...validateBranch(loaded.branch));
  diagnostics.push(...validateResidue(loaded.residue, conceptIds));
  diagnostics.push(
    ...validateCoverage(
      loaded.profile,
      loaded.nodes,
      relations,
      loaded.lifecyclePolicies,
    ),
  );

  const allRefs = [
    ...(loaded.profile.model_source_refs ?? []),
    ...loaded.nodes.flatMap((node) => node.source_refs ?? []),
    ...relations.flatMap((relation) => relation.evidence_refs ?? []),
    ...loaded.lifecyclePolicies.flatMap(
      (policy) => policy.source_refs ?? [],
    ),
    ...(loaded.branch.source_refs ?? []),
  ];
  const sourceValidation = await validateSourceRefs(
    allRefs,
    loaded.sources,
  );
  diagnostics.push(...sourceValidation.diagnostics);

  return {
    status: diagnostics.length === 0 ? "pass" : "fail",
    diagnostics,
    counts: {
      nodes: loaded.nodes.length,
      relations: relations.length,
      lifecycle_policies: loaded.lifecyclePolicies.length,
      residue_items: loaded.residue.items?.length ?? 0,
      sources: loaded.sources.sources.length,
    },
    digests: {
      profile: sha256Canonical(loaded.profile),
      node_set: sha256Canonical(loaded.nodes),
      relation_set: sha256Canonical(relations),
      lifecycle_set: sha256Canonical(loaded.lifecyclePolicies),
      branch_view: sha256Canonical(loaded.branch),
      residue: sha256Canonical(loaded.residue),
    },
    source_bindings: [...sourceValidation.checked.entries()]
      .map(([sourcePath, sha256]) => ({ path: sourcePath, sha256 }))
      .sort((a, b) => a.path.localeCompare(b.path)),
    loaded,
  };
}

export function buildReceipt(validation, negativeControls) {
  if (validation.status !== "pass") {
    throw new Error("Cannot build a passing receipt from failed validation.");
  }
  return {
    schema_version: "body-war-business-ontology-receipt/v1",
    test_id: "T-BWO-001",
    status: "pass",
    ontology_status: "candidate-local",
    authority_effect: "none",
    release_admission: "not-granted",
    claim_ceiling:
      "Validated source-bound business meaning graph; no DomainSpec, runtime, promotion, or production effect.",
    counts: validation.counts,
    digests: validation.digests,
    diagnostic_contract: DIAGNOSTIC_CODES,
    negative_controls: negativeControls,
    source_bindings: validation.source_bindings,
  };
}

async function main() {
  const validation = await validateBusinessOntology();
  if (validation.status !== "pass") {
    process.stderr.write(
      `${renderDeterministicJson({
        status: validation.status,
        diagnostics: validation.diagnostics,
      })}`,
    );
    process.exitCode = 1;
    return;
  }
  const legal = await readJson(
    path.join(packageRoot, "fixtures/valid/legal-transition.json"),
  );
  const invalid = await readJson(
    path.join(
      packageRoot,
      "fixtures/invalid/direct-promotion-transition.json",
    ),
  );
  const lifecycle = validation.loaded.lifecyclePolicies.find(
    (policy) => policy.policy_id === legal.policy_id,
  );
  const legalDiagnostics = validateTransition(legal, lifecycle);
  const invalidDiagnostics = validateTransition(invalid, lifecycle);
  const negativeControls = {
    legal_transition: {
      policy_id: legal.policy_id,
      from: legal.from,
      to: legal.to,
      result: legalDiagnostics.length === 0 ? "accepted" : "rejected",
    },
    direct_promotion: {
      policy_id: invalid.policy_id,
      from: invalid.from,
      to: invalid.to,
      result: invalidDiagnostics.length === 0 ? "accepted" : "rejected",
      diagnostic: invalidDiagnostics[0]?.code,
    },
  };
  if (
    negativeControls.legal_transition.result !== "accepted" ||
    negativeControls.direct_promotion.result !== "rejected"
  ) {
    throw new Error("Lifecycle negative controls did not hold.");
  }
  const receipt = buildReceipt(validation, negativeControls);
  const receiptPath = path.join(
    packageRoot,
    "receipts/validation-receipt.json",
  );
  await mkdir(path.dirname(receiptPath), { recursive: true });
  await writeFile(receiptPath, renderDeterministicJson(receipt));
  process.stdout.write(
    `${renderDeterministicJson({
      status: validation.status,
      counts: validation.counts,
      receipt: path.relative(repositoryRoot, receiptPath),
    })}`,
  );
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  await main();
}
