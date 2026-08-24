# review-authority-non-collapse.md — one gate: authority never granted

Agent: Heisenberg, Werner · role skeptic (authority non-collapse) · dispatch
`2026-08-20-ontology-stable-version-and-runtime-research`

**Claim ceiling.** Cited synthesis only. Grants no ontology authority, authorizes no runtime
implementation, promotes nothing, lifts no gate. `ontology-authority-not-granted` and
`runtime-implementation-not-authorized` stand. I attack only whether the proposal claims authority
it was never granted. Precision, testability, and falsifiability are another reviewer's gate and I
do not touch them. Selectors verified by me today; `executed` = command run, `observed` = file read.

## Gate verdict: **needs-revision**

Not `fail`: nothing in the synthesis mutates an authority surface, records a verdict, or lifts a
gate. Two objections are blocking and both are repairable by wording that returns what the proposal
never held.

---

## Surviving objections

**O1 — BLOCKING. §2 is titled a kind the ontology route may not define.**
Rule: `cyberAlchemy-v2/ontology/PACKAGE-MODEL.md:50` lists "runtime contract definition" under
"Out of scope"; the owner is named at `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md:32` —
`kind.runtime_contract`, owner route "task-session after owner gates", forbidden collapse "Not
generated mirror output" (observed). §2 is headed "Candidate runtime contract" and its clauses are
imperative — "**Must do.** (a)…(g)". The synthesis names this prohibition itself in §1's
"Explicitly out" ("runtime-contract definition (`PACKAGE-MODEL.md:46-54`)") and in C3 ("Precedent
without owners licenses a test, not a build"), then writes the contract anyway. This is a lapse
against its own finding, not a disagreement with it. Repair: retitle to *requirements a runtime
contract would have to satisfy, to be authored by task-session after owner gates*, and convert
"Must do" to "would have to".

**O2 — BLOCKING. The version declares no authority kind, so its state is blocked, not candidate.**
Rule: `CAV2-D49` (`cyberAlchemy-v2/authority/definitions/DEFINITIONS.md`, §CAV2-D49 Normative
Definition, observed): an artifact whose kind is not in the closed enumeration "may not acquire or
exercise authority — it defaults to **blocked** pending an owner decision… Adding a kind is itself
owner-gated." "Edge-law version" is not among the nine kinds (`AUTHORITY-KINDS.md:25-35`). C2 goes
further and calls the version "eligible to be routed to decision-gate" — eligibility is an admission
judgment owned by decision-gate (`AUTHORITY-KINDS.md:28`, `kind.decision`). Repair: name the kind it
claims (`kind.spec` or `kind.evidence`), or state default-deny blocked and let the owner say
eligible.

**O3 — MAJOR. The identifier grammar is an owner act on one axis.** Choosing a version *name* is
not itself minting here: the stem is precedented at
`…/ontology-candidate-graph-prototype/src/evaluator/policy-disposition.mjs:8`,
`owner: "ontology-edge-law-owner"` (observed). The **slash** is the problem. Every identifier in the
artifact being versioned uses dash grammar — `candidate-v1` (`src/contracts/candidate-v1.mjs:299`),
`candidate-policy-v1` (`policy-disposition.mjs:5`), `candidate-result-v1` /
`candidate-run-receipt-v1` (`src/evidence/run-writer.mjs:42,78`) — and grammar normalization is an
explicitly owner-routed deferred decision:
`arcanum/…/schema-validation-plan/decision-gates/OVS-GATE-004-default-output-declaration.md:138-141`
— "Whether the emitted record's dot-grammar identity is normalized to the package's slash grammar…
Recorded in `<emission-contract>` as owner-routed; renaming would orphan records already held by a
consuming repository." Second point: `ontology-edge-law-owner` has **zero** occurrences under
`cyberAlchemy-v2/authority/` or `cyberAlchemy-v2/ontology/` (grep, executed) — it is an unbound
literal in implementation code. Naming a version after an unregistered owner reads as ownership that
does not exist. Repair: use `ontology-edge-law-v1`, or defer the grammar to OVS-GATE-004.

**O4 — MAJOR. "Emits diagnostics, never dispositions" is the wrong invariant, and A3 crosses it.**
`policy-disposition.mjs:31-38` returns a field literally named `disposition`, valued `policy-pass` /
`policy-fail` / `policy-indeterminate`; A3 requires reproducing all three. Testing the boundary as
asked: a typed diagnostic with a declared code is **not** a verdict merely by being typed. It
becomes one at three points, and the corpus names all three — (i) `authority_effect != "none"`
(`policy-disposition.mjs:36`; ingest rule `cyberAlchemy-v2/SOURCE-MAP.md:32-33`); (ii) deciding a
case whose owner is unbound, which is why `specializes` must return indeterminate with
`POLICY_OWNER_UNBOUND` (`:58`); (iii) a consumer treating the output as admission —
`cyberAlchemy-v2/ontology/projections/README.md:47-49`: "A projection may emit owner-approved state
only when the owner decision permits the use scope. Blocked, deferred, or unknown candidates may
appear only as such." The synthesis binds (i) and (ii) and binds no consumer at all. §2(a)
"refuse to run on mismatch" is a *self*-refusal and claims nothing. Repair: replace the slogan with
the two-part invariant plus an explicit "no consumer may treat this output as admission".

**O5 — MINOR. Unowned imperatives in §3 and X1/X4.** Declaring what would demonstrate a version does
**not** authorize its construction — that inference does not go through. But §1 says A2 "exists to
fix" the defect, §3 says "Only A1–A2 are additions", and X1's settling evidence is bare "A2
executed" while X4 says "Execute the Node suite" — X2/X3/X5 name owners and these do not. Against
standing residue `runtime-implementation-not-authorized` and `PACKAGE-MODEL.md:50`, add an owner
column to §3 as §4 already has.

---

## Cleanly within authority — and why

1. **The WOR import grants nothing.** C3's split ("the method transfers, the authorization does
   not") is correct. `live_state_sha256 == replay_state_sha256` is a self-checking property of a
   fixture, and the source dispatch's own ceiling (`WOR/RESULT.md`, quoted in
   `CONTEXT-CORRECTION.md`) disclaims "authority" explicitly — nothing was granted there, so nothing
   was over-granted here. What A6 *needs* (a reducer) is caught by O1, not by the import.
2. **`Status: candidate` is not a promotion.** It is the corpus's own minimum-authority header
   convention — `AUTHORITY-KINDS.md:3` and `promotion-requests/README.md:2` both carry it. Refusing
   to write `stable`, citing `AUTHORITY-MODEL.md:155-159` (OQ-1, "Status: OPEN", verified), claims
   less than the corpus permits. That is the right direction of error.
3. **§2's "Must never decide" list is well-formed.** I re-verified each: `LIFECYCLE-MODEL.md:48-49`
   ("It must not fill the verdict hole"), `AUTHORITY-KINDS.md:32`, `PACKAGE-MODEL.md:46-54`,
   `NODE-MODEL.md:18`. Every prohibition names a real owner at an accurate selector.
4. **The rename does not settle label governance.** That deferred gate is scoped to `meaning` as the
   long-term global branch label (`GOVERNED-CANDIDATE-BUNDLE.md:156`; import ban at
   `OVS-GATE-004:129-135`). `ontology-edge-law/v1` is not a branch label and does not touch it. The
   question I was sent to test clears — on grammar only, see O3.
5. **§5 routing and the `attacks.md` exclusion** are correct authority hygiene: unresolved rows go to
   named owners, and CR-9 material is refused as confirmation.
