# UI Prototyping Studio

Accountable UI exploration: generate 1–3 bounded variants → intentionally select a baseline → annotate with canonical comments → synthesize a deterministic mutation draft → **explicit human approval** → apply → append-only revision manifest → hand off. Governance is a feature, not friction; **ergonomics is the first principle**.

This is a **standalone project** (extracted from the now-deprecated `domainspec` monorepo). It is deliberately scoped to what is real and buildable today.

## What's here

| Path | What it is |
|------|-----------|
| [SPEC.md](SPEC.md) | **Lean spec** — the L0→L2 survival/trust floor (this release). The buildable contract. |
| [CRAFT.md](CRAFT.md) · [.craft/](.craft/) | Craft ledger — live project state (contexts, decisions, blockers, gaps). Source of truth = `.craft/ledger.yml`. |
| [development/deep-spec-dispatch/](development/deep-spec-dispatch/) | The deep-spec exploration that produced the design + plan + readiness verdict ([RESULT.md](development/deep-spec-dispatch/RESULT.md), [DEEP-SPEC-PROPOSAL.md](development/deep-spec-dispatch/DEEP-SPEC-PROPOSAL.md), [ONE-SHOT-IMPLEMENTATION-PLAN.md](development/deep-spec-dispatch/ONE-SHOT-IMPLEMENTATION-PLAN.md)). |
| [development/standalone-extraction/](development/standalone-extraction/) | The plan to bring the code over and make this project runnable. |
| `provenance/` | Archive, not spine: the 19-doc full-vision DomainSpec spec (`legacy-domainspec-spec/`) and a vendored design-skills reference tree (`open-design-reference/`). Mine for detail; do not treat as current. |

## Scope (this release): L0→L2

Per the deep-spec readiness verdict, only **L0** exists in code (the 10-state session machine + governance enforcement). This release hardens that working floor:

- **L0** — the working exploration loop + governance invariants (auto-apply forbidden, approval-before-apply, append-only manifest, variantCount 1–3).
- **L1** — accessibility (keyboard, ARIA, focus, labels).
- **L2** — layout integrity (no overflow/clip/overlap, target size, responsive).

**Deferred** (design only, see `development/deep-spec-dispatch/`): L3 interaction-flow gates · L4 identity/DNA + conformance-delta · L5 fitness scoring · L6 human-evidence/trust. Plus open questions OQ-1..4.

## Status

- Spec spine + Craft ledger: **in place**.
- Code (backend + web + e2e): **extraction pending** — see [development/standalone-extraction/EXTRACTION-PLAN.md](development/standalone-extraction/EXTRACTION-PLAN.md). The backend module is a clean lift (node + fastify); the frontend is plain React + Vite + CSS.

## Running (after code extraction)

```bash
pnpm install
pnpm build      # backend (tsc) + web (vite)
pnpm test       # backend node:test slice tests
pnpm test:e2e   # playwright (wp01 / wp02wp03)
```
