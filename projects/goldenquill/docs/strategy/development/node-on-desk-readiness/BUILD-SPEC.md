# BUILD-SPEC — node-on-desk-readiness (PARENT recomposition surface)

- Node: `node-on-desk-readiness` (Craft `CTX-NOD-ROOT`)
- Role: **parent recomposition surface**, not a worker. This spec proves the ten child
  nodes together produce a working customer node. It does **not** duplicate child build
  detail — each child owns its own `each child space's BUILD-SPEC.md`.
- Sources: `docs/strategy/development/node-on-desk-readiness/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md`,
  parent ledger `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml`,
  `docs/strategy/development/node-on-desk-readiness/CRAFT.md`,
  the ten child ledgers (read-only, for dependency edges),
  `docs/golden-quill-task-role-breakdown-handoff.md`.
- Law 3: parent-level only. No `orgs/` reads or references. All sources are repo-root strategy/feature/spec artifacts.
- Authored: 2026-06-13. Status: **REFINE-SOLVABLE gap authored; recomposition NOT yet proven** (no child runtime receipts recomposed upward).

---

## 0. Per-gap verdict summary

| Gap | Verdict | Disposition in this spec |
| --- | --- | --- |
| **GAP-NOD-SEQUENCE** | **REFINE-SOLVABLE — RESOLVED HERE** | Parent recomposition SEQUENCE authored below (§2 Define, §3 Design, §4 Plan, §5 Acceptance, §6 First steps). Derived entirely from in-repo child dependency edges. |
| **GAP-NOD-HOURS-RATES** | **DECISION-GATED — NOT RESOLVED (operator input)** | Surfaced as operator callout §7.1. Blank Est. Hrs / Rate across the workbook; budget not computable. Owner: Josh (staffing-budget-and-triggers). Structure is local; values are operator business judgment. |
| **GAP-NOD-CANON-VOCAB** | **DECISION-GATED — NOT RESOLVED (blocked on DEC-BC-POSTURE-VOCAB)** | Surfaced as operator callout §7.2. Deprecated posture vocabulary in workbook row B. Owner: boundary-and-canon. Gates Recomposition Gate RG-1. |
| **UI phase question** (DEC-BC-UI-BOUNDARY / GAP-TRB-UI-PHASE) | **DECISION-GATED — NOT RESOLVED** | Surfaced as operator callout §7.3. v0.1 no-UI lock collision. Owner: boundary-and-canon governance. Gates RG-1. |
| **Recomposition residue** | **OPEN — readiness path mappable, NOT proven** | §8. No child `RUNTIME-HANDOFF` has run (`not_run` across all ten). Path is sequenced but no upward receipts exist. |

---

## 1. The ten child nodes and their spec paths

Each child owns its detailed build. This parent references them; it does not restate them.

| # | Child node | Child BUILD-SPEC (canonical path) | Workbook workstream | Child ledger |
| --- | --- | --- | --- | --- |
| C1 | boundary-and-canon | `docs/strategy/development/boundary-and-canon/BUILD-SPEC.md` | Canon/posture/UI scope (cross-cutting) | `docs/strategy/development/boundary-and-canon/.craft/ledger.yml` |
| C2 | hardware-golden-image | `docs/features/hardware-golden-image/BUILD-SPEC.md` | A. Hardware & Physical Node + Golden Image | `docs/features/hardware-golden-image/.craft/ledger.yml` |
| C3 | tilth-runtime-build | `docs/features/tilth-runtime-build/BUILD-SPEC.md` | B. Software — Tilth Build | `docs/features/tilth-runtime-build/.craft/ledger.yml` |
| C4 | quality-security-proof | `docs/features/quality-security-proof/BUILD-SPEC.md` | C. Quality, Security & Proof | `docs/features/quality-security-proof/.craft/ledger.yml` |
| C5 | capital-logic-library | `docs/features/capital-logic-library/BUILD-SPEC.md` | D. Capital Logic Content | `docs/features/capital-logic-library/.craft/ledger.yml` |
| C6 | sales-contracting-legal | `docs/strategy/development/sales-contracting-legal/BUILD-SPEC.md` | E. Selling & Contracting | `docs/strategy/development/sales-contracting-legal/.craft/ledger.yml` |
| C7 | white-glove-delivery-node-care | `docs/strategy/development/white-glove-delivery-node-care/BUILD-SPEC.md` | F. White-Glove Delivery | `docs/strategy/development/white-glove-delivery-node-care/.craft/ledger.yml` |
| C8 | company-operations-finance | `docs/strategy/development/company-operations-finance/BUILD-SPEC.md` | G. Company Operations | `docs/strategy/development/company-operations-finance/.craft/ledger.yml` |
| C9 | staffing-budget-and-triggers | `docs/strategy/development/staffing-budget-and-triggers/BUILD-SPEC.md` | Roles & Gaps + hours/rates | `docs/strategy/development/staffing-budget-and-triggers/.craft/ledger.yml` |
| C10 | after-acceleration-roadmap | `docs/strategy/development/after-acceleration-roadmap/BUILD-SPEC.md` | After Acceleration | `docs/strategy/development/after-acceleration-roadmap/.craft/ledger.yml` |

> Note: `each child space's BUILD-SPEC.md` is the canonical reference path for each child build.
> As of authoring, child BUILD-SPECs are not yet written; this parent sequence defines the
> order in which they should be produced and recomposed.

---

## 2. DEFINE — the parent recomposition problem

**Core question (from RESEARCH-RESULT):** what evidence proves the ten child nodes add up
to a working customer-node readiness path?

**Parent's job:** bind the children into a dependency-ordered readiness path with
done-definitions and recomposition gates, so that when child runtime receipts arrive they
can be recomposed upward into a single "node-on-desk ready" assertion.

**Cross-child dependency edges (the seams where "children add up" is proven or fails).**
These are the encoded edges, sourced from child ledgers, not invented here:

- **E1 posture-canon → tilth.** `GAP-TRB-POSTURE-CANON` (block, owner boundary-and-canon)
  depends on `DEC-BC-POSTURE-VOCAB` (blocking) + `BLK-BC-POSTURE-VOCAB`. The posture
  enforcement row in Tilth Build (workbook B, line 50) cannot be executed until canon
  vocabulary is corrected. Source: tilth ledger `gaps[1]` + boundary ledger `decisions[0]`,
  `typed_items[0]`.
- **E2 UI-phase canon → tilth.** `GAP-TRB-UI-PHASE` (flag) ↔ `DEC-BC-UI-BOUNDARY` (phase
  boundary) ↔ `GAP-BC-UI-SCOPE`. Operator console row (workbook B, line 53) collides with
  the locked v0.1 no-UI boundary; phase decision must land before the row is executable.
  Source: tilth ledger `gaps[2]` + boundary ledger `gaps[0]`, `decisions[1]`.
- **E3 Golden-Image → tilth packaging.** `GAP-TRB-GOLDEN-IMAGE-HANDOFF` (flag, coordinate)
  depends on hardware image-verify + signing: `GAP-HGI-IMAGE-VERIFY` (block) and
  `GAP-HGI-BACKUP-RECOVERY` (block). The Golden Image assembly row (workbook B, line 55)
  packages the runtime onto a verified, signed, repeatable image. Source: tilth ledger
  `gaps[3]` + hardware ledger `gaps[2,3]`.
- **E4 QSP instrumentation → COF + WGD.** `GAP-QSP-INSTRUMENTATION` (support hrs/node,
  usage baselines, renewal-intent capture) feeds `GAP-COF-VALIDATION-PACKET` (investor/
  validation packet evidence) and `GAP-WGD-DAY60` (Day 60 review metrics + renewal signal).
  QSP also owns `GAP-QSP-CLAIMS-REGISTER`, which feeds `GAP-SCL-SALES-MATERIALS` (claims
  evidence before sales material hardens). Source: QSP ledger `gaps[2,3]` + COF ledger
  `gaps[3]` + WGD ledger `gaps[2]` + sales ledger `gaps[0]`.
- **E5 capital → promotion-governance ledger.** `REL-CLL-PROMO-GOV` / parent
  `REL-NOD-LINK-PROMO-GOV` link capital-logic-library to the existing root promotion-
  governance Craft ledger (`[repo-root] .craft/ledger.yml`) rather than recreating it.
  Source: parent ledger `relations[0]` + capital ledger `relations[0]`.
- **E6 staffing ← everything cost-bearing.** `GAP-SBT-HOURS-RATES` (block) gates any budget
  for every onboard-now/onboard-later role across QSP security reviewer
  (`GAP-QSP-SECURITY-REVIEWER`), capital domain experts (`GAP-CLL-DOMAIN-EXPERTS`), sales
  legal (`GAP-SCL-LEGAL-FIRST-LOI`), and the WGD/CS handoff trigger
  (`GAP-WGD-CS-HANDOFF` ↔ `GAP-SBT-ONBOARD-LATER`). Source: staffing ledger `gaps[0,2]`
  + the named child blockers.

**Out of scope for this parent spec (owned by children):** individual hardware specs,
runtime module work packs, test-plan authoring, card content, contract drafting, install
playbook steps. Reference the child BUILD-SPECs for that detail.

---

## 3. DESIGN — the readiness path (dependency layers)

The path is a partial order, not a strict line. Layers below are dependency-ordered: a
layer may begin only when its upstream recomposition gate (§4) has cleared. Children inside
a layer can run in parallel.

```
Layer 0  CANON LOCK            C1 boundary-and-canon (posture vocab + UI phase)
            │  (gates E1, E2)
Layer 1  PHYSICAL + RUNTIME    C2 hardware-golden-image  ║  C3 tilth-runtime-build
            │  C3 posture/UI rows unblocked by Layer 0
            │  C3 Golden Image row consumes C2 image-verify+signing (E3)
Layer 2  PACKAGED ARTIFACT     Golden Image assembly (C2×C3 seam closed; signed, repeatable)
            │  (gates E3)
Layer 3  PROOF                 C4 quality-security-proof (guardrails-as-tests over Layer 2;
            │                   independent security review of boundary + signing chain)
            │  (claims register + instrumentation defined → E4)
Layer 4  CONTENT + COMMERCIAL  C5 capital-logic-library (cards, promo-gov link E5)  ║
            │                   C6 sales-contracting-legal (legal-first before LOI; claims
            │                   evidence from C4 → E4)
Layer 5  DELIVERY              C7 white-glove-delivery-node-care (repeatable playbook over a
            │                   proven, packaged, content-loaded node)
Layer 6  OPERATING FLOOR       C8 company-operations-finance (support triage, Node Care,
            │                   validation packet fed by C4 instrumentation → E4)
Layer X  CROSS-CUTTING         C9 staffing-budget-and-triggers (budget + onboarding triggers
            │                   gate every cost-bearing role across all layers → E6)
Layer 7  POST-CAPITAL          C10 after-acceleration-roadmap (sequenced against deployed-
                               node count + renewal data; depends on Layers 5–6 evidence)
```

**Layer X (staffing) is cross-cutting, not terminal.** It does not sit "at the end"; its
budget/trigger outputs are an input to every layer that onboards a paid role. It is blocked
on `GAP-NOD-HOURS-RATES` (operator input, §7.1), so it cannot be closed locally even though
its structure is known.

---

## 4. PLAN — recomposition gates (RG-n)

A recomposition gate clears only when **every** upstream child has emitted a runtime receipt
satisfying its done-definition (§5) AND the named cross-child seam is closed. Gates are the
parent's certification points. All gates are currently **OPEN** (no child receipts exist).

| Gate | Clears when | Binds children | Closes edges | Blocked by |
| --- | --- | --- | --- | --- |
| **RG-1 Canon Lock** | `DEC-BC-POSTURE-VOCAB` selected (three-posture canon) AND `DEC-BC-UI-BOUNDARY` phased AND `BLK-BC-POSTURE-VOCAB` closed | C1 | E1, E2 | §7.2, §7.3 (operator/governance) |
| **RG-2 Runtime Buildable** | RG-1 clear; C3 posture + UI rows unblocked; C3 work packs sequenced (`GAP-TRB-WORK-PACKS`) | C3 (uses C1) | E1, E2 | RG-1 |
| **RG-3 Image Verified** | C2 image-verify (`GAP-HGI-IMAGE-VERIFY`) + backup/recovery (`GAP-HGI-BACKUP-RECOVERY`) have tested procedures; reference spec captured | C2 | — | — |
| **RG-4 Packaged Artifact** | RG-2 + RG-3 clear; Golden Image assembly seam closed — runtime packaged onto verified signed image, repeatably (`GAP-TRB-GOLDEN-IMAGE-HANDOFF` closed) | C2 × C3 | E3 | RG-2, RG-3 |
| **RG-5 Proof** | RG-4 clear; C4 guardrails-as-tests pass over the packaged artifact (`GAP-QSP-TEST-PLAN`); independent security review assigned + run (`GAP-QSP-SECURITY-REVIEWER`); claims register + instrumentation defined | C4 (over C2×C3) | E4 (defines feeds) | RG-4, §7.1 (reviewer cost) |
| **RG-6 Sellable** | RG-5 clear; claims register feeds sales materials (`GAP-SCL-SALES-MATERIALS`); legal-first artifacts exist before first LOI (`GAP-SCL-LEGAL-FIRST-LOI`); launch cards authored + expert-validated (`GAP-CLL-*`) | C5, C6 | E4, E5 | RG-5, §7.1 (legal/expert cost) |
| **RG-7 Deliverable** | RG-4 + RG-5 + RG-6 clear; C7 repeatable delivery playbook exists over a proven, packaged, content-loaded node (`GAP-WGD-PLAYBOOK`) | C7 | — | RG-4, RG-5, RG-6 |
| **RG-8 Operable** | RG-7 clear; C8 support triage boundaries (`GAP-COF-SUPPORT-TRIAGE`), Node Care cadence, validation packet fed by C4 instrumentation (`GAP-COF-VALIDATION-PACKET`) | C8 (uses C4) | E4 | RG-7 |
| **RG-X Budgeted** (cross-cutting) | `GAP-SBT-HOURS-RATES` filled; onboarding triggers confirmed (`GAP-SBT-ONBOARD-NOW/LATER`); every cost-bearing role across RG-5/6/7/8 has a budget line | C9 | E6 | §7.1 (operator input) |
| **RG-9 Node-on-Desk Ready** (terminal recomposition) | RG-1…RG-8 + RG-X all clear; all child `RUNTIME-HANDOFF` receipts recomposed upward into parent ledger `recomposition[]` with status `pass` | all | all | every upstream gate |
| **RG-10 Scale Sequenced** | RG-9 clear; C10 themes sequenced against deployed-node count + renewal data (`GAP-AAR-SEQUENCING`); non-founder install proven (`GAP-AAR-REPEATABILITY`) | C10 | — | RG-9 |

**Critical-path spine:** RG-1 → RG-2 → RG-4 → RG-5 → RG-7 → RG-9 → RG-10. RG-3 parallels
RG-1/RG-2 and joins at RG-4. RG-6 and RG-8 hang off RG-5/RG-7. RG-X gates cost across the
spine and is operator-blocked from the start.

---

## 5. Child done-definitions (parent-level recomposition contract)

What each child must emit for its layer's gate to clear. These are recomposition criteria,
not the child's internal build steps — the child BUILD-SPEC owns those.

| Child | Done-definition (what the parent recomposes) |
| --- | --- |
| C1 boundary-and-canon | Posture vocabulary corrected to canon three-posture set; UI row phased (v0.1 / read-only-projection / later-phase); `DEC-BC-POSTURE-VOCAB` + `DEC-BC-UI-BOUNDARY` closed. |
| C2 hardware-golden-image | Reference workstation spec testable; burn-in thresholds defined; Golden Image write verified per-unit; backup/export/recovery procedure tested; update-signing chain exists. |
| C3 tilth-runtime-build | Runtime rows sequenced into work packs; posture + UI rows consuming corrected canon; runtime emits a Golden-Image-ready packaging handoff. |
| C4 quality-security-proof | Guardrails-as-tests pass over packaged artifact; independent security review run; claims register populated; instrumentation defined and emitting. |
| C5 capital-logic-library | Five launch cards authored + expert-validated; rule packs owned; promotion-governance link live (no recreation). |
| C6 sales-contracting-legal | Legal-first artifacts (agreement, LOI, data-policy, procurement, insurance) exist before first LOI; sales materials carry claims-register evidence. |
| C7 white-glove-delivery-node-care | Repeatable delivery playbook from pre-deployment through training; Day 60 review shape defined. |
| C8 company-operations-finance | Entity/banking/bookkeeping checklist; support-triage boundaries; Node Care cadence; validation packet ownership. |
| C9 staffing-budget-and-triggers | Hours/rates filled (operator); onboarding triggers confirmed for every cost-bearing role; computable budget. |
| C10 after-acceleration-roadmap | Themes sequenced against deployed-node + renewal evidence; non-founder install proven. |

---

## 6. ACCEPTANCE CRITERIA (parent recomposition surface)

The parent node is "done" when:

1. **AC-1 Sequence authored.** A dependency-ordered readiness path with done-definitions and
   recomposition gates exists (this document). — **MET** as of authoring; closes the
   author-portion of GAP-NOD-SEQUENCE.
2. **AC-2 Edges bound.** Every encoded cross-child edge (E1–E6) is represented by a
   recomposition gate (RG-1…RG-X). — **MET**.
3. **AC-3 Gates traceable.** Each RG names its child(ren), the edge(s) it closes, and its
   upstream blockers; no gate references `orgs/` data. — **MET** (Law 3 clean).
4. **AC-4 Operator items surfaced, not resolved.** GAP-NOD-HOURS-RATES, GAP-NOD-CANON-VOCAB,
   and the UI phase question are surfaced as callouts (§7) and left for the named owner. —
   **MET**.
5. **AC-5 Recomposition proven.** All ten child `RUNTIME-HANDOFF` receipts recomposed upward
   with status `pass`; RG-9 clears. — **NOT MET** (recomposition residue, §8). This is the
   only acceptance criterion the parent cannot self-satisfy; it requires child runtime runs.

**Parent gate state:** `flag` (sequence authored, recomposition unproven). Flips to `pass`
only at RG-9.

---

## 7. DECISION-GATED / OPERATOR-INPUT callouts (NOT resolved here)

### 7.1 GAP-NOD-HOURS-RATES — [block, owner: Josh]
Est. Hrs and Notes/Rate columns are blank across the entire workbook (handoff lines 34–80,
88–97). No staffing or capital budget is computable. Structure is local (roles, onboarding
triggers, layer assignment all known); the **values are operator business judgment**, not
external lookup. Gates RG-X across the whole spine. EXT-REQ-02 (fractional-role market-rate
benchmarks) is parked and DEFERRED — only runs if Josh wants market anchors and explicitly
approves. **Action required: Josh fills hours/rates in staffing-budget-and-triggers.**

### 7.2 GAP-NOD-CANON-VOCAB — [block, owner: boundary-and-canon]
Workbook posture row (handoff line 50) uses deprecated "Unrestricted / Hybrid / Sanitized /
Sovereign" vocabulary. Canon is the three-posture set Frontier-Eligible / Split-Context
Hybrid / Local-Only-Sovereign ("Sanitized" deprecated). Blocked on `DEC-BC-POSTURE-VOCAB`
(boundary ledger, blocking, status active). Gates RG-1 → cascades to RG-2 via E1.
**Action required: governance closes DEC-BC-POSTURE-VOCAB.**

### 7.3 UI phase question — [decide, owner: boundary-and-canon governance]
Workbook "Operator console UI" row (handoff line 53) collides with the locked v0.1
headless/no-UI boundary. `DEC-BC-UI-BOUNDARY` (phase_boundary, active) + `GAP-BC-UI-SCOPE`
+ `GAP-TRB-UI-PHASE` mirror this. Must be phased (v0.1 read-only projection vs. later product
surface) before the row is executable. Gates RG-1 → RG-2 via E2.
**Action required: governance closes DEC-BC-UI-BOUNDARY.**

---

## 8. Recomposition residue (path mappable, NOT proven)

- Every child carries Refine + Research routes at `pass` but `RUNTIME-HANDOFF` at `not_run`
  (verified across all ten child ledgers). No child runtime receipt has been produced.
- Parent ledger `recomposition[0].status: flag`, residue: "Hours/rates, canon corrections,
  sequencing, and child-ledger task decomposition remain open." This spec closes the
  *sequencing* portion; the other three remain.
- The readiness path is now **mappable** (RG-1…RG-10 with edges bound) but **not proven**:
  no upward receipts exist, so RG-9 (terminal) cannot clear and AC-5 stays unmet.
- External research stays DEFERRED (EXT-REQ-01 deployment-readiness patterns, EXT-REQ-02
  fractional-role rates) — neither runs without a surviving named gap + Josh's approval.

---

## 9. FIRST STEPS (to begin proving the path)

1. **Unblock RG-1 (operator/governance).** Resolve §7.2 (DEC-BC-POSTURE-VOCAB) and §7.3
   (DEC-BC-UI-BOUNDARY) in boundary-and-canon. These gate the entire runtime spine.
2. **Unblock RG-X input (operator).** Josh fills hours/rates (§7.1) so staffing budget and
   onboarding triggers become computable for every cost-bearing role.
3. **Author child BUILD-SPECs in dependency order**, starting with C1 (boundary), then C2/C3
   in parallel, per §3. Each lands at `each child space's BUILD-SPEC.md`.
4. **Run child Refine→Invoke→runtime** for Layer 0–1 children; emit `RUNTIME-HANDOFF`
   receipts.
5. **Recompose upward.** As each child receipt arrives, record it in parent ledger
   `recomposition[]` and clear the corresponding RG. RG-9 clears when all ten are `pass`.

---

## Output file

`docs/strategy/development/node-on-desk-readiness/BUILD-SPEC.md`
