# Findings — OQ-6 open questions: exception-lane permanence + edge-witness reading

Dispatch: `2026-07-08-open-questions-noncollapse` · type: research · exit: **resolved**
Final approver: Vlachopulos (auditor) — **ACCEPT**. 8 agents (4 explorer / 1 synthesizer / 2 skeptic / 1 auditor), 1 zig-zag loop.
Source questions: the two open questions left by [2026-07-08-d6-node-noncollapse.md](../../../../definitions/reviews/2026-07-08-d6-node-noncollapse.md).

> **One-line answer to both.** Neither question is a fact of nature and neither is "mostly an
> owner decision with a small residue" — **the residue is the structure.** Both answers are
> owner-decidable *only given today's bijections*, and those bijections are the fragile,
> unmonitored, load-bearing part. Two draft claims were **refuted/withdrawn** under review; what
> survives is smaller, mechanically testable, and louder about its own fragility.

---

## The reconciling fact both questions share (verified)

The checker claims to implement DESIGN-SPEC-v2, whose W-edge witness has **four clauses** —
(1) an edge *exercised in a real instance* (NOT the schema's `edge_participation` declaration),
(2) DS-D8 resolution, (3) non-laundering, (4) owner-admitted. The **shipped `wEdge`
([meta-type-noncollapse.ts:105-107](../../../../impl/tools/lib/meta-type-noncollapse.ts#L105-L107))
implements clause 2 alone** — a `setEq` over DS-D8-resolved source/target sets. Clause 1 and
clause 3 are **not in code**; clause 3 is *proxied* by `DEFAULT_EXCEPTION_ALLOWLIST =
{rule,policy,calculation}` ([:21](../../../../impl/tools/lib/meta-type-noncollapse.ts#L21)),
which short-circuits the trio to `exception-lane` at
[:115](../../../../impl/tools/lib/meta-type-noncollapse.ts#L115) *before* the witnesses run.
Both open questions turn on this gap: the spec mandates a certified/exercised witness; the
implementation ships a proxy because the certified form is either un-computable under the moat
(OQ-A) or un-populatable without a corpus (OQ-B). **Auditor-confirmed against source.**

---

## OQ-A — can mechanical detection replace the owner-enumerated exception lane?

| | |
|---|---|
| **Corrected answer** | The honest core is an **induction / identifiability limit — mechanically testable, NOT a moat/undefinability limit.** The question "is `formal_return_type ↦ (verb,target)` a *law* or an *accident of the current rows*?" is decidable by inspecting the registry; it never requires reading a value's meaning. |
| **Max defensible modal** | **"Stable while D15 and the owner's laundering-judgment hold, over the registry as it stands."** Not "permanent," not "conditionally permanent" — *axiom-relative and registry-relative.* |
| **Owner decision (crisp)** | Keep D15's moat AND keep judging the trio's `enforces/applies/calculates` edges as laundered correlates of `formal_return_type`? If yes → the allowlist stands. If a trio-separating edge with an endpoint typing *provably independent of* `formal_return_type` ever appears → the lane dissolves for that pair. |

**Withdrawals / demotions forced by review:**
- ❌ **WITHDRAWN — "certification is moat-forbidden."** Testing the functional dependency
  `value ↦ verb` treats the value as an **uninterpreted equality key** — exactly what
  `attribute-equals` already does opaquely — and never parses meaning. Co-variation is
  **shape-detectable without a moat read**; the claim was self-refuting (Gödel, construction A).
  An owner-provenance annotation (`derived-from` / `independent-of`) also makes certification
  architecturally available via the owner gate the design already ships (construction B).
- ⬇️ **DEMOTED — the keystone total function `{boolean↦enforces, strategy↦applies,
  value↦calculates}` is FALSE at n=3.** Calculation sources **two** verbs with **different
  targets** — `calculates→Operation`
  ([relationships.yml:100-102](../../../../definitions/relationships/relationships.yml#L100-L102))
  and `queries→Entity`
  ([relationships.yml:229](../../../../definitions/relationships/relationships.yml#L229)). So the
  edge carries information *beyond* the return sort; where a sort maps to multiple `(verb,target)`
  with distinct targets, shape-detection certifies "clean" outright (Taleb; **auditor-verified
  against source**).
- ❌ **STRUCK — "permanent."** D15 is an amendable owner-decision convention carrying a misuse
  warning ([DEFINITIONS.md:591](../../../../definitions/DEFINITIONS.md#L591)), not a theorem.

**The genuinely hard residue narrows to one case:** a hypothetical type byte-identical in
`(verb, target, formal_return_type)` to Rule (Taleb's "Scenario A2"), separable only by author
self-declaration. That is an **identifiability gap** (law vs. artifact), not undefinability — and
it is the *only* thing the lane irreplaceably covers.

**Two independent defeaters — preserved, do not collapse:**
- **Gödel (MODAL):** "permanent" fails even in a **frozen** registry — it rests on a repealable
  axiom with no backing theorem.
- **Taleb (EMPIRICAL):** the bijection is **fragile to the 15th meta-type** and unmonitored — and
  *already leaking* via Calculation.
- A registry-relative impossibility proof can be **sound AND fragile at once**; neither defeater
  subsumes the other.

**Hidden antecedent (elevated from footnote):** the collapse-resistance holds only while *each
`formal_return_type` sort maps to exactly one `(verb,target)` pair* — **unmonitored, and already
violated.**

---

## OQ-B — is the edge witness "authority-resolved" the right permanent reading, or must it tighten to "exercised instance"?

| | |
|---|---|
| **Corrected answer** | **The closure invariant that would make authority-resolution permanently sound is ILL-POSED** (upgraded from "unsound now"). It quantifies over "composes into different code" — Rice-undecidable in general — rescued to decidable only by pinning to D3's finite 4-axis proxy. **Proxy and target diverge exactly on D3's own clean-widening corollary.** |
| **The static contradiction** | [DEFINITIONS.md:111](../../../../definitions/DEFINITIONS.md#L111) — admissible IFF *composes into different code*; [:115](../../../../definitions/DEFINITIONS.md#L115) — *"widen a SOURCE endpoint (same target, same semantics) = clean"* admits a type **because it does NOT compose into different code.** Present at **N=14, no new type needed** (Gödel; **auditor-confirmed**). |
| **Owner decision (crisp)** | Adopt "every DS-D8 signature endpoint must be backed by an exercised, D3-witnessed edge" as a **promotion gate**? If yes → authority = exercised by construction, `wEdge` (clause 2) is a permanently-sound cache. If no → build the instance corpus and flip `wEdge` to clause 1, eating the collapse until coverage lands. |

**Withdrawal:** ❌ **"closure invariant → memoized cache → converge."** A cache memoizing an
ill-defined key does not converge; it stabilizes on the proxy's blind spot. And clean-widening is
the move the edge-law economy **prefers** ([:119-120](../../../../definitions/DEFINITIONS.md#L119-L120)),
so ghost endpoints are a **permanent generator**, not a one-time audit — the corpus already shows
`queries`=3 sources, `exposes`/`applies`=2 targets.

**The 28× / 8→1 collapse claim carries two silent assumptions — surface both:**
1. **It keys DS-D8 resolution on `feature_scope`.** Saga and Workflow both source `orchestrates`
   ([relationships.yml:148-177](../../../../definitions/relationships/relationships.yml#L148-L177)),
   two rows differing by `source_type` and `feature_scope`. **Key on verb-id alone and Saga~Workflow
   collapse today** — no new type needed. Any collapse count must ship *with its resolution key.*
2. **It conflates transient-collapse** (types whose distinction the corpus *will* exercise) **with
   structural-collapse** (genuinely vacuous types that *should* merge). Reporting one aggregate
   hides the signal that some types ought to be retired.

---

## Verdict table

| # | Question | Verdict | Owner / evidence |
|---|---|---|---|
| OQ-A | Can mechanical detection replace the exception lane? | **Not within the moat by certification — but "moat-forbidden" and "permanent" are WITHDRAWN.** Honest limit = finite-corpus identifiability; hard residue = Scenario-A2 author-declaration case only. Owner-decidable, but on a *fragile unmonitored bijection*. | internal (checker + DEFINITIONS + relationships.yml); external (nominal/structural typing, Tarski, Rice — all **demoted to analogy, none load-bearing**) |
| OQ-B | Is authority-resolution the right permanent reading? | **No by the design's own lights (spec already mandates exercised) — and the invariant that would rescue authority-resolution is ILL-POSED.** Resolvable by one owner decision (closure-as-promotion-gate) OR forced-tighten if the clean-widening audit finds a zero-composition membership. | internal (wEdge, D3, DS-D8, clean-widening corollary); external (functorial semantics / Spivak; coalgebraic behavioral equivalence / Jacobs) |

---

## Deciding tests — now runnable (no new corpus needed)

- **T-A1 (identifiability):** enumerate `formal_return_type ↦ {(verb,target)}` over active rows;
  any sort → ≥2 pairs means the total function is an accident. **Already TRUE for `value`.**
- **T-A2 (co-variation as opaque key):** run `value ↦ verb` as an equality-key check across
  instances — a covariation that holds is shape-*certifiable*, one that breaks is *detected*;
  either way no moat read. This is the concrete refutation of "moat-forbidden."
- **T-A3 (A2 probe):** search for two active types sharing an identical
  `(verb,target,formal_return_type)` triple → a genuine author-declaration-only distinction.
- **T-B1 (proxy divergence):** compute D3's 4-axis proxy per edge; flag pairs identical on all 4
  axes but distinct as types → clean-widened phantoms (expect `orchestrates` under verb-id keying).
- **T-B2 (resolution-key sensitivity):** recompute the collapse count under key = verb-id /
  (verb-id, feature_scope) / (verb-id, source, target). The count is meaningful only *with its key.*
- **T-B3 (transient/structural split):** partition each collapse set by "does any pending corpus
  row add a distinguishing axis-value?" → transient; else structural (escalate for merge).

---

## Implications for the D6 residue note

1. Replace "conditionally permanent" with **"stable while D15 + owner laundering-judgment hold,
   registry-relative"** — a live promotion-gate obligation, not a property.
2. Record **both defeaters separately** (Gödel-modal, Taleb-empirical); do not let one absorb the other.
3. Move the **bijection antecedent** (each `formal_return_type` sort ↦ one `(verb,target)`) into the
   D6 claim — and note it is **already violated** (Calculation).
4. Strike **"certification is moat-forbidden"** → "certification is architecturally available
   (opaque equality-key test + owner-provenance annotation); the surviving limit is finite-corpus
   identifiability."
5. State the **OQ-B antecedent as ill-posed** (Rice-undecidable, proxy-pinned; diverges on the
   clean-widening corollary).
6. Every collapse count ships **with its resolution key** and a **transient/structural split.**

## Implications for the checker — instruments review forced

| Instrument | What it does | Fires on |
|---|---|---|
| **Bijection-monitor gate (OQ-A)** | maintains `formal_return_type ↦ {(verb,target)}`; **warn** when a sort maps to ≥2 pairs (target already separates them → lane unnecessary), **escalate** when a `(verb,target,return)` triple hosts ≥2 types (Scenario A2 hard collapse) | already warns on `value` |
| **Clean-widening non-separation fix (OQ-B)** | mark clean-widened endpoints (same target, same semantics, widened source) **non-separating in `wEdge`** so they cannot manufacture phantom distinctions | `orchestrates`, `queries`, `exposes`, `applies` |
| **Declare the resolution key** | the checker must state whether DS-D8 resolution keys on verb-id / +feature_scope / +endpoints — Saga~Workflow collapse depends on it | `orchestrates:148-177` |
| **Transient-vs-structural split** | partition every collapse set; never report a bare aggregate | the 28× set |
| **Annotate `wEdge` + allowlist** | docstrings currently read as if `wEdge` is the full a1 fix — it is clause-2-only; the allowlist is a clause-3 proxy | `meta-type-noncollapse.ts:21,105-107` |

---

## Still-open — declared unverified (the required next verification pass)

The dispatch honestly did **not** close these; they are cheap and should run before any number is quoted:
1. **The 91 / 27 / 28× magnitudes** — Jacobs' checker run, unverified by the panel; **re-run the
   CLI under each T-B2 resolution key.**
2. **DS-D8's actual resolution key** — the *data* (Saga/Workflow both `orchestrates`, split by
   `feature_scope`) is confirmed; the **resolver was not located** to confirm it *keys on*
   `feature_scope`. One-line read of the DS-D8 resolver.
3. **`attribute-equals` opaque-token semantics** — one-line re-read of `relationships.yml:17` (cited
   as the opaque-equality precedent for T-A2).

Auditor's two copy-edit notes: "D15 is an amendable misuse-warning" is a loose gloss (D15 is the
declared-attributes *convention* that *contains* a misuse warning); "Saga & Workflow differ only by
feature_scope" also omits their `source_type` difference. Neither touches a load-bearing inference.
