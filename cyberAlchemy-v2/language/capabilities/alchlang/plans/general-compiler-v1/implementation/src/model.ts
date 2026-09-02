export const LEAF_NODES = ["fact_ref", "literal", "entity_ref", "actor_ref", "state_ref"] as const;
export const UNARY_OPERATORS = ["not", "exists", "absent"] as const;
export const BINARY_OPERATORS = ["eq", "neq", "lt", "lte", "gt", "gte", "in", "contains", "and", "or"] as const;

export type ScalarType = "string" | "integer" | "decimal" | "boolean" | "identifier" | "timestamp" | "duration" | "enum" | "reference" | "list" | "record";
export type Expression =
  | { node: "fact_ref" | "entity_ref" | "actor_ref" | "state_ref"; ref: string }
  | { node: "literal"; value_type: ScalarType; value: unknown }
  | { operator: string; operands: Expression[] };

export interface CompilerIssue {
  code: string;
  path: string;
  message: string;
}

export class CompilationRejected extends Error {
  constructor(readonly issues: CompilerIssue[]) {
    super(issues.map((issue) => `${issue.code} at ${issue.path}: ${issue.message}`).join("\n"));
    this.name = "CompilationRejected";
  }
}

export interface NormalizedFact { id: string; type: ScalarType; required: boolean; owner: string }
export interface NormalizedRule { id: string; condition: Expression | { legacy_predicate: string }; owner: string; source_refs: string[] }
export interface NormalizedEvent { id: string; payload_facts: string[]; authority_boundary_ref: string | null }
export interface NormalizedTransition { id: string; subject_ref: string; from_state_ref: string; to_state_ref: string; trigger_ref: string | null; guard_rule_refs: string[]; resulting_event_refs: string[]; authority_boundary_ref: string | null }
export interface NormalizedEffect { id: string; pattern_ref: string; integration_binding_ref: string; write_refs: string[]; event_refs: string[]; guarantee: string; failure_continuation: string; authority_boundary_ref: string }
export interface NormalizedAction { id: string; actor_refs: string[]; subject_refs: string[]; input_facts: string[]; precondition_rule_refs: string[]; permission_refs: string[]; outcome_refs: string[]; performs: Array<{ effect_ref: string; integration_binding_ref: string }>; authority_boundary_ref: string }
export interface NormalizedPermission { id: string; actor_refs: string[]; action_refs: string[]; condition: Expression | { legacy_condition: string }; authority_boundary_ref: string }
export interface NormalizedExample { id: string; kind: string; expected: string; affected_rule_refs: string[] }

export interface NormalizedDomain {
  schema_version: string;
  domain_id: string;
  title: string;
  owners: string[];
  terms: Array<{ id: string; kind: string; meaning: string }>;
  edges: Array<{ id: string; type: string; source: string; target: string }>;
  facts: NormalizedFact[];
  rules: NormalizedRule[];
  events: NormalizedEvent[];
  states: Array<{ id: string; subject_ref: string }>;
  transitions: NormalizedTransition[];
  effects: NormalizedEffect[];
  actions: NormalizedAction[];
  permissions: NormalizedPermission[];
  examples: NormalizedExample[];
  authority_boundaries: string[];
  authority_effect: "none";
  residue: Array<{ code: string; subject_ref: string; owner_route: string; detail: string }>;
  metadata: Record<string, unknown>;
}

export interface CompilationPlan {
  model: NormalizedDomain;
  type_model: Array<{ id: string; fields: NormalizedFact[] }>;
  predicate_model: NormalizedRule[];
  event_contracts: NormalizedEvent[];
  state_machines: Array<{ subject_ref: string; states: string[]; transitions: NormalizedTransition[] }>;
  effect_contracts: NormalizedEffect[];
  action_ports: NormalizedAction[];
  permission_guards: NormalizedPermission[];
  test_obligations: Array<{ id: string; kind: string; expected: string; rule_refs: string[] }>;
  documentation_model: { title: string; term_count: number; rule_count: number; claim_ceiling: string };
  graph_model: { nodes: Array<{ id: string; kind: string }>; edges: Array<{ id: string; type: string; source: string; target: string }> };
  trace_ledger: Array<{ output_ref: string; source_refs: string[] }>;
  unsupported_residue: NormalizedDomain["residue"];
}

export interface CompilationResult {
  plan: CompilationPlan;
  files: Record<string, string>;
  source_digest: string;
  plan_digest: string;
  authority_effect: "none";
}
