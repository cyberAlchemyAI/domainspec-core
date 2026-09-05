import { CompilationRejected } from "./model.js";
import { translateLegacyPredicate } from "./predicate-parser.js";
function value(expression, facts) {
    if ("node" in expression) {
        if (expression.node === "literal")
            return expression.value;
        if (expression.node === "fact_ref")
            return facts[expression.ref];
        return expression.ref;
    }
    const operands = expression.operands.map((operand) => value(operand, facts));
    switch (expression.operator) {
        case "not": return !Boolean(operands[0]);
        case "exists": return operands[0] !== undefined && operands[0] !== null;
        case "absent": return operands[0] === undefined || operands[0] === null;
        case "eq": return operands[0] === operands[1];
        case "neq": return operands[0] !== operands[1];
        case "lt": return operands[0] < operands[1];
        case "lte": return operands[0] <= operands[1];
        case "gt": return operands[0] > operands[1];
        case "gte": return operands[0] >= operands[1];
        case "and": return Boolean(operands[0]) && Boolean(operands[1]);
        case "or": return Boolean(operands[0]) || Boolean(operands[1]);
        case "in": return Array.isArray(operands[1]) && operands[1].includes(operands[0]);
        case "contains": return Array.isArray(operands[0]) ? operands[0].includes(operands[1]) : typeof operands[0] === "string" && operands[0].includes(String(operands[1]));
        default: throw new CompilationRejected([{ code: "UNKNOWN_OPERATOR", path: "$.runtime", message: `runtime cannot evaluate ${expression.operator}` }]);
    }
}
export function evaluateSfolFormula(expression, facts) {
    return Boolean(value(expression, facts));
}
/** @deprecated Use evaluateSfolFormula. */
export const evaluateExpression = evaluateSfolFormula;
export function evaluateRule(rule, facts, legacyRegistry = {}) {
    const expression = "legacy_predicate" in rule.condition ? translateLegacyPredicate(rule.condition.legacy_predicate, legacyRegistry) : rule.condition;
    return evaluateSfolFormula(expression, facts);
}
export async function executeAction(model, request, adapters, legacyRegistry = {}) {
    const action = model.actions.find((item) => item.id === request.action_id);
    if (!action)
        throw new CompilationRejected([{ code: "ACTION_NOT_FOUND", path: "$.action_id", message: `${request.action_id} is not declared` }]);
    if (action.actor_refs.length && !action.actor_refs.includes(request.actor_ref))
        throw new CompilationRejected([{ code: "ACTOR_DENIED", path: "$.actor_ref", message: `${request.actor_ref} cannot execute ${action.id}` }]);
    for (const fact of action.input_facts)
        if (!(fact in request.facts))
            throw new CompilationRejected([{ code: "MISSING_ACTION_INPUT", path: `$.facts.${fact}`, message: `${fact} is required` }]);
    if (!request.authority_grants.includes(action.authority_boundary_ref))
        throw new CompilationRejected([{ code: "AUTHORITY_DENIED", path: "$.authority_grants", message: `missing exact grant ${action.authority_boundary_ref}` }]);
    const ruleResults = {};
    for (const ruleId of action.precondition_rule_refs) {
        const rule = model.rules.find((item) => item.id === ruleId);
        if (!rule)
            throw new CompilationRejected([{ code: "UNRESOLVED_REFERENCE", path: `$.actions.${action.id}`, message: `missing rule ${ruleId}` }]);
        ruleResults[ruleId] = evaluateRule(rule, request.facts, legacyRegistry);
        if (!ruleResults[ruleId])
            throw new CompilationRejected([{ code: "RULE_DENIED", path: `$.rules.${ruleId}`, message: `precondition ${ruleId} evaluated false` }]);
    }
    const permissionResults = {};
    for (const permissionId of action.permission_refs) {
        const permission = model.permissions.find((item) => item.id === permissionId);
        if (!permission)
            throw new CompilationRejected([{ code: "UNRESOLVED_REFERENCE", path: `$.actions.${action.id}`, message: `missing permission ${permissionId}` }]);
        if (!permission.actor_refs.includes(request.actor_ref))
            throw new CompilationRejected([{ code: "ACTOR_DENIED", path: `$.permissions.${permissionId}`, message: `${request.actor_ref} is outside the permission` }]);
        if (permission.authority_boundary_ref !== action.authority_boundary_ref)
            throw new CompilationRejected([{ code: "AUTHORITY_BOUNDARY_MISMATCH", path: `$.permissions.${permissionId}`, message: "permission and action boundaries differ" }]);
        const condition = "legacy_condition" in permission.condition ? translateLegacyPredicate(permission.condition.legacy_condition, legacyRegistry) : permission.condition;
        permissionResults[permissionId] = evaluateSfolFormula(condition, request.facts);
        if (!permissionResults[permissionId])
            throw new CompilationRejected([{ code: "PERMISSION_DENIED", path: `$.permissions.${permissionId}`, message: `permission ${permissionId} evaluated false` }]);
    }
    const adapter = adapters[action.id];
    if (!adapter)
        throw new CompilationRejected([{ code: "ADAPTER_NOT_BOUND", path: `$.adapters.${action.id}`, message: "an explicit action adapter is required" }]);
    const result = await adapter.execute({ ...request, domain_id: model.domain_id, authority_boundary_ref: action.authority_boundary_ref });
    const allowedEvents = new Set(action.outcome_refs);
    const emitted = result.emitted_events ?? [];
    for (const event of emitted)
        if (!allowedEvents.has(event))
            throw new CompilationRejected([{ code: "UNDECLARED_EVENT", path: `$.adapter.${action.id}`, message: `${event} is not an action outcome` }]);
    return { status: "executed", action_id: action.id, outcome: result.outcome, emitted_events: emitted, rule_results: ruleResults, permission_results: permissionResults, adapter_data: result.data };
}
