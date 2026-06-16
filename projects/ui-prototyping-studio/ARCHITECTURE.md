---
id: ui-prototyping-studio-architecture
project: ui-prototyping-studio
title: "UI Prototyping Studio — Architecture Vision (Claude Code-native, CLI-operated)"
status: draft
node_type: architecture
updatedAt: 2026-06-15
---

# Architecture Vision

> Authored via `invoke design` from [SPEC.md](SPEC.md) + the aspect files. Lean, L0→L2, matching the
> spine altitude. Architecture decisions live in [.craft/ledger.yml](.craft/ledger.yml) (`DEC-*`); this
> document is the structure they imply, not a re-decision.

## 1. One sentence

**The studio is a governance harness around a single generation agent: Claude Code generates UI; a
`studio` CLI is the only seam; the orchestration core enforces the gates; the human disposes every
durable change.** The studio itself does *not* generate — it governs.

## 2. The shape

```
        ┌─────────────────────────── VSCode / Claude Code ───────────────────────────┐
        │  Human ──asks──▶ Claude Code ──generates HTML──▶ `studio variants register` │
        │    ▲                                                          │             │
        │    │ reviews (studio preview) + gates (CLI)                   ▼             │
        └────┼──────────────────────────────────────────────┐   ┌──────────────┐    │
             │                                               └──▶│  studio CLI  │    │
             │   operating SKILL.md teaches Claude Code           └──────┬───────┘    │
             └──────────────── the discipline ──────────────────────────┼────────────┘
                                                                         ▼
                                  ┌──────────────────── Orchestration Core ────────────────────┐
                                  │  application/ (use-cases + studio-orchestration-module)     │
                                  │  domain/ (StudioSession state machine, invariants INV-1..9, │
                                  │           deterministic synthesis)                          │
                                  │  ports: StudioSessionStorePort                              │
                                  └───────────────┬─────────────────────────────────────────────┘
                                                  ▼
                                  infrastructure/ file-backed session store (.data/)
```

There is **no MCP server, no web SPA, no API key, no in-process agent loop** in the MVP. Claude Code is
the engine; the CLI is the surface; the core is the governance.

## 3. Components & responsibilities

| Component | Responsibility | Boundary |
|---|---|---|
| **Claude Code** (in VSCode) | The generation/mutation engine: turns a prompt into 1–3 HTML variants; executes approved mutations. The *only* agentic actor. | External. Plugs in at the `variants register` / `batch apply` seams. Never approves/applies (skill-enforced + server-enforced). |
| **`studio` CLI** | The single operation surface for **both** Claude Code and the human (see [interfaces.md](interfaces.md)). Thin adapter over the orchestration module. | `interface/` layer. Holds no business rules. |
| **Operating skill** (`SKILL.md`) | Teaches Claude Code the `studio` discipline: generate → `variants register` → hand gates to the human. | Prompt-layer contract; carries no authority. |
| **Orchestration core** | The governance harness: the `StudioSession` state machine, invariants `INV-1..9`, deterministic comment→task synthesis, baseline/anchor logic. Owns *all* rule enforcement. | `application/` + `domain/`. Pure; no I/O. |
| **Session store** | Durable, file-backed session/variant/comment/batch/revision state. | `infrastructure/`, behind `StudioSessionStorePort`. `.data/`. |
| **`studio preview`** | Visual review: opens variant/revision HTML in a browser. The HTML *is* the output. | Read-only view; no gate authority. |

## 4. Layering & dependency rules (hexagonal — as it exists in code)

```
interface/  (studio CLI, [legacy] http-routes)   ── depends on ──▶ application/
application/ (use-cases, orchestration module, ports)             ── depends on ──▶ domain/
infrastructure/ (file store, newspaper adapter)  ── implements ──▶ application/ports
domain/      (models, state machine, invariants, errors)          ── depends on ──▶ nothing
```

- **Dependencies point inward.** `domain/` knows nothing of CLI, store, or Claude Code.
- **Gates live in the core, never in the adapter.** The CLI cannot bypass a gate with a flag; `batch apply` rejects non-approved / `system:auto` / stale server-side (INV-3/4/5/8).
- **Generation is external.** The core ingests *registered* variants; it does not own an LLM. This is what makes the runtime swappable.

## 5. The generator seam

The pivotal architectural choice: **generation is delegated, not embedded.**

- **Real adapter (MVP):** Claude Code produces HTML and calls `studio variants register --from <dir>`. The core validates count/shape and records `PrototypeVariant`s.
- **Test adapter:** `studio variants register --fake` (deterministic fixture) drives e2e — stable IDs, no model, no network.
- **One seam, many futures:** because the core only sees *registered variants*, alternative engines (an in-process Anthropic-SDK generator, an MCP tool, a different agent) are future adapters behind the same seam — none required now.

## 6. Data flow (the governed loop)

`session open` → `prompt submit` → **Claude Code generates** → `variants register` → `baseline select|commit`
→ `comment add` (human intent) → `synthesize` (**deterministic** fold, core-owned) → `batch approve` (human)
→ **Claude Code executes** the mutation → `batch apply` (core appends exactly one `RevisionManifestEntry`)
→ iterate or `handoff export`. Full transition contract in [states.md](states.md); semantics in [operations.md](operations.md).

**Agent proposes (generate, execute-mutation); human disposes (select, approve, apply); the core arbitrates (synthesis, invariants).**

## 7. Trust & governance architecture

Governance is the product, not a constraint bolted on:
- **Server-side gates.** Selection, approval, staleness, and non-auto-actor checks are enforced in the orchestration core (INV-3/4/5/8) — the CLI and Claude Code are untrusted callers.
- **Determinism where intent is sacred.** Comment→task synthesis is deterministic (sha1 task IDs, no timestamps), so the agent can never reinterpret the human's comments.
- **Append-only lineage.** Exactly one `RevisionManifestEntry` per apply; revision head is the staleness oracle.
- **Ergonomics-first.** The agent earns its keep on reversible work (generation); the human spends attention only at the named irreversible checkpoints.

## 8. Runtime & deployment

- **Claude Code-native, local.** Runs inside VSCode with Claude Code. No service to deploy, no key to manage, no agent loop to operate.
- **State:** file-backed under `.data/` (gitignored). Single-user, local-first.
- **Packaging:** the orchestration core + CLI ship as one backend package (`tsx`/`tsc`, fastify only if the legacy REST surface is retained); the operating skill ships as `SKILL.md`.

## 9. Extension points (deferred, each behind a named seam)

| Future | Seam it plugs into | Tracked as |
|---|---|---|
| Standalone product (own the model) | Anthropic-SDK adapter behind the generator seam | `DEC-CLI-NOT-MCP-012` note |
| Multi-client / typed tools | MCP adapter behind the same core | `DEC-RUNTIME-CLAUDE-CODE-011` note |
| Click-to-annotate web view | UI over `comment add` | `GAP-ANNOTATION-UX-006` |
| Identity/DNA + conformance-delta | new domain types + `IdentityEvidence` surface | L4 (`BLK-IDENTITY-TYPES-002`) |
| Failure/recovery states | new states + store failure-injection | L3 (`BLK-FAILURE-STATES-003`) |

## 10. Architecture decisions (pointers, not re-decisions)

`DEC-FRESH-MINIMAL-008` (lean spine, archive the rest) · `DEC-INTERFACE-MODEL-009` (human workbench +
embedded assistant) · `DEC-GENERATOR-PORT-010` (generation is a seam, not embedded) ·
`DEC-RUNTIME-CLAUDE-CODE-011` (Claude Code-native) · `DEC-CLI-NOT-MCP-012` (CLI, not MCP). Full text and
rationale in [.craft/ledger.yml](.craft/ledger.yml); human view in [CRAFT.md](CRAFT.md).
