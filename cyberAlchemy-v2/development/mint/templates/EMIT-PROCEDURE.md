---
node_type: procedure
is_session: false
status: candidate
boundary: INTERNAL — Mint emit-logic (L1 stage-2); intended-not-shipped, non-executed spec
created: 2026-06-29
authored_by: task-session (SWU-3)
swu: SWU-3 (authority-spine emit step — the L1 stage-2 logic)
composes:
  - templates/L0-compose-contract.md (stage 1 — produces the tree this stage casts onto)
  - templates/{authority-model,source-spine,promotion-policy,constitution,definitions,crosswalk}.md (the 6 emit-templates, SWU-2)
front_door: development/authority-triage/SKILL.md (review-mode, INTERNAL)
note: Paths are repo-root-relative from domainspec-core/. This is the PROCEDURE; the worked output is examples/<domain>/.
---

# Mint — EMIT PROCEDURE (SWU-3, the L1 stage-2 logic)

> **Stage 2 of the 5-stage mint flow** (ARCHITECTURE-BUNDLE §The 5-stage mint flow,
> row 2 `authority-spine seed`). It runs **after** L0 (the tree exists with empty
> authority slots, per `L0-compose-contract.md`) and **before** L2 (the signed
> decision-gate, BLOCKED on the attestation/signer capability). Input: the 6 SWU-2
> templates + a `<DOMAIN>` spec. Output: the domain's authority spine, written into the
> minted tree, with every domain-originated kind **proposed** (not ratified) through the
> authority-triage front-door in review-mode.

## What this procedure is (and is NOT)
- **IS:** the deterministic, repeatable instantiation logic — for each of the 6 templates,
  *how a placeholder is filled, where the file is written in the minted repo, and how a
  proposed kind is routed through authority-triage for the domain owner to ratify.*
- **IS NOT:** a runtime tool (Mint is intended-not-shipped) and NOT the L2 signing act.
  The signed mint record this stage seeds is **L0-attributional placeholder** (see §6) —
  it records *who proposed what*, not a cryptographic attestation, because L2 signing is
  blocked on the attestation capability (`../../attestation-capability/`).

## Inputs
| input | meaning | source |
|---|---|---|
| the minted tree | L0 output: partition tree + clone-safe attach, **empty** authority slots | `L0-compose-contract.md` §What L0 produces |
| `<DOMAIN>` spec | the domain's name, objective, governed subject, primary source, separable concerns, conflation risks, proposal-unit name, and the candidate domain-originated authority function(s) | operator / domain interview |
| the 6 templates | `templates/{authority-model,source-spine,promotion-policy,constitution,definitions,crosswalk}.md` | SWU-2 |
| authority-triage | the front-door classifier/router (review-mode, INTERNAL) | `development/authority-triage/SKILL.md` |

## The inherit / localize boundary this procedure enforces (the load-bearing rule)
Every fill obeys the SPEC §Inheritance boundary test:

> **defines *how* authority is made → INHERIT (do not parameterize); *what* authority the
> domain holds → LOCALIZE (fill the placeholder).**

- **INHERITED (copied verbatim, never a `<DOMAIN>` slot):** the 4-column table FORMATs, the
  source-movement pipeline shape, the non-collapse *rule structure* (`X is not Y`), the
  promotion-ladder shape, the gate vocabulary (`pass/flag/block/defer`), the claim≤evidence
  rule, the anti-laundering rule shape, the load-bearing-term tracking rule, the three-voice
  definition-card format.
- **LOCALIZED (every `<DOMAIN>`/`<...>` placeholder):** the kind *rows*, the definitions, the
  constitution *object* rules, the source *families*, the gates, the bridge *concepts*, the
  decisions.

## The no-leak rule (Obs-B, baked into every fill)
**cav2 never appears on a resolution path — citation / harvested precedent only.** This
procedure NEVER fills a placeholder with "cav2 resolves / cav2 is the method authority /
route to cav2". The ONLY cav2 mentions a conforming emit produces are:
1. the `source-spine.md` **CyberAlchemy v2** family row — `Allowed use: harvested precedent
   (supporting source), citation/provenance ONLY`; `Blocked use: on ANY resolution path`;
2. the `crosswalk.md` **CyberAlchemy v2** row — a crosswalked precedent with a
   `borrow-carefully` Boundary verdict;
3. optional `Evidence:` citations in definition cards (provenance, not a resolution path).
Every method/promotion/admission/source-posture/non-collapse decision resolves to the minted
repo's **own** `authority/`. The leak the precedent's `2026-06-26` mint-act output committed
("CAV2 as external method authority") is **impossible to emit** through this procedure: no fill
rule produces that phrasing, and a default check (§7) greps for it.

---

## Per-template emit steps (the deterministic procedure)

### Step 0 — derive the `<DOMAIN>` fill-set
From the `<DOMAIN>` spec, derive the fill-set ONCE (reused across all templates so the spine
is internally consistent):

| placeholder family | derived from the domain spec |
|---|---|
| `<DOMAIN>` / `<DOMAIN_OBJECTIVE_SENTENCE>` | the domain name + its one-line purpose |
| `<DOMAIN_GOVERNED_SUBJECT>` / `<DOMAIN_PRIMARY_SOURCE_*>` | what the domain governs + its official source |
| `<DOMAIN_PROPOSAL_UNIT>` | the domain's unit of proposal (research: invariant; process: rule-change) |
| `<DOMAIN_ORIGINATED_KIND_n>` + `<DOMAIN_NEW_OWNER_ROUTE_n>` | **the candidate domain-originated authority function(s)** — the Obs-A core (see Step 1) |
| `<DOMAIN_NON_COLLAPSE_n>` / `<DOMAIN_BLOCK_n>` / `<DOMAIN_SEPARABLE_CONCERN_n>` | the domain's specific conflation risks |

**Gate (failure mode, EXECUTION-PACK §Failure mode):** if the domain yields **no** candidate
domain-originated kind, the procedure emits a `blocked-default-deny` authority-model and routes
to the owner to enumerate kinds first — it does NOT emit a re-skin to fill the slot.

### Step 1 — `authority-model.md` → `<TARGET_REPO>/authority/AUTHORITY-MODEL.md`  (the Obs-A core)
1. Fill the inherited 4-column kinds table. The fixed rows (Primary source, Related evidence,
   Local synthesis, Candidate-proposal-unit, Workflow witness, External policy authority) are
   meta-machinery — localize only their labels.
2. **For each candidate domain-originated kind, run the authority-triage front-door
   (review-mode):**
   - **intake** the candidate kind (home: the `<DOMAIN>` spec);
   - **precedent sweep** (build-from-owned) over `cyberAlchemy-v2/authority/` — confirm the
     function is NOT already owned by a cav2 D49 row;
   - **F3(c) membership test** (criterion §5) — the kind is domain-originated **iff it is
     NEITHER lexically NOR by-owner-route identical to any cav2 D49 row.** A kind routed to
     `constitution-governance` governing source-posture/promotion is **owner-route identical to
     cav2's `Constitution`** → REJECT as a re-skin (the precedent's exact `Method authority`
     hole). The kind must carry a **genuinely new owner route** (a new governance function);
   - **D49 default-deny:** the kind is not a row in cav2's enumeration → it defaults denied for
     *cav2*, which is correct: it is a **domain-local** kind, proposed into the domain's OWN
     table, NOT added to cav2's closed set. Triage's verdict is `new-authority (domain-local)`,
     routed to the **domain owner** for ratification.
3. Write the domain-originated row(s) **bold + flagged** `⟵ domain-originated (PROPOSED;
   owner-ratify)`. Each PROPOSED kind carries a **default-deny Blocked-use cell** (WORK-PACK
   SWU-3 acceptance: "every proposed kind carries a default-deny row").
4. Keep the **D49 owner-gate note** verbatim: Mint *proposes*; the `<DOMAIN>` owner *ratifies*;
   this is the domain's own table, **not** a change to cav2's enumeration.
5. Localize the non-collapse rules; keep the last one (harvested precedent ≠ final correctness)
   verbatim in shape — it is the Obs-B rule at the rule level.

### Step 2 — `source-spine.md` → `<TARGET_REPO>/authority/source-spine.md`
1. Fill the Source-Families table. The **CyberAlchemy v2** row is **citation/provenance only**;
   its Blocked-use cell EXPLICITLY forbids cav2 on any resolution path. (Inherited verbatim —
   this row is the Obs-B fix at the source-family level; do not soften it.)
2. Localize the domain's evidence families; keep the source-kind label set verbatim (note that
   harvested framework precedent gets `supporting-source`, **never** `authority`).
3. Keep the Harvested-Local-Controls demotions and the closing "no cyclic citation chain
   promotes authority" line verbatim in shape.

### Step 3 — `promotion-policy.md` → `<TARGET_REPO>/authority/promotion-policy.md`
1. Localize the ladder rung labels; every "May promote to" target is a `<DOMAIN>`-local state —
   promotion never crosses into a framework authority.
2. Fill the required gates. The **Authority gate** routes to `this repo's authority/` (never a
   framework). Fill **≥1 domain-originated gate** (a gate cav2 has no analog for) — Obs-A
   support at the rule level.
3. Keep the promotion-block "would resolve by traversing into a framework attachment → BLOCK"
   verbatim (Obs-B at the promotion level).

### Step 4 — `constitution.md` → `<TARGET_REPO>/authority/constitutions/<DOMAIN>-CONSTITUTION.md`
1. This file IS the localized home of method authority (source posture, promotion discipline,
   non-collapse, separation) — owned here, NOT delegated to any framework.
2. Localize the object rules (`<DOMAIN>-C1..Cn`); each carries a `Validation mode:` line.
3. Fill **≥1 domain-originated object rule** (`<DOMAIN>-Cn`) — a credibility rule cav2 has no
   analog for (Obs-A rule-level).
4. Keep the inherited meta-rules verbatim in shape: claim≤evidence, finding-to-development
   contract, local-status-non-collapse, **No Reciprocal Authority Laundering** (the Obs-B
   positive control — "transfers no framework authority"), load-bearing-term tracking.
   *(Note: the CONSTITUTION kind's owner route is `constitution-governance` in both cav2 and the
   domain — the constitution itself is inherited meta-machinery; the domain-ORIGINATED kinds for
   Obs-A live in AUTHORITY-MODEL, not here. Filling a domain object rule here is NOT an Obs-A
   kind.)*

### Step 5 — `definitions.md` → `<TARGET_REPO>/definitions/DEFINITIONS.md`
1. Seed 1–2 three-voice cards (`<DOMAIN>-D1`, `<DOMAIN>-D2`); the domain owner authors the rest
   through the definitions lifecycle.
2. `<DOMAIN>-D2` is the domain-originated term card. Its `Evidence:` MAY cite a harvested cav2
   snapshot — that is **provenance, not a resolution path** (removing the attach does not change
   the definition). A `Source kind: method-authority` points at the **domain's OWN** constitution,
   never cav2.

### Step 6 — `crosswalk.md` → `<TARGET_REPO>/RELATED-FRAMEWORK-CROSSWALK.md`  (stage 4 / L2-adjacent)
> **Sequencing note:** per the crosswalk template header, the crosswalk EMIT is stage 4 (L2-
> adjacent), not stage 2. SWU-3 (this procedure) seeds it for completeness so the spine is whole,
> but its `promotion-candidate` bridge rows are proposals for a **separate downstream owner-
> ratified** act (the D49 owner-gate), **never** the mint act (criterion Obs-C note).
1. The **CyberAlchemy v2** row appears as ONE crosswalked precedent: `Source kind:
   local-inference`, `Boundary: borrow-carefully` — citation with a verdict, never authority.
2. A `promotion-candidate` bridge row is a proposal for a future owner decision; keep the
   "Crosswalk ≠ dependency (Obs-B)" closing note verbatim.

---

## §6 — The signed mint record (L0-attributional PLACEHOLDER; L2 signing BLOCKED)
Stage 3 of the flow emits `<TARGET_REPO>/authority/decisions/<date>-mint.md`. **L2
cryptographic/attested signing is BLOCKED** on the attestation/signer capability
(`../../attestation-capability/`; owner decision 2026-06-29). Until that capability's L1
integrity-seal MVP exists, this procedure emits an **L0-attributional placeholder** record:
- it **names** the proposed domain-originated kinds and the owner route each was triaged to;
- it records `signed_record: PLACEHOLDER (L0-attributional) — L2 attestation pending on
  ../../attestation-capability/`;
- it carries the propose-not-ratify posture: Mint **proposed** these kinds; the `<DOMAIN>` owner
  **ratifies** in a separate act. The placeholder is honest evidence of *who proposed what*, not
  a forged attestation. **Obs-A/B/C are scored at this record's commit** (the mint-act output
  state, criterion §5) — the placeholder is sufficient to define that boundary; only the
  *cryptographic* seal is deferred.

## §7 — Emit self-checks (run after every emit, before the record)
Deterministic checks a conforming emit must pass (these are the per-emit analog of the
criterion's mechanical sub-rules — NOT the frozen N=3 run):
1. **parses** — every emitted authority-model table parses (4 columns, no dangling `<...>`).
2. **default-deny** — every PROPOSED kind has a non-empty Blocked-use cell.
3. **no-leak grep (Obs-B)** — `grep -niE "as (an? )?(external )?method authority"` over the
   emitted spine returns **zero** matches; every cav2 mention sits in a citation / precedent /
   forbid frame.
4. **domain-originated present (Obs-A)** — ≥1 kind row fails the F3(c) test against every cav2
   D49 row (lexical AND owner-route new), AND ≥1 promotion-policy/constitution rule is
   domain-originated.
5. **resolution scan (Obs-B/Obs-C)** — every governance rule the spine enforces resolves inside
   the minted `authority/`; removing the `--source` attach leaves zero dangling references; no
   rule requires cav2 to ADD/ALTER a D49 row to be operable.

A failing check 1–5 is a **block** — do not emit the record over a failing spine.

## §8 — claim ≤ proof
This procedure is **intended-not-shipped emit-logic**, validated on the hand-built worked
example (`examples/`), NOT a run of the frozen criterion. SURVIVED/FALSIFIED are rendered only
by the downstream N=3 run (criterion §4). What §7 proves per emit: the spine is leak-stripped,
parses, and carries a domain-originated kind **by construction** — it cannot reproduce the
precedent's leak.
