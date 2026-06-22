# Define: Verification Weaver

## Intent

Create a candidate public Arcana capability named `verification-weaver` that
routes testing targets to existing evidence owners and joins their native
receipts into one parent receipt.

Smallest sound definition:

`verification-weaver routes a testing target to status-qualified evidence owners and
joins their typed receipts into one public-safe testing receipt, preserving
gaps, residue, and promotion boundaries.`

## Problem

Testing knowledge in `domainspec-core` is real but dispersed:

- deterministic DomainSpec test derivation;
- UI/UX Playwright evidence design;
- practical command runners across TypeScript, shell, Python, Playwright, and
  Arcanum fixture runners;
- architecture-to-test-gap mapping;
- research evidence sufficiency rules;
- private reference implementations that cannot be copied into public
  `arcanum`.

A reusable public tool needs to compose these lanes without stealing their
authority.

## Non-Goals

`verification-weaver` does not:

- derive tests;
- validate UX;
- execute experiments;
- map architecture;
- adjudicate research claims by itself;
- execute task sessions;
- mutate definitions;
- promote artifacts;
- copy private implementation code or examples into public `arcanum`;
- treat generated runtime evidence as canonical source.

## Glossary

- `route`: produce a typed route plan plus parent `VERIFICATION-WEAVE` receipt.
- `target classification`: finite enum with discriminants and stop conditions.
- `owner lane`: owner capability, owned verb, input contract, output receipt,
  evidence artifact, stop conditions, and promotion boundary.
- `obligation`: source-anchored, owner-scoped requirement with stable key and
  expected evidence.
- `evidence`: concrete artifact path or handle with provenance and owner.
- `gap`: missing or failed obligation/evidence with owner and next route.
- `residue`: unresolved material after routing or owner execution.
- `receipt`: structured record containing target, lanes, owner artifacts,
  status, gaps, residue, and next route.
- `adjudicate`: parent-receipt sufficiency classification only. It compares
  owner receipts against declared obligations and emits `pass`, `flag`, or
  `block`; it is not lane validation, evidence-status upgrade, promotion, or
  semantic authority.

## Source Lessons

- `arcanum/arcana/test-derivation/SKILL.md` is draft/repository-local. It owns
  the public formal derivation lane, currently status-limited to L0
  state-transition scope, and requires a round-trip oracle.
- `arcanum/arcana/ux-evidence-validator/SKILL.md` is seed/not promoted. It owns
  UX evidence contracts, browser evidence shape, and human residue, but not an
  executable calibrated validator yet.
- `arcanum/arcana/experiment-harness/SKILL.md` owns repeatable
  experiment mechanics, fixtures, run outputs, and reports.
- `arcanum/arcana/architecture-pattern-inventory/SKILL.md` owns
  architecture evidence mapping.
- `arcanum/arcana/research-evidence-harness/SKILL.md` owns research evidence
  mechanics and dry-run/live separation, but cannot upgrade claim status from
  synthetic fixtures alone.
