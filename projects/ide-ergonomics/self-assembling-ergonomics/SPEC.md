# SPEC - Self-Assembling Ergonomics Action

Status: flagship strategy artifact; no runtime implementation
Date: 2026-06-23
Owner if pursued: IDE Ergonomics host-surface owner plus Spellcraft / Sigil Development
Builds on: [README.md](README.md)
Route contract: [self-assembling-ergonomics.dispatch.json](self-assembling-ergonomics.dispatch.json) (validated)

## 1. Problem

The [ERGONOMICS-OPPORTUNITIES.md](../ERGONOMICS-OPPORTUNITIES.md) map is a document
a human reads, prioritizes, and then hand-builds. Each improvement still costs a
full author → design → plan → build → test cycle the user has to drive. The map
grows faster than a person can work it.

The opportunity is to let the surface run that cycle on itself: pick an evidenced
candidate, assemble it, test it, and bring back a finished thing to judge. The
danger is the same fact stated differently: a surface that can build and test
itself can ship itself. This spec exists to capture the loop **and** the gate that
keeps the human as the only authority that can promote.

## 2. Primitive

`self-assembling-ergonomics` is a meta composition primitive with six linked
models, each owned by an existing capability:

1. `candidate_suggestion` - one evidenced improvement drawn from the map plus
   observed friction telemetry. (`inventory` / `observability` / `signal-observer`)
2. `scoped_start` - explicit, bounded user consent to assemble a named candidate.
3. `isolated_assembly` - define/design/plan and owner-lifecycle drafts produced in
   an isolated candidate space. (`invoke` → `spellcraft` / `sigil-development`)
4. `preregistered_criterion` - an acceptance criterion frozen **before** any test
   run. (`experiment`)
5. `self_test_result` - the run verdict against that frozen criterion.
   (`experiment-harness`)
6. `approval_promotion` - the user-run test, the approval decision, and the
   owner-routed promotion with a receipt. (`decision-gate` → owning capability)

## 3. The Loop

```text
suggest -> scoped start -> isolated assembly -> preregister criterion
       -> self-test -> notify -> user test + approve -> owner-routed promotion
```

The load-bearing invariant across all six models:

> **Assembled and green is not shipped.** Models 1–5 may run autonomously. Model 6
> is the only model that mutates anything outside the candidate space, and it
> requires the user-run test and an explicit approval.

## 4. Candidate Suggestion Model

```yaml
candidate_suggestion:
  candidate_id: <stable-host-id>
  title: <short improvement title>
  evidence:
    map_ref: <ERGONOMICS-OPPORTUNITIES anchor or null>
    friction_signals:
      - source: observability | signal-observer | inventory | user-report
        ref: <telemetry-handle-or-path>
        count: <observed-occurrences>
  problem: <what is hard today>
  proposed_acceptance_idea: <one-line of what "done" would look like>
  target_owner: spellcraft | sigil-development | definitions-governance | host-surface
  autonomy_layer: L0 | L1 | L2
```

Rules:

- A suggestion must cite at least one real `map_ref` or one real `friction_signal`.
  A suggestion with neither is invalid and must not be offered.
- `autonomy_layer` defaults to the lowest rung the candidate supports; raising it
  requires evidence from the rung below (see README autonomy ladder).

## 5. Scoped Start Model

```yaml
scoped_start:
  candidate_id: <candidate-id>
  consent: granted | declined
  scope:
    candidate_space: <worktree-or-development-sandbox-path>
    write_allowlist:
      - <path-prefix-inside-candidate-space>
  granted_by: user
  granted_at: <timestamp>
```

Rules:

- The loop never self-grants consent. No `scoped_start.consent: granted` means no
  assembly.
- `write_allowlist` paths are all inside `candidate_space`; no canonical or runtime
  path may appear.

## 6. Isolated Assembly Model

```yaml
isolated_assembly:
  candidate_id: <candidate-id>
  candidate_space: <path>
  invoke_artifacts:
    - kind: define | design | plan
      path: <candidate-space-relative-path>
  owner_lifecycle_drafts:
    - owner: spellcraft | sigil-development
      kind: spell-draft | sigil-draft
      path: <candidate-space-relative-path>
      promoted: false
  touched_canonical_paths: []   # must remain empty
```

Rules:

- `owner_lifecycle_drafts[].promoted` is always `false` at this stage.
- `touched_canonical_paths` must be empty; any entry is a boundary violation and
  blocks the loop.

## 7. Pre-Registered Criterion Model

```yaml
preregistered_criterion:
  candidate_id: <candidate-id>
  frozen_at: <timestamp>     # must precede any self_test_result.run_at
  success_condition: <falsifiable statement of what passing means>
  failure_condition: <what would falsify it>
  measurement: <command | fixture | ui-check | review-prompt>
  user_runnable_test:
    instruction: <bounded test the user will run to judge it>
    expected_signal: pass | flag | block | measurement
```

Rules:

- The criterion is frozen before the run. `frozen_at` precedes `run_at`.
- The success condition cannot be edited after a result exists; a changed condition
  is a new criterion with a new freeze, not an amendment.

## 8. Self-Test Result Model

```yaml
self_test_result:
  candidate_id: <candidate-id>
  criterion_ref: <preregistered-criterion-id>
  run_at: <timestamp>
  verdict: SURVIVED | FALSIFIED | INVALID
  evidence_ref: <path-or-output-summary>
  residue:
    - <gap-or-follow-up>
```

Rules:

- A `FALSIFIED` or `INVALID` verdict ends the autonomous loop with a residue entry;
  it does not silently retry until `SURVIVED`.
- Only `SURVIVED` proceeds to notify the user — and even then, only as a candidate
  for the user's own test, never as a promotion.

## 9. Notification + Approval Model

```yaml
approval_promotion:
  candidate_id: <candidate-id>
  notification:
    channel: push
    message: "ready for your test + approval"   # never "done" / "shipped"
    verdict: SURVIVED
    user_runnable_test: <from preregistered_criterion>
  user_test_result: not-run | pass | flag | block
  decision: approved | rejected | deferred
  decided_by: user
  promotion:
    routed_to: spellcraft | sigil-development | definitions-governance | null
    receipt_ref: <artifact-or-verdict-handle-or-null>
```

Rules:

- `promotion.routed_to` is non-null only when `decision: approved` **and**
  `user_test_result: pass`.
- Promotion executes through the owning capability and returns a `receipt_ref`. The
  loop itself never writes the promoted artifact.
- `rejected` and `deferred` leave the candidate in its space with residue; nothing
  is promoted.

## 10. Owner-Safe Actions

| Action | Allowed effect | Boundary |
| --- | --- | --- |
| `suggest_candidate` | Propose one evidenced improvement. | Must cite a real map entry or friction signal. |
| `request_scoped_start` | Ask the user for bounded build consent. | No assembly without granted consent. |
| `assemble_in_candidate_space` | Author invoke + owner-lifecycle drafts in isolation. | No writes outside `candidate_space`; `touched_canonical_paths` stays empty. |
| `preregister_criterion` | Freeze the acceptance criterion. | Frozen before run; immutable after a result exists. |
| `run_self_test` | Run the test against the frozen criterion. | Cannot edit the success condition; no retry-until-green. |
| `notify_user` | Send the result + a user-runnable test. | Message is "ready for test + approval," never "shipped." |
| `route_promotion` | On approval, hand promotion to the owner. | Only with `approved` + passing user test; owner writes the artifact. |

Disallowed effects:

- offering a suggestion with no evidence;
- assembling without scoped consent;
- writing to `arcanum/` canonical capabilities, definitions, or runtime;
- editing the success criterion after seeing the result;
- retrying silently until a test passes;
- promoting, installing, or claiming "shipped" before the user test + approval;
- writing the promoted artifact from loop state instead of the owning capability.

## 11. Pass Conditions

A static proof over a fixture candidate passes when a reader can answer:

- what evidence (map entry or friction signal) justified the suggestion;
- what scope the user consented to, and what the write allowlist was;
- which invoke and owner-lifecycle drafts were produced, all inside the candidate
  space, with no canonical paths touched;
- what success condition was frozen, and that it was frozen before the run;
- what the self-test verdict was and what residue it left;
- what test the user was asked to run, and what they decided;
- which owner executed the promotion and what receipt proved it — or why nothing
  was promoted.

The proof fails if:

- a suggestion has no evidence;
- assembly touched a canonical or runtime path;
- the success criterion changed after a result existed;
- a FALSIFIED result was silently retried;
- anything was promoted without the user test + approval;
- the loop wrote a promoted artifact directly instead of routing to the owner.
