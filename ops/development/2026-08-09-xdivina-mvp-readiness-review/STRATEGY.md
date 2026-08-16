# xDivina MVP Readiness Review Strategy

## Preliminary answer

The repository does not support the simple claim that xDivina is “not yet an
MVP.” It directly records a passed bounded human browser/GIMP workflow, and the
current commit adds many editor-core operations after that trial. It also
directly records that the broader Phase 0 production gate is not passed.

The review therefore uses three evidence tiers:

1. **Bounded local browser MVP** — the disposable same-machine workflow and its
   current semantic editor operations.
2. **Distributable desktop MVP** — a non-developer can install and run a chosen
   shell on the selected platform, complete the narrow workflow offline, and
   recover work without manual GIMP/ComfyUI setup.
3. **Production/commercial readiness** — cross-platform packaging, broader
   compatibility, model/licensing policy, hardening, updates, support, and beta
   evidence.

The first tier appears implemented by project claims but has not yet been
independently reviewed against the current post-trial commit. The second and
third tiers remain unproven. That is a preflight observation, not the review
verdict.

## P1 trigger decision

Dispatch is required by synthesis, context protection, isolation, and
parallelism. The target spans product contracts, current UI and adapter code,
live and fixture tests, security and licensing boundaries, shell performance,
format compatibility, and a human-trial record. One reviewer would be likely
to let either “it runs,” “the plan says no,” or “it is not distributable” own
the whole definition of MVP.

## Lanes, groups, and subagents

| Group | Subagent | Role | Lens / anti-bias angle | Expected output | Scheduling |
| --- | --- | --- | --- | --- | --- |
| `mvp-attackers` | Fong, Brendan | explorer / attacker | product-contract fidelity and three-tier MVP minimality | cited scope/status attack receipt | parallel, then robot talks |
| `mvp-attackers` | Turing, Alan | explorer / attacker | executable code, test, browser, GIMP, and fixture/live separation | cited reproducibility attack receipt | parallel, then robot talks |
| `mvp-attackers` | Ahrens, Sönke | explorer / attacker | fresh-user operability, security, license, compatibility, and distribution | cited boundary attack receipt | parallel, then robot talks |
| `change-request-synthesizer` | Shannon, Claude | writer / synthesizer | reconcile without inflating claims | three-tier matrix and candidate `findings.md` | after all attacker initial and final positions |
| `finding-verifiers` | Gödel, Kurt | skeptic / verifier | scope attack | KEEP/DROP receipt against literal contracts | parallel after draft |
| `finding-verifiers` | Popper, Karl | skeptic / verifier | executable counter-example attack | KEEP/DROP receipt with actual checks | parallel after draft |
| `coverage-auditor` | Brandenburg, Martin | dedicated auditor and final approver | coverage, citation, severity, tier, and zero-finding enforcement | ACCEPT/REJECT receipt | after both verifiers |

The attacker anti-bias axis is `methodology`. The verifier axis is
`attack-vector`. Pairwise predicted disagreements are stored in the exact
schema sheet, not only in this prose.

## Dependency flow

```text
3 attackers in parallel
  -> robot-talk final positions
  -> 1 synthesizer
  <-> 2 verifiers in one bounded zig-zag
  -> 1 dedicated coverage auditor
  -> parent closeout

verifiers --feedback, at most once--> attackers when current evidence is missing
```

All sequential and zig-zag handoffs are owner-gated. A missing or blocked
agent stops downstream execution. Feedback is eligible only on the declared
edge and within its one-loop cap.

## Inventory preflight

- Owner index: parseable machine index, 306 entries, partial source coverage.
- Exact xDivina matches: none.
- Target machine index: unavailable.
- Selected: one high-confidence exact-corpus review-strategy precedent for
  route mechanics and claim ceilings.
- Excluded: ontology research, Body War planning review, and a duplicate
  Arcanum revalidation projection because their domain evidence does not apply.
- Gap: the current xDivina commit post-dates its Phase 0 and bounded human-trial
  records with many editor-core commits.
- Design consequence: bind every lane to one current commit and corpus, require
  a three-tier MVP matrix, and verify every finding from current target bytes or
  actual non-network checks.
- Authority ceiling: Inventory is discovery only.

Packet: `strategy-inventory-packet.json`.

The strategy-result Inventory update is deferred because the shared root
`index.json`, `index.md`, and `log.md` already contain unrelated uncommitted
changes. This residue does not grant or remove dispatch authority.

## Bound corpus and outputs

- Target: `projects/xdivina`
- Commit: `755b09aa6681e0a6ef2d7fed3707dcfe877efc39`
- Required state: clean `main` matching `origin/main`
- Corpus manifest: `review-corpus.txt`
- Required review outputs after confirmation: `attacks.md` and `findings.md`

`findings.md` must contain the three-tier status matrix, current evidence,
per-artifact KEEP/FIX decisions, verified surviving findings, and the smallest
severity-ordered change requests with falsifiable acceptance checks.

## Dispatch Spec and execution boundary

`DISPATCH-ROUTE.json` binds the four waves to `distill`,
`ux-evidence-validator`, `domainspec-subagents-strategy`, and `orchestrate`
ownership. Review agents are read-only over xDivina. Only the synthesizer may
write `findings.md`; the parent preserves verbatim returns and lifecycle
receipts in this working folder.

No dependency installation, external network access, xDivina edit, Git action,
publication, deployment, release, or implementation is in scope.

## Gate and ledger state

- Dispatch type: live `review`.
- Form: schema `0.8.0`.
- Confirmation-readiness: `PASS` at sheet SHA-256
  `45e8a24dfd22ba12bed09b66c0de8495fd51823bf7dea2a2a8f2298b647eecb2`;
  schema `0.8.0`; ledger mutation `none`.
- Material projection: preserved in `material-strategy-projection.json` at
  material SHA-256
  `5bf9fbac5764cc22ebd597db5d255e18b12fac000643be1765fb4066daf662d6`.
- Dispatch Spec: `FLAG` with no block. Receipt wiring and all 55 corpus paths
  validate; remaining notices are that the validator counts role IDs rather
  than the sheet's 3/2 agent instances and does not list the installed
  `ux-evidence-validator` capability in its canonical subset.
- Check-tension: independent `PASS/PASS` at the exact sheet digest; handles
  `/root/xdivina_tension_checker` and `/root/xdivina_tension_reviewer`.
- Human confirmation: required after all machine gates pass.
- Registration: not performed.
- Review execution: not started.
- Ledger: unchanged; if confirmed, exactly one dispatch row and one close row.
- Closeout: `resolved` when the dedicated auditor accepts the verified
  change-request list, even if artifact verdicts are FIX.

## Claim ceiling

This proposal is not the MVP review result. A later accepted review can say
which tier the current evidence supports and what change requests remain. It
cannot itself implement those requests or prove distribution, deployment,
release, production readiness, commercial readiness, or market success.

## Next human action

Reply `confirmed` to register and run this exact material strategy. Discussion,
questions, or permission to revise the draft are not confirmation.
