---
title: GoldenQuill Repository Research Findings Ledger
date: 2026-05-29
dispatch: goldenquill-repository-research-20260529
status: research-receipts
---

# Repository Research Findings Ledger

## Run Scope

Read-only repository research run. No `orgs/*/PROJECT_CONTEXT.md` files were read. Subagents inspected architecture, feature/workflow surface, verification, governance/current-truth, data/security/org isolation, and product/UI surfaces.

## A1 Implementation Architecture

Paths read included `pyproject.toml`, `golden_quill_substrate/`, `pipeline/nervous_system/`, `pipeline/orchestrator/`, `pipeline/loop/`, `pipeline/logician/`, `pipeline/sovereignty/`, and `pipeline/vault/`.

Material findings:

- `golden_quill_substrate/contracts.py` is schema authority only. It explicitly does not own authorization, routing, retrieval, or state transitions.
- `pipeline/nervous_system/api.py` is the HTTP/control surface for identity, applied-as, route mode, human reauth, command handling, action handling, and projection reads.
- `pipeline/orchestrator/router.py` owns seat dispatch and cloud/local provider routing.
- `pipeline/orchestrator/provider_boundary.py` is the canonical cloud egress wrapper.
- `pipeline/logician/pre_gate.py` and `pipeline/logician/gate_runner.py` own PRE/POST gate sequence and state-machine discipline.
- `pipeline/vault/vault_write.py`, `pipeline/vault/gate_and_open.py`, and `pipeline/sovereignty/boot.py` form the persistence, path-safety, and boot-trust layer.
- `pyproject.toml` package discovery includes `pipeline*` but not `golden_quill_substrate*`.

Improvement candidates:

- Add wheel/install smoke coverage for `golden_quill_substrate.*` if it is meant to ship.
- Consolidate or generate classification-context types used by router and provider boundary.
- Document caller-owned factory obligations in `pipeline/loop/`.
- Decide whether Cedar remains a v0.1 text shim or enters a governed v0.2 runtime integration route.

## A2 Feature And Workflow Surface

Paths read included `skills/*/SKILL.md`, `pipeline/cli/*.py`, `tilth/bin/`, `apps/`, `pipeline/orchestrator/seats/`, `pipeline/seats/`, `pipeline/loop/`, `pipeline/scout/`, `pipeline/nervous_system/`, and tests inventory.

Material findings:

- Scout has a broad production contract: discover, verify, review, and six discovery channels.
- The orchestrator Scout seat is narrower than the full Scout architecture.
- `pipeline/cli/tilth_scout_ui.py` and `docs/scout_dev_vs_production_path.md` identify a dev bridge that intentionally bypasses production classification, sovereignty boot, vault writes, and audit trail.
- Skills expose more product intent than code proves in some lanes.
- CLIs cover intake, classification review, memory, metrics, FID, WPFA, and Scout/UI work.
- `apps/tilth_ui/src/App.tsx` is still starter-like, while `apps/tilth_ui/server.mjs` serves a stitch shell/local command surface.

Improvement candidates:

- Create a skill/CLI/module/test coverage index with statuses: `implemented`, `dev-only`, `scaffold`, `spec-only`.
- Add a current callable-entrypoints table to `docs/scout_dev_vs_production_path.md`.
- Generate a CLI inventory from `pipeline/cli/*.py`.
- Classify or quarantine Vite starter UI files if they are no longer the real surface.

## A3 Verification And Quality

Paths read included `tests/`, `.github/workflows/ci.yml`, `.github/workflows/signature_roundtrip.yml`, `scripts/run_tests.sh`, `scripts/run_lint.sh`, `pipeline/linting/`, and `docs/LOCAL_DEVELOPMENT.md`.

Material findings:

- `scripts/run_tests.sh` and `scripts/run_lint.sh` require `.venv/bin/python3` and Python `>=3.11`.
- `.github/workflows/ci.yml` runs lint and tests on Python 3.11 and 3.12, plus a wheel-install smoke.
- `.github/workflows/signature_roundtrip.yml` verifies signed assets but may not yet be branch-protection required.
- `pipeline/linting/ast_lint.py` registers the main AST lint bundle.
- Test inventory found 425 `test*.py` files; largest clusters are `logician`, `seats`, `nervous_system`, `loop`, `vault`, `sovereignty`, `scout`, and `linting`.

Improvement candidates:

- Make `signature-roundtrip` branch-protection required once stable.
- Add one `scripts/verify_all.sh` wrapper for tests, AST lint, and signature verification.
- Add a lightweight CI job that runs documented local quick-start verification.
- Add a macOS or Python 3.14 smoke lane if Josh's local pin remains operationally important.
- Audit lint rules that are tested but not included in the required lint path.

## A4 Governance And Current Truth

Paths read included `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, `docs/AGENT_CONTEXT_INDEX.md`, `docs/COLLABORATOR_HANDOFF.md`, `docs/TECHNICAL_BACKLOG.md`, `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md`, `pipeline/architecture/v0.1/`, `pipeline/engineering/`, `MEMORY.md`, `lessons.md`, and `vault_shared/cards/publisher_pubkey.signed.yaml`.

Material findings:

- `pipeline/engineering/lock_history.v1.jsonl` is the hard current-truth ledger when sidecar indexes disagree.
- The ledger reaches logical row 292 on 2026-05-18, while `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, and `ACTIVE_BLUEPRINT_INDEX.md` stop around row 279.
- `vault_shared/cards/publisher_pubkey.signed.yaml` records a card-publisher key rotation from `0b1a0bbf...` to `c93f1881...`.
- Rows 276-278 were later revoked/superseded by rows 282-284 and fixed forward by rows 285-292, but front-door docs still treat earlier rows as current.
- `architecture_v7_0_11_card_amendment.md` still self-identifies as draft / lock-ready while other docs treat card-system artifacts as active/signed.

Improvement candidates:

- Refresh `PROJECT_STATUS.md` to row 292.
- Refresh `RUNTIME_MATURITY_MATRIX.md` card rows and key state.
- Refresh `ACTIVE_BLUEPRINT_INDEX.md` to §0.5 v35 / row 292.
- Add a clear reconciliation note for `architecture_v7_0_11_card_amendment.md`.
- Restore or intentionally document absent `daily_logs/`.

## A5 Data, Security, And Org Isolation

Paths read included `pipeline/sovereignty/`, `pipeline/vault/`, `pipeline/orchestrator/provider_boundary.py`, `deployment_posture.py`, `classification_review.py`, `pipeline/nervous_system/model_access_boundary.py`, `route_policy.py`, `pipeline/logician/`, top-level `logician/`, and `vault_shared/`.

Material findings:

- Provider egress is centered in `pipeline/orchestrator/provider_boundary.py`.
- Data class leakage scans happen before and after provider calls.
- `deployment_posture.py` defaults to local-only on missing/malformed state; signature verification is caller-owned.
- `classification_review.py` writes and signs per-org classification registers, then runs F-CLASS register gates.
- Signed-register loading fails closed, but the default `vault_shared/classification/` path is absent in this checkout.
- Org isolation is layered across workspace path gates, Cedar/Python evaluator, filesystem namespace checks, and vault root checks.
- `vault_shared/cedar/org_isolation.cedar` is explicitly skeleton/non-load-bearing; Python evaluator is current authority.

Improvement candidates:

- Provision or document the missing `vault_shared/classification/` default path.
- Ensure production wiring always supplies `operator_signed_register` to `enforce_outbound_boundary`.
- Move posture attestation verification closer to `set_posture()` or document the caller-owned proof path.
- Convert deferred split-context allowlist/leak scans into a tracked Gate 2 item if not already covered.
- Decide when FD broker and bind-mount namespace stubs graduate.

## A6 Product, UI, And Journey Surfaces

Paths read included `docs/FRONTEND_BOUNDARY.md`, `docs/golden_quill_website_build_spec_v1.md`, `docs/project_audit_2026-05-18.md`, `docs/scout_dev_vs_production_path.md`, `docs/whitepapers/*`, `landing/`, `apps/tilth_demo_v0/`, `apps/tilth_ui/`, and `apps/tilth_ui_react/`.

Material findings:

- `docs/FRONTEND_BOUNDARY.md` names `apps/tilth_ui_react/` as the canonical frontend target and `apps/tilth_ui/` as legacy scaffold/archive.
- `apps/tilth_demo_v0/README.md` says it is not production.
- `apps/tilth_ui_react/src/App.tsx` still hardcodes demo identity/cycle data and placeholder/static routes.
- `apps/tilth_ui_react/src/api/SubstrateClient.ts` has the intended backend boundary shape.
- `landing/BRIEF_FOR_NEXT_GENERATOR.md` conflicts with current customer-facing entity discipline by naming Sovereign Node language.
- `docs/whitepapers/*.md` files are detected as Word documents, not readable Markdown.

Improvement candidates:

- Add `docs/PRODUCT_SURFACE_INDEX.md`.
- Add `apps/tilth_ui_react/STATUS.md`.
- Add `apps/tilth_ui/ARCHIVE_NOTICE.md` or move old Stitch material under explicit archive.
- Regenerate or rename mislabeled whitepaper `.md` files.
- Reconcile landing generator brief with website spec and customer-facing vocabulary.

## Parent A7 Existing Candidate Recovery

Existing improvement queues already present:

- `docs/TECHNICAL_BACKLOG.md`: Gate 1, Gate 2, safe-first, Josh-decision, and LOCK-process buckets.
- `docs/github_issues_drafts_2026-05-17.md`: issue-ready hardening drafts for lock history, router schema, gate ordering, metadata isolation, Decimal currency, and more.
- `docs/project_audit_2026-05-18.md`: ranked blast-radius risks and top recommendations.
- `pipeline/roadmap/`: deferred v0.2+ feature explorations.
- `docs/card_system_deep_research_2026-05-17/`: card-system blocker and patch-queue package.

## Parent A8 Net-New Improvement Discovery

Net-new or partially new candidates surfaced by this run:

- Repository current-truth refresh pack: update `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, and `ACTIVE_BLUEPRINT_INDEX.md` to row 292.
- Product surface index: one canonical map for UI, landing, whitepapers, demos, archives, and production target surfaces.
- Implementation-status matrix: map skills, CLIs, modules, tests, and maturity labels.
- `golden_quill_substrate` packaging smoke: prove whether substrate contracts ship in wheels.
- `verify_all` wrapper: local command matching CI expectations.
- Whitepaper format hygiene: rename/regenerate `.md` files that are actually Word documents.

## Residue

- `daily_logs/` is absent though wake-up and docs reference it.
- Current test/lint suite was not run as part of this research; validation is path evidence plus dispatch validation.
- Some candidates need operator decisions before implementation because they touch LOCKed, signed, customer-facing, or governance surfaces.
