# Craft View - ide-extension

Human view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is the source
of truth for project-local state.

## Root Context - CTX-IDEEXT-L0

**Stage:** scaffold
**Gate:** flag

**Purpose:** Prove an L0 governed IDE-adjacent workbench before claiming an IDE
agent, VS Code/VSCodium product, embedded browser automation surface, or unified
authority layer.

**Next move:** Run the L0 witness queue: validate schemas, run `npm run smoke`,
then add Playwright browser evidence over the adjacent local URL.

## Decisions

### DEC-IDEEXT-L0-BOUNDARY

Selected: local-server-first governed workbench.

Rationale: the evidence supports a loopback workbench with manifests,
approval-gated dry-run envelopes, and receipts. It does not yet support an
autonomous IDE agent or embedded VSCodium automation claim.

### DEC-IDEEXT-MODULES-NOT-KERNEL

Selected: Craft, Whisper, UI Studio, IDE Ergonomics, OpenRouter, OpenClaw,
Hermes, and ResonantOS precedents are modules/adapters, not kernel dependencies.

Rationale: kernel bloat would collapse the project into a renamed bundle of
prior surfaces instead of a distinct governed action boundary.

## Active Gaps

- GAP-IDEEXT-PLAYWRIGHT-MCP: Playwright MCP has not yet driven the local
  workbench.
- GAP-IDEEXT-VSCODIUM-WEBVIEW: embedded VSCodium webview automation is not
  locally witnessed.
- GAP-IDEEXT-MANIFEST-VALIDATOR: schemas exist, but the manifest validator is
  minimal and should grow failing invalid-fixture tests.
- GAP-IDEEXT-PROVIDER-ADAPTER: OpenRouter adapter is a boundary stub; no live
  key handling or streaming proof yet.

## Artifacts

- [README.md](README.md)
- [SPEC.md](SPEC.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [development/founding-research/research.md](development/founding-research/research.md)
- [development/founding-research/findings.md](development/founding-research/findings.md)
- [schemas/](schemas/)
- [public/demo/l0.html](public/demo/l0.html)

