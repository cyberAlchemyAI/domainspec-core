# CyberAlchemy v2 Goals

Status: active private package
Package owner: CyberAlchemy v2 product owner
Definition owner: definitions-governance
Visibility: private
Authority effect: none

This package keeps long-lived goals connected to their Project, product purpose,
owners, success evidence, lifecycle, and any explicitly registered parent-model
instance bindings. It answers five concrete questions:

1. Which future result are we trying to reach?
2. Which Project owns that result?
3. What evidence would show that the result was reached?
4. How does the result support the CyberAlchemy product thesis?
5. Which exact recursive-instance and construction bindings, if any, does the Project carry?

The canonical meanings are [Goal (`CAV2-D59`)](../authority/definitions/DEFINITIONS.md#cav2-d59-goal)
and [Project (`CAV2-D60`)](../authority/definitions/DEFINITIONS.md#cav2-d60-project).
The [Goal Document Type](GOAL-DOCUMENT-TYPE.md) defines the canonical artifact
contract. JSON goal files are the machine-readable source for each goal. The
ontology view is a projection; it does not replace the goal document.

## Project-owned recursive bindings

Project records use `instance_binding_refs` to name records in the closed
[Recursive Instance Binding registry](bindings/recursive-instance-bindings.json).
The registry is shaped by `CAV2-D64-SCHEMA`; it is not an authority store and
does not make a binding valid by registration. Each binding retains its exact
parent model and version, distinct model and instance authority-claim refs,
inherited contract, extension scope, adoption decision, conformance evidence,
drift and recomposition routes, and recursive stop.

The registry is currently empty. Both Projects carry empty reference lists.
`CA2-PROJECT-DEFINE` is now a real proposed `CAV2-D60` Project; the DomainSpec
minted-project under Define remains a different carrier and is not silently
treated as that Project or as a binding. The candidate authority claims and
inherited contract now exist, but their promotion, the typed model-instance
relation, owner adoption decision, conformance evidence, and recursive stop remain explicit in
[binding residue](bindings/residue.json).
The additive v1-to-v2 Project migration is recorded by
[`CAV2-PROJECT-SCHEMA-AMEND-D64-001`](ontology/project-binding-schema-amendment.json).

## Project-owned construction bindings

Project records use `construction_binding_refs` to name complete records in the
closed [ConstructionBinding registry](bindings/construction-bindings.json). The
Project named by `project_ref` owns each record. A prototype record selects an
exact tested D65 construction contract and non-authoritative ontology scaffold,
then tracks the Project's definition, product, business-ontology, DomainSpec,
compiled-graph, system-ontology, implementation, product-candidate, product-test,
and product-approval stages without inheriting any authority from them.

The registry now contains one CyberAlchemy Lab prototype binding to the exact
tested Governance D65 revision-2 contract. Only definition prototypes and the
ontology scaffold are present for the Lab product; every product-building stage
and product approval remains absent. The historical empty-registry v8-to-v9
change remains recorded by
[`CAV2-GOAL-PACKAGE-SCHEMA-AMEND-D65-CONSTRUCTION-BINDING-001`](ontology/construction-binding-schema-amendment.json),
and the non-vacuous prototype migration is recorded by
[`CAV2-GOAL-PACKAGE-SCHEMA-AMEND-D65-PROTOTYPE-CONSTRUCTION-001`](ontology/prototype-construction-schema-amendment.json).

## Binding prerequisites

Before a Project can reference a concrete binding, its prerequisite records
must exist separately from the binding itself. The
[authority-claim registry](bindings/authority-claims.json) now carries two
complete source-declared candidate `CAV2-D34` tuples: one for the parent
`cav2.define` product-meaning lane and one for the
`cav2.define.system-runtime.v1` instance lane. The same Project owns their
coordination, but it does not activate either authority claim.

The [inherited-contract registry](bindings/inherited-contracts.json) binds the
parent and instance to exact profile states. It records the current
`child-package` topology as an unresolved candidate relation, not an admitted
`CAV2-D16` model-instance relation. A separate
[admitted-relation registry](bindings/admitted-model-instance-relations.json)
records the exact directed `instance_of` admission without changing that topology record.
Every candidate and admitted record carries a canonical content
digest recomputed by the validator. The contract's adoption decision and
conformance ref are explicitly null. The v2-to-v3 package/profile change is witnessed by
[`CAV2-GOAL-PACKAGE-SCHEMA-AMEND-D64-PREREQ-001`](ontology/binding-prerequisite-schema-amendment.json).

## Adoption decision preparation

The [adoption-decision candidate registry](bindings/adoption-decision-candidates.json)
binds one no-effect decision envelope to the exact Define model-version ref,
inherited-contract digest, frozen relation candidate, and admitted relation digest.
The exact `instance_of` kind was selected and then admitted by the protected joint-owner
[admission decision](decisions/define-model-instance-relation-admission/selection.json).
The envelope remains unchanged with null adoption posture and owner decision so
its frozen digest remains independently reproducible.
The admission is only the `typed_relation` witness; it is not adoption, conformance,
binding completeness, or authority.

The protected [exact parent adoption gate](decisions/define-exact-parent-adoption/DECISION.md)
presents adopt, reject, defer, and stop for the exact frozen pre-decision envelope,
parent version, inherited-contract digest, and admitted-relation digest. The
[selection](decisions/define-exact-parent-adoption/selection.json) records the
runtime owner's `ADOPT-EXACT-PARENT-CONTRACT` choice.
Only the `CyberAlchemy v2 Define runtime owner` owns this local D48 adoption choice;
the product owner retains parent-model meaning without co-deciding local adoption.

The separate [adopted-parent-contract registry](bindings/adopted-parent-contracts.json)
projects the immutable owner decision while keeping its historical conformance ref null. A later
concrete binding must reference that decision, never the candidate envelope. The
v3-to-v4 package/profile change is
witnessed by
[`CAV2-GOAL-PACKAGE-SCHEMA-AMEND-D64-ADOPTION-CANDIDATE-001`](ontology/adoption-decision-candidate-schema-amendment.json).
The later v5-to-v6 exact-admission change is witnessed by
[`CAV2-GOAL-PACKAGE-SCHEMA-AMEND-D64-RELATION-ADMISSION-001`](ontology/model-instance-relation-admission-schema-amendment.json).
The v6-to-v7 owner-adoption change is witnessed by
[`CAV2-GOAL-PACKAGE-SCHEMA-AMEND-D48-EXACT-PARENT-ADOPTION-001`](ontology/exact-parent-adoption-schema-amendment.json).

## Conformance assessment

The [conformance-assessment registry](bindings/conformance-assessments.json)
evaluates the four exact inherited-contract terms without rewriting the frozen
candidate, adoption decision, or adopted-contract projection. Each term has
structural support, but the aggregate is deliberately `indeterminate`: the live
system-ontology validator reports DomainSpec source-currentness drift, stale
receipt currency, compiler conformance as not evaluable, and stale cross-package
residue. Consequently conformance remains not proven and binding eligibility is
denied. The v7-to-v8 change is witnessed by
[`CAV2-GOAL-PACKAGE-SCHEMA-AMEND-D64-CONFORMANCE-ASSESSMENT-001`](ontology/conformance-assessment-schema-amendment.json).

## Simple Model

```text
Product thesis
      ^
      | traced_to
      |
   Project ---- owns ----> Goal ---- evaluated_by ----> Evidence
      |                       ^
      +---- Research ---------+
      +---- Experiment -------+
                              |
                              +---- pursued_by ----> plans, tasks, experiments
```

A Goal says what future result should become true. A Project keeps that Goal
connected to the other work. Evidence lets the owner judge achievement. Plans,
tasks, and experiments may change without silently changing the Goal.

## Current Projects And Goals

- Proposed Define Project: [CyberAlchemy v2 Define](projects/define/project.json)
- Draft Define Goal: [Establish first-class Define ownership without authority collapse](projects/define/goals/define-first-class-ownership.goal.json)
- Proposed Registry Context Project: [CyberAlchemy v2 Registry Context](projects/registry-context/project.json)
- Draft Registry Context Goal: [Prove the first deterministic Registry Context vertical](projects/registry-context/goals/registry-context-first-vertical.goal.json)
- Proposed Essays Project: [Essays](projects/essays/project.json)
- Draft Essays Goal: [Build the first ontology-governed Essays writing runtime](projects/essays/goals/essays-first-runtime.goal.json)
- Project: [PythonConstraint Whole Experiment](projects/pythonconstraint-whole/project.json)
- Goal: [Prove the whole PythonConstraint experiment](projects/pythonconstraint-whole/goals/pythonconstraint-whole.goal.json)
- Ontology view: [Goal ontology](ontology/goal-view.json)
- Research: [PythonConstraint admission research](../research/projects/pythonconstraint-whole/research/pythonconstraint-admission/research.md)
- Experiment: [PythonConstraint whole experiment](../experiments/projects/pythonconstraint-whole/experiments/pythonconstraint-whole/experiment.md)

The Define, Registry Context, and Essays Projects are proposed and their Goals
are draft. They coordinate bounded meaning, ownership, and evidence requirements
without proving their intended runtimes. The PythonConstraint Goal is active and
not yet proved. Existing benchmark admission supports target selection, not
proof that the whole experiment works.

## Validate

From the repository root:

```bash
python3 cyberAlchemy-v2/goals/scripts/validate.py
```

The validator deterministically discovers every `projects/*/project.json` and
`projects/*/goals/*.goal.json` carrier and checks source digests, schema-facing
record shapes, stable IDs, Project-to-Goal closure, complete and separate D34
candidate tuples, exact-state inherited contracts, binding reference closure,
D16-shaped relation candidates, exact user-selection closure, D48-shaped
adoption-decision candidate envelopes, exact frozen-candidate and admission-decision
digest closure, one qualified admitted relation, exact protected D48 gate and owner-selection closure,
an adopted D48 posture, one exact review-only conformance assessment, one
Project-owned D65 prototype ConstructionBinding, its exact tested-contract and
scaffold closure, absent product approval, and denied authority-request eligibility,
D64 field completeness,
separate owner lanes, adoption/evaluation posture, recursive stops, ontology
endpoints, lifecycle rules, evidence links, and the authority ceiling. The
default command is check-only. Materialize one append-only receipt explicitly:

```bash
python3 cyberAlchemy-v2/goals/scripts/validate.py --write-receipt
```

The narrower D65 consumer slice can be checked independently of unrelated Goals
source drift:

```bash
python3 cyberAlchemy-v2/goals/scripts/validate_prototype_construction_binding.py
python3 -m unittest cyberAlchemy-v2/goals/tests/test_d65_prototype_binding.py
```

## Claim Ceiling

This package defines and instantiates a goal model, gives Define a proposed
Project and draft Goal, and makes Project binding prerequisites, one exact
admitted `instance_of` relation for CAV2-D16 typed-relation witnessing, and an exact
D48 parent-contract adoption decision, an indeterminate conformance assessment,
and one Project-owned prototype ConstructionBinding registered for the
CyberAlchemy Lab ontology-runtime integration Goal.
The original selected candidate remains
immutable evidence. It does not activate the
candidate authority claims, reinterpret `child-package` topology as semantic admission, treat the
candidate envelope as the owner decision, register a Define binding, treat the
Lab prototype binding as product approval, satisfy D64 or D65, treat adoption as conformance, accept or
implement a Define runtime, route live definitions, achieve either Goal,
approve a plan, authorize implementation, publish anything, deploy anything,
or prove product value.
