# Modal Tonal Nodal Graph Build Specification for ResonantOS

Version: **v2 — Post-Hoc Issue Packager scope**
Status: **Proposal for ResonantOS design review**
Primary V1 shape: **on-demand / sidecar / schema-first artifact pipeline**

---

# 1. Executive Summary

The Modal Tonal Nodal Graph (**MTNG**) is proposed as an on-demand engine for turning selected messy work evidence into useful, reviewable artifacts.

For V1, MTNG should **not** be a live runtime orchestrator. It should not dynamically branch active user intent during normal ResonantOS operation, promote memory automatically, modify agents directly, or assign contribution value.

The safest and most useful V1 is the **MTNG Post-Hoc Issue Packager**:

```text
mtng run --profile resonantos_debug_session \
  --terminal ./session.log \
  --chat ./chatgpt-transcript.md \
  --git-diff ./changes.diff \
  --out ./mtng-output/
```

Expected V1 outputs:

```text
./mtng-output/
  signal-manifest.yaml
  branch-nodes.yaml
  developer-issue-packet.md
  memory-candidates.md
  contribution-records.yaml
  validator-report.md
  audit-log.jsonl
  okf/
```

The core workflow is:

```text
selected inputs
→ signal records
→ mode proposals
→ branch nodes only when boundaries change
→ node validators
→ issue packet / memory candidates / contribution records / OKF export
```

The core boundary rule is:

> Branch only when validation, output artifact, context needs, tool requirements, memory treatment, contribution record type, safety boundary, or authority boundary changes.

MTNG should prove value as a local, selected-input, audit-first tool before any deeper integration into ResonantOS runtime systems.

---

# 2. Provenance and Review Status

This proposal is derived from ResonantOS debugging, provider-routing, UI-affordance, local-agent workflow, developer-handoff, memory, OKF/export, and contribution-accounting discussions.

It has been updated after three review passes:

1. **Analog 6 Technical Review** — validated the architecture but requested integration mapping, fast-path handling, mode-detection recovery, graph recombination clarity, overhead budgeting, and V1 scope clarification.
2. **Raptor mini Audit Review** — strongly recommended MTNG only as an offline/sidecar/on-demand, audit-first, memory-safe, authority-bounded pipeline for V1.
3. **Gemini Outside Review** — recommended a strict V1 boundary: post-hoc context distiller / issue packager, not online runtime control.

This document intentionally narrows V1 after those reviews.

---

# 3. V1 Positioning

## V1 Is

```text
- on-demand
- selected-input
- sidecar-compatible
- CLI-first or schema-first
- audit-first
- review-oriented
- memory-safe
- OKF-exportable
- contribution-capture capable
- provider-policy respecting
```

## V1 Is Not

```text
- always-on monitoring
- active runtime orchestration
- live user-intent branching
- automatic agent mutation
- direct memory promotion
- contribution valuation
- provider-routing replacement
- Guardian Core replacement
- hidden background analysis of all data
```

## Recommended V1 Name

**MTNG Post-Hoc Issue Packager**

This name is intentionally plain. It explains the first useful behavior without overselling the broader architecture.

---

# 4. Problem Statement

Agent workflows often fail because one context is asked to hold too many unresolved jobs at once.

Example mixed report:

```text
Engineer chat does not respond.
Settings controls appear unwired.
The Home screen hides or obscures tools.
I clicked around and am not sure which action caused the failure.
```

A flat summary risks losing the structure:

```text
- reproduction uncertainty
- provider routing failure
- settings persistence uncertainty
- UX affordance confusion
- onboarding/documentation gap
- contribution/triage record
```

Common failure modes:

1. Original reproduction path is lost.
2. Confirmed observations are mixed with speculation.
3. UX confusion is mislabeled as backend failure.
4. Provider failure swallows the user’s actual task.
5. Memory becomes a junk drawer.
6. The agent retries or reinterprets instead of producing a validated artifact.
7. Non-code labor such as triage, clarification, review, and synthesis disappears from contribution records.

MTNG addresses this by creating bounded artifacts only when a real boundary changes.

---

# 5. Core Concept

MTNG is a workflow-shaping model:

```text
Signal → Mode → Node → Validator → Synthesis
```

## Signal

A selected raw input or event.

Examples:

```text
terminal transcript
ChatGPT transcript
meeting transcript
agent log
build output
git diff
bug report
PR thread
community discussion
provider/tool failure
```

## Mode

A proposed kind of work.

Examples:

```text
bug_intake.reproduction
bug_intake.environment
provider.routing
settings.persistence
ux.affordance
docs.onboarding
memory.workflow_lesson
contribution.artifact_record
synthesis.developer_issue
```

## Routing Signature

A detectable clue that suggests a mode may be active.

Earlier drafts used the term “Tone.” For V1 implementation and maintainer review, use **Routing Signature** instead. This avoids making the implementation sound dependent on metaphor.

Examples:

```text
"I clicked around"
  possible signature for reproduction uncertainty or UX affordance review

"does not respond"
  possible signature for runtime/provider failure

"expected X but saw Y"
  possible signature for bug-intake mode

"this keeps happening"
  possible signature for workflow lesson or memory candidate
```

Routing signatures are **hints**, not proof.

## Node

A bounded processing unit with a contract.

A node declares:

```text
accepts
rejects
allowed context
blocked context
output artifact
validator
status
merge target
contribution hooks
```

## Validator

A structural check that determines whether the node produced the right kind of artifact.

Validators are not just quality checks. They are also misrouting detectors.

## Synthesis

The process of combining validated or explicitly partial/failed nodes into a final artifact, such as a developer issue packet.

---

# 6. On-Demand Deployment Model

MTNG should analyze selected work surfaces for selected purposes.

It should not run on all user data.

It should not need to stay active for an entire work session.

A user or maintainer should choose:

```text
- input files or transcripts
- scraping configuration
- enabled modes
- output artifacts
- persistence policy
- whether memory candidates are generated
- whether contribution records are generated
- whether OKF export is generated
```

## Operating Modes

### Batch Analysis Mode

Completed material is fed to MTNG.

Inputs:

```text
terminal session
ChatGPT export
meeting transcript
Discord/forum scrape
GitHub issue/PR discussion
agent logs
build/test output
```

Outputs:

```text
bug report
developer handoff packet
agent improvement packet
memory candidates
community suggestions
contribution records
regression checklist
OKF bundle
```

### Session Wrap-Up Mode

The user runs MTNG after work.

Example:

```text
Run MTNG on this terminal log, ChatGPT transcript, and git diff.
Generate a developer issue packet, memory candidates, and contribution records.
```

### Post-Hoc Audit Mode

MTNG analyzes prior work to recover artifacts, lessons, or contribution records.

Example:

```text
Feed MTNG the merged PR, review thread, test logs, and related discussion.
Produce contribution records and identify missing regression coverage.
```

### Targeted Live Mode

Targeted live mode is **deferred**. It may be considered later only after the post-hoc pipeline proves value and integration boundaries are clear.

---

# 7. Run Profiles and Scraping Configurations

Each run should have an explicit profile.

```yaml
mtng_run_profile:
  id: "mtng_run_..."
  run_type: "batch_analysis | session_wrap_up | post_hoc_audit | export"
  operator: "user_or_maintainer_ref"
  purpose:
    - "bug_report"
    - "memory_candidates"
    - "contribution_records"
  input_sources:
    - type: "terminal_transcript"
      path_or_ref: "./session.log"
    - type: "chat_transcript"
      path_or_ref: "./chat.md"
    - type: "git_diff"
      path_or_ref: "./changes.diff"
  scraping_config: "resonantos_debug_session"
  enabled_modes:
    - "bug_intake.reproduction"
    - "bug_intake.environment"
    - "provider.routing"
    - "settings.persistence"
    - "ux.affordance"
    - "contribution.artifact_record"
  output_targets:
    - "developer_issue_packet"
    - "memory_candidate_packet"
    - "contribution_record_packet"
    - "okf_bundle"
  memory_promotion:
    default: "review_only"
  contribution_accounting:
    capture: true
    valuation: false
  persistence:
    save_raw_inputs: false
    save_derived_artifacts: true
    save_audit_log: true
```

Example scraping configs:

```yaml
scraping_configs:
  resonantos_debug_session:
    preferred_inputs:
      - terminal transcript
      - agent chat transcript
      - test output
      - git diff
    modes:
      - bug_intake.reproduction
      - bug_intake.environment
      - provider.routing
      - settings.persistence
      - ux.affordance
      - synthesis.developer_issue

  community_feedback_session:
    preferred_inputs:
      - Discord thread
      - forum export
      - meeting notes
    modes:
      - user_intent.clarification
      - ux.affordance
      - docs.onboarding
      - memory.workflow_lesson
      - synthesis.community_suggestions

  contribution_review_session:
    preferred_inputs:
      - PR thread
      - commit log
      - review comments
      - test results
      - meeting transcript
    modes:
      - contribution.artifact_record
      - review.regression_prevention
      - synthesis.contribution_summary
```

---

# 8. Data Minimization and Persistence

MTNG should process only selected inputs required for the selected run profile.

It should not assume access to:

```text
the whole file system
all project history
all conversations
all user memory
all team activity
all active application state
```

Recommended defaults:

```yaml
persistence_defaults:
  raw_inputs:
    save_by_default: false
    reason: "Raw transcripts may contain unrelated or sensitive material."

  derived_artifacts:
    save_by_default: true
    examples:
      - developer issue packet
      - memory candidate packet
      - contribution records
      - validator report
      - OKF bundle

  audit_log:
    save_by_default: true
    reason: "Explains what MTNG did without requiring raw transcript retention."

  durable_memory:
    save_by_default: false
    reason: "Memory promotion requires review."

  contribution_records:
    save_by_default: "operator_configurable"
    reason: "Contribution capture should be explicit."
```

---

# 9. Engine Plus Specialty Tools

MTNG should be built as an engine with attachable specialty tools.

## Engine Owns

```text
run profiles
input manifests
signal lifecycle
mode registry
branch rules
loop limits
node lifecycle
contract schemas
validator gates
merge readiness
memory candidate status
contribution record status
audit log
budget limits
export manifest
```

## Specialty Tools Provide

```text
transcript scrapers
terminal session parsers
meeting summarizers
mode detectors
provider diagnostics
bug report extractors
UX issue extractors
settings wiring checkers
docs/onboarding analyzers
artifact validators
synthesis generators
memory candidate writers
contribution record generators
OKF/Markdown/JSON exporters
```

## Mutation Boundary

Specialty tools should not mutate graph state directly.

They submit proposals:

```yaml
tool_result:
  proposes:
    - create_branch
    - mark_node_passed
    - mark_node_failed
    - add_memory_candidate
    - add_contribution_record
    - request_human_review
```

The engine accepts, rejects, validates, or queues proposals according to policy.

---

# 10. Phase 0: ResonantOS Integration Mapping

Before implementation, map MTNG against existing ResonantOS architecture.

The V1 assumption should be:

> MTNG augments existing ResonantOS systems. It does not replace them.

Systems to map:

```text
Guardian Core
Blackboard/shared state
Bridge Server
Event bus
Provider routing / provider fabric
Memory/archive / Living Archive
Add-on capability model
```

Questions to answer:

```text
Signal:
  Where do selected events or artifacts enter ResonantOS?

Mode:
  Is there an existing task/event/route classification concept?

Node:
  Is there an existing bounded delegated-work unit?

Branch:
  Can one input become multiple related artifacts?

Synthesis:
  Where are outputs merged into reports, answers, issues, or memory candidates?

Memory:
  Where do review-only memory candidates belong?

Contribution:
  Is there an audit or artifact history mechanism?

Inspection:
  Where should validator status, audit logs, and outputs be viewed?
```

## V1 State Ownership Recommendation

For V1, MTNG should own its run-local state inside its output directory.

ResonantOS does not need to own MTNG runtime state in V1.

```text
MTNG V1 owns:
  ./mtng-output/signal-manifest.yaml
  ./mtng-output/branch-nodes.yaml
  ./mtng-output/validator-report.md
  ./mtng-output/audit-log.jsonl
  ./mtng-output/okf/

ResonantOS may later ingest:
  developer issue packet
  review-only memory candidates
  contribution records
  OKF bundle
  audit summary
```

Any ingestion of agent-improvement packets, rule updates, tool changes, or memory candidates should require an explicit Guardian/maintainer approval path.

---

# 11. Provider Fabric and Capability Grants

MTNG should not introduce a new model/provider routing layer in V1.

It should either:

1. Run as a standalone local CLI with explicit model configuration, or
2. Use existing ResonantOS provider policy when running inside ResonantOS.

If MTNG specialty tools are packaged as ResonantOS add-ons, they must declare and request capabilities through the existing add-on/tool permission model.

Examples:

```text
read_terminal_transcript
read_chat_transcript
read_git_diff
read_workspace_file
write_output_directory
propose_memory_candidate
emit_audit_event
export_okf_bundle
```

MTNG tools should not bypass capability gates to read files, memory, provider state, or workspace data.

---

# 12. Branching Rules for V1

The earlier numeric Branch Pressure Score is deferred.

Numeric scoring may be useful after empirical runs, but V1 should use a simpler binary trigger model.

## V1 Branch Triggers

Create a branch when one of these is true:

```text
output artifact type changes
validation contract changes
required tool changes
context boundary changes
memory treatment changes
contribution record type changes
safety or authority boundary appears
explicit human/operator split requested
```

## V1 Default

If the signal can produce one clear artifact with one validator, do not branch.

## Deferred Policy

The following are future tuning layers, not V1 requirements:

```text
weighted branch pressure scoring
numeric escalation thresholds
learned branch policies
automatic graph optimization
runtime branch-based orchestration
```

---

# 13. Fast Path for Simple Signals

A signal should take the fast path when:

```text
1. one dominant mode is proposed
2. no V1 branch trigger fires
3. one output artifact is obvious
4. one validation contract is enough
5. no safety, memory, contribution, tool, or authority boundary changes
```

Fast-path flow:

```text
selected signal
→ one proposed mode
→ one node
→ validator
→ artifact or explicit missing-info marker
→ optional review-only memory/contribution candidate
```

Example:

```text
The settings page crashes when I click Save on Windows.
```

Output:

```yaml
node:
  mode: bug_intake.reproduction
  artifact: reproduction_section
  branch_count: 1
  status: closed
  closed_result: partial_or_passed
```

---

# 14. V1 Node Lifecycle

The earlier five-stage detection lifecycle is deferred.

V1 should use a simpler state machine:

```text
proposed → processing → closed
```

The `closed` state carries a result:

```yaml
closed_result:
  - passed
  - partial
  - failed
  - rejected
  - superseded
  - needs_human
```

This keeps the pilot schema small while preserving auditability.

## Node Contract Example

```yaml
node:
  id: "node_reproduction_001"
  signal_id: "sig_001"
  mode: "bug_intake.reproduction"
  state: "proposed | processing | closed"
  closed_result: "passed | partial | failed | rejected | superseded | needs_human"
  branch_reason:
    - "validation contract differs from provider diagnosis"
  accepts:
    - "user actions"
    - "visible results"
    - "environment facts"
  rejects:
    - "root cause speculation"
    - "fix proposals"
  allowed_context:
    - "selected raw report"
    - "selected environment metadata"
  blocked_context:
    - "unverified diagnosis"
    - "unrelated project history"
  output_artifact:
    type: "dev_report.reproduction_section"
    path: "artifacts/reproduction-section.md"
  validator:
    - "has steps or explicit missing-step marker"
    - "has expected result or unknown marker"
    - "has actual result"
    - "separates facts from speculation"
  contribution_hooks:
    - "reproduction"
    - "triage"
    - "clarification"
```

---

# 15. Validators as Safety Nets

Validators should reveal both poor output and wrong routing.

Example: a `provider.routing` branch is created, but the input has no endpoint evidence, no provider setting, no log, and no model response failure.

Validator result:

```yaml
validator_result:
  node_id: "node_provider_001"
  status: "failed"
  reason: "insufficient provider-routing evidence"
  possible_reroute:
    - "ux.affordance"
```

## Misrouting Recovery Limits

To avoid rerouting loops, V1 should use hard limits:

```yaml
v1_loop_limits:
  max_reroutes_per_signal: 1
  max_validator_failures_per_node: 1
  max_new_branches_after_validation_failure: 1
  on_second_failure: "write_uncertainty_to_audit_and_stop"
```

If a branch fails after one reroute attempt, MTNG should stop trying to resolve it automatically and record uncertainty.

---

# 16. Anti-Bifurcation Loop Breaker

MTNG should detect when an analysis workflow starts looping.

Loop signals:

```text
repeated tool call without new evidence
interpretation shift without artifact
scope expansion after failure
summary produced without validator pass
claiming completion while validators fail
re-opening closed branch without new evidence
```

V1 action:

```text
freeze current signal state
stop retries for that node
write loop warning to audit log
close unresolved node as needs_human or failed
continue only with already valid artifacts
```

V1 should not attempt complex automatic recovery after repeated failure.

---

# 17. Recombination and Synthesis for V1

Graph recombination should be narrow in V1.

A synthesis artifact may include:

```text
passed nodes
partial nodes with explicit missing information
failed/rejected/blocked nodes only as status notes
```

It must not hide conflict or uncertainty.

## Merge Rule

```yaml
synthesis_target:
  type: "developer_issue_packet"
  required_nodes:
    bug_intake.reproduction:
      allowed_results: ["passed", "partial"]
    bug_intake.environment:
      allowed_results: ["passed", "partial"]
  optional_nodes:
    provider.routing:
      allowed_results: ["passed", "partial", "failed", "rejected", "needs_human"]
    ux.affordance:
      allowed_results: ["passed", "partial", "failed", "rejected", "needs_human"]
  rule: "Include unresolved optional nodes as clearly labeled status sections."
```

## Conflict Rule

If two nodes conflict, do not choose a winner without evidence.

```yaml
conflict:
  status: "unresolved"
  action:
    - "record conflict in validator-report.md"
    - "include conflict note in developer-issue-packet.md"
    - "do not generate implementation request from conflict"
```

Implementation requests are out of V1 scope unless all required nodes pass and maintainers approve the handoff.

---

# 18. Memory Candidate Pipeline

Memory output is review-only in V1.

MTNG may produce memory candidates, but it must not promote durable memory automatically.

Example:

```yaml
memory_candidate:
  id: "mem_001"
  type: "workflow_lesson"
  content: "Clicked-around UI reports should be split into reproduction, UX, provider, settings, and docs branches before implementation."
  evidence_refs:
    - "sig_001"
    - "node_reproduction_001"
  confidence: "medium"
  ttl: "review_required"
  promotion_status: "needs_review"
```

---

# 19. Contribution Capture Pipeline

MTNG may capture contribution structure, not value.

V1 contribution record:

```yaml
contribution_record:
  id: "contrib_001"
  signal_id: "sig_001"
  branch_node_id: "node_reproduction_001"
  contributor_ref: "user_or_agent_or_team_member"
  contribution_type:
    - "triage"
    - "reproduction"
  artifact_ref: "artifacts/reproduction-section.md"
  validator_status: "partial"
  status: "recorded"
  notes: "Converted ambiguous clicked-around report into a testable reproduction section."
```

V1 must not decide:

```text
compensation
ownership
voting power
tokenization
governance weight
economic conversion
leaderboard ranking
```

Future governance may offset, factor, unitize, weight, or otherwise value contribution records, but that is outside MTNG V1.

---

# 20. OKF Alignment and Edge-Case Handling

MTNG should use Google’s Open Knowledge Format (**OKF**) for as much categorization, export, and knowledge interchange as practical.

## Principle

```text
OKF describes knowledge artifacts.
MTNG controls workflow state.
```

MTNG should be **OKF-first**, not OKF-only.

## Prefer OKF For

```text
developer issue packets
memory candidates
workflow lessons
project facts
design decisions
runbooks
tool descriptions
agent improvement proposals
community suggestions
contribution summaries
post-hoc audit reports
exported branch artifacts
synthesis artifacts
```

## Keep MTNG-Native For

```text
branch lifecycle state
validator execution state
reroute limits
loop warnings
merge readiness
graph mutation proposals
raw audit events
temporary runtime state
safety/authority boundary state
```

## OKF Insufficiency Cases

OKF may be insufficient for:

```text
typed graph edges
validator pass/fail gates
unresolved merge conflicts
safety boundaries
retry-loop state
memory TTL/confidence/promotion status
contribution supersession history
tool mutation proposals
```

## Edge-Case Rule

When OKF is insufficient:

```text
1. preserve the closest OKF-readable artifact
2. add MTNG extension metadata
3. flag the edge case explicitly
4. link to canonical MTNG-native YAML/JSON if needed
5. do not flatten operational meaning into misleading prose
```

Example OKF-compatible frontmatter with MTNG extensions:

```yaml
---
type: "Developer Issue"
title: "Desktop provider routing and hidden affordance failure"
description: "Issue packet generated from selected debug-session inputs."
tags:
  - resonantos
  - mtng
  - provider-routing
  - ux-affordance

mtng_schema_version: "0.2"
mtng_record_type: "synthesis_artifact"
signal_refs:
  - "sig_001"
included_node_refs:
  - "node_reproduction_001"
  - "node_provider_001"
  - "node_ux_001"
validator_status: "partial"
merge_status: "ready_for_triage_not_implementation"
memory_promotion_status: "review_only"
edge_case_flags:
  - "partial_merge"
  - "unresolved_provider_root_cause"
---
```

Suggested edge-case flags:

```yaml
edge_case_flags:
  - okf_extension_required
  - typed_edges_required
  - partial_merge
  - unresolved_conflict
  - runtime_state_only
  - not_for_durable_memory
  - validator_failed
  - validator_partial
  - needs_human_review
  - superseded_artifact
  - contribution_status_required
  - safety_boundary_present
```

---

# 21. V1 Pilot: Post-Hoc Issue Packager

## Pilot Goal

Prove MTNG can convert selected messy work evidence into a clearer developer issue packet without touching live runtime authority.

## Inputs

```text
terminal logs
chat transcripts
git diffs
bug reports
agent logs
selected notes
```

## Outputs

```text
signal-manifest.yaml
branch-nodes.yaml
developer-issue-packet.md
memory-candidates.md
contribution-records.yaml
validator-report.md
audit-log.jsonl
okf/
```

## Pilot Scope Includes

```text
Phase 0 integration mapping
run-local state
fixed mode registry
binary branch triggers
fast path / no branch option
simple validators
manual or semi-automatic synthesis
review-only memory candidates
contribution capture metadata
OKF export with MTNG fallback
```

## Pilot Scope Excludes

```text
automatic live agent delegation
direct memory promotion
wallet/browser control actions
full contribution valuation
runtime reconstruction
automatic rule mutation
provider-routing replacement
Guardian Core replacement
```

## Pilot Success Criteria

The pilot succeeds if:

1. A mixed report becomes clearer after processing.
2. The issue packet is more actionable than a flat summary.
3. Validators catch missing information.
4. Provider failure does not swallow UX or onboarding concerns.
5. UX confusion does not get mislabeled as backend failure.
6. Contribution records capture triage/reproduction/review/synthesis work.
7. Outputs are inspectable and auditable.
8. Added overhead is acceptable.
9. Raw inputs are not retained unless explicitly configured.
10. OKF export is useful without hiding MTNG-native edge cases.

---

# 22. Minimal V1 Data Structures

```yaml
Signal:
  id: string
  source_type: string
  source_ref: string
  timestamp: string
  raw_content_ref: string
  run_profile_id: string

RunProfile:
  id: string
  run_type: string
  operator: string
  purpose: list
  input_sources: list
  scraping_config: string
  enabled_modes: list
  output_targets: list
  persistence: object

ModeProposal:
  signal_id: string
  mode: string
  confidence: number
  routing_signatures: list
  rationale: string
  state: "proposed | processing | closed"
  closed_result: string

BranchNode:
  id: string
  signal_id: string
  mode: string
  branch_reason: list
  accepts: list
  rejects: list
  allowed_context: list
  blocked_context: list
  output_artifact_type: string
  validator: list
  assigned_tool: string
  state: string
  closed_result: string
  output_ref: string
  contribution_hooks: list

SynthesisArtifact:
  id: string
  signal_id: string
  included_node_ids: list
  excluded_node_ids: list
  artifact_type: string
  content_ref: string
  validation_status: string

MemoryCandidate:
  id: string
  source_signal_id: string
  source_node_ids: list
  memory_type: string
  content: string
  confidence: string
  ttl: string
  promotion_status: string

ContributionRecord:
  id: string
  signal_id: string
  branch_node_id: string
  contributor_ref: string
  contribution_type: list
  artifact_ref: string
  validator_status: string
  status: string

AuditEvent:
  id: string
  timestamp: string
  run_profile_id: string
  event_type: string
  actor_ref: string
  subject_ref: string
  details: object
```

---

# 23. Initial Mode Registry for Pilot

Keep the pilot list small.

```yaml
modes:
  - id: bug_intake.reproduction
    artifact: reproduction_section
    validator: reproduction_validator

  - id: bug_intake.environment
    artifact: environment_summary
    validator: environment_validator

  - id: provider.routing
    artifact: provider_diagnostic_packet
    validator: provider_routing_validator

  - id: settings.persistence
    artifact: settings_wiring_checklist
    validator: settings_persistence_validator

  - id: ux.affordance
    artifact: ux_issue_packet
    validator: ux_affordance_validator

  - id: docs.onboarding
    artifact: onboarding_gap_note
    validator: docs_onboarding_validator

  - id: contribution.artifact_record
    artifact: contribution_record
    validator: contribution_record_validator

  - id: synthesis.developer_issue
    artifact: developer_issue_packet
    validator: developer_issue_validator
```

Additional modes should be proposed through review, not added casually.

---

# 24. Build Order

## Stage 0: Integration Mapping

Map MTNG concepts to ResonantOS components and decide whether the first implementation is CLI-only, sidecar service, schema-only pipeline, or inspection panel.

## Stage 1: Schema and Contracts

Define:

```text
run profile schema
scraping config schema
signal manifest schema
branch node schema
validator report schema
memory candidate schema
contribution record schema
OKF export conventions
```

## Stage 2: On-Demand Runner

Implement:

```text
mtng run
selected input ingestion
output directory creation
audit-log.jsonl
manifest writing
raw input retention policy
```

## Stage 3: Fast Path and Binary Branching

Implement:

```text
single-artifact fast path
binary branch triggers
manual split override
branch cap
reroute cap
```

## Stage 4: Validators and Artifacts

Implement initial validators and artifacts for:

```text
reproduction section
environment summary
provider diagnostic packet
UX issue packet
developer issue packet
```

## Stage 5: OKF Export

Export human-readable artifacts as OKF-compatible Markdown plus MTNG extension metadata where needed.

## Stage 6: Memory and Contribution Candidates

Generate review-only memory candidates and contribution records.

## Stage 7: Optional Inspection UI

Add a developer inspection panel only if the CLI artifact pipeline proves useful.

---

# 25. Evaluation Tests

## Test 1: Fast Path

Input is a clean single-mode bug report.

Expected:

```text
one node
one artifact
no unnecessary branches
validator report
```

## Test 2: Mixed UI/Provider Report

Input contains reproduction uncertainty, provider failure, settings confusion, and UX affordance issue.

Expected:

```text
multiple branches only where artifact/validator boundaries change
separate provider and UX outputs
unknowns marked explicitly
no root cause asserted without evidence
```

## Test 3: Misrouting

A provider branch lacks provider evidence.

Expected:

```text
validator fails
possible reroute recorded
max one reroute
second failure writes uncertainty and stops
```

## Test 4: Contribution Capture

A report is clarified by one person, fixed by another, and reviewed by a third.

Expected:

```text
artifact-linked contribution records
no valuation
validator status preserved
```

## Test 5: OKF Edge Case

A synthesis artifact has partial merge and unresolved conflict.

Expected:

```text
OKF-readable Markdown produced
MTNG extension metadata includes edge_case_flags
canonical YAML/JSON state preserves typed semantics
```

## Test 6: Privacy / Data Minimization

Run profile selects terminal log and git diff only.

Expected:

```text
no unrelated files inspected
raw input retention follows config
audit log records selected sources
```

---

# 26. Risks and Mitigations

## Over-Branching

Mitigation:

```text
binary branch triggers
fast path default
branch cap
manual review for ambiguous splits
```

## Under-Branching

Mitigation:

```text
validators expose missing structure
operator can split manually
review feedback can propose new contracts
```

## Misrouting Loops

Mitigation:

```text
max one reroute
max one validator failure per node
second failure stops and writes uncertainty
```

## Scope Creep

Mitigation:

```text
Post-Hoc Issue Packager V1
runtime integration deferred
contribution valuation deferred
memory promotion deferred
small mode registry
```

## Privacy / Overreach

Mitigation:

```text
selected inputs only
raw retention off by default
scraping config visible
audit log visible
```

## Existing Architecture Collision

Mitigation:

```text
Phase 0 mapping first
run-local state in V1
reuse provider fabric
respect add-on capability gates
no Guardian replacement
```

## OKF Flattening

Mitigation:

```text
OKF-first, not OKF-only
MTNG extension metadata
edge-case flags
native YAML/JSON when needed
```

---

# 27. Questions for Tom / Maintainers

1. Is MTNG V1 acceptable as an internal developer tool rather than product-visible runtime behavior?
2. Should the first pilot be CLI-only, or should it have a minimal inspection panel?
3. Where should V1 artifacts and audit logs live?
4. Should MTNG output be shaped for Living Archive intake, GitHub issue generation, or both?
5. Can MTNG reuse current provider/model policy without adding routing logic?
6. What is the acceptable V1 failure mode: missed branches or extra conservative branches?
7. Which pilot dataset should prove usefulness first?
8. What is the no-go condition for continuing after the pilot?
9. What capabilities must MTNG specialty tools request if run inside ResonantOS?
10. Which OKF categories should be preferred for exported artifacts?

---

# 28. Non-Goals to Preserve

MTNG V1 should not:

```text
run continuously
inspect all user data
control live runtime behavior
replace Guardian Core
replace provider routing
promote memory automatically
value contributions economically
modify agents or tools without review
hide uncertainty in synthesis
force all artifacts into OKF when OKF is insufficient
```

---

# 29. Final Summary

MTNG v2 is a narrowed, review-driven proposal.

The first useful form is not a full runtime architecture.

The first useful form is:

> An on-demand Post-Hoc Issue Packager that processes selected logs, transcripts, diffs, and reports into developer issue packets, review-only memory candidates, contribution records, validator reports, and OKF-compatible exports.

Its core discipline is:

```text
Branch only when boundaries change.
Validate before synthesis.
Capture evidence before memory.
Record contribution structure before valuation.
Use OKF where it fits.
Preserve MTNG-native semantics where OKF is insufficient.
```

If the V1 pilot proves that this produces better developer handoffs than flat summaries, without unacceptable overhead or architecture disruption, MTNG can be considered for deeper ResonantOS integration later.
