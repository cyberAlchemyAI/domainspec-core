# Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `arcanum/spells/invoke/design.md`
- Outputs: `ARCHITECTURE-BUNDLE.md`, `UX-PLAN.md`,
  `GLOSSARY-CONSISTENCY.md`, `DESIGN-TRANSPORT.md`
- Design views: context, high-level structure, low-level components, workflow
  process, decision flow, dependency interface
- Design selection receipt: `DESIGN-SELECTION-RESULT.json`
- Design evidence state: `design-validator-pass`
- Evidence ceiling: Design validation only; Plan evidence is separate
- Plan evidence: `plan-evidence-pending`
- Template/profile selection: DomainSpec architecture profile plus Architecture
  and UX companions
- Dispatch techniques: sequence, artifact-contract bridge, owner-boundary
  check, concrete-path evidence, validation loop, residue ledger, handle
  handoff, observability grouping
- Distill validation: pass; Poker shared-record contract is the smallest
  coherent first unit
- Implementation layering: seed in `ARCHITECTURE-BUNDLE.md`
- Work-pack: n/a
- Decisions: one dedicated React/TypeScript/Vite application; build-time
  admitted records; projection before rendering; separate card and
  collaboration state; versioned gateway boundary; restricted-first rollout
- Unresolved gaps: D-005 publication owner, executed audits, durable gateway
  technology at L2, final Whisper/project-owner copy
- Next route: acceptance review, then Plan if accepted
