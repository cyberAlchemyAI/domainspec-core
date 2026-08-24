# CyberAlchemy Naturalized Interface Design Research Strategy

Status: `confirmation-ready`
Dispatch type: `research`
Evidence contract: `exact-binding`
Authority effect: `none`

## P1 Trigger Decision

Dispatch is required. The work must reconcile three genuinely different
judgment surfaces: human-participant visual/environmental evidence, a
schema-based categorical architecture crosswalk, and the implemented White
Tower's task and browser behavior. The source packages are large enough to
threaten parent context, the three explorer lanes can run independently, and
the final design recommendations need adversarial cognitive and definitional
checks before a writer turns them into a prototype route.

## Source-Version Finding

The user's version suspicion is correct, but the two sources live on different
repository surfaces:

- `schema-based-learning-crosswalk.md` is not in the current working tree. The
  remote `domainspec-core` `master` head was verified read-only as
  `41deffcd2bcf1adfbaedb894dc5b6e92c36be51b`; that exact commit contains
  `projects/framework-unification/discovery/schema-based-learning-crosswalk.md`.
- `domainspec-lean-formalization` local `main` is 113 commits behind its remote
  `main`. The existing `origin/main` object and a read-only remote check both
  resolve to `a4655d938c92e25be8ffd31b6f92b7e544f86e66`, which contains
  `research-psychology/naturalized-digital-environments/`.

No fetch, pull, checkout, merge, tracking-ref update, or source copy is needed
for the research dispatch: agents can read the immutable objects with `git
show`. Exact file hashes and status ceilings are in
`strategy-inventory-packet.json`.

## Intended Result

The final `findings.md` must answer four things:

1. Which ideas already justify preserving or changing the White Tower's
   information structure?
2. Which ideas are only architectural analogy or an interface hypothesis?
3. What is the smallest prototype experiment that discriminates between them?
4. What must remain unclaimed until a human study or stronger source exists?

The main artifact is an exact crosswalk:

```text
source selector
  -> evidence class and claim ceiling
  -> current White Tower task/selector
  -> candidate intervention
  -> automated witness
  -> required human witness or explicit residue
```

## Groups And Subagents

| Group | Execution | Anti-bias purpose | Agents and outputs |
| --- | --- | --- | --- |
| `explorers` | three lanes in parallel | Human empirical evidence vs categorical schema boundaries vs implemented interface behavior | **Tversky, Amos** — C1/C2/C3/C4 visual-intervention and transfer audit. **Spivak, David** — schema/implementation/semantics and collapse-test audit. **Alexander, Christopher** — current White Tower task/selector map and measurable prototype experiments. |
| `synthesizer` | after all explorers | Reconcile without converting evidence, analogy, or hypothesis into each other | **Simon, Herbert** — exact design crosswalk, KEEP/CHANGE/EXPERIMENT/REJECT matrix, smallest slice, and counterexamples. |
| `reviewers` | two lanes in parallel after synthesis, with one bounded zig-zag | Cognitive-effect vacuity vs definitional architecture collapse | **Kahneman, Daniel** — scope, transfer, measurement, and unsupported-benefit gate. **Capucci, Matteo** — schema/view/learning/execution non-collapse gate. |
| `writer` | after exact-binding evidence closure | Produce a direct interface decision artifact without inflating proof | **Schön, Donald** — `findings.md` author with ranked experiments and next decision. |
| `auditor` | after writer | Independent source, claim-ceiling, interface, accessibility, and non-authority audit | **Brandenburg, Martin** — ACCEPT or one bounded writer revision. |

## Dependency Flow

```text
explorers (parallel)
  -> synthesizer
  <-> reviewers (parallel; zig-zag cap 1)
  -> exact-binding evidence closure
  -> writer
  -> auditor
  -> parent final approval
```

One conditional synthesizer-to-explorers feedback edge may repair a missing
source binding. One auditor-to-writer feedback edge may repair supported
wording or structure. Missing evidence cannot be repaired by the writer.

## Inventory Preflight

- Machine index: `.arcanum/inventory/index.json`.
- Validation: `lookup_readiness=ready`; 305 entries; zero failures; 150 tag
  warnings; partial source coverage; Inventory read-model boundary only.
- Selected context: Interactive Ontology Learning Map; Learning Graph and
  Next-Route Guide; UI Prototyping Studio interface continuity review; and the
  CyberAlchemy Lab foundation recovery result.
- Direct-source gaps: neither named source nor the just-completed White Tower
  result is currently inventoried. Exact Git objects and current product hashes
  therefore override nearby Inventory summaries for this dispatch.
- Excluded as scope expansion: categorical DNG/semantic hierarchy research,
  categorical deep-learning tower research, and the broader Studio architecture
  review.
- Design consequence: task-relevant structure and task-irrelevant ambient
  character are separate experimental variables. Decorative naturalness cannot
  carry a cognitive-benefit claim.

The complete non-authority lookup and exact-source packet is in
`strategy-inventory-packet.json`.

## Gates And Ledger State

- Live research sheet schema: `0.8.0`.
- Candidate sheet: `dispatch-sheet.json`; it intentionally omits
  `evidence_binding` before confirmation.
- Confirmation-readiness validator: `pass`; schema `0.8.0`; ledger mutation
  `none`; frozen sheet SHA-256
  `756ca46f43273149a1f45684f48ecbe4d59ac2bc14ad1beee99834fd209bba3b`.
- Check-tension: `PASS/PASS`; both independent agents recomputed the frozen
  digest and passed tests 1-5 with no apontamentos.
- Human confirmation: required for this exact material strategy and sheet
  digest.
- Registration: not started; the append-only ledger remains untouched.
- If confirmed and run: exactly one dispatch append and one close append, with
  every research agent joined and closed and result Inventory/observability
  updated afterward.

## Boundaries

- Research reads immutable Git objects and current product evidence; it does not
  update either repository checkout.
- After confirmation, only strategist-owned `research.md`, writer-owned
  `findings.md`, and bounded receipts may be created in this working folder.
- No edits to the White Tower HTML, loader, tests, server, source research,
  Inventory owners, Arcanum, ontology, definitions, Git, publication,
  promotion, release, deployment, or production state.
- Browser structure can be validated without implying human comprehension.
- The naturalized-environments finding remains a rejected-after-loop-2 working
  synthesis. The schema crosswalk remains a candidate architecture discovery.

## Next Human Action

Reply exactly `confirmed` to authorize registration and execution of the frozen
sheet digest shown above. Any other reply is discussion, revision, or decline;
it is not confirmation.
