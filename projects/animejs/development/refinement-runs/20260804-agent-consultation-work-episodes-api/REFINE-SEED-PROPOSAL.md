# Refine Seed Proposal

## Intent

Define, design, and plan an agent-facing API for the existing Anime.js agent knowledge vault. Agents must be able to consult the source-bound graph while they work and append evidence-bearing work episodes so later agents can learn from concrete attempts and outcomes.

## Selected interpretation

This is two capabilities, not one read/write endpoint:

1. a read-only consultation capability over an immutable neutral projection; and
2. a separately authorized append capability over an append-only WorkEpisode event journal.

The journal is reduced deterministically into episode snapshots and candidate graph material. It never rewrites source documentation nodes directly. Closing an episode does not prove success, and no WorkEpisode automatically becomes a verified Lesson.

## Desired output

A non-executed development package containing:

- closed API and state-transition contracts;
- a six-view architecture design;
- security, identity, evidence, idempotency, concurrency, replay, and recovery rules;
- representative positive and negative scenarios;
- L0-L3 implementation layering;
- a split Work Pack with atomic SWUs and Task Session closeout synchronization contracts.

## Confirmed route

The operator confirmed the full ten-stage Refine sequence and two read-only design critics: one attacks API and authority boundaries; one attacks episode integrity and replay semantics. External research is not authorized by this confirmation.

## Scope and ceilings

- Writable during this run: this refinement-run directory plus mandatory governed dispatch ledger evidence.
- Read-only evidence: the Anime.js vault, the existing Augmentor consultation design/implementation evidence, Inventory, and current repository contracts.
- Forbidden: vault/product/runtime mutation, workspace-resonant mutation, deployment, promotion, release, public publication, Git commit, or Git push.
- Result ceiling: design and plan evidence only. No API, journal, integration, verified Lesson, deployment, or production readiness is created by this run.

## Research mode

`research-if-gap-appears`, local-first. A material external-evidence gap would require a named bounded research proposal and separate operator confirmation.
