# Plan Review Findings

**Dispatch:** `2026-07-28-body-war-login-score-plan-review`  
**Verdict:** **REVISE; no CRITICAL finding.**  
**Evidence boundary:** frozen verification by Rittel, Horst ended
`NO_OBJECTION`; see [`attacks.md`](./attacks.md#rittel-horst--frozen-verification).
These are change requests only. They do not implement fixes, select an SWU, or
authorize execution.

## `SPEC.md` and `ARCHITECTURE.md`

| # | file | quoted/literal evidence | severity | proposed fix |
| --- | --- | --- | --- | --- |
| SYN-JSP-001 | `SPEC.md:114-131,180-189,214-227`; `ARCHITECTURE.md:146-173` | `ScorePreview` stores `evidenceActivityIds[]` and derived points, while calculation may use “one unique day” and V0 allows “one qualifying day maximum until history is fetched.” The persisted score key promises a unique “geometry + policy + evidence digest,” but no canonical input snapshot is defined; geometry explicitly retains warm-up, commute, or unrelated segments. | **MAJOR — local fixture blocker** | Add a versioned `ScoreInputSnapshot` containing the window anchor/timezone, eligibility, canonical evidence-set and geometry/policy digests, per-activity metrics, aggregation, and provenance. Require explicit segmentation or label/suppress non-comparable sparse-history totals. |
| SYN-JSP-002 | `SPEC.md:229-244`; `ARCHITECTURE.md:117-152` | The API declares three mutating POST routes, then requires “one idempotent orchestration boundary.” The single proposed key contains principal, track, activity, consent version, and policy version, while the persisted derived stages require derivation and evidence identity. | **MAJOR — local fixture blocker** | Define one resumable command plus read selector and separate canonical identities for confirmation, geometry, and score. |
| SYN-JSP-003 | `SPEC.md:149-168`; `ARCHITECTURE.md:237-252` | Geometry fetch must “authenticate the activity as owned” and “fail closed on ownership mismatch,” but the sequence persists “confirmation + redacted evidence” before the detail/stream call and compensation says to “retain the confirmation/evidence stage” if that call fails. | **MAJOR — shared L0 contract** | Validate fake ownership before attaching evidence in L0; retain only a non-evidence pending intent until validation succeeds. Keep live provider/account revalidation in the real-provider lane. |

**Artifact verdicts:** `SPEC.md` — **FIX**; `ARCHITECTURE.md` — **FIX**.

## `DESIGN-SCOPE-MANIFEST.json` and denominator

| # | file | quoted/literal evidence | severity | proposed fix |
| --- | --- | --- | --- | --- |
| SYN-JSP-004 | `DESIGN-SCOPE-MANIFEST.json:264-313`; `ARCHITECTURE.md:88-91,154-169,333-340,385-390` | The rule says raw streams must avoid “persistence and logging,” but `data_and_log_sinks` lists only `sink:journey-persistence`. Architecture also names errors, structured logs, test snapshots, receipts, and raw-stream/token canary checks. | **MAJOR — local no-leak blocker** | Enumerate and sentinel-test every active L0 application, error, log, test, snapshot, and receipt sink; extend the denominator later for hosted access/trace sinks. |
| SYN-JSP-007 | `DESIGN-SCOPE-MANIFEST.json:358-393`; `DESIGN-DENOMINATOR-RECEIPT.json:35-84`; `EXECUTION-PACK.md:14-19` | Each planned acceptance claim is encoded as `"evidence_state": "authored-complete"`, while the execution pack says “no SWU is selected,” “no Task Session preflight has run,” and no live-provider action is authorized. | **MINOR — Plan evidence-lane repair** | Rename the state to `contract_authored`, add `execution_state: not_run`, and keep receipt selectors nullable until validated. |
| SYN-JSP-010 | `DESIGN-SCOPE-MANIFEST.json:282-298`; `ARCHITECTURE.md:355-364,423-424` | Both `effect:external-strava-read` and `effect:persist-private-geometry` carry `"reversible": true`, while geometry deletion is still bound to a future policy and `GAP-JSP-002` is open. | **MINOR — taxonomy repair** | Distinguish irreversible reads, compensability, and policy-bound deletion capability. |

**Artifact verdicts:** `DESIGN-SCOPE-MANIFEST.json` — **FIX**;
`DESIGN-DENOMINATOR-RECEIPT.json` — **FIX**.

## `CONTEXT-PACK.md` and `ONTOLOGY-MAP.md`

| # | file | quoted/literal evidence | severity | proposed fix |
| --- | --- | --- | --- | --- |
| SYN-JSP-008 | `CONTEXT-PACK.md:25-52`; `DESIGN-SCOPE-MANIFEST.json:12-87`; `ONTOLOGY-MAP.md:70-78` | O6 marks the BWOI proof-track boundary “covered” and selects its prior `SPEC.md`, while the Design inclusion list has no selector for it. The ontology promises “no bridge claim without selector/digest.” | **MINOR — traceability only** | Bind the prior proof explicitly as immutable historical CT-2-only context, or mark O6 `informed`, not `covered`. No Craft recomposition is required. |

**Artifact verdicts:** `CONTEXT-PACK.md` — **FIX**; `ONTOLOGY-MAP.md`
— **FIX**.

## `app/src/auth/strava-oauth.ts`

| # | file | quoted/literal evidence | severity | proposed fix |
| --- | --- | --- | --- | --- |
| SYN-JSP-005 | `app/src/auth/strava-oauth.ts:120-157`; `ARCHITECTURE.md:79-91,344-351` | The callback parses `tokenResponse.scope` and immediately persists it without rejecting loss of the required activity scope. The plan says refresh replaces tokens “atomically,” but its concurrency section specifies only journey keys and no account-row CAS or singleflight. | **MAJOR — real-provider only** | Validate required accepted scopes; use account-row version/CAS or singleflight refresh, reread, bounded retry, and most-recent-token persistence. |

**Artifact verdict:** **FIX in the real-provider lane; not an L0 blocker.**

## Hosted work, dispatch, and layering

| # | file | quoted/literal evidence | severity | proposed fix |
| --- | --- | --- | --- | --- |
| SYN-JSP-006 | `WORK-PACK.md:189-238`; `EXECUTION-DISPATCH.json:169-205,327-342`; `IMPLEMENTATION-LAYERING.md:63-84` | Work Pack has separate `SWU-JSP-HOST-001 — Admission Package` and `SWU-JSP-WITNESS-001 — One Supervised Execution`, but dispatch step `s5` is “Admit and run” with one generic receipt requiring only status/artifacts/validation/audit/residue. Layering calls the hosted one-attempt route L2; Work Pack calls it L3. | **MAJOR — hosted only** | Split HOST receipt → explicit parent admit/reject gate → separately authorized WITNESS receipt; add a claim-specific receipt schema and standardize lane vocabulary. |

**Artifact verdicts:** `WORK-PACK.md` — **FIX**;
`EXECUTION-DISPATCH.json` — **FIX**; `IMPLEMENTATION-LAYERING.md` —
**FIX**.

## `UX-PLAN.md`

| # | file | quoted/literal evidence | severity | proposed fix |
| --- | --- | --- | --- | --- |
| SYN-JSP-009 | `UX-PLAN.md:78-89,104-113` | The responsive contract and browser witnesses name only 320px and 390px widths; no explicit viewport-height, 200% text, long-content, or orientation witness appears. The keyboard order contains selection, consent, submit, and result but no text-entry control. | **MINOR — moderated-local hardening** | Add height, 200% text, long-content, and orientation witnesses; do not add a software-keyboard witness to this non-text-entry flow. |

**Artifact verdict:** **FIX**.

## Severity-Ordered Change Requests

1. **MAJOR — local fixture blockers:** SYN-JSP-001, SYN-JSP-002,
   SYN-JSP-004.
2. **MAJOR — shared contract:** SYN-JSP-003, with live ownership proof
   deferred.
3. **MAJOR — real-provider only:** SYN-JSP-005.
4. **MAJOR — hosted only:** SYN-JSP-006.
5. **MINOR — non-blocking:** SYN-JSP-007 through SYN-JSP-010.

## Dropped Finding

**Mandatory split of SWU-JSP-005 — REFUTED.** The frozen verifier confirmed that
L0 idempotency is intentional and the unit has one orchestration/API owner,
acceptance set, and atomicity verdict. Correct SYN-JSP-002 inside the unit;
split only if later sizing evidence proves it non-atomic.

## Parent Approval

Accepted as the dispatch change-request list. Every surviving finding above is
cited to the frozen verified return and current artifact bytes; the refuted SWU
split is not present as a change request. Acceptance closes the review, but
does not apply these fixes or grant implementation authority.
