import { CompilationRejected, type CompilerIssue, type Expression, type ScalarType } from "./model.js";
import { parsePredicate } from "./predicate-parser.js";

type Row = { line: number; text: string };
type Section = { kind: string; id: string; rows: Row[]; line: number };

export interface ParsedDomainSource { carrier: Record<string, unknown>; source_kind: "markdown-alchlang" | "plain-alchlang" }

function extractSource(markdown: string): { text: string; source_kind: ParsedDomainSource["source_kind"] } {
  const blocks = [...markdown.matchAll(/```alchlang\s*\n([\s\S]*?)```/g)];
  if (blocks.length > 1) throw new CompilationRejected([{ code: "SOURCE_BLOCK_COUNT", path: "$", message: "expected exactly one alchlang code block" }]);
  if (blocks.length === 1) return { text: blocks[0][1], source_kind: "markdown-alchlang" };
  if (markdown.includes("```")) throw new CompilationRejected([{ code: "SOURCE_BLOCK_COUNT", path: "$", message: "Markdown code fence must be labelled alchlang" }]);
  return { text: markdown, source_kind: "plain-alchlang" };
}

const words = (value: string): string[] => value.split(",").map((item) => item.trim()).filter(Boolean);
const scalarTypes = new Set<ScalarType>(["string", "integer", "decimal", "boolean", "identifier", "timestamp", "duration", "enum", "reference", "list", "record"]);

export function parseDomainSource(markdown: string): ParsedDomainSource {
  const extracted = extractSource(markdown);
  const rows = extracted.text.split(/\r?\n/).map((text, index) => ({ line: index + 1, text: text.replace(/\s+$/, "") })).filter((row) => row.text.trim() && !row.text.trimStart().startsWith("#"));
  const issues: CompilerIssue[] = [];
  let domainId = ""; let title = ""; let owner = "";
  const sections: Section[] = [];
  let current: Section | null = null;
  let latestEntity = ""; let anonymousRule = 0;
  for (const row of rows) {
    if (/^\s/.test(row.text)) {
      if (!current) issues.push({ code: "TEXT_SYNTAX", path: `$line:${row.line}`, message: "indented line without a section" });
      else current.rows.push({ line: row.line, text: row.text.trim() });
      continue;
    }
    const domain = /^domain\s+([A-Za-z_][\w.-]*)(?:\s+"([^"]+)")?$/.exec(row.text);
    if (domain) { domainId = domain[1]; title = domain[2] ?? domain[1]; current = null; continue; }
    const ownerMatch = /^owner\s+([A-Za-z_][\w.-]*)$/.exec(row.text);
    if (ownerMatch) { owner = ownerMatch[1]; current = null; continue; }
    const header = /^(entity|actor|states|rule|boundary|permission|action|effect|event|example)\s+([A-Za-z_][\w.-]*):?$/.exec(row.text);
    if (header) { current = { kind: header[1], id: header[2], rows: [], line: row.line }; sections.push(current); if (header[1] === "entity") latestEntity = header[2]; continue; }
    if (/^states?:$/.test(row.text) && latestEntity) { current = { kind: "states", id: latestEntity, rows: [], line: row.line }; sections.push(current); continue; }
    if (row.text === "rule:") { current = { kind: "rule", id: `anonymous-rule-${++anonymousRule}`, rows: [], line: row.line }; sections.push(current); continue; }
    issues.push({ code: "TEXT_SYNTAX", path: `$line:${row.line}`, message: `unsupported declaration ${JSON.stringify(row.text)}` });
  }
  if (!domainId) issues.push({ code: "TEXT_REQUIRED", path: "$", message: "missing: domain <id> \"<title>\"" });
  if (!owner) issues.push({ code: "MISSING_OWNER", path: "$", message: "missing explicit owner <route>" });

  const terms: any[] = []; const facts: any[] = []; const states: any[] = []; const transitions: any[] = [];
  const rules: any[] = []; const actions: any[] = []; const effects: any[] = []; const permissions: any[] = []; const events: any[] = []; const examples: any[] = []; const boundaries: any[] = []; const edges: any[] = [];
  const factTypes = new Map<string, ScalarType>();

  for (const section of sections.filter((item) => item.kind === "entity")) {
    terms.push({ term_id: section.id, kind: "entity", meaning: `Declared entity ${section.id}.` });
    for (const row of section.rows) {
      const field = /^([A-Za-z_][\w.-]*):\s*(\w+)(?:\s+(required|optional))?$/.exec(row.text);
      if (!field || !scalarTypes.has(field[2] as ScalarType)) { issues.push({ code: "TEXT_FIELD", path: `$line:${row.line}`, message: "expected field: <type> [required|optional]" }); continue; }
      const type = field[2] as ScalarType; factTypes.set(field[1], type);
      facts.push({ fact_id: field[1], type, required: field[3] !== "optional", owner_route: owner });
    }
  }
  for (const section of sections.filter((item) => item.kind === "actor")) {
    if (section.rows.length) issues.push({ code: "TEXT_ACTOR", path: `$line:${section.line}`, message: "actor declarations have no body" });
    terms.push({ term_id: section.id, kind: "actor", meaning: `Declared actor ${section.id}.` });
  }
  for (const section of sections.filter((item) => item.kind === "states")) {
    let initial = "";
    for (const row of section.rows) {
      const initialMatch = /^initial\s+([A-Za-z_][\w.-]*)$/.exec(row.text);
      if (initialMatch) { initial = initialMatch[1]; continue; }
      const transition = /^([A-Za-z_][\w.-]*)\s*->\s*([A-Za-z_][\w.-]*)(?:\s+when\s+([A-Za-z_][\w.-]*))?(?:\s+emits\s+([A-Za-z_][\w.-]*))?$/.exec(row.text);
      if (!transition) { issues.push({ code: "TEXT_TRANSITION", path: `$line:${row.line}`, message: "expected <from> -> <to> [when <rule>] [emits <event>]" }); continue; }
      for (const state of [transition[1], transition[2]]) if (!states.some((item) => item.state_id === state && item.subject_ref === section.id)) states.push({ state_id: state, subject_ref: section.id });
      transitions.push({ transition_id: `${section.id}-${transition[1]}-${transition[2]}`, subject_ref: section.id, from_state_ref: transition[1], to_state_ref: transition[2], trigger_ref: null, guard_rule_refs: transition[3] ? [transition[3]] : [], authority_boundary_ref: null, resulting_event_refs: transition[4] ? [transition[4]] : [] });
    }
    if (initial && !states.some((item) => item.state_id === initial && item.subject_ref === section.id)) states.push({ state_id: initial, subject_ref: section.id });
    for (const state of states.filter((item) => item.subject_ref === section.id)) if (!terms.some((term) => term.term_id === state.state_id)) terms.push({ term_id: state.state_id, kind: "state", meaning: `State ${state.state_id} of ${section.id}.` });
    if (initial) edges.push({ edge_id: `${section.id}-initial-${initial}`, type: "occupies", source_ref: section.id, target_ref: initial });
  }
  for (const section of sections.filter((item) => item.kind === "rule")) {
    if (section.rows.length !== 1) { issues.push({ code: "TEXT_RULE", path: `$line:${section.line}`, message: "rule requires exactly one predicate line" }); continue; }
    try {
      const named = /\s+is\s+considered\s+([A-Za-z_][\w.-]*)\.?$/i.exec(section.rows[0].text);
      const ruleId = section.id.startsWith("anonymous-rule-") && named ? named[1] : section.id;
      const cleaned = section.rows[0].text.replace(/^A\s+\w+\s+with\s+/i, "").replace(/\s+is\s+considered\s+[A-Za-z_][\w.-]*\.?$/i, "");
      const condition = parsePredicate(cleaned, factTypes);
      rules.push({ rule_id: ruleId, scope_refs: [], fact_refs: [...factTypes.keys()].filter((id) => JSON.stringify(condition).includes(`\"${id}\"`)), condition, consequence: "satisfied", exception_refs: [], owner_route: owner, source_refs: [`text:${section.line}`] });
    } catch (error) { if (error instanceof CompilationRejected) issues.push(...error.issues.map((issue) => ({ ...issue, path: `$line:${section.rows[0].line}${issue.path}` }))); else throw error; }
  }
  for (const section of sections.filter((item) => item.kind === "boundary")) {
    const declaredOwner = section.rows.find((row) => row.text.startsWith("owner "))?.text.slice(6);
    if (declaredOwner !== owner) issues.push({ code: "MISSING_OWNER", path: `$line:${section.line}`, message: "boundary owner must equal the declared domain owner" });
    boundaries.push({ boundary_id: section.id, owner_route: declaredOwner ?? "" });
  }
  for (const section of sections.filter((item) => item.kind === "event")) {
    const values = Object.fromEntries(section.rows.map((row) => { const match = /^(subject|payload|boundary)\s+(.+)$/.exec(row.text); if (!match) issues.push({ code: "TEXT_EVENT", path: `$line:${row.line}`, message: "expected subject, payload or boundary" }); return match ? [match[1], match[2]] : ["", ""]; }));
    events.push({ event_id: section.id, subject_refs: values.subject ? [values.subject] : [], payload_facts: words(values.payload ?? ""), trigger_refs: [], authority_boundary_ref: values.boundary ?? null, source_refs: [`text:${section.line}`] });
  }
  for (const section of sections.filter((item) => item.kind === "permission")) {
    const values = Object.fromEntries(section.rows.map((row) => { const match = /^(actor|action|when|boundary)\s+(.+)$/.exec(row.text); if (!match) issues.push({ code: "TEXT_PERMISSION", path: `$line:${row.line}`, message: "expected actor, action, when or boundary" }); return match ? [match[1], match[2]] : ["", ""]; }));
    const rule = rules.find((item) => item.rule_id === values.when);
    if (!rule) issues.push({ code: "UNRESOLVED_REFERENCE", path: `$line:${section.line}`, message: `permission rule ${values.when} is not declared` });
    permissions.push({ permission_id: section.id, actor_refs: values.actor ? [values.actor] : [], action_refs: values.action ? [values.action] : [], target_refs: [], scope_refs: [], condition: rule?.condition ?? { node: "literal", value_type: "boolean", value: false }, exception_refs: [], confirmation_policy_ref: null, authority_boundary_ref: values.boundary ?? "" });
  }
  for (const section of sections.filter((item) => item.kind === "effect")) {
    const values = Object.fromEntries(section.rows.map((row) => {
      const match = /^(pattern|binding|writes|emits|guarantee|on-failure|boundary)\s+(.+)$/.exec(row.text);
      if (!match) issues.push({ code: "TEXT_EFFECT", path: `$line:${row.line}`, message: "expected pattern, binding, writes, emits, guarantee, on-failure or boundary" });
      return match ? [match[1], match[2]] : ["", ""];
    }));
    for (const required of ["pattern", "binding", "writes", "emits", "guarantee", "on-failure", "boundary"]) {
      if (!values[required]) issues.push({ code: "TEXT_EFFECT_REQUIRED", path: `$line:${section.line}`, message: `effect ${section.id} requires ${required}` });
    }
    effects.push({ effect_id: section.id, pattern_ref: values.pattern ?? "", integration_binding_ref: values.binding ?? "", write_refs: words(values.writes ?? ""), event_refs: words(values.emits ?? ""), guarantee: values.guarantee ?? "", failure_continuation: values["on-failure"] ?? "", authority_boundary_ref: values.boundary ?? "" });
    terms.push({ term_id: section.id, kind: "effect", meaning: `Declared effect ${section.id}.` });
  }
  for (const section of sections.filter((item) => item.kind === "action")) {
    const multi: Record<string, string[]> = {};
    for (const row of section.rows) {
      const allowed = /^allowed only when\s+(.+)$/.exec(row.text);
      if (allowed) { try { const ruleId = `${section.id}-allowed`; const condition = parsePredicate(allowed[1], factTypes); rules.push({ rule_id: ruleId, scope_refs: [], fact_refs: [], condition, consequence: "satisfied", exception_refs: [], owner_route: owner, source_refs: [`text:${row.line}`] }); (multi.requires ??= []).push(ruleId); } catch (error) { if (error instanceof CompilationRejected) issues.push(...error.issues); else throw error; } continue; }
      const confirmation = /^requires human confirmation when\s+.+\s+is\s+([A-Za-z_][\w.-]*)\.?$/.exec(row.text);
      if (confirmation) { const rule = rules.find((item) => item.rule_id === confirmation[1]); if (!rule) issues.push({ code: "UNRESOLVED_REFERENCE", path: `$line:${row.line}`, message: `confirmation rule ${confirmation[1]} is not declared` }); else { if (!terms.some((term) => term.term_id === "Human")) terms.push({ term_id: "Human", kind: "actor", meaning: "Explicit human confirmation actor." }); const permissionId = `${section.id}-human-confirmation`; permissions.push({ permission_id: permissionId, actor_refs: ["Human"], action_refs: [section.id], target_refs: [], scope_refs: [], condition: rule.condition, exception_refs: [], confirmation_policy_ref: null, authority_boundary_ref: "" }); (multi.permission ??= []).push(permissionId); } continue; }
      const performs = /^performs\s+([A-Za-z_][\w.-]*)\s+using\s+([A-Za-z_][\w.-]*)$/.exec(row.text);
      if (performs) { (multi.performs ??= []).push(`${performs[1]}::${performs[2]}`); continue; }
      const match = /^(actor|subject|input|requires|permission|boundary|emits)\s+(.+)$/.exec(row.text); if (!match) { issues.push({ code: "TEXT_ACTION", path: `$line:${row.line}`, message: "expected actor, subject, input, requires, permission, boundary, emits or performs <effect> using <binding>" }); continue; } (multi[match[1]] ??= []).push(...words(match[2]));
    }
    actions.push({ action_id: section.id, actor_refs: multi.actor ?? [], subject_refs: multi.subject ?? [], input_facts: multi.input ?? [], precondition_rule_refs: multi.requires ?? [], permission_refs: multi.permission ?? [], confirmation_policy_ref: null, outcome_refs: multi.emits ?? [], performs: (multi.performs ?? []).map((value) => { const [effect_ref, integration_binding_ref] = value.split("::"); return { effect_ref, integration_binding_ref }; }), authority_boundary_ref: multi.boundary?.[0] ?? "" });
  }
  for (const section of sections.filter((item) => item.kind === "example")) {
    const values = Object.fromEntries(section.rows.map((row) => { const match = /^(kind|expected|rules)\s+(.+)$/.exec(row.text); if (!match) issues.push({ code: "TEXT_EXAMPLE", path: `$line:${row.line}`, message: "expected kind, expected or rules" }); return match ? [match[1], match[2]] : ["", ""]; }));
    examples.push({ example_id: section.id, kind: values.kind ?? "positive", facts: {}, expected_interpretation: values.expected ?? "", affected_rule_refs: words(values.rules ?? ""), boundary_witness_refs: [], source_refs: [`text:${section.line}`] });
  }
  if (issues.length) throw new CompilationRejected(issues);
  return {
    source_kind: extracted.source_kind,
    carrier: {
      schema_version: "cav2.alchlang.carrier/v2-candidate",
      identity: { domain_id: domainId, title }, owners: [{ owner_route: owner }], terms, edges, facts, rules, events, states, transitions, effects, actions, permissions, examples,
      authority: { authority_effect: "none", boundaries }, residue: []
    }
  };
}
