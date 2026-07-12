# Context Pack: SWU-MSB-005

## Selection And Sources

- Task/SWU: `TASK-BRIDGE-KERNEL / SWU-MSB-005`
- Dependency: [SWU-MSB-004](../20260712T062622Z-swu-msb-004/TASK-SESSION-RESULT.md)
- Controls: result/receipt task contract, approved architecture, v2 result and
  receipt schemas, active-claim projection, artifact containment, mutation queue
- Runtime: local Codex; no delegation

## Execution Decision

- Result endpoint accepts the schema-bound active claim/session/request fields.
- Kernel verifies all locally knowable bindings and treats resolved skill SHA-256
  as unattested session evidence; it does not resolve the skill itself.
- Only `passed`, `flagged`, and `blocked` are admitted in L0.
- Source evidence refs must resolve before any result artifact is written.
- Claim artifact is execution `before_ref`; result, terminal-after, and receipt
  artifacts are written before one atomic `bridge.result_recorded` event.
- That event consumes authorization, completes the claim, terminalizes the
  envelope, appends `skill.execution`, and makes all refs resolvable together.

## Gates And Evidence

- Active claim/recovery dependency: pass.
- Decisions/blockers: none.
- Required proof: valid terminal result; wrong session/attempt/skill/hash shape;
  missing evidence; duplicate/post-release result; interrupt race; restart;
  receipt separation and artifact resolution; append-failure nonterminal safety.
- Gate verdict: PASS.
