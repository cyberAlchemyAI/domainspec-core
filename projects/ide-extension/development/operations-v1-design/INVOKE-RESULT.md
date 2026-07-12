# Invoke Result: Operations V1 Design

- Mode: `design`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library
- Phase status: `pass`
- Mode contract: `.agents/skills/invoke/design.md`
- Outputs: `ARCHITECTURE-BUNDLE.md`, `DECISIONS.md`, `UX-PLAN.md`,
  `GLOSSARY-CONSISTENCY.md`, `IMPLEMENTATION-LAYERING-SEED.md`,
  `DESIGN-TRANSPORT.md`, `DISTILL-VALIDATION.md`
- Design views: context, high-level structure, low-level components, workflow
  process, decision flow, dependency interface
- Glossary consistency: `pass`
- Template/profile selection: existing DomainSpec architecture-bundle pattern
  plus architecture and UX companions; eligible because the target crosses
  kernel, storage, server, session, and browser surfaces
- Dispatch techniques: recorded in `DESIGN-TRANSPORT.md`; full dispatch
  validates separately
- Distill validation: `pass` in `DISTILL-VALIDATION.md`; derive plus immutable
  replacement is the smallest coherent unit and recomposes into whole-document
  operations
- Implementation layering: `IMPLEMENTATION-LAYERING-SEED.md`
- Work-pack: n/a
- Decisions: separate surface identity, immutable blob authority, complete-
  revision commits, whole-document first, parser transformations, CAS/retry,
  separate navigation, trusted-local exception, no implicit sync
- Unresolved gaps: parser/version, body limits, blob GC, navigation durability;
  declared regions remain deferred design work
- Target artifact: Operations V1 architecture, owned by
  `projects/ide-extension`
- Next route: `invoke plan operations_v1` after design acceptance

No runtime, specification, existing V0 design, or work-pack artifact was
mutated by this Invoke design run.
