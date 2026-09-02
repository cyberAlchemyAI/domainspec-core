export function lower(model) {
    const subjects = model.terms.filter((term) => term.kind === "entity");
    const nodes = [
        ...model.terms.map((term) => ({ id: term.id, kind: term.kind })),
        ...model.facts.map((fact) => ({ id: fact.id, kind: "fact" })),
        ...model.rules.map((rule) => ({ id: rule.id, kind: "rule" })),
        ...model.events.map((event) => ({ id: event.id, kind: "event" })),
        ...model.effects.map((effect) => ({ id: effect.id, kind: "effect" })),
        ...model.actions.map((action) => ({ id: action.id, kind: "action" })),
    ].sort((a, b) => a.id.localeCompare(b.id));
    return {
        model,
        type_model: subjects.map((subject) => ({ id: subject.id, fields: model.facts })),
        predicate_model: model.rules,
        event_contracts: model.events,
        state_machines: subjects.map((subject) => ({ subject_ref: subject.id, states: model.states.filter((state) => state.subject_ref === subject.id).map((state) => state.id), transitions: model.transitions.filter((transition) => transition.subject_ref === subject.id) })),
        effect_contracts: model.effects,
        action_ports: model.actions,
        permission_guards: model.permissions,
        test_obligations: model.examples.map((example) => ({ id: example.id, kind: example.kind, expected: example.expected, rule_refs: example.affected_rule_refs })),
        documentation_model: { title: model.title, term_count: model.terms.length, rule_count: model.rules.length, claim_ceiling: "Target-neutral candidate output; no acceptance, execution, or effect authority." },
        graph_model: { nodes, edges: [...model.edges].sort((a, b) => a.id.localeCompare(b.id)) },
        trace_ledger: [
            ...model.rules.map((rule) => ({ output_ref: `predicate_model:${rule.id}`, source_refs: rule.source_refs.length ? rule.source_refs : [`rule:${rule.id}`] })),
            ...model.actions.map((action) => ({ output_ref: `action_port:${action.id}`, source_refs: [`action:${action.id}`, ...action.precondition_rule_refs.map((id) => `rule:${id}`)] })),
            ...model.effects.map((effect) => ({ output_ref: `effect_contract:${effect.id}`, source_refs: [`effect:${effect.id}`, `pattern:${effect.pattern_ref}`, `binding:${effect.integration_binding_ref}`] })),
            ...model.events.map((event) => ({ output_ref: `event_contract:${event.id}`, source_refs: [`event:${event.id}`] })),
        ].sort((a, b) => a.output_ref.localeCompare(b.output_ref)),
        unsupported_residue: model.residue,
    };
}
