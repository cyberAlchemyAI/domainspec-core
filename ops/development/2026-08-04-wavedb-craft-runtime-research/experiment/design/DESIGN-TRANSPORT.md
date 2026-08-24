# Design Transport

- Mode: `design`
- Architecture: `ARCHITECTURE.md`
- Scope manifest: `DESIGN-SCOPE-MANIFEST.json`
- Denominator receipt: `DESIGN-DENOMINATOR-RECEIPT.json`
- Selection result: `DESIGN-SELECTION-RESULT.json`
- Evidence state: `design-validator-pass`
- Fixed point: pass-one and pass-two digests are equal
- Selected outputs: baseline architecture plus authority/trust,
  security/abuse, state/event, persistence/concurrency,
  failure/compensation, integration/versioning, data lifecycle, quality, and
  validation contracts
- Explicitly unselected: migration/rollout and UX
- Glossary consistency: `pass`
- Design Distill: `pass`
- Plan handoff: author a high-complexity split Work Pack with WP-0 through WP-6,
  one selected provenance SWU, complete per-SWU closeout contracts, and an
  execution gate that blocks native installation until exact provenance passes.
