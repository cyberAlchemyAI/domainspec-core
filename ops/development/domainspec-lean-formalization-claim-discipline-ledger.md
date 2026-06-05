# DomainSpec Lean Formalization Claim Discipline Ledger

Date: 2026-06-01
Dispatch: `domainspec-lean-formalization-research-20260601`

## Governing Rule

Claim text must stay inside proof, theorem, audit, or cited-source evidence.

Evidence:

- `domainspec-lean-formalization/CLAUDE.md:13-19` says to stop and question when a claim outruns proof, novelty is unverified, or the underlying goal is unclear.
- `domainspec-lean-formalization/CLAUDE.md:25-32` says to cite rather than rediscover, and to keep claim strength within Lean proof or cited theorem.
- `domainspec-lean-formalization/CLAUDE.md:41-60` routes bridge writing, conjectures, audits, and precedent search through explicit workflows.

## Local Mechanical Checks

Read-only text checks performed in parent lane:

- Top-level root Lean files: 144.
- Top-level `lean-formalization/files/new/*.lean` files: 29.
- Strict active-sorry scan: 30 active `sorry` lines in 8 files.

Strict active-sorry files:

- `lean-formalization/AsymmetricTowerHRigidity.lean`
- `lean-formalization/AsymmetricTowerHInfra.lean`
- `lean-formalization/files/new/HilleYosida.lean`
- `lean-formalization/files/new/Resolvent.lean`
- `lean-formalization/files/new/Generator.lean`
- `lean-formalization/files/new/Uniqueness.lean`
- `lean-formalization/BridgeEssSurj.lean`
- `lean-formalization/P1Positive.lean`

Important caveat: this is a text scan, not a full Lake build or dependency-cone proof audit.

## Proved Or Source-Level Claims

Use this label when a claim has Lean source support and no active `sorry` was found in the sampled theorem body. A full proof-status claim still needs build plus dependency-cone sorry/axiom audit.

Evidence examples:

- M5 adjunction triple: `lean-formalization/DomainSpec.lean:140`.
- T0' C1/C2/C3 and `GeneralSchema` relative to stated assumptions: `lean-formalization/DomainSpec.lean:159`.
- Reflection-tower persistence: `lean-formalization/ReflectionTower.lean:349`.
- Anchored tower M6 refutation packaging: `lean-formalization/ReflectionTowerAnchored.lean:422`.
- Bicyclic faithful-but-leaky Lan-unit counterexample: `lean-formalization/Bicyclic.lean:51`.
- M6 refutation: `lean-formalization/M6Counter.lean:145`.
- M2 unrestricted refutation: `lean-formalization/M2Counter.lean:51`.
- Conditional bridge adjunction: `lean-formalization/BridgeAdjunction.lean:21`.
- Discrete second-law surface: `lean-formalization/SecondLawDiscrete.lean:216`.

Safe wording: "Lean source contains theorem/counterexample support for..."

Unsafe wording: "the whole dependency cone is proof-closed" unless a build, sorry scan, and axiom audit are all current.

## Build-Evidenced Or Documented Claims

Use this label when the repository documents closure/build status but the current route did not independently re-run a successful build.

Evidence examples:

- `research/audits/closure-marks-2026-05-20/discovery.md:74` documents Bicyclic closure after a fix.
- `lean-formalization/files/lakefile.toml:1` defines many root default targets.
- `lean-formalization/files/new/lakefile.toml:1` defines a separate Lake project for `files/new`.

Current route result: Lake validation did not complete. One build attempt timed out during toolchain setup; another failed while fetching/updating Mathlib refs. Treat this as an environment/tooling blocker, not a proof failure.

## Documented Research Claims

Use this label when the claim is supported by prose research artifacts and not currently asserted as a theorem.

Evidence examples:

- Two-layer by three-axis research thesis: `research/README.md:12-15`, `research/README.md:31-35`.
- Intra-axis/inter-axis status and native DomainSpec-system conjectural status: `research/README.md:41-47`.
- Open conjectures: `research/README.md:61-67`.
- Publication split between two-layer residue paper and horizontal companion: `docs/paper.md:15-25`, `docs/paper-companion.md:27-36`.
- `research-gpt` gap-closure governance: `research-gpt/README.md:21-31`, `research-gpt/TOWER.md:41-50`.

Safe wording: "The research spine frames..."

Unsafe wording: "Lean proves the whole three-axis program."

## Conjectural Or Open Claims

Use this label for named frontier work.

Evidence examples:

- M2-restricted, M6', and M6-restricted remain open: `docs/domainspec-two-layer-framework.md:158-167`.
- DomainSpec-system-level inter-axis independence remains conjectural: `research/README.md:41-47`.
- Joint `(Delta, X)` characterization of Lan-unit faithfulness remains open: `BACKLOG.md:151-153`.
- Delta-parametric towers and IAI bridge remain open: `BACKLOG.md:155-181`.
- Full pseudofunctorial rung-3+ work is blocked on tricategory infrastructure: `BACKLOG.md:309-317`.
- System-of-towers remains open: `BACKLOG.md:333-343`.
- Continuous/RG/Landauer/Clausius physical thermodynamics remains open: `THERMODYNAMICS.md:136-153`.

Safe wording: "open frontier", "named conjecture", "blocked on..."

Unsafe wording: "settled" or "closed" without new proof evidence.

## Analogy Claims

Use this label for explanatory bridges that are valuable but not formal theorem equivalences.

Evidence examples:

- Noether coda is a scope warning, not a theorem: `docs/paper.md:295-308`.
- Lawvere/fixed-point language is demoted where finite self-reference is missing: `BACKLOG.md:81-99`, `lean-formalization/ReflectionTower.lean:82`.
- CyberAlchemy/spine relation is a bridge between formal and operational registers: `docs/spine-cyberalchemy-relation.md:14-23`.
- Reflection Tower/Arcanum "isomorphism" language is explicitly qualified by open judgment calls: `docs/reflection-tower-arcanum-isomorphism.md:102-113`.

Safe wording: "analogy", "operational register", "compatible presentation".

Unsafe wording: "formal equivalence", "same object", or "theorem" unless formalized.

## Refuted Or Negative Claims

Use this label where the repository has counterexample evidence or explicit negative closure.

Evidence examples:

- M6 strong is refuted: `lean-formalization/M6Counter.lean:145`, `docs/domainspec-two-layer-framework.md:158-167`.
- M2 unrestricted is refuted: `lean-formalization/M2Counter.lean:51`, `docs/domainspec-two-layer-framework.md:158-167`.
- Finite Lawvere fixed-point reading is structurally blocked in the current tower: `BACKLOG.md:81-99`, `lean-formalization/ReflectionTower.lean:82`.
- Strong observer/Noether unification is rejected or demoted: `LEAN-ARCHITECTURE.md:399`.

Safe wording: "refuted in this setting" or "closed negative under current formalization".

## Unsupported Or Overstated Claims To Demote

Demote these until a refreshed mechanical audit proves otherwise:

- "All Lean is sorry-free." Current strict text scan found active sorries.
- "The Mathlib PR-ready tree is all sorry-free." Current `files/new` contains analytic declared libraries with active sorries.
- "23 PR-ready files" as a whole-tree statement. Current local count is 29 top-level `files/new/*.lean`, and docs disagree on count.
- "Tier-1 thermodynamics prize is fully closed." Current safe reading is finite/discrete/costed witness surface plus open continuous/physical theorem work.
- "Reflection Tower and Arcanum are literally isomorphic." Current safe reading is partial alignment or compatible presentation.
- "Literature audits prove absolute novelty." Current safe reading is no preemption found in the surveyed corpus as of the audit date.

## Claim Discipline Verdict

The repository's best discipline is strong, but its front-door summaries are stale in places. The correct research posture is:

1. Keep theorem claims local to the file, theorem, and dependency evidence actually inspected.
2. Treat green build, no active `sorry`, no axioms, and PR-ready as four different statuses.
3. Treat bridge language as analogy or operational relation unless formalized.
4. Treat counterexamples as central results, not failed attempts.
5. Run a mechanical current-truth refresh before editing root claims.
