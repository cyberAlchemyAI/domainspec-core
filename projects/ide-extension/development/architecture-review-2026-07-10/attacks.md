# Architecture Review: Collected Attacks

Status: collected transcript index for registered review `2026-07-10-ide-extension-architecture-review`.

The complete attacker and verifier returns remain authoritative in `raw/`. This index faithfully preserves each attacker's initial and final position, surviving attacks, robot-talks outcome, and verifier disposition without replacing the source transcripts.

## W. Ross Ashby

- **Complete transcript:** [raw/ashby.md](raw/ashby.md)
- **Initial position:** The paper boundary is disciplined, but implemented L0 is a happy-path UI/persistence loop rather than a trustworthy authority boundary. Executable variety does not yet absorb hostile approval, concurrency, grant, evidence, or recovery conditions.
- **Original findings:** unauthenticated approval; replayable approval; singleton envelope overwrite; unenforced grant policy; approval-to-passed collapse; weak audit consistency/integrity; decorative receipt evidence; parse-only schema validation.
- **Surviving attacks:** loopback-only binding; no browser credential custody or live provider call; honest proposed/deferred layer labels; happy-path persistence and smoke behavior.
- **Final position:** L0 is a useful deterministic demonstration, but fields named approval, evidence, and receipt do not yet enforce the invariants that make them authoritative.
- **Robot-talks outcome:** held self-approval as CRITICAL; conceded secret custody as a present defect and retained it as a promotion gate; raised runtime schema enforcement to MAJOR; held approval-to-passed as MAJOR; withdrew generic hash-chain implications while retaining the reproduced cross-store race; reframed mutable provenance and unresolved ownership as promotion blockers unless used as current authority.

## Carl Hewitt

- **Complete transcript:** [raw/hewitt.md](raw/hewitt.md)
- **Initial position:** Implemented L0 is a loopback workbench with a narrow happy-path witness. L0.5, L0.6, L1, and L2 remain explicitly unimplemented.
- **Original findings:** client-supplied self-approval; replay and concurrent duplicate receipts; schemas parsed but not enforced; arbitrary grants; declared typestate skips `running`.
- **Reproduced outcome:** the same principal could propose and approve; two concurrent approvals both returned `201`, produced two receipt events and distinct receipts, while mutable workbench state retained only one.
- **Surviving attacks:** pre-approval run rejects with `409`; listener binds to loopback; proposed and deferred integrations are not presented as implemented.
- **Final position:** approval identity and one-use semantics, runtime contract enforcement, and grant authorization must be repaired before the L0 witness can support governance claims.
- **Robot-talks outcome:** held self-approval and replay as CRITICAL concerns; held runtime schema enforcement as MAJOR; rejected generic tamper demands; treated provenance as a later promotion blocker. Hewitt explicitly dissented on approval-to-`passed`: **MINOR at implemented L0**, because L0 says approval records a no-op receipt, but **MAJOR if carried into L0.5**.

## Axel van Lamsweerde

- **Complete transcript:** [raw/van-lamsweerde.md](raw/van-lamsweerde.md)
- **Initial position:** The conceptual boundary is coherent, but ownership legitimacy, reproducibility, and contract enforcement are not mechanically established.
- **Original findings:** parse-only schema validation; unresolved module ownership; passing smoke code overread as approval proof; mutable external MCP/chat provenance; untyped receipt references.
- **Surviving attacks:** honest layer separation; rejection of canvas authority; remote precedents remain deferred/specimen-only; the narrow L0 smoke scenario genuinely passes.
- **Final position:** L0 is a functioning local demonstration, not a reference-integrity-enforced governance kernel; L0.5/L0.6 are bounded proposals and L1/L2 remain deferred.
- **Robot-talks outcome:** revised self-approval/replay to CRITICAL; held schema enforcement as MAJOR; revised approval-to-`passed` to MAJOR; conceded cryptographic audit requirements while retaining the concrete race; held mutable research and unresolved source/owner references as promotion blockers rather than present authority defects.

## Donella H. Meadows

- **Complete transcript:** [raw/meadows.md](raw/meadows.md)
- **Initial position:** The corpus understands that visible context and sourced capability must not become authority, but L0 currently demonstrates cooperative operation rather than hostile containment.
- **Original findings:** self-approval; replay; capability smuggling; unbound context/evidence; non-attributable audit; absent secret custody; false schema assurance.
- **Surviving attacks:** loopback binding; no browser key storage; no implemented browser mutation path; generally honest layer labeling.
- **Final position:** L0 proves prepare/display/approve/persist/receipt on a cooperative dry run, not an adversarially governed action boundary.
- **Robot-talks outcome:** held self-approval and replay; conceded secret custody as a present defect and retained it as a provider-promotion gate; raised runtime schema enforcement to MAJOR; held approval-to-`passed` as MAJOR; replaced generic tamper evidence demands with the reproduced state/event race; reframed unresolved provenance as a promotion blocker unless it participates in authority.

## Converged Robot-Talks Outcomes

- Present defect: caller-controlled self-approval.
- Present defect: reusable approval and the reproduced concurrent state/event divergence.
- Present defect: unenforced grant vocabulary and policy.
- Present MAJOR: runtime envelopes, receipts, and manifests are not constrained by the declared schemas.
- Majority position: approval directly becoming `passed` is MAJOR receipt-semantic collapse. Hewitt retains an explicit MINOR-at-L0 dissent.
- Promotion gate, not present defect: secret custody before any live provider lane.
- Not implied by L0: generic cryptographic hash-chain or tamper-evidence requirements.
- Promotion blocker: mutable provenance and unresolved `source_refs`/owner routes, unless current authority or capability admission relies on them.
- Surviving strengths: loopback-only binding, pre-approval run blocking, honest layer labels, absence of live browser/provider authority, and a passing narrow smoke path.

## Zig-Zag Verifiers

### Horst Rittel

- **Complete verifier transcript:** [raw/rittel-verification.md](raw/rittel-verification.md)
- **Method:** Inspected every candidate and cited target, then exercised the real server in a disposable temporary state directory. Distinguished reproduced fact, literal fact, and inference.
- **Reproduced evidence:** self-approval `201`; sequential replay `201`; concurrent replay `[201, 201]`; unknown grant prepare `201`; scalar `context_refs` prepare `201`; older pending approval `404` after a second prepare; three read-model receipts versus four receipt events; default evidence path exists; synthetic after reference does not resolve as a file.
- **Disposition:** Verified AR-CAND-001, 002, 003, 005, 006, 008, 009, 010, and 011; reclassified AR-CAND-004 and 007. No item was refuted or merged.
- **Key corrections:** AR-004 is unvalidated and unbound grant declaration, not executed capability bypass. AR-007 has partial run/approval/before binding and a real default evidence file, but lacks materialized after-state and complete binding. Generic cryptographic audit requirements remain outside L0.
- **Dissent:** Rates AR-001 CRITICAL at present L0 and AR-003 MAJOR at present L0.

### Donald Schon

- **Complete verifier transcript:** [raw/schon-verification.md](raw/schon-verification.md)
- **Method:** Used the literal implemented-L0 acceptance contract as the boundary; proposed controls create promotion gates rather than present defects unless L0 behavior contradicts an L0 claim or corrupts an L0 artifact.
- **Disposition:** Reclassified AR-CAND-001, 003, 004, and 007; verified AR-CAND-002, 005, 006, 008, 009, 010, and 011.
- **Key corrections:** AR-001 is MAJOR L0 human-attribution failure and CRITICAL before effectful L0.5+. AR-003 is MINOR L0 typestate inconsistency because `SPEC.md:149-157` says approval records the no-op receipt, and MAJOR before L0.5's distinct invocation. AR-004 makes no executed-capability claim. AR-007 requires resolvable persisted L0 references while stronger identity/context/digest custody belongs to L0.5.
- **Promotion boundary:** AR-009 and 010 are promotion blockers only; AR-011 is a provider-promotion gate only. None is a present L0 defect.

## Final Verifier Synthesis

- AR-CAND-002 remains the sole CRITICAL present-L0 finding.
- AR-CAND-001, 004, 005, 006, 007, and 008 are MAJOR present-L0 findings.
- AR-CAND-003 is MINOR at present L0 and MAJOR before L0.5 promotion.
- AR-CAND-009 and 010 remain promotion blockers only; AR-CAND-011 remains a promotion gate only.
- Rittel's higher present-L0 severities for AR-CAND-001 and AR-CAND-003 remain explicit dissent for final audit.
- Raw verifier reports remain the verbatim authority; `findings.md` is now the PENDING FINAL AUDIT synthesis.
