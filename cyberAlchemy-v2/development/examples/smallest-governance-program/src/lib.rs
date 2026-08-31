//! A deliberately small, no-effect Governance Program interpreter.

use std::fmt;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct VersionedRef<'a> {
    pub id: &'a str,
    pub version: u32,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct GovernanceRequest<'a> {
    pub principal: &'a str,
    pub subject: &'a str,
    pub action: &'a str,
    pub target: &'a str,
    pub consequence: &'a str,
    pub requested_effect: &'a str,
    pub integration_surface: &'a str,
    pub mode: &'a str,
    pub context: &'a str,
}

pub type RequestSelector<'a> = GovernanceRequest<'a>;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EffectCeiling {
    NoEffect,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ProgramClause<'a> {
    RequireAdoptedRule {
        rule: VersionedRef<'a>,
        constitution: VersionedRef<'a>,
    },
    RequireApplicableRule {
        rule: VersionedRef<'a>,
    },
    RequireActiveBinding {
        rule: VersionedRef<'a>,
        binding: VersionedRef<'a>,
    },
    RequireAuthorityPermit {
        layer: &'a str,
    },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct GovernanceProgram<'a> {
    pub id: &'a str,
    pub version: u32,
    pub effect_ceiling: EffectCeiling,
    pub selector: RequestSelector<'a>,
    pub clauses: &'a [ProgramClause<'a>],
}

pub type FactScope<'a> = GovernanceRequest<'a>;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorityDisposition {
    Permit,
    Forbid,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum FactValue<'a> {
    RuleAdopted {
        rule: VersionedRef<'a>,
        constitution: VersionedRef<'a>,
        adopted: bool,
    },
    RuleApplicable {
        rule: VersionedRef<'a>,
        applicable: bool,
    },
    EnforcementBindingActive {
        rule: VersionedRef<'a>,
        binding: VersionedRef<'a>,
        active: bool,
    },
    Authority {
        layer: &'a str,
        disposition: AuthorityDisposition,
    },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct GovernanceFact<'a> {
    pub scope: FactScope<'a>,
    pub source: &'a str,
    pub verifier: &'a str,
    pub value: FactValue<'a>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct GovernanceFactSet<'a> {
    pub facts: &'a [GovernanceFact<'a>],
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum GovernanceVerdict {
    Allow,
    Deny,
    Abstain,
    Error,
}

impl fmt::Display for GovernanceVerdict {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let value = match self {
            Self::Allow => "allow",
            Self::Deny => "deny",
            Self::Abstain => "abstain",
            Self::Error => "error",
        };
        formatter.write_str(value)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EvaluationReason<'a> {
    AllClausesSatisfied,
    ExplicitAuthorityForbid(&'a str),
    RequestOutsideProgram,
    MissingFact(ProgramClause<'a>),
    UnsatisfiedPrecondition(ProgramClause<'a>),
    InvalidProgram,
    InvalidFactMetadata,
    FactOutsideRequestScope,
    UndeclaredFact,
    DuplicateOrConflictingFact,
}

impl fmt::Display for EvaluationReason<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::AllClausesSatisfied => formatter.write_str("all declared clauses are satisfied"),
            Self::ExplicitAuthorityForbid(layer) => {
                write!(
                    formatter,
                    "authority layer {layer:?} explicitly forbids the request"
                )
            }
            Self::RequestOutsideProgram => {
                formatter.write_str("the request does not match the program selector")
            }
            Self::MissingFact(clause) => {
                write!(formatter, "a required fact is missing for {clause:?}")
            }
            Self::UnsatisfiedPrecondition(clause) => {
                write!(
                    formatter,
                    "a governance precondition is not established for {clause:?}"
                )
            }
            Self::InvalidProgram => formatter.write_str("the program is empty or invalid"),
            Self::InvalidFactMetadata => {
                formatter.write_str("a fact has no visible source or verifier")
            }
            Self::FactOutsideRequestScope => {
                formatter.write_str("a fact is scoped to a different request")
            }
            Self::UndeclaredFact => formatter.write_str("the fact set contains an undeclared fact"),
            Self::DuplicateOrConflictingFact => {
                formatter.write_str("the fact set contains duplicate or conflicting facts")
            }
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Evaluation<'a> {
    pub verdict: GovernanceVerdict,
    pub reason: EvaluationReason<'a>,
}

/// Interpret one declarative Governance Program without performing any effect.
pub fn evaluate<'a>(
    program: &GovernanceProgram<'a>,
    request: &GovernanceRequest<'a>,
    fact_set: &GovernanceFactSet<'a>,
) -> Evaluation<'a> {
    if program.id.is_empty() || program.version == 0 || program.clauses.is_empty() {
        return error(EvaluationReason::InvalidProgram);
    }
    match program.effect_ceiling {
        EffectCeiling::NoEffect => {}
    }

    if program.selector != *request {
        return abstain(EvaluationReason::RequestOutsideProgram);
    }

    let expected_scope = *request;
    for (index, fact) in fact_set.facts.iter().enumerate() {
        if fact.source.is_empty() || fact.verifier.is_empty() {
            return error(EvaluationReason::InvalidFactMetadata);
        }
        if fact.scope != expected_scope {
            return error(EvaluationReason::FactOutsideRequestScope);
        }
        if !program
            .clauses
            .iter()
            .any(|clause| clause_accepts_fact(clause, fact))
        {
            return error(EvaluationReason::UndeclaredFact);
        }
        if fact_set.facts[index + 1..]
            .iter()
            .any(|other| same_fact_key(fact, other))
        {
            return error(EvaluationReason::DuplicateOrConflictingFact);
        }
    }

    for clause in program
        .clauses
        .iter()
        .filter(|clause| !matches!(clause, ProgramClause::RequireAuthorityPermit { .. }))
    {
        let Some(fact) = fact_set
            .facts
            .iter()
            .find(|fact| clause_accepts_fact(clause, fact))
        else {
            return abstain(EvaluationReason::MissingFact(*clause));
        };

        match (clause, fact.value) {
            (
                ProgramClause::RequireAdoptedRule { .. },
                FactValue::RuleAdopted { adopted: false, .. },
            )
            | (
                ProgramClause::RequireApplicableRule { .. },
                FactValue::RuleApplicable {
                    applicable: false, ..
                },
            )
            | (
                ProgramClause::RequireActiveBinding { .. },
                FactValue::EnforcementBindingActive { active: false, .. },
            ) => return abstain(EvaluationReason::UnsatisfiedPrecondition(*clause)),
            _ => {}
        }
    }

    let mut missing_authority = None;
    for clause in program
        .clauses
        .iter()
        .filter(|clause| matches!(clause, ProgramClause::RequireAuthorityPermit { .. }))
    {
        let Some(fact) = fact_set
            .facts
            .iter()
            .find(|fact| clause_accepts_fact(clause, fact))
        else {
            missing_authority.get_or_insert(*clause);
            continue;
        };

        if let (
            ProgramClause::RequireAuthorityPermit { layer },
            FactValue::Authority {
                disposition: AuthorityDisposition::Forbid,
                ..
            },
        ) = (clause, fact.value)
        {
            return deny(EvaluationReason::ExplicitAuthorityForbid(layer));
        }
    }

    if let Some(clause) = missing_authority {
        return abstain(EvaluationReason::MissingFact(clause));
    }

    Evaluation {
        verdict: GovernanceVerdict::Allow,
        reason: EvaluationReason::AllClausesSatisfied,
    }
}

fn clause_accepts_fact(clause: &ProgramClause<'_>, fact: &GovernanceFact<'_>) -> bool {
    match (clause, fact.value) {
        (
            ProgramClause::RequireAdoptedRule { rule, constitution },
            FactValue::RuleAdopted {
                rule: actual_rule,
                constitution: actual_constitution,
                ..
            },
        ) => rule == &actual_rule && constitution == &actual_constitution,
        (
            ProgramClause::RequireApplicableRule { rule },
            FactValue::RuleApplicable {
                rule: actual_rule, ..
            },
        ) => rule == &actual_rule,
        (
            ProgramClause::RequireActiveBinding { rule, binding },
            FactValue::EnforcementBindingActive {
                rule: actual_rule,
                binding: actual_binding,
                ..
            },
        ) => rule == &actual_rule && binding == &actual_binding,
        (
            ProgramClause::RequireAuthorityPermit { layer },
            FactValue::Authority {
                layer: actual_layer,
                ..
            },
        ) => layer == &actual_layer,
        _ => false,
    }
}

fn same_fact_key(left: &GovernanceFact<'_>, right: &GovernanceFact<'_>) -> bool {
    match (left.value, right.value) {
        (
            FactValue::RuleAdopted {
                rule, constitution, ..
            },
            FactValue::RuleAdopted {
                rule: other_rule,
                constitution: other_constitution,
                ..
            },
        ) => rule == other_rule && constitution == other_constitution,
        (
            FactValue::RuleApplicable { rule, .. },
            FactValue::RuleApplicable {
                rule: other_rule, ..
            },
        ) => rule == other_rule,
        (
            FactValue::EnforcementBindingActive { rule, binding, .. },
            FactValue::EnforcementBindingActive {
                rule: other_rule,
                binding: other_binding,
                ..
            },
        ) => rule == other_rule && binding == other_binding,
        (
            FactValue::Authority { layer, .. },
            FactValue::Authority {
                layer: other_layer, ..
            },
        ) => layer == other_layer,
        _ => false,
    }
}

fn abstain<'a>(reason: EvaluationReason<'a>) -> Evaluation<'a> {
    Evaluation {
        verdict: GovernanceVerdict::Abstain,
        reason,
    }
}

fn deny<'a>(reason: EvaluationReason<'a>) -> Evaluation<'a> {
    Evaluation {
        verdict: GovernanceVerdict::Deny,
        reason,
    }
}

fn error<'a>(reason: EvaluationReason<'a>) -> Evaluation<'a> {
    Evaluation {
        verdict: GovernanceVerdict::Error,
        reason,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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
            source: "synthetic:test-source",
            verifier: "synthetic:fixture-verifier",
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

    #[test]
    fn allows_only_when_every_declared_clause_is_satisfied() {
        let facts = complete_facts(AuthorityDisposition::Permit);
        let result = evaluate(&PROGRAM, &REQUEST, &GovernanceFactSet { facts: &facts });
        assert_eq!(result.verdict, GovernanceVerdict::Allow);
    }

    #[test]
    fn denies_an_explicit_authority_forbid() {
        let facts = complete_facts(AuthorityDisposition::Forbid);
        let result = evaluate(&PROGRAM, &REQUEST, &GovernanceFactSet { facts: &facts });
        assert_eq!(result.verdict, GovernanceVerdict::Deny);
    }

    #[test]
    fn abstains_when_a_required_fact_is_missing() {
        let mut facts = complete_facts(AuthorityDisposition::Permit);
        facts.remove(2);
        let result = evaluate(&PROGRAM, &REQUEST, &GovernanceFactSet { facts: &facts });
        assert_eq!(result.verdict, GovernanceVerdict::Abstain);
    }

    #[test]
    fn abstains_when_the_request_does_not_match() {
        let facts = complete_facts(AuthorityDisposition::Permit);
        let different_request = GovernanceRequest {
            target: "public:other-document",
            ..REQUEST
        };
        let result = evaluate(
            &PROGRAM,
            &different_request,
            &GovernanceFactSet { facts: &facts },
        );
        assert_eq!(result.verdict, GovernanceVerdict::Abstain);
    }

    #[test]
    fn errors_on_duplicate_or_conflicting_facts() {
        let mut facts = complete_facts(AuthorityDisposition::Permit);
        facts.push(fact(FactValue::Authority {
            layer: "publication",
            disposition: AuthorityDisposition::Forbid,
        }));
        let result = evaluate(&PROGRAM, &REQUEST, &GovernanceFactSet { facts: &facts });
        assert_eq!(result.verdict, GovernanceVerdict::Error);
    }

    #[test]
    fn errors_on_identical_duplicate_facts() {
        let mut facts = complete_facts(AuthorityDisposition::Permit);
        facts.push(facts[4]);
        let result = evaluate(&PROGRAM, &REQUEST, &GovernanceFactSet { facts: &facts });
        assert_eq!(result.verdict, GovernanceVerdict::Error);
    }

    #[test]
    fn clause_order_does_not_turn_a_missing_binding_into_a_denial() {
        let reversed_clauses = [CLAUSES[4], CLAUSES[3], CLAUSES[2], CLAUSES[1], CLAUSES[0]];
        let reversed_program = GovernanceProgram {
            clauses: &reversed_clauses,
            ..PROGRAM
        };
        let mut facts = complete_facts(AuthorityDisposition::Forbid);
        facts.remove(2);
        let fact_set = GovernanceFactSet { facts: &facts };

        let original = evaluate(&PROGRAM, &REQUEST, &fact_set);
        let reversed = evaluate(&reversed_program, &REQUEST, &fact_set);

        assert_eq!(original.verdict, GovernanceVerdict::Abstain);
        assert_eq!(reversed.verdict, GovernanceVerdict::Abstain);
    }
}
