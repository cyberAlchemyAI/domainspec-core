---
tags: [subagents, dispatch, review, strategy, specs, domainspec, invoke, governance]
node_type: strategy
is_session: false
layer: architecture
nature: procedural
status: draft
version: 0.1.0
last_updated: 2026-06-16
governing_law: constitution/subagents-strategy-constitution-proposal.md@v0.6.1-proposal
governing_constitution: constitution/specs-development-review-constitution.md@v0.1.0-proposal
type_skill: skills/review/SKILL.md
---

# Strategy — specs-development review

A **named, reusable review strategy**: when the *specs development phase* produces or
updates a DomainSpec spec document family, red-team **every created document** under
`dispatch_type: review` and ship verified change requests before the spec is treated as a
stable interface.

This is the **reference recipe** (the *how*) for the obligation set in
`constitution/specs-development-review-constitution.md` (the *what/why*): that constitution
requires the review (R-SDR-1), whole-corpus coverage (R-SDR-2), tensioned gate-passed lenses
(R-SDR-3), cited claim≤proof findings (R-SDR-4), and ledger registration (R-SDR-5); this doc
shows the dispatch shape that satisfies them. It is a **recipe**, not new law. It composes the public `invoke` spec-template family
(`arcanum/spells/invoke/templates/domainspec-spec/`) with the private dispatch-governance
chain (router → `review` → `register-dispatch`). Per submodule discipline that composition
lives only here, in the private parent — never in `arcanum`. The strategy adds **no field
and no principle**; every rule below is owned upstream and cited.

## When this strategy fires (P1 trigger)

Apply it whenever the specs development phase emits the DomainSpec spec document family for
a feature — i.e. an `invoke` `define`-mode run authoring `SPEC.md` plus its per-aspect docs
(`operations.md` · `queries.md` · `interfaces.md` · `states.md` · `events.md` ·
`mappings.md`, and the bundle/pack docs the template family ships). It satisfies the
router's P1 triggers:

- **synthesis** — the corpus is many cross-linked documents (SPEC + ≥6 aspect docs + the
  Concept Registry that ties them);
- **context protection** — the raw red-team output (every finding, every refutation) is far
  larger than the change-request list the parent needs back;
- **isolation** — attackers read the spec read-only; nothing they produce mutates the targets.

A single trivial spec (one inline capability, no aspect docs) may not clear P1 — review it
inline. The strategy is for the full document family.

## Target corpus

**All created documents** of the feature's spec family — not a sample. The attackers each
read the *whole* corpus (full reading), differing by lens, never by partitioning the files
(`review` skill, "Attack lenses"). Concretely:

- `SPEC.md` — What This Module Owns → Module Map → Capabilities → Domain Concepts →
  **Concept Registry** (typed IDs) → Feature Concept Graph → Aspect Docs index →
  Cross-Feature Dependencies / Produces-For.
- the per-aspect docs the SPEC links to (`operations.md`, `queries.md`, `interfaces.md`,
  `states.md`, `events.md`, `mappings.md`, `architecture-bundle.md`, `execution-pack.md`).

## Attack lenses (P5 — the tension axes)

Three attackers, one lens each, **pairwise tensioned on the `attack-vector` axis**
(`anti-bias-vector-composition`; gate-checked by `check-tension` before the human confirm).
The lenses specialize the `review` skill's established set to the spec family:

| # | lens | what it attacks in a spec | bias it carries (exposed by the others) |
|---|------|----------------------------|------------------------------------------|
| A1 | **fidelity / governance** | Concept Registry typed against DS-D1 meta-types; Feature-Concept-Graph edges against DS-D2 / `RELATIONSHIPS.md` canonical names; SPEC governance thresholds (line/row limits → `capabilities/` split); required sections present | accepts a structure as legitimate because the *format permits it* — A2/A3 judge by whether the pointer resolves / the operator can fill it |
| A2 | **reference-integrity / mechanics** | every cross-doc link and `#anchor` resolves; every Concept Registry ID is unique and is actually defined in the aspect doc it cites; Feature-Concept-Graph edge endpoints exist in the registry; no double-owned concept | accepts that if a link *looks* right it resolves — A1 exposes semantic mistyping behind a resolving link; A3 exposes un-fillability |
| A3 | **operability / abuse-gaming** | can an operator fill the family end-to-end without inventing steps; can the downstream consumers (spec→test derivation, doc→metrics, registry sync — see template `README.md`) actually consume it; can the format be satisfied **in letter while hollow** (placeholder `{tokens}` left, empty capability tables, registry IDs with no defining body) | accepts the author's self-description of completeness — A1/A2 hold it to law and to literal resolution |

A group of 3 attackers spreads 3 distinct lenses (≥ 2 required); `robot_talks: true` is
**recommended** so each attacker confronts the others along the lens tension before the
group returns (collapse detection per P14 → the synthesizer must receive each attacker's
**initial and final** positions).

## Canonical shape (review chassis, v0.6.0)

```
attackers ──sequential──▶ synthesizer ◀──zig-zag──▶ verifiers ──sequential──▶ coverage-auditor
    ▲                          │
    └┄┄┄┄┄┄┄┄┄feedback┄┄┄┄┄┄┄┄┄┘   (conditional — P6, only if material may be missing)
```

| group | role | n | tension axis (`anti_bias`) |
|-------|------|---|-----------------------------|
| `attackers` | `explorer` ×3, `robot_talks: true` | 3 | `attack-vector` (governance/fidelity vs reference-integrity/mechanics vs operability/abuse) |
| `synthesizer` | `writer` ×1 | 1 | — (single writer; no tension) |
| `verifiers` | `skeptic` ×2 | 2 | `methodology` / `source-corpus` (deductive against DomainSpec law vs empirical against the literal spec files) |
| `coverage-auditor` | `auditor` ×1 | 1 | — (single auditor; the natural dedicated `final_approver`, P12) |

- **`anti_bias_global`** is **required** (≥ 2 fan-out groups): *attack-vector spread on the
  attack composed with a source-corpus split on verification (DomainSpec governing law vs the
  literal spec files)*.
- **`final_approver`: `coverage-auditor`** — a dedicated approver that does no other work
  (P12); it fires the **zero-findings red flag** if all attackers returned nothing, and
  accepts/rejects the change-request list. (When no coverage-auditor group is declared and
  `final_approver` is `parent`, `parent` fires the flag instead — `review` skill, Outputs.)
- **`max_loops`** default **1**; raise to **2** only to re-run the same chain after fixes are
  applied (owner's call — applying change requests is a follow-up act, not part of the review).

## Verification discipline (P10 — claim ≤ proof)

Verifiers refute on two independent corpora in zig-zag with the synthesizer
(`loop_cap: 2`; a verifier turn raising no objection terminates the exchange):

- **V1 deductive** — does DomainSpec law (`arcanum/definitions/DEFINITIONS.md` DS-D1/DS-D2,
  `RELATIONSHIPS.md`, the template's own governance notes) *actually require* what the
  finding claims? Drop findings that hold the spec to a standard it never adopts.
- **V2 empirical** — open the literal spec files and resolve every cited link/anchor on
  disk. Drop findings that misquote, or that the files already satisfy / contradict.

A finding either verifier refutes is **dropped, not softened**.

## Outputs (review flavor, P9)

Everything lands in `working_folder` (a docs path; **never** under `vault/`):

- `attacks.md` — the collected attacker + verifier returns, verbatim.
- `findings.md` — per-document section → table `| # | file | evidence | severity | proposed fix |`
  → per-document verdict **KEEP / FIX** (FIX iff ≥ 1 surviving CRITICAL or MAJOR) → a closing
  change-request list ordered by severity. Every surviving finding **quotes the spec** and
  **cites the attack return** it came from.
- **`docs/features/{feature}/SPEC-REVIEW-REPORT.md`** — the **gate artifact** the lifecycle
  reads. A short report next to `SPEC.md` carrying one `Verdict: PASS | FLAG | BLOCK` line
  (house shape, mirrors `ALIGNMENT-REPORT.md`) + the change-request list. This — not a ledger
  row — is what the pipeline Step-4b checkpoint and the `domainspec-spec-feature` soft-gate
  consume, so the signal is immune to the two-ledger resolution fork.

Severity taxonomy (`review` house): **CRITICAL** (breaks the system / corrupts the registry /
contradicts DomainSpec law) · **MAJOR** (functional gap, doc-vs-doc drift, load-bearing
omission) · **MINOR** (wording, stale pointer). The dispatch **closes `resolved`** once the
`coverage-auditor` accepts the change-request list — **FIX verdicts are deliverables**, not
non-resolution.

## Lifecycle (router §3 — unchanged)

1. **Propose** — fill the dispatch sheet from this recipe; run the **`check-tension` gate**
   (two independent infra agents verify the `attackers` and `verifiers` groups against
   Tests 1–4). Only **both PASS** reaches the human.
2. **Confirm** — the human's explicit affirmative. Nothing persists before it.
3. **Register + run** — append the dispatch row (`register-dispatch`), schedule groups by
   dependency, run attackers read-only over the spec corpus.
4. **Close** — report `exit_reason` + `agents_spawned` in chat and in `findings.md`; append
   the close row.

## Wiring into the lifecycle

The obligation is split into a **human-run producer** and a **deterministic consumer** so the
single human-gate rule is never violated (the lifecycle must **read** the review's verdict, not
**fire** the review):

- **Producer (human-gated).** The review runs the only legal way — `domainspec-subagents-strategy`
  → propose → `check-tension` → human confirm → run → register. Target = the authored
  `docs/features/{feature}/` spec family. Deliverable = `SPEC-REVIEW-REPORT.md` (verdict line) +
  the registered close row (R-SDR-5, in the feature repo's ledger).
- **Consumer (deterministic, warn-only today).** Two read-only checkpoints, no auto-dispatch:
  - `domainspec-spec-feature` **step 10** — soft recommendation on the direct-authoring path
    (names the report + the `spec_review_waived` waiver).
  - `domainspec-pipeline` **Step 4b** — the implement choke point that catches every path to
    spec-derived code; reads the `SPEC-REVIEW-REPORT.md` verdict, tiers by Step-1 complexity,
    and recommends-but-proceeds (advisory). This *is* the R-SDR-1 validator.
- **No arcanum change.** `invoke` stays a pure authoring front door; the review never leaks into
  the public submodule.
- **Bootstrap note.** The first concrete run (the `domainspec-spec` **template** review,
  2026-06-16) was the evidence run that satisfied promotion prerequisite (a); the standing
  wiring above targets **authored feature specs**, not the templates.

## Pointers (single owners — this doc re-decides nothing)

- **Universal law / lifecycle / invariants:** `skills/domainspec-subagents-strategy/SKILL.md`
  (router) → `constitution/subagents-strategy-constitution-proposal.md` (§4 invariants, §5 fields).
- **Review-type judgment** (lenses, severity, verification, findings shape):
  `skills/review/SKILL.md`.
- **Sheet/record form** (field tables, enums, appender, close row): `skills/register-dispatch/SKILL.md`.
- **Anti-bias design + gate:** `.claude/skills/anti-bias-vector-composition/SKILL.md` (design)
  and `.claude/skills/check-tension/SKILL.md` (the init-time gate).
- **Agent names:** `implementation/domainspec/telemetry/agents/agent-pool.yaml`.
- **Spec template family under review:** `arcanum/spells/invoke/templates/domainspec-spec/`.
</content>
