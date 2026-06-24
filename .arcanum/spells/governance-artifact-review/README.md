# Spell: governance-artifact-review

Status: **candidate** (n=1 evidence — see Promotion Block)
Scope: repository-local (domainspec-core)
Owner: spellcraft

## Canonical ID

`governance-artifact-review`

## Aliases

- `promotion-readiness-review`
- `formal-governance-review`

## Purpose

Red-team a set of **staged governance / definition / inventory artifacts before
promotion** and return **verified, severity-ranked change requests routed to the
owning governance gate**. It composes the existing review machinery into a fixed,
repeatable recipe so each governance review does not re-derive its lens-set,
baseline-binding, or verification discipline. The spell **never promotes or
applies changes** — it produces change requests; the owning gate applies them.

Derived (2026-06-23) by reflecting on the run that red-teamed the
authority-lifecycle candidates and surfaced that the staged invariant collapsed
into the existing Authority Rule.

## Trigger conditions

- One or more artifacts are **staged as candidates** (definition candidate,
  constitution-rule draft, discipline candidate, inventory synthesis/cards,
  source-cluster entry) **before an owner promotion decision**, AND
- at least one **review trigger (P1)** holds (synthesis ≥3 sources, or
  context-protection, or isolation) so a dispatch is warranted over inline work.

Do **not** use for: a single trivial artifact (review inline), or after promotion
(use the owning gate's own drift audit).

## Required sigils (referenced, not copied)

- [`domainspec-subagents-strategy`](../../../.claude/skills/domainspec-subagents-strategy/SKILL.md) — router; lifecycle, gates, `final_approver`, `exit_reason`.
- [`review`](../../../.claude/skills/review/SKILL.md) — type skill; attack lenses, severity taxonomy, verification discipline, change-request shape (inline by default).
- [`check-tension`](../../../.claude/skills/check-tension/SKILL.md) — init-time anti-bias gate over the reviewer group.
- [`register-dispatch`](../../../.claude/skills/register-dispatch/SKILL.md) — dispatch + close rows in the ledger.

## Optional sigils

- The **owning gate** that consumes the change requests — one or more of
  [`definitions-governance`](../../../.claude/skills/definitions-governance/SKILL.md),
  [`constitution-governance`](../../../.claude/skills/constitution-governance/SKILL.md),
  [`discipline-governance`](../../../.claude/skills/discipline-governance/SKILL.md).
- [`inventory`](../../../.claude/skills/inventory/SKILL.md) — to capture the review as evidence-cards + synthesis.

## Prerequisites

- Target artifacts exist and are candidate-status (not yet promoted).
- The **owning baseline doc(s)** exist for the vacuity lens — e.g.
  `cyberAlchemy-v2/authority/promotion-policy.md`, `.../AUTHORITY-MODEL.md`, or
  the relevant canonical constitution.

## Shared state

- `targets` — the staged artifact set under review.
- `owning_gate` — which governance gate will consume the change requests.
- `baseline_docs` — the owning law the vacuity lens tests against.
- `change_requests` — the verified, severity-ranked output list.

## Execution phases

| # | Phase | Input | Output | Gate | Failure policy |
|---|---|---|---|---|---|
| 1 | **Scope** | trigger + targets | `targets`, `owning_gate`, `baseline_docs` resolved | targets are candidate-status | if any target is already promoted → route to the owning gate's drift audit instead, not this spell |
| 2 | **Propose + tension-gate** | targets | review sheet with the **fixed 3-lens reviewer group** + `working_folder: inline` | **check-tension** must PASS (both agents) | reprove or disagree → revise sheet, re-gate |
| 3 | **Confirm** | gated sheet | frozen sheet | explicit human affirmative | silence/question ≠ confirm; do not run |
| 4 | **Register + run** | frozen sheet | dispatch row + 3 reviewer returns | reviewers run in parallel | a reviewer error → partial group result, told to verifier |
| 5 | **Verify (P8)** | reviewer returns | findings checked against actual files/baseline | each finding verified before it is reported | unverifiable finding → **dropped**, not reported |
| 6 | **Synthesize + route** | verified findings | severity-ranked deduped `change_requests` + owning-gate routing note (+ optional inventory capture) | claim ≤ proof | none survive → `resolved` (clean) |
| 7 | **Close** | outcome | `exit_reason` + `agents_spawned` in chat + close row | two ledger appends | — |

### The fixed reviewer set (the spell's core contract — attack-vector tensioned)

1. **claim>proof / overclaim** — any artifact asserting more than its source sustains (false "proved"/"owned"/binding labels).
2. **contradiction / coherence** — cross-artifact drift + internal inconsistency; do the cited cards still back the claims?
3. **vacuity / collapse-test — MUST be bound to `baseline_docs`.** Does the candidate add anything the owning law does not already give, or is it a re-skin? *(This binding is the load-bearing lesson: an unbound vacuity lens is under-evidenced — it is what caught the authority-lifecycle invariant collapsing into the Authority Rule.)*

## Handoff artifacts

- `change_requests` — inline severity-ranked verified list (review is inline by default).
- routing note naming the **owning gate** for each change request.
- optional: inventory evidence-cards + synthesis capturing the review.

## Gates

- **check-tension** (phase 2, mandatory — reviewer group is n≥2 evaluate).
- **human confirm** (phase 3, the single human gate).
- **P8 verification** (phase 5 — no finding is reported unverified).
- **owner gate** (phase 6 — the spell routes, never applies).

## Failure policy

- check-tension reprove/disagree → back to strategist (no human gate reached).
- reviewer error → partial group result, surfaced to the verifier and human.
- finding fails verification → dropped (claim ≤ proof).
- target already promoted → out of scope; route to the owning drift audit.

## Local customization

- `baseline_docs` for the vacuity lens (per target domain).
- `owning_gate` (definitions / constitution / discipline).
- inline (default) vs persisted `working_folder`.
- whether to capture via `inventory`.

## Observability

`.arcanum/observability/` exists — emit spell-level telemetry: phases attempted,
sigils invoked, gates passed/blocked (esp. check-tension reproves), reviewer
count, findings raised vs verified vs dropped, change requests routed, owning
gate, `exit_reason`, user corrections.

## Output contract

```markdown
## Governance Artifact Review Result
- Targets: <artifact paths>
- Owning gate(s): <definitions | constitution | discipline>
- Reviewers: claim>proof, contradiction, vacuity(baseline-bound)
- check-tension: pass | reproved
- Findings: <raised> raised / <verified> verified / <dropped> dropped
- Change requests (severity-ranked): <list, inline>
- exit_reason: resolved | dissent_irreconcilable | user_abort | error
- Routed to: <gate(s)>
```

## Promotion Block (claim ≤ proof)

This spell is **candidate** on **n=1** evidence (one successful run, 2026-06-23).
Promotion to a reusable/library spell is **blocked** until:

1. an experiment harness is initialized via `experiment-harness` (`--profile spellcraft`) with low/medium/complex examples; AND
2. ≥3–5 real governance reviews run through it (reflection-policy usage threshold), with telemetry showing the fixed lens-set and baseline-bound vacuity lens hold across domains.

Until then: usable as a documented local recipe, not promoted.
