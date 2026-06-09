# Reconciliation — ontologize ontology model ↔ dispersed existing ontology work

Resolves the three open reconciliation items in [HANDOFF.md](HANDOFF.md): (1) reconcile the 4-branch
model with prior art; (2) decide whether the existing CyberAlchemy entries feed the pilots; (3)
cross-check the Lane B 3-EXTEND / 2-NET-NEW classification against the actually-installed sigils.

Tags: **[SB]** source-backed (path) · **[H]** hypothesis. Candidate-only — no canonical promotion, no
pricing/contracts/named clients. All `arcanum/*`, `cyberAlchemy/*`, GoldenQuill, and the proof are
read-only evidence; only this file was written. Owner decisions are recommendations, not verdicts.

## 1. Branch model reconciliation

### Mapping table — ontologize branch ↔ prior art

| ontologize branch | (a) `ontology-vault-branching` proof | (b) `cyberAlchemy/04-operational-ontology` (+ ONTOLOGY-ARCHITECTURE) | Match? |
| --- | --- | --- | --- |
| **B1 — meaning** (a.k.a. business/domain/intent) | "Business ontology — intent, rules, outcomes, premises, value claims" [SB `arcanum/research/proofs/ontology-vault-branching/proof-report.md`] | "Business Ontology — domain intent, actors, policies, value, business rules, premises" [SB `arcanum/development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md:73,136`] | **Same concept, different label** (see naming decision) |
| **B2 — system** | "System ontology — implementation artifacts, tests, telemetry, constraints" [SB proof-report.md] | "System Ontology — implementation facts, services, APIs, data flows, tests, infrastructure, runtime" [SB ONTOLOGY-ARCHITECTURE.md:74,137] | **Clean match** |
| **B3 — operational** (run context: run id, denominators, lifecycle) | **Absent.** Proof models only business/system/bridge; no run-context branch [SB `ontology-vault-branching/README.md:3` "three coordinated layers"; proof-report.md:5 names only business/system/bridge] | **Namesake but divergent.** "Operational Ontology" here = reusable knowledge about *agent operation* (routes, sigils, prompts, failure modes), NOT a per-run denominator context [SB `cyberAlchemy/agentic-system/slices/04-operational-ontology/concepts.md:48-61`] | **DIVERGENCE — see note** |
| **B4 — bridge** | "Bridge ontology — `realized_by`, `tested_by`, `observed_by`, `constrained_by`; drift as preserved gap" [SB proof-report.md:31-33] | "Bridge Ontology — traceability, drift, evidence links, validation across business/system/operation" [SB ONTOLOGY-ARCHITECTURE.md:75,138] | **Clean match** (edge set matches DAG-AND-METRICS §3) |

### The B1 naming question: "meaning" vs "business"

The prior art is consistent and uses **"business"** everywhere it is canonical:
- `arcanum/BUSINESS-ONTOLOGY.md` — the title and the whole document say **Business Ontology** [SB].
- The `ontology-vault` sigil's only branch token is `business` (`map --branch business`,
  `--branches business,system`, `validate --bridge business-system`) [SB `arcanum/arcana/ontology-vault/SKILL.md:4,35-40`].
- The proof's pass-criteria and next-use pattern say "business map", `--branches business,system` [SB proof-report.md:18-23,46].
- ONTOLOGY-ARCHITECTURE.md's stable-branch table lists "Business" [SB:55,73,136].

"meaning" is ontologize's own gloss — ONTOLOGY-BRANCHES.md already records it as a parenthetical alias:
"B1 — meaning (a.k.a. business / domain / intent)" [SB `projects/ontologize/ONTOLOGY-BRANCHES.md:23`].
No prior-art file names the branch "meaning". The GoldenQuill synthesis (cited as the source for the
4-branch framing) uses "meaning/system/operational/bridge" as a *research* vocabulary [SB ONTOLOGY-BRANCHES.md:8-9], which is where the term entered ontologize.

**DECISION (owner):** What is the canonical name of B1 — "meaning" or "business"? —
**Recommendation: canonical = "business" (carrying "meaning/domain/intent" as documented aliases),
because every promotable Arcanum surface — the runtime token in `ontology-vault`, `BUSINESS-ONTOLOGY.md`,
and the stable-branch table — already calls it "business," so aligning avoids a label-vs-runtime mismatch
the moment a client touches the sigil.** Keep "meaning" as the *client-facing intuition* gloss only.
Do not unilaterally rewrite ONTOLOGY-BRANCHES.md; this is an owner call.

### Genuine model divergence — B3

This is the one real divergence and it must not be smoothed:

- **ontologize B3 = a per-run operational context** (run id, org scope, deadline/posture, lifecycle
  state, and crucially "run boundary = metric denominators") [SB ONTOLOGY-BRANCHES.md:25,51].
- **cyberAlchemy/arcanum "Operational Ontology" = an ontology of *agent operation*** — routes, context
  solutions, failure modes, prompt contracts, maintenance triggers ("the system governing the
  governor") [SB `cyberAlchemy/agentic-system/slices/04-operational-ontology/concepts.md:30-44,76-88`].

These share a name but model different things. Two further divergences in *status*:
- Prior art's **stable** model is **three branches** (Business/System/Bridge). Operational is explicitly
  a **candidate extension, "not a permanent fourth branch until user or ontology-harness review accepts
  it"** [SB ONTOLOGY-ARCHITECTURE.md:55,79,139]. ontologize promotes operational to a first-class
  fourth branch [SB ONTOLOGY-BRANCHES.md:25,30].
- The proof proves only the **three-branch** business/system/bridge claim; it does not exercise any
  operational branch at all [SB proof-report.md].

**DECISION (owner) — RESOLVED 2026-06-08 (Victor):** Should ontologize's B3 keep the name "operational"
given the namesake clash, and should it stay first-class? — **Resolved: (i) B3 stays first-class, and all
four branches are first-class** (GoldenQuill's denominator/`stage ≠ outcome` rules are genuinely a
run-context branch boundary [SB ONTOLOGY-BRANCHES.md:28-30]); **(ii) B3 is renamed "run-context"**
everywhere in the project, to avoid colliding with arcanum's already-documented "Operational Ontology =
agent-operation" branch — **because two different branches sharing one word would cause silent
meaning-collapse exactly where the model's value is keeping meanings apart.** This **resolves R13 and
R14**. The rename was applied across the living design docs (ONTOLOGY-BRANCHES, DESIGN, DAG-AND-METRICS,
assessment); historical refinement-run receipts and session logs keep the original "operational" wording
as dated record. The card-config term "operational primitive" was renamed "card primitive" to remove the
last overload of the word.

## 2. Existing entries decision — feed the pilots, or stay separate?

### Evidence

- `cyberAlchemy/ontology/entries/` contains **exactly one entry**:
  `knowledge-governance-authority-ladder.md`, branch **`knowledge-governance`**, status candidate [SB
  `cyberAlchemy/ontology/README.md:30`; `cyberAlchemy/ontology/entries/` listing].
- Its subject is **how knowledge moves from raw evidence to promoted ontology** — i.e., the governance
  meta-layer, an agent/CyberAlchemy-internal concern [SB README.md:30].
- The other eight items under `cyberAlchemy/ontology/` are **source digests** (arcanum business-ontology,
  ontology-vault harness, necronomicon substrate, CyberAlchemy method, DomainSpec intent, drift/tuning,
  AEO, observed-invocation) — explicitly "evidence, not final authority" [SB
  `cyberAlchemy/ontology/source-ledger.md:33-40,54-56`].
- **Vertical match check:** none of these touch the pilot verticals. The pilots are **cap factory**
  (yield/MES events) and **logistics** (routing/TMS events) [SB ONTOLOGY-BRANCHES.md:56-68]. The
  existing material is about Arcanum/agentic-system meta-governance, with **zero** manufacturing or
  logistics domain content [SB ledger + entry inspection].

### Reuse vs cost

| Consume them into the pilots | Keep them separate |
| --- | --- |
| **Buys:** the authority-ladder / promotion-state pattern is genuinely reusable as a *method template* for how a pilot's B1 entries get promoted [SB authority-ladder entry] | **Avoids:** importing a `knowledge-governance` branch + agent-operation digests that are irrelevant to a factory/logistics ontology (irrelevant-vertical contamination) |
| | **Avoids:** re-validation burden — these are candidate digests, "not final authority"; inheriting them as pilot content would drag a re-review obligation into the pilot [SB ledger:54-56] |
| | **Avoids:** the namesake B3 trap — adopting CyberAlchemy's "Operational Ontology" wholesale would re-import the agent-operation meaning of "operational" into a product where B3 means run-context (§1) |

**DECISION (owner):** Should `cyberAlchemy/ontology/entries` feed the cap-factory + logistics pilots, or
stay separate? — **Recommendation: keep them SEPARATE as pilot *content*; reuse only the
authority-ladder as a *governance-method pattern*. Because the single existing entry and all eight
digests are Arcanum/agentic-system meta-governance with no manufacturing or logistics domain overlap,
consuming them as pilot ontology would add re-validation burden and irrelevant-vertical noise while
buying nothing the pilots need — whereas the promotion-ladder pattern is worth lifting as a reusable
template, not as inherited entries.** The pilots populate fresh per-vertical B1/B2/B3 entries from the
assessment (WORK-PACK T1), not from this pack. [H on "worth lifting" — promotion-ladder reuse is a
method judgment; the vertical-mismatch evidence is [SB].]

## 3. Lane B bridges cross-check — does the 3-EXTEND / 2-NET-NEW split hold?

LANE-B-DESIGN.md claims: **3 EXTEND** (Bridge 2 dispatch, Bridge 3 lint, Bridge 5 cadence) + **2 NET-NEW**
(Bridge 1 signed register, Bridge 4 metric-drift) [SB LANE-B-DESIGN.md:13-15,40-79].

### Installed-sigil verification

| Bridge | Class claimed | Sigils it reuses | Installed? | Verdict |
| --- | --- | --- | --- | --- |
| **2 — event→card dispatch** | EXTEND | `inventory`, `context-builder`, `observed-invocation-loop` | all present in `.claude/skills/` + `arcanum/spells/` [SB] | **CONFIRM EXTEND** — substrate exists; the gap (event-type→card index) is a config/build add-on, not a missing engine |
| **3 — 11-rule lint** | EXTEND | `inventory` (lint) + custom `promotion-record` entry type | `inventory` installed [SB] | **CONFIRM EXTEND** — extension is a custom entry type + rule assertions on `inventory lint`; semantic rules remain per-vertical (acknowledged gap) |
| **5 — reflection cadence** | EXTEND | `workflow-reflect`, `ontology-vault distill-sessions`, `decision-gate` + external scheduler | `workflow-reflect`, `ontology-vault`, `decision-gate` all installed [SB]; **scheduler not a sigil** (handled by `schedule`/cron) | **CONFIRM EXTEND, with caveat** — the three governance sigils are present; the only missing piece is a scheduler, which is correctly flagged as a non-sigil lane-design choice [SB LANE-B-DESIGN.md:79] |
| **1 — signed classification register** | NET-NEW | (none — no native signed field→authority register) | n/a | **CONFIRM NET-NEW** — no installed sigil signs/gates a field→authority register; `inventory` stores, `ontology-vault` maps, neither signs [SB LANE-B-DESIGN.md:42] |
| **4 — metric-drift proof-harness** | NET-NEW | (none — observability tracks invocations, not metric time-series) | n/a | **CONFIRM NET-NEW** — `observability-setup`/`observed-invocation-loop` are installed but track sigil runs, not numerator/denominator time-series; `workflow-reflect` groups signals, not metrics [SB LANE-B-DESIGN.md:65-67] |

Installed-skill listing confirms `ontology-vault`, `ontology-harness`, `inventory`, `context-builder`,
`workflow-reflect`, `decision-gate`, `observability-setup`, `observed-invocation-loop` are all present
under `.claude/skills/` and `arcanum/`; `arcanum/arcana/ontology-vault/` ships SKILL.md + templates [SB].

**Verdict: the 3-EXTEND / 2-NET-NEW classification HOLDS.** No bridge changes class. The only correction
is a clarification already present in the design: Bridge 5's "scheduler" dependency is not a sigil and
must be satisfied by `schedule`/cron, so Bridge 5 is EXTEND-of-sigils-plus-external-scheduler.

### Build sequencing (gated — not now)

Sequencing per LANE-B-DESIGN.md build order [SB:84]:

```text
Bridge 2 (dispatch) ─▶ Bridge 3 (lint) ─▶ [Bridge 1 signed register — advisory in pilot-1]
                    ─▶ Bridge 5 (cadence) ─▶ Bridge 4 (metric drift)
```

**Builds are gated on a greenlit Lane-B/Hybrid pilot — NOT now.** Building or installing any bridge is a
separate `sigil-development` route, not this reconciliation [SB LANE-B-DESIGN.md:8-9,103]. The honest
client offer stands: reuse layers + 3 EXTEND bridges via configuration; 2 NET-NEW builds (signed
register, metric-drift harness) are explicitly scoped/priced separately [SB LANE-B-DESIGN.md:92-96].

## Residue

New items discovered here (not already in
[residue/open-residue.md](residue/open-residue.md)):

- **R12 — B1 canonical name unresolved.** "meaning" (ontologize) vs "business" (all prior art). Owner:
  product/ontology owner. Next object: decision-gate on the §1 naming recommendation. [SB clash]
- ~~**R13 — B3 namesake collision with arcanum "Operational Ontology."**~~ **RESOLVED 2026-06-08:** B3
  renamed **run-context** across the project (§1). The divergence from arcanum's agent-operation
  "Operational Ontology" is now explicit, not silent.
- ~~**R14 — Branch-count mismatch (3 stable vs 4 first-class).**~~ **RESOLVED 2026-06-08:** owner decided
  **all four branches are first-class** in ontologize (run-context denominators are load-bearing for
  honest BI). This intentionally diverges from the Arcanum/CyberAlchemy prior art, which treats
  operational as a candidate extension; the divergence is documented in §1 and ONTOLOGY-BRANCHES.md.
- **R15 — Authority-ladder reuse-as-template undecided.** Whether to lift
  `knowledge-governance-authority-ladder.md` as the pilots' promotion-method template (vs designing
  fresh). Owner: design. Next object: assessment / WORK-PACK T1. [H]

Carried (already tracked): existing-entries vertical mismatch underpins, but does not duplicate,
open-residue R1 (cross-vertical generalization). No edits made to open-residue.md.
