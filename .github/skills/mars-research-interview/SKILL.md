---
name: mars-research-interview
description: 'Interview a greenfield or brownfield research effort to discover scope, inspect existing evidence, generate counterarguments, and produce MARS-ready hypotheses and experiment candidates.'
argument-hint: '[greenfield|brownfield|auto] [research-project-or-topic]'
agent: mars-research-interviewer
allowed-tools: Read, Write, Glob, Grep, AskQuestions
---

<objective>
Convert a vague research direction or a partially executed research effort into a MARS-ready scope baseline.

This skill helps researchers and business operators bring context into the open, stabilize terminology, produce candidate hypotheses, surface counterarguments, and identify experiments that are worth formal protocol design.
It also establishes the definitions authority pattern early: canonical semantics in `definitions/DEFINITIONS.md`, lookup in `definitions/DEFINITIONS-INDEX.md`, and papers as condensed synthesis artifacts.
</objective>

<when-to-use>
Use this skill when:
- a research direction exists but the scope is still fuzzy
- a project already has claims, runs, or artifacts and needs a brownfield scoping pass
- the team needs initial hypotheses, propositions, and experiment candidates before planning execution
- a business owner wants to test a strategic intervention, such as pricing, onboarding, or positioning, with disciplined counterarguments
</when-to-use>

<inputs>
Primary inputs:
- `research/projects/mars/**`
- target research project docs, runbooks, results, data, and claims
- operator answers gathered during the interview

Key MARS references:
- `research/projects/mars/PROJECT.yaml`
- `research/projects/mars/claims/CLAIMS.md`
- `implementation/mars/definitions/MARS-PIPELINE.md`
- `research/projects/mars/results/MARS-EVIDENCE-STATUS.md`
- `implementation/mars/templates/project-overview-template.md`
- `implementation/mars/templates/initial-definitions-template.md`
- `implementation/mars/templates/hypotheses-template.md`
- `implementation/mars/templates/experiment-candidates-template.md`
</inputs>

<process>
1. Read the core MARS references first.
2. Detect mode.
   - `greenfield`: no stable protocol or evidence baseline exists.
   - `brownfield`: claims, data, results, or implementation already exist.
   - `auto`: inspect and choose.
3. Build a cheap evidence baseline.
   - For brownfield, inspect current artifacts before asking avoidable questions.
   - For greenfield, capture problem statement, decision owner, unit of analysis, intervention ideas, constraints, and success metrics.
4. Run the interview.
   - Ask focused questions about hypotheses, competing explanations, available evidence, operator constraints, and what decision the experiment should change.
5. Draft four core artifacts.
   - `research/projects/<project>/PROJECT-OVERVIEW.md` from `implementation/mars/templates/project-overview-template.md`
   - `research/projects/<project>/definitions/DEFINITIONS.md` as the canonical definitions source
   - `research/projects/<project>/definitions/DEFINITIONS-INDEX.md` as the definition ID lookup and traceability map
   - `research/projects/<project>/definitions/INITIAL-DEFINITIONS.md` from `implementation/mars/templates/initial-definitions-template.md` as optional ideation notes
   - `research/projects/<project>/claims/HYPOTHESES.md` from `implementation/mars/templates/hypotheses-template.md`
   - `research/projects/<project>/experiments/EXPERIMENT-CANDIDATES.md` from `implementation/mars/templates/experiment-candidates-template.md`
6. Add counterarguments and falsifiers.
   - Each hypothesis should list at least one counterargument, one confounder, and one disconfirming outcome.
7. Finish with a readiness verdict.
   - `ready for protocol design`
   - `needs more discovery`
   - `blocked on scope or evidence`
</process>

<quality-bar>
- Separate `observed`, `stated`, and `hypothesized` material.
- Brownfield findings must be grounded in existing artifacts where possible.
- Hypotheses must be falsifiable and decision-relevant.
- Experiment candidates must include signal, expected effect, and invalidation condition.
- Canonical terms and IDs should be authored in `definitions/DEFINITIONS.md` and `definitions/DEFINITIONS-INDEX.md`; avoid treating paper text as normative definitions.
- Recommendations must say when not to run an experiment yet.
</quality-bar>

<examples>
- `/mars-research-interview greenfield strategy experiments for early-stage SaaS pricing`
- `/mars-research-interview brownfield audit current MARS evidence around technique specialization`
- `/mars-research-interview auto bring context and counterarguments for onboarding funnel experiments`
</examples>