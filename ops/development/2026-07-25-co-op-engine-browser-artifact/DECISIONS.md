---
module: co-op-engine-browser-artifact
phase: define
status: blocked
updatedAt: 2026-07-25
decision_gate: product-definition
---

# Define Decision Record

## Gate Result

- Result: BLOCK
- Resolved blocker decisions: 3
- Current question: D-004
- Design handoff: closed
- Source: accepted research findings and candidate Define specification

## D-001 — Product Mechanism

**Question:** What collaboration mechanism should the first Co-Op browser
artifact define?

**Why this blocks:** the choice changes the information architecture, meeting
flow, eligible-card supply, interaction state, measurement denominator, and
meaning of the page when no live meeting is happening.

### Option A — Experiment Exchange with evidence-triggered clinics

- Benefit: all fourteen eligible experiments remain discoverable; live time
  follows observable translation or negotiation needs; reciprocal appointments
  and receipts remain the outcome.
- Cost/risk: requires card-quality discipline, expiry, facilitation rules, and
  enough eligible supply; may feel more operational than a showcase.
- Choose when: asynchronous discovery and mixed-domain participation matter.
- Downstream impact: preserves the candidate state model and meeting route
  already described in `SPEC.md`.
- Reversibility: can shrink to Clinic-only if admitted trials show poor card
  quality or low asynchronous value.
- Research recommendation: **recommended**.

### Option B — Clinic-only Cohort

- Benefit: simpler live facilitation for a small recurring high-trust group;
  useful when eligible-card supply is scarce or access/privacy negotiation
  dominates.
- Cost/risk: weak asynchronous discovery; privileges live attendees; facilitator
  selection becomes more powerful.
- Choose when: the group is small, recurring, and primarily needs translation
  and trust-building rather than open exchange.
- Downstream impact: requires rewriting the meeting route, selection policy,
  self-guided artifact role, and comparison denominators before Design.
- Reversibility: may later open into an Exchange after card quality and demand
  are witnessed.

### Standing Option — Explain / more context

This does not resolve the gate. If selected, expand the evidence, downstream
changes, reversibility, and dependent decisions, then ask D-001 again.

**Selected option:** Option A — Experiment Exchange with evidence-triggered
clinics

**Decision source:** user reply `1`, 2026-07-25

**Rationale:** selected the research-recommended mechanism that keeps all
fourteen eligible experiments asynchronously discoverable while reserving live
time for evidence-backed translation and negotiation needs.

**Status:** resolved

## D-002 — Product and Portfolio Truth Ownership

**Question:** Who should own product decisions and cross-project truth for the
first artifact?

**Why this blocks:** Design needs a named authority for the product mechanism,
display names, maturity vocabulary, verification dates, expiry labels, and
approval of later source corrections.

### Option A — User owns both roles for the first artifact

- Benefit: one accountable authority can resolve names, policy, and Design
  approval quickly.
- Cost/risk: concentrates product and truth-review responsibility; individual
  project owners must still approve their own claims.
- Choose when: this is a founder-led first proof and delegation can follow
  after the first witnessed cycle.
- Downstream impact: record the current user as Co-Op product owner and
  portfolio truth owner, while preserving project-owner veto over local truth.
- Research recommendation: **recommended for the bounded first artifact**.

### Option B — Split the roles

- Benefit: separates product priorities from cross-project evidence review.
- Cost/risk: requires a named second owner and an explicit disagreement rule
  before Design can proceed.
- Choose when: another person already curates project status and can accept the
  evidence/expiry workload.
- Downstream impact: record the user as product owner and wait for the named
  portfolio truth owner plus precedence rule.

### Option C — Leave both roles unassigned

- Benefit: avoids false attribution.
- Cost/risk: Define remains blocked and Design cannot begin.
- Choose when: ownership must be established outside this session.
- Downstream impact: stop after the Define package.

### Standing Option — Explain / more context

This does not resolve the gate. If selected, expand the approval scope,
project-owner veto, conflict handling, workload, and later delegation path,
then ask D-002 again.

**Selected option:** Option A — user owns both roles for the first artifact

**Decision source:** user reply `1`, 2026-07-25

**Rationale:** keep the first proof accountable and fast to adjudicate while
retaining every project owner's veto over its own facts, claim ceiling, and
source interpretation. Delegation remains possible after the first witnessed
cycle.

**Owner identity:** current repository owner/operator, `vrondelli`

**Status:** resolved

## D-003 — Card Admission, SLA, Expiry, Refresh, and Stale Policy

**Question:** Which policy bundle should govern whether a project experiment is
eligible for the first Exchange?

**Why this blocks:** filters, clinic supply, measurements, and public truth all
depend on how quickly owners respond and how long a card can remain current
without reconfirmation.

All options require one accountable owner, source, observable act, current
witness, limitation, claim ceiling, bounded ask, privacy/reuse terms, expected
witness, and stop rule.

### Option A — Weekly operating policy

- Owner response SLA: 48 hours.
- Card expiry: 14 days after owner verification.
- Review cadence: every 7 days and before a card enters a live clinic.
- Stale behavior: expiry immediately removes the card from eligible and clinic
  views but preserves its history.
- Refresh: return to `draft`; require owner reconfirmation, updated verification
  date, and revalidation of changed source, claim, ask, privacy, and schedule
  fields before `eligible`.
- Benefit: matches a weekly meeting without forcing daily maintenance.
- Cost/risk: owners must review at least every other meeting.
- Research recommendation: **recommended for the first proof**.

### Option B — Meeting-bound strict policy

- Owner response SLA: 24 hours.
- Card expiry: 7 days.
- Review cadence: before every meeting.
- Stale and refresh rules: same fail-closed behavior as Option A.
- Benefit: strongest currentness discipline.
- Cost/risk: high owner burden; eligible supply may collapse.
- Choose when: claims, access, or privacy change rapidly.

### Option C — Low-burden monthly policy

- Owner response SLA: 72 hours.
- Card expiry: 30 days.
- Review cadence: monthly and before a clinic.
- Stale and refresh rules: same fail-closed behavior as Option A.
- Benefit: easier for early or lightly staffed projects.
- Cost/risk: stale asks and misleading availability can persist too long for a
  weekly exchange.
- Choose when: the artifact is mostly asynchronous orientation.

### Standing Option — Explain / more context

This does not resolve the gate. If selected, expand the effects on eligible
supply, owner workload, currentness, measurements, and false recruitment
signals, then ask D-003 again.

### Explanation requested — 2026-07-26

The user selected `Explain / more context`. That reply did not resolve D-003;
the later Option C selection is recorded below.

The fields govern different risks:

- **Response SLA** is how long an owner may leave a new offer unanswered. It is
  not a promise to accept the offer.
- **Expiry** is how long the card's availability and evidence assertion may be
  treated as current. It is not deletion.
- **Review cadence** is an earlier checkpoint; it can refresh a still-valid
  card or remove it before expiry.
- **Stale** means preserved for orientation and history but removed from
  eligible, clinic, and new-appointment flows.
- **Refresh** is a new admission attempt, not a button that silently restores
  the prior card.

Common fail-closed behavior for every real option:

1. A missed response SLA moves the card to `response_overdue`; it remains
   inspectable but cannot enter a new candidate pair or clinic until the owner
   responds.
2. Expiry moves the card to `stale`; existing appointments and receipts remain
   visible to their permitted participants.
3. Refresh returns the card to `draft` and requires owner reconfirmation,
   verification date, and revalidation of changed source, claim, ask, privacy,
   effort, and schedule fields.
4. Every card and receipt records the policy version that governed it, so a
   later policy change does not rewrite historical meaning.

| Policy | What changes operationally | Owner burden | False-availability risk | Likely effect on first proof |
| --- | --- | --- | --- | --- |
| A — 48h / 14d / weekly review | A card may span two weekly meetings but receives a midpoint review. | moderate | moderate, bounded by weekly check | enough eligible supply to test the Exchange while still exposing maintenance cost |
| B — 24h / 7d / every-meeting review | Every live meeting requires a fresh owner assertion. | high | lowest | cleanest currentness, but early projects may disappear and make the Exchange look empty |
| C — 72h / 30d / monthly review | One assertion may span roughly four meetings. | low | highest | easier catalog maintenance, but weak evidence about whether offers are actually available now |

Concrete example: if a Poker bot author offers help on Monday and the owner has
not answered by Wednesday under Option A, the card can still explain the
project but cannot recruit another candidate pair until the owner responds. If
the owner does respond, the card still expires fourteen days after its last
verified admission unless the weekly review refreshes it.

Dependent decisions:

- D-004 must decide which overdue, stale, owner-contact, and historical fields
  each audience may see.
- The acceptance contract must count `eligible`, `response_overdue`, and
  `stale` separately; hiding overdue or stale records would inflate the
  denominator.
- Design must make time and policy version explicit and testable instead of
  relying on an implicit browser clock.

**Recommendation remains Option A.** It best matches a weekly meeting, gives
owners two meeting cycles of validity, and still creates a weekly opportunity
to detect stale asks. Option B is safer when source, privacy, or access changes
every week. Option C is appropriate only if the artifact becomes primarily a
catalog rather than an active weekly exchange.

All three bundles are reversible after witnessed sessions because the policy is
versioned. Changing policy must affect future admission and refresh only; it
must not reinterpret prior appointments or receipts.

**Selected option:** Option C — low-burden monthly policy

**Decision source:** explanation requested by user reply `4`, then Option C
selected by user reply `3`, 2026-07-26

**Rationale:** minimize maintenance pressure on early and lightly staffed
projects while preserving fail-closed overdue, stale, refresh, history, and
policy-version semantics. The product must measure whether the longer validity
window produces misleading availability.

**Approved policy**

- Owner response SLA: 72 hours.
- Card expiry: 30 days after owner verification.
- Review cadence: monthly and before every live clinic.
- Missed SLA: `response_overdue`; inspectable but blocked from new candidate
  pairs and clinics.
- Expiry: `stale`; removed from eligible and clinic views, history preserved.
- Refresh: return to `draft`; require owner reconfirmation, new verification
  date, and revalidation of changed source, claim, ask, privacy, effort, and
  schedule fields.
- History: every card, appointment, and receipt retains its governing policy
  version.

**Status:** resolved

## D-004 — Privacy Ownership and Visibility-Matrix Process

**Question:** Who should own privacy policy for the first artifact, and what
scope should Design admit?

**Why this blocks Design:** the artifact may carry participant offers,
availability, owner contacts, appointments, receipts, story-state proposals,
and presenter metadata. Design cannot close its selectors until every field has
one visibility owner and disallowed data is excluded from route, DOM, network,
storage, export, screenshot, and trace surfaces.

### Option A — User owns privacy for a deny-by-default first proof

- The current user owns the privacy policy and field matrix for the first
  proof.
- Every field receives exactly one minimum visibility class: `public`,
  `meeting_visible`, `assigned_collaborator`, `participant_private`, or
  `owner_private`.
- Unclassified fields block rendering, transport, persistence, and export.
- Initial fixtures use synthetic or explicitly consented low-risk participant
  data.
- An independent negative leakage audit remains mandatory before public use.
- Benefit: keeps the first Design moving with one accountable policy owner.
- Cost/risk: policy and product ownership remain concentrated.
- Research recommendation: **recommended for the bounded first proof**, with
  independent audit separation.

### Option B — Assign a separate privacy owner

- The user remains product owner; a named second person owns the visibility
  matrix, consent, retention, and leakage policy.
- Benefit: separates product pressure from privacy adjudication.
- Cost/risk: Design remains blocked until the person accepts the role and
  precedence rules.
- Choose when: the artifact will use real participant data during the first
  proof.

### Option C — Public/demo-only first proof

- Design admits only public project fields and synthetic interaction records.
- Real participant identity, availability, negotiation, appointment, and
  receipt data stay outside the artifact.
- Benefit: smallest privacy surface and simplest initial browser proof.
- Cost/risk: cannot witness the full recruitment-to-receipt loop in-product;
  those steps remain facilitated/offline.
- Choose when: proving page/presentation projection matters more than testing
  the complete collaboration workflow.

### Standing Option — Explain / more context

This does not resolve the gate. If selected, expand the field classes,
observable-surface threats, consent/retention implications, independent-audit
boundary, and what each option removes from the first proof, then ask D-004
again.

**Selected option:** Option A — user owns privacy for a deny-by-default first
proof

**Decision source:** user reply `1`

**Rationale:** This keeps one accountable privacy policy owner for the bounded
proof while preserving independent challenge. Every admitted field must have
exactly one minimum visibility class. Unclassified fields fail closed across
rendering, transport, persistence, export, screenshots, and traces. Initial
fixtures are synthetic or explicitly consented and low-risk. An independent
negative leakage audit remains mandatory before public use.

**Status:** resolved

## D-006 — Implementation and Deployment Target

**Question:** Where should the first browser artifact live, and how should its
first deployment be exposed?

**Why this blocks Design:** component boundaries, write scope, build commands,
browser fixtures, access controls, hosting metadata, and deployment evidence
cannot be selected until the artifact has one implementation home.

### Option A — New isolated Co-Op Engine project with restricted deployment

- Create a dedicated browser app under `projects/co-op-engine/`.
- Treat the page and meeting presentation as two projections of one application
  and one admitted data model.
- Establish a new Sites project and checked-in `.openai/hosting.json` during
  implementation.
- Keep the first production deployment access-restricted until the privacy,
  black-box, comprehension, coherence, conversational-language, and naming
  gates pass.
- Benefit: durable ownership, exact write scope, realistic browser/deployment
  evidence, and no coupling to an unrelated product.
- Cost/risk: adds a new project surface and hosting lifecycle that must be
  maintained.
- Recommendation: **recommended** for a real website/presentation proof.

### Option B — Repository-local, local-only prototype

- Build under
  `ops/development/2026-07-25-co-op-engine-browser-artifact/prototype/`.
- Validate in a local browser with synthetic fixtures; do not deploy.
- Benefit: smallest reversible implementation surface.
- Cost/risk: proves the interaction locally but not hosting, access control,
  deployment, or durable product ownership.
- Choose when: the immediate goal is interaction learning rather than a
  recruitable website.

### Option C — Integrate into the existing DomainSpec web application

- Add the artifact to `implementation/domainspec/apps/web/`.
- Reuse its application/tooling boundary and deploy through that product's
  future hosting route.
- Benefit: reuses an existing frontend surface.
- Cost/risk: couples a cross-project recruitment product to the private
  DomainSpec application, expands regression scope, and obscures ownership.
- Choose when: Co-Op Engine is intentionally a DomainSpec product feature, not
  a portfolio-level product.

### Standing Option — Explain / more context

This does not resolve the gate. If selected, compare lifecycle ownership,
hosting/access-control evidence, public/private boundaries, test scope, and
the migration cost between a prototype and durable project, then ask D-006
again.

**Selected option:** Option A — new isolated Co-Op Engine project with
restricted deployment

**Decision source:** user reply `1`

**Rationale:** A dedicated `projects/co-op-engine/` application gives the
website/presentation one durable owner and exact browser boundary without
coupling it to the private DomainSpec application. Implementation will create
the Sites project and checked-in `.openai/hosting.json`. The first production
deployment remains access-restricted until privacy, black-box UI,
comprehension, coherence, conversational-language/copy, and naming gates pass.

**Status:** resolved

## Queued Decision

| ID | Decision | Class | Why it matters |
| --- | --- | --- | --- |
| D-005 | Assign publication/naming review for precedents and public labels. | pre-publication blocker | Internal lineage and third-party names cannot imply endorsement. |

## Deferrable Decisions

- exact clinic signal threshold and room-size rule;
- listener evidence taxonomy;
- two-meeting stop-rule calibration;
- later exchange-without-clinics comparison;
- authoring/admin interface beyond the first bounded record flow.

## Assumptions

- The two audience profiles remain technical builder without internal-framework
  context and writer/musician-like domain practitioner building with AI.
- Veritasium lineage remains internal-only.
- Audit contracts remain proposed until executable and witnessed.
- Whisper composition remains downstream of stable truth and surface contracts.
