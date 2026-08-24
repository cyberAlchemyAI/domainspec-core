---
id: arcanum-framework-sigil-development-and-validation-lifecycle
kind: page
type: workflow
title: Arcanum framework sigil development and validation lifecycle
updated: 2026-08-06
status: verified
confidence: high
tags:
  - inventory
  - arcanum
  - capability
  - observability
  - determinism
  - claim-le-proof
  - promotion-guardrail
sources:
  - arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md
  - arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md
  - arcanum/framework/EXPERIMENT-HARNESS-STANDARD.md
selectors:
  - '#workflow-overview'
  - '#stage-8---review-and-validation'
  - '#stage-10---promotion'
  - '#minimum-validation-matrix'
  - '#required-evidence-types'
  - '#promotion-rule'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - templates-are-starter-shapes-not-passing-evidence
  - experiment-results-require-artifact-specific-validation
  - promotion-remains-owner-gated
---

# Arcanum framework sigil development and validation lifecycle

Sigil Development is a twelve-stage lifecycle: candidate capture, tier classification, intent design, behavior contract, quality and failure design, template and artifact design, observability design, review and validation, trial execution, promotion, observation and reflection, and maintenance.

Validation experiments require a declared target, hypothesis, fixtures, environment, procedure, expected results, observed results, and verdict. The minimum matrix covers positive, negative, boundary, repeatability, and realistic-task behavior. Reproducibility requires preserving exact inputs, environment assumptions, commands, outputs, and validators.

The Experiment Harness standard keeps fixtures, prompts, outputs, run evidence, validators, and reports artifact-local. Runners must capture failures honestly, keep raw output separate from normalized verdicts, and use artifact-specific checks in addition to generic harness checks.

## Gate boundary

A passing experiment supplies promotion evidence; it does not promote a capability. Templates are reusable authoring aids, not proof that a run or implementation satisfies the lifecycle.
