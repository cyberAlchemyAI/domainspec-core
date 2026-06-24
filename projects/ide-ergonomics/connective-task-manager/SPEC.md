# SPEC - Connective Task Manager

Status: flagship strategy artifact; no runtime implementation
Date: 2026-06-23
Owner if pursued: IDE Ergonomics host-surface owner plus Craft/route owners
Builds on: [README.md](README.md)

## 1. Problem

Task managers usually rank work by status, deadline, or manual priority. Agentic
work needs more. A task can be high priority but too ambiguous for a tired session.
A blocker can be small but consequential. A next move can look ready until a quick
user-executed test fails. A comfortable task can steal attention from a domain
priority that blocks the whole project.

Connective solves the scheduling gap between:

- what Craft says is pending;
- what the domain says matters;
- what the user can actually attend to now;
- what evidence says is safe to execute.

## 2. Primitive

`connective-task-manager` is a flagship composition primitive with five linked
models:

1. `craft_work_import` - reads Craft scopes, pending nodes, next moves, blockers,
   decisions, gaps, receipts, and stale state.
2. `human_indicator_snapshot` - opt-in session signals supplied or approved by the
   user.
3. `user_executed_test_evidence` - bounded checks the user or local environment ran
   and can inspect.
4. `domain_priority_lens` - priority, risk, deadline, dependency, owner, and product
   path signals.
5. `execution_lane_recommendation` - ranked next actions with explanation,
   confirmation, owner route, and expected receipt.

## 3. Task Candidate Model

```yaml
task_candidate:
  candidate_id: <stable-host-id>
  craft_scope: <repo-relative-path>
  source_rows:
    - kind: context | blocker | decision | gap | artifact | next_move | recomposition
      id: <craft-row-id-or-null>
      selector: <ledger-path-or-human-view-anchor>
  title: <short task title>
  current_status: ready | blocked | ambiguous | stale | deferred | running | complete
  domain_priority: low | medium | high | critical
  domain_reason: <why this matters>
  cognitive_load:
    estimated: low | medium | high | unknown
    drivers:
      - ambiguity
      - context-reload
      - cross-domain-reasoning
      - emotional-friction
      - long-feedback-loop
  attention_fit:
    required_focus: low | medium | high
    minimum_time: <duration-or-unknown>
    interruption_tolerance: low | medium | high
  validation_need:
    required_tests:
      - <test-or-check-id>
    current_evidence: none | partial | pass | flag | block
  recommended_route: interrogation | decision-gate | refine | task-session | export | defer
  explanation: <why this candidate is ranked here>
```

## 4. Human Indicator Snapshot

```yaml
human_indicator_snapshot:
  snapshot_id: <stable-host-id>
  captured_at: <timestamp>
  source: user-entered | inferred-with-confirmation | default-unspecified
  available_time: <duration-or-unknown>
  focus_level: low | medium | high | unknown
  fatigue: low | medium | high | unknown
  confidence: low | medium | high | unknown
  frustration: low | medium | high | unknown
  interruption_risk: low | medium | high | unknown
  desired_mode: solo | pair-with-agent | review-only | planning-only | unknown
  notes: <optional user-visible note>
```

Rules:

- Unknown is acceptable and must not be invented.
- Inferred indicators must be shown to the user before use.
- Indicators should be session-local by default.
- The snapshot must never be framed as medical or psychological assessment.

## 5. User-Executed Test Evidence

```yaml
user_executed_test:
  test_id: <stable-id>
  task_candidate_id: <candidate-id>
  kind: command | ui-check | review-prompt | fixture-run | manual-confirmation
  instruction: <what the user or local environment runs>
  expected_signal: pass | flag | block | measurement
  result: not-run | pass | flag | block | inconclusive
  evidence_ref: <path-or-output-summary-or-null>
  freshness: fresh | stale | unknown
```

Examples:

- run a focused validation command;
- inspect a UI path in a browser;
- answer one decision-gate question;
- run a small proof fixture;
- confirm whether a task is too cognitively heavy for the current session.

User-executed tests are evidence, not coercion. A failed or inconclusive test should
change recommendation, not shame the user.

## 6. Domain Priority Lens

```yaml
domain_priority_lens:
  priority_source:
    - craft-next-move
    - blocker
    - owner-decision
    - product-path
    - deadline
    - validation-risk
    - downstream-dependency
  project_priority: low | medium | high | critical
  blocked_downstream_work:
    - <craft-row-or-artifact>
  risk_if_deferred: low | medium | high | critical
  owner_requirement: <person|route|none>
  reason: <short human-readable rationale>
```

## 7. Recommendation Model

```yaml
execution_lane_recommendation:
  recommendation_id: <stable-host-id>
  generated_at: <timestamp>
  craft_export_ref: <craft-state-export-id>
  human_snapshot_ref: <snapshot-id>
  candidates:
    - <task-candidate-id>
  ranked_lanes:
    - rank: 1
      candidate_id: <task-candidate-id>
      route: interrogation | decision-gate | refine | task-session | export | defer
      fit: strong | acceptable | weak | blocked
      reason: <why this lane is recommended>
      load_warning: <none-or-warning>
      domain_warning: <none-or-warning>
      required_confirmation: true
      expected_receipt: <artifact-or-verdict-kind>
  not_recommended:
    - candidate_id: <task-candidate-id>
      reason: <why not now>
```

Ranking rules:

- Blocked tasks cannot rank above executable tasks unless the recommended action is
  to clear the blocker.
- Critical domain work can outrank low-load comfort work, but the panel must expose
  load risk and offer a lower-load route such as Interrogation or Decision Gate.
- High cognitive-load tasks should require either strong domain reason, user
  confirmation, or a split into a lower-load first move.
- Stale Craft state or stale test evidence should recommend refresh before
  execution.

## 8. Interactive Choice Contract

```yaml
connective_choice:
  prompt: <single focused question>
  recommended_lane: <ranked-lane-id>
  options:
    - run_recommended
    - ask_interrogation_first
    - open_decision_gate
    - refine_before_execution
    - run_user_test
    - defer
    - explain_more
  selected_option: <option-or-null>
  consequence_preview: <what will happen next>
```

Question rules:

- Ask one question at a time.
- Always include `Explain / more context` for consequential route selection.
- Show why the recommended lane balances human indicators, task readiness, and
  domain priority.
- Do not auto-run the selected owner route until confirmation.

## 9. Owner-Safe Actions

| Action | Allowed effect | Boundary |
| --- | --- | --- |
| `refresh_craft_work` | Re-read Craft scopes and pending nodes. | No ledger mutation. |
| `capture_human_snapshot` | Ask or confirm opt-in session indicators. | Unknown is allowed; no surveillance. |
| `run_user_test` | Run or prompt a bounded test. | Result changes recommendation, not authority. |
| `recommend_lane` | Rank next execution lanes. | Recommendation is not execution. |
| `run_selected_route` | Dispatch to the selected owner capability. | Owner route owns artifacts and receipts. |
| `defer_task` | Keep task visible and record optional note. | Does not lower domain priority silently. |

Disallowed effects:

- inventing human indicators;
- storing sensitive human-state history without explicit retention policy;
- using attention signals to override a user's explicit choice;
- hiding domain priority because a task is uncomfortable;
- running high-impact tasks without owner-route receipts;
- writing directly to Craft ledgers from recommendation state;
- claiming cognitive or medical assessment.

## 10. Pass Conditions

A static proof over fixture work passes when a reader can answer:

- which Craft rows produced the task candidates;
- what human indicators were known, unknown, or user-confirmed;
- what user-executed tests were run and what they showed;
- which domain priority signals affected ranking;
- why the recommended lane fits the current attention budget;
- what alternative was deferred and why;
- what owner route would execute next;
- what receipt would prove progress.

The proof fails if:

- recommendations cannot be traced to Craft rows;
- human indicators are invented or hidden;
- low-load tasks always outrank domain-critical tasks;
- domain-critical tasks ignore cognitive-load warnings;
- stale tests are treated as fresh;
- recommendation state mutates Craft authority directly;
- the user cannot override or ask for more context.
