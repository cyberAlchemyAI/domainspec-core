import { BINARY_OPERATORS, CompilationRejected, LEAF_NODES, UNARY_OPERATORS } from "./model.js";
const SCALARS = new Set(["string", "integer", "decimal", "boolean", "identifier", "timestamp", "duration", "enum", "reference", "list", "record"]);
function obj(value, path, issues) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
        issues.push({ code: "UNSUPPORTED_SEMANTIC_CONSTRUCT", path, message: "expected an object" });
        return {};
    }
    return value;
}
function text(value, path, issues) {
    if (typeof value !== "string" || value.length === 0) {
        issues.push({ code: "UNSUPPORTED_SEMANTIC_CONSTRUCT", path, message: "expected a non-empty string" });
        return "";
    }
    return value;
}
function list(value, path, issues) {
    if (!Array.isArray(value)) {
        issues.push({ code: "UNSUPPORTED_SEMANTIC_CONSTRUCT", path, message: "expected an array" });
        return [];
    }
    return value;
}
const strings = (value, path, issues) => list(value, path, issues).map((item, index) => text(item, `${path}[${index}]`, issues));
function assertUnique(values, path, issues) {
    const seen = new Set();
    for (const value of values) {
        if (seen.has(value))
            issues.push({ code: "DUPLICATE_IDENTIFIER", path, message: `duplicate identifier ${value}` });
        seen.add(value);
    }
}
function validateExpression(value, path, facts, refs, issues) {
    const node = obj(value, path, issues);
    if (typeof node.node === "string") {
        if (!LEAF_NODES.includes(node.node)) {
            issues.push({ code: "UNSUPPORTED_SEMANTIC_CONSTRUCT", path, message: `unknown leaf ${node.node}` });
            return { expression: { node: "literal", value_type: "boolean", value: false }, type: "unknown" };
        }
        if (node.node === "literal") {
            const valueType = text(node.value_type, `${path}.value_type`, issues);
            if (!SCALARS.has(valueType))
                issues.push({ code: "TYPE_MISMATCH", path, message: `unknown literal type ${valueType}` });
            return { expression: { node: "literal", value_type: valueType, value: node.value }, type: valueType };
        }
        const ref = text(node.ref, `${path}.ref`, issues);
        const group = node.node === "fact_ref" ? "facts" : node.node === "entity_ref" ? "entities" : node.node === "actor_ref" ? "actors" : "states";
        if (!refs[group].has(ref))
            issues.push({ code: "UNRESOLVED_REFERENCE", path: `${path}.ref`, message: `${ref} is not a declared ${group.slice(0, -1)}` });
        const type = node.node === "fact_ref" ? (facts.get(ref) ?? "unknown") : "reference";
        return { expression: { node: node.node, ref }, type };
    }
    const operator = text(node.operator, `${path}.operator`, issues);
    const unary = UNARY_OPERATORS.includes(operator);
    const binary = BINARY_OPERATORS.includes(operator);
    if (!unary && !binary)
        issues.push({ code: "UNKNOWN_OPERATOR", path: `${path}.operator`, message: `${operator} is not in the carrier contract` });
    const operands = list(node.operands, `${path}.operands`, issues).map((operand, index) => validateExpression(operand, `${path}.operands[${index}]`, facts, refs, issues));
    const expected = unary ? 1 : 2;
    if (operands.length !== expected)
        issues.push({ code: "TYPE_MISMATCH", path: `${path}.operands`, message: `${operator} expects ${expected} operands` });
    const comparison = ["eq", "neq", "lt", "lte", "gt", "gte"].includes(operator);
    if (comparison && operands.length === 2 && operands[0].type !== "unknown" && operands[1].type !== "unknown" && operands[0].type !== operands[1].type) {
        issues.push({ code: "TYPE_MISMATCH", path, message: `${operator} cannot compare ${operands[0].type} with ${operands[1].type}` });
    }
    if (["and", "or", "not"].includes(operator) && operands.some((operand) => operand.type !== "boolean" && operand.type !== "unknown")) {
        issues.push({ code: "TYPE_MISMATCH", path, message: `${operator} requires boolean operands` });
    }
    return { expression: { operator, operands: operands.map((operand) => operand.expression) }, type: "boolean" };
}
function requireRefs(items, allowed, path, issues) {
    for (const [index, item] of items.entries())
        if (!allowed.has(item))
            issues.push({ code: "UNRESOLVED_REFERENCE", path: `${path}[${index}]`, message: `${item} is not declared` });
}
function normalizeV2(root, issues) {
    const required = ["identity", "owners", "terms", "edges", "facts", "rules", "events", "states", "transitions", "actions", "permissions", "examples", "authority", "residue"];
    for (const key of required)
        if (!(key in root))
            issues.push({ code: "UNSUPPORTED_SEMANTIC_CONSTRUCT", path: `$.${key}`, message: "required carrier-v2 section is missing" });
    const identity = obj(root.identity, "$.identity", issues);
    const domainId = text(identity.domain_id, "$.identity.domain_id", issues);
    const title = text(identity.title, "$.identity.title", issues);
    const ownerRows = list(root.owners, "$.owners", issues).map((value, index) => obj(value, `$.owners[${index}]`, issues));
    const owners = ownerRows.map((owner, index) => text(owner.owner_route, `$.owners[${index}].owner_route`, issues));
    if (owners.length === 0)
        issues.push({ code: "MISSING_OWNER", path: "$.owners", message: "at least one explicit owner route is required" });
    const termRows = list(root.terms, "$.terms", issues).map((value, index) => obj(value, `$.terms[${index}]`, issues));
    const terms = termRows.map((term, index) => ({ id: text(term.term_id, `$.terms[${index}].term_id`, issues), kind: text(term.kind, `$.terms[${index}].kind`, issues), meaning: text(term.meaning, `$.terms[${index}].meaning`, issues) }));
    const entityIds = new Set(terms.filter((term) => term.kind === "entity").map((term) => term.id));
    const actorIds = new Set(terms.filter((term) => term.kind === "actor").map((term) => term.id));
    const stateIds = new Set(terms.filter((term) => term.kind === "state").map((term) => term.id));
    const factRows = list(root.facts, "$.facts", issues).map((value, index) => obj(value, `$.facts[${index}]`, issues));
    const facts = factRows.map((fact, index) => {
        const type = text(fact.type, `$.facts[${index}].type`, issues);
        if (!SCALARS.has(type))
            issues.push({ code: "TYPE_MISMATCH", path: `$.facts[${index}].type`, message: `${type} is not a fact type` });
        const owner = text(fact.owner_route, `$.facts[${index}].owner_route`, issues);
        if (!owners.includes(owner))
            issues.push({ code: "MISSING_OWNER", path: `$.facts[${index}].owner_route`, message: `${owner} is not declared in owners` });
        return { id: text(fact.fact_id, `$.facts[${index}].fact_id`, issues), type, required: fact.required === true, owner };
    });
    const factTypes = new Map(facts.map((fact) => [fact.id, fact.type]));
    const factIds = new Set(facts.map((fact) => fact.id));
    const authority = obj(root.authority, "$.authority", issues);
    const boundaryRows = list(authority.boundaries, "$.authority.boundaries", issues).map((value, index) => obj(value, `$.authority.boundaries[${index}]`, issues));
    const authorityBoundaries = boundaryRows.map((boundary, index) => text(boundary.boundary_id, `$.authority.boundaries[${index}].boundary_id`, issues));
    const boundaryIds = new Set(authorityBoundaries);
    if (authority.authority_effect !== "none")
        issues.push({ code: "UNSUPPORTED_SEMANTIC_CONSTRUCT", path: "$.authority.authority_effect", message: "compiler accepts only non-effectful carriers" });
    const refs = { facts: factIds, entities: entityIds, actors: actorIds, states: stateIds };
    const ruleRows = list(root.rules, "$.rules", issues).map((value, index) => obj(value, `$.rules[${index}]`, issues));
    const rules = ruleRows.map((rule, index) => {
        const owner = text(rule.owner_route, `$.rules[${index}].owner_route`, issues);
        if (!owners.includes(owner))
            issues.push({ code: "MISSING_OWNER", path: `$.rules[${index}].owner_route`, message: `${owner} is not declared in owners` });
        return { id: text(rule.rule_id, `$.rules[${index}].rule_id`, issues), condition: validateExpression(rule.condition, `$.rules[${index}].condition`, factTypes, refs, issues).expression, owner, source_refs: strings(rule.source_refs, `$.rules[${index}].source_refs`, issues) };
    });
    const ruleIds = new Set(rules.map((rule) => rule.id));
    const eventRows = list(root.events, "$.events", issues).map((value, index) => obj(value, `$.events[${index}]`, issues));
    const events = eventRows.map((event, index) => {
        const payloadFacts = strings(event.payload_facts, `$.events[${index}].payload_facts`, issues);
        requireRefs(payloadFacts, factIds, `$.events[${index}].payload_facts`, issues);
        const boundary = event.authority_boundary_ref === null ? null : text(event.authority_boundary_ref, `$.events[${index}].authority_boundary_ref`, issues);
        if (boundary && !boundaryIds.has(boundary))
            issues.push({ code: "MISSING_AUTHORITY_BOUNDARY", path: `$.events[${index}].authority_boundary_ref`, message: `${boundary} is not declared` });
        return { id: text(event.event_id, `$.events[${index}].event_id`, issues), payload_facts: payloadFacts, authority_boundary_ref: boundary };
    });
    const eventIds = new Set(events.map((event) => event.id));
    const stateRows = list(root.states, "$.states", issues).map((value, index) => obj(value, `$.states[${index}]`, issues));
    const states = stateRows.map((state, index) => ({ id: text(state.state_id, `$.states[${index}].state_id`, issues), subject_ref: text(state.subject_ref, `$.states[${index}].subject_ref`, issues) }));
    requireRefs(states.map((state) => state.subject_ref), entityIds, "$.states.subject_ref", issues);
    for (const state of states)
        stateIds.add(state.id);
    const permissionRows = list(root.permissions, "$.permissions", issues).map((value, index) => obj(value, `$.permissions[${index}]`, issues));
    const permissionIds = new Set(permissionRows.map((permission, index) => text(permission.permission_id, `$.permissions[${index}].permission_id`, issues)));
    const effectRows = list(root.effects ?? [], "$.effects", issues).map((value, index) => obj(value, `$.effects[${index}]`, issues));
    const effectIds = new Set(effectRows.map((effect, index) => text(effect.effect_id, `$.effects[${index}].effect_id`, issues)));
    const effects = effectRows.map((effect, index) => {
        const boundary = text(effect.authority_boundary_ref, `$.effects[${index}].authority_boundary_ref`, issues);
        if (!boundaryIds.has(boundary))
            issues.push({ code: "MISSING_AUTHORITY_BOUNDARY", path: `$.effects[${index}].authority_boundary_ref`, message: `${boundary} is not declared` });
        const writeRefs = strings(effect.write_refs, `$.effects[${index}].write_refs`, issues);
        const eventRefs = strings(effect.event_refs, `$.effects[${index}].event_refs`, issues);
        requireRefs(writeRefs, entityIds, `$.effects[${index}].write_refs`, issues);
        requireRefs(eventRefs, eventIds, `$.effects[${index}].event_refs`, issues);
        const guarantee = text(effect.guarantee, `$.effects[${index}].guarantee`, issues);
        if (guarantee !== "atomic-state-and-outbox")
            issues.push({ code: "UNSUPPORTED_EFFECT_GUARANTEE", path: `$.effects[${index}].guarantee`, message: `${guarantee} is not supported` });
        const failure = text(effect.failure_continuation, `$.effects[${index}].failure_continuation`, issues);
        if (failure !== "rollback")
            issues.push({ code: "UNSUPPORTED_FAILURE_CONTINUATION", path: `$.effects[${index}].failure_continuation`, message: `${failure} is not supported` });
        return { id: text(effect.effect_id, `$.effects[${index}].effect_id`, issues), pattern_ref: text(effect.pattern_ref, `$.effects[${index}].pattern_ref`, issues), integration_binding_ref: text(effect.integration_binding_ref, `$.effects[${index}].integration_binding_ref`, issues), write_refs: writeRefs, event_refs: eventRefs, guarantee, failure_continuation: failure, authority_boundary_ref: boundary };
    });
    const actionRows = list(root.actions, "$.actions", issues).map((value, index) => obj(value, `$.actions[${index}]`, issues));
    const actionIds = new Set(actionRows.map((action, index) => text(action.action_id, `$.actions[${index}].action_id`, issues)));
    const actions = actionRows.map((action, index) => {
        const boundary = text(action.authority_boundary_ref, `$.actions[${index}].authority_boundary_ref`, issues);
        if (!boundaryIds.has(boundary))
            issues.push({ code: "MISSING_AUTHORITY_BOUNDARY", path: `$.actions[${index}].authority_boundary_ref`, message: `${boundary} is not declared` });
        const actorRefs = strings(action.actor_refs, `$.actions[${index}].actor_refs`, issues);
        const subjectRefs = strings(action.subject_refs, `$.actions[${index}].subject_refs`, issues);
        const inputFacts = strings(action.input_facts, `$.actions[${index}].input_facts`, issues);
        const ruleRefs = strings(action.precondition_rule_refs, `$.actions[${index}].precondition_rule_refs`, issues);
        const permissionRefs = strings(action.permission_refs, `$.actions[${index}].permission_refs`, issues);
        const performs = list(action.performs ?? [], `$.actions[${index}].performs`, issues).map((value, performIndex) => {
            const row = obj(value, `$.actions[${index}].performs[${performIndex}]`, issues);
            const effectRef = text(row.effect_ref, `$.actions[${index}].performs[${performIndex}].effect_ref`, issues);
            const bindingRef = text(row.integration_binding_ref, `$.actions[${index}].performs[${performIndex}].integration_binding_ref`, issues);
            if (!effectIds.has(effectRef))
                issues.push({ code: "UNRESOLVED_EFFECT", path: `$.actions[${index}].performs[${performIndex}].effect_ref`, message: `${effectRef} is not declared` });
            const effect = effects.find((candidate) => candidate.id === effectRef);
            if (effect && effect.integration_binding_ref !== bindingRef)
                issues.push({ code: "EFFECT_BINDING_MISMATCH", path: `$.actions[${index}].performs[${performIndex}].integration_binding_ref`, message: `${bindingRef} does not match ${effect.integration_binding_ref}` });
            return { effect_ref: effectRef, integration_binding_ref: bindingRef };
        });
        requireRefs(actorRefs, actorIds, `$.actions[${index}].actor_refs`, issues);
        requireRefs(subjectRefs, entityIds, `$.actions[${index}].subject_refs`, issues);
        requireRefs(inputFacts, factIds, `$.actions[${index}].input_facts`, issues);
        requireRefs(ruleRefs, ruleIds, `$.actions[${index}].precondition_rule_refs`, issues);
        requireRefs(permissionRefs, permissionIds, `$.actions[${index}].permission_refs`, issues);
        return { id: text(action.action_id, `$.actions[${index}].action_id`, issues), actor_refs: actorRefs, subject_refs: subjectRefs, input_facts: inputFacts, precondition_rule_refs: ruleRefs, permission_refs: permissionRefs, outcome_refs: strings(action.outcome_refs, `$.actions[${index}].outcome_refs`, issues), performs, authority_boundary_ref: boundary };
    });
    const permissions = permissionRows.map((permission, index) => {
        const boundary = text(permission.authority_boundary_ref, `$.permissions[${index}].authority_boundary_ref`, issues);
        if (!boundaryIds.has(boundary))
            issues.push({ code: "MISSING_AUTHORITY_BOUNDARY", path: `$.permissions[${index}].authority_boundary_ref`, message: `${boundary} is not declared` });
        const actorRefs = strings(permission.actor_refs, `$.permissions[${index}].actor_refs`, issues);
        const permissionActionRefs = strings(permission.action_refs, `$.permissions[${index}].action_refs`, issues);
        requireRefs(actorRefs, actorIds, `$.permissions[${index}].actor_refs`, issues);
        requireRefs(permissionActionRefs, actionIds, `$.permissions[${index}].action_refs`, issues);
        return { id: text(permission.permission_id, `$.permissions[${index}].permission_id`, issues), actor_refs: actorRefs, action_refs: permissionActionRefs, condition: validateExpression(permission.condition, `$.permissions[${index}].condition`, factTypes, refs, issues).expression, authority_boundary_ref: boundary };
    });
    const transitionRows = list(root.transitions, "$.transitions", issues).map((value, index) => obj(value, `$.transitions[${index}]`, issues));
    const transitions = transitionRows.map((transition, index) => {
        const from = text(transition.from_state_ref, `$.transitions[${index}].from_state_ref`, issues);
        const to = text(transition.to_state_ref, `$.transitions[${index}].to_state_ref`, issues);
        requireRefs([from, to], stateIds, `$.transitions[${index}].state_refs`, issues);
        const trigger = transition.trigger_ref === null ? null : text(transition.trigger_ref, `$.transitions[${index}].trigger_ref`, issues);
        if (trigger && !actionIds.has(trigger) && !eventIds.has(trigger))
            issues.push({ code: "UNRESOLVED_REFERENCE", path: `$.transitions[${index}].trigger_ref`, message: `${trigger} is neither action nor event` });
        const guardRefs = strings(transition.guard_rule_refs, `$.transitions[${index}].guard_rule_refs`, issues);
        const resultRefs = strings(transition.resulting_event_refs, `$.transitions[${index}].resulting_event_refs`, issues);
        requireRefs(guardRefs, ruleIds, `$.transitions[${index}].guard_rule_refs`, issues);
        requireRefs(resultRefs, eventIds, `$.transitions[${index}].resulting_event_refs`, issues);
        const boundary = transition.authority_boundary_ref === null ? null : text(transition.authority_boundary_ref, `$.transitions[${index}].authority_boundary_ref`, issues);
        if (boundary && !boundaryIds.has(boundary))
            issues.push({ code: "MISSING_AUTHORITY_BOUNDARY", path: `$.transitions[${index}].authority_boundary_ref`, message: `${boundary} is not declared` });
        return { id: text(transition.transition_id, `$.transitions[${index}].transition_id`, issues), subject_ref: text(transition.subject_ref, `$.transitions[${index}].subject_ref`, issues), from_state_ref: from, to_state_ref: to, trigger_ref: trigger, guard_rule_refs: guardRefs, resulting_event_refs: resultRefs, authority_boundary_ref: boundary };
    });
    const edgeRows = list(root.edges, "$.edges", issues).map((value, index) => obj(value, `$.edges[${index}]`, issues));
    const edges = edgeRows.map((edge, index) => ({ id: text(edge.edge_id, `$.edges[${index}].edge_id`, issues), type: text(edge.type, `$.edges[${index}].type`, issues), source: text(edge.source_ref, `$.edges[${index}].source_ref`, issues), target: text(edge.target_ref, `$.edges[${index}].target_ref`, issues) }));
    const semanticEdges = actions.flatMap((action) => action.performs.flatMap((performed) => {
        const effect = effects.find((candidate) => candidate.id === performed.effect_ref);
        if (!effect)
            return [];
        return [
            { id: `${action.id}-performs-${effect.id}`, type: "performs", source: action.id, target: effect.id },
            { id: `${effect.id}-instantiates-${effect.pattern_ref}`, type: "instantiates", source: effect.id, target: effect.pattern_ref },
            { id: `${effect.id}-uses-${effect.integration_binding_ref}`, type: "uses", source: effect.id, target: effect.integration_binding_ref },
            ...effect.write_refs.map((target) => ({ id: `${effect.id}-writes-${target}`, type: "writes", source: effect.id, target })),
            ...effect.event_refs.map((target) => ({ id: `${effect.id}-emits-${target}`, type: "emits", source: effect.id, target }))
        ];
    }));
    const externalSemanticIds = new Set(effects.flatMap((effect) => [effect.pattern_ref, effect.integration_binding_ref]));
    const allSemanticIds = new Set([...terms.map((term) => term.id), ...facts.map((fact) => fact.id), ...rules.map((rule) => rule.id), ...events.map((event) => event.id), ...states.map((state) => state.id), ...effects.map((effect) => effect.id), ...actions.map((action) => action.id), ...permissions.map((permission) => permission.id), ...authorityBoundaries, ...externalSemanticIds]);
    edges.push(...semanticEdges);
    for (const [index, edge] of edges.entries())
        requireRefs([edge.source, edge.target], allSemanticIds, `$.edges[${index}]`, issues);
    const examples = list(root.examples, "$.examples", issues).map((value, index) => obj(value, `$.examples[${index}]`, issues)).map((example, index) => ({ id: text(example.example_id, `$.examples[${index}].example_id`, issues), kind: text(example.kind, `$.examples[${index}].kind`, issues), expected: text(example.expected_interpretation, `$.examples[${index}].expected_interpretation`, issues), affected_rule_refs: strings(example.affected_rule_refs, `$.examples[${index}].affected_rule_refs`, issues) }));
    for (const [index, example] of examples.entries())
        requireRefs(example.affected_rule_refs, ruleIds, `$.examples[${index}].affected_rule_refs`, issues);
    for (const [name, ids] of Object.entries({ terms: terms.map((x) => x.id), facts: facts.map((x) => x.id), rules: rules.map((x) => x.id), events: events.map((x) => x.id), states: states.map((x) => x.id), effects: effects.map((x) => x.id), actions: actions.map((x) => x.id), permissions: permissions.map((x) => x.id), boundaries: authorityBoundaries }))
        assertUnique(ids, `$.${name}`, issues);
    const residue = list(root.residue, "$.residue", issues).map((value, index) => obj(value, `$.residue[${index}]`, issues)).map((item, index) => ({ code: text(item.code, `$.residue[${index}].code`, issues), subject_ref: text(item.subject_ref, `$.residue[${index}].subject_ref`, issues), owner_route: text(item.owner_route, `$.residue[${index}].owner_route`, issues), detail: text(item.detail, `$.residue[${index}].detail`, issues) }));
    return { schema_version: text(root.schema_version, "$.schema_version", issues), domain_id: domainId, title, owners, terms, edges, facts, rules, events, states, transitions, effects, actions, permissions, examples, authority_boundaries: authorityBoundaries, authority_effect: "none", residue, metadata: {} };
}
function normalizeLegacy(root, issues) {
    const domainId = text(root.domain_id, "$.domain_id", issues);
    const owner = text(root.owner_route, "$.owner_route", issues);
    if (root.authority_effect !== "none")
        issues.push({ code: "UNSUPPORTED_SEMANTIC_CONSTRUCT", path: "$.authority_effect", message: "compiler accepts only non-effectful carriers" });
    const termRows = list(root.terms, "$.terms", issues).map((value, index) => obj(value, `$.terms[${index}]`, issues));
    const terms = termRows.map((term, index) => ({ id: text(term.id, `$.terms[${index}].id`, issues), kind: "concept", meaning: text(term.meaning, `$.terms[${index}].meaning`, issues) }));
    const subject = obj(root.primary_subject, "$.primary_subject", issues);
    const subjectId = text(subject.term_id, "$.primary_subject.term_id", issues);
    const subjectTerm = terms.find((term) => term.id === subjectId);
    if (subjectTerm)
        subjectTerm.kind = "entity";
    else
        issues.push({ code: "UNRESOLVED_REFERENCE", path: "$.primary_subject.term_id", message: `${subjectId} is not a term` });
    const fields = list(subject.fields, "$.primary_subject.fields", issues).map((value, index) => obj(value, `$.primary_subject.fields[${index}]`, issues));
    const facts = fields.map((field, index) => { const rawType = text(field.type, `$.primary_subject.fields[${index}].type`, issues); const type = rawType === "uuid" ? "identifier" : rawType; if (!SCALARS.has(type))
        issues.push({ code: "TYPE_MISMATCH", path: `$.primary_subject.fields[${index}].type`, message: `${rawType} is not supported` }); return { id: text(field.id, `$.primary_subject.fields[${index}].id`, issues), type, required: field.required === true, owner }; });
    const boundaries = list(root.authority_boundaries, "$.authority_boundaries", issues).map((value, index) => obj(value, `$.authority_boundaries[${index}]`, issues));
    const authorityBoundaries = boundaries.map((boundary, index) => text(boundary.id, `$.authority_boundaries[${index}].id`, issues));
    const boundaryIds = new Set(authorityBoundaries);
    const ruleRows = list(root.rules, "$.rules", issues).map((value, index) => obj(value, `$.rules[${index}]`, issues));
    const rules = ruleRows.map((rule, index) => ({ id: text(rule.id, `$.rules[${index}].id`, issues), condition: { legacy_predicate: text(rule.predicate, `$.rules[${index}].predicate`, issues) }, owner, source_refs: [] }));
    const ruleIds = new Set(rules.map((rule) => rule.id));
    const eventRows = list(root.events, "$.events", issues).map((value, index) => obj(value, `$.events[${index}]`, issues));
    const events = eventRows.map((event, index) => ({ id: text(event.id, `$.events[${index}].id`, issues), payload_facts: strings(event.payload, `$.events[${index}].payload`, issues), authority_boundary_ref: null }));
    const eventIds = new Set(events.map((event) => event.id));
    const permissionRows = list(root.permissions, "$.permissions", issues).map((value, index) => obj(value, `$.permissions[${index}]`, issues));
    const permissions = permissionRows.map((permission, index) => ({ id: text(permission.id, `$.permissions[${index}].id`, issues), actor_refs: [text(permission.actor, `$.permissions[${index}].actor`, issues)], action_refs: [text(permission.action_ref, `$.permissions[${index}].action_ref`, issues)], condition: { legacy_condition: text(permission.condition, `$.permissions[${index}].condition`, issues) }, authority_boundary_ref: "" }));
    const actionRows = list(root.actions, "$.actions", issues).map((value, index) => obj(value, `$.actions[${index}]`, issues));
    const actions = actionRows.map((action, index) => { const boundary = text(action.authority_boundary_ref, `$.actions[${index}].authority_boundary_ref`, issues); if (!boundaryIds.has(boundary))
        issues.push({ code: "MISSING_AUTHORITY_BOUNDARY", path: `$.actions[${index}].authority_boundary_ref`, message: `${boundary} is not declared` }); const ruleRefs = strings(action.rule_refs, `$.actions[${index}].rule_refs`, issues); requireRefs(ruleRefs, ruleIds, `$.actions[${index}].rule_refs`, issues); const outcomeRefs = strings(action.event_refs, `$.actions[${index}].event_refs`, issues); requireRefs(outcomeRefs, eventIds, `$.actions[${index}].event_refs`, issues); return { id: text(action.id, `$.actions[${index}].id`, issues), actor_refs: [], subject_refs: strings(action.reads, `$.actions[${index}].reads`, issues).filter((ref) => !ref.includes(".")), input_facts: [], precondition_rule_refs: ruleRefs, permission_refs: permissions.filter((permission) => permission.action_refs.includes(String(action.id))).map((permission) => permission.id), outcome_refs: outcomeRefs, performs: [], authority_boundary_ref: boundary }; });
    const actionIds = new Set(actions.map((action) => action.id));
    for (const [index, permission] of permissions.entries()) {
        requireRefs(permission.action_refs, actionIds, `$.permissions[${index}].action_ref`, issues);
        const action = actions.find((item) => item.id === permission.action_refs[0]);
        permission.authority_boundary_ref = action?.authority_boundary_ref ?? "";
    }
    const machine = obj(root.state_machine, "$.state_machine", issues);
    const states = strings(machine.states, "$.state_machine.states", issues).map((id) => ({ id, subject_ref: subjectId }));
    const stateIds = new Set(states.map((state) => state.id));
    const transitions = list(machine.transitions, "$.state_machine.transitions", issues).map((value, index) => obj(value, `$.state_machine.transitions[${index}]`, issues)).map((transition, index) => { const from = text(transition.from, `$.state_machine.transitions[${index}].from`, issues); const to = text(transition.to, `$.state_machine.transitions[${index}].to`, issues); requireRefs([from, to], stateIds, `$.state_machine.transitions[${index}]`, issues); const ruleRef = transition.rule_ref === null ? null : text(transition.rule_ref, `$.state_machine.transitions[${index}].rule_ref`, issues); if (ruleRef)
        requireRefs([ruleRef], ruleIds, `$.state_machine.transitions[${index}].rule_ref`, issues); const eventRef = transition.event_ref === null ? null : text(transition.event_ref, `$.state_machine.transitions[${index}].event_ref`, issues); if (eventRef)
        requireRefs([eventRef], eventIds, `$.state_machine.transitions[${index}].event_ref`, issues); return { id: text(transition.id, `$.state_machine.transitions[${index}].id`, issues), subject_ref: subjectId, from_state_ref: from, to_state_ref: to, trigger_ref: null, guard_rule_refs: ruleRef ? [ruleRef] : [], resulting_event_refs: eventRef ? [eventRef] : [], authority_boundary_ref: null }; });
    const edges = list(root.ontology_edges, "$.ontology_edges", issues).map((value, index) => obj(value, `$.ontology_edges[${index}]`, issues)).map((edge, index) => ({ id: text(edge.id, `$.ontology_edges[${index}].id`, issues), type: text(edge.type, `$.ontology_edges[${index}].type`, issues), source: text(edge.source, `$.ontology_edges[${index}].source`, issues), target: text(edge.target, `$.ontology_edges[${index}].target`, issues) }));
    const examples = list(root.examples, "$.examples", issues).map((value, index) => obj(value, `$.examples[${index}]`, issues)).map((example, index) => ({ id: text(example.id, `$.examples[${index}].id`, issues), kind: text(example.kind, `$.examples[${index}].kind`, issues), expected: text(example.expected, `$.examples[${index}].expected`, issues), affected_rule_refs: [] }));
    const residue = rules.map((rule) => ({ code: "LEGACY_OPAQUE_PREDICATE", subject_ref: rule.id, owner_route: owner, detail: "Retained for traceability; not executable until migrated to the carrier-v2 typed AST." }));
    return { schema_version: text(root.schema_version, "$.schema_version", issues), domain_id: domainId, title: text(root.title, "$.title", issues), owners: [owner], terms, edges, facts, rules, events, states, transitions, effects: [], actions, permissions, examples, authority_boundaries: authorityBoundaries, authority_effect: "none", residue, metadata: { runtime_profile: root.runtime_profile, compatibility_mode: "v1-reference" } };
}
export function validateAndNormalize(input) {
    const issues = [];
    const root = obj(input, "$", issues);
    const version = text(root.schema_version, "$.schema_version", issues);
    const model = version === "cav2.alchlang.carrier/v2-candidate" ? normalizeV2(root, issues) : version === "alchlang.governed-domain-description/v1-candidate" ? normalizeLegacy(root, issues) : (() => { issues.push({ code: "UNSUPPORTED_SEMANTIC_CONSTRUCT", path: "$.schema_version", message: `${version} is not supported` }); return normalizeV2(root, issues); })();
    if (issues.length)
        throw new CompilationRejected(issues);
    return model;
}
