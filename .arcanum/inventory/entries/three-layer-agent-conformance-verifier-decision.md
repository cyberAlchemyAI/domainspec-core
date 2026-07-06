---
tags: [inventory, synthesis, cav2, authority, deterministic-validation, governance-determinism, agent-conformance, three-layer-validation, assurance-case, moat, kodamai, claim-le-proof, public-private-boundary, formalism]
node_type: synthesis
is_session: false
layer: architecture, governance
nature: explanatory, reference, decision
status: candidate
created: 2026-07-06
sources:
  - cyberAlchemy-v2/TO-VLAD/TO-VLAD-deterministic-validation-inconsistencies.md
  - .arcanum/inventory/entries/deterministic-validation-for-all-cav2-synthesis.md
  - cyberAlchemy-v2/ontology/promotion-requests/2026-06-23-authority-object-schema-proposal.md
  - cyberAlchemy-v2/authority/definitions/DEFINITIONS.md
  - arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md
  - .arcanum/inventory/queries/2026-07-06-ai-assurance-certification-vocabulary-research/findings.md
  - cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md
boundary: INTERNAL — moat-adjacent (the agent⊨spec verifier is the private moat). Do NOT copy into public arcanum/.
---

# Three-Layer Agent Conformance + General ⊨-Verifier Build Decision

Non-authority Inventory read model. Synthesizes a working session (2026-07-06) that
started from the TO-VLAD review of the "deterministic validation for all of CAV2"
synthesis and ended at a build decision. Promotes nothing; records a **proposed**
development-project decision pending `craft`/`invoke` authoring and a `decision-gate`.

- ID: three-layer-agent-conformance-verifier-decision
- Type: synthesis (with proposed decision)
- Status: candidate
- Confidence: high (analysis); the build decision is **proposed**, not gated
- Task fit: scoping the cav2 agent-conformance verifier development project; revising the
  deterministic-validation synthesis (B1/C1/C2); reconciling the `Validation Mode` enum;
  answering "what proof does agent work need" for high-stakes (robotics/health) framing.

## 1. The TO-VLAD review holds (spot-checked, not relayed)

Four highest-cost findings were verified against the actual corpus, all confirmed:
- **A1 (keystone):** the schema the plan waits on
  (`2026-06-23-authority-object-schema-proposal.md` §3) lists 10 fields with **no `axes`
  and no `specializes`** — yet the synthesis's queries quantify over `axis` and
  build-from-owned needs `specializes`. Clearing OQ-1 as-is freezes the wrong schema.
- **C1:** `CAV2-D29` (DEFINITIONS.md:1792) is the **Axis Orthogonality Invariant**
  (axis-vs-axis), not object-pair distinctness (that is D22, DEFINITIONS.md:1224). The
  synthesis cites D29 for the wrong thing.
- **C2:** the `review → mixed → validator` ladder is unattested; every corpus
  `Validation mode:` value is `review` or `hybrid`. `mixed`/`validator` appear nowhere.
- **C3:** "the catalog" does not exist; only `disciplines/DISCIPLINES.md` exists and it
  catalogs disciplines, not governance rules.

Verdict: the review is accurate where checked; the synthesis is a sound **direction** but
is **over-specced** and blocked on vocabulary that does not exist yet.

## 2. B1 is a settled-strategy conflict, not a text fix

The synthesis frontmatter/body call determinism "the attestation moat." This contradicts
(a) its own parent (`cav2-authority-and-determinism-synthesis` demoted determinism to "an
optimization, not a necessity") **and** (b) the settled [[validation-moat-model]]
(2026-07-02): validators/criteria are the **public funnel**; the moat is **engine +
Kodamai + corpus**. Elevate B1 above Victor's "cheap text fix" bucket — it re-inflates a
claim already ruled against, and this entry is a `candidate` that would propagate it.

## 3. The three-layer agent-conformance model (the load-bearing result)

"Constitution determinism toward **agent action and output**" is not one validator; it is
three layers, split by *what the check reads*:

| Layer | Reads | Instrument | Role |
| --- | --- | --- | --- |
| **1 — output-structural** | declared fields/edges in the produced artifact | SMT / script over typed records | public funnel |
| **2 — output-semantic** | the *meaning* of the produced content | LLM-judge / human | review shell |
| **3 — action-conformance** | whether the *agent's actual reasoning* conformed, beyond its self-report | **agent ⊨ spec verifier** | **the moat** ([[kodamai-smithe-correctness-moat]]) |

Consequences established:
- **D1 dissolves partially, not fully.** "Every governance rule reduces to an SMT query"
  is false for *use-constraint* rules (evidence-is-not-authority, no-inherit-by-proximity).
  Moving the check to authoring-time over the agent's *declared* output makes the
  **structural** half checkable (you make the agent emit the field); the **semantic** half
  (silent leakage) stays Layer 2; the **action** half stays Layer 3. Honest claim: "rules
  over declared fields reduce to SMT."
- **The boundary is fractal.** Even a total schema (the Lean kernel) certifies
  *conformance to an encoding*, never *rightness of the encoding*. "Encoding choice stays
  human" reappears at every rung, not just the top.
- **Output+schema generalizes as a GATE, not a CERTIFICATE.** Most agent work has a
  machine-checkable structural schema (code/proofs → near-total via compiler/kernel;
  docs/findings/authority-nodes → scaffold-only: cites resolve, fields present, no leak;
  judgment/plan → report-shape only). Passing the schema is necessary, rarely sufficient.

## 4. Enum reconciliation (fixes C2 from owned material)

`arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md` already authors the real ladder:
**`review → hybrid → deterministic`** (a rule may be marked `deterministic` only when it is
a field/edge **presence** check). The synthesis's `mixed`/`validator` are a mis-naming of
`hybrid`/`deterministic`. cav2 constitutions use only `review`/`hybrid`; the arcanum enum is
the more complete one. One-owner reconciliation needed. Guard: never force a semantic/action
rule to `deterministic` via a proxy field — that returns PASS while the real violation slips
(the D1 overreach recreated at script level).

## 5. High-stakes proof (robotics / health)

Stakes do not change the layers; they change **how high up the stack the regulator forces
you to climb**. For high-risk domains the required proof is a **conformity-grade assurance
case**, and its load-bearing rungs — **runtime conformance** + **external conformity
assessment** — are exactly the items the owned assurance research
([ai-assurance findings §7–8](../queries/2026-07-06-ai-assurance-certification-vocabulary-research/findings.md))
marks **Future-Only / Forbidden**. Regimes to map onto (vocabulary pressure only, per that
research): NIST AI RMF, ISO/IEC 42001, EU AI Act (Art. 43 conformity assessment); plus
domain regimes IEC 62304 / ISO 14971 / FDA SaMD (health), ISO 10218 / 13482 / 26262 / SOTIF
21448 (robotics). What the repo can provide **today** is the *readiness floor* (Layer-1
schema gate + Layer-2 Lean invariant specimen + receipts + L1 attestation), **not** the
assurance case.

## 6. Decision (SCAFFOLDED — DEFINE+DESIGN authored): build Option 2 — a general ⊨-verifier

- **Difference between options:** where the **engine/plug-in boundary** is drawn. Option 1
  (one-off dose-checker) bakes the domain in — nothing transfers. Option 2 (a general core:
  `spec + action → conform/not-conform + fallback`, with a thin dosage plug-in) is reusable.
  **Option 2 subsumes Option 1's deliverable** (it produces the dosage witness for free), so
  "do both" = build Option 2.
- **The moat is earned on the distant witness (robot, #3), not two-of-same-kind.** AV-D1
  resolved to a three-witness ramp: dosage → **data-access** (cheap, build-from-owned; de-risks
  the harness + builds a reusable permission-gate component, but is another memoryless permission
  point-decision, so it proves *breadth*, not generality) → **robot force-limit** (continuous +
  temporal + real-time — the axis that actually tests generality). Data-access de-risks robot's
  *plumbing*, **not** its hard axis. Same-kind witnesses do not discharge the gate (anti-B1).
- **Dosage specimen = witness #1, bounded internal only.** A formal dose-permission spec +
  Lean invariant + monitor prototype + a "what this does not prove" page. **Not** a deployed
  medical device (that triggers real high-risk/conformity obligations).
- **Boundary:** the general verifier + engine is the **private moat**; the specimen is the
  demonstration you may cite (the [[engine-algorithm-proprietary]] shape). Realization ties
  to the Lean kernel at [[lean-kernel-location-and-status]]
  (`domainspec-lean-formalization/lean-engineer/`).
- **Executed 2026-07-06 (DEFINE + DESIGN):** project scaffolded at
  `projects/domainspec-v2/development/agent-spec-conformance/` (v2 dev lane, not cav2 — Two-Lane
  Discipline; sibling plane to `code-tag-conformance`), registered as ledger
  `CTX-DSV2-AGENT-SPEC-CONFORMANCE`. **AV-D2 boundary designed:** core owns the
  `certify → verdict → fallback` pipeline + a **plural certify-backend interface** (`structural` /
  `invariant-proof` / `runtime-monitor`) + fail-closed discipline; the plug-in owns the domain +
  declares its backend. Over-fit trap = shipping one backend (SMT, fits dosage+data-access); robot
  forcing a *new backend behind the same interface* = SURVIVED-general, forcing the *interface* to
  change = FALSIFIED-general. Next: `invoke plan` (L0/L1/L2).

## Residue

- Build decision **scaffolded** (DEFINE + DESIGN + craft-registered), not yet gated — pending
  `invoke plan` (work-pack L0/L1/L2) and a `decision-gate` before implementation and before any
  "general/moat" claim (gated at witness #3).
- Resolved 2026-07-06: three-witness ramp dosage → data-access → robot; DEFINE + DESIGN authored at
  projects/domainspec-v2/development/agent-spec-conformance/ (ledger CTX-DSV2-AGENT-SPEC-CONFORMANCE). Moat
  claim gated at the distant witness (robot, #3), not two-of-same-kind.
- Open: A1 amendment to the schema proposal (type `axes`/`specializes`) must land before OQ-1
  is declared clearable; B1 correction to the deterministic-validation synthesis is pending.
- Promotes no certification, conformity, runtime-conformance, formal-correctness, or
  provably-correct-agent claim (aligns with the assurance findings' Forbidden list).
