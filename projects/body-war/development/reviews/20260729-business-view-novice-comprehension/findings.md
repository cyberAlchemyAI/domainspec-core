# Body War Business View Novice-Comprehension Findings

## Executive decision

Accept three HIGH change requests and one MEDIUM protocol-admission blocker.

The comprehension instrument belongs beside the existing views as a separately
generated learner-only `BUSINESS-COMPREHENSION-TASK.html`. It does not belong
inside `BUSINESS-JOURNEY-EXPERIMENT.html` or `BUSINESS-VIEWS.html`.

The journey remains a reference stimulus after its authority and narrative
repairs. The printable gallery stays outside the initial novice protocol.
Reviewer keys, audits, rubrics, stalls, results, and human records remain
separate and unshipped.

No Body War novice or human comprehension has been demonstrated.

| Severity | Change request | Decision | One-line repair |
| --- | --- | --- | --- |
| HIGH | CR-1 | Accept with verifier fixes | Generate an isolated learner task from a dedicated catalog and keep every adjudication and run artifact outside learner bytes. |
| HIGH | CR-2 | Keep, authority-constrained | Render distinct boundary meanings and endpoint-matched residue owner/gate data without changing ontology relations, status, or digests. |
| HIGH | CR-3 | Accept with authority fix | Remove unsupported story causality, align A/B navigation, use unordered relation groups, and make native no-JavaScript access valid. |
| MEDIUM | CR-4 | Protocol-admission blocker | Admit a generated view as a novice stimulus only with a pinned durable browser-structure receipt. |

## CR-1 — Separate Body War reading instrument

Disposition: `accept-with-verifier-fixes`  
Severity: `HIGH`

### Exact seam

Create an independently generated projection:

```text
authoring/comprehension-task-catalog.mjs
  -> scripts/generate-comprehension-task.mjs
    -> BUSINESS-COMPREHENSION-TASK.html
      -> tests/business-comprehension.test.mjs
```

Only learner task data may enter that catalog and generator. The current
business-view generator continues to own its existing two HTML projections
(`projects/body-war/ontology/business/scripts/generate-views.mjs:20-26,912-922`).

Removing the comprehension catalog, generator import, and output must leave
ontology nodes, relations, lifecycle policies, and semantic digests unchanged.

### Learner-visible surface

Preregister these candidate reading loci once:

- `locate`
- `trace`
- `retell`
- `distinguish`
- `boundary`
- `vocabulary`

Keep task, loci, prompt, and chosen stimulus bytes identical across matched
arms. These are candidate measurement categories until structurally pretested;
they are not yet validated human instruments.

Score:

- exact keyed relation or edge identity;
- correct sibling-branch identification;
- correct authority or non-promotion boundary; and
- explicit rejection of an invented sequence or branch feed.

Do not score paraphrase overlap.

### Reviewer-only surface

The following remain outside learner generation and outside shipped learner
bytes:

- allow/deny manifest;
- keyed relation, branch, boundary, and invented-sequence rules;
- answer key and coverage audit;
- correctness rubric;
- stall log and severity classification;
- agent-pretest results; and
- later human-witness records.

The historical instrument demonstrates the required separation
(`projects/domainspec-v2/development/comprehension-novice-test/novice-agent.md:12-23`;
`task-coverage-audit.md:7-18`). Its current `task.md:50-52` still exposes
reviewer leakage history and is not admissible as a new blind Body War learner
task.

### Task and stall effect

Correctness and observed friction are orthogonal.

- Correctness is scored from the reviewer key.
- Stall locus uses the six reading categories above.
- Severity remains `blocker`, `friction`, or `cosmetic`.
- Zero observed stalls is valid data.
- The historical `>=5 stalls` rule does not transfer.

### Contamination and acceptance

Any reviewer key, audit, rubric, correctness judgment, stall result, human
record, or reviewer metadata in learner bytes invalidates the run.

Required deterministic fixtures:

- exact task/prompt/stimulus digests;
- explicit learner allow/deny enforcement;
- negative reviewer-string leakage;
- keyed edge/branch/boundary answers;
- invented-sequence rejection;
- zero-stall valid run; and
- byte-identical matched-arm inputs.

### Evidence and authority ceiling

Agent execution is structural pre-test evidence only
(`DEFINE.md:45-59`). Human comprehension requires a separately authorized human
witness.

The instrument cannot promote ontology meaning or establish runtime, release,
or production. The package remains `candidate-local`,
`authority_effect: none`, `release_admission: not-granted`
(`projects/body-war/ontology/business/profile.json:5-10`).

One-line repair: build a fresh isolated Body War reading task whose learner
generator cannot access reviewer-only measurement artifacts.

## CR-2 — Separate blocked gate, non-promotion, and projection meanings

Disposition: `keep-authority-constrained`  
Severity: `HIGH`

### Exact seam

Extend presentation annotations in
`authoring/view-catalog.mjs`. Let `scripts/generate-views.mjs` read
`profile.json` and `residue.json` strictly as removable projection inputs.

Current tone logic collapses different meanings
(`scripts/generate-views.mjs:482-505`), and the card details expose only the
relation owner (`generate-views.mjs:531-540`).

### Learner-visible surface

Render three distinct meanings:

1. `Blocked — owner decision required`
2. `Explicitly does not promote`
3. `Projection only`

For every displayed relation:

- preserve the existing `Relation owner`;
- find every residue item whose `affected_concepts` contains either displayed
  endpoint; and
- show every matching `Blocking owner` and `Next gate`.

Score-policy and geometry-privacy residue demonstrate the needed fields
(`residue.json:7-40`).

Display the exact package ceiling:

```text
candidate-local
authority_effect: none
release_admission: not-granted
```

### Reviewer-only surface

Keep an expected endpoint-to-residue join set and negative fixtures proving
that the projection did not invent:

- a new relation;
- a new status;
- one selected blocker when multiple residue records match;
- an accepted gate decision; or
- authority or promotion.

### Task, contamination, and acceptance

Boundary and distinguish tasks become keyed to literal relation, tone, owner,
and gate data rather than to color alone. Because the stimulus changes, it
receives a new digest and cannot be silently compared with old bytes.

Required checks:

- all three tones remain distinct;
- Relation owner remains present;
- zero, one, and multiple endpoint-residue matches work;
- every matching owner and next gate is visible and programmatically
  associated;
- the exact package ceiling is visible; and
- ontology node and relation digests remain unchanged
  (`receipts/validation-receipt.json:29-35`).

### Evidence and authority ceiling

Residue and profile are projection inputs only. The view explains existing
candidate meaning and unresolved owner routes; it does not decide a gate,
synthesize ontology relations, or promote anything.

Explicit non-promotion relations remain source-owned
(`authoring/view-catalog.mjs:159-168`).

One-line repair: join removable residue projection data by
`affected_concepts`, preserve Relation owner, and show every matching blocker
without creating ontology meaning.

## CR-3 — Repair causal, branch, collection, and no-JavaScript semantics

Disposition: `accept-with-authority-fix`  
Severity: `HIGH`

### Exact seam

Revise:

- catalog prose at `authoring/view-catalog.mjs:127-181,299-332`;
- relation-list and navigation rendering at
  `scripts/generate-views.mjs:546-589`;
- progressive enhancement at `scripts/generate-views.mjs:657-680`; and
- deterministic assertions in `tests/business-views.test.mjs`.

### Learner-visible surface

Remove only prose that implies unsupported causality, temporal execution,
verification, or proof. Preserve legitimate literal state and authority
vocabulary when the relation actually supports it.

Required structural changes:

- sibling navigation markers match the headings `A/B`;
- relation collections use unordered lists;
- both stories remain visible and navigable through ordinary links/content
  without JavaScript; and
- JavaScript progressively enhances that valid native surface into keyboard
  tabs.

### Reviewer-only surface

Keep:

- an edge-local expected-reading set;
- a list of unsupported causal or temporal paraphrases; and
- scoring rules that penalize an invented order or branch feed.

Do not penalize legitimate literal state or authority terms.

### Task, contamination, and acceptance

Trace and retell answers may use only admitted relations. Explanatory chapter
order is not runtime evidence. The catalog currently combines the correct
sibling note with conflicting causal prose
(`authoring/view-catalog.mjs:173-183,326-332`).

Required checks:

- A/B navigation and heading parity;
- unordered relation collections;
- native no-JavaScript access to both stories;
- JavaScript keyboard-tab enhancement;
- absence of the specific unsupported causal/temporal/proof prose; and
- every scored answer maps to an exact relation.

### Evidence and authority ceiling

Navigation and structural parity establish operability only. The journey
remains an explanatory relation projection, not runtime order, verified
evidence, authority proof, or comprehension evidence.

One-line repair: make wording and scoring relation-local, align A/B semantics,
and preserve complete native story access before progressive enhancement.

## CR-4 — Durable browser receipt before protocol admission

Disposition: `keep-scope-narrowed`  
Severity: `MEDIUM`

This is a blocker only for admitting the affected generated view as a novice
protocol stimulus. It does not block ontology validation or deterministic
artifact generation.

### Exact seam

Add a receipt-producing browser-validation lane for the exact generated
stimulus. Keep `scripts/generate-views.mjs --check` as the deterministic
generation gate. Existing tests only inspect source strings and structures
(`tests/business-views.test.mjs:102-118,161-196`).

The printable gallery remains outside the initial protocol unless it gets its
own stimulus/task definition and durable browser receipt.

### Receipt contract

Pin:

- stimulus and input digests;
- task, loci, prompt, catalog, and generator digests;
- Node, Playwright, and browser versions;
- browser revision, executable path, and executable hash;
- viewport, device-pixel ratio, JavaScript, no-JavaScript, reduced-motion, and
  print modes;
- runtime isolation behavior;
- exact assertions and artifacts;
- observed results, timestamps, failures, and terminal status; and
- agent-pretest and human-witness state.

### Acceptance and ceiling

Before protocol admission, verify:

- stimulus-only loading;
- keyboard behavior;
- responsive semantic structure;
- native no-JavaScript access;
- JavaScript progressive enhancement;
- reduced-motion and print behavior;
- boundary/owner/gate visibility;
- negative reviewer-data leakage; and
- exact artifact identity.

Browser success proves only the pinned rendering and interaction assertions. It
does not prove human comprehension, score correctness, ontology authority,
promotion, release, or production readiness.

One-line repair: require a fully pinned browser receipt before any generated
view becomes a novice-test stimulus.

## Smallest coherent follow-up implementation slice

1. Add the dedicated learner-task catalog, generator, HTML output, and tests.
2. Add reviewer-only protocol schemas and negative leakage fixtures outside
   learner generation.
3. Correct boundary tones, endpoint-residue projection, and package-ceiling
   rendering in the journey.
4. Correct causal prose, A/B navigation, unordered relation lists, and native
   no-JavaScript access.
5. Run deterministic and scoped Node validation.
6. Produce one pinned browser receipt for the exact candidate stimulus.
7. Run an agent structural pre-test only after those gates pass.

Do not run a human arm as part of that implementation slice.

This review does not implement or authorize the slice. Implementation requires
a separately approved bounded work package. Human witnessing requires a
separate authorization. Neither action changes ontology or release authority.

