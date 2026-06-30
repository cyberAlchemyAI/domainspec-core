---
tags: [inventory, cav2, authority, constitution-governance, constitution-namespace, saturn, machine-map, claim-le-proof, build-from-owned]
node_type: synthesis
is_session: false
layer: governance, architecture
nature: reference
status: candidate
created: 2026-06-29
boundary: INTERNAL — discusses cav2 + Saturn (private); do NOT copy into public arcanum/
dispatch_id: 2026-06-29-constitution-namespaces-axioms-role
dispatch_type: research
working_folder: inline (conversational synthesis + one read-only cross-wiring sweep; dispatch_id is a trace handle, not a registered working_folder)
sources:
  - implementation/domainspec/AXIOMS.md
  - implementation/domainspec/CONSTITUTION.md
  - research/projects/domainspec/definitions/CONSTITUTION.md
  - cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md
  - ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md
  - .arcanum/inventory/entries/machine-map-and-moat-synthesis.md
  - cyberAlchemy-v2/development/research/2026-06-25-cav2-authority-synthesis/findings.md
---

# Constitution namespaces + the AXIOMS→CONSTITUTION governance unit's system role

Candidate Inventory synthesis (**promotes nothing**; owners = DomainSpec
implementation-governance + cav2 authority). Claim ≤ proof throughout. Two results:
(1) a disambiguation map of the repo's four independent "constitution" namespaces,
backed by a read-only cross-wiring sweep; (2) the importance read on the DomainSpec
`AXIOMS → CONSTITUTION` governance unit for cav2 / machine-map / saturn.

## 1. Four constitution namespaces — only DomainSpec uses bare `C#`

| Namespace | File | IDs | Role |
|---|---|---|---|
| **DomainSpec governance** | `implementation/domainspec/CONSTITUTION.md` | `C1`–`C11` | governed by AXIOMS `A1`–`A6` (sibling); each clause → a CI gate |
| **Research doc-hygiene** | `research/projects/domainspec/definitions/CONSTITUTION.md` | `RC1`–`RC3` | markdown-link discipline; unrelated to AXIOMS |
| **cav2 authority** | `cyberAlchemy-v2/authority/constitutions/` (e.g. STABLE-REPOSITORY) | `CAV2-C*`, `CAV2-VC*` | cav2 promotion/authority gates |
| **Consumer repos** | `projects/*/domainspec/CONSTITUTION.md` (body-war, whisky-doses) | own copies of `C1`–`C11` | copies, not cross-references |

**Sweep verdict (read-only audit, this session): collision is LATENT, never TRIPPED.**
No cross-wired references — every clause-ID stays inside its own tree; kodamai and the
cav2-authority-synthesis cite cav2's *own* `CAV2-C*`, correctly scoped. cav2 (`CAV2-C*`)
and research (`RC*`) are **prefixed → self-disambiguating**; only DomainSpec uses bare
`C#`, and today only `AXIOMS.md` writes it unlinked (still locally unambiguous because it
sits next to its sibling). Arcanum's `*-CONSTITUTION.md` files (SCHEMA, ARTIFACT,
MARKDOWN-LINKING…) are *named*, not `C#`-clause-numbered → no collision.

## 2. The mis-pairing correction

`AXIOMS.md` (A1–A6) governs its **sibling** `implementation/domainspec/CONSTITUTION.md`
(C1–C11), which carries an explicit `L4 Axiom` column mapping each clause back to A1–A6 —
**not** the research `definitions/CONSTITUTION.md` (RC1–RC3). The two are unrelated; pairing
AXIOMS with the research RC file is a common confusion this entry exists to kill.

## 3. AXIOMS → CONSTITUTION importance for cav2 / machine-map / saturn

**What the unit is.** DomainSpec's *implementation-governance* constitution: 6 axioms → 11
clauses → each clause bound to a CI gate (spec-as-source C1/C6, no-policy-in-adapters
C2/C7, computable signals C3/C8, observer⊥executor C4/C9, shift-left + async-prune C5/C10,
metric health C11). It is **one of the only governance artifacts with real teeth today** —
cav2 is review-mode-no-validator, Saturn is unshipped.

| Target | Governs it? | Real role | Weight |
|---|---|---|---|
| **cav2** | No | object-level S5 kept one recursion below cav2's meta-S5 (machine-map E1: two System-5s); cav2 self-governs via `CAV2-C*` | structural, not governing |
| **machine-map** | — | the object **baseline** (C1/C6 make DomainSpec measurable) + **A4 (observer⊥executor) IS the machine-map's central correction** (read-only observer, not daemon — Conant-Ashby) | high |
| **saturn** | No | the intent layer's loop-participation contract: A1 baseline-down, A3/C3/C8 signals-up, A4 = regulator-distinct, A5+C5/C10 = Saturn's inner-blocking/outer-async two-loop, C11 = health to outer loop | high intent / low live |

**Through-line:** the unit is small but load-bearing as the system's only *computable*
governance exemplar — the object baseline the machine-map builds on, the loop-contract
Saturn would consume, and deliberately **not** cav2's meta-authority. Its importance is
that it is **built and enforced** while most surrounding governance is review-mode or
roadmap. Alternatives to its computable style: cav2's review-mode owner-routed
classification (a different philosophy — DomainSpec chose computable because A3 holds
"instruction-only enforcement is insufficient"); the observe-and-mutate daemon (machine-map
explicitly refuses it).

## Connections
- [[machine-map-and-moat-synthesis]] — the VSM frame: DomainSpec=object baseline, cav2=missing
  S5, Saturn=control loop; the two-System-5s recursion boundary that makes "cav2 does not
  govern AXIOMS" precise.
- [[deterministic-validation-for-all-cav2-synthesis]] / [[fol-constitution-validation-complement-synthesis]]
  — cav2's *own* deterministic-validation program over `CAV2-C*` (the namespace the
  kodamai/fol work cites — a different constitution from this unit's C1–C11).
- [[kodamai-smithe-correctness-layer-synthesis]] — the agent⊨spec prize; same governance-vs-residue split.

## Residue
- **Open contradiction (carried, not resolved):** machine-map records AUTHORITY-MAP ("CONSTITUTION
  exists") vs GOVERNANCE-ATTENUATION ("System-5 missing"). Whether *this unit* already fills
  the cav2 System-5 slot is a live cav2-owner question.
- **Saturn is intended-not-shipped** (SATURN-LAYER-MAP §4 + machine-map) — the unit's "Saturn
  role" is aspirational alignment; today it governs only DomainSpec's own implementation.
- **Disambiguation note proposed-not-applied:** a one-block header note in `AXIOMS.md` linking
  bare `C#` to the sibling `CONSTITUTION.md` was proposed to close the latent collision; not
  yet applied (owner approval pending).

## Boundary
Inventory candidate read-model. Promotes nothing. INTERNAL — discusses cav2 + Saturn (private).
