---
title: Golden Quill / Tilth Current-State Assessment
date: 2026-05-16
author: Codex
status: planning artifact; not a LOCK ceremony
scope: what we had, what changed in the last 48-72 hours, what exists now, and what the next audit must prove
---

# Current-State Assessment

## Executive Read

The project is materially stronger than the 2026-05-11 architecture proficiency assessment. That 47/80 score is now historical, not current. Since then, the repository gained CI signal, memory-query/consolidation work, Reflection Packet v1 architecture, card-class artifacts, Wave 1 and Wave 2 card LOCK ceremonies, provider-boundary design and implementation, a vocabulary scrub, apolitical-dialect hardening, deployment and Alpha-readiness documentation, and the first PA foundation corpus pass.

The honest current posture is not "Alpha" as a single label. The canonical framing is now two gates:

- **Gate 1: internal replay with Paul Norton.** Goal: clean-clone reproducibility, CI clarity, no embarrassing stale docs or fossil scripts, and a coherent audit map for Paul.
- **Gate 2: first paid client.** Goal: sovereignty claims are structurally true in runtime, not only in architecture text; signed assets, boundary enforcement, observability posture, bypass/resume flow, and card/runtime loaders are coherent.

The work of the last 48-72 hours moved Gate 1 close to reachable, especially through PR #3, but the current local workspace is not itself a clean baseline. It is a large dirty worktree containing many locally LOCKed or staged-forward artifacts that are not all in canonical Git history.

## What We Had

Before this push, Golden Quill / Tilth had:

- A real headless v0.1 deterministic core: router classification boundary, F-CLASS gates, Classification Review, Intake, Uploader, CIC/CLC orthogonality gates, and a stable 339-test smoke bar.
- A strong governance culture: SOUL/USER/AGENTS, router.yaml, lock_history, L-005 two-cycle cross-family review, and Save-On-Decide discipline.
- A documented architecture that was ahead of much of the field on signed assets, BYOK, local-first posture, Law 3 org isolation, and deterministic Logician gates.
- A weak memory layer relative to the rest of the system: the 2026-05-11 assessment named memory competence as the single load-bearing Beta-blocking dimension.
- No reliable GitHub CI signal at the start of the audit loop.
- A mismatch between architecture claims and runtime proof in several places: Reflection Packet activation, card loaded/signature claims, package metadata, and provider egress wrapping.
- A repo-truth problem: significant work lived in local untracked files or ignored validation trees, while lock_history and daily logs sometimes referred to those files as if they were canonical.

## What Changed

The recent work landed along five major tracks.

### 1. Audit and Reproducibility Track

- Tandem QA/QC pressure audit artifacts were written under `pipeline/validation/tandem_qa_qc_pressure_audit_2026-05-16/`.
- The initial audit verdict was `ALPHA_READY_FOR_INTERNAL_REPLAY_ONLY`; the later Claude Code/Codex delta tightened that to `NOT_ALPHA_READY` / `NOT_PAUL_READY_AS_A_CLEAN_TECHNICAL_BASELINE` until gate fixes landed.
- Operator decisions were consolidated in `pipeline/handoffs/tandem_qa_qc_remediation_decisions_2026-05-16.md`.
- PR #3, `ci: land PR2 keepers and CC003 quarantine`, is open and mergeable at GitHub PR #3.
- Verified GitHub state: PR #3 head `2d68a3f` has CI run `25963750751`, completed successfully across four jobs: quality gate on Python 3.11 and 3.12, plus wheel-install CLI smoke on Python 3.11 and 3.12.
- Current local branch state is not identical to PR #3 head. Local branch `codex-pr2-cc003-cleanup` is at `571ee94`, ahead 1 and behind 3 relative to its remote, while the rebased PR head lives in a separate clean temp worktree as `2d68a3f`.

### 2. Runtime Boundary and Egress Track

- CC-003 direct-Anthropic operator glue was quarantined in the PR #3 line.
- `R-NO-DIRECT-PROVIDER-HTTP` was added as an AST-lint guard.
- CC-007 was designed, Thesis-reviewed, LOCKed as §4 v2.x.5 + §0.5 v27, then partially implemented in runtime code.
- New runtime surfaces include `pipeline/orchestrator/provider_boundary.py`, `pipeline/orchestrator/deployment_posture.py`, `pipeline/vault/classification/signed_register_loader.py`, `pipeline/vault/policies/outbound_boundary.cedar`, and `pipeline/logician/cedar_engine.py`.
- Seat-local provider modules were refactored toward the shared `OutboundCallable` shape; the Red Team Groq dual-path was collapsed in the v2.x.6 fixture migration.
- Remaining cleanup: router legacy `_enforce_cloud_boundary_pre/post` is still load-bearing and explicitly deferred to an OD-5 follow-on. Cedarpy integration is v0.2 substrate-addition territory, not cheap cleanup.

### 3. Card System Track

- Wave 1 cards were LOCKed: Food Systems CIC and Operating Capacity CLC.
- Wave 2 drafted, Thesis-reviewed, and then LOCKed 12 additional cards at rows 250-262.
- The card vocabulary scrub retired the old term workspace-wide for forward surfaces, with historical audit trails preserved.
- v7.0.12 retired the four-axis political enum and replaced it with CLC-keyed register state, backed by F-DIALECT and R-NO-POLITICAL-AXIS-LITERAL hardening.
- There are now 14 card YAMLs under `pipeline/cards/`: 6 CIC and 8 CLC.
- Important caveat: card lifecycle fields say signed/loaded, but `pipeline/cards/loader.py`, `pipeline/cards/validators.py`, and multiple F-CARDS gates still carry v0.2 first-wave `NotImplementedError` bodies. That can be legitimate if the claim is "signed asset declared and schema-valid"; it is not legitimate if the claim is "runtime loader is live."

### 4. Memory, Reflection, and Brain/JIT Track

- Memory CLI work landed in the recent arc, but the earlier "auto" framing needs care: current evidence supports a CLI and at least one live consolidation, not a fully observed automatic session-start consolidation loop.
- Reflection Packet v1 was LOCKed, and v0.2 first-wave work exists in planning/handoff form, but runtime activation remains an audit-sensitive boundary.
- Brain/JIT alignment work is strategically useful, especially for Paul, but remains research and architecture fit analysis. No F-BRAIN / R-BRAIN enforcement wrapper exists in the runtime tree today.

### 5. Documentation and Handoff Track

- `docs/platform_engineer_onboarding.md` and `docs/platform_engineer_quick_reference.md` give Paul a real starting surface.
- `docs/alpha_readiness_checklist.md` and `docs/v0_1_beta_deployment_runbook.md` separate code-tree readiness from real customer deployment readiness.
- `docs/paul_norton_memory_alignment_brief_2026-05-15.md` maps Paul/Brain/JIT onto Tilth's memory weakness.
- FID Phase 1 scaffold and dispatch plans now exist under `pipeline/funder_intelligence/` and `pipeline/handoffs/fid_*`.
- A PA foundation corpus pass exists locally under `data/` plus `pipeline/funder_corpus/`, with docs at `docs/pa_foundation_dataset.md`.

## What We Have Now

### Solid

- A deterministic v0.1 smoke path with known prior result: 339/339 passing.
- GitHub CI signal exists on PR #3, verified success on 2026-05-16 for PR head `2d68a3f`.
- Current lock_history high-water mark is row 262, with 264 JSONL lines on disk.
- 125 `f_*.py` gate modules exist under `pipeline/logician/gates`.
- 14 card YAMLs exist locally: 6 CIC and 8 CLC.
- Router/provider-boundary hardening has real code and tests, not just architecture text.
- The deprecated political-axis vocabulary has been replaced architecturally by CLC-keyed register state.
- The project now has a better vocabulary for readiness: Gate 1 internal replay vs Gate 2 first paid client.

### Brittle

- The local workspace is heavily dirty. Many docs, blueprints, runtime modules, card artifacts, tests, funder-corpus files, and vault assets are modified or untracked.
- Local current branch is not the same as the clean PR #3 branch whose CI passed.
- `pipeline/cards/__pycache__` exists in the workspace and should be treated as generated noise.
- The old audit prompt references `pipeline/handoffs/tandem_qa_qc_remediation_2026-05-16.md`, but the present file on disk is `pipeline/handoffs/tandem_qa_qc_remediation_decisions_2026-05-16.md`.
- Some lock_history rows still use historical `card_cartridge` lock_class for continuity even though forward vocabulary is card-only. Auditors must distinguish historical query compatibility from active vocabulary drift.

### Still Open

- Merge or otherwise reconcile PR #3 into canonical main before treating CI as the baseline.
- Decide how local LOCKed artifacts and untracked card/funder/runtime files become canonical Git truth without sweeping unrelated dirty state.
- Reconcile card `runtime_load_status: loaded` language with the v0.2-dormant loader and F-CARDS body reality.
- Verify Reflection Packet state after PR #1/PR #3 and local dirty state converge.
- Finish or explicitly defer router OD-5 deduplication.
- Turn Brain/JIT from research into an enforceable wrapper only after F-BRAIN / R-BRAIN style gates are specified and locked.
- Produce a gate-family LIVE/DORMANT manifest so 125 gate modules do not require humans to infer maturity from docstrings.

## Maturity Table

| Surface | Current maturity | Evidence anchor | Audit question |
|---|---|---|---|
| v0.1 smoke path | REAL | 339-test smoke in recent logs | Does it still pass in the clean PR #3 branch and local dirty tree? |
| GitHub CI | PARTIAL to REAL | PR #3 run `25963750751` green | Is PR #3 merged or still a side branch? |
| Packaging / shipped CLI imports | PARTIAL | PR #3 wheel smoke green | Does canonical main have the fix? |
| Provider egress boundary | PARTIAL | CC-007 runtime companion + tests | Are all seat-local provider paths actually wrapped in production dispatch? |
| Card signed assets | PARTIAL | rows 226-262 + card YAML signatures | Do loader/signature gates enforce, or only declare? |
| F-CARDS loader/gates | ASPIRATIONAL/PARTIAL | `NotImplementedError` in loader, validators, many F-CARDS gates | Is "loaded" safe wording before v0.2 body landings? |
| Reflection Packet | PARTIAL | §16 LOCK + audit findings | Is it dormant, live, or half-activated in the current converged branch? |
| Memory query/consolidation | PARTIAL | CLI work + memory index updates | Is it operator-invoked only or automatic at session start? |
| Brain/JIT | ASPIRATIONAL | alignment brief only | What local/sovereign wrapper is required before use? |
| FID Phase 1 | PARTIAL | scaffold + dispatch plans | Is any funder intelligence artifact locked, or only pre-staged? |
| PA foundation corpus | REAL locally, PARTIAL canonically | `data/`, `pipeline/funder_corpus/`, docs | Is large data ignored and reproducibly regenerable? |
| Customer deployment readiness | PARTIAL | runbook + alpha checklist | Are Gate 1 and Gate 2 labels used consistently? |

## Audit Posture Needed Next

The next audit should not re-run the old 2026-05-16 prompt verbatim. It must be a reconciliation audit with three simultaneous baselines:

1. **Current local dirty workspace** at `/Users/goldenquill/Downloads/GoldenQuill`.
2. **Canonical GitHub main** at `origin/main` / `HyphaeNated/GoldenQuill`.
3. **PR #3 clean CI branch** at head `2d68a3f`.

The audit must answer:

- Which findings from the earlier tandem audit are now closed, which remain open, and which changed severity?
- Which claims are true in lock_history but false or unproven in runtime?
- Which claims are true locally but not yet true in canonical Git?
- What exact work is required for Gate 1 internal replay with Paul?
- What exact work remains for Gate 2 first paid client?
- Which artifacts are research/planning only and must not be represented as runtime features?

The prompt for that audit is filed separately at:

`pipeline/handoffs/project_wide_reconciliation_audit_prompt_2026-05-16.md`
