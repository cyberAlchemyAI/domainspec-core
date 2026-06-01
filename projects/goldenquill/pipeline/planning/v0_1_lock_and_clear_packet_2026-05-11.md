---
title: v0.1 lock-and-clear packet
filed: 2026-05-11
operator: Josh
status: ACTIVE_CLEARANCE_PACKET
supersedes:
  - pipeline/planning/v0_1_beta_readiness_2026-05-10.md
  - pipeline/planning/v0_1_beta_launch_posture_2026-05-10.md
canonical_repo: https://github.com/HyphaeNated/GoldenQuill.git
initial_commit: d3bc8b100b30e75f37afcf59483d565ec6ac69e2 (2026-05-15 16:58 EDT — "Initial commit: Golden Quill workspace bootstrap"; 1407 files, 59.3 MB; author HyphaeNated noreply email)
purpose: Define exactly what must be true to declare v0.1 locked enough to move primary build attention to v0.2.
---

# v0.1 Lock-and-Clear Packet

## Decision

v0.1 is not the full Golden Quill product arc. v0.1 is the headless, single-tenant, BYOK, local-first grant submission workstation: Intake, Classification Review, classification-aware routing, Scout/Scribe/Editor/Judge/Red Team/Logician, Uploader prepare-and-stage, human final submit, and an audit trail.

v0.2 begins after v0.1 has a reproducible submission-mode run package and the public language no longer overclaims sovereignty, local-only processing, post-award reporting, or legal-entity posture.

## Dogwood Proof

Dogwood counts as operational proof: a real external client deliverable was completed end-to-end through OpenClaw, and the client was pleased.

What Dogwood does not yet provide by itself is the v0.1 clearance artifact an outside engineer needs: a reproducible repo-backed run packet. The next proof should not be another client delivery. It should be a sanitized or internal replay with:

- input manifest
- Classification Review register path + signature status
- routing decisions
- model-call boundary log
- final staged package path
- Uploader no-auto-submit proof
- audit trail path
- focused test command + result

## Current Clearance Gates

| Gate | Status | Evidence | What remains |
|---|---:|---|---|
| Scope freeze | DONE | This packet defines v0.1 as submission-mode only. | Do not pull v0.2 rows into v0.1. |
| Data/posture claim cleanup | DONE | README, SOUL, CLAUDE, white-glove playbook, architecture overview, and website FAQ now use local-first/BYOK/approved-cloud-route language. | Re-run claim grep before outside review. |
| Legal/name posture cleanup | DONE for live docs | Live docs now say FIT Farms LLC is the current legal entity and Golden Quill is its project until future spin-off. | Historical locked/audit files still contain old language and should be treated as archive. |
| Classification register authority | DONE | Canonical register path is `orgs/<slug>/vault/classification/register.yaml`; white-glove playbook now matches the orchestrator. | Keep this path singular in all future docs. |
| F-CLASS-COVERAGE wording | DONE | Live docs now describe it as a runtime enforcement-module/test coverage gate, not an unset-field gate. | Do not reintroduce the old wording. |
| Router cloud boundary | DONE | `pipeline/orchestrator/router.py` requires `classification_context` before cloud dispatch; tests live at `tests/orchestrator/test_router_classification_boundary.py`. | Keep these tests in the v0.1 smoke suite. |
| Intake/Uploader current-tree proof | DONE | Focused v0.1 smoke suite passed 339 tests on Python 3.14; AST lint on `pipeline/` passed. | Keep this suite as the v0.1 regression bar. |
| Reproducible submission dry run | OPEN | Dogwood proves delivery through OpenClaw. | Produce one repo-backed replay packet before serious technical handoff. |
| Technical lead handoff | DONE | `docs/v0_1_TECHNICAL_LEAD_BRIEF.md`. | Keep it under revision control as the first outside-review artifact. |

## v0.1 Smoke Test Bar

Before marking v0.1 clear, run a focused suite that covers:

- router classification boundary
- F-CLASS coverage + outbound boundary gates
- Classification Review orchestrator
- Intake seat
- Uploader seat
- CIC x CLC orthogonality guard
- AST lint on `pipeline/`

Recorded 2026-05-11:

```bash
scripts/run_tests.sh tests/orchestrator/test_router_classification_boundary.py tests/logician/gates/test_f_class_coverage_incomplete.py tests/logician/gates/test_f_class_outbound_boundary.py tests/logician/gates/test_f_class_routing_indeterminate.py tests/integration/classification_review tests/seats/intake tests/seats/uploader tests/logician/gates/test_f_cic_clc_coupling_violation.py tests/logician/gates/test_f_cic_clc_match_null.py tests/logician/gates/test_f_cic_clc_enum_drift.py
```

Result: `339 passed in 1.80s`.

```bash
scripts/run_lint.sh pipeline
```

Result: clean exit `0`.

## Safe Public Language

Use:

> Golden Quill is local-first and BYOK. Confidential and Operator-flagged content stays local. Public + Shareable content may use explicit approved cloud routes under the operator's own keys, with routing recorded in the audit trail.

Do not use until separately enforced by OS/network policy:

- "nothing phones home"
- "no cloud dependency"
- "no data exfiltration"
- "Sovereign mode" as a mechanical guarantee
- "post-award reporting burden disappears" for v0.1

## What Is Not a v0.1 Blocker

- Data Collector runtime
- Report Generator runtime
- Cultivator phone interface
- UI / Next.js / dashboard
- multi-tenant support
- managed edition
- metered billing
- State-rules cards
- Twilio/Postmark/MTProto/WhatsApp BYOK envelope
- Stage-5 Sovereign Node commons
- OS/firewall-enforced Sovereign mode, as long as the public language stays at local-first/BYOK/explicit approved cloud routes

## Move-To-v0.2 Rule

Primary build attention can move to v0.2 when:

1. The smoke test bar above is green or any exceptions are named as non-v0.1.
2. One reproducible submission-mode replay packet exists.
3. Live public/docs language is clean under the claim grep.
4. The technical lead brief exists and points to the current lock packet.
5. The founder explicitly accepts that v0.2 work starts while historical archive docs still contain old language.

## v0.2 First Target

After v0.1 clears, the clean first v0.2 target is post-award evidence/reporting hardening:

- Data Collector runtime path
- Report Generator runtime path
- Report-mode activation in track registry
- State-rules/BYOK communications envelope
- post-award consent and privacy review

Do not reopen v0.1 architecture to do this. Treat v0.2 as a new build lane fed by the v0.1 submission/audit substrate.
