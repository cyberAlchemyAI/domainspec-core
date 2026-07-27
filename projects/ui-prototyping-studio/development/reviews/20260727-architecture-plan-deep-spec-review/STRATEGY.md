# UI Prototyping Studio Architecture, Plan, And Deep-Spec Review Strategy

Status: form-valid and double-PASS; unconfirmed, unregistered, not run

## P1 Trigger

This is a governed `review` dispatch because the architecture, plans, Craft
state, deep-spec package, and live implementation already exist, while the
requested deliverable is a verified set of change requests rather than new
architecture or implementation.

Synthesis, isolation, context protection, and parallelism all apply. No single
reader should be allowed to collapse current runtime behavior, historical
design intent, plan executability, and authority status into one verdict.

## Lanes, Subagents, And Outputs

1. `attackers` runs three explorers in parallel with robot talks on the
   canonical `methodology` axis.
   - `Alexander, Christopher` uses formal contract and governance analysis.
   - `Turing, Alan` uses computational and empirical falsification.
   - `Beer, Stafford` uses historical lineage and supersession tracing.
2. `synthesizer` runs `Noether, Emmy` as the single writer after all attacker
   returns. It deduplicates and severity-ranks cited candidate change requests.
3. `verifiers` runs two skeptics in parallel on the canonical `attack-vector`
   axis.
   - `Russell, Bertrand` performs definitional and scope falsification.
   - `Schön, Donald` performs reproducible counter-example and fresh-operator
     falsification.
4. `coverage-auditor` runs `Brandenburg, Martin` after verification and
   recommends accept or reject without creating findings.
5. The parent remains the independent final approver.

The intended outputs are `attacks.md` and `findings.md`. Review agents are
read-only over Studio target artifacts. Surviving findings must include file,
quoted evidence, severity, and a one-line proposed fix. The final findings must
also include per-artifact KEEP/FIX verdicts, an authority and supersession
recommendation, and a dependency-safe next-plan recommendation.

## Dependency Flow

`attackers -> synthesizer <-> verifiers -> coverage-auditor -> parent`

- Attackers to synthesizer is sequential.
- Synthesizer to verifiers is zig-zag with cap 1.
- Synthesizer to attackers is conditional feedback with cap 1 if material
  coverage is missing.
- Verifiers to coverage auditor is sequential.
- Whole-sequence `max_loops` is 1.

## Review Corpus And Questions

All attackers review the complete declared corpus:

- current state and root contracts: `.craft/ledger.yml`, `CRAFT.md`,
  `ARCHITECTURE.md`, `SPEC.md`, root `WORK-PACK.md`, and `PLAN-NEXT.md`;
- deep spec: the result, synthesized design, proposal, one-shot plan,
  residuality stressors, UX evidence report, Playwright plan, and cold-start
  findings;
- current proposal: the complete July 10 governed-state projection
  architecture, layering, work-pack, execution pack, transport, tasks, and
  waves;
- live selectors: preview and annotation projection, current-head resolution,
  diff admission, and the e2e helper.

The review must decide through evidence:

- which artifact owns current state, architecture contract, proposal history,
  executable plan, and validation receipts;
- what deep-spec intent remains live, what is implemented under newer seams,
  what is stale, and what should remain explicitly historical;
- whether current root documents and Craft projections match the live
  standalone Studio;
- whether the July plan can produce its own acceptance evidence in dependency
  order;
- whether current-head, visible-style-diff, e2e, and handoff claims stay within
  reproducible proof.

Body War/TROQAR evidence is selector and copy precedent only. Open Design is a
subordinate comparison surface only. Neither becomes target architecture
authority.

## Preflight State Snapshot

These are routing observations, not accepted review findings:

- the deep-spec package exists and is valuable, but its own result is
  conditional and its proposal did not mutate the canonical spec;
- the July governed-state projection package is the newest coherent
  architecture direction, but remains `flag` and proposed;
- current source still exposes the exact current-head, style-diff, and e2e
  selectors identified by the prior research;
- the first July SWU requires Playwright evidence while the independently
  declared e2e-helper repair is assigned to a later-numbered SWU, creating a
  sequencing question that the review must verify;
- Craft is the scoped state authority, but its indexes and next-move text do
  not visibly reconcile the July plan.

Passing typecheck and unit tests is implementation evidence only. The observed
e2e harness failure blocks fresh browser proof but does not prove product
behavior failed.

## Inventory Preflight

The machine index selected one high-confidence, closed strategy-result entry:
`ui-prototyping-studio-ux-ui-upgrade-research-strategy-result-synthesis`.
It contributes the current-head, visible-style-diff, preview-coherence,
durable-action, deterministic-e2e, handoff, mobile/annotation, and documentation
selectors.

Body War/TROQAR and the Open Design reference were explicitly excluded as
target authority. No Evidence Card or EvidenceSet was selected. Current runtime
state, Craft-to-plan linkage, fresh browser evidence, and a single
authority/supersession map remain gaps.

The concrete design consequence is a three-method whole-corpus attack plus two
independent verifier attack vectors. Inventory is discovery context only; every
surviving finding must be established against the current target.

See `strategy-inventory-packet.json` for source references, selectors,
exclusions, gaps, residue, and the non-authority notice.

## Gate And Ledger State

- Form owner: schema `0.7.0`.
- Form validation: `PASS`.
- Frozen sheet SHA-256:
  `13b3ef9f9c7aa62300406b9c7bcc7bf8ab17e12e3fc3e8383995538447338140`.
- Tension checker:
  `ups-architecture-review-tension-checker-13b3ef9f = PASS`.
- Tension reviewer:
  `ups-architecture-review-tension-reviewer-13b3ef9f = PASS`.
- Ledger mutation: `none`.
- Human confirmation: pending.
- Registration: not registered.
- Review: not run.
- Studio targets: unchanged.

If confirmed, the exact frozen sheet will be registered before any working
agent runs. At termination, one append-only close row will record the actual
agent counts, loops, feedback prompts, outcome, and exit reason.

## Next Human Action

Reply `confirmed` to freeze and authorize registration and execution of this
exact sheet, request a revision, or decline.
