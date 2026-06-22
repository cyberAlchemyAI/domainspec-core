# Runtime Architecture Mapper Receipt

Agent id: `019ee093-8d2e-7a32-b32c-601bb217698c`
Role id: `runtime-architecture-mapper`
Agent name: `Grothendieck, Alexander`
Status: `flag`

## Findings

| Severity | File | Evidence | Proposed fix |
| --- | --- | --- | --- |
| major | `REFINE-DISPATCH.json` | The route says it "still needs module boundaries, interfaces, artifact ownership, and CLI command shape." | Make `SWU-PAA-001R`/`SWU-PAA-001` explicitly produce an MVP runtime architecture packet, not only contract docs. |
| major | `check-tension-sheet.md`, `DESIGN.md` | Selected route is "one toy poker game"; root design says "Kuhn and Leduc fixtures." | Decide the first executable MVP as Kuhn-only with Leduc staged, or rename the route to Kuhn+Leduc and keep both in acceptance gates. |
| major | `WORK-PACK.md`, `DESIGN.md` | Runtime code waits "until the concrete runtime root is selected"; output tree only names docs/spec/fixtures. | Add a concrete runtime root and module tree before implementation task-session: CLI, runner, protocol, referee, transcript, replay, diagnostics. |
| major | `SPEC.md`, `DESIGN.md` | Deadline defaults and clock rules are open while M0 "must freeze" timing. | Freeze soft/hard deadlines, monotonic clock source, flush start, JSON stop point, grace, timeout class, crash/EOF kill behavior, and process retirement. |
| major | `SPEC.md`, `DESIGN.md` | Public replay redaction remains open while transcript split is required. | Define exact referee transcript vs public replay schemas, including raw seed handling, seed handles/commitments, hashes, and export timing. |
| major | `REFINE-SEED-PROPOSAL.md`, `DESIGN.md` | Seed names "Minimal sample agents"; L0 output tree has no sample-agent owner. | Add `examples/agents/` and `fixtures/l0/agents/`, separating friendly sample agents from abuse fixtures. |
| minor | `AGENT-AUTHOR-GUIDE.md` | "Exact schema will be versioned" but no first runnable command exists. | Add a CLI command contract: run match, eval fixture pack, replay transcript, emit diagnostics. |

## Minimum Component Catalog

| Component | Minimum MVP responsibility | Owner boundary |
| --- | --- | --- |
| CLI | Parse agent commands, match config, seed/orbit count, output dir; expose `run`, `eval`, `replay`, `doctor`. | Owns UX and file paths, not game truth. |
| Runner | Spawn one process per seat, wire stdin/stdout/stderr, enforce env allowlist, timeouts, crash/EOF policy. | Owns lifecycle, not legal actions or scoring. |
| Protocol adapter | Serialize decision envelope, parse first stdout JSON action, validate id/version/action shape. | Owns schema and parse errors, not hidden state. |
| Referee | Own toy game state, legal actions, accepted transitions, fallback action, payout. | Owns truth; never exports raw truth to agents. |
| Transcript | Write private referee transcript and redacted public replay material. | Owns event fields and redaction split, not score coefficients. |
| Replay | Re-read transcript and reproduce accepted actions, fallbacks, payouts, diagnostics. | Owns determinism proof, not live game control. |
| Fixtures | Golden Kuhn first; Leduc only if kept in MVP; invalid, timeout, leak, fallback-abuse matrices. | Owns falsification cases, not production runtime policy. |
| Diagnostics | Compute raw EV, invalid rate, timeout rate, fallback count, replay determinism from transcript. | Owns reports, not adjusted leaderboard ranking. |
| Sample agents | Legal-random, check/fold, timeout, invalid JSON, crash/EOF. | Owns examples and abuse probes, not referee behavior. |

## Interface Gaps Or Ownership Ambiguities

- `local-kuhn-cli-mvp` conflicts with root Kuhn+Leduc M0 language.
- No selected runtime root, package boundary, language, or test root exists yet.
- CLI command surface and match config schema are not frozen.
- Runner lifecycle lacks stdout buffering, stderr redaction, crash/EOF, kill, retry, and retirement semantics.
- Fallback policy is named but not owned as a deterministic function with fixture-visible outputs.
- Transcript/replay redaction remains open despite being a replay acceptance gate.
- Diagnostics lack a stable output schema and source-of-truth rule beyond "derived from transcript."
- Sample agents are MVP-required in the seed but not owned by the current output tree.

## File-Tree Recommendation

```text
projects/poker-agent-arena/
  spec/l0/runtime/
    cli.md
    match-config.md
    process-lifecycle.md
    diagnostics-report.md
  src/poker_agent_arena/
    cli.py
    runner/process.py
    protocol/envelopes.py
    protocol/validation.py
    games/kuhn.py
    referee/core.py
    transcript/writer.py
    replay/verifier.py
    diagnostics/report.py
  fixtures/l0/
    kuhn_hidden_info/
    invalid_output_matrix/
    timeout_fallback/
    fallback_abuse/
    leak_canary/
    agents/
      legal_random.py
      check_fold.py
      timeout.py
      invalid_json.py
      crash.py
      eof.py
  examples/agents/
    legal_random.py
    check_fold.py
  tests/l0/
    test_protocol.py
    test_runner_lifecycle.py
    test_kuhn_referee.py
    test_replay.py
    test_diagnostics.py
```

## Handoff To Parent Synthesis

The runtime boundary is directionally sound but not task-session-ready. Parent synthesis should keep the selected MVP local, toy-first, and non-Hold'em, then repair the handoff by freezing one runtime root, one first toy scope, the CLI command contract, process lifecycle policy, replay/redaction schemas, diagnostics schema, and sample-agent ownership.
