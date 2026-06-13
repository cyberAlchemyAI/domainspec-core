# BUILD-SPEC — After-Acceleration Roadmap

- Craft node: `after-acceleration-roadmap`
- Parent space: `node-on-desk-readiness`
- Source contract: `docs/golden-quill-task-role-breakdown-handoff.md` (Sheet 2, "WHAT COMES NEXT — AFTER STARTUP CAPITAL / ACCELERATION", lines 84–97)
- Refine evidence: `docs/strategy/development/after-acceleration-roadmap/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md`
- Ledger: `docs/strategy/development/after-acceleration-roadmap/.craft/ledger.yml`
- Stage / gate: `start` / `flag` — future-stage roadmap (DESC-AAR-001), **not a v0.1 build gate**
- Status: planning / spec only. Authored 2026-06-13.

> **Scope guard (Law 2 — No Boundary Drift).** This node tracks what comes *after* startup capital. It does **not** define or gate any v0.1 first-node readiness work — that belongs to `node-on-desk-readiness` and its per-workstream sibling nodes (hardware-golden-image, tilth-runtime-build, quality-security-proof, capital-logic-library, sales-contracting-legal, white-glove-delivery-node-care, company-operations-finance). The only coupling is **read-only**: this roadmap *consumes* metrics that v0.1 instrumentation already plans to emit. It writes nothing back into v0.1 scope.
>
> **Law 3 (Org Isolation).** No `orgs/` content is referenced or required by this spec. All triggers are fleet-level operational metrics, not per-org applicant data.
>
> **Authoring boundary.** This spec authors the **structure** of the post-acceleration stage gates. All numeric **threshold values** are founder judgment and are marked `[OPERATOR-INPUT]`. Nothing here fabricates a threshold.

---

## 1. Define

### 1.1 What this node is

The post-acceleration roadmap is the ordered set of business motions Golden Quill (FIT Farms) takes once startup capital / accelerator funding lands and the first node is live on a customer desk. Sheet 2 of the source workbook enumerates **eight themes** but assigns them **no order, no threshold, and no trigger** (RESEARCH-RESULT finding 2). The substance of this node is to convert that flat list into a **stage-gate model**: each theme stays dormant until a named piece of evidence crosses an operator-set threshold.

### 1.2 The eight themes (verbatim from source)

| # | Theme | Source role assignment (Sheet 2) |
| --- | --- | --- |
| T1 | **Repeatability** | Customer Success lead + Field Tech (built from Founder's first installs) |
| T2 | **Sales beyond founder network** | Founder → dedicated Sales/Partnerships role |
| T3 | **Product hardening** | AI + Backend Engineers; full-time technical hire absorbs knowledge |
| T4 | **Capital Logic Library** (expansion) | Founder (editorial) + AI Engineer + Domain Experts |
| T5 | **Service line validation** | Founder (scoping); Admin Lead (conditional hire) |
| T6 | **New markets** | Founder + Backend Engineer; Security Reviewer |
| T7 | **Next financing** | Founder + QA / Measurement |
| T8 | **Team build-out** | Founder (hiring); whole team (onboarding) |

### 1.3 The trigger metrics (where the evidence comes from)

The sequencing evidence is a **downstream read of v0.1 instrumentation already planned** (RESEARCH-RESULT finding 6), not new research. The feeding sources in the source workbook (Sheet 1):

| Metric ID | Metric | v0.1 source (Sheet 1) |
| --- | --- | --- |
| M-NODES | Deployed-node count | Derived from per-node deployment record / install ledger (lines 70–71); also the explicit basis for Team build-out (line 97) |
| M-SUPPORT | Support hours per node | "Instrumentation: support hrs/node…" (line 61); Day 60 use review "support load" (line 76) |
| M-RENEWAL | Renewal-intent / renewal data | "…renewal-intent capture" (line 61); Day 60 "renewal signal" (line 76); Next-financing evidence set (line 96) |
| M-UNIT-ECON | Measured unit economics | Next-financing evidence set (line 96); deposit/invoicing/cost tracking (line 69) |
| M-INSTALL-LABOR | Install labor (hours-to-install, non-founder-run) | Repeatability done-condition (line 90); imaging/white-glove rows (lines 38, 70–76) |
| M-CHANNEL | Channel plan / qualified pipeline | Next-financing evidence set (line 96); sales materials + pipeline tracker (line 66) |
| M-PILOT-RISK | Service-pilot labor & reputational-risk evidence | Service-line pilot dimensions (line 94) |
| M-CAPITAL | Capital milestone (accelerator close / financing round close) | Capital track (founder role, line 107) |

### 1.4 Definition acceptance criteria

- AC-D1: All eight themes named with their source role assignment (§1.2). ✔
- AC-D2: Each trigger metric traced to a v0.1 instrumentation source line (§1.3). ✔
- AC-D3: No theme silently introduces a v0.1 build obligation (Law 2). ✔
- AC-D4: No threshold value fabricated; all deferred to `DEC-AAR-STAGE-GATES` (§4). ✔

---

## 2. Design — Stage-Gate Model

### 2.1 Design principle

Each theme activates only when its **gate condition** evaluates true. A gate condition is `metric(s) ≥ threshold` where the metric is a v0.1 instrumentation read and the threshold is `[OPERATOR-INPUT]`. Themes may share a common precondition (`M-CAPITAL` — capital has landed) because the entire sheet is post-capital by definition; that precondition is the **roadmap entry gate**, not a per-theme gate.

Gate states are deterministic and read-only:

- `DORMANT` — gate condition false; no work authorized.
- `ARMED` — primary metric crossed threshold; secondary conditions pending; founder review due.
- `ACTIVE` — gate condition fully true; theme work authorized.

A gate never auto-advances theme work; it authorizes the founder to open it. This keeps `DEC-AAR-STAGE-GATES` (founder-owned) as the live control even after thresholds are set.

### 2.2 The stage-gate table (STRUCTURE — values are operator-input)

This is the canonical deliverable for **GAP-AAR-SEQUENCING**. Columns are fixed; the `Threshold` column is the only operator-input surface.

| Gate ID | Theme | Primary trigger metric | Secondary / gating evidence | Threshold (operator-input) | Gate question | Done / advance condition |
| --- | --- | --- | --- | --- | --- | --- |
| G-T1 | T1 Repeatability | M-INSTALL-LABOR (non-founder install proven) | M-NODES (enough first installs to harden a playbook) | `[OPERATOR-INPUT: # founder installs before playbook freeze]` | Has a non-founder run an install end-to-end at acceptable labor cost? | Non-founder completes one end-to-end install from the playbook (see GAP-AAR-REPEATABILITY, §4.2) |
| G-T2 | T2 Sales beyond founder network | M-CHANNEL (qualified pipeline outside founder network) | M-NODES, M-RENEWAL (reference-able live customers) | `[OPERATOR-INPUT: # reference customers + pipeline size]` | Is there proof the offer sells without the founder's personal network? | First non-network deal closed via a partner channel or campaign |
| G-T3 | T3 Product hardening | M-SUPPORT (support load signals hardening priorities) | M-NODES (fleet large enough to need fleet-scale ops) | `[OPERATOR-INPUT: support hrs/node ceiling + fleet size]` | Is fleet-scale operation (multi-seat, fleet updates, Sovereign GA) blocking growth? | Sovereign-mode build audited; sanitization GA; fleet update/monitoring live |
| G-T4 | T4 Capital Logic Library expansion | M-NODES (opt-in outcome data volume) | M-RENEWAL (engaged customers willing to opt in) | `[OPERATOR-INPUT: # opt-in nodes for pattern feedback]` | Is there enough opt-in outcome data to refine and extend cards offline? | Outcome-data opt-in pipeline live; ≥1 new/extended card validated by expert bench |
| G-T5 | T5 Service line validation | M-PILOT-RISK (controlled-pilot labor & reputational risk measured) | M-NODES (customer base to source pilots) | `[OPERATOR-INPUT: pilot count + risk go/no-go bar]` | Do grant-admin pilots prove acceptable labor & reputational risk? | Pilot go/no-go passes (see GAP-AAR-SERVICE-PILOTS, §4.3); admin-lead hire authorized only on PASS |
| G-T6 | T6 New markets | M-NODES + M-UNIT-ECON (core market proven first) | Security Reviewer assurance for Sovereign/Tribal/consortium governance | `[OPERATOR-INPUT: core-market maturity bar]` | Is the core market stable enough to extend into Tribal / institutional / consortium? | Governance + assurance review complete *before* any new-market sale (source line 95) |
| G-T7 | T7 Next financing | M-UNIT-ECON + M-RENEWAL + M-SUPPORT + M-CHANNEL (data-room set) | M-NODES (deployment proof) | `[OPERATOR-INPUT: unit-econ + renewal data-room bar]` | Is the data room complete with measured unit economics, support-load, renewal, and channel evidence? | Data room assembled from the five named evidence classes (source line 96) |
| G-T8 | T8 Team build-out | M-NODES (explicit: "sequenced against deployed-node count", line 97) | M-SUPPORT (support load justifies CS/field hires) | `[OPERATOR-INPUT: node count per hire tranche]` | Does deployed-node count + support load justify the next hire tranche? | Each hire (technical / CS / field / sales) opens at its own node-count tranche |

**Notes on the table structure:**

- **Two themes arrive with native triggers** (RESEARCH-RESULT finding 3): T8 is explicitly "sequenced against deployed-node count" (M-NODES) and T5 hires the admin lead "only if pilots prove it" (M-PILOT-RISK go/no-go). These two rows encode source-given logic; the other six rows' trigger bindings are *authored here* and their thresholds are net-new operator decisions.
- **Roadmap entry gate (shared precondition):** `M-CAPITAL ≥ [OPERATOR-INPUT: capital-landed marker]`. Until this is true, every gate is `DORMANT` regardless of other metrics — the whole sheet is post-capital.
- **Ordering is emergent, not hardcoded.** The table does not impose a strict 1→8 sequence; gates fire when their evidence arrives. Natural dependency: T1 (repeatability) and T8 (team) tend to arm earliest because they read M-NODES/M-INSTALL-LABOR directly; T7 (financing) tends to arm last because its data-room set aggregates the most metrics. The founder may still open any gate manually once ARMED.

### 2.3 Metric → gate feed matrix

Confirms every gate is fed by an existing v0.1 instrumentation read (no new measurement infra required at this node).

| Metric | Feeds gates |
| --- | --- |
| M-NODES | G-T1, G-T2, G-T3, G-T4, G-T5, G-T6, G-T7, G-T8 |
| M-SUPPORT | G-T3, G-T7, G-T8 |
| M-RENEWAL | G-T2, G-T4, G-T7 |
| M-UNIT-ECON | G-T6, G-T7 |
| M-INSTALL-LABOR | G-T1 |
| M-CHANNEL | G-T2, G-T7 |
| M-PILOT-RISK | G-T5 |
| M-CAPITAL | Roadmap entry gate (all) |

### 2.4 Design acceptance criteria

- AC-G1: Every one of the eight themes has exactly one gate row with a primary trigger metric (§2.2). ✔
- AC-G2: Every trigger metric in the table appears in §2.3 traced to a v0.1 source (no orphan metric). ✔
- AC-G3: Threshold column is the *only* operator-input surface; no numeric value is asserted by this spec. ✔
- AC-G4: The two source-native triggers (T5, T8) are preserved, not overwritten. ✔
- AC-G5: Gate states are deterministic and never auto-advance theme work (founder retains control). ✔
- AC-G6: No gate condition reads or writes `orgs/` data (Law 3) or imposes a v0.1 build task (Law 2). ✔

---

## 3. Plan — Sequenced Work Items

Planning only. No execution authorized here. Each item names owner, input, output, and done-condition (Autonomy Rule 3 — Be Explicit).

| Plan ID | Work item | Owner | Input | Output | Done-condition | Blocks on |
| --- | --- | --- | --- | --- | --- | --- |
| P-1 | Set threshold values into the §2.2 table | Josh | §2.2 table; v0.1 instrumentation baselines once they exist | Filled `Threshold` column | All eight gate thresholds + entry-gate marker assigned | `DEC-AAR-STAGE-GATES` resolved (§4.1) |
| P-2 | Wire gate evaluation to instrumentation reads | QA/Measurement (Victor) | v0.1 instrumentation outputs (M-NODES, M-SUPPORT, M-RENEWAL, …) | Read-only gate dashboard / status surface | Each gate computes DORMANT/ARMED/ACTIVE from live metrics | v0.1 instrumentation landing (downstream coupling, RESEARCH-RESULT finding 6) |
| P-3 | Author non-founder install playbook + curriculum | Customer Success lead + Field Tech | White-glove + imaging rows (source lines 38, 70–76) | Playbook + training curriculum | Non-founder runs an install end-to-end (GAP-AAR-REPEATABILITY done-condition) | Needs a real pilot (§4.2) |
| P-4 | Scope controlled grant-admin service pilot | Josh (scoping) | Service-line dimensions (source line 94) | Pilot scope + go/no-go design with labor & reputational-risk as measured variables | Go/no-go criteria defined; pilot bounded | Controlled-scope + risk evidence (§4.3) |
| P-5 | Define next-financing data-room assembly checklist | Josh + QA/Measurement | Five evidence classes (source line 96) | Data-room manifest mapping each class to its instrumentation source | Data-room checklist complete and traceable to G-T7 | G-T7 ARMED |

### 3.1 Plan acceptance criteria

- AC-P1: Every plan item has owner / input / output / done-condition (Rule 3). ✔
- AC-P2: Every gap (§4) maps to at least one plan item (GAP-AAR-SEQUENCING→P-1/P-2; GAP-AAR-REPEATABILITY→P-3; GAP-AAR-SERVICE-PILOTS→P-4). ✔
- AC-P3: No plan item executes v0.1 build work; P-2 and P-3 *consume* v0.1 outputs but author no v0.1 obligation. ✔

---

## 4. Operator-Input & Needs-Pilot Callouts (NOT fabricated)

### 4.1 DEC-AAR-STAGE-GATES `[owner: Josh]` — threshold values are founder judgment

The §2.2 table structure is authored; the numeric thresholds are not, and cannot be researched into existence (RESEARCH-RESULT residue). Josh sets: the capital-landed entry marker, and one threshold per gate (G-T1…G-T8). Until set, the ledger decision stays `PENDING` and every gate reads `DORMANT`. This is the live control surface — structure here, judgment from Josh.

### 4.2 GAP-AAR-REPEATABILITY `[owner: Josh / customer-success-field-tech]` — needs a real pilot

The non-founder install playbook (P-3) is buildable from existing white-glove/imaging rows, but its **proof requires a real pilot**: done-condition is *a non-founder runs an install end-to-end*. The spec authors the work item and its acceptance test; it does not assert the proof has occurred. No simulated or self-asserted pass counts.

### 4.3 GAP-AAR-SERVICE-PILOTS `[owner: Josh]` — needs controlled scope + risk evidence

Grant-administration service-line pilots (P-4) must run at **controlled scope** with **labor and reputational risk** as measured variables (source line 94) before any admin-lead hire. The admin-lead hire (T5 role) is authorized **only on a PASS go/no-go** — this is a source-native conditional trigger, preserved as G-T5's advance condition. The spec designs the pilot scope and go/no-go structure; it does not pre-judge the outcome or authorize the hire.

---

## 5. Per-Gap Verdict

| Gap | Treatment | Verdict | Where resolved |
| --- | --- | --- | --- |
| `GAP-AAR-SEQUENCING` | decide (Refine-solvable structure) | **AUTHORED** — stage-gate table structure + metric-to-gate bindings authored (§2.2, §2.3); thresholds deferred to operator | §2.2, §2.3, P-1, P-2 |
| `DEC-AAR-STAGE-GATES` | decision | **DEFERRED — operator-input** (threshold values are founder judgment) | §4.1 |
| `GAP-AAR-REPEATABILITY` | validate | **PLANNED — needs real pilot** (non-founder end-to-end install) | §4.2, P-3 |
| `GAP-AAR-SERVICE-PILOTS` | pilot | **PLANNED — needs controlled-scope pilot + risk evidence before admin-lead hire** | §4.3, P-4 |

---

## 6. Residue & Coupling

- This node's readiness is **coupled to v0.1 instrumentation landing** (RESEARCH-RESULT finding 6 / residue): gate evaluation (P-2) cannot run until M-NODES / M-SUPPORT / M-RENEWAL / M-UNIT-ECON / M-CHANNEL emit live data. Structure can be authored now; live gate computation waits on v0.1.
- Bounded external-research requests (EXT-AAR-01 sequencing-threshold norms, EXT-AAR-02 install-labor benchmarks, EXT-AAR-03 service-line risk norms) remain **deferred and approval-gated** (RESEARCH-RESULT r04). They are not consumed by this spec. If Josh later approves a bounded external pass, the thresholds in §2.2 and the risk bars in §4.3 are the surfaces they would inform — they do not change the table *structure*.
- Owner boundary honored: this spec mutates no canonical/lifecycle artifact and does not edit `.craft/ledger.yml`.
