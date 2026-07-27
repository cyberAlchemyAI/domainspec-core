# Invoke Design Transport

## Source Contracts

- `SPEC.md`
- `GLOSSARY.md`
- `DECISIONS.md`
- `CONTEXT.md`
- `../2026-07-25-co-op-engine-portfolio-research/findings.md`

All are bound by exact digests in `DESIGN-SCOPE-MANIFEST.json`.

## Outputs

- `ARCHITECTURE-BUNDLE.md`
- `UX-PLAN.md`
- `DEPENDENCY-INTERFACE-MAP.md`
- `DESIGN-DECISIONS.md`
- `DESIGN-RISKS.md`
- `GLOSSARY-CONSISTENCY.md`
- `DESIGN-PLANNED-WITNESSES.json`
- `DESIGN-DISTILL-VALIDATION.md`
- `DESIGN-DISPATCH-TRACE.md`
- `DESIGN-DENOMINATOR-RECEIPT.json`
- `DESIGN-SELECTION-RESULT.json`

## Gate State

- Six required views: authored.
- Design selection: `pass`.
- Fixed point: true.
- Evidence state: `design-validator-pass`.
- Selected outputs: 12, including baseline architecture, UX plan, and validation
  contracts.
- Glossary consistency: pass.
- Distill: pass.
- Implementation layering: seed authored in the architecture bundle.
- Plan evidence: pending.
- Implementation/deployment: not authorized.
- Public release: blocked on audits and D-005.

## Next Handle

```text
invoke:
  next_stage: acceptance-review
  if_accepted: plan
  target: co-op-engine-browser-app
  implementation_home: projects/co-op-engine
  recommended_first_unit: SWU-COOP-001
  evidence_ceiling: design-validator-pass
```

## Transport Boundary

No matching Necronomicon product section exists, so Design does not create or
promote one. This report is the local handoff authority. Normal Invoke Plan may
consume only the exact artifacts above plus the acceptance-review result.
