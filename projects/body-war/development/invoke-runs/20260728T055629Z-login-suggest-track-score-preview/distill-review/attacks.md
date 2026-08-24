# Review Attack Transcript

Dispatch: `2026-07-28-body-war-login-score-plan-review`

Evidence boundary: verbatim subagent returns from the registered review. These
returns are candidate review evidence, not fixes, execution authority, or a
prototype-readiness verdict.

## Abramsky, Samson — Initial Position

Abramsky, Samson — initial verdict: **REVISE**. No CRITICAL finding; mutation remains blocked.

1. **MAJOR — BWOI evidence does not compose into this wider journey.** `CONTEXT-PACK.md:32,51` marks O6 covered using the prior proof track, but `DESIGN-SCOPE-MANIFEST.json:107-137` omits that selector and still declares `unknowns: []` at line 395. The prior proof owns CT-2 only (`...20260727.../SPEC.md:21-29,122-129`); its terminal receipt says wider SuggestedTrack claims remain outside scope (`.craft/ledger.yml:1034-1044`). BWOI receipts merely inform the child (`.craft/ledger.yml:1131-1158`), while the recomposition list has no SuggestedTrack/BWOI entry (`.craft/ledger.yml:1160-1181`). Thus `ONTOLOGY-MAP.md:78` claims exact selector/digest traceability that the Design denominator does not carry.  
   **Fix:** classify BWOI as historical CT-2 evidence only; bind its exact selector and ceiling, or require a separately authorized recomposition/bridge receipt before it supports O6.

2. **MAJOR — HOST-01 and WITNESS-01 collapse at execution, and L2/L3 meanings drift.** Research explicitly separates admission, execution, and repeat safety (`findings.md:142-183,185-222,232-251`) and assigns the parent an admit/reject act (`findings.md:295-305`). Yet `EXECUTION-DISPATCH.json:169-200` combines “admit and run” in one step with only `T-JSP-STRAVA-003` output; `WORK-PACK.md:260-271` likewise reviews HOST/WITNESS as one atomic row. Meanwhile L2 means hosted real-provider in `IMPLEMENTATION-LAYERING.md:63-73`, but only gateway code in `WORK-PACK.md:189-219`; hosted work moves to L3 at lines 220-238.  
   **Fix:** create distinct HOST admission and WITNESS execution steps/receipts separated by an explicit parent gate, and use one stable lane vocabulary.

3. **MAJOR — SWU-JSP-005 is task-shaped and silently absorbs RF-01.** It owns consent identity, staged orchestration, multiple API routes, recovery, duplicate semantics, and authority controls (`WORK-PACK.md:119-134`). That combines LP-01, the new geometry/score journey, and RF-01, although research says RF-01 gates repeat/retry and is not required for the contained first witness (`findings.md:232-251`). Because SWU-005 precedes every local and hosted gate, RF-01 becomes an undeclared first-witness precondition.  
   **Fix:** split exact confirmation/LP-01, journey orchestration, and repeat-safe RF-01 into independently selectable units with an explicit containment decision.

4. **MAJOR — Score evidence cannot be deterministically recomposed.** Calculation requires qualifying activity evidence inside candidate geometry (`SPEC.md:180-189`), but `ScorePreview` stores IDs and component outputs without a canonical input/evidence digest (`SPEC.md:114-131`), while persistence promises uniqueness by an unspecified “evidence digest” (`ARCHITECTURE.md:146-153`). Raw streams are discarded, and no operation maps plural `evidenceActivityIds[]` to qualifying geometry measurements. DEC-JSP-001 also omits window anchor/timezone, eligible sport/activity rules, pace aggregation, and history acquisition (`SPEC.md:214-227`; `ARCHITECTURE.md:289-303`). Owner ratification could therefore “complete” while calculation remains non-total.  
   **Fix:** define and persist a versioned canonical `ScoreInputSnapshot` with eligibility, window/timezone, per-activity derived metrics, geometry/evidence digests, aggregation, and provenance.

5. **MAJOR — API operations do not realize the declared orchestration semantics.** The API exposes three independent mutating POSTs (`SPEC.md:231-240`) while immediately requiring one idempotent orchestration boundary (`SPEC.md:242-244`). Architecture says the journey orchestrator consumes one confirmation request and resumes staged effects (`ARCHITECTURE.md:73,117-142`), but no route is assigned that semantic ownership.  
   **Fix:** designate one command endpoint as the durable orchestrator; make stage endpoints internal or idempotent read/resume surfaces.

6. **MINOR — Reversibility is overstated.** External Strava reads and private-geometry persistence are marked reversible (`DESIGN-SCOPE-MANIFEST.json:282-298`) although a read cannot be undone and deletion policy is unratified.  
   **Fix:** model compensability/deletion separately from reversibility.

7. **MINOR — Authored contracts look like completed evidence.** All acceptance claims use `evidence_state: authored-complete` (`DESIGN-SCOPE-MANIFEST.json:358-393`), then feed a `design-validator-pass`, despite witnesses remaining planned.  
   **Fix:** rename to `contract_authored`; carry `execution_state: not_run`.

Defended zero-finding attempts: every declared local source digest matches current bytes; Dispatch Spec and Design validators pass; all four planned npm commands exist. No SWU is selected and execution is explicitly blocked (`EXECUTION-PACK.md:14-30`). Fake/real and promotion ceilings are consistently stated. Current official Strava documentation supports the listed activity/detail/stream endpoints and scope distinction ([API reference](https://developers.strava.com/docs/reference/), [authentication](https://developers.strava.com/docs/authentication/)). No files changed.

## Ashby, W. Ross — Initial Position

Initial adversarial position — Ashby, W. Ross. Read-only; no files changed. All 20 non-distill artifacts were reviewed, and all 15 manifest inclusion digests match current bytes.

`JSP = projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview`

1. **CRITICAL — Machine-readable evidence is falsely complete.** `${JSP}/DESIGN-SCOPE-MANIFEST.json:360-390` marks local, moderated-human, real-provider, score, and authority acceptance claims `authored-complete`; the denominator repeats this at `DESIGN-DENOMINATOR-RECEIPT.json:38-82`. Yet `ARCHITECTURE.md:394-402` says every witness is merely planned, and `EXECUTION-PACK.md:14-19` says no execution is authorized. Failure trace: a downstream selector consumes `authored-complete`, admits hosted/human work, and treats authored witness text as evidence. **Fix:** encode these as `planned|required`, populate receipt selectors, and permit `complete` only after receipt validation.

2. **MAJOR — OAuth admission and refresh are race-unsafe.** Current callback stores whatever accepted scope is returned without rejecting missing `activity:read` (`app/src/auth/strava-oauth.ts:125-157`). The plan says refresh updates ciphertexts atomically (`ARCHITECTURE.md:88-90`) but defines no per-account lock/CAS while concurrency controls cover only journey writes (`ARCHITECTURE.md:344-351`). Two requests can read the same expiring refresh token; one rotation invalidates it while the other fails or overwrites newer credentials. Strava explicitly says returned refresh tokens rotate and the older token becomes invalid immediately ([authentication contract](https://developers.strava.com/docs/authentication/)). **Fix:** validate accepted scope at callback and use row-versioned CAS/singleflight refresh with one reread/retry.

3. **MAJOR — Ownership is revalidated after durable evidence mutation.** The workflow writes confirmation/redacted evidence before fetching detail/streams (`ARCHITECTURE.md:237-243`), and compensation retains that evidence when provider fetch fails (`ARCHITECTURE.md:247-252`), although the spec requires authenticated ownership and fail-closed behavior (`SPEC.md:161-168`). Failure trace: activity was listed, account is relinked or visibility/scope changes, detail ownership fails, but `evidence_submitted` remains for an unverified current binding. **Fix:** revalidate provider account/activity ownership before attaching candidate evidence, or persist only a non-evidence pending intent until validation passes.

4. **MAJOR — Raw-stream “no leak” has no complete sink model.** The manifest’s only `data_and_log_sinks` entry is journey persistence (`DESIGN-SCOPE-MANIFEST.json:300-313`) despite the normative rule covering logging (`:264-270`) and architecture mentioning errors, logs, snapshots, and receipts (`ARCHITECTURE.md:88-91,154-169`). Failure trace: malformed `latlng` enters an exception detail or HTTP diagnostic, then structured logging records it even though raw arrays never reach Postgres. **Fix:** enumerate application/error/access/trace/test/receipt sinks and run sentinel leak tests against every sink.

5. **MAJOR — Idempotency conflates confirmation with derived outputs.** The key includes policy version but omits consent digest, derivation version, policy digest, and canonical evidence-set digest (`ARCHITECTURE.md:117-142`; manifest concurrency at `DESIGN-SCOPE-MANIFEST.json:233-242`). Meanwhile three mutation routes are exposed before promising one orchestration boundary (`SPEC.md:229-244`). Failure trace: policy V2 yields a new key and duplicates the same confirmation/evidence; alternatively new 14-day evidence arrives under V1 and replay returns a stale completed score. **Fix:** separate keys: confirmation `(principal,track,activity,consent digest)`, geometry `(confirmation,derivation digest)`, score `(geometry,policy digest,evidence-set digest)` behind one resumable command/read selector.

6. **MAJOR — Geometry and score are circular and sparse-history output is numerically misleading.** The selected activity creates the candidate geometry and then contributes distance/pace to its own score (`SPEC.md:170-190`); approach/exit segments are deliberately not removed (`ARCHITECTURE.md:171-173`, acknowledged risk at `:426`). The same one activity may contribute `1/14` frequency (`SPEC.md:218-224`) although the source rule defines frequency across unique visit days in a 14-day cycle (`docs/features/game-rules/SPEC.md:79-94`). Failure trace: home→park→home becomes the “track,” self-satisfies distance membership, and displays a total whose frequency looks historical but was never fetched. **Fix:** require runner-confirmed segmentation or independent track geometry; render frequency/total unavailable until the complete window is fetched, or label a separate non-comparable single-activity projection.

7. **MAJOR — Real-provider receipt can structurally pass without proving the claim.** `EXECUTION-DISPATCH.json:327-342` requires only generic status/artifacts/validation/audit fields, while the work pack requires exact identity, consent, state/count delta, and forbidden-value evidence (`WORK-PACK.md:230-238`). Failure trace: a generic `status: pass` receipt omits provider mode, artifact digest, track/activity/consent hashes, pre/post counts, refresh result, and sink-scan result yet satisfies dispatch shape. **Fix:** bind a claim-specific schema and validator containing every admission and witness selector/result.

8. **MINOR — Responsive consent validation is width-only.** `UX-PLAN.md:78-89,104-113` tests 320/390 widths but not viewport height, text zoom, long names/copy, orientation, or software keyboard. Failure trace: wrapped retention text pushes consent/action behind the keyboard while a desktop-width assertion passes. **Fix:** add viewport-height, 200% text, long-content, orientation, and keyboard witnesses with zero-POST-until-visible-affirmation assertions.

Defended zero-finding attempts: no selector drift (15/15 current hashes match); no implicit `source_backed`/controller transition found (`ARCHITECTURE.md:279-287`, `EXECUTION-DISPATCH.json:360-365`); fake/real separation is stated consistently in prose; current OAuth state and CSRF paths are preserved. Those defenses do not cure the machine-evidence and receipt defects above.

## Abramsky, Samson — Robot-Talk Final Position

Final position — **REVISE**, no CRITICAL finding.

Agreements with Ashby:

- **MAJOR:** ownership must be revalidated before `evidence_submitted`. The workflow persists confirmation/evidence before the ownership-checking detail/stream fetch (`ARCHITECTURE.md:237-252` versus `SPEC.md:161-168`). Retaining a pending intent is valid; retaining candidate evidence is not.
- **MAJOR:** raw-stream protection lacks a closed sink denominator. The manifest enumerates persistence only (`DESIGN-SCOPE-MANIFEST.json:300-313`) while architecture promises protection across logs, errors, snapshots, and receipts (`ARCHITECTURE.md:88-91,154-169`).
- **MAJOR:** Ashby #5 correctly strengthens my orchestration/recomposition findings. The single key mixes confirmation and policy identity while omitting consent, derivation, policy, and evidence digests (`ARCHITECTURE.md:117-142`), and the API exposes three mutation routes despite requiring one orchestration boundary (`SPEC.md:229-244`).
- **MAJOR:** the real-provider receipt is structurally too generic (`EXECUTION-DISPATCH.json:327-342`) for the exact witness obligations in `WORK-PACK.md:230-238`.
- **MAJOR:** scoring is circular and semantically underdetermined. The selected activity creates the geometry and scores against it; approach/exit segments remain (`SPEC.md:170-190`; `ARCHITECTURE.md:171-173,426`). A `1/14` frequency contribution is not comparable with a complete 14-day history.
- **MINOR:** responsive evidence lacks long-copy, zoom, height, and orientation stressors. I would not require a software-keyboard witness unless the tested path includes text entry.

Challenges:

1. **Ashby #1 is not CRITICAL.** `authored-complete` is dangerously named, but literal execution gates prevent the proposed automatic admission: `selected_swu: none` (`EXECUTION-PACK.md:7`), execution is blocked (`:14-19`), no step is authorized (`EXECUTION-DISPATCH.json:13`), and dispatch authorization is `blocked` (`:24-29`). Keep this **MINOR**, or **MAJOR** only if an actual consumer is shown to treat the field as executed evidence. Fix remains `contract_authored` plus `execution_state: not_run`.

2. **Ashby #2’s “old refresh token becomes invalid immediately” is not established by the cited artifact evidence.** The missing accepted-scope check and absent CAS/singleflight design are real; retain **MAJOR** as a lost-update/concurrent-refresh risk, but remove the unsupported invalidation timing claim. Fix: required-scope validation, row-versioned CAS, reread, and bounded retry.

Merged formulation/fix:

- Split durable identities into confirmation `(principal, track, activity, consent digest)`, geometry `(confirmation, derivation digest)`, and score `(geometry digest, policy digest, canonical ScoreInputSnapshot digest)`.
- Persist a versioned `ScoreInputSnapshot` containing eligibility, window anchor/timezone, per-activity derived metrics, evidence provenance, and aggregation rules.
- Make one command endpoint the resumable orchestrator.
- Split HOST admission and WITNESS execution into separate steps, claim-specific schemas, receipts, and an explicit parent admit/reject gate.
- Treat incomplete history as a separately named, non-comparable single-activity projection unless the owner explicitly ratifies suppressing total/frequency output.

Disposition of my findings:

- **Defend MAJOR:** HOST/WITNESS collapse and unstable L2/L3 vocabulary; SWU-JSP-005 being task-shaped and silently absorbing RF-01; score non-recomposability; contradictory orchestration mapping.
- **Revise MAJOR → MINOR:** BWOI. The run does not directly reuse BWOI authority: `DEFINE-TRANSPORT.md:19` keeps it immutable, and the old proof is explicitly CT-2-only. The remaining defect is traceability: O6 marks it covered while the Design denominator omits its selector. Fix the selector/ceiling; do not demand Craft recomposition merely to use historical boundary evidence.
- **Defend MINOR:** false reversibility tags and `authored-complete` terminology.
- **Drop:** none, but the BWOI claim is narrowed as above.

## Ashby, W. Ross — Robot-Talk Final Position

## FINAL POSITION — Ashby, W. Ross

**Verdict: REVISE. No CRITICAL finding.** I revise my earlier severity because `${JSP}/EXECUTION-PACK.md:14-30` and `PLAN-TRANSPORT.md:19-20` explicitly block execution and leave every SWU unselected.

### Agreements and merged findings

- **MAJOR — HOST admission and live execution collapse.** I accept Abramsky #2 and merge it with my weak-receipt finding. `WORK-PACK.md:222-238` defines separate HOST and WITNESS units, but `EXECUTION-DISPATCH.json:169-203` combines them, while its generic real-provider receipt fields at `:327-342` cannot prove provider mode, immutable artifact, identities, consent digest, state/count delta, or leak scan.  
  **Merged fix:** distinct HOST admission receipt → explicit parent admit/reject event → separately authorized WITNESS receipt with claim-specific schema.

- **MAJOR — Score inputs are non-recomposable and semantically circular.** Abramsky #4 strengthens my sparse-history finding. `SPEC.md:114-131` lacks a canonical input snapshot, `:180-189` requires plural qualifying evidence, and `:218-224` nevertheless permits one-activity frequency. The selected activity also derives the geometry against which it is scored; approach/exit segments remain (`ARCHITECTURE.md:171-173`).  
  **Merged fix:** persist a versioned `ScoreInputSnapshot` containing window anchor/timezone, eligibility, evidence-set digest, per-activity derived metrics, geometry/policy digests, aggregation rules, and provenance; suppress a comparable total when history is incomplete.

- **MAJOR — The API does not realize its orchestration contract.** Abramsky #5 and my idempotency finding are the same load-bearing defect. Three POST mutations appear at `SPEC.md:231-240`, followed by a one-boundary requirement at `:242-244`; the key at `ARCHITECTURE.md:119-142` omits consent, derivation, policy-byte, and evidence-set digests.  
  **Merged fix:** one durable command/read selector, with separate confirmation, geometry, and score stage keys based on canonical digests.

- **MINOR — Reversibility is overstated.** Agree with Abramsky #6: `DESIGN-SCOPE-MANIFEST.json:282-298` cannot make an external read “reversible,” and geometry deletion remains unratified.

### Challenges

- **Abramsky #1 is MINOR, not MAJOR.** The BWOI selector omission is real traceability debt, but `CONTEXT-PACK.md:32,51` uses it for ontology/DomainSpec separation, not journey acceptance. The prior artifact itself excludes complete lifecycle and geometry claims (`...20260727.../SPEC.md:122-129`). No execution gate depends on BWOI.  
  **Fix retained:** bind it explicitly as historical CT-2-only context or mark O6 “informed,” not “covered.”

- **Abramsky #3 overstates “silently absorbs RF-01.”** Idempotency is explicit in `WORK-PACK.md:119-134` and L0 at `IMPLEMENTATION-LAYERING.md:29-30`; a newer plan may intentionally harden before the older one-shot frontier. The unit may be broad, but this is selection/atomicity debt, not a MAJOR correctness defect. The actual MAJOR issue is the incorrect stage/key model above.

- **Authored-complete is MINOR, not my earlier CRITICAL.** `DESIGN-SCOPE-MANIFEST.json:358-393` misleadingly labels planned claims `authored-complete`, but `ARCHITECTURE.md:394-402` calls the witnesses planned and execution remains blocked. Rename it `contract_authored` with `execution_state: not_run`.

### Disposition of my findings

- **Defend as MAJOR:** OAuth accepted-scope/refresh race; ownership revalidation after evidence persistence; incomplete raw-stream sink inventory; orchestration/idempotency; score snapshot/sparse-history semantics; hosted receipt weakness.
- **Revise:** evidence-lane finding from CRITICAL to MINOR.
- **Defend as MINOR:** responsive-consent matrix lacks height, zoom, long-content, orientation, and software-keyboard witnesses.
- **Drop as standalone:** geometry circularity and API split; both are subsumed by the merged score and orchestration findings.

All selector digests remain current; no files were changed.

## Moss, Lawrence S. — Synthesis

Synthesis verdict: **REVISE; no CRITICAL finding.** All 15 Design inclusions still match current bytes. Inventory summaries were not used as authority.

### Working local-fixture prototype blockers

- **SYN-JSP-001 — MAJOR — ACCEPT/MERGE: score input is non-recomposable and semantically circular.**  
  Evidence: `SPEC.md:114-131,180-189,214-227`; `ARCHITECTURE.md:146-173`. The activity defines the geometry and then scores against it; plural evidence lacks a canonical input snapshot, while sparse history can still produce comparable-looking totals.  
  Fix: persist a versioned `ScoreInputSnapshot` with window/timezone, eligibility, evidence-set and geometry/policy digests, per-activity metrics, aggregation, and provenance. Require confirmed segmentation/geometry or label the result a non-comparable single-activity projection; suppress total/frequency until its evidence contract is met.

- **SYN-JSP-002 — MAJOR — ACCEPT/MERGE: API and idempotency do not realize the orchestration contract.**  
  Evidence: `SPEC.md:229-244`; `ARCHITECTURE.md:117-152`. Three POST stages coexist with a promised single durable boundary, while one key conflates confirmation, derivation, policy, and evidence identity.  
  Fix: designate one resumable command plus read selector; use separate canonical keys for confirmation `(principal, track, activity, consentDigest)`, geometry `(confirmation, derivationDigest)`, and score `(geometryDigest, policyDigest, ScoreInputSnapshotDigest)`.

- **SYN-JSP-003 — MAJOR — ACCEPT: ownership validation occurs after durable evidence mutation.**  
  Evidence: `ARCHITECTURE.md:237-252`; `SPEC.md:149-168`. Confirmation/evidence is stored before the ownership-checking provider detail call, then retained on failure.  
  Fix: validate account/activity ownership before evidence attachment, or persist only a non-evidence pending intent until validation passes.

- **SYN-JSP-004 — MAJOR — ACCEPT: raw-stream protection lacks a closed sink denominator.**  
  Evidence: `DESIGN-SCOPE-MANIFEST.json:264-313`; `ARCHITECTURE.md:88-91,154-169,333-340`. Only journey persistence is enumerated despite rules covering logs, errors, snapshots, and receipts.  
  Fix: enumerate application/error/access/trace/test/snapshot/receipt sinks and require sentinel leak tests for each.

### Later real-provider/hosted residue

- **SYN-JSP-005 — MAJOR — DEFER TO REAL-PROVIDER LANE: OAuth scope and refresh concurrency.**  
  Evidence: `app/src/auth/strava-oauth.ts:125-157` stores returned scope without rejecting required-scope loss; `ARCHITECTURE.md:79-91,344-351` promises atomic replacement without CAS/singleflight. Current Strava documentation explicitly says a newly returned refresh token invalidates the prior token immediately. [Strava authentication contract](https://developers.strava.com/docs/authentication/)  
  Fix: callback required-scope validation plus account-row version/CAS or singleflight refresh, reread, bounded retry, and most-recent-token persistence.

- **SYN-JSP-006 — MAJOR — ACCEPT/MERGE: HOST admission, witness execution, receipt proof, and lane vocabulary drift.**  
  Evidence: `WORK-PACK.md:189-238` separates provider code, HOST, and WITNESS; `EXECUTION-DISPATCH.json:169-205,327-342` combines admission/execution and accepts generic receipt fields; `IMPLEMENTATION-LAYERING.md:63-84` assigns hosted execution to L2 while the work pack calls it L3.  
  Fix: separate HOST receipt → explicit parent admit/reject gate → separately authorized WITNESS receipt; bind a claim-specific schema containing provider mode, immutable artifact identity, consent/identity digests, pre/post counts, refresh result, and sink scan; standardize L2/L3 names.

### Non-blocking change requests

- **SYN-JSP-007 — MINOR — NARROW: misleading `authored-complete`.**  
  Evidence: manifest `:358-393` and denominator `:38-82`; counter-evidence: `EXECUTION-PACK.md:14-30`, `PLAN-TRANSPORT.md:19-20`, `ARCHITECTURE.md:394-402`. Execution is unmistakably blocked, so this is not CRITICAL.  
  Fix: `contract_authored`, `execution_state: not_run`, and nullable receipt selectors until validated.

- **SYN-JSP-008 — MINOR — NARROW: BWOI traceability only.**  
  Evidence: `CONTEXT-PACK.md:32,51` marks O6 covered, but the manifest inclusion/source denominator omits the prior proof selector while `ONTOLOGY-MAP.md:78` promises exact traceability.  
  Fix: bind it explicitly as immutable historical CT-2-only context, or mark O6 “informed,” not “covered.” No Craft recomposition is required.

- **SYN-JSP-009 — MINOR — ACCEPT IN PART: responsive stressors.**  
  Evidence: `UX-PLAN.md:78-89,104-113`. Add viewport-height, 200% text scaling, long content, and orientation witnesses. **Do not require a software-keyboard witness:** the specified critical flow contains selection controls, checkbox, and submit, but no text-entry interaction.

- **SYN-JSP-010 — MINOR — ACCEPT: reversibility taxonomy.**  
  Evidence: `DESIGN-SCOPE-MANIFEST.json:282-298`. External reads are not reversible, and geometry deletion remains unratified.  
  Fix: distinguish irreversible reads, compensability, and deletion capability.

Dropped/refuted: **SWU-JSP-005 need not split.** `IMPLEMENTATION-LAYERING.md:22-44` explicitly adopts idempotency for L0, and `WORK-PACK.md:119-134,258-267` gives it one orchestration/API owner and independently reviewable result. The older RF-01 boundary only says retry safety was unnecessary for the contained hosted witness; it does not prohibit this newer plan from hardening L0. Correct SYN-JSP-002 within the unit; split only if implementation sizing later proves it non-atomic. “Silently absorbs RF-01” is therefore dropped.

## Rittel, Horst — Frozen Verification

Frozen verification report — Rittel, Horst. Read-only; no files changed.

Checks: 15/15 manifest inclusion digests match current bytes; Design extraction/selection reran twice deterministically and exactly matched both stored receipts; root-installed Dispatch Spec validator passes; scoped JSON parses pass. The four npm commands are future SWU-JSP-007 execution gates, so were not run during this unselected, read-only Plan review.

- **SYN-JSP-001 — SURVIVES, MAJOR, local-fixture blocker.** `SPEC.md:114-131,180-189,214-227` lacks canonical score inputs while allowing one-day frequency; `ARCHITECTURE.md:146-173` persists only derived outputs and retains approach/exit segments. Fix stands: canonical versioned `ScoreInputSnapshot`, explicit geometry/segmentation and sparse-history labeling/suppression.

- **SYN-JSP-002 — SURVIVES, MAJOR, local-fixture blocker.** `SPEC.md:231-244` exposes three POST mutations but requires one orchestration boundary; `ARCHITECTURE.md:119-152` uses one key lacking consent, derivation, policy-byte, and evidence-set digests. Proposed staged keys and one resumable command/read selector are required.

- **SYN-JSP-003 — SURVIVES, MAJOR, shared L0 contract with real-provider proof later.** `ARCHITECTURE.md:237-252` durably writes confirmation/evidence before detail/stream validation and retains it on failure; `SPEC.md:149-168` requires ownership and fail-closed behavior. L0 must validate fake ownership before evidence attachment; live account/activity revalidation remains real-provider work.

- **SYN-JSP-004 — SURVIVES, MAJOR, local no-leak blocker for active sinks.** Manifest `:264-313` defines the rule but enumerates only journey persistence; `ARCHITECTURE.md:88-91,154-169,333-340,385-390` covers errors, logs, snapshots, and receipts. Close and sentinel-test every sink active in L0; extend the denominator for hosted access/trace sinks later.

- **SYN-JSP-005 — SURVIVES, MAJOR, real-provider only.** `strava-oauth.ts:125-157` stores accepted scope without required-scope rejection; `ARCHITECTURE.md:79-91,344-351` has no token-row CAS/singleflight. Strava currently says apps must inspect accepted scopes and that a newly returned refresh token immediately invalidates the prior token. [Official authentication contract](https://developers.strava.com/docs/authentication/) Fix stands.

- **SYN-JSP-006 — SURVIVES, MAJOR, hosted admission/witness only.** `WORK-PACK.md:189-238` separates L2 provider work, HOST, and WITNESS; `EXECUTION-DISPATCH.json:169-205,327-342` collapses admission/execution and permits a generic receipt; `IMPLEMENTATION-LAYERING.md:63-84` places hosted execution in L2 while Work Pack uses L3. Proposed split, claim schema, parent gate, and vocabulary repair stand.

- **SYN-JSP-007 — SURVIVES, MINOR, Plan evidence-lane repair; not a prototype blocker.** Manifest `:358-393` and denominator `:38-84` say `authored-complete`; `ARCHITECTURE.md:394-402`, `EXECUTION-PACK.md:14-30`, and `PLAN-TRANSPORT.md:19-20` prove witnesses are planned and execution unselected. Rename exactly as proposed.

- **SYN-JSP-008 — SURVIVES, MINOR, traceability only.** `CONTEXT-PACK.md:32,51` marks O6 covered; manifest inclusions `:12-87` omit the prior proof; `ONTOLOGY-MAP.md:78` promises exact selector/digest traceability. Prior proof `SPEC.md:18-29,118-129` is CT-2-only. Bind as historical context or mark “informed”; no recomposition.

- **SYN-JSP-009 — SURVIVES, MINOR, moderated-local UX hardening; not L0 functionality.** `UX-PLAN.md:78-89,104-113` specifies widths but no explicit height, 200% text, long-content, or orientation witnesses. No text-entry control exists, so software-keyboard evidence remains correctly excluded.

- **SYN-JSP-010 — SURVIVES, MINOR, taxonomy repair; not a prototype blocker.** Manifest `:282-298` marks external reads and geometry persistence reversible; deletion remains policy-bound (`ARCHITECTURE.md:355-364,423-424`). Separate irreversibility, compensability, and deletion capability.

**Dropped SWU split — REFUTED, confirmed.** Research `findings.md:232-251` says RF-01 is mandatory only for hosted repeat/retry, not the one-attempt witness. Current `IMPLEMENTATION-LAYERING.md:22-44` intentionally requires L0 idempotency, while `WORK-PACK.md:119-134,258-267` gives SWU-JSP-005 one orchestration/API owner, acceptance set, and atomicity verdict. Correct SYN-JSP-002 inside the unit; split only on later sizing evidence.

**NO_OBJECTION.**
