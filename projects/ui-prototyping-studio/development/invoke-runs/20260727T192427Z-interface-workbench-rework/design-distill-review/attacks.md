# Design Distill Review Returns

Dispatch:
`2026-07-27-ui-prototyping-studio-design-distill-review`

The returns below are preserved verbatim. Inventory references in the agent
prompts were discovery-only; every candidate finding still requires literal
artifact verification.

## Hewitt, Carl — Initial Position

```text
Hewitt INITIAL POSITION — mechanics/correctness/narrow-first (read-only)

CRITICAL: none.

MAJOR-1 FIX — “fresh reads” do not guarantee one coherent projection under external writes. Architecture says “Projection versions derive from fresh current store reads” (ARCHITECTURE.md §Persistence/Concurrency, lines 241-249), while current builder separately calls listRevisions, listVariants, resolveCurrentHtml, getStagedCandidate, listComments, and getHandoffBundle (governed-state-projection.ts lines 80-106, 151-157); /state separately reads session, builds projection, then reads staged again (studio.ts 440-453). Counterexample: CLI Accept/Revert between these reads yields a torn body whose top-level head/staged fields disagree with projection and whose hash could canonize a state that never existed. One-line fix: require projection construction from one coherent store snapshot/lock epoch (or bounded read-verify-retry) and require top-level compatibility fields be derived from that same projection.

MAJOR-2 FIX — region-render failure semantics permit a mixed DOM with no exact recovery model. Refresh patches changed regions sequentially then marks version (ARCHITECTURE.md lines 138-147); failure says “stop before marking version applied; retain prior region where possible” (lines 251-261). If regions 1–2 commit and region 3 throws, applied whole-version remains old while DOM is half-new; retry can duplicate effects or reconcile context against already-mutated DOM. One-line fix: specify render-to-detached-fragment then atomic per-region commit plus per-region applied-version bookkeeping/rollback, and a witness that injects failure after an earlier region commit.

MAJOR-3 FIX — single-flight “reuse” loses an action-triggered trailing refresh in the poll/action race. Contract says reuse existing flight (ARCHITECTURE.md 136-150). Counterexample: poll starts on V0, external/action write commits V1, action completion calls refresh but reuses the V0 flight; no immediate V1 fetch occurs, so action completion is stale until next timer. UPW-FIX-005 only duplicates observations of the same new version (WITNESS-CONTRACTS.md 17), not an old in-flight observation crossing a write. One-line fix: coalesce concurrent callers but set a dirty/trailing-refresh flag for any request arriving during flight (mandatory for action completion), and add ordered deferred-response race fixtures.

MAJOR-4 FIX — schema validation is structural but version/region semantic coherence is unspecified. The client validates schema, compares region versions, then marks the new whole version (ARCHITECTURE.md 138-147, 266-274). Counterexample: valid-shape response advertises V2 while all region versions equal V1, or a region object changes under an unchanged region hash; client can mark V2 without rendering its content. UPW-FIX-015 says “invalid schema” only (WITNESS 27). One-line fix: define and validate digest coherence (each region hash over its exact object; whole hash over schema+regions) before reconciliation/patch, with hash-mismatch mutants.

MAJOR-5 FIX — stated L0 separation is contradicted by the frozen architecture. “Continuity is L0. Information architecture and visual hierarchy are later” (ARCHITECTURE.md 17-19), but L0’s projection is already keyed as spine/canvas/inspector/review/history/actions (85-117), and DESIGN-TRANSPORT freezes keyed rendering and context reconciliation while passing Plan an L0–L3 map (DESIGN-TRANSPORT.md 37-55). That forces hierarchy-region redesign into the first defect repair. One-line fix: define L0 as a minimal existing-DOM stable-shell transport (canonical snapshot/version, inert unchanged poll, action/poll coordinator, current context preservation), leaving semantic six-region decomposition/order to later SWUs.

MINOR-1 FIX — “canonical JSON” is not named precisely enough for independent recomputation in a no-build runtime (ARCHITECTURE.md 110-113; WITNESS 60). One-line fix: name an exact canonicalization algorithm/rules (key ordering, arrays, null, Unicode, number/undefined rejection) and golden vectors.

MINOR-2 FIX — witness accounting omits request ordering, refresh callers, render attempts/commits/failures, and invalidation reason identity; current counters (WITNESS.md 29-39) cannot prove the race/failure semantics above. One-line fix: extend accounting with request/response sequence IDs, caller reason, queued trailing refresh, per-region attempted/committed version, render error, and context invalidation tuple.

KEEP candidates: server-owned opaque full+region versions; stable document; safe DOM sinks/route allowlist; stale server-side action checks; unchanged null representation; explicit context binding; no-build/loopback constraint; planned-vs-executed evidence ceiling.

Survived attacks: duplicated same-version response is idempotent if single-flight and applied-version checks are implemented; stale Accept/Revert identity remains server-rejected (studio.ts 361-407); iframe-local navigation/scroll can survive unrelated region updates when canvas/frame source identity is unchanged; invalid schema/network failure is correctly required to preserve last known work; null-staged unchanged states are directly covered; external CLI freshness remains an intended source, but atomic snapshot coherence does not survive.
```

## Alexander, Christopher — Initial Position

```text
INITIAL POSITION — Alexander/Christopher (read-only Distill attacker)

Verdict candidate: FIX (no CRITICAL found; two MAJOR mechanics/contracts gaps and two MINOR coverage gaps). All 10 selected outputs are materially authored: six base views plus authority/trust, security/abuse, state/event, persistence/concurrency, failure/compensation, integration/versioning, quality, UX Plan, and validation contracts (ARCHITECTURE.md:48-50,52-295; DESIGN-SELECTION-RESULT.json selected_outputs). The package is appropriately bounded, but the planned witness denominator does not yet prove every promise it makes.

MAJOR-1 — partial keyed-render failure can leave a mixed projection with the old whole-projection version. The coordinator patches changed regions sequentially, marking the version only afterward (ARCHITECTURE.md:138-147), while failure policy merely says retain the prior region “where possible” (253-261). If region N fails after N-1 patched, DOM and applied-version identity diverge; retry/reconciliation/idempotence are underspecified. UPW-FIX-015 covers network, invalid schema, and rejected action, not a mid-commit renderer failure (WITNESS-CONTRACTS.md: fixture 015; validator table). Fix: require off-DOM construction/validation of every changed fragment followed by an atomic commit, or specify per-region commit/version/rollback semantics; add a renderer-failure-at-region-N negative witness asserting no mixed governed surface and deterministic retry.

MAJOR-2 — single-flight reuse has an action-vs-poll stale-response race. `refresh(reason)` reuses any in-flight request (ARCHITECTURE.md:138-150). If Accept completes while a pre-action poll is in flight, action refresh can reuse the pre-transition response and fail to observe the accepted transition until a later poll. Existing duplicate-observation witness tests the converse (same new version twice), not this stale in-flight ordering (WITNESS-CONTRACTS.md UPW-FIX-005). Fix: give action completion a mandatory trailing refresh/epoch rule when it joined a request started before the action receipt; add the exact deferred-response interleaving witness and require one eventual application without double patch.

MINOR-1 — FR-14 copy has no hard planned witness. Copy is normative (SPEC.md:103-105; UX-PLAN.md:131-139), but UPW-FIX-001–015 contains no browser-copy/secondary-CLI-disclosure assertion; L5 only says contract review (VALIDATION-STRATEGY.md Evidence Layers). Fix: add a state/copy matrix witness (or explicitly classify copy as review-only), checking browser action wording and CLI detail demotion.

MINOR-2 — selected accessibility/security surface exceeds named negative fixtures. UX promises visible focus, keyboard parity, no color-only information, and a separately tested assertive blocking-error path (UX-PLAN.md:141-155), while fixture rows directly cover frames/live scopes/contrast/targets but not those four claims. Security says iframe sandbox and route-family allowlisting persist (ARCHITECTURE.md:229-239), but the named security negative is only raw outer-shell injection; the validator pass condition mentions frames without explicit sandbox-removal/route-injection mutants (WITNESS-CONTRACTS.md validator table). Fix: either add focused positive/negative witnesses for these claims or narrow them to Plan-owned review residue; explicitly add sandbox-removal and disallowed-route mutants.

Per-artifact candidates:
- ARCHITECTURE.md — FIX: atomic keyed commit + action/poll epoch/trailing-refresh semantics; KEEP all six views, state/action spine, authority/store boundaries, safe sinks, sandbox, compatibility, quality ceilings.
- SPEC.md — KEEP, with FIX only if new failure/race acceptance clauses are housed here; requirements are otherwise coherent and scoped.
- UX-PLAN.md — KEEP information architecture, mobile order, current/staged/history semantics, focus/status rules and claim ceiling; FIX witness binding for copy and the currently unwitnessed a11y promises.
- WITNESS-CONTRACTS.md — FIX: add renderer mid-commit, stale in-flight action race, copy, keyboard/focus/color/error-status, sandbox and route-allowlist witnesses.
- VALIDATION-STRATEGY.md — FIX only to register those exact negatives; KEEP Chromium-only initial ceiling and explicit cross-browser/human/release residue.
- DESIGN-TRANSPORT.md / DECISIONS-AND-GAPS.md / GLOSSARY* / selection receipts — KEEP; gates and semantic prohibitions are clean.

Minimal coherent Design recommendation: retain the stable no-build shell, six keyed regions, server-owned opaque versions, application/store authority, contextual inspector, staged review, collapsed history, and mobile semantic order. Add only (1) transactional region-commit semantics, (2) an action-after-poll freshness rule, and (3) the smallest witness rows needed for promises already normative. Do not add a framework, push transport, durable draft store, or broader release/accessibility program.

Survived attacks: lifecycle vocabulary and application authority remain unchanged (ARCHITECTURE.md:189-205,218-227); staged is never silently current and Export stays terminal-only (SPEC.md:124-134; UX-PLAN.md:94-105); outer DOM uses safe sinks and prototype HTML stays iframe-contained (ARCHITECTURE.md:115-117,132-134); history is secondary but retained (UX-PLAN.md:109-115); mobile task order is explicit (49-56,159-170); human, cross-browser, broad accessibility, Plan, execution, release and production claims remain outside Design (SPEC.md:61-72,156-167; VALIDATION-STRATEGY.md residue); planned witnesses stay unexecuted; prior completed GSP is not reopened—new cycle is explicitly distinct and no selected SWU exists (DECISIONS-AND-GAPS.md D-01/D-09, G-10). The proposal is not over-designed relative to the verified continuity defect: rejected framework/push/durable-store expansions are disciplined (ARCHITECTURE.md:297-306).
```

## Hewitt, Carl — Final Robot-Talk Position

```text
FINAL POSITION — Hewitt after confrontation with Alexander

Agreements

- No CRITICAL findings.
- Retain MAJOR: sequential region rendering can leave a mixed-version DOM. Alexander independently confirms the exact failure: “sequential region patch plus mark-whole-version-afterward permits mixed DOM.” The load-bearing contract is `ARCHITECTURE.md` lines 138–147, while failure handling only says “stop before marking version applied; retain prior region where possible” at lines 251–261. This is insufficient without detached preparation plus commit, rollback, or explicit per-region recovery state.
- Retain MAJOR: action completion may reuse a pre-action poll flight and temporarily miss the committed transition. `ARCHITECTURE.md` lines 138–150 require reuse of the in-flight request but do not require a trailing fetch. Alexander’s “trailing refresh/epoch semantics” is the right repair.
- Agree that witness coverage must be expanded or claims narrowed. Alexander’s missing focus/keyboard/no-color/assertive-error and route/sandbox witnesses complement my missing race, partial-render, and digest-coherence witnesses. `WITNESS-CONTRACTS.md` lines 29–39 currently account for outcomes but not enough causal ordering or render-commit evidence.

Disagreements / refutations

- Reject Alexander’s recommendation to retain the six keyed regions unchanged for the first repair. The corpus says “Continuity is L0. Information architecture and visual hierarchy are later” (`ARCHITECTURE.md` lines 17–19), yet the proposed initial projection hard-codes `spine`, `canvas`, `inspector`, `review`, `history`, and `actions` (`ARCHITECTURE.md` lines 85–117). That is an avoidable coupling between the verified continuity defect and later hierarchy work. Six regions may remain the L1/L2 target, but they should not be an L0 prerequisite.
- Alexander omits the coherent-snapshot defect. “Fresh current store reads” (`ARCHITECTURE.md` lines 241–249) do not make multiple reads atomic. Current construction reads revisions, variants, current HTML, staged state, comments, and handoff separately (`governed-state-projection.ts` lines 80–106 and 151–157), while `/state` separately rereads staged state (`studio.ts` lines 440–453). An external CLI write can therefore produce a torn response that never represented one governed instant. This remains MAJOR.
- Alexander omits semantic digest coherence. Structural schema validation alone cannot reject a changed whole version paired with unchanged region hashes, or changed region bytes paired with an old region hash. The client then may mark a whole version applied without applying its content under `ARCHITECTURE.md` lines 138–147. This remains MAJOR, though it can be merged with the canonicalization repair.
- Alexander’s FR-14 copy issue is valid but MINOR. It does not threaten the continuity repair; add a state/copy matrix or explicitly classify it as review-only.
- Alexander’s accessibility/security witness gap is MINOR if the affected statements remain Design obligations rather than claimed implementation results. It becomes MAJOR only if Design Distill treats those contracts as fully test-bound without adding witnesses.

Severity reconciliation

- MAJOR: coherent server snapshot and compatibility-field consistency.
- MAJOR: transactional/per-region recoverable render commit.
- MAJOR: trailing action refresh across poll/action races.
- MAJOR: semantic whole/region digest coherence.
- MAJOR: L0 must be separable from six-region hierarchy work.
- MINOR: exact canonical-JSON algorithm and golden vectors.
- MINOR: causal witness accounting additions.
- MINOR: FR-14 copy witness.
- MINOR: focus/keyboard/no-color/assertive-error and sandbox/route witnesses, or corresponding claim narrowing.

Merged minimal change set

1. Define one coherent projection snapshot/epoch; derive legacy `state`, `head`, and `stagedHash` from that same snapshot.
2. Specify exact canonicalization and require server and validator recomputation of every region digest and the whole digest.
3. Define rendering as prepare/validate first, then atomic region commit where possible; otherwise record exact per-region applied versions and deterministic recovery. Add failure-at-region-N.
4. Change single-flight semantics to coalesce requests while queuing one mandatory trailing refresh when an action or newer epoch arrives during a flight. Add a deferred old-poll/action/new-state witness.
5. Split L0 from later hierarchy: L0 repairs the existing surface’s transport, inert unchanged polling, action freshness, and context continuity; the six semantic regions and reordered hierarchy become later dependent work.
6. Extend witness accounting with request/response order, caller reason, snapshot epoch, trailing-refresh state, attempted/committed region versions, render failure, and context invalidation identity/reason.
7. Add the smallest copy, focus/keyboard/error, sandbox/route, and digest-mismatch fixtures—or narrow those statements to planned review obligations.

Own findings retained/dropped

- Retain all five initial MAJOR findings.
- Retain both initial MINOR findings.
- Drop none.
- Merge my render-failure and action-race findings with Alexander’s MAJOR-1 and MAJOR-2.
- Accept Alexander’s two MINOR findings as additions.
- KEEP: authority and lifecycle boundaries, safe-sink direction, staged/current separation, stale server-side Accept/Revert rejection, terminal-only Export, no-build loopback runtime, claim ceilings, and rejection of framework/push/durable-draft expansion.
```

## Alexander, Christopher — Final Robot-Talk Position

```text
FINAL POSITION — Alexander/Christopher

Agreements

- Agree with Hewitt MAJOR-1. “Fresh current store reads” and serialized durable writes do not establish a coherent multi-store read snapshot (ARCHITECTURE.md:80-81,241-249). An external CLI write between state/file/artifact reads could produce a projection whose fields are individually fresh but mutually inconsistent, then canonically bless that torn projection. Retain as MAJOR. Minimal fix: require a coherent read epoch/lock or read-version → assemble → read-version verification/retry, and derive legacy compatibility fields from that same accepted projection; add an interleaved external-write witness.
- Agree with Hewitt MAJOR-2; it is identical to my MAJOR-1. Sequential changed-region patching followed by late whole-version marking permits mixed DOM on renderer N failure (ARCHITECTURE.md:138-147,251-264). Retain as MAJOR with detached build/validate + atomic commit, or exact rollback/per-region bookkeeping, plus injected mid-render failure proof.
- Agree with Hewitt MAJOR-3; it is identical to my MAJOR-2. Reusing an in-flight pre-action poll can swallow the action-triggered refresh (ARCHITECTURE.md:138-150). Retain as MAJOR. Require dirty/trailing refresh or request epoch semantics and an ordered deferred-response race fixture.
- Agree with Hewitt MINOR-1. “Canonical JSON” is not reproducible enough without exact key ordering, Unicode/string/number/null rules and golden vectors (ARCHITECTURE.md:110-113). Retain as MINOR; it strengthens FR-01 without expanding product scope.
- Agree with Hewitt MINOR-2. Existing accounting separates navigation, applied versions, POSTs and heads, but not request start/finish order, caller reason, render attempt/commit/failure, or invalidated binding identity (WITNESS-CONTRACTS.md, “Navigation And Update Accounting”). Retain as MINOR and use those fields in the three new race/failure witnesses.

Disagreements / severity changes

- Downgrade Hewitt MAJOR-4 to MINOR. Digest/region semantic coherence needs a server-side validator and hash-mismatch golden/mutant tests because the architecture declares exact digest semantics (ARCHITECTURE.md:87-117), but requiring the browser to recompute cryptographic digests is not yet justified. This is a trusted loopback server, safe sinks remain mandatory, and malformed schema already blocks patching (ARCHITECTURE.md:229-239). Fix: validate whole/region digests at projection construction and in contract tests; the browser validates schema/major version and treats version values as opaque. Escalate only if compatibility fields can be independently assembled—which MAJOR-1’s same-snapshot rule should prohibit.
- Refute Hewitt MAJOR-5. The six semantic regions are not an unjustified L0 implementation freeze: they correspond directly to already-required state-specific surfaces and local-context boundaries (SPEC.md:40-59,87-105; ARCHITECTURE.md:70-130). A single coarse rerender would reintroduce unrelated context destruction, explicitly rejected at ARCHITECTURE.md:297-306. The actual layering remains open: stable shell may stay embedded for L0/L1 and renderer extraction is optional L2 (ARCHITECTURE.md:207-216). No finding. Plan should slice continuity before hierarchy/polish, but Design should retain the six-region contract.

Own initial findings retained/dropped

- Retain both initial MAJOR findings, merged into Hewitt MAJOR-2 and MAJOR-3.
- Retain MINOR copy-witness gap: FR-14 and UX copy rules are normative (SPEC.md:103-105; UX-PLAN.md:131-139), but UPW-FIX-001–015 has no explicit copy/CLI-disclosure witness. Add a compact state/copy matrix or mark it explicitly review-only.
- Retain MINOR accessibility/security witness gap. Visible focus, keyboard parity, no-color-only communication, and separately tested assertive errors are normative (UX-PLAN.md:141-155) without exact fixture rows; iframe sandbox/route allowlisting are normative (ARCHITECTURE.md:229-239) but the named negative proof is only raw outer-shell injection. Add focused witnesses/mutants or narrow the claims. Do not inflate them into certification.
- Drop none of my initial findings.

Merged minimal change set

1. Specify one coherent projection-read epoch and same-projection compatibility fields.
2. Specify detached validation/atomic region commit (or exact rollback/per-region applied bookkeeping).
3. Specify action-dirty/trailing-refresh ordering over an older in-flight poll.
4. Define canonical JSON precisely; validate whole/region digest coherence server-side with golden vectors and hash-mismatch mutants.
5. Extend witness accounting and add only the missing targeted proofs: torn read, mid-render failure, stale-poll/action race, copy matrix, keyboard/focus/color/assertive-error checks, sandbox removal, and disallowed route injection.
6. Keep the six-region stable no-build shell, lifecycle/action spine, current canvas, contextual inspector, staged review, collapsed history, mobile order, safe sinks, iframe boundary, current application/store authority, and all claim ceilings. Human, cross-browser, broad accessibility, Plan, execution, release, and production remain outside Design (SPEC.md:61-72,156-167; VALIDATION-STRATEGY.md “Residue Rules”). The completed GSP chain remains terminal and distinct; the new cycle does not select an SWU (DECISIONS-AND-GAPS.md D-01, D-09, G-10).
```

## Schön, Donald — Verifier Return

```text
Schön verification: **PASS / no objection after the five stated revisions.** No CRITICAL finding survives. The candidate does not inflate implementation, accessibility, human-outcome, Plan, release, or production claims.

### Candidate verification

- **DDR-01 — VERIFIED — MAJOR**
  - `ARCHITECTURE.md:74-81,243-249` promises projection/version derivation from fresh store state, not a coherent snapshot.
  - Current bytes independently read revisions, variants, current HTML, staged state, comments, and handoff (`governed-state-projection.ts:82-106,151-157`); `/state` then rereads staged state separately (`studio.ts:440-453`).
  - An external writer can therefore produce mutually inconsistent projection/compatibility fields. Same-snapshot compatibility derivation is required. This is a real consistency defect, not an invented blocker.

- **DDR-02 — VERIFIED — MAJOR**
  - `ARCHITECTURE.md:138-147` patches regions before marking the whole version; `:253-261` merely retains the prior region “where possible.”
  - Failure after an earlier patch leaves mixed governed DOM under the old whole-version identity.
  - Detached preparation plus commit, or exact rollback/per-region recovery bookkeeping, is required. Do not over-prescribe framework or literal cross-DOM atomicity.

- **DDR-03 — VERIFIED — MAJOR**
  - `ARCHITECTURE.md:138-150` reuses an existing flight for both polling and action completion.
  - UPW-FIX-005 covers two observations of the same new version, not an old in-flight poll crossing a completed action.
  - Require one trailing refresh when an action completion joins an older flight, with ordered race evidence. This preserves single-flight rather than rejecting it.

- **DDR-04 — VERIFIED — MINOR**
  - `ARCHITECTURE.md:110-113` does not specify canonical JSON sufficiently for independent recomputation.
  - UPW-VAL-VERSION supplies only canonical recomputation plus a nullable mutant; it does not prove exact region-object and whole-projection digest coherence.
  - Correct ownership is server construction/versioner plus contract validation and golden vectors. The browser treats digests as opaque and validates schema compatibility; browser cryptographic recomputation is neither required nor justified.

- **DDR-05 — VERIFIED — MINOR**
  - FR-14 copy lacks an exact witness.
  - UPW-FIX-003/local-context rules cover some focus preservation, but not the full keyboard-parity, no-color-only, or separately tested assertive-error obligations.
  - UPW-VAL-SECURITY names sandbox/allowlist persistence, but its only explicit negative is raw outer-shell injection; sandbox-removal and disallowed-route mutants are absent.
  - Current accounting omits ordering/reason/trailing-refresh/render-attempt-commit-failure/invalidation identity needed by DDR-01–03.
  - Add narrowly targeted witnesses or explicitly narrow nonessential language to review-only residue. This is not accessibility completeness or certification.

### Finding to drop

- **REFUTED — drop Hewitt MAJOR-5 (“six regions improperly forced into L0”).**
  - The six regions directly implement selected surface and local-context obligations (`SPEC.md:40-59,87-105`; `ARCHITECTURE.md:70-130`) and prevent the expressly rejected coarse rerender (`ARCHITECTURE.md:297-306`).
  - Retain the six-region Design target. Clarify only that Plan owns L0–L3 slicing and need not place every hierarchy/visual change into the first SWU.
  - Severity: **none / no finding**.

### Selection and witness accounting

The two-pass result is a fixed point and selects exactly ten outputs:

`architecture`, seven required architecture extensions, `ux-plan`, and `validation-contracts`.

All are accounted for:

- DDR-01: base, persistence/concurrency, integration/versioning, validation.
- DDR-02: base, failure/compensation, quality, validation.
- DDR-03: base, persistence/concurrency, state/event, quality, validation.
- DDR-04: base, integration/versioning, quality, validation.
- DDR-05: security/abuse, quality, UX Plan, validation.
- Authority/trust has no defect and is explicitly retained unchanged.

`PLANNED-WITNESSES.json` accounts for UPW-FIX-001–015 exactly once, all as `planned-design-contract`; the review correctly identifies additions/refinements rather than pretending those witnesses executed. Existing UPW-FIX-014 preserves current-head/staged separation, acknowledgment, append-only Revert, and terminal-only Export.

### Per-artifact recommendation

- `ARCHITECTURE.md` — **FIX** DDR-01–04 and L0 slicing clarification; otherwise **KEEP**.
- `UX-PLAN.md` — **FIX** witness binding or narrow exact DDR-05 promises; otherwise **KEEP**.
- `WITNESS-CONTRACTS.md` — **FIX** with the bounded new races, failure, digest, copy, accessibility, sandbox, route, and causal-accounting evidence.
- `VALIDATION-STRATEGY.md` — **FIX** to register those exact proofs and server-owned digest validation; **KEEP** evidence ceilings.
- `DESIGN-TRANSPORT.md` — **FIX** unqualified single-flight wording and pass all five revisions plus six-region/L0 adjudication forward; **KEEP** blocked Plan admission and `authority_effect: none`.
- `SPEC.md` — **KEEP**; add clauses only if chosen as the normative home for the repaired mechanics.
- `GLOSSARY-CONSISTENCY.md` — **KEEP**, then rerun after wording changes.
- Selection/denominator/scope/planned-witness receipts — **KEEP**.

Final verified set: **DDR-01 MAJOR, DDR-02 MAJOR, DDR-03 MAJOR, DDR-04 MINOR, DDR-05 MINOR.** After those bounded fixes: **PASS, no objection.**
```
