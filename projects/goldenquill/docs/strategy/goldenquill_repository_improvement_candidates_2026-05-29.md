---
title: GoldenQuill Repository Improvement Candidates
date: 2026-05-29
dispatch: goldenquill-repository-research-20260529
status: ranked-candidates
---

# Improvement Candidates

## Ranked Candidates

| Rank | Candidate | Candidate Status | Category | Owner Surface | Why It Matters | Validation Path | Next Route |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | Current-truth refresh pack for `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, and `ACTIVE_BLUEPRINT_INDEX.md` | net-new / partial-overlap | safe-first + governance hygiene | front-door docs | Front-door docs stop at row 279 while lock history reaches row 292; this misleads every future research or implementation run. | Compare docs against `pipeline/engineering/lock_history.v1.jsonl` and `vault_shared/cards/publisher_pubkey.signed.yaml`; no LOCKed files edited. | task-session |
| 2 | `docs/PRODUCT_SURFACE_INDEX.md` | net-new | safe-first | docs/product | UI/product surfaces mix target, prototype, archive, demo, generated, and draft artifacts. | Index `apps/`, `landing/`, `docs/whitepapers/`, frontend docs; verify no org data read. | task-session |
| 3 | `docs/IMPLEMENTATION_STATUS_MATRIX.md` mapping skill -> CLI/module/test/maturity | net-new | safe-first | docs/engineering | Skills and visible features outpace proven implementation in some lanes. | Build from `skills/`, `pipeline/cli/`, modules, tests, and maturity vocabulary. | task-session |
| 4 | Wheel packaging smoke for `golden_quill_substrate.*` | net-new | safe-first / CI hardening | pyproject/tests | `pyproject.toml` packages `pipeline*` only; substrate contracts may be absent from installed wheels. | Build wheel, install into temp venv, import `pipeline.*` and `golden_quill_substrate.*`. | task-session |
| 5 | `scripts/verify_all.sh` wrapper | net-new / partial-overlap | safe-first | scripts/CI | Local verification currently requires remembering separate test/lint/signature commands. | Run tests + lint + optional signature check; compare with CI workflow. | task-session |
| 6 | Product/website vocabulary reconciliation | partial-overlap | Josh decision + product docs | landing/docs | Landing brief uses customer-facing Sovereign Node language that conflicts with workspace rules. | Compare `landing/BRIEF_FOR_NEXT_GENERATOR.md`, `docs/golden_quill_website_build_spec_v1.md`, `SOUL.md`. | decision-gate |
| 7 | Whitepaper format hygiene | net-new | safe-first / docs hygiene | docs/whitepapers | `.md` files appear to be Word documents, making source-of-truth unclear. | `file docs/whitepapers/*`; identify canonical docs; rename/regenerate only after operator confirms. | decision-gate then task-session |
| 8 | Signed register production-default path documentation/provisioning | partial-overlap | Gate 2 | vault/classification | Loader default path fails closed when `vault_shared/classification/` is absent. | Verify expected deployment provisioning path; decide whether to document or create template. | decision-gate |
| 9 | Provider-boundary signed-register required wiring check | partial-overlap | Gate 2 / security | orchestrator/provider boundary | Boundary can skip signed-register literal scan when `operator_signed_register=None`; production must never omit it. | Add test or AST lint that production cloud path passes signed register. | task-session |
| 10 | `apps/tilth_ui_react/STATUS.md` | net-new | UI-lane | apps/tilth_ui_react | Target frontend is scaffolded; status doc prevents accidental production claims. | Read frontend boundary and current React files; mark blockers. | task-session |

## Existing Or Recovered Candidates

Already queued elsewhere:

- Gate 1 blockers: F-DIALECT operator-content edits, capstone hash drift, lock-history row-null hygiene, phantom memory reference.
- Gate 2 blockers: Logfire end-to-end verification, M13 end-to-end, Reflection Packet activation, provider HTTP lint maturation, LIVE/DORMANT gate-family manifest.
- GitHub issue drafts: lock-history backfill, router schema validation, gate ordering manifest, vault metadata leakage, Decimal-only currency tolerance.
- Project audit recommendations: signing backup, operational freeze playbook, Paul onboarding green path, glossary, threat model, customer-cycle replay harness, CI hardening.
- Card-system package: existing blocker maps and patch queues under `docs/card_system_deep_research_2026-05-17/`.

## Prior-Art Notes

- The current-truth refresh pack overlaps with cleanup-plan/front-door discipline, but the specific row 292/key-rotation refresh is newly evidenced by this run.
- Product surface index is net-new as an explicit cross-surface artifact.
- Implementation-status matrix is net-new as a crosswalk of skills, CLIs, modules, tests, and maturity labels.
- `verify_all.sh` overlaps with existing scripts but is net-new as a unifying local verification entry point.

## Recommended First Pick

Pick **Rank 1: Current-truth refresh pack** first. It has high leverage, low implementation risk, and directly improves every later research or engineering run.
