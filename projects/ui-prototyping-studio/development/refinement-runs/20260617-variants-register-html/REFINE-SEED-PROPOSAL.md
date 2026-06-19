---
id: refine-seed-variants-register-html
project: ui-prototyping-studio
title: "Refine Seed — the missing `variants register` HTML-ingestion capability (WW2)"
status: seed
node_type: refine-seed
run_id: 20260617-variants-register-html
updatedAt: 2026-06-17
---

# Refine Seed — variants register HTML ingestion

## Target

The WW2 blocker: the studio cannot register **real** variant HTML. The stub `generateVariants`
(`generate-variants.ts:56`) emits a dangling `htmlArtifactRef` path with no HTML body and no
`data-od-id`, and the CLI `variants register` just calls that stub. So there is no real content for
preview/annotation/mutation, and M2 (`data-od-id`) is structurally unprovable.

## Source context (local-first)

- `application/artifact-content-port.ts` (M0b: `readHtml`/`stageHtml`/`commitHtml`/`discardStagedHtml`, content-addressed).
- `domain/canonicalize.ts` (M0c: deterministic canonicalizer + hash).
- `domain/models.ts` (`PrototypeVariant.htmlArtifactRef`), `application/generate-variants.ts`, `cli/studio.ts`.
- `development/operating-skill-harness/` (M2 needs real HTML), `WORK-PACK.md` ("real generation = Claude Code via variants register, M-later").

## What this run must produce

- An **x-ray** of the generate→register→content-port→variant-ref→annotate seam.
- A **tournament** of HTML-ingestion interfaces (file/dir/stdin/manifest).
- A **dialectic** on `data-od-id` responsibility (agent-stamps vs core-validates), resolved.
- A **toy-game** design: register with/without `data-od-id` → does the gate fire?
- A build-ready **SWU** (non-executed) that lifts WW2 and exercises M2.

## Run parameters

- Preset standard · Research no-research (all local) · Subagents recommended → run **inline** (confirmed).
- Write scope: this run folder. Building is a later `task-session`.
- Validation surface: the toy-game falsification + the M0b/M0c reuse check.
