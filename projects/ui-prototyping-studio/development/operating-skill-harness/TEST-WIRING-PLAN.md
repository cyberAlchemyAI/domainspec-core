---
id: operating-skill-test-wiring-plan
project: ui-prototyping-studio
title: "Plan — test the operating SKILL, wire it into the project, run a first test"
status: proposal
node_type: implementation-plan
invoke_mode: plan
complexity: medium
target_artifact: operating SKILL (operating-contract) + its harness
updatedAt: 2026-06-17
---

# Plan — test the SKILL → wire it in → first test

Three phases: **(P1) test** the SKILL's behavior via the harness on a real transcript; **(P2) wire** it
into the project (capture adapter + test surface + install, gated); **(P3) first test** — executed in this
run. Planning artifact; the first test is then actually run.

## Standing constraints (carried)

- The SKILL is the **sole control on agent self-disposal** (F2/`GAP-CORE-IDENTITY-GATE-010`: the core has
  no human-vs-agent identity gate). So the harness is the **compensating control** — it must be green
  before the SKILL installs live, and live install also waits on the F2 decision (`PLAN-FIXES.md`).
- The studio CLI is operational (verified: `session open` returns a session; tsx run). `variants generate`
  is the stub generator; real `variants register` (HTML with `data-od-id`) needs live Claude Code generation.

## SWU manifest

| SWU | Title | Depends on | Write scope | Acceptance |
|-----|-------|-----------|-------------|------------|
| **TW1** | Live-capture adapter | harness | `operating-skill-harness/capture-session.sh` | runs a studio verb under a given `STUDIO_ACTOR`, appends one transcript JSONL line `{actor,verb,args,narration}` |
| **TW2** | First test (live capture → harness) | TW1, studio CLI | run only (transcript under `example-runs/`, report under `runs/`) | a real SKILL-honoring session transcript scored by the runner; report recorded |
| **WW1** | Wire harness into project test surface | TW2 green | `backend/package.json` (or root) `test:skill` script | `pnpm test:skill <transcript>` runs the runner; non-zero on block/fail |
| **WW2** | M2 coverage on the real register path | TW1 | capture adapter + runner | capture the generated/registered variant HTML so M2 (`data-od-id`) is actually exercised, not skipped |
| **WW3** | Install the SKILL live (GATED) | harness green + F2 decided | project `SKILL.md` or `.claude/skills/ui-prototyping-studio/SKILL.md` | promote `06-SKILL-draft.md` (post Quality-bar/F1/F3 fixes) only after WW1 green AND `DEC-UX-REVIEW-FIX-BEFORE-BUILD-023`/F2 cleared |

## Per-SWU detail

### TW1 — live-capture adapter `[script]`
- **Inputs:** actor, verb, verb-args. **Output:** the verb's stdout + one appended JSONL transcript line.
- **Rules:** set `STUDIO_ACTOR=<actor>`; run `tsx src/cli/studio.ts <verb> <args>`; record `{actor, verb,
  args:{selector,elementLabel,odId,label,...}, narration}`; never invent narration. **Verify:** a 1-verb
  run appends a well-formed line the runner can parse.

### TW2 — first test (executed in this run)
- Drive a SKILL-honoring loop: agent → `session open`, `prompt submit`, `variants generate`; human →
  `baseline select|commit`, `comment add`; agent → `synthesize`; human → `batch approve`, `batch apply`.
  Each invocation captured via TW1 → transcript. Run `run-validation-fixtures.sh <transcript>`.
- **Verify:** a report under `runs/` with `RESULT`, `QUALITY_BAR_STATUS`, `ANTI_PATTERN_HITS_JSON`. Expected:
  M1 pass (agent never gates), M3 pass, M4 pass, M5 pass; **M2 not exercised** by the stub path (→ WW2).

### WW1 — project test surface
- Add `"test:skill": "bash development/operating-skill-harness/run-validation-fixtures.sh"` (path-adjusted).
  **Verify:** `pnpm test:skill <transcript>` exits non-zero on a known-violation transcript.

### WW2 — M2 on the real path
- The stub `variants generate` doesn't surface HTML in args, so M2 (`data-od-id`) is skipped. Fix: the
  capture adapter records the registered variant's `htmlArtifactRef`/HTML, and the runner checks `data-od-id`
  there. **Verify:** a register event with stamped HTML passes M2; one without fails.

### WW3 — install (GATED, not now)
- Promote the corrected `06-SKILL-draft.md` to the live skill location **only after** WW1 is green and the
  F2 identity-gate decision is resolved (the SKILL is the sole control; installing it before the harness is
  green would ship the control unverified). **Verify:** live `SKILL.md` present; harness green; F2 decided.

## Implementation-layering

- **L0 — harness runs (done):** runner self-tested (pass/violation). Promotion = a green report.
- **L1 — live capture (TW1/TW2):** real transcript from the real CLI. Promotion = a recorded run report.
- **L2 — wired into project (WW1/WW2):** `test:skill` script + M2 coverage. Promotion = non-zero on violation, M2 exercised.
- **L3 — install (WW3):** gated on L2 green + F2. Promotion = live SKILL + green harness + F2 decided.

## Validation strategy (per slice)

TW1 → parse-check one line · TW2 → a real runner report · WW1 → exit-code check on a violation transcript ·
WW2 → M2 pass/fail fixtures · WW3 → presence + harness-green + F2-decided gate.

## Next route

`task-session` per SWU (TW1 → TW2 now → WW1/WW2 → WW3 gated). This run executes **TW2 (first test)** below.
