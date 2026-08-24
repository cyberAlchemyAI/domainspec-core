# Codex Goal Profile Result

- Source work-pack: `ops/development/2026-08-01-intent-route-arcanum-addon/planning/WORK-PACK.md`
- Selected unit: explicit one-shot stream `IRO-FULL-STREAM`; first frontier `SWU-IRO-001`
- Readiness: `pass` for Goal authoring; runtime execution remains not started
- Goal budget: default `4000` characters; `pass`
- Decision profile: `.arcanum/profiles/decision-profile.yml`; consumed only strictest-safe/default-deny, gated mutation, propose-then-promote, smallest-reliable, reconcile-before-act, and owner-scoped effects
- One-shot mode: yes, explicitly selected by the repaired Work Pack
- Capability policy: exact allowlist in `IRO-FULL-STREAM.md` and `EXECUTION-CONTRACT.json`; subagents off by default; terminal and joined closeout receipts required
- Sidecar profile: `planning/goals/IRO-FULL-STREAM/GOAL-SIDECAR.md`
- Native Goal: `planning/goals/IRO-FULL-STREAM/00-goal-command.md`
- Verification surface: execution-contract validator, Dispatch Spec, per-unit commands, receipt schemas, and semantic-change WPRA regeneration
- Boundaries: fixed epoch coordinator receipts plus only the separately approved current owner material scope
- Handoff pack: `planning/work-pack/session-evidence/IRO-FULL-STREAM/20260802T013311Z/CONTEXT-PACK.md` and `CONTEXT-PACK.json`
- Strict coverage: `pass`, 12/12
- WPRA v2: `pass`, `PROJECTION_READY`; selected unit none; mutation ready false; authority effect none
- Fallback exploration: named gaps only; deferred approvals are not explorable
- Extra-source reporting: required
- Stop condition: exact blocker report on a missing/stale/wrong-owner receipt, ambiguous scope, forbidden write, failed validation, second repair failure, or authority-boundary request
- Validation: compact goal budget, Context digests/coverage, execution graph, receipt paths, and WPRA receipt must all pass before handoff

## Native Goal

See [`00-goal-command.md`](00-goal-command.md). Starting it is a separate native
runtime action and is not performed by this authoring package.
