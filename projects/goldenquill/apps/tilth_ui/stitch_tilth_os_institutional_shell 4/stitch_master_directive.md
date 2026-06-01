# STITCH MASTER DIRECTIVE — Golden Quill / Tilth Operator Console

Use this document together with `DESIGN.md`. `DESIGN.md` controls the visual system: colors, typography, layout, elevation, shapes, and component styling. This file tells Stitch what the application is, what screens to generate, what interaction behaviors are mandatory, and what must not be invented.

The output should be a desktop-first interface prototype for Golden Quill: an operator-owned grant intelligence workbench running Tilth. It is not a chatbot, not a generic SaaS dashboard, not a grantmaker CRM, and not an autonomous grant-submission system.

Golden Quill is the node. Tilth is the funding operating system inside it. The UI is the operator console where a human runs a structured agent council through funding work: discovery, evidence intake, eligibility gating, section decomposition, drafting, scoring, adversarial review, budget validation, final sign-off, audit, and institutional memory.

The product thesis is:

> Golden Quill gives mission-driven organizations a governed, local-first grant workbench where AI accelerates funding work, but the operator retains authorship, judgment, custody, and signature authority.

Every screen should answer one operator question, expose the relevant constraints, and show the next valid action. Do not add decorative AI fantasy elements. Do not add a chat surface. Do not hide audit or posture state.

---

## 1. Required Global Shell

Every desktop screen must include the same global shell.

### Top Bar

Always visible. Height approximately 56px.

Left:
- Golden Quill wordmark or compact product mark.
- Active organization or node slug in monospace.
- Current cycle ID if a cycle is active.

Center:
- Optional compact command/search field. It must not look like chat. Label it “Search vault, FIDs, cycles, evidence.”

Right:
- Posture badge: `FRONTIER`, `HYBRID`, or `LOCAL`.
- Audit pill: current verification status and latest lock-history count.
- Signing key chip: truncated Ed25519 fingerprint.
- Operator avatar or initials.

Top bar priority:
1. Fail-closed warnings can visually override everything.
2. Posture must always remain visible.
3. Audit status must always remain visible.
4. Signing key must remain visible on desktop.

### Left Navigation Rail

Desktop width approximately 220px.

Primary nav items:
1. Home
2. Discovery
3. Evidence Intake
4. Eligibility Gates
5. Module Mapper
6. Drafting
7. Budget
8. Judge
9. Red Team
10. Sign-Off
11. Audit Trail
12. Cards
13. FIDs
14. Cost
15. Settings

Each item may include a small mono count chip for pending actions.

### Main Work Surface

Elastic central canvas. This is where the active screen lives. It should be dense but legible, with strong hierarchy. Do not create empty marketing dashboards.

### Right Inspector

Width approximately 380px. Context-sensitive.

The inspector should show:
- selected source evidence
- gate explanation
- section constraints
- claim provenance
- score rationale
- model/posture event
- amendment impact
- current action dependencies

### Footer

Persistent on desktop. Include:
- machine identity
- full or truncated signing key fingerprint
- active posture
- corpus freshness
- local node status

---

## 2. System Personality

The UI should feel:
- infrastructure-grade
- sober
- institutional
- precise
- warm but not soft
- local-first
- credible enough for grant compliance
- tactile enough to feel like owned equipment

Avoid:
- consumer SaaS enthusiasm
- playful empty states
- chatbot personality
- marketing copy
- blue/purple AI gradients
- fake 3D neural imagery
- animated robot assistants
- “Welcome back!” dashboards

The operator is technically literate. Do not condescend. Use direct language.

Good copy:
- “DO NOT DRAFT — hard eligibility gate failed.”
- “Unknown is blocking because this is a hard gate.”
- “Drafting under signed eligibility override.”
- “Gate result stale. NOFO source changed 42 minutes ago.”
- “Saved just now · local draft hash updated.”

Bad copy:
- “There may be an issue.”
- “AI recommends caution.”
- “Oops, something went wrong.”
- “Let’s write your grant!”

---

## 3. Golden Quill Workflow Doctrine

Render the interface as a structured grant lifecycle, not a conversation.

The main loop:

1. Discover
2. Ingest
3. Gate
4. Decompose
5. Draft
6. Validate budget
7. Score
8. Red Team
9. Sign
10. Audit
11. Remember

The UI should make each stage visible and show whether the operator is allowed to proceed.

Golden Quill does not write grants autonomously. It prepares, drafts, flags, scores, and organizes. The operator reviews, decides, signs, and submits.

---

## 4. Mandatory Interaction Contracts

### 4.1 Autosave

Every editable text area must autosave.

Display:
- “Saved just now”
- “Saving…”
- “Offline draft preserved”
- “Save failed — retry required”
- local draft hash or version ID where appropriate

Behavior to represent visually:
- save on blur
- save every short burst of typing
- manual Save Draft button remains available for operator confidence
- recovered draft state if reopening after interruption

Do not rely on a hidden autosave with no visible status.

### 4.2 Edit Leases

Do not render chaotic multi-cursor collaboration as the main model.

Use edit leases:
- one active editor per block
- field or section border shows who holds the lease
- operator can reclaim lease
- lease expiration visible
- file upload areas use first-writer-wins
- text blocks can show conflict warnings

Collaboration is permission-scoped:
- Operator
- Delegate Editor
- Reviewer / Observer
- Signer
- Maintainer / Admin

Only the Operator can produce final submission/sign-off unless a specific policy says otherwise.

### 4.3 Revision Required / Annotation Mode

When something needs correction, do not reopen the entire packet.

Render constrained resolution mode:
- unaffected sections locked
- only required fields highlighted
- side panel explains the issue
- reason may come from Logician, Judge, Red Team, reviewer, or operator
- changed fields resubmitted
- affected scores/gates marked stale
- audit event written

Visual language:
- yellow/amber for revision-required
- rust for fail-closed
- blue should not be used as the dominant correction color; use earth palette tokens

### 4.4 Fail-Closed Gates

Hard gates block Scribe.

Rules:
- Unknown + hard gate = fail-closed.
- Stale source + hard gate = fail-closed until refreshed.
- Contradictory evidence + hard gate = fail-closed until operator resolves.
- Scribe may not draft until hard gates pass or an explicit cryptographic override is signed.

A fail-closed state must be the loudest visual state in the app:
- rust border
- pink/rust wash
- left fail bar
- large direct copy
- disabled forward action

Copy:
> DO NOT DRAFT — hard eligibility gate failed.

### 4.5 Signed Risk Override

Golden Quill is sovereign. The operator is the ultimate authority. But an override is not a dismissal.

If the operator overrides a failed gate:
- require typed rationale
- require Ed25519 signature
- mark the cycle as “Drafting under signed eligibility risk”
- mark the audit trail permanently
- keep the original gate result visible
- do not convert override into pass

Visual state:
- risk-unlocked
- rust risk-mark banner
- “Override signed” chip
- visible rationale preview
- audit event link

### 4.6 Evidence TTL / Source Decay

Any passed gate or score can become stale if underlying source evidence changes.

Render staleness triggers:
- NOFO hash changed
- FID charter updated
- applicant profile changed
- SAM/UEI source refreshed
- posture changed
- evidence TTL expired

UI behavior:
- mark affected gate as stale
- revoke Scribe access if necessary
- mark Judge panel score stale if dependent claim changed
- show “recheck required”

### 4.7 No Silent Mutation

Signed artifacts are immutable.

If a signed artifact changes:
- create amendment
- show before/after diff
- require rationale
- require signature if consequential
- invalidate dependent artifacts where necessary

If a gate-bearing fact changes:
- Logician gate becomes stale.

If a score-bearing claim changes:
- Judge panel score becomes stale.

If posture changes:
- audit event is mandatory.

---

## 5. Semantic Governance / Vault Intake Doctrine

Golden Quill should not behave like a fancy Dropbox.

When a user drops notes, PDFs, budgets, letters, scans, or voice transcripts into the Vault, the intake surface must enforce semantic discipline.

### Evidence Intake Must Fail-Closed on Entry

If an item cannot be classified:
- do not quietly index it
- mark it “Uncommitted”
- show required classification fields
- show ontology conflicts
- ask the operator to resolve before memory commit

Example states:
- Classified
- Needs operator classification
- Contradiction detected
- Duplicate suspected
- Source stale
- Sensitive data detected
- Not indexed

The machine should make it easier to govern memory, but it must not allow memory rot.

### Contradiction Handling

If two signed or source-backed facts conflict, do not average them.

Render the conflict:
- ED statement says X
- Board minutes say Y
- Website says Z
- Prior grant says W

Operator decision required:
- choose governing source for this cycle
- mark contextual exception
- sign resolution
- write audit event

### Local Schema Enforcement

Use UI language that implies local schemas can evolve per organization:
- “Node schema”
- “Local ontology”
- “Vault class”
- “Classification rule”
- “Migration required”
- “Schema conflict”

Do not imply one universal SaaS schema governs all organizations.

---

## 6. Prioritized Screen Set

Generate P0 screens first. P1 and P2 can be secondary screens or later frames.

### P0 Screens

1. Operator Home / Mission Control
2. Scout Discovery
3. Upload Guidance
4. Application Guide
5. Evidence Intake / Vault Gate
6. Logician Eligibility Gates
7. Grant Module Mapper
8. Scribe Drafting Workspace
9. Budget Allocator & Validator
10. Judge Panel / Evidence Ladder
11. Red Team Review
12. Sign-Off / Export Console
13. Audit Trail / Amendment Ledger

### P1 Screens

14. Claim Amendment Mode
15. Card Selection Matrix
16. FID Browser
17. Model Cost Dashboard
18. Posture Drawer
19. Collaboration / Roles Panel

### P2 Screens

20. Post-Award Compliance Tracker
21. Internal Reviewer Split Screen
22. Admin / Maintainer Settings
23. Schema Migration / Ontology Governance Surface

Do not generate a grantmaker CRM portal as the main product. Do not make a foundation admin dashboard the home screen. Golden Quill is applicant/operator-side first.

---

## 7. P0 Screen Requirements

### 7.1 Operator Home / Mission Control

Question answered:
> What requires my decision today?

Primary components:
- Active cycle cards
- Blocked gates
- Drafts awaiting review
- Stale evidence alerts
- Upcoming deadlines
- Audit health
- Posture state
- Model cost summary
- Recent signed events

Layout:
- top alert strip for fail-closed or stale events
- central active cycles list
- right inspector showing selected cycle details
- bottom recent lock-history timeline

Must show at least one active opportunity, one blocked gate, one saved draft, and one audit event.

### 7.2 Scout Discovery

Question answered:
> Which opportunities are worth pursuing, and why?

Primary components:
- CIC selector
- CLC selector
- FID/funder envelope selector
- one-shot search button
- daemon mode indicator
- ranked opportunity cards
- confidence ribbons
- source backing tier
- deadline urgency
- fit rationale
- evidence gaps
- “open eligibility gates” action

Opportunity card fields:
- funder
- program code
- deadline
- amount
- confidence
- readiness score
- source tier
- reason surfaced
- blocking unknowns

Do not show generic “AI results.” Show source-backed Scout output.

### 7.3 Evidence Intake / Vault Gate

Question answered:
> Can this material safely become institutional memory?

Primary components:
- file drop zone
- intake queue
- classification cards
- source type selector
- sensitivity labels
- contradiction detector
- schema conflict panel
- “Commit to Vault” button disabled until resolved

Required states:
- parsed
- needs classification
- duplicate suspected
- contradiction detected
- sensitive data detected
- ready to commit
- committed with hash

This is the UI expression of semantic governance. The machine must refuse unstructured garbage.

### 7.4 Logician Eligibility Gates

Question answered:
> Are we structurally allowed to draft?

Primary components:
- vertical gate cascade
- pass/warn/fail/stale/unknown badges
- source evidence excerpts
- remediation actions
- short-circuit cascade indicator
- untested-due-to-block states
- cryptographic override drawer
- disabled/open Scribe action

Must include:
- a fail-closed banner
- at least one passed gate
- one unknown hard gate
- one untested due to block gate
- one stale evidence warning

Do not make this look like a checklist only. It is a compliance boundary.

### 7.5 Grant Module Mapper

Question answered:
> What exactly does this RFA require, section by section?

Primary components:
- section map
- rubric weights
- page/word limits
- evidence requirements
- sensitivity classification
- model/posture recommendation
- dependency graph
- missing materials list

Each section should show:
- section name
- required length
- rubric weight
- evidence readiness
- drafting status
- gate dependency
- recommended agent/model posture

### 7.6 Scribe Drafting Workspace

Question answered:
> What draft section is being produced, under what constraints, using what evidence?

Primary components:
- left section navigator
- central serif drafting canvas
- inline conjecture tags
- suspicious term underlines
- autosave indicator
- active edit lease chip
- right inspector with register, evidence, source citations, admin-risk terms
- top chip showing funder register

Required:
- no chat input
- no “generate entire grant” button
- section-by-section drafting
- visible provenance on claims
- operator edit authority

### 7.7 Budget Allocator & Validator

Question answered:
> Does the budget satisfy the funder’s math and allowable-use constraints?

Primary components:
- spreadsheet-like grid
- category rows
- requested funds
- cash match
- in-kind match
- indirect costs
- totals
- validation warnings
- allocation sliders for 100% distribution cases
- source/quote attachment column

Required validation states:
- over budget cap
- match missing
- indirect rate conflict
- unallowable cost
- quote required
- ready for Logician validation

### 7.8 Judge Panel / Evidence Ladder

Question answered:
> How strong is this proposal against the funder’s actual rubric?

Primary components:
- predicted score
- rubric criteria
- weighted bars
- evidence-tier pills
- claim drilldowns
- stale score warning
- model identity
- cross-family rigor warning if relevant

Evidence ladder tiers:
- strongest
- acceptable
- weak
- unacceptable

Every score should be drillable into the claims and sources supporting it.

### 7.9 Red Team Review

Question answered:
> Where will this proposal get attacked, downgraded, or rejected?

Primary components:
- probe checklist
- hit/clean/uncertain verdicts
- attack vector details
- required response
- unresolved risk count
- council split banner if Judge and Red Team diverge

Probe categories:
- fake fit
- missing evidence
- unsupported impact
- overclaim
- weak partnership
- budget mismatch
- funder dialect mismatch
- AI-sounding language
- compliance risk

### 7.10 Sign-Off / Export Console

Question answered:
> Is this packet ready for the operator to sign and manually submit?

Primary components:
- final packet preview
- readiness checklist
- hard gate summary
- Judge current/stale state
- Red Team unresolved items
- export package list
- signature input
- lock-history preview
- posture attestation
- manual submission reminder

Copy:
> Golden Quill prepares the packet. The operator submits through the funder’s required portal.

No autonomous submission.

### 7.11 Audit Trail / Amendment Ledger

Question answered:
> What happened, who authorized it, and what changed?

Primary components:
- timeline of events
- lock-history rows
- signature events
- before/after diffs
- posture events
- model invocation events
- amendment records
- stale/invalidated artifacts
- filters by cycle, agent, artifact, posture, actor

Must be visibly important, not buried.

---

## 8. P1 Screen Requirements

### Claim Amendment Mode

Render a constrained correction surface:
- read-only packet context
- highlighted claims needing action
- side panel with reason
- resubmit changed fields only
- audit impact preview

### Card Selection Matrix

Render 6 CIC × 8 CLC matrix:
- identity category
- capital logic lens
- charter excerpt
- activation status
- confidence/readiness marker

Default launch identities:
- Food Systems
- Education
- Public Agency
- Arts & Culture
- Cooperative
- Regenerative Systems Supplier / Ecosystem Intermediary

Capital logic categories:
- Public Purpose & Works
- Catalytic Change
- Capacity-Building / Operating Capacity
- Research & Evidence
- Market Access
- Credit & Underwriting
- Sponsorship & Corporate Support
- Commons / Shared Assets

### FID Browser

Render funder intelligence records:
- funder/program name
- verification status
- freshness indicator
- source corpus completeness
- last used cycle
- gate taxonomy status
- rubric availability

### Model Cost Dashboard

Render cost as operational visibility:
- per-cycle cost
- per-seat/model cost
- cache hit rate
- posture-aware comparison
- cost saved by local execution
- cost risk if frontier model selected

### Posture Drawer

Render explicit posture switch:
- Frontier-Eligible
- Split-Context Hybrid
- Local-Only Sovereign

Posture change requires typed confirmation and signature. Mid-cycle posture changes should warn or block if they invalidate gates.

### Collaboration / Roles Panel

Render role-scoped permissions:
- Operator
- Delegate Editor
- Reviewer / Observer
- Signer
- Maintainer / Admin

Show who can edit, comment, sign, approve, export, and invite.

---

## 9. P2 Screen Requirements

### Post-Award Compliance Tracker

Render later-stage reporting:
- awarded grants
- reporting deadlines
- evidence requirements
- disbursement dependencies
- closeout status
- renewal readiness

### Internal Reviewer Split Screen

Render optional review mode:
- left: packet/document
- right: rubric
- COI gate
- comments
- score submission

### Schema Migration / Ontology Governance

Render local node schema management:
- current schema version
- field mappings
- unresolved ontology conflicts
- migration preview
- signed migration commit

This screen is for maintainers, not ordinary operators.

---

## 10. Component Rules

Use these components consistently.

### AuditPill

Always visible on desktop. Shows:
- verified / warning / failed
- latest event
- lock-history count
- click opens Audit Trail

### PostureBadge

Always visible. Shows:
- FRONTIER / HYBRID / LOCAL
- color-coded
- click opens Posture Drawer

### GateCard

Shows:
- gate code
- gate name
- verdict
- source
- remediation
- affected downstream screens

### FailClosedBanner

Dominant state. Must disable forward action. Copy must be blunt.

### EvidenceTierPill

Shows:
- strongest
- acceptable
- weak
- unacceptable

Used in Judge, Scribe, Red Team, and Audit.

### ClaimTraceLine

Inline claim provenance:
- claim
- source
- confidence
- sensitivity
- current/stale state

### EditLeaseChip

Shows:
- current editor
- field/section lock
- time remaining
- reclaim action for operator

### SignaturePanel

Shows:
- artifact hash
- Ed25519 fingerprint
- signature input/paste area
- validation state
- lock-history preview

### AmendmentDiff

Shows:
- old value
- new value
- actor
- rationale
- signature impact
- affected gates/scores

### VaultIntakeCard

Shows:
- file/source name
- parsed status
- classification status
- contradictions
- sensitivity
- commit readiness

---

## 11. Demo Data To Use

Generate realistic sample data. Do not use lorem ipsum.

### Organization

Name: FIT Farms LLC  
Node: `fit-farms-pgh-001`  
Operator: Josh Inklovich  
Posture: Split-Context Hybrid  
Signing key: `Ed25519 · 4a3f…b2c8`  
Active card: Food Systems × Research & Evidence  

### Opportunity 1

Funder: USDA  
Program: Value-Added Producer Grant  
Deadline: June 27, 2026  
Fit: 86%  
Status: Gate blocked  
Blocker: UEI/SAM evidence stale  

### Opportunity 2

Funder: SARE  
Program: Farmer/Rancher Grant  
Deadline: August 1, 2026  
Fit: 78%  
Status: Ready for Module Mapper  

### Opportunity 3

Funder: Local Foundation  
Program: Regenerative Community Food Systems  
Deadline: July 15, 2026  
Fit: 71%  
Status: Evidence gaps  

### Gate Examples

- E-101 Entity type: PASS
- E-104 UEI/SAM registration: UNKNOWN → FAIL-CLOSED
- E-112 Deadline eligibility: PASS
- E-118 Match requirement: UNTESTED_DUE_TO_BLOCK
- E-130 NOFO source hash: STALE

### Draft Section

Section: Project Narrative  
Register: USDA-RD — mechanism-aware  
Inline tag: `[CONJECTURE — source pending]`  
Suspicious term: “revolutionary”  
Autosave: Saved 18 seconds ago  
Edit lease: Operator holds lease  

### Judge Panel

Predicted score: 82 / 100  
Stale flag: No  
Weak area: Market demand evidence  
Evidence unacceptable: unsupported buyer relationship claim  

### Red Team Hit

Probe: Fake-fit partnership signal  
Verdict: HIT  
Reason: Proposal claims institutional buyer interest without letter, quote, or email evidence.  
Required action: remove claim or attach source.  

### Audit Event

Event: Gate failed closed  
Cycle: `cycle_2026-05-20T14:32Z`  
Artifact hash: `b61d…9e2a`  
Signature: unsigned  
Action required: resolve or override  

---

## 12. Non-Goals

Do not generate:
- chatbot interface
- message bubbles
- AI avatar
- autonomous grants.gov submission
- generic CRM home
- grantmaker payment administration as main screen
- blue/purple AI theme
- marketing landing page
- gamified progress streaks
- unverified “win probability” without evidence ladder
- hidden model routing
- hidden audit trail
- silent admin edits
- passive Dropbox-like vault

---

## 13. Stitch Prompt Template

Use this exact language when prompting Stitch for each screen:

> Generate a desktop-first Golden Quill screen using the attached DESIGN.md and this directive. Golden Quill is an operator-owned Tilth grant intelligence console, not a chatbot. Keep the posture badge, audit pill, signing key, left nav, right inspector, and footer visible. Use the earth-tone infrastructure palette, serif reading typography, and monospace IDs/hashes. Render realistic grant workflow data. The screen must answer the operator question stated in the prompt. Do not add chat UI, generic SaaS blue/purple styling, marketing content, autonomous submission, or hidden audit behavior.

Then append the specific screen prompt.

---

## 14. First Generation Batch

Generate these first, in this order:

1. Operator Home / Mission Control
2. Evidence Intake / Vault Gate
3. Logician Eligibility Gates
4. Grant Module Mapper
5. Scribe Drafting Workspace
6. Judge Panel / Evidence Ladder
7. Red Team Review
8. Sign-Off / Export Console
9. Audit Trail / Amendment Ledger
10. Scout Discovery

Reason for this order:
- Home establishes the shell.
- Intake establishes semantic governance.
- Gates establish fail-closed doctrine.
- Mapper establishes the grant-specific workflow.
- Scribe/Judge/Red Team/Sign-Off establish the application cycle.
- Audit proves credibility.
- Scout plugs discovery into the same system.

Discovery is strategically important, but the governance and drafting loop must visually exist first so Golden Quill does not become “grant search with AI prose.”

---

## 15. Final Instruction To Stitch

Render Golden Quill as a serious operator console for funding work under constraint.

The operator should look at the interface and immediately understand:
- what is being pursued
- what is blocked
- what evidence exists
- what changed
- what is signed
- what is stale
- what data posture is active
- what the council produced
- what the human must decide next

If a generated screen looks like ordinary SaaS, it failed.
If it looks like a chatbot, it failed.
If it hides audit or posture, it failed.
If it lets Scribe draft around unresolved eligibility, it failed.
If it treats the Vault like Dropbox, it failed.

The target is not friendliness. The target is trust.

---

## 16. Final Hardening Addendum: Quarantine, Epoch, and Portal Staging

### Quarantine must be visible

If a file, note, scan, or transcript cannot be classified or conflicts with node ontology, render it as quarantined. Do not leave it as a harmless pending item and do not make it available to Scout, Scribe, Judge, or Red Team.

Required copy:
> QUARANTINED — ontology unresolved. This file is stored but unavailable to the council until mapped.

### Epoch / Sync must be visible

The top bar must include an `EpochSyncIndicator` or equivalent sync chip. The operator must know whether the node is synced, backup-pending, local-only, offline-local, verifying, remote-unavailable, or in sync conflict.

Examples:
- `SYNCED · evt_0008`
- `BACKUP PENDING — 3 events not synced`
- `LOCAL-MODE: OFFLINE`
- `SYNC CONFLICT — export disabled`

### Portal staging is allowed; autonomous submission is not

Golden Quill may show a portal-staging preparation surface:
- portal field checklist
- upload checklist
- packet-to-portal mapping
- required document readiness
- manual submission reminder

Do not render an autonomous `Submit to Grants.gov` button. The operator submits.
