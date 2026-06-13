# BUILD-SPEC — Quality, Security & Proof (Golden Quill Node)

**Node:** `quality-security-proof` · **Context:** `CTX-QSP-ROOT` · **Workstream:** C (Quality, Security & Proof)
**Owner (QA / Measurement / Epistemics):** Victor · **Founder decisions:** Josh
**Status:** Implementation-ready (planning/spec only) · **Authored:** 2026-06-13

## 0. Provenance & Scope

This BUILD-SPEC converts Workstream C proof rows into acceptance tests and evidence gates for first-customer-node readiness. It is the Refine→Invoke (Define→Design→Plan) authoring product for the four REFINE-SOLVABLE gaps, plus an operator callout for the one decision-gated gap.

**Sources (cited by path):**
- `docs/golden-quill-task-role-breakdown-handoff.md` rows 56-61 (Workstream C), rows 96, 110, 115, 80 (After-Acceleration + Roles & Gaps).
- `docs/features/quality-security-proof/.craft/ledger.yml` (gaps[0-3], DESC-QSP-001).
- `docs/features/quality-security-proof/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md` + `REFINE-DISPATCH.json`.
- `CLAUDE.md` — Five Operating Laws; F-CLASS-* sixteen-primitive roster (v7.0.10 LOCKED 2026-05-11); F-WPFA-* twelve-code roster (§17 v1 LOCKED 2026-05-11); Beta deployment fail-closed gates.

**Guardrails honored:**
- Substrate LOCKED (Pydantic AI + Logfire + Ollama/vLLM + DSPy/GEPA + Logician/Cedar per ADR-001 / v7.0.3). No substrate proposals here.
- **Law 3 / org-isolation:** no `orgs/<slug>/` PROJECT_CONTEXT read or referenced. Test fixtures use synthetic orgs (`orgs/_TEMPLATE` shape only, never live client data).
- **Owner-boundary (rg06):** this is planning/spec authoring. It defines tests and registers; it does not implement runtime, sign anything, or claim Task Session / Sigil authority.
- This pass authors the four REFINE-SOLVABLE gaps fully. It does **not** author a fake answer for the operator-input gap (security-reviewer assignment) — that is surfaced as a callout in §6.

**Six Workstream C proof surfaces** (rows 56-61): (1) test plan + guardrails-as-tests, (2) internal deployment test, (3) independent security review, (4) claims register, (5) canonical demo standard, (6) instrumentation. This spec fully authors (1), (4), (6); records (2) and (5) as adjacent acceptance hooks consumed by the test plan; routes (3) to Josh.

---

## 1. GAP-QSP-TEST-PLAN — Guardrails-as-Tests

**Owner:** Victor · **Verdict:** refine-solvable · **Severity:** block · **Treatment:** author

### 1.1 DEFINE — what the test plan must prove

A deployment is **not customer-eligible** unless every named fail-closed gate in the canonical rosters has a concrete acceptance test that demonstrates (a) the gate **fires** on the prohibited input, and (b) the system **fails closed** (no cloud emission, no unsigned deployment, route → LOCAL) rather than failing open. The plan covers four enforcement axes drawn from the workbook row 56 mandate — *posture enforcement, classification routing, audit completeness, fail-closed coverage* — cross-walked against the actual gate primitives in `CLAUDE.md`.

**Truth source:** the test plan does not invent guardrails. It tests the Five Laws and the two locked gate rosters as they already exist. Where a gate has no test, that is a `F-CLASS-COVERAGE-INCOMPLETE`-class hole and blocks deployment.

### 1.2 DESIGN — test matrix structure

Four enforcement axes, each a test class. Every test is `(gate_id) → (prohibited input fixture) → (assert fail-closed behavior + assert audit/Logfire span emitted)`. The matrix is the deliverable; the table below is the canonical cross-walk.

**Axis A — Posture enforcement** (three v7.0.10 postures: Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign)

| Gate / Law | Prohibited input fixture | Expected fail-closed behavior | Acceptance test ID |
| --- | --- | --- | --- |
| Posture selection requires Ed25519 sign-off (v7.0.10 §1.4 step 4) | deployment manifest, posture set, no operator signature | deployment blocked; no cycle dispatch | `T-QSP-POST-01` |
| `F-CLASS-POSTURE-MID-CYCLE-CHANGE` | posture re-select issued mid-cycle | fail-closed; posture change refused until cycle close | `T-QSP-POST-02` |
| Local-Only-Sovereign route discipline | any seat call under `local_only_sovereign` | route LOCAL with no further checks; zero cloud egress observed | `T-QSP-POST-03` |
| `local_only_validated` write-protection | attempt to flip default `false`→`true` without SN-LLC quarterly signature | flip refused; "production-validated" claim ungated | `T-QSP-POST-04` |

**Axis B — Classification routing** (per-field register: public / shareable / confidential / operator_flagged)

| Gate | Prohibited input fixture | Expected fail-closed behavior | Acceptance test ID |
| --- | --- | --- | --- |
| `F-CLASS-REGISTER-UNSIGNED` | register present, operator Ed25519 missing | cycle blocked | `T-QSP-CLASS-01` |
| `F-CLASS-REGISTER-SIGNATURE-INVALID` | register signed with wrong key | verification fails; blocked | `T-QSP-CLASS-02` |
| `F-CLASS-REGISTER-HASH-MISMATCH` | register body mutated post-signature | hash mismatch; blocked | `T-QSP-CLASS-03` |
| `F-CLASS-ROUTING-INDETERMINATE` | field with indeterminate class routed | fail-closed to LOCAL default | `T-QSP-CLASS-04` |
| `F-CLASS-NEW-FACT-UNCLASSIFIED` | INCREMENTAL_INGEST fact with no class | defaults to `confidential`, pending re-class | `T-QSP-CLASS-05` |
| Frontier-Eligible routing split | confidential/operator_flagged field under frontier-eligible | routed LOCAL, never cloud | `T-QSP-CLASS-06` |
| `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` | scaffold work outside signed allow-list under Split-Context | PRE-gate blocks cloud route | `T-QSP-CLASS-07` |
| `F-CLASS-SPLIT-CONTEXT-LEAK` | applicant-fact present in pre-cloud scaffold payload | PRE-scan blocks cloud emission | `T-QSP-CLASS-08` |
| `F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` | `[SLOT_<anything>]` pattern (regex `\[SLOT_[^\]]*\]`) in cloud-routed prompt | defense-in-depth gate fires; payload blocked (deprecated mechanism — firing = bug/attack) | `T-QSP-CLASS-09` |
| Post-substance-assembly local pin | draft carrying confidential substance routed to Editor/RedTeam | all subsequent seats route LOCAL | `T-QSP-CLASS-10` |

**Axis C — Audit completeness** (every invocation, payload class, cross-boundary event, hash — workbook row 52 / Five Laws audit discipline)

| Gate | Prohibited input fixture | Expected fail-closed behavior | Acceptance test ID |
| --- | --- | --- | --- |
| Every agent invocation emits a Logfire span with payload-class label | seat call with no span | audit-incomplete; cycle cannot close clean | `T-QSP-AUDIT-01` |
| Every cross-boundary (LOCAL→cloud) event logged with hash | cloud route with no boundary event record | audit gap flagged; blocked | `T-QSP-AUDIT-02` |
| `F-CLASS-HIGH-STAKES-FLAG-LEAK` | heavy-Judge swap flag in a cloud payload | gate fires; payload blocked | `T-QSP-AUDIT-03` |
| `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` | heavy-Judge model fetched over network | blocked; model must be pre-loaded on appliance | `T-QSP-AUDIT-04` |
| `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` | router-template update unsigned/wrong-signed | stays on prior pinned version | `T-QSP-AUDIT-05` |
| `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` | Coefficient Registry signed with wrong key | blocked against white-glove-pinned pubkey | `T-QSP-AUDIT-06` |

**Axis D — Fail-closed coverage (META)**

| Gate | Prohibited input fixture | Expected fail-closed behavior | Acceptance test ID |
| --- | --- | --- | --- |
| `F-CLASS-COVERAGE-INCOMPLETE` | one required F-CLASS-* module or test missing from runtime tree | deployment blocked before any cycle | `T-QSP-COV-01` |
| WPFA receipt integrity `F-WPFA-COUNTERFACTUAL-INFLATION` | receipt baseline_model_id ≠ registry baseline_model_id | P0 audit-integrity block; not bypassable for buyer receipts | `T-QSP-COV-02` |
| `F-WPFA-OPERATOR-SIGNATURE-MISSING` | buyer-facing PDF emission with no operator Ed25519 | emission blocked (structural attestation boundary) | `T-QSP-COV-03` |
| `F-WPFA-CROSS-ORG-LEAK` | CycleReceipt write path slug ≠ receipt.org_slug | Law 3 structural block | `T-QSP-COV-04` |
| `F-WPFA-PDF-CONFIDENTIAL-LEAK` | buyer PDF would render a `confidential`-classified field | render blocked (Law 3 + v7.0.7) | `T-QSP-COV-05` |
| Five Laws as Logician PRE/POST gates | a draft claim with no RFA/PROJECT_CONTEXT trace (Law 1); silent flagged-term rewrite (Law 4); fabricated credential (Law 5) | Logician fail-closed; revision routed to operator | `T-QSP-LAW-01..03` |

**Cross-walk completeness assertion:** the sixteen F-CLASS-* primitives and twelve F-WPFA-* codes named in `CLAUDE.md` each map to at least one `T-QSP-*` test above (the four defense-in-depth + structural codes share tests where one fixture exercises the pair). The matrix file enumerates the 1:1 map and is itself checked by `T-QSP-COV-01`.

### 1.3 PLAN — first steps (Victor)

1. Create the canonical matrix file `docs/features/quality-security-proof/guardrail-test-matrix.yaml` — one row per `T-QSP-*` ID with `{gate_id, axis, fixture_ref, expected_behavior, status}`. This file is the single source the META gate checks against.
2. Author synthetic fixtures under a test-only fixtures path (synthetic orgs only — no live `orgs/` data; Law 3). One fixture per prohibited-input column.
3. Implement tests against the LOCKED Logician/Cedar gate surface (deterministic Python + Cedar; zero-token). Tests assert *fail-closed*, not just *error raised*.
4. Wire the matrix into the existing `scripts/run_tests.sh` pinned-interpreter suite (Python 3.14 `.venv` — never system `python3`).
5. Gate handoff: a deployment may not present to a customer until every matrix row is `status: pass` and `T-QSP-COV-01` (META) is green.

### 1.4 Acceptance criteria

- Every F-CLASS-* (16) and F-WPFA-* (12) code has ≥1 `T-QSP-*` test; verified by the matrix self-check.
- Every test asserts fail-closed behavior (no cloud emission / no deployment / route-to-LOCAL), not merely an exception.
- All four axes (posture / classification / audit / fail-closed) have green coverage.
- The full matrix runs under `scripts/run_tests.sh` and exits 0.
- No fixture references live client data (Law 3 self-check).

---

## 2. GAP-QSP-CLAIMS-REGISTER — Claim → Evidence-Category Mapping

**Owner:** Victor (Josh approves any claim touching sales copy) · **Verdict:** refine-solvable · **Severity:** flag · **Treatment:** author

### 2.1 DEFINE

Every external/customer-facing claim Golden Quill makes must trace to an evidence category before sales material hardens (row 59). The discipline is modeled directly on the WPFA buyer-facing chain in `CLAUDE.md` §17: *every claim links to coefficient + cycle_id + Logfire trace_id*. Generalized, every claim links to **evidence_category → evidence_handle → trace/provenance ref**, and a claim with no resolvable evidence handle may not ship.

### 2.2 DESIGN — register schema

Register file: `docs/features/quality-security-proof/claims-register.yaml`. One entry per claim:

```yaml
- claim_id: CLM-QSP-NNN
  claim_text: "verbatim external claim"
  surface: [sales_one_pager | demo | website | LOI | validation_packet | node_care]
  evidence_category: <one of the closed set below>
  evidence_handle: <concrete artifact path / test ID / coefficient ID / cycle_id>
  provenance_ref: <Logfire trace_id | signed-receipt id | reviewer sign-off id | "n/a-structural">
  classification_check: <pass|fail>   # may not render confidential field (mirrors F-WPFA-PDF-CONFIDENTIAL-LEAK)
  sales_touch: <true|false>           # if true → Josh approval required before ship
  status: [draft | evidenced | approved | shipped]
```

**Closed set of evidence categories** (each maps to a producing surface already in the system):

| evidence_category | Backed by | Example handle |
| --- | --- | --- |
| `guardrail-test` | §1 test matrix | `T-QSP-CLASS-06` |
| `security-review` | independent reviewer sign-off (GAP-QSP-SECURITY-REVIEWER) | reviewer report id |
| `wpfa-receipt` | WPFA CycleReceipt (§17) | `coefficient_id` + `cycle_id` + `trace_id` |
| `instrumentation-metric` | §3 instrument definitions | `INS-QSP-*` metric id |
| `demo-integrity` | canonical demo standard (row 60 — live, never staged-as-live) | demo run log id |
| `deployment-test` | internal deployment test (row 57) | install-from-checklist run id |
| `architecture-lock` | locked architecture / Five Laws | `CLAUDE.md` clause ref |
| `structural-attestation` | operator Ed25519 boundary | signature id (`provenance_ref: n/a-structural` where boundary, not measured) |

### 2.3 PLAN — first steps (Victor)

1. Seed the register by harvesting every claim currently implied by Workstream E sales scope and the validation packet (row 80) — but author **only the schema rows and evidence mapping**, not the sales copy itself.
2. For each claim, resolve a concrete `evidence_handle`; any claim that cannot resolve one is marked `status: draft` and flagged as **unshippable** until evidenced.
3. Mark `sales_touch: true` on every claim destined for customer-facing copy; these route to Josh for approval (business judgment per RESEARCH-RESULT r03).
4. Add a CI/self-check: a claim with `status: shipped` and an unresolved `evidence_handle` or `classification_check: fail` fails the check (mirrors `F-WPFA-PDF-CONFIDENTIAL-LEAK` discipline).

### 2.4 Acceptance criteria

- Every entry has a non-empty `evidence_category` (from the closed set) and a resolvable `evidence_handle`.
- No `shipped` claim has `classification_check: fail`.
- Every `sales_touch: true` claim carries a recorded Josh approval before `status: shipped`.
- Register self-check runs in the pinned suite and exits 0.

### 2.5 Cross-node consumer

This register **feeds `sales-contracting-legal`** (Workstream E) sales materials. The contract is: sales-contracting-legal may use a claim in customer-facing copy **only** if its `claims-register.yaml` entry is `status: approved` (evidenced + Josh-signed for sales-touch). The claims register is the upstream gate; sales copy is the downstream consumer.

---

## 3. GAP-QSP-INSTRUMENTATION — Instrument Definitions

**Owner:** Victor · **Verdict:** refine-solvable · **Severity:** flag · **Treatment:** author

### 3.1 DEFINE

Define the instruments that capture support-load, usage baselines, and renewal intent before first node, so the After-Acceleration data room (row 96: "measured unit economics, support-load evidence, renewal data") and the white-glove Day-60 review (row 76) have real numbers, not estimates. Vocabulary is sourced from the WPFA CycleReceipt primitive (`CLAUDE.md` §17) — typed, per-org, per-cycle, deterministic, with Decimal/int-micro-watt-hour discipline (A12 mandate; no float).

### 3.2 DESIGN — instrument definitions

Definitions file: `docs/features/quality-security-proof/instrument-definitions.yaml`. Each instrument:

```yaml
- instrument_id: INS-QSP-NNN
  metric_name: <name>
  unit: <unit; Decimal or int per A12 — no float>
  source: <CycleReceipt field | support issue log (row 78) | Day-60 review (row 76)>
  capture_cadence: [per-cycle | per-node | per-quarter | ongoing]
  baseline_target: <value or "TBD-first-node">
  consumer: [data-room | day-60 | validation-packet | node-care]
```

**Canonical instruments (first set):**

| instrument_id | metric | unit | source | cadence | consumer |
| --- | --- | --- | --- | --- | --- |
| `INS-QSP-SUPPORT-HRS` | support hours / node | Decimal hours | support issue log (row 78) triage records | per-node, ongoing | data-room, day-60 |
| `INS-QSP-USAGE-CYCLES` | grant cycles run / node / quarter | int count | CycleReceipt count per org_slug | per-quarter | data-room, validation-packet |
| `INS-QSP-USAGE-DOLLARS` | actual dollars consumed vs counterfactual | Decimal USD | CycleReceipt (actual vs flagship baseline) | per-cycle | data-room, validation-packet |
| `INS-QSP-USAGE-ENERGY` | watt-hours consumed | int micro-watt-hours (A12, no float) | CycleReceipt energy field | per-cycle | data-room |
| `INS-QSP-RENEWAL-INTENT` | renewal-intent signal | enum {strong, neutral, at-risk} + free note | Day-60 use review (row 76) | per-node at Day-60, ongoing | data-room, node-care |
| `INS-QSP-BASELINE-USAGE` | first-30-day usage baseline / node | int cycles + Decimal hours | CycleReceipt + support log | per-node (Day 0–30) | day-60, validation-packet |

### 3.3 PLAN — first steps (Victor)

1. Author the definitions file with the six instruments above; derive every CycleReceipt-sourced field name from the existing §17 sub-kind (do not invent receipt fields).
2. For each instrument, name the exact source field/log and the consumer; mark baselines `TBD-first-node` where no data exists yet.
3. Define the Day-60 capture form fields (renewal-intent enum + note) so Customer Success (row 76) captures them consistently.
4. Confirm A12 Decimal/int discipline: assert no instrument uses float; energy in int micro-watt-hours.

### 3.4 Acceptance criteria

- Six instruments defined with `unit`, `source`, `cadence`, `consumer` populated.
- Every CycleReceipt-sourced field name matches an existing §17 receipt field (no invented fields).
- No instrument unit is float (A12 self-check).
- Renewal-intent capture form fields enumerated for Day-60.

### 3.5 Cross-node consumers

Instrumentation **feeds `company-operations-finance`** (the validation packet, row 80) **and `white-glove-delivery-node-care`** (the Day-60 use review, row 76). Contract: those nodes consume `INS-QSP-*` metric ids; this node owns the definitions and the A12-clean capture discipline. The validation packet pulls `data-room` consumers; Day-60 pulls `day-60` consumers.

---

## 4. Adjacent Workstream-C surfaces (recorded, not separately authored)

These two rows are owned by this node but are consumed *as evidence hooks* by the artifacts above rather than authored as standalone gaps in this pass:

- **Internal deployment test (row 57)** — "full install from checklist by someone who didn't write it." Surfaces as evidence category `deployment-test` (§2.2) and as the install-run handle consumed by the claims register. First step: Victor authors the install-from-checklist run protocol; a passing run id becomes a claims-register evidence handle.
- **Canonical demo standard (row 60)** — "Scout population sequence — live, never staged-as-live." Surfaces as evidence category `demo-integrity` (§2.2). First step: Victor defines the live-demo integrity checklist (the prohibition on staged-as-live is itself a guardrail testable under §1 Axis C audit completeness — demo runs must emit real Scout spans).

---

## 5. Cross-Node Consumer Map (summary)

| This node produces | Consumed by | Contract |
| --- | --- | --- |
| `claims-register.yaml` | `sales-contracting-legal` (Workstream E sales materials) | sales copy may use a claim only if its register entry is `status: approved` |
| `instrument-definitions.yaml` (`data-room` consumers) | `company-operations-finance` (validation packet, row 80) | finance pulls `INS-QSP-*` ids; QSP owns definitions + A12 discipline |
| `instrument-definitions.yaml` (`day-60` consumers) | `white-glove-delivery-node-care` (Day-60 review, row 76) | Day-60 captures renewal-intent + usage baseline via QSP-defined form |
| `guardrail-test-matrix.yaml` | `tilth-runtime-build`, `hardware-golden-image` (gates they must pass) | a build is deployment-eligible only when the matrix is green |

---

## 6. OPERATOR-INPUT CALLOUT (do not author)

### GAP-QSP-SECURITY-REVIEWER — independent security reviewer is onboard-now but unassigned

**Owner:** Josh · **Verdict:** operator-input (staffing/assignment — business judgment, not a research or spec question).

The workbook (rows 58, 115) lists an independent External Security Reviewer covering **data-boundary enforcement, Sovereign build, and signing chain**, onboard-now, one-time + recurring at major releases. The *role and scope* are defined; the **assignment of a named person/firm is an open operator decision** that this spec deliberately does not invent.

**What Josh decides:**
1. Assign a named reviewer (person/firm) to the role.
2. Confirm scope-of-work: boundary enforcement + Sovereign build + signing chain (deferred bounded request **B1** in RESEARCH-RESULT can supply scope-of-work exemplars *if* Josh approves an external pass — currently deferred under rg03).
3. Set the recurrence trigger (which releases count as "major").

**Dependency note:** the claims register evidence category `security-review` (§2.2) and the test-plan axes for boundary/signing (`T-QSP-CLASS-*`, `T-QSP-AUDIT-05`) have a downstream dependency on the reviewer's independent sign-off. Until the reviewer is assigned and reports, any claim relying on `evidence_category: security-review` stays `status: draft` (unshippable). This does not block authoring §1–§3; it blocks *shipping security-review-backed claims*.

---

## 7. Per-Gap Verdict Lines

```
GAP-QSP-TEST-PLAN       | Victor | refine-solvable | authored: 4-axis guardrail test matrix cross-walking all 16 F-CLASS-* + 12 F-WPFA-* + Five Laws to T-QSP-* acceptance tests; Victor builds guardrail-test-matrix.yaml + synthetic fixtures, wires to scripts/run_tests.sh | docs/features/quality-security-proof/BUILD-SPEC.md §1
GAP-QSP-CLAIMS-REGISTER | Victor | refine-solvable | authored: claim→evidence-category schema (8-category closed set on WPFA claim→coefficient→cycle_id→trace_id model); Victor seeds claims-register.yaml, resolves evidence handles, routes sales-touch claims to Josh | docs/features/quality-security-proof/BUILD-SPEC.md §2
GAP-QSP-INSTRUMENTATION | Victor | refine-solvable | authored: 6 instrument definitions (support hrs/node, usage cycles/dollars/energy, renewal-intent, 30-day baseline) sourced from WPFA CycleReceipt vocab w/ A12 Decimal discipline; Victor authors instrument-definitions.yaml + Day-60 capture form | docs/features/quality-security-proof/BUILD-SPEC.md §3
GAP-QSP-SECURITY-REVIEWER | Josh | operator-input | decide: assign named independent reviewer + confirm boundary/Sovereign/signing-chain scope + set major-release recurrence; gates shipping of security-review-backed claims only, does not block §1-§3 authoring | docs/features/quality-security-proof/BUILD-SPEC.md §6
```
