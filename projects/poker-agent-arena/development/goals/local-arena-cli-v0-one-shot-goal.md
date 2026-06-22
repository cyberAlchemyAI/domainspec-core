# Codex Goal Profile - Local Arena CLI v0 MVP

## Codex Goal Profile Result

- Source work-pack: `projects/poker-agent-arena/WORK-PACK.md`
- Selected unit: `WP-PAA-001` one-shot stream, ordered as `SWU-PAA-001R` through `SWU-PAA-004`
- Readiness: pass
- Goal budget: 4000 characters; pass, measured 919 characters
- Decision profile: `.arcanum/profiles/decision-profile.yml`; consumed operational effects only: default-deny outside scope, smallest reliable slice, reconcile before mutation, validate before broadening, accept recommended defaults unless unsafe, named-gap exploration, no commits/pushes/gitlink moves, stop on human-only decisions. Private profile contents were not copied.
- One-shot mode: yes
- Capability policy: `refine`, `invoke`, `craft`, `decision-gate`, and native helper subagents are allowed only through the lanes named in the sidecar; governed DomainSpec dispatches still require their own confirmation gate.
- Sidecar profile: `projects/poker-agent-arena/development/goals/local-arena-cli-v0-mvp-sidecar.md`
- Native Goal:
  ```text
  /goal Execute Poker Agent Arena Local Arena CLI v0 one-shot from projects/poker-agent-arena/development/goals/local-arena-cli-v0-mvp-sidecar.md with private policy .arcanum/profiles/decision-profile.yml: finish SWU-PAA-001R..SWU-PAA-004 inside projects/poker-agent-arena only. Pack-first; accept sidecar defaults unless contradicted or unsafe; use refine/invoke/craft/decision-gate and helper subagents only in sidecar lanes with receipts; no arcanum, implementation/domainspec, validation/poker-team, telemetry, unrelated parent writes, commits, pushes, or gitlink moves. Verify spec/docs/tests plus python -m poker_agent_arena.cli doctor/eval/replay, hidden-info canaries, invalid/timeout/fallback handling, diagnostics, replay determinism, and public replay redaction. Update Craft after gates. Stop blocked if scope widens, hidden-info/replay/diagnostics/smoke proof cannot pass, or a human-only decision is needed.
  ```
- Verification surface: `WORK-PACK.md`, `MVP-PATH.md`, `development/refinement-runs/20260619T143102Z-mvp-design/RUNTIME-HANDOFF.md`, `development/refinement-runs/20260619T143102Z-mvp-design/RESULT.md`, `development/refinement-runs/20260619T143102Z-mvp-design/evidence-index.json`, contract examples, unit tests, hidden-information canaries, and final CLI smoke for `doctor`, `eval`, and `replay`.
- Boundaries: write scope is `projects/poker-agent-arena/`; do not mutate `arcanum`, `implementation/domainspec`, `validation/poker-team`, telemetry ledgers, or unrelated parent files.
- Handoff pack: `projects/poker-agent-arena/MVP-PATH.md` and `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/evidence-index.json`
- Strict coverage: pass for goal generation; runtime proof remains required before MVP completion.
- Fallback exploration: named gaps only.
- Extra-source reporting: required.
- Stop condition: stop with a blocked report if a route-scope decision is needed, if the sidecar defaults cannot be implemented safely, if hidden-information safety cannot be proven, or if final smoke/replay evidence cannot be produced inside the bounded write scope.
- Validation: runtime executed; see `projects/poker-agent-arena/development/verification/local-arena-cli-v0/VERIFICATION.md`.
