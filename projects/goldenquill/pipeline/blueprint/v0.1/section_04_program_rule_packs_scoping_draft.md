---
title: Program Rule Packs — Scoping Draft (NOT in amendment queue)
section: §4 Logician (probable owner; §11 new-section is an open option)
parent_blueprint: section_04_logician.md
parent_version: v2.1 (with v2.6 deferred-scope DRAFT in flight; §4 on path to LOCKED-as-a-whole post-Round-L capstone)
amendment_status: SCOPING DRAFT — NOT entering the §4 v2.x amendment chain. Slot v2.7 is reserved but not claimed.
scope: Capture and design-scope the "Program Rule Packs" architectural principle surfaced by the 2026-04 research corpus. Determine whether the principle lands as §4 amendment, new blueprint section, or architecture v7.x amendment. Surface the design forks for Thesis Team review before any LOCK-bearing edit.
provenance: research/logician_formal_logic/01_Formalizing_Grant_Compliance_Logic.docx + research/capital_logic_cards/01_Capital_Logic_Cards_Architecture_v2_engineering.docx (triaged 2026-05-01); v9 biz plan §3 + Appendix B (Capital Logic Cards integrated 2026-05-01); on-disk nascent artifact pipeline/rubrics/vapg_fy26.json (extracted 2026-04-12).
authored_date: 2026-05-01
authored_by: Tilth-core session, in dialogue with Josh
---

# Program Rule Packs — Scoping Draft

## §0. What this draft is, and isn't

This is a **scoping draft**, filed under blueprint/v0.1/ as a parked design proposal. It is NOT an amendment. It does NOT enter the §4 v2.x amendment chain (currently at v2.6 DRAFT). It does NOT modify any locked file. It does NOT obligate Thesis Team review on any timetable.

What this draft does: capture the principle, inventory cross-section impacts, sketch a candidate schema, and surface the 7 open design questions that need Josh + Thesis Team adjudication before any LOCK-bearing edit is authored.

The §4 v2.1 LOCK + v2.6 deferred-scope amendment chain is on a journey to "LOCKED-as-a-whole post-Round-L capstone" (per `pipeline/handoffs/section_4_logician_lock_as_a_whole_journey_map_2026-04-29.md`). Adding Program Rule Packs work to that chain risks disrupting the capstone. **One open question (§7) is whether to interrupt the capstone or sequence Program Rule Packs as a follow-on.**

## §1. The principle

**Program Rule Packs (PRPs) are program-specific deterministic rule libraries — eligibility, costs, attachments, deadlines, page limits, scoring criteria — that live alongside but separate from Capital Logic Cards.** Cards carry semantic / voice / evidence grammar; PRPs carry program-specific structural gates. The two are joined at orchestration time (§5 Pipeline) by binding a draft to the PRP its target program requires.

Stated as a separation principle: **"Cards carry funding grammar. Programs carry funding rules."** A Farmer Card may reference USDA VAPG, SARE, REAP, EQIP, SCBGP, or SBIR pathways — but the Card MUST NOT redefine program law. Program law lives in the PRP.

The principle has two consequences for the locked architecture:

1. **§4 Logician's rule-enforcement scope expands.** Today §4 enforces cross-program invariants (RFA hash, org isolation, dossier lock, source verification, admin-risk monotonicity). Under PRP, §4 ALSO enforces per-program structural gates loaded from the PRP active for the target opportunity.

2. **A new operator-authored artifact class enters Tilth.** PRPs are signed, versioned, source-bound rule sets. They are NOT generated; they are operator-authored (or operator-curated from upstream RFA + CFR text) and cryptographically signed before they enter the runtime.

## §2. Existence audit

Per `feedback_preflight_existence_audit.md` — tag every load-bearing mechanism EXISTS / PARTIAL / ASPIRATIONAL / OUT-OF-SCOPE with on-disk evidence.

| Mechanism | Tag | Evidence |
|---|---|---|
| PRP data file format | PARTIAL | `pipeline/rubrics/vapg_fy26.json` is a nascent PRP (meta, eligible_applicants, matching_requirements, scoring_criteria, key_regulations, critical_requirements). No formal schema, no signature, not §4-loaded. |
| PRP storage location | ASPIRATIONAL | `pipeline/rubrics/` holds vapg_fy26.json today; whether PRPs live there or in a dedicated `pipeline/program_rule_packs/` is open. |
| PRP loading at PRE-gate | MISSING | §4 PRE-gate row table (rows 1-20, with rows 19-20 deferred to Round M per v2.6) does not include any PRP-load or PRP-validate rows. |
| PRP enforcement at POST-gate | MISSING | §4.4.1 POST-gate checks structural properties (BT10 grep verify, BT11 dossier lock, admin-risk scan) but NOT program eligibility, cost ceilings, page limits, or attachment completeness. |
| Card → PRP binding | ASPIRATIONAL | Research doc 1 §12.10 specifies `program_references: [{program_id, relationship, notes}]` in Card schema. No on-disk Card schema yet — Cards are themselves a v9-converged research concept, not a locked architecture artifact. |
| Operator signature on PRPs | MISSING | No signing/loading machinery for PRP files exists. (§4 v2.1 has operator-signed claim-evidence maps; analogous mechanism for PRPs would mirror that pattern.) |
| Source-binding to upstream policy (CFR / RFA / agency notice) | MISSING | vapg_fy26.json has `source_url` but no hash, no fetch-date verification, no upstream-drift detection. |
| Datalog / RGL formal grammar (per research doc 2) | OUT-OF-SCOPE for v0.1 | Datalog stratified-negation rule library is a Stage-2+ concern. v0.1 PRP can be JSON/YAML hard-gate / review-flag / advisory tags without full Datalog semantics. |

## §3. Cross-section impact inventory

PRP touches more than §4. Each section below names the touch surface; only the architecture / Thesis Team can decide whether each becomes an amendment, a new section, or a no-op.

### §3.1 §0.5 Interface Index — new contract rows
- New `kind: rule_pack` (or extension of an existing kind).
- Contract rows for PRP-load, PRP-validate, PRP-enforce, PRP-sign-verify operations.
- New failure-code prefixes: `F-PRP-LOAD-*`, `F-PRP-SIG-*`, `F-PRP-MISSING-*`, `F-PRP-EXPIRED-*`, etc.

### §3.2 §4 Logician — primary owner
- New §4.X subsection for PRP loading, validation, and enforcement.
- New PRE-gate rows (probable order ≥ 21) for PRP-presence + PRP-signature + PRP-freshness checks.
- New POST-gate checks for program-specific eligibility / cost / attachment / page-limit gates.
- New failure codes per §3.1.
- Gate-runner method for PRP-aware sign-off.

### §3.3 §5 Pipeline — orchestration
- Track-registry entry for PRP-aware draft submission.
- Loading PRP at pipeline-run start (after §0.5 index check, before seat compilation).
- Threading the active PRP into the seat compilation context so Scribe/Editor/Judge/Red Team see it.

### §3.4 §7 Scribe — draft-time awareness
- Scribe receives the active PRP at compile-time so it can avoid drafting against constraints that will fail Logician POST-gate (e.g., word counts that exceed page limits, costs that exceed ceilings).
- Open question: does Scribe see the PRP as content (informing the draft), or only as constraints (gating the draft)?

### §3.5 §9 Judge — scoring rubric
- Funder's own rubric (per `feedback_judge_rubric_strategy.md`) is currently the Judge's primary input. PRPs include `scoring_criteria` (vapg_fy26.json has these). Reconcile: is funder rubric a subset of PRP, or a separate artifact PRP references?

### §3.6 §6 Operating Envelope — track registry
- §6 ships the track-registry mechanism (per A6 R.PF1). PRP-aware tracks register here. Probable no §6 amendment needed if the track-registry shape is generic enough — but verify.

### §3.7 Architecture v7.x — open
- If PRP is a v0.1 architectural commitment (not just a v0.1.x blueprint feature), it warrants an architecture-level amendment establishing the principle. Probable architecture A-row: "Cards carry grammar; Programs carry rules; Logician enforces; Pipeline orchestrates."
- Alternatively, if PRP is purely a blueprint-level addition with no architecture commitment shift, no architecture amendment is needed.

## §4. Candidate schema sketch (NOT prescriptive)

Drawn from `pipeline/rubrics/vapg_fy26.json` + research doc 1 §11.1 + research doc 2 RGL framing. **Surface for Thesis Team critique only — not a proposal to LOCK.**

```yaml
program_rule_pack:
  pack_id: "usda_vapg_fy26"             # unique, lowercase, snake_case
  pack_version: "1.0.0"                  # SemVer; bumped on rule changes
  pack_signature: "<operator_keyring_sig>"  # ed25519 over canonical-JSON pack body
  signed_at: "2026-05-01T00:00:00Z"
  signed_by: "operator:josh@..."
  
  meta:
    funder: "USDA Rural Development"
    program: "Value-Added Producer Grant"
    nofo_number: "RDBCP-VAPG-2026"
    fiscal_year: 2026
    assistance_listing: "10.352"
    deadline: "2026-04-22T13:00:00-04:00"
    source_url: "..."
    source_doc_hash: "<sha3-512 of the RFA PDF>"   # binds to upstream
    extracted_date: "2026-04-12"
  
  eligibility_rules:
    - rule_id: "vapg.eligibility.applicant_class"
      kind: "hard_gate"                  # hard_gate | review_flag | advisory
      predicate: "applicant.entity_type IN {independent_producer, agricultural_producer_group, farmer_or_rancher_cooperative, majority_controlled_producer_based_business_venture}"
      failure_code: "F-PRP-VAPG-ELIG-CLASS"
      source_ref: "RFA §C.1, p.12"
  
  cost_ceilings:
    - rule_id: "vapg.cost.planning_max"
      kind: "hard_gate"
      predicate: "grant_type == 'planning' IMPLIES total_request <= 50000"
      failure_code: "F-PRP-VAPG-COST-PLANNING"
      source_ref: "RFA §A.1.a"
  
  attachment_requirements: [...]
  page_limits: [...]
  scoring_criteria: [...]    # may reference funder rubric externally or carry it inline
  critical_requirements: [...]
  matching_requirements: [...]
  
  lifecycle:
    state: "stable"                      # draft | sandbox | pilot | stable | deprecated
    deprecation_date: null
    successor_pack_id: null
```

**Schema-shape questions surfaced (not answered):**
- JSON or YAML or both?
- Cedar policies inline, or generated from PRP at load-time?
- Datalog clauses embedded (research doc 2), or string predicates evaluated by §4 Cedar?
- Per-rule `failure_code` namespacing (`F-PRP-{PACK}-{RULE}`) — pin or operator-chosen?

## §5. Storage and lifecycle

Open. Three options:

**(a) `pipeline/program_rule_packs/{pack_id}.{version}.yaml`** — analogous to `pipeline/rubrics/`. Operator-authored, git-versioned, signed at lock-time.

**(b) `pipeline/rubrics/{pack_id}/`** — extend the rubrics folder, since vapg_fy26.json already lives there. Rename rubrics to rule_packs, or keep rubrics as a sub-concern.

**(c) `vault_shared/rule_packs/{pack_id}/`** — vault-stored, treated like router.yaml under §2 Vault Topology. Stronger sovereignty story; harder operator authoring loop.

Lifecycle states (drawn from research doc 1): `draft → sandbox → pilot → stable → deprecated`. Pack signing happens at the `stable` transition. Deprecation requires successor pack reference.

## §6. Open questions for Thesis Team

These are the design forks the Team needs to adjudicate. Each has architecture-level consequences.

1. **Architecture vs blueprint scope.** Is "Program Rule Packs" an architecture-level commitment (warrants architecture v7.x amendment) or purely a blueprint-level feature (§4 amendment + §0.5 contract rows)?

2. **§4 amendment vs new §11 section.** Does PRP land as a §4 v2.7+ amendment (extends Logician's existing rule-enforcement scope) or as a new top-level blueprint section §11 "Program Rule Packs" (parallel to §6 Operating Envelope, owned by the §4 Logician runtime)?

3. **Sequencing vs §4 lock-as-a-whole capstone.** §4 is on a journey to LOCKED-as-a-whole post-Round-L. Does PRP work interrupt that capstone (PRP enters as v2.7 before LOCK-as-a-whole), or does PRP wait for post-LOCK-as-a-whole as a §4 v3.x or §11 v1.0 round?

4. **Schema language.** YAML+predicate-strings (operator-friendly, simple to parse), Cedar policies (consistent with existing §4 Cedar evaluation), Datalog/RGL (per research doc 2; full stratified-negation semantics; v0.1-overscope risk), or hybrid (declarative metadata + Cedar/Datalog inline)?

5. **Storage.** `pipeline/program_rule_packs/`, extended `pipeline/rubrics/`, or `vault_shared/`? Operator authoring loop friction is the deciding factor.

6. **Funder rubric ↔ PRP `scoring_criteria` reconciliation.** §9 Judge currently uses funder's own rubric (per Judge rubric strategy). PRP carries `scoring_criteria`. Are these the same artifact (PRP IS the rubric source-of-truth) or separate (PRP carries structural gates only; rubric stays out)? Affects whether `pipeline/rubrics/vapg_fy26.json` becomes the canonical PRP or splits.

7. **Source-drift detection.** PRPs carry `source_doc_hash`. Should §4 PRE-gate include a freshness check that fetches the upstream RFA / CFR section and re-hashes, failing closed on drift? (`F-PRP-SOURCE-DRIFT`?) Or is drift detection a Heartbeat agent concern, out of §4 scope?

## §7. Sequencing options

Three viable sequences:

**Option A: Park until §4 LOCKED-as-a-whole, then §11 new-section round.** — REJECTED 2026-05-04.
- Pro: doesn't disrupt the capstone. Cleanest separation.
- Con: §4 LOCKED-as-a-whole inherits the missing-PRP gap as a known deferral.
- Estimated cost: 2 Thesis rounds for §11 v1.0 + ~5 Thesis rounds for §4 amendments to consume §11.
- **Rejection rationale:** Ships §4 with zero PRP awareness; contractor would have to retrofit the hook after LOCK.

**Option B: Interrupt capstone with §4 v2.7 PRP-load amendment, finish capstone afterward.** — REJECTED 2026-05-04.
- Pro: §4 LOCKED-as-a-whole ships PRP-aware out the gate.
- Con: blows up Round L capstone scope; risks 2026-04-29 journey map slipping by weeks.
- Estimated cost: +3 Thesis rounds before LOCK-as-a-whole.
- **Rejection rationale:** Schedule risk outweighs the benefit of shipping PRP-complete at LOCK-as-a-whole.

**Option C: Hybrid — §4 LOCKED-as-a-whole minimally PRP-aware via a thin v2.3 amendment exposing Card and PRP primitives at the schema level, full PRP semantics deferred to Phase One contractor deliverable.** — SELECTED 2026-05-04.
- Pro: §4 ships with the load-bearing hook; full semantics ship later. Schema is pinned so contractor inherits a clean interface contract.
- Con: requires the same care as v2.6 deferred-scope honesty pattern; another deferral.
- Estimated cost: +1 Thesis round before LOCK-as-a-whole + full PRP build as Phase One contractor work.
- **Selection rationale:** Lets v0.1 ship coherent without committing engineering capacity to full PRP build before contractor onboards. PRPs become a Phase One contractor deliverable with schema already pinned.

**Sequencing constraint (2026-05-04):** A6 Part 2 (compound-transaction LOCK: §4 v2.3 amendment + §0.5 v6 row addition + Thesis audit) follows A2 (v7.0.1 GPP LOCK close-out) so the amendment goes through GPP discipline.

## §8. Provenance

- `research/logician_formal_logic/01_Formalizing_Grant_Compliance_Logic.docx` — Datalog/RGL theory, NSF PAPPG / USDA SBIR / 2 CFR §200 worked examples.
- `research/capital_logic_cards/01_Capital_Logic_Cards_Architecture_v2_engineering.docx` — explicit "card grammar vs Program Rule Packs" separation; PRP schema shape v1; Farmer Card v1 as acceptance test.
- `Golden_Quill_Business_Plan_v9_Integrated.docx` — v9 §3 + Appendix B integrate Capital Logic Cards into the canonical product story; PRP separation principle is the v0.1 engineering correlate of that integration.
- `pipeline/rubrics/vapg_fy26.json` — nascent PRP on disk, extracted 2026-04-12.
- `pipeline/blueprint/v0.1/section_04_v2_6_deferred_scope_amendment.md` — v2.6 deferred-scope honesty pattern modeled here.
- `pipeline/blueprint/v0.1/section_06_operating_envelope.md` — scoping draft style modeled here.

## §9. NOT in scope of this scoping draft

- Authoring the actual amendment text. (That's a follow-on round, sequenced per §7.)
- Designing the Datalog/RGL semantics (research doc 2). v0.1 should ship without full Datalog semantics; defer to Stage-2.
- Designing the Card schema. Cards are a v9-converged research concept; PRP relates to Cards but does not require Cards to ship first.
- Re-opening the §4 v2.1 LOCK semantics. PRP work extends §4; it does not amend prior locked semantics.
- Building any tooling. Scoping only — no code, no test vectors, no implementation rounds.
