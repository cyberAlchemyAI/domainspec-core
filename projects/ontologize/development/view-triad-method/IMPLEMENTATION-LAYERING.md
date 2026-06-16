---
module: ontologize-view-triad-method
version: current
status: draft
updatedAt: 2026-06-15
docType: implementation-layering
---

# Implementation Layering: Ontologize View-Triad Method

## Purpose

Define the decision-first layers for making the branch-materializing view triad a repeatable Ontologize method while protecting existing product docs until evidence justifies integration.

## Target And Scope

- Target: Ontologize view-triad method with B1/B2/B3/B4 materialization.
- Scope: process/method extension.
- Current state: partially implemented. Ontologize has the engagement baseline and optimization-chain method; it does not yet have the triad method artifact or pilot triad.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether the view triad can be stated as a branch-materializing Ontologize method without rewriting the existing product baseline. | Method boundary plus source inventory and Branch Materialization Register. | `VIEW-TRIAD-METHOD.md` draft, source matrix, branch register, output path decision. | Pilot triad, product-doc integration, client use. | Reviewable method boundary with B1/B2/B3/B4 coverage and no edits to product-facing docs. | Continue to pilot, narrow, or stop. |
| L1 | After this layer, we know whether the method produces a coherent branch-aware pilot triad for Ontologize itself. | Ontologize `system-view`, `engineer-view`, and `ontology-view` drafts. | Shape/stance view, decision inventory, B3 run-context record, B4 bridge ledger, typed ontology view, validation report. | Client application, public offering edits, automated validators. | Branch coverage map, stance coverage map, authority-strike results, typed edge/guard checklist. | Harden, rerun, or stop. |
| L2 | After this layer, we know whether the triad integrates safely with optimization chains and deliverables. | Integration checklist and references. | `OPTIMIZATION-CHAIN-METHOD.md` integration note, deliverable reference pattern, no-double-decision gate, branch recomposition gate. | Hosted tooling, broad registry sync, canonical promotion. | Cross-artifact validation report and sample BI claim trace through branch register. | Prepare pilot/client route or remediate. |
| L3 | After this layer, we know whether the method is repeatable across targets. | Second target or client-safe corpus run. | Repeatability checklist, routing guide, signals/reflection. | Production tooling and external publication. | Two runs with comparable branch validation receipts and no source leakage. | Package for pilot, defer, or promote through owner-approved route. |

## Non-Regression Guardrails

- Existing Ontologize product and public offering docs remain unchanged until L0 passes.
- The optimization-chain method remains the BI-expression layer.
- The view triad never decides twice: shape, verdict, term meaning, and BI claim each have one home.
- Branch definitions stay in `ONTOLOGY-BRANCHES.md`; this pack only records coverage and execution gates.
- B3 run-context and B4 bridge evidence are publication-blocking gates, not optional explanatory color.
- Promotion decisions cite layer evidence, not preference.
- Public/private boundary remains intact; `implementation/domainspec` sources are private submodule content unless separately approved.

## Recommended Next Layer

- Next layer: L0.
- Key decision unlocked: whether the method extension is branch-complete, safe, and precise enough to pilot.
- Major deferred scope: client application and product-facing integration.
