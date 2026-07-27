# Verified Design Distill Change Requests

Dispatch:
`2026-07-27-ui-prototyping-studio-design-distill-review`

Verifier verdict: `PASS / no objection after the five stated revisions`.

This review found no CRITICAL defect. Three MAJOR and two MINOR Design defects
survived literal verification. FIX is the review deliverable; it is not evidence
that any fix has been authored, implemented, or executed.

## ARCHITECTURE.md

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| DDR-01 | `ARCHITECTURE.md`; `governed-state-projection.ts`; `studio.ts` | Architecture promises “fresh current application/store state” and “fresh current store reads,” while the current builder performs separate reads and `/state` rereads staged state independently. A concurrent CLI write can therefore produce a torn projection and incompatible legacy fields. See `attacks.md`, Hewitt initial MAJOR-1, Alexander final agreement, and Schön DDR-01. | MAJOR | Require a coherent read epoch/lock or bounded read-version/assemble/recheck/retry protocol; derive legacy `state`, `head`, and `stagedHash` from that accepted projection. |
| DDR-02 | `ARCHITECTURE.md` | The refresh sequence patches changed regions before marking the whole version, while failure handling only says to retain the prior region “where possible.” A later renderer failure can leave mixed governed DOM under the old whole-version identity. See `attacks.md`, both attacker returns and Schön DDR-02. | MAJOR | Require detached prepare/validate plus commit, or exact rollback/per-region recovery bookkeeping; add failure-at-region-N evidence without prescribing a framework. |
| DDR-03 | `ARCHITECTURE.md`; `WITNESS-CONTRACTS.md` | Polling and action completion reuse one in-flight request, but UPW-FIX-005 only covers duplicate observations of the same new version. A completed action can join an older poll and lose immediate transition observation. See `attacks.md`, both attacker returns and Schön DDR-03. | MAJOR | Preserve single-flight while queuing one mandatory trailing refresh when action completion or a newer epoch arrives during an older flight; add the ordered race witness. |
| DDR-04 | `ARCHITECTURE.md`; `WITNESS-CONTRACTS.md` | “Canonical JSON” lacks exact recomputation rules, and UPW-VAL-VERSION does not prove that every region digest binds its exact object and the whole digest binds the full projection. See `attacks.md`, Hewitt digest/canonicalization findings, Alexander’s owner correction, and Schön DDR-04. | MINOR | Define canonicalization rules and golden vectors; validate digest coherence in server construction and contract tests. Keep browser versions opaque and limit the client to schema compatibility. |

Verdict: **FIX** for DDR-01 through DDR-04. **KEEP** the stable no-build shell,
six-region target, authority/store boundaries, safe sinks, frame boundary,
state vocabulary, current/staged separation, append-only Revert, terminal-only
Export, and rejected framework/push/durable-draft expansion.

The verifier refuted the proposal to remove the six-region contract from
Design. Plan may slice coherent transport/refresh/recovery before visual and
hierarchy work, but Design retains all six region identities.

## UX-PLAN.md

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| DDR-05 | `UX-PLAN.md`; `SPEC.md`; `WITNESS-CONTRACTS.md` | FR-14 copy and the UX keyboard, focus, no-color-only, and separately tested assertive-error obligations do not all have exact planned witness bindings. See `attacks.md`, Alexander initial MINOR-1/MINOR-2 and Schön DDR-05. | MINOR | Add the smallest exact copy/focus/keyboard/color/assertive-error witnesses, or narrow nonessential statements explicitly to review-only residue without claiming accessibility completeness. |

Verdict: **FIX** the witness binding under DDR-05. **KEEP** the information
architecture, mobile semantic order, current/staged/history semantics, and
human-evidence ceiling.

## WITNESS-CONTRACTS.md

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| DDR-01 | `WITNESS-CONTRACTS.md` | No planned witness interleaves an external durable write across projection assembly to prove coherent snapshot and same-projection compatibility fields. | MAJOR | Add a torn-read negative fixture and same-snapshot assertion. |
| DDR-02 | `WITNESS-CONTRACTS.md` | UPW-FIX-015 covers network, invalid schema, and rejected action, not a renderer failure after an earlier region prepares or commits. | MAJOR | Add renderer-failure-at-region-N evidence proving no mixed governed surface and deterministic recovery. |
| DDR-03 | `WITNESS-CONTRACTS.md` | UPW-FIX-005 covers duplicate new-version observations, not an old deferred poll response crossing a completed action. | MAJOR | Add ordered request/action/response evidence proving one trailing refresh and one eventual application. |
| DDR-04 | `WITNESS-CONTRACTS.md` | UPW-VAL-VERSION lacks exact canonicalization vectors and whole/region hash-mismatch mutants. | MINOR | Add canonical JSON golden vectors and region/whole mismatch mutants owned by server/contract validation. |
| DDR-05 | `WITNESS-CONTRACTS.md` | Current fixtures and accounting do not cover every normative copy, interaction, sandbox, allowlist, or causal-order promise. | MINOR | Add compact copy, keyboard/focus/color/error, sandbox-removal, disallowed-route, and causal accounting witnesses. |

Verdict: **FIX**. Extend accounting with request/response order, caller reason,
accepted snapshot epoch, trailing-refresh state, render attempt/commit/failure,
per-region version, and context invalidation identity/reason.

## VALIDATION-STRATEGY.md

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| DDR-01–03 | `VALIDATION-STRATEGY.md` | The current layers do not name the torn-read, partial-render, or old-poll/action interleavings required to prove the three MAJOR mechanics repairs. | MAJOR | Register the three exact deterministic positive/negative fixtures and their counters. |
| DDR-04–05 | `VALIDATION-STRATEGY.md` | The current validator scope does not bind precise server digest coherence, copy, interaction, sandbox-removal, or disallowed-route mutants. | MINOR | Register these bounded checks while preserving the Chromium-only initial ceiling and human/cross-browser/release residue. |

Verdict: **FIX** the planned validators. **KEEP** the evidence ceilings.

## DESIGN-TRANSPORT.md

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| DDR-01–05 | `DESIGN-TRANSPORT.md` | The current transport freezes unqualified single-flight refresh and does not pass coherent snapshot, recoverable commit, canonical digest validation, or expanded witness obligations to Plan. | MAJOR | Pass all five revisions forward and clarify that the six-region target is stable while Plan owns L0–L3 SWU slicing. |

Verdict: **FIX**. **KEEP** `authority_effect: none`, blocked Plan admission until
the Design revisions are authored, and every claim ceiling.

## SPEC.md

No surviving finding requires a SPEC change. If the repaired mechanics are
placed there as normative acceptance clauses, that is an authorship choice,
not a separate defect.

Verdict: **KEEP**.

## GLOSSARY-CONSISTENCY.md

No semantic collapse or ownership contradiction survived verification. Rerun
the consistency check after wording changes.

Verdict: **KEEP**.

## Architecture View 1–6 Coverage

| View | Literal Design surface | Review disposition |
| --- | --- | --- |
| View 1: Context | Browser operator, loopback Studio server, application/store services, and terminal operator boundaries | **KEEP.** DDR-01 strengthens coherence inside the existing server/store boundary; it does not move authority or add an actor. |
| View 2: High-Level Structure | Lifecycle/action spine, current canvas, contextual inspector, staged review, historical lineage, and state actions | **KEEP target; FIX transport obligations.** The six regions remain the Design target. Plan owns when hierarchy changes enter L0–L3 SWUs. |
| View 3: Low-Level Components | Projection builder/versioner, stable shell, refresh coordinator, region renderers, context reconciler | **FIX DDR-01–04.** Same-snapshot construction, recoverable commit, trailing refresh, and canonical digest ownership are component contracts. |
| View 4: Workflow Process | Poll, action completion, version comparison, reconciliation, region update, and acknowledgment/action flows | **FIX DDR-02–03.** Add recoverable partial-render behavior and the ordered action-versus-poll trailing refresh. |
| View 5: State And Event | Existing lifecycle vocabulary, current/staged identity, action gates, Revert, Export, and refresh events | **KEEP semantics; FIX DDR-03 event ordering.** No new lifecycle state or authority is introduced. |
| View 6: Deployment And Runtime | Loopback, no-build embedded shell, optional later extraction, and existing browser/server boundary | **KEEP.** DDR-04 remains server/contract-owned; no browser crypto requirement, framework migration, push transport, or deployment expansion is admitted. |

All six architecture views were attacked and dispositioned. The seven selected
architecture extensions are covered by the surviving findings matrix:
authority/trust is KEEP; security/abuse is DDR-05; state/event is DDR-03;
persistence/concurrency is DDR-01 and DDR-03; failure/compensation is DDR-02;
integration/versioning is DDR-01 and DDR-04; quality is DDR-02 through DDR-05.

## UPW-FIX-001–015 Coverage

Every existing witness remains exactly once in `PLANNED-WITNESSES.json` with
evidence state `planned-design-contract`. The review changes the planned
contract only; none of these rows has executed.

| Witness | Existing obligation | Review disposition |
| --- | --- | --- |
| UPW-FIX-001 | Canonical absent-staged representation | **KEEP; refine under DDR-04** with canonicalization golden vectors. |
| UPW-FIX-002 | Unchanged desktop polling is inert | **KEEP.** This remains the primary unchanged-version continuity proof. |
| UPW-FIX-003 | Unchanged mobile polling preserves local work | **KEEP; refine under DDR-05** with explicit invalidation identity and causal accounting while preserving focus/drafts/scroll. |
| UPW-FIX-004 | One Accept causes one intended update | **KEEP; refine under DDR-03** so action completion joining an older poll queues one trailing refresh. |
| UPW-FIX-005 | Duplicate transition observations are idempotent | **FIX/extend under DDR-03.** Retain duplicate-new-version proof and add the distinct old-poll/action/new-state ordering fixture. |
| UPW-FIX-006 | Stale local context is explicitly invalidated | **KEEP; refine under DDR-05** with bound identity and invalidation-reason accounting. |
| UPW-FIX-007 | Comparison frames are distinguishable | **KEEP.** Accessible frame names remain required. |
| UPW-FIX-008 | Annotation feedback uses only `cf-msg` | **KEEP.** Exact live-scope contract remains unchanged. |
| UPW-FIX-009 | State actions use only `act-msg` or `act-msg2` | **KEEP; refine under DDR-05** with the separately tested assertive blocking-error path. |
| UPW-FIX-010 | Unrelated content is not live | **KEEP.** No extra announcements are introduced by refresh changes. |
| UPW-FIX-011 | Light-surface normal text meets contrast floor | **KEEP; complement under DDR-05** with a no-color-only communication check. |
| UPW-FIX-012 | Outer workbench actions meet target-size floor | **KEEP.** The target-size proxy and exception discipline remain bounded. |
| UPW-FIX-013 | Mobile task hierarchy remains operable | **KEEP.** It binds responsive order while Plan still owns SWU slicing. |
| UPW-FIX-014 | Governance behavior does not regress | **KEEP.** Current/staged separation, acknowledgment, append-only Revert, and terminal-only Export remain mandatory. |
| UPW-FIX-015 | Failed or malformed refresh preserves work | **FIX/extend under DDR-02 and DDR-04.** Add renderer-failure-at-region-N, digest-mismatch mutants, and deterministic recovery without false transition. |

Additional bounded planned witnesses are required for DDR-01 coherent-snapshot
interleaving and DDR-05 copy, keyboard/focus/color/error, sandbox-removal, and
disallowed-route coverage. Their addition must not be misreported as execution
of UPW-FIX-001–015.

## Fixed-Point And Receipt Artifacts

The denominator, scope manifest, two-pass selection result, glossary, and
planned-witness receipt remain valid Design inputs. The change requests add or
refine Design obligations; they do not claim any witness executed.

Verdict: **KEEP**.

## Refuted Finding

Drop Hewitt MAJOR-5, “six regions improperly forced into L0.” The six regions
are selected surface and local-context obligations and guard against the
rejected coarse rerender. Retain the target contract; state only that Plan may
place transport/refresh/recovery and hierarchy changes in different SWUs.

## Closing Change-Request List

1. **DDR-01 MAJOR:** define a coherent projection snapshot and derive
   compatibility fields from it.
2. **DDR-02 MAJOR:** define recoverable region rendering that cannot silently
   leave mixed governed DOM.
3. **DDR-03 MAJOR:** add action-aware trailing refresh semantics across an
   older in-flight poll.
4. **DDR-04 MINOR:** define canonical JSON and server/contract-owned digest
   coherence proofs.
5. **DDR-05 MINOR:** bind the remaining copy, interaction, security, and causal
   mechanics promises to exact witnesses or narrow nonessential language.

## Evidence And Authority Boundary

The verified outcome is **FIX, then candidate PASS**. Planned witnesses remain
unexecuted. Human outcomes, cross-browser generalization, broad accessibility
conformance, lifecycle acceptance, Plan admission, SWU selection,
implementation, release, deployment, and production readiness remain unproven
and separately owned. The completed governed-state-projection chain remains
terminal and is not reopened by this review.
