# Golden Quill / Tilth v0.1 Technical Lead Brief

## What This Is

Golden Quill is FIT Farms LLC's customer-owned AI workstation project. Tilth is the headless grant/funding workflow system that runs on one Golden Quill.

v0.1 is a single-tenant, BYOK, local-first submission workstation. It ingests organization context, classifies data, finds and verifies opportunities, drafts and reviews grant sections, applies deterministic gates, stages the final package, and leaves final submission authority with the human operator.

## What This Is Not

v0.1 is not a UI product, managed SaaS product, multi-tenant platform, post-award reporting system, phone-capture system, or cooperative commons. Those are v0.2+ or later.

## What Is Already Real

- Grant-finder and grant-writer skills are deployed in Cowork and have produced funded-grade outputs.
- Josh won three competitive grants in 2026 using the current skills-based workflow.
- Dogwood was delivered end-to-end through OpenClaw for a real external client.
- The repo now contains locked architecture/blueprints, deterministic gate modules, Classification Review tooling, Intake/Uploader seats, and router boundary tests.

## Non-Negotiables

- Headless v0.1.
- Single tenant.
- BYOK only.
- Human final submit.
- No Managed Edition or metered billing.
- Classification-driven routing.
- Confidential and Operator-flagged data stay local.
- Public + Shareable content may use explicit approved cloud routes.
- Pydantic AI + Logfire + Ollama/vLLM + deterministic Logician gates remain the substrate.

## What Must Work Before v0.1 Clears

1. Classification Review produces a signed register at `orgs/<slug>/vault/classification/register.yaml`.
2. Cloud routing is impossible without a classification context.
3. Semantic slot names never reach cloud prompts.
4. Post-fill drafts route local.
5. Intake can populate/extend the KFR with operator-confirmed facts.
6. Uploader stages packages but cannot auto-submit.
7. Logician gates fail closed.
8. One reproducible submission-mode run packet exists.
9. Public language says local-first/BYOK/approved cloud routes, not "nothing phones home."

## What Can Stay Manual in Phase One

- White-glove onboarding.
- Customer file organization.
- First Classification Review.
- Final grant strategy judgment.
- Final portal submit.
- Customer support.
- Security review triage.

Manual is acceptable only where the audit trail is explicit. Manual hidden inside claims of automation is not acceptable.

## First Engineer Tasks

1. Run the v0.1 smoke suite named in `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md`.
2. Build a sanitized replay packet from an internal or Dogwood-shaped run.
3. Verify no direct cloud model path bypasses `pipeline/orchestrator/router.py`.
4. Re-run claim grep across README, docs, and website assets.
5. Produce a one-page data-flow/trust-boundary diagram.

## What To Ignore Initially

- UI.
- multi-tenant design.
- Stage-5 commons.
- phone/Cultivator capture.
- Report Generator runtime.
- Data Collector runtime.
- payment/billing.
- hardware fleet ops beyond one Golden Quill.

## Founder Care-Abouts

Josh cares about sovereignty, grant correctness, customer trust, and getting the working manual/OpenClaw operation hardened into a reproducible system. Do not replace the architecture. Make the locked system runnable, provable, and easier to hand off.
