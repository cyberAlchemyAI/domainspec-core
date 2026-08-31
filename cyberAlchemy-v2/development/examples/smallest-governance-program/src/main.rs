use smallest_governance_program::{
    evaluate, AuthorityDisposition, EffectCeiling, FactScope, FactValue, GovernanceFact,
    GovernanceFactSet, GovernanceProgram, GovernanceRequest, ProgramClause, VersionedRef,
};

const RULE: VersionedRef<'static> = VersionedRef {
    id: "demo-publication-rule",
    version: 1,
};
const CONSTITUTION: VersionedRef<'static> = VersionedRef {
    id: "demo-constitution",
    version: 1,
};
const BINDING: VersionedRef<'static> = VersionedRef {
    id: "demo-publication-binding",
    version: 1,
};
const REQUEST: GovernanceRequest<'static> = GovernanceRequest {
    principal: "synthetic:demo-agent",
    subject: "candidate:demo-document",
    action: "publish",
    target: "public:demo-document",
    consequence: "demo-document-becomes-public",
    requested_effect: "publication",
    integration_surface: "synthetic:demo-surface",
    mode: "evaluate_only",
    context: "smallest-governance-program",
};
const CLAUSES: [ProgramClause<'static>; 5] = [
    ProgramClause::RequireAdoptedRule {
        rule: RULE,
        constitution: CONSTITUTION,
    },
    ProgramClause::RequireApplicableRule { rule: RULE },
    ProgramClause::RequireActiveBinding {
        rule: RULE,
        binding: BINDING,
    },
    ProgramClause::RequireAuthorityPermit {
        layer: "repository",
    },
    ProgramClause::RequireAuthorityPermit {
        layer: "publication",
    },
];
const PROGRAM: GovernanceProgram<'static> = GovernanceProgram {
    id: "smallest-publication-governance",
    version: 1,
    effect_ceiling: EffectCeiling::NoEffect,
    selector: REQUEST,
    clauses: &CLAUSES,
};
const SCOPE: FactScope<'static> = REQUEST;

fn fact(value: FactValue<'static>) -> GovernanceFact<'static> {
    GovernanceFact {
        scope: SCOPE,
        source: "synthetic:demo-source",
        verifier: "synthetic:demo-verifier",
        value,
    }
}

fn complete_facts(publication: AuthorityDisposition) -> Vec<GovernanceFact<'static>> {
    vec![
        fact(FactValue::RuleAdopted {
            rule: RULE,
            constitution: CONSTITUTION,
            adopted: true,
        }),
        fact(FactValue::RuleApplicable {
            rule: RULE,
            applicable: true,
        }),
        fact(FactValue::EnforcementBindingActive {
            rule: RULE,
            binding: BINDING,
            active: true,
        }),
        fact(FactValue::Authority {
            layer: "repository",
            disposition: AuthorityDisposition::Permit,
        }),
        fact(FactValue::Authority {
            layer: "publication",
            disposition: publication,
        }),
    ]
}

fn facts_for(scenario: &str) -> Result<Vec<GovernanceFact<'static>>, &'static str> {
    match scenario {
        "allow" => Ok(complete_facts(AuthorityDisposition::Permit)),
        "deny" => Ok(complete_facts(AuthorityDisposition::Forbid)),
        "abstain" => {
            let mut facts = complete_facts(AuthorityDisposition::Permit);
            facts.remove(2);
            Ok(facts)
        }
        "error" => {
            let mut facts = complete_facts(AuthorityDisposition::Permit);
            facts.push(fact(FactValue::Authority {
                layer: "publication",
                disposition: AuthorityDisposition::Forbid,
            }));
            Ok(facts)
        }
        _ => Err("expected one scenario: allow, deny, abstain, or error"),
    }
}

fn main() {
    let scenario = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "abstain".to_owned());
    let facts = match facts_for(&scenario) {
        Ok(facts) => facts,
        Err(message) => {
            eprintln!("error: {message}");
            std::process::exit(2);
        }
    };

    let evaluation = evaluate(&PROGRAM, &REQUEST, &GovernanceFactSet { facts: &facts });

    println!("program={}/v{}", PROGRAM.id, PROGRAM.version);
    println!("request={} {}", REQUEST.action, REQUEST.target);
    println!("scenario={scenario}");
    println!("effect_ceiling=no_effect");
    println!("verdict={}", evaluation.verdict);
    println!("reason={}", evaluation.reason);
    println!("effect_executed=false");
}
