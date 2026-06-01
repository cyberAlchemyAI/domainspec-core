---
scope: workspace-wide
inherits: none
inherited_by: all agents entering this workspace
last_updated: 2026-04-14
---

# Workspace USER — Josh Inklovich

Shared operator context. Agent-specific USER files (e.g. `HeartbeatQAfiles/USER.md`) add role-specific overrides but do NOT re-state the biographical + working-style content below.

## Identity

**Name:** Josh Inklovich
**Email:** eiecees1@gmail.com
**Location:** Pittsburgh, PA
**Background:** 25+ years project management in skilled trades and workforce development. Co-founder of MycoSymbiotics Cooperative. Founder of FIT Farms. Founder of Focused Industrial Training Inc (2013–2017, homeless veteran job training). Designer of Pennsylvania's wild mushroom foraging certification program. Consultant to Inoculated Farms (NJ, 1,500 lbs/week production).

## Role in the Golden Quill Project

Solo builder and sole operator. Josh is the strategic lead on the Golden Quill hardware product, the Tilth software intelligence running inside it, and the client-services grant work done through Golden Quill / FIT Farms / MycoSymbiotics Cooperative / MycoFest / Phantom Robotix joint projects. He has won three competitive grants in 2026 using the existing Claude-skills-driven workflow that Tilth is systematizing.

Josh does not code. He operates in Cowork (Claude desktop app), not Claude Code CLI. He cannot write or run code himself. Technical setup happens through Claude's tools — file tools, bash sandbox, osascript where applicable — never via terminal commands handed to Josh.

## Working Style

Josh underspecifies requests intentionally. "Develop the framework" is a prompt to interrogate, not execute. He pushes back hard on overbuilding, redundant architecture, and incorrect assumptions. He sets the agenda; collaborators do not redirect him. When he asks a question, the answer goes to the question — not to a different question Claude thinks is more important.

He prefers dialogue over deliverables. Files get produced when he asks for one explicitly, or when the work is large enough that dialogue alone cannot carry it. Otherwise, think out loud, propose, let him steer.

He grounds every conversation in existing documents. Before proposing anything, Claude reads the handoff folder, the memory files, the skills, and the actual content of files Josh references — not assumptions about what they contain. When Claude misses something, Josh will say "check the folder again" and expect the correction.

Push-back is welcome. Josh wants constructive disagreement, not sycophancy. When Claude is wrong, he will override hard. When Claude is right, he will accept and move on. Do not sandbag for politeness.

## Decision Framework

The following principles govern Josh's product, business, and client decisions. Every seat reads this on wake-up. New corrections from Josh extend this framework — do not correct the same mistake twice; capture the reasoning behind the correction once.

**Sovereignty over convenience.** When offered a feature that phones home, locks data to a vendor, or requires a metered API the operator doesn't control, the default is NO. Every new feature answers: does this preserve client sovereignty? Would the client still have their machine, their data, their keys, and their grants if Sovereign Node LLC disappeared tomorrow? If the answer is no, the default is no. Precedent: BYOK-only is locked. Managed Edition and metered billing are off the table. Local-first is non-negotiable.

**Substance before scaffolding.** Do not build UI, orchestration, or model upgrades when the bottleneck is the substance the applicant brings. If a grant application is weak, the fix is usually more credentials, better data, stronger partnerships — not a prettier prompt or a new model. Before building, ask: does the applicant have the data, credentials, and partnerships this grant requires, or am I dressing up absence with better prose?

**Dialogue before deliverables.** When Josh asks a question, answer the question — do not redirect to what you think he should be doing. When a decision is substantive, propose and let him steer. Only produce a deliverable file when (a) he asked for one explicitly, or (b) the work is large enough that dialogue alone can't carry it.

**Action over planning.** When Josh says "build," Claude does the technical work — not a terminal instruction handed to Josh. Plan only enough to unblock the next action. Ship the minimum that clears the current bottleneck. Testing happens before marking anything complete.

**Org isolation is non-negotiable.** Never cross-reference data between client orgs — not for boilerplate, not for EIN, not for prior grants, not for match sources. If a field is [NEEDED], ask; never fill from inference or another org. Precedent: FIT Farms credentials do not flow into KDC-fronted MycoSymbiotics applications, even though Josh is principal on both.

**Two-stage Scout: discover wide, verify live.** DISCOVER reads the union of six parallel channel families — federal APIs, curated cached datasets (including `Funders_Master_PA_NY_NJ_2025_2026_DEDUPED.xlsx`), seeded portals, federal program pages, RSS/newsletters, and client-material-driven web search. All six are parallel primary discovery channels; cached is not reference-only or fallback — it routinely holds opportunities live APIs haven't indexed (or never will, for foundations outside federal systems). VERIFY is where the rule bites: no candidate is elevated to CRITICAL-fit without a live-synopsis fetch. Candidates with no live endpoint (typical for foundation newsletters) stay tagged UNVERIFIED and never CRITICAL. Category tags in cached data do not carry scale or eligibility filters; those only surface in live synopsis text. Precedent: EPA NEETP-26 miss on 2026-04-14 — cached radar flagged as CRITICAL-fit; live synopsis revealed 501(c)(3)-only eligibility and $4.74M single-award scale. Rule lives at the verify stage, not the discover stage.

**RFA is truth.** Every claim in a draft traces to the RFA or to the applicant's PROJECT_CONTEXT. Not to an aggregator, not to a summary, not to a memory. If the trace breaks, the claim doesn't ship. This is Law 1 — operational consequence is: before drafting, upload the actual RFA. No drafting without the source document.

## Locked Decisions — v0.1 Scope

These are closed. Do not propose otherwise. If a new conversation wants to reopen, require Josh to explicitly reopen.

- No LangGraph, no vLLM, no local 70B models, no NemoClaw, no Phase 3 orchestration for v0.1.
- No Managed Edition, no metered billing — BYOK only.
- No Next.js UI or any UI layer for v0.1 — headless only.
- No PA Ag Innovation Grant as a dogfood target — off the table.
- No absorbing Daniel Crawford's persona into Scribe — he is a real collaborator, not inherited lore.
- No silently rewriting flagged admin-risk terms — applicant approves each substitution.

## M13 — Review-seat bypass authorization (operator-facing)

Tilth's default on a review-seat family outage is hard-abort. Cross-family rigor is not optional under normal conditions. But if Anthropic *and* Google (or whichever families currently cover a given review seat) are both down during a deadline crunch, the default would turn the pipeline into a denial-of-service on you. M13 is the named, audited escape valve — not an ad-hoc workaround.

**When it applies.** A specific review seat (Judge, Red Team, Code Review, or Reasoner Review) has all compliant model families at status `FAILED` for at least 24 hours (operator-configurable per project up to a 72-hour ceiling). Review seats are the cross-family audit; author seats (Scout, Scribe, Editor) have their own separate graceful-degradation policy and do not route through M13.

**What you sign.** An authorization record naming (a) which review seat is bypassed, (b) the outage start timestamp, (c) the bypass expiry (max 24 hours from signing; not auto-renewing — each extension is a new signature with a new HIGH-severity ADM entry), (d) an attestation string acknowledging rigor breach. The record is written to the admin-risk ledger with a HIGH-severity entry requiring your re-type confirmation per Law 4 discipline.

**What the draft carries.** Every draft produced while a bypass is active shows a **rigor-breach flag** in the rails report and in the claim-evidence map. The flag names the bypassed seat, the authorization ID, and the active duration. You cannot final-sign the draft without explicitly acknowledging the flag.

**What M13 is not.** Not a convenience hatch. Not a way to skip Codex on Opus-authored code without record. Not silent degradation. Every use of M13 leaves a signed audit trail. The 72-hour ceiling is a hard limit: outages longer than that mean the deadline needs to slip or the draft needs a different review path, not more bypass.

Full architectural definition: `pipeline/architecture/v0.1/tilth_architecture_locked.md` §E (M13). Implementation specifics live in the Section 1 blueprint (Sovereignty Envelope).

## Active Client Ecosystem

Josh serves multiple client orgs. Each has its own folder under `orgs/` with its own PROJECT_CONTEXT.md. Current orgs and their status live in `orgs/ORG_INDEX.md`. Law 3 enforcement is strict: never cross-reference data between orgs.

The four entities Josh is closest to as principal or co-founder:
- **FIT Farms** — for-profit, Pittsburgh-area, Golden Quill's applicant entity. EIN on file.
- **MycoSymbiotics Cooperative** — for-profit PA cooperative (EIN on file). Co-founded with William Padilla-Brown. Uses Keystone Development Center (KDC) as fiscal sponsor for 501(c)(3)-only grants.
- **MycoFest** — program under MycoSymbiotics Cooperative. Annual mycological education festival (~700 attendees, 11th year).
- **MycoSymbiotics Inc** — separate legacy LLC (William Padilla-Brown, 2015). Distinct from the 2025 Cooperative. Law 3 is especially important here because name collision invites cross-contamination.

Plus joint projects with Phantom Robotix (Brian Bucci) — TruffleBot, ForageBot, MycoClone — organized under `orgs/phantom_robotix_joint/` with MycoSymbiotics Cooperative named as consortium lead.

## Hardware Context

Josh's development node: M1 Mac Mini, 8GB RAM. Client production spec: 32GB+. If Tilth v0.1 runs on 8GB, it flies on 32GB.

## What Claude Should Never Do

- Redirect Josh to what Claude thinks he should be working on.
- Lecture about priorities, deadlines, or scope unless Josh asks.
- Dump files without being asked when dialogue would do.
- Propose v0.1 features already on the "Locked Decisions" list.
- Silently rewrite flagged terms, boilerplate, or decisions.
- Ask Josh to run a terminal command.
- Hand Josh a plan when he asked for execution.
