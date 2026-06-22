# REVIEW — MTNG v2 build spec (red-team, dispatched)

> **Bridge layer (NON-SOURCE).** This is the parent's synthesis of a tensioned, gated review
> dispatch — change requests, not source claims. Local-only. Claim ≤ proof: every finding cites
> a spec section the parent independently confirmed against `01-MTNG-build-spec-v2.md` (P8).

- **Dispatch:** `2026-06-22-mtng-v2-review` · `dispatch_type: review` · schema v0.6.0
- **Gate:** check-tension PASS/PASS (Brandenburg checker, Gödel reviewer — agreed)
- **Lenses (tensioned, axis = attack-vector):** A = Russell (necessity → DEFER), B = Capucci (readiness → FIX-THEN-BUILD). Raw returns in `_dispatch/lens-A.md`, `_dispatch/lens-B.md`.
- **Aggregation:** parent synthesis (P7 — not a bare concat); parent = `final_approver` (P12).

---

## Owning verdict — **FIX-AND-PROVE BEFORE BUILD** (a bounded defer)

The two lenses split exactly on their predicted axis, and the split is *real but narrow*: **both
say do not write production code against this spec yet.** They differ only on what the defer is
*for*.

- Russell (necessity): defer until the **value delta** over a flat-summary-plus-template baseline
  is measured — the load-bearing claim (R-VPR) is untested and the spec admits it.
- Capucci (readiness): grant the value, but fix the **build-safety preconditions** first — an
  unverified integration surface (Phase 0), an unimplementable merge step, an unfalsifiable
  pilot, and three contradictory node schemas.

The parent reconciles these as **complementary gates on the same go decision, ordered by cost**:
Russell's value-proof gate is *cheaper* than Capucci's Phase 0 and should run first — if the
packager can't beat a disciplined template, the integration work is moot. So:

> **Gate 0 (go/no-go, cheapest):** pre-register a falsifiable head-to-head — MTNG packet vs a
> disciplined flat summary + standard issue template, fixed metric, independent judge, bounded
> overhead. If it doesn't win, stop. *(Russell F1 = Capucci F3 = R-VAL/R-VPR.)*
> **Gate 1 (build-safety, only if Gate 0 passes):** Phase 0 against the real repo *or* a
> standalone-CLI declaration (Capucci F1); a merge schema + conflict predicate (F2); one
> canonical node schema (F7); an engine-authority policy table (F4).
> **Gate 2 (tuning):** classifier-accuracy harness (F5/R-CLS) and overhead budget (F6/R-OVH).

This is neither KILL (the underlying discipline is sound and the residue map is honest) nor
immediate FIX-THEN-BUILD (you would be fixing the build before knowing it's worth building).

## Consolidated findings (deduped, severity-ranked)

| # | Finding | Sev | Spec | Lens | Residue |
|---|---|---|---|---|---|
| **C1** | **Value proposition untested** — pilot criteria qualitative, no baseline/metric/judge; "more actionable than a flat summary" never measured. | **blocker** | §21, §25 | A-F1 + B-F3 | R-VPR, R-VAL |
| **C2** | **Phase 0 unperformed** — build order opens with integration mapping whose inputs (the repo) aren't in hand; ResonantOS internals asserted, not mapped. | **blocker** | §10, §24-S0 | B-F1 | R-INT |
| **C3** | **Mode/Routing-Signature detection** substring-based, no method spec, accuracy unmeasured; `confidence` unpopulated; "dominant mode" undefined; the core failure point per two prior reviewers. | major | §5, §13, §22, §23 | A-F4 + B-F5 | R-CLS |
| **C4** | **Recombination is prose, not a schema** — no merge algorithm, no conflict-detection predicate, no required-node-unsatisfied rule. | major | §17, §22 | A-F6 + B-F2 | R-MRG |
| **C5** | **Engine authority policy undefined** — "accepts/rejects according to policy" with no policy; no Guardian in standalone V1; `AuditEvent.actor_ref` can't distinguish engine-auto from human. | major | §9, §10, §22 | B-F4 | R-AUT |
| **C6** | **Apparatus unjustified for the single-developer pilot** — 8 emitted artifacts; contribution records are write-only (no V1 consumer, valuation forbidden); branch triggers partly co-fire by construction. | major | §1, §12, §19 | A-F2 + A-F3 + A-F5 | — |
| **C7** | **Overhead unestimated** — criterion #8 ("acceptable overhead") has no cost model, budget schema, or RunProfile budget field. | minor | §9, §21#8, §22 | A-F7 + B-F6 | R-OVH |
| **C8** | **Schema drift + OKF unverified** — node schema differs across §14/§22 (`output_artifact{type,path}` vs `output_artifact_type`, `assigned_tool` only in §22); §23 singular `validator` vs list; `merge_target` in no schema; OKF "Format" vs "Framework", existence unpinned. | minor | §14, §20, §22, §23 | B-F7 | R-OKF |

## Concrete change-request shortlist (what to do, in order)

1. **Freeze a falsifiable value criterion** (`experiment` skill): baseline = disciplined flat
   summary + issue template; ≥1 quantitative metric (e.g. validator recall on N seeded-missing-
   info fixtures, threshold stated); independent judge; the no-go condition §27 Q8 asks for. *(C1)*
2. **Resolve the integration surface:** run Phase 0 on the real repo and publish a mapping table,
   *or* declare V1 a standalone CLI and strike §10/§11 from the V1 path. *(C2)*
3. **Specify the merge:** conflict-detection predicate, required-node-unsatisfied behavior
   (emit-with-`blocked` section), a `conflicts[]` field, one worked example. *(C4)*
4. **Publish one canonical `BranchNode` schema** referenced by §14/§22/§23; reconcile `validator`
   cardinality (list everywhere); place `assigned_tool`/`merge_target`/`contribution_hooks` once. *(C8)*
5. **Add an engine acceptance-policy table** and constrain `actor_ref` to an enum. *(C5)*
6. **Trim the pilot:** ship `developer-issue-packet.md` + `validator-report.md` + `audit-log.jsonl`;
   defer contribution records + OKF until a named consumer exists. *(C6, C8)*
7. **Add a detection-method spec + accuracy harness** and an **overhead budget**. *(C3, C7)*

## Subagent closeout ledger (research-tower subagent-closeout-rule + G8)

| Lane | Assigned question | Evidence returned | Integration decision | Rejected/blocked | Final status | Follow-up owner |
|---|---|---|---|---|---|---|
| **check-tension/checker** (Brandenburg) | Is the review sheet genuinely tensioned (Tests 1–4)? | VERDICT PASS, all 4 tests | Gate passed → sheet to human | — | `closed` (infra) | — |
| **check-tension/reviewer** (Gödel) | Independent verdict + Test-3 collapse risk | VERDICT PASS; "red-team is the shared role, not the gate" | Gate passed (both agree) | — | `closed` (infra) | — |
| **lens-A** (Russell, necessity) | Should the packager exist, or is it ceremony? | 7 findings, verdict DEFER | **integrated** → C1,C3,C4,C6,C7 | none rejected; F2(template-equivalence) folded into C6 framing not a standalone CR | `integrated` | parent |
| **lens-B** (Capucci, readiness) | Is the spec safe to build as written? | 7 findings, verdict FIX-THEN-BUILD | **integrated** → C1–C5,C7,C8 | F7 sub-claim "§22 lacks contribution_hooks" **corrected** (it's present; `merge_target` is the absent field) — finding kept, error noted | `integrated` (1 correction) | parent |

No lane left implicit, unreviewed, or open. The two helper/gate agents are infrastructure
(not registered as a dispatch); recorded here and in the close row's `agents_spawned`.

## Exit

- **exit_reason:** `resolved` — the axis disagreement (DEFER vs FIX-THEN-BUILD) was *reconcilable*
  into one ordered gate sequence; not `dissent_irreconcilable`.
- Closes **R-DST** (the v1-vs-v2 endorsement gap): v2-as-written has now been reviewed on its own
  terms, not on the Analog 6 PDF's praise for the larger v1.
- Partially advances **R-AUT** (C5 gives the concrete fix) — moved from PARTIAL to "fix specified."
