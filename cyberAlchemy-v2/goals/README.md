# CyberAlchemy v2 Goals

Status: active private package
Package owner: CyberAlchemy v2 product owner
Definition owner: definitions-governance
Visibility: private
Authority effect: none

This package keeps long-lived goals connected to their Project, product purpose,
owners, success evidence, and lifecycle. It answers four concrete questions:

1. Which future result are we trying to reach?
2. Which Project owns that result?
3. What evidence would show that the result was reached?
4. How does the result support the CyberAlchemy product thesis?

The canonical meanings are [Goal (`CAV2-D59`)](../authority/definitions/DEFINITIONS.md#cav2-d59-goal)
and [Project (`CAV2-D60`)](../authority/definitions/DEFINITIONS.md#cav2-d60-project).
The [Goal Document Type](GOAL-DOCUMENT-TYPE.md) defines the canonical artifact
contract. JSON goal files are the machine-readable source for each goal. The
ontology view is a projection; it does not replace the goal document.

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

## Current Project And Goal

- Project: [PythonConstraint Whole Experiment](projects/pythonconstraint-whole/project.json)
- Goal: [Prove the whole PythonConstraint experiment](projects/pythonconstraint-whole/goals/pythonconstraint-whole.goal.json)
- Ontology view: [Goal ontology](ontology/goal-view.json)
- Research: [PythonConstraint admission research](../research/projects/pythonconstraint-whole/research/pythonconstraint-admission/research.md)
- Experiment: [PythonConstraint whole experiment](../experiments/projects/pythonconstraint-whole/experiments/pythonconstraint-whole/experiment.md)

The current goal is active and not yet proved. Existing benchmark admission is
supporting evidence for target selection, not proof that the whole experiment
works.

## Validate

From the repository root:

```bash
python3 cyberAlchemy-v2/goals/scripts/validate.py
```

The validator checks source digests, schema-facing record shapes, stable IDs,
Project-to-Goal closure, ontology endpoints, lifecycle rules, evidence links,
and the authority ceiling. It writes one append-only receipt for the checked
material digest.

## Claim Ceiling

This package defines and instantiates a goal model. It does not achieve the
PythonConstraint goal, approve a plan, authorize implementation, publish
anything, deploy anything, or prove product value.
