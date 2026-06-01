---
title: GoldenQuill Promotion Governance Vocabulary Revision Proposal
date: 2026-06-01
status: proposed
observed_capability: invoke
invoke_mode: design
---

# GoldenQuill Promotion Governance Vocabulary Revision Proposal

## Purpose

Keep implementation-facing GoldenQuill promotion governance artifacts in
GoldenQuill-native language.

The architecture may keep historical research receipts in findings ledgers, but
new design, proposal, validator, fixture, task-session, and implementation docs
should avoid external method vocabulary that does not belong to the grant
product surface.

## Keep

Use these terms:

- application stage;
- final outcome;
- validation state;
- evidence packet;
- source-backed event;
- grant outcome event;
- KPI observation;
- stage-depth score;
- promotion candidate;
- owner decision;
- governance layer;
- approved allowed uses;
- proposed allowed uses;
- redaction/generalization gate;
- org-scoped feedback;
- workspace-safe learning.

## Replace

| Avoid In Active Design | Use Instead |
| --- | --- |
| external method transfer | grant evidence-state discipline |
| mathematical verification label | validation state |
| research-ending label | final outcome field |
| formal validator analogy | GoldenQuill validator rule |
| research-method vocabulary | grant workflow vocabulary |

## Revision Scope

Apply this vocabulary revision to:

- architecture designs;
- proposals;
- refine seeds;
- task-session handoffs;
- validator docs;
- fixture names;
- implementation comments;
- dashboards.

Do not rewrite raw research findings only to hide source history. If an older
finding cites an external source, leave it as evidence history unless it is
being promoted into active architecture language.

## Acceptance Criteria

- New architecture/proposal artifacts have no external method vocabulary.
- Active promotion-mechanism artifacts use `application stage`, `final outcome`,
  and `validation state`.
- Validator fixture names are GoldenQuill-native.
- Any future task-session uses this vocabulary policy as an input.
