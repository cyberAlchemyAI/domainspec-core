# Candidate Synthesis

Dispatch:
`2026-07-27-ui-prototyping-studio-design-distill-review`

No CRITICAL finding survives. Five underlying defects survive after
deduplication: three MAJOR mechanics obligations and two MINOR
contract/evidence defects.

## DDR-01 — MAJOR — Coherent Projection Snapshot

- Evidence: `ARCHITECTURE.md:74-81` says the builder derives regions from
  “fresh current application/store state”; `ARCHITECTURE.md:243-249` says
  versions derive from “fresh current store reads.” Current bytes instead
  perform separate reads of revisions, variants, current HTML, staged state,
  comments, and handoff (`governed-state-projection.ts:82-106,151-157`), then
  `/state` independently rereads staged state for compatibility fields
  (`studio.ts:440-453`).
- Defect: freshness plus serialized writes does not establish one coherent read
  instant. A CLI write between reads can produce a torn projection and
  inconsistent legacy `state`, `head`, and `stagedHash`.
- Fix: require one coherent read epoch/lock or bounded
  read-version/assemble/recheck/retry protocol, and derive compatibility fields
  from the accepted projection snapshot.
- Selected outputs: `architecture`,
  `architecture:persistence-concurrency`,
  `architecture:integration-versioning`, `validation-contracts`.
- Source: Hewitt initial MAJOR-1; Alexander final agreement.

## DDR-02 — MAJOR — Transactional Or Recoverable Region Commit

- Evidence: `ARCHITECTURE.md:138-147` requires sequential
  comparison/reconciliation/update and only afterward marks the whole version;
  `ARCHITECTURE.md:253-261` says on region-render failure to stop before marking
  the version applied and retain the prior region “where possible.”
- Defect: failure after an earlier region patch can leave a mixed DOM carrying
  the old whole-version identity. “Where possible” supplies neither rollback
  nor an exact recovery state.
- Fix: require detached preparation/validation followed by atomic commit, or
  specify exact rollback/per-region applied-version recovery; add
  failure-at-region-N evidence.
- Selected outputs: `architecture`, `architecture:failure-compensation`,
  `architecture:quality`, `validation-contracts`.
- Source: Hewitt initial MAJOR-2; Alexander initial MAJOR-1; both final
  positions.

## DDR-03 — MAJOR — Trailing Refresh Across Action/Poll Race

- Evidence: `ARCHITECTURE.md:138-150` says to reuse the in-flight request and
  makes polling and action completion call the same coordinator.
  `WITNESS-CONTRACTS.md` UPW-FIX-005 covers duplicate observations of the same
  new version, not an old poll response crossing a successful action.
- Defect: action completion can join a poll started before the write and lose
  its immediate observation of the committed transition until the timer fires.
- Fix: coalesce concurrent callers but queue one mandatory trailing refresh
  when action completion or a newer epoch arrives during flight; add the
  ordered deferred-response witness.
- Selected outputs: `architecture`, `architecture:persistence-concurrency`,
  `architecture:state-event`, `architecture:quality`,
  `validation-contracts`.
- Source: Hewitt initial MAJOR-3; Alexander initial MAJOR-2; both final
  positions.

## DDR-04 — MINOR — Canonical Digest Coherence And Ownership

- Evidence: `ARCHITECTURE.md:110-113` says SHA-256 over canonical JSON for
  whole and region objects but does not define canonicalization;
  `ARCHITECTURE.md:268-274` requires browser schema-major validation;
  `WITNESS-CONTRACTS.md` UPW-VAL-VERSION only names canonical recomputation and
  a nullable-coercion mutant.
- Defect: independent server/test recomputation is underspecified, and no
  mutant proves that each region digest matches its exact object and the whole
  digest matches the complete projection.
- Adjudication: MINOR, not MAJOR. The version is server-owned and opaque to the
  browser (`SPEC.md:107-122`); browser cryptographic recomputation is an
  unjustified implementation choice. Coherence belongs to the projection
  builder/versioner and contract validator. It becomes MAJOR only if
  independently assembled compatibility data remains possible after DDR-01.
- Fix: define canonicalization rules and golden vectors; validate whole/region
  digest coherence at server construction and in contract tests, while the
  browser treats digests as opaque and validates schema compatibility.
- Selected outputs: `architecture`, `architecture:integration-versioning`,
  `architecture:quality`, `validation-contracts`.
- Source: Hewitt initial MAJOR-4/MINOR-1; Alexander final downgrade and owner
  correction.

## DDR-05 — MINOR — Selected Promises Lack Exact Witness Binding

- Evidence: FR-14 requires browser-action copy plus secondary CLI disclosure
  (`SPEC.md:103-105`); UX requires keyboard parity, focus handling, separately
  tested assertive errors, and no color-only information (`UX-PLAN.md`,
  Interaction/Accessibility Contracts); security requires sandboxed frames and
  route-family allowlisting (`ARCHITECTURE.md:229-239`). UPW-FIX-001–015 and
  validator negatives do not cover all of these obligations. Existing
  accounting records navigation, applied versions, POSTs, and heads, not
  request ordering/caller reason/render attempt-commit-failure/invalidation
  identity (`WITNESS-CONTRACTS.md`, Navigation And Update Accounting).
- Defect: the planned denominator cannot prove all selected normative promises
  or the causal mechanics introduced by DDR-01–DDR-03.
- Fix: add the smallest copy matrix; focus/keyboard/color/assertive-error
  checks; sandbox-removal and disallowed-route mutants; causal accounting for
  request epoch/order/reason, trailing refresh, render
  attempt/commit/failure, and invalidation identity; or explicitly narrow any
  nonessential statement to review-only residue.
- Selected outputs: `ux-plan`, `architecture:security-abuse`,
  `architecture:quality`, `validation-contracts`.
- Source: Hewitt initial MINOR-2; Alexander initial MINOR-1/MINOR-2; both final
  positions.

## Six-Region L0 Adjudication

Drop Hewitt’s proposed MAJOR finding. The six regions are Design obligations
traceable to selected requirements (`SPEC.md:40-59,87-105`;
`ARCHITECTURE.md:70-130`) and their identity boundaries are relevant to
preserving context. Removing them would weaken keyed continuity and risk the
rejected coarse-rerender alternative (`ARCHITECTURE.md:297-306`).

Design must not imply that all visual/hierarchy changes form one L0
implementation unit. Retain the six-region target contract while stating in
Design Transport that L0 may first establish coherent
transport/refresh/recovery over the stable shell and Plan decides when each
semantic region or hierarchy change enters a selected SWU.

## Per-Artifact Disposition

- `ARCHITECTURE.md`: FIX DDR-01 through DDR-04 and clarify six-region target
  versus Plan-owned L0 slicing. KEEP authority/store boundaries, stable
  no-build shell, safe sinks/frame boundary, state vocabulary, staged/current
  separation, append-only Revert, terminal-only Export, and rejected
  expansion.
- `UX-PLAN.md`: FIX by binding or narrowing the exact copy/accessibility
  promises under DDR-05. KEEP information architecture, mobile semantic order,
  current/staged/history semantics, and human-evidence ceiling.
- `WITNESS-CONTRACTS.md`: FIX with torn-read, mid-render failure,
  stale-poll/action race, digest mutants/golden vectors, causal accounting,
  copy, accessibility, sandbox, and route witnesses.
- `VALIDATION-STRATEGY.md`: FIX by registering the exact new positive/negative
  proofs and server-owned digest validation. KEEP Chromium-only initial ceiling
  and explicit cross-browser/human/release residue.
- `GLOSSARY-CONSISTENCY.md`: KEEP. Re-run consistency after wording changes.
- `DESIGN-TRANSPORT.md`: FIX unqualified single-flight language and pass
  coherent snapshot, recoverable commit, digest validation, and six-region/L0
  clarification forward. KEEP `authority_effect: none`, pending Design Distill,
  and blocked Plan admission.

## Candidate Verdict

FIX, then candidate PASS. With the five bounded changes, this remains the
smallest coherent architecture without a framework, push transport, durable
draft store, authority migration, or release expansion.

Planned witnesses remain unexecuted. Human outcomes, cross-browser
generalization, broad accessibility conformance, lifecycle acceptance, Plan
admission, SWU selection, implementation, release, deployment, and production
readiness remain unproven and separately owned.
