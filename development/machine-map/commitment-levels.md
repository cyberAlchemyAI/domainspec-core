# Commitment Levels — A Third Cut Over the Machine

A commitment-level lens over the same machine the [machine-map findings](findings.md) describe. It
reads the machine not by VSM system (findings.md) and not by the two axes of the
[Concept Map](../../projects/framework-unification/CONCEPT-MAP.md), but by **what each artifact
commits you to** — and therefore how fast, and with how much ceremony, it is allowed to change.
Claim ≤ proof throughout: every load-bearing claim cites a file or a named prior mechanism;
everything *designed* rather than *built* is flagged as such.

---

## 0. Status banner — read this first

This is a **PROPOSED conceptual LENS, not a description** — a *third cut* alongside CONCEPT-MAP's
two axes (pipeline × three mechanisms), which it **does not replace** and whose OQ-A-locked stage
order it does **not** re-sequence. Where that frame slices the engine by *what is produced* and
*what is guaranteed*, this one slices by *what is committed*.

**Nothing here is built beyond what is cited as built.** The three-level model, the canonical
families, the inverse authority↔velocity relation, and the two-faces framing are a designed lens.
The only "built" pieces are ones prior docs already mark built — the frontmatter schema, the signal
ledger, the manual gates (findings.md / CONCEPT-MAP) — plus the premise/axiom/constitution node
types, which are built as an *installed capability* per the **ontology-vault SKILL** (§4), not per
those two docs. Roadmap, not description: the machine is mostly unbuilt (findings.md §5).

This is **not "domainspec-v2" and not an Ontology-A/B merge** — that merge was ruled unsound
(`research/2026-06-24-ontology-operationalization/findings.md` §1, row (g)). The full overclaim
guard lives once, in §9.

---

## 1. The three levels

Three bands, separated by what the terminal artifact of each **commits you to**.

| Level | Commits you to | Terminal artifact | Change-velocity & ceremony | Residue | Governed by |
|---|---|---|---|---|---|
| **UNDERSTANDING** (research) | *nothing* until promoted — a provisional finding that **authorizes an action** but obliges no downstream build | **DISCOVERY** — a triangulated finding; provisional, provenance-bearing, promotable, **read-only after save** | fast to produce; **promotion out of it is gated** (a discovery earns the right to become canon) | the discovery node + its provenance chain (append-only; read-only after save) | nothing above it — but **write-incapable toward authority**: no write-edge to `promotion-status` (the write-authority proviso, §6) |
| **CANONICAL** | a **durable commitment that governs everything downstream** | belief-canon · rule-canon · spec (see §4) | **slow, high ceremony** — driven by authority/blast-radius; for *obliging* canon, also by discharge-cost (§5) | the artifact, **plus — for obliging canon — its discharge/gate**; an obliging artifact with *no* check = `governance-gap` (§5) | the two System-5 policies (object-level "docs before code"; the two-S5 question is **OPEN**, §4) |
| **EXECUTION / ENFORCEMENT** | **the running reality, now** — the change *is* an event | a **diff + new code state** (the event is ephemeral; its durable trace is the signal ledger) | **high-frequency, low-ceremony** | the diff + new code state; the event itself is not archived, its signal is | **GOVERNED BY** the two OBLIGING families (rule-canon + spec), via discharge (§6); belief-canon bears on execution only indirectly, through the spec/rule it consistency-constrains (§5) |

> **Band commitment ≠ node commitment.** "Commits you to" is a *band-level* property — the durability
> and ceremony a whole band imposes. It is distinct from a node's *convicção* (commitment-confidence,
> §7), which grades how strongly one individual artifact is held.

**The inverse relation (a DESIGN INTUITION, unmeasured — no instrument in this repo has tested it):**
higher authority → slower, more ceremonial change; deliberate, so *code does not change at
axiom-velocity and axioms do not freeze at code-velocity*.

**"Altitude" reuses I9's metaphor, not its claim.** Reading the three bands as three
commitment-heights borrows the *altitude* framing of CONCEPT-MAP's **I9** ("every stage is the same
process at a different altitude", *built (convention)*). But I9's actual content is *recursive
self-application* — a stage re-entering the pipe — a different claim than an authority-strata ordering;
only the metaphor is reused here, its recursion content credited where it applies, at §6's Tier-2 re-entry.

---

## 2. Disambiguation (load-bearing — keep near the top)

The three levels partition artifacts by an **independent COMMITMENT attribute** — how durable and
binding an artifact is — **realized via two distinct gates: PROMOTION-gating at the
understanding↔canonical seam, and the epistemology DISCHARGE-gate (§5's two-faces) at the
canon↔execution seam.** They are **not** a re-ordering of the OQ-A-locked stage sequence, and the
table below is an **approximate mapping, not the definition** of the partition.

Relation to Axis 2 is **mixed, not clean**:
- **Orthogonal** to REPRESENTATION (typing) and COMMUNICATION (provenance): a discovery, a
  constitution, and a diff each still carry typing and provenance — those mechanisms are
  band-invariant.
- **COUPLED** to EPISTEMOLOGY (the residue/gate mechanism): in its BROAD form throughout (convicção/
  consistency for belief-canon, discharge/gate for obliging canon), but only the OBLIGING sub-band and
  the **canon↔execution seam** are defined through the NARROW discharge/gate that is §5's two-faces.
  (The understanding↔canonical boundary is defined by PROMOTION-gating, not the two-faces.)

**Approximate stage/band mapping:**

| Axis-1 stage OR canon family | Commitment band |
|---|---|
| define → research → findings → **discovery** | **UNDERSTANDING** |
| **spec** (Axis-1 stage) · rule-canon · belief-canon | **CANONICAL** |
| plan → (stories → tests) → implement → verify → emit-signals | **EXECUTION** |

Only `spec` in the middle row is an OQ-A pipeline stage; rule- and belief-canon are authored
*beside* the pipeline (belief-canon's route into the graph is the **line-180 PLANNED /
out-of-scope** discovery→knowledge-node branch, §3). Two consequences:

1. **The commitment axis cross-cuts the stage order.** In the locked sequence `… discovery → plan →
   spec …`, **`plan` (execution) precedes `spec` (canonical)** — so the bands are **not contiguous**
   along the stage line. The pipeline interleaves canonical-authoring with execution.
2. **The mapping is lossy at the seam.** `stories`/`tests` are spec-derived build artifacts on the
   canonical→execution boundary; they inherit obligations from the spec but sit execution-side
   because they *prepare the change*. Band edges are not sharp.

---

## 3. Discovery as the hinge

The **discovery** is doubly load-bearing: the *terminal artifact of UNDERSTANDING* **and** the
*fork* deciding **which KIND of durable commitment** it becomes. Both horns land in CANONICAL — the
fork is *within* canonical, not canonical-vs-execution:

- **discovery → spec** — the discovery becomes an implementation contract (the OQ-A pipeline path).
- **discovery → knowledge-node** — CONCEPT-MAP marks this branch **PLANNED / OUT-OF-SCOPE in real
  code** (`CONCEPT-MAP.md` ~line 180; `TUNING-LOOP.md` v2.x), "the closest existing analogue of the
  typed-connected-objects vision."

This lens **names and motivates** the second horn — it is *why* the belief-canon family (§4) needs a
home that is not `spec` — but **does not close it, upgrade it to in-scope, or claim it is built.**

**Execution is never a sibling of this fork.** It is always *downstream* of whichever canonical horn
is taken: there is **no `discovery → execution` write-path** that skips a canonical commitment.
"Docs before code" (the DomainSpec object-policy, `implementation/domainspec/AUTHORITY-MAP.md`)
holds — a discovery authorizes; it does not mutate code. The path is always discovery → (canonical
commitment) → execution.

---

## 4. The canon splits by what it binds

The CANONICAL band is not one thing. It splits by **what kind of claim the artifact binds you to** —
a *belief* held by commitment, a *rule* that obliges, or a *contract* to be built.

| Family (gloss) | Binds | Node type(s) | Obliges an action? | What binds it |
|---|---|---|---|---|
| **CRENÇA** (*belief*) | a claim you **bet** is TRUE | **axioma** · **premissa** · **experimento** (below) | **no** — constrains what you may *assert*, not what you must *do* | **convicção** — bound by CONVICTION, not by proof |
| **REGRA** (*rule*, normative) | what you **must / must not** do | **constituição** | **yes** | a **discharge/gate** — bound by ENFORCEMENT (§5) |
| **SPEC** (contract) | what the system **shall be** | spec + glossary/domain-dictionary | yes, of the build | the **discharge** execution provides — bound by ENFORCEMENT (§6) |

> **experimento is a FUTURE, empty slot** — *empirically-earned* truth, a belief graduated from bet
> to established-by-experiment. **Not populated** in this repo. Whether an experiment *result* is
> even a node of this kind, or merely a confidence-upgrade event on a premissa, is an **open fork**
> (§8a).

**Two things about this table are aspirational, not descriptive:**

1. **The node types are PRE-EXISTING** (borrowed, not invented here): the premise/axiom/constitution/
   convention taxonomy is an *installed capability* — the `ontology-vault` sigil lists exactly
   "premise, axiom, constitution, or convention documents" as governed inputs
   (`.claude/skills/ontology-vault/SKILL.md` ~line 84). This section's contribution is only the
   **belief-vs-rule labelling** over those types plus the authority-strata mapping — not the types.
2. **The belief/rule cut is an aspirational RE-TYPING over a messy substrate — it leaks against the
   repo's real axioms.** The existing `axioma` node type is *heterogeneous*, not cleanly descriptive:
   `implementation/domainspec/vault/axiom/ontology-axioms.md` states axioms as obligations ("Labels
   **must** be orthogonal"; a rule that "should not exist") — normative, not descriptive — and
   **AX-ONT-7** is `node_type: axiom` yet explicitly a revisable *bet* ("we are betting accordingly …
   we expect to revise or retire this axiom"), i.e. premissa-grade. `AUTHORITY-MAP.md` frames
   `AXIOMS.md` as "governance principles / highest-level governance logic" (normative). So the clean
   crença/regra cut is a **proposed re-typing the current substrate does not yet honor**, not a
   description of it.

**Conceptual / epistemic-principle notes sit OUTSIDE this partition.** A meta thinking-tool (informs
all, obliges nothing) is not a pipeline-produced artifact, so it is neither understanding, canonical,
nor execution — the commitment partition ranges only over pipeline-produced artifacts and is **not
exhaustive over all artifact kinds.** Conceptual notes cut *across* the bands, the way Axis-2
mechanisms do.

### The two-System-5 question — an OPEN candidate convergence, NOT earned

It is tempting to say the belief-vs-rule split "recovers" the two System-5s of findings.md §1.
**It does not, and this doc will not claim it does.** The two cuts are **orthogonal**:

- **findings.md §1 splits by RECURSION LEVEL.** cav2's `AUTHORITY-MODEL` is **S5-outer**
  (meta-authority over what may *count as* an authority KIND); DomainSpec's AXIOMS and CONSTITUTION
  are **S5-inner** (object-policy inside one manufactured authority). Critically, **axioma and
  constituição sit at the SAME level, S5-inner** — findings.md groups them together, one recursion
  apart from cav2.
- **The belief-vs-rule cut SPLITS the two artifacts findings.md GROUPS.** Here axioma is *belief*
  (held by commitment) and constituição is *rule* (normative) — different families **at the same
  recursion level.**

So one cut groups {axioma, constituição} by recursion level while the other separates them by what
they bind. **These are orthogonal partitions, not the same partition seen twice.** Whether they
*converge* into a single richer authority model is a **candidate convergence that is NOT earned** —
carried as an open question (§8c), alongside findings.md's own OQ-cav2-link ("cav2-as-DomainSpec's-S5
is analogy, not a repo-cited dependency"). This lens deliberately does **not** write "re-derives /
recovers / grounds the two-S5 split," and the authority↔velocity axis (§1) is **silent on the
recursion boundary** — both S5s land in the same *canonical* band, so that axis cannot collapse them.

---

## 5. Governance has two faces — but only for OBLIGING canon

CONCEPT-MAP's **I4** ("claim ≤ proof", *designed, Lean-deferred*) is usually read as a gate on
*content* claims. This section **applies it to obliging governance** — an *application* of I4 + the
`governance-gap` signal + the Open-Questions residue convention, **not a new mechanism.**

**The two faces apply to REGRA and SPEC — the canon that obliges an action:**
- **STATEMENT** — the text of the rule/contract. *Cheap.* A constitution clause is a sentence.
- **DISCHARGE** — the work that **proves reality obeys it**: the validator, the CI check, the gate.
  *Expensive.*

**The governance-gap test keys on the "Obliges an action?" predicate (§4's column), NOT on node-type.**
An ungated artifact is a `governance-gap` **iff it obliges an action** — the node-type label never
decides it. Belief-grade content obliges nothing → no discharge of its own; the "author no canon that
contradicts an axiom" constraint is a REGRA-grade meta-rule over the belief graph, not the belief's
discharge. So until §4's re-typing lands, §4 item #2's obliging axiomas ("Labels **must** be orthogonal")
land on the OBLIGING side by ACTUAL binding — then class (a) or (b) per whether any check exists.

**Two residue classes for obliging canon (do not conflate them):**
- **(a) TRULY ungated** — *no* check of any kind exists. This is the `governance-gap` (CONCEPT-MAP's
  "framework blind spot"), tracked as "asserted, not gated" (sibling of **OQ-G**, "legibility
  asserted, not gated"). The aphorism below is scoped to **class (a) only.**
- **(b) MANUALLY gated** — a human discharge exists but is not automated. A manually-gated rule **IS
  gated** because that discharge — the owner *as decider/gate* — exists; the owner is the gate the
  read-only arm proposes *to* (§6), not part of the arm. It is **automation-debt** (findings.md's
  Step 3: make S3 continuous), **not a governance-gap.**

> **A rule without *any* gate is an opinion with frontmatter.** (Class (a) only — a manually checked
> rule is a gated rule carrying automation-debt.)

**On cost and ceremony (bounding §1's slowness claim):** for **gated** canon (rules/specs),
change-cost ∝ how hard the discharge is to re-prove — *"cost ∝ provability"* (a design aphorism, not
a measured finding). This does **not** explain §1's ceremony *in general*: the belief family is the
**highest-authority, least-gated** canon, so its ceremony is driven by **authority / blast-radius**
(§1's inverse relation), **orthogonal** to provability — "ceremony is the discharge" only where one exists.

**Where the repo stands:** findings.md is blunt that **S3 is manual** ("built but MANUAL"; §1, §3
Step 3) — so most existing obliging canon is class **(b)**, automation-debt, **not** class (a)
governance-gap. The fix is findings.md's own Step 3, which this lens does not pre-empt.

---

## 6. Execution = the enforcement arm

Execution is not a fourth canonical family beside crença/regra/spec — it is a different LEVEL, the
**enforcement arm of the two OBLIGING families (regra + spec).** A diff exists to *discharge* what
regra or spec obliges (make code obey a spec, make reality obey a constitution). This is why §3's
fork never lets execution bypass canon: execution has nothing to enforce without an obliging
statement above it.

**The boundary test is NOT code-vs-doc.** It is:

> **Does authoring this artifact discharge a machine-CHECKABLE obligation?**

If yes, it is execution regardless of whether it is `.ts` or `.md`. A schema file a validator runs is
execution; a prose "principle" that nothing checks is canon, not execution (belief-grade if it
obliges nothing, §4). Two tiers:

- **Tier 1 — configure existing gate machinery.** A new rule inside an *already-built* linter,
  validator, or schema. *Cheap* — the check itself needs **no new spec→verify cycle**; you are
  configuring machinery that already passed one.
- **Tier 2 — build new checking machinery.** The obligation's check does not yet exist, so producing
  it **re-enters the pipeline** `spec → code → verify` on its own account. That re-entry **is
  CONCEPT-MAP's I9 self-application** (a stage running at a lower altitude) — and it does **not**
  settle §8b's "one execution vs two" fork: it is self-application *within* the code altitude, not
  evidence of a second one. Tier 2 is where a governance obligation becomes a small product.

**Bind to the read-only discipline.** The enforcement arm is an **observer that PROPOSES to a gate +
owner — never a measure-and-mutate daemon.** findings.md is categorical: standing up an acting daemon
is "the one move all three governance-theorem lenses forbid" (§0, §2). And the 2026-06-24
ontology-operationalization findings supply the load-bearing invariant: **no modeling surface may
hold a write-edge to `promotion-status`/authority** — the *write-authority proviso*, which must be an
**architectural absence**, not a relaxable policy
(`research/2026-06-24-ontology-operationalization/findings.md` §2). Execution changes *code reality*,
never *authority reality*: the moment the arm can write its own promotion-status, the regulator
re-fuses with the regulated (Conant-Ashby) and §1's band separation is void.

---

## 7. Corroborating (not confirming) evidence — the ZefraHub vault

**ZefraHub is a SEPARATE application repository** — a sibling that *consumes* Arcanum, not part of
this engine. It **reportedly** builds the belief-canon branch on disk — structural shape only, **not
verified here**: node types **axiom / premise / constitution / conceptual**, typed **derives-from /
supersedes** edges, and a **dual-confidence** scheme separating *veracidade* (veracity —
evidence-confidence: how true) from *convicção* (conviction — commitment-confidence: how bound-in).

**What this does and does not license:**

- **It corroborates that the belief-canon branch is BUILDABLE** — a sibling repo instantiates shapes
  matching those §4 describes. Corroboration, not confirmation: it raises the credence that the design
  is realizable.
- **It is NOT this repo's build status and NOT engine behavior.** Nothing in ZefraHub is built
  *here* (§0's status floor holds); it is a consumer app, so its vault does not mean *this* machine
  runs the branch.
- **Public/private boundary respected.** No ZefraHub domain prose is imported; only the structural
  shape is named. Its dual-confidence split independently echoes the ontology-vault quality-bar's
  "evidence confidence" vs "commitment confidence" (`.claude/skills/ontology-vault/SKILL.md`).

---

## 8. Open forks — preserve, do NOT resolve

Three forks are named and left open. Closing any is an owner decision this doc lacks the evidence to
make.

**(a) The experiment horn.** Is an *experiment result* a **first-class canonical node** (experimento,
§4) — its own belief type — **or** merely a **confidence-upgrade event on a premissa** (bumping
veracidade without minting a new node)? The **existing tooling LEANS toward the confidence-event horn
without deciding it**: `ontology-vault`'s `promote-confidence` and `premise-review` modes are built to
*move a premise's confidence*, not to mint an experiment node
(`.claude/skills/ontology-vault/SKILL.md`). That lean is evidence, not a verdict — the fork stays
open, and experimento stays an empty slot until it is closed.

**(b) The execution-altitude horn.** Is execution **code-only** (one altitude — the diff), **or is
there a second execution at a second altitude** (a governance-execution enforcing canon *about the
machine itself*, distinct from code that serves the domain)? This ties to findings.md's
**OQ-Saturn-scope**: Saturn = "the S3↔S4 control loop" vs Saturn = "the whole stack" is unresolved
(`findings.md` §1; `SATURN-LAYER-MAP.md` OQ-2). Whole-stack → plausibly two executions; control-loop
→ one. Note §6's Tier-2 re-entry does **not** settle this. Unresolved — carried.

**(c) The two-S5 reconciliation (carried from §4).** Whether the belief-vs-rule cut and the
recursion-level cut *converge* into one authority model, or remain permanently orthogonal, is open.
It inherits findings.md's OQ-cav2-link (cav2-as-S5 is analogy, not a cited link). The
authority↔velocity axis of §1 is explicitly **not** allowed to settle it — both S5s share the
canonical band, so the axis is silent on the recursion boundary.

---

## 9. What this doc does NOT decide or claim

Closing overclaim guard (the "built vs lens" and "not domainspec-v2" disclaimers live once, in §0):

- Does **not** claim the belief-vs-rule split **re-derives, recovers, or grounds** the two
  System-5s — an **open, unearned analogy**; §4 shows the cuts are orthogonal.
- Does **not** populate **experimento** — a reserved FUTURE slot, empty by design.
- Does **not** treat the inverse authority↔velocity relation as measured, or "cost ∝ provability" as
  a finding — both are design intuitions/aphorisms (§1, §5).
- Does **not** open any `discovery → execution` path skipping a canonical commitment (§3), nor
  upgrade the `discovery → knowledge-node` branch to in-scope (§3; CONCEPT-MAP ~line 180).
- Does **not** re-announce I9, the `governance-gap` signal, the ontology-vault node types, or the
  write-authority proviso as novel — all pre-existing and credited.
- Does **not** treat ZefraHub as engine behavior or this repo's build status — sibling-repo
  corroboration only, as reported.
- **Is itself a conceptual note / meta thinking-tool** sitting OUTSIDE the commitment partition (§4):
  it obliges no action, so §5's two-faces test (which ranges only over obliging canon) does not touch
  it — no discharge, **not** a governed rule, **not** a governance-gap.

> **Proposed follow-up (not performed here):** CONCEPT-MAP should carry a reciprocal `relates-to`
> back-link to this doc as its *third cut* — a separate change outside `development/machine-map/`,
> noted so it is not forgotten, not silently added.

---

## 10. Connections

| Document | Type | Description |
|---|---|---|
| [findings.md](findings.md) | `derives-from` / `relates-to` | The machine-map synthesis this lens re-reads by commitment. Sources the two-S5 recursion-level split (§4), the manual-S3 fact (§5), the read-only-not-daemon discipline (§6), and OQ-Saturn-scope (§8b). |
| [../../projects/framework-unification/CONCEPT-MAP.md](../../projects/framework-unification/CONCEPT-MAP.md) | `relates-to` | The two-axis map this is a *third cut* over. Sources the OQ-A stage order (§2), I4 (§5), I9 (§1/§6), the `governance-gap` signal (§5), and the line-180 discovery→knowledge-node branch (§3). A reciprocal back-link is a **proposed follow-up**, not made here. |
| [research/2026-06-24-ontology-operationalization/findings.md](research/2026-06-24-ontology-operationalization/findings.md) | `cites` | The write-authority proviso (§6) and the ruling that the Ontology-A/B merge is unsound (§0). |
| [../../implementation/domainspec/AUTHORITY-MAP.md](../../implementation/domainspec/AUTHORITY-MAP.md) | `cites` | S5-inner object-policy (AXIOMS as "governance principles"; "docs before code") — one of the two System-5s (§3, §4). |
| [../../implementation/domainspec/vault/axiom/ontology-axioms.md](../../implementation/domainspec/vault/axiom/ontology-axioms.md) | `cites` | The heterogeneous-`axioma` counter-example (AX-ONT-7 = axiom-typed but a revisable bet) grounding §4's "aspirational re-typing" flag. |
| [../../cyberAlchemy-v2/authority/AUTHORITY-MODEL.md](../../cyberAlchemy-v2/authority/AUTHORITY-MODEL.md) | `cites` | S5-outer meta-authority over authority KINDS — the other System-5 (§4). |
| [../../.claude/skills/ontology-vault/SKILL.md](../../.claude/skills/ontology-vault/SKILL.md) | `credits` | Pre-existing installed capability holding the premise/axiom/constitution/convention node types (§4) and the evidence-vs-commitment confidence split (§7). The node types are borrowed, not invented here. |
| ZefraHub vault (external sibling repo) | `corroborated-by` | Sibling app repo that **reportedly** instantiates axiom/premise/constitution/conceptual nodes, typed derives-from/supersedes edges, and dual confidence (veracidade + convicção) — **as reported, not verified here.** Corroborates *buildability* of the belief-canon branch — not this repo's build status, not engine behavior. Public/private boundary respected; no domain prose imported. |
