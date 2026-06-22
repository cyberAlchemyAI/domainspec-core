# Local Arena CLI v0 MVP Sidecar

This sidecar is the dense execution frame for the compact native Codex goal in
`local-arena-cli-v0-one-shot-goal.md`. The `/goal` line carries control; this
file carries the work-pack navigation, defaults, capability lanes, and stop
rules.

## Objective

Deliver the Poker Agent Arena MVP: a local CLI arena that runs a Kuhn
hidden-information fixture end to end against sample agent processes, writes
private transcript material, exports redacted public replay, replays
deterministically, and reports clean EV beside fallback-inclusive EV, invalid
rate, timeout rate, fallback count, and replay determinism.

## Source Frame

Read these first, in order:

1. `projects/poker-agent-arena/MVP-PATH.md`
2. `projects/poker-agent-arena/WORK-PACK.md`
3. `projects/poker-agent-arena/SPEC.md`
4. `projects/poker-agent-arena/AGENT-RULES.md`
5. `projects/poker-agent-arena/RULES.md`
6. `projects/poker-agent-arena/.craft/ledger.yml`
7. `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/RUNTIME-HANDOFF.md`
8. `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/RESULT.md`
9. `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/evidence-index.json`

Broaden only for a named gap in `MVP-PATH.md`, `WORK-PACK.md`, or this sidecar.
Report each extra source, which gap it answered, and whether it changed the
implementation.

## Runtime Decision Profile Policy

Use `.arcanum/profiles/decision-profile.yml` as a private runtime policy file.
Consume only operational effects needed for this goal; do not copy profile
contents into public docs, reusable examples, or canonical skill/package text.

For this one-shot, the consumed policy is:

- default-deny outside the named write boundary;
- smallest reliable slice first, but execute the full selected stream in order;
- reconcile existing artifacts before code mutation;
- validate one layer before broadening to the next;
- accept recommended defaults unless local evidence makes a default unsafe;
- use named-gap exploration only, with final reporting for every extra source;
- no commits, pushes, parent gitlink moves, or public-submodule edits;
- stop on silent scope widening, hidden-information uncertainty, untestable
  claims, or any need for a human-only decision.

## Selected Stream

Execute one stream only:

1. `SWU-PAA-001R` - repair the handoff and make the defaults executable.
2. `SWU-PAA-001` - freeze the versioned Local Arena CLI v0 contract.
3. `SWU-PAA-002` - implement the local CLI runner and Kuhn fixture gate.
4. `SWU-PAA-003` - add replay, redaction, and diagnostics acceptance.
5. `SWU-PAA-004` - add author proof, sample agents, and quickstart proof.

Runtime code starts only at `SWU-PAA-002`.

## MVP Defaults

Treat these defaults as selected for this MVP run unless an inspected source
contradicts them or implementation proves them unsafe:

- Runtime language/root: Python package under `src/poker_agent_arena/`.
- CLI namespace: `paa`.
- CLI commands: `paa doctor`, `paa run`, `paa eval`, `paa replay`.
- First fixture gate: Kuhn hidden information.
- Decision timeout: `5000ms`.
- Process cleanup timeout: `10000ms`; cleanup only, not accepted action time.
- Clock: monotonic.
- Deadline start: after the arena flushes the decision envelope to agent stdin.
- Deadline stop: first complete stdout JSON object.
- Late output: timeout event; ignored for gameplay.
- Invalid output: deterministic fallback per invalid decision; no match
  retirement in v0 unless a fixture explicitly tests retirement as a post-MVP
  extension.
- Public replay: opaque seed handles; raw seed material stays referee-only.
- First proof orbit: tiny deterministic smoke orbit, with fixture-config support
  for larger orbits later.
- Fallback: passive deterministic legal action order: `check`, `fold`, `call`,
  then minimum legal wager action by rule-defined order.
- MVP scoring: clean EV, fallback-inclusive EV, invalid rate, timeout rate,
  fallback count, replay determinism.
- Leduc, Hold'em engine parity, adjusted leaderboard scoring, and novelty
  mechanics remain deferred.

`SWU-PAA-001R` should reconcile these defaults back into the scoped Craft ledger
as accepted execution defaults or explain why a default became unsafe.

## Capability Lanes

- `refine`: use only to repair a named design or plan gap that blocks the
  selected stream.
- `invoke`: use only to author missing define/design/plan/handoff artifacts
  explicitly required by `WORK-PACK.md` or `MVP-PATH.md`.
- `craft`: update `projects/poker-agent-arena/.craft/ledger.yml` and
  `projects/poker-agent-arena/CRAFT.md` after each meaningful gate with closed
  defaults, new blockers, residual gaps, artifacts, and next move.
- `decision-gate`: use only if a default above becomes unsafe or contradictory.
  If the gate cannot resolve from local evidence, stop and report the exact
  decision needed.
- Native helper subagents: allowed for non-overlapping review, fixture audit,
  test diagnosis, or implementation slices when the parent can verify their
  diffs and checks. Require role receipts in the final report. Subagents may not
  widen scope, mutate outside `projects/poker-agent-arena/`, or skip parent
  verification.
- Governed DomainSpec dispatches: do not register or run without the explicit
  human confirmation required by `domainspec-subagents-strategy`.

## Output Tree

Before MVP completion, create or update:

```text
projects/poker-agent-arena/
  spec/l0/runtime/
  spec/l0/protocol/
  spec/l0/transcript/
  spec/l0/diagnostics/
  spec/l0/fixtures/
  spec/l0/state-namespaces.md
  src/poker_agent_arena/
  examples/agents/
  fixtures/l0/
```

Keep friendly sample agents under `examples/agents/`. Keep adversarial
validation material under `fixtures/l0/`.

## Verification

Use the narrowest checks available after each SWU. Final proof must include
commands equivalent to:

```sh
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli doctor
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli eval --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/check_call.py --agent-b projects/poker-agent-arena/examples/agents/legal_random.py --out projects/poker-agent-arena/.tmp/smoke
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli replay projects/poker-agent-arena/.tmp/smoke/private-transcript.jsonl --out projects/poker-agent-arena/.tmp/smoke/replay
```

Also verify:

- agent-visible observations never include opponent card, deck order, raw seed,
  future state, referee trace, or reversible hidden-state hash;
- invalid output, timeout, crash, and EOF produce named diagnostics and
  deterministic fallback;
- `paa replay` reproduces accepted actions, fallback events, payouts, and
  diagnostics from private transcript material;
- public replay export follows `spec/l0/transcript/redaction-policy.md`;
- fallback and invalid-output behavior cannot improve displayed rank in the
  bundled abuse fixtures;
- author quickstart works from a fresh checkout without hidden local assumptions.

## Stop Conditions

Stop with a blocked report if:

- completing the MVP would require widening beyond Kuhn-first Local Arena CLI v0;
- a default in this sidecar becomes unsafe and cannot be resolved locally;
- hidden-information safety cannot be proven;
- the referee transcript and public replay split cannot be kept separate;
- final doctor/eval/replay smoke cannot pass inside `projects/poker-agent-arena/`;
- implementation requires mutating `arcanum`, `implementation/domainspec`,
  `validation/poker-team`, telemetry ledgers, or unrelated parent files.
- a needed decision is human-only under the runtime decision profile.

## Final Report

Report:

- SWUs completed and artifacts created;
- defaults accepted, changed, or blocked;
- Craft rows updated;
- decision-profile policy effects applied, without copying private profile text;
- extra sources used and the named gap each answered;
- helper subagents used, with role receipts;
- validation commands and outcomes;
- any remaining blockers or residue.
