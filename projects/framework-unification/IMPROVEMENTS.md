---
tags: [framework-unification, improvements, recommendations, residue, blockers]
node_type: discovery
is_session: false
layer: architecture
nature: explanatory
status: draft
version: 0.1.0
last_updated: 2026-06-15
created_by: victorboscaro@gmail.com
---

# Framework Unification — Improvements

> **What this node is.** A prioritized list of improvements for this workspace and its
> sibling Lean repo (`../../../domainspec-lean-formalization`), authored from a read-only
> exploration of both. It is a recommendation map, **not** a build order and **not** a claim
> that any improvement has been applied. Each item carries its provenance and verification
> status; the cross-repo bet carries its collapse-test inline (per the program's keystone rule).

This doc distills an exploration sweep of both repos against the workspace plan recorded in
[`README.md`](README.md) and [`discovery/discovery.md`](discovery/discovery.md). It does not
ratify any open decision; it only sharpens *what to do next and in what order*.

---

## Objective

Give the owner an ordered, honestly-typed list of improvements — separating what is **verified
by reading the project's own docs** from what is **relayed and still unverified** — so the next
move targets the real seam (the residue-type blocker), not the workspace headline.

## Context — provenance and verification status

Two tiers of claim appear below. The tier is marked on every item.

- **[verified-here]** — confirmed by directly reading this project's docs
  ([`README.md`](README.md), [`discovery/discovery.md`](discovery/discovery.md)). The three
  critical blockers, OQ-1…OQ-5, and the aspirational status of Lean/PermGuard are in this tier.
- **[relayed-unverified]** — surfaced by a subagent reading the **sibling Lean repo** and **not
  re-confirmed in this session**. Treat as a lead to check, never as an asserted fact. Subset
  rule applies: do not let these harden into claims downstream until re-verified.

---

## A. framework-unification (this workspace)

### A-1. Re-order the phase plan: attack the residue-type blocker *before* paired-views — [verified-here]
The plan is `research → discovery → paired-views`, and paired-views targets the two duplicated
owners (OQ-1, OQ-2). But what actually gates implementation is the **residue-type blocker**
(`cyber-alchemy-lean-fusion/DESIGN.md §7`): *what type does artifact-level residue carry such
that it fires the gate mechanically?* That blocker is suspected **identical** to the
`obligation_id` bridge B-1 (OQ-2). Resolving it collapses one full blocker and half of
`domainspec-language`'s B-1 at once.
- **Recommendation:** spin a dedicated research dispatch on OQ-2 *now*, in parallel with
  paired-views — do not wait for owners to be assigned. It is the highest-leverage single move.

### A-2. Re-verify the cross-repo claims before any ratify — [verified-here]
`v0.5.2`-proposal, `R30` verbatim, and `P-SS-9` are **relayed** from an agent reading the
sibling domainspec repo (recorded as such in `dispatch-composition-attack/findings.md §3` and
the discovery's source-dispatch note). "Fits now ≠ verified now."
- **Recommendation:** re-confirm the three texts in their owning tree before OQ-1's typed-DAG
  ratification. Until then, mark them `relayed` wherever they are cited.

### A-3. Quarantine aspiration from architecture with one linkable scope note — [verified-here]
`discovery.md` already states it honestly (OQ-4): the Lean backing certifies the **formal
residue object, not Arcanum runs**; PermGuard's binary exists but is **unwired** and is a
verified *decision core*, not a security guarantee. The risk is downstream docs inflating these
into guarantees.
- **Recommendation:** add a single `SCOPE.md` (or a pinned section) that every view links to,
  stating the aspirational boundary once. Cheaper than repeating the caveat per-doc and harder
  to lose.

### A-4. Decide the `arcanum` submodule question explicitly — [verified-here]
The engine is mapped **by description**, not source (OQ-5); the `arcanum` submodule is
uninitialized and the Lean repo was outside the read corpus.
- **Recommendation:** make OQ-5 a gate on paired-views: if paired-views needs real engine code,
  `make bootstrap` first; if not, record that paired-views is description-only and accept the
  seam. Do not enter paired-views with this undecided.

### A-5. Close the observability producer gap as the first build after owners — [verified-here]
`.arcanum/observability/signals/sigil-invocations.jsonl` has a **writer but no producer**
(OQ-3) — the one concrete unblock of the feedback loop. The skill-detection coverage gap
(`.claude/skills` invisible to the producer) argues for driving the producer from the
envelope/record, not from skill detection.
- **Recommendation:** scope producer-from-record as the first implementation task once OQ-1/OQ-2
  owners exist; note the skill-detection limitation in that scope.

---

## B. domainspec-lean-formalization (sibling repo) — [relayed-unverified unless noted]

These came from a subagent reading the Lean repo and are **not** re-confirmed here. Listed so
the owner can check them, not so they can be cited.

### B-1. Commit the clean uncommitted work — [relayed-unverified]
Reported: three new sorry-free `.lean` files (`BridgeKernelPairEssImage`, `ChargeFluxWeighted`,
`CollapseEmergence`), four 2026-06-15 session logs, and a `ResidueCompositionLaw.lean` cleanup
are untracked/uncommitted.
- **Recommendation:** verify sorry-free status (`lake build` + axiom check) and commit. Until
  verified, "sorry-free" stays a lead, not a claim.

### B-2. Resolve the narrative↔proof tension on Gibbs — [relayed-unverified]
Reported: `README` describes Gibbs as "closed" while `PRIZES.md` marks the **canonical instance**
as open. If true, this is a direct subset-rule violation in the repo most committed to that rule.
- **Recommendation:** run the dirigida check `README ↔ PRIZES`; if the tension is real, demote
  the README line to conditional language. **Cheapest high-value action across both repos.**

### B-3. Surface the new files and confirm the ω-self-similar framing reads OPEN — [relayed-unverified]
Reported: the three new files are undocumented in `README`/`LEAN-ARCHITECTURE`, and the
30+-file ω-self-similarity cluster is structurally OPEN.
- **Recommendation:** add 3-line annotations for the new files; audit public docs so
  ω-self-similarity reads OPEN, not closed.

---

## C. The cross-repo bet (keystone candidate, with collapse-test)

The §7 residue-type blocker here is **exactly** the object the Lean repo has been building
(`Residue.lean`, `UniversalResidueFunctor.lean`, the charge-flux work). Two outcomes are worth
one focused dispatch:

1. the Lean repo **already carries** the type that fires the gate, and nobody has bridged it; or
2. the gate's "fires mechanically" requirement **sharpens** what the Lean residue type still
   owes (non-vacuity on the instance, not just functorial non-vacuity).

- **Collapse-test (binds the headline, per the keystone rule):** if `obligation_id` bridge B-1
  is *already* the residue-type and that identity is trivially checkable by reading the two
  artifacts side by side, this bet collapses to zero contribution and becomes a citation-only
  note. The dispatch must be prepared to return exactly that verdict.

---

## What this doc does NOT claim

- Does **not** assert any [relayed-unverified] item (B-1…B-3) is true — they are leads to check.
- Does **not** ratify the `v0.5.2` typed-DAG, assign any owner, or resolve OQ-1…OQ-5.
- Does **not** claim residue-type ≡ `obligation_id` B-1 — it recommends *testing* the identity.
- Does **not** treat the Lean proofs as certifying Arcanum correctness, nor PermGuard as a
  security guarantee.

---

## Open Questions

> Per the workspace convention ([`SCOPE.md`](SCOPE.md) §3), this doc's own open items (distinct
> from the OQ-1…OQ-5 it re-prioritizes).

- **OQ-i. Sequence: which improvement goes first?** — **Context:** A-1 (residue-type) is now
  reframed as a Lean-owned, deferred integration point ([`SCOPE.md`](SCOPE.md) §1), so the
  highest-leverage *useful* moves become A-3 (this scope note, done) and the OQ-3 observability
  producer. **Recommendation:** sequence A-3 → observability producer → paired-views.
  **Status:** OPEN.
- **OQ-ii. When do the [relayed-unverified] items get checked?** — **Context:** B-1…B-3 are leads
  from the sibling Lean repo, not re-confirmed. **Recommendation:** run the cheap dirigida check
  on B-2 (Gibbs `README ↔ PRIZES`) before any commit there; treat B-1/B-3 as leads until verified.
  **Status:** OPEN.

## Connections

| Document | Type | Description |
|---|---|---|
| [SCOPE.md](SCOPE.md) | `relates-to` | Scope/conventions; §1 reframes A-1/C (residue-type = Lean-owned, deferred). |
| [discovery/discovery.md](discovery/discovery.md) | `derives-from` | The open questions (OQ-1…OQ-5) these improvements re-prioritize. |
| [README.md](README.md) | `cites` | Workspace plan and open-decisions table being re-ordered. |
| [layers/cyber-alchemy-lean-fusion/DESIGN.md](layers/cyber-alchemy-lean-fusion/DESIGN.md) | `cites` | §7 residue-type blocker — the keystone bet's anchor. |
| `../../../domainspec-lean-formalization` | `relates-to` | Sibling Lean repo; source of all [relayed-unverified] items and the cross-repo bet. |
