---
tags: [subagents, dispatch, review, constitution, specs, domainspec, governance]
node_type: constitution
is_session: false
layer: architecture
nature: procedural
status: draft
version: 0.1.0-proposal
last_updated: 2026-06-16
governs: the DomainSpec spec document family produced in the specs development phase
subordinate_to: constitution/subagents-strategy-constitution-proposal.md@v0.6.1-proposal
reference_recipe: strategies/specs-development-review.md@v0.1.0
type_skill: skills/review/SKILL.md
---

# Specs-Development Review Constitution — PROPOSAL

A **modular, artifact-type-scoped** constitution. It records one obligation: a DomainSpec
spec document family produced in the **specs development phase** must be red-teamed by a
`review` dispatch covering **all** its documents before that spec is treated as a stable
downstream interface.

It is **not** new dispatch law. It **specializes** the subagents-strategy constitution
(`subordinate_to` above) for one artifact type, and binds the `review` type skill's
judgment. The *how* — the canonical chassis, the three tensioned lenses, the agent design —
lives in the reference recipe (`strategies/specs-development-review.md`); this constitution
owns only the **obligation and its form**, so the recipe can evolve without re-ratifying law.

## §1 — Scope & authority

- **Scope.** Spec artifacts of the DomainSpec spec template family
  (`arcanum/spells/invoke/templates/domainspec-spec/`): `SPEC.md` and every per-aspect doc
  it emits (`operations.md` · `queries.md` · `interfaces.md` · `states.md` · `events.md` ·
  `mappings.md`, and the bundle/pack docs). Nothing else.
- **Owner.** The dispatch-governance owner (the human strategist).
- **Authority.** Subordinate to `subagents-strategy-constitution-proposal.md` (v0.6.x) and
  to the `review` type skill. It may **add** an obligation within its scope; it may **not**
  relax any universal invariant of the parent constitution, and (R-SDR-6) it adds **no**
  human gate beyond the parent's single entry confirm.

## §2 — Selection predicate (when this constitution is selected)

Select this constitution for a task **iff both** hold:

1. the artifact under work is (or will be) a DomainSpec spec document family per §1, **and**
2. the task is in, or is closing, the **specs development phase** (a `define`-mode `invoke`
   run authoring the family, or a material update to an existing family).

If either is false, do not load it — Context Builder selection alone covers narrower needs.

## §3 — Rules

Each rule carries a statement, its rationale, an example / non-example, and one validation
mode (§5). IDs are stable (`R-SDR-n`).

### R-SDR-1 — Mandatory review before spec-derived consumption
A spec document family in scope **MUST** be the target of a `dispatch_type: review`
**before** any downstream step **that derives from the spec** consumes it as settled —
**stories, test derivation, implementation, registry sync**.
- *Anchor (corrected).* The enforcement anchor is **spec → implementation**, *not*
  "spec → plan". In `domainspec-pipeline` the order is `plan → spec` (Step 1 Plan, Step 2
  Spec), so "plan" runs *before* the spec exists and cannot be the gate. The reliable
  choke point that every path to spec-derived code passes through is the **implement
  step** (and the spec-authoring soft-gate for the direct-authoring path).
- *Rationale.* The aspect docs + Concept Registry are the **stable interface** downstream
  DomainSpec capabilities derive from; an un-red-teamed spec propagates its defects into
  every derivation.
- *Example.* `domainspec-spec-feature` finishes `SPEC.md` + aspect docs → a review is
  proposed, human-gated, run, closed `resolved`, emitting
  `docs/features/{feature}/SPEC-REVIEW-REPORT.md` → the pipeline's Step-4b checkpoint
  reads a non-`BLOCK` verdict before `domainspec-implement` runs.
- *Non-example.* Jumping from a freshly authored spec straight to implementation with no
  `SPEC-REVIEW-REPORT.md` and no waiver. **Violation** (warn-only today; see §6).
- *No auto-dispatch.* Neither the pipeline nor `domainspec-spec-feature` may **fire** the
  review — a governed dispatch needs an explicit human confirm + check-tension pass first
  (R-SDR-6 / parent single-gate). They **recommend** it and **read its artifact**.
- *Validation:* the **deterministic check is the `SPEC-REVIEW-REPORT.md` verdict artifact**
  (existence + non-`BLOCK` verdict, or a `spec_review_waived` waiver), mirroring how
  `ALIGNMENT-REPORT.md` is consumed. Advisory (warn-only) today; promotion to a hard
  `block` is the owner flip in §6. The report artifact — not a ledger row — is the gate
  signal, so it is immune to the ledger-resolution fork (the close row remains the R-SDR-5
  audit record, registered in the **feature repo's** ledger via `$CLAUDE_PROJECT_DIR`).

### R-SDR-2 — Whole-corpus coverage (no sampling)
The review **MUST** cover **all** created documents of the family. Attackers read the whole
corpus (full reading), differing by lens — **never** by partitioning the files.
- *Rationale.* Spec defects are cross-document (a registry ID defined nowhere, an aspect
  link that dangles); a per-file partition cannot see them.
- *Non-example.* Reviewing only `SPEC.md` and skipping the aspect docs it links. **Violation.**
- *Validation:* `review` (the coverage-auditor verifies every target was attacked from every
  declared lens and fires the zero-findings red flag).

### R-SDR-3 — Tensioned attack lenses, gate-passed
The attacker group **MUST** spread **≥ 2** distinct review attack-lenses on the
`attack-vector` axis, **pairwise tensioned**, and **MUST** pass the `check-tension` gate
(Tests 1–4) before the human confirm.
- *Rationale.* One lens (or N untensioned clones) produces correlated blind spots reported
  with false confidence; structural opposition cancels the bias (P5).
- *Example.* fidelity/governance × reference-integrity × operability/abuse, each attacker
  one lens, gate PASS by two independent agents.
- *Non-example.* Three "find problems in the spec" attackers, no named axis. **Violation
  (gate REJECT).**
- *Validation:* `hybrid` (deterministic `check-tension` Tests 1–4 + review of the lens set).

### R-SDR-4 — Verified change requests, claim ≤ proof
Every surviving finding **MUST** quote the spec and cite the attack return it came from; a
finding a verifier refutes is **dropped, not softened**. The deliverable is `findings.md`
(cited change requests, per-document KEEP/FIX verdict) plus `attacks.md` (verbatim returns)
in the dispatch `working_folder`.
- *Rationale.* P10 — an over-stated spec finding is itself a defect; demote, never inflate.
- *Non-example.* A `findings.md` row with no quote and no attacker citation. **Violation.**
- *Validation:* `review` (verifiers refute; coverage-auditor confirms drops were real drops).

### R-SDR-5 — Registered, one row
The review dispatch **MUST** be recorded in the ledger — one dispatch row at dispatch, one
close row at termination — per `register-dispatch` (append-only).
- *Rationale.* Auditability of which spec was reviewed, by what design, with what outcome.
- *Validation:* `deterministic` (the append-only hook + the appender's schema-v0.6.0
  validation enforce row shape and the two-append rule).

### R-SDR-6 — One gate only
This constitution introduces **no** additional human gate. The single human gate is the
parent constitution's **entry confirm**; this rule exists to forbid a second sign-off
sneaking in via the spec-phase.
- *Rationale.* Gate proliferation defeats the lean-governance intent of the parent.
- *Validation:* `review`.

## §4 — Composition & precedence

Composes **narrowest-scope-first** (constitution-governance composition rules):

1. a task-specific spec-review pack (if one is generated),
2. **this** artifact-type constitution,
3. the `review` type skill's judgment,
4. the subagents-strategy framework constitution (v0.6.x),
5. repository defaults.

On conflict with the framework constitution: **preserve both rules**; this (narrower)
constitution governs *within its scope* but **never** overrides a universal invariant or the
single-gate rule of the parent — those are not overridable here. Any precedence conflict that
is not a clean specialization is a **blocker** → route through `decision-gate`, not a silent
newest-wins.

## §5 — Validation surface

| Rule | Mode | Adapter / check | Status |
|------|------|-----------------|--------|
| R-SDR-1 | `deterministic` (warn-only) | `SPEC-REVIEW-REPORT.md` verdict check at `domainspec-pipeline` Step-4b (implement choke point) + the `domainspec-spec-feature` step-10 soft-gate; `spec_review_waived` frontmatter waiver | active (advisory); flip to `block` per §6 |
| R-SDR-2 | `review` | coverage-auditor (whole-corpus + zero-findings flag) | active |
| R-SDR-3 | `hybrid` | `check-tension` Tests 1–4 (deterministic gate) + lens-set review | active |
| R-SDR-4 | `review` | verifiers (zig-zag) + coverage-auditor acceptance | active |
| R-SDR-5 | `deterministic` | append-only hook + `append-dispatch.cjs` schema-v0.6.0 validation | active |
| R-SDR-6 | `review` | human confirm; no second gate present | active |

A validator added for any rule **MUST** cite that rule and **MUST NOT** be broader than the
rule's scope (§1).

## §6 — Promotion boundary, retirement & split triggers

- **Promotion.** This constitution is a **PROPOSAL** (`status: draft`). Both prerequisites
  for promoting R-SDR-1 to a hard `block`-severity gate are now **met**: (a) the first
  review dispatch ran and closed `resolved` as evidence (the `domainspec-spec` template
  review, 2026-06-16), and (b) the deterministic validator exists — the
  `SPEC-REVIEW-REPORT.md` verdict check wired at pipeline Step-4b and the
  `domainspec-spec-feature` soft-gate. R-SDR-1 is therefore held at **warn-only by current
  owner decision**, not by missing prerequisites; flipping the Step-4b `BLOCK` branch from
  "recommend + proceed" to "halt" is now a one-line owner act (`promote`).
- **Retirement.** Retire if the obligation is absorbed into the parent constitution or the
  spec template family is discontinued.
- **Split trigger.** If this file accumulates rules unrelated to the spec-phase review
  obligation, split them out — it must not become a catch-all.

## §7 — Pointers (single owners — re-decides nothing)

- **Parent law / invariants / lifecycle:** `constitution/subagents-strategy-constitution-proposal.md`
  via the router `skills/domainspec-subagents-strategy/SKILL.md`.
- **Review-type judgment** (lenses, severity, verification, findings shape): `skills/review/SKILL.md`.
- **Reference recipe** (the dispatch shape that satisfies these rules): `strategies/specs-development-review.md`.
- **Sheet/record form:** `skills/register-dispatch/SKILL.md`.
- **Anti-bias gate:** `.claude/skills/check-tension/SKILL.md` (enforces R-SDR-3).
- **Spec family under governance:** `arcanum/spells/invoke/templates/domainspec-spec/`.
</content>
