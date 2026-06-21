---
tags: [inventory, verification-weaver, evidence-card, promotion-guardrail]
node_type: evidence-card
is_session: false
layer: research
nature: reference
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-verification-weaver-research
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-21-verification-weaver/
sources:
  - ops/development/verification-weaver/research/2026-06-21-verification-weaver-research/findings.md
  - ops/development/verification-weaver/development-package/WORK-PACK.md
---

# Evidence Cards: Verification Weaver

## Card VW-CARD-001

- ID: `VW-CARD-001`
- Status: candidate
- Claim or candidate: `verification-weaver` is a candidate public Arcana
  testing-specific router and parent receipt contract.
- Source refs:
  - `ops/development/verification-weaver/research/2026-06-21-verification-weaver-research/findings.md`
  - `ops/development/verification-weaver/development-package/DEFINE.md`
- Authority level: Inventory candidate read model.
- Promotion owner: `sigil-development`
- Trace: extracted from subagent synthesis plus auditor-repaired findings; the
  card records the candidate route only and does not create public sigil
  authority.
- Residue: public package is not implemented or promoted.

## Card VW-CARD-002

- ID: `VW-CARD-002`
- Status: candidate
- Claim or candidate: owner lanes must remain status-qualified and cannot be
  absorbed by the parent receipt.
- Source refs:
  - `arcanum/arcana/test-derivation/SKILL.md`
  - `arcanum/arcana/ux-evidence-validator/README.md`
  - `arcanum/arcana/experiment-harness/SKILL.md`
  - `ops/development/verification-weaver/development-package/IMPLEMENTATION-LAYERING.md`
- Authority level: Inventory candidate read model.
- Promotion owner: owning capability for each lane; `sigil-development` for the
  future parent package.
- Trace: auditor repair required draft/seed/status-limited wording before
  handoff readiness.
- Residue: exact owner receipts will exist only after public fixtures and
  validator are implemented.

## Card VW-CARD-003

- ID: `VW-CARD-003`
- Status: candidate
- Claim or candidate: public package validation must include negative controls
  for mixed, unsupported, private, generated-only, no-oracle, UX-human,
  UX-density, flaky E2E, adapter, research dry-run, architecture folder-only,
  and parent-promotion cases.
- Source refs:
  - `ops/development/verification-weaver/development-package/negative-controls/NEGATIVE-CONTROLS.md`
  - `ops/development/verification-weaver/development-package/QUALITY-BAR.md`
- Authority level: Inventory candidate read model.
- Promotion owner: `experiment-harness` for validation evidence;
  `sigil-development` for package promotion.
- Trace: Bell counterexample gate required negative controls to fail closed;
  auditor repair required runnable-case fields.
- Residue: the controls are authored as requirements; they are not validation
  evidence until implemented and run.

## Card VW-CARD-004

- ID: `VW-CARD-004`
- Status: candidate
- Claim or candidate: private implementation evidence is internal-only and must
  be excluded from public fixtures, examples, and proof claims.
- Source refs:
  - `ops/development/verification-weaver/research/2026-06-21-verification-weaver-research/research.md`
  - `ops/development/verification-weaver/development-package/IMPLEMENTATION-LAYERING.md`
  - `arcanum/arcana/test-derivation/SKILL.md`
- Authority level: Inventory candidate read model.
- Promotion owner: `sigil-development` plus public/private boundary review.
- Trace: public `test-derivation` says the private engine is design reference
  only; auditor required split internal evidence from public package text.
- Residue: future task-session must run private-path and generated-output scans.
