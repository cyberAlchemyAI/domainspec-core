---
title: DomainSpec Core Project History
status: narrative
created: 2026-08-07
last_updated: 2026-08-08
scope: repository formation, owner evolution, v1-to-v2 transition, validation, formal correction, authority design, and bounded implementation evidence
authority_effect: none
voice_reference: business-philosopher/assuntos/meta-representations/meta-layers.md
voice_effect: style only; no historical or authority effect
---

# DomainSpec Core Project History

> The facts in this history come from DomainSpec Core and its separately owned
> repositories. The Business Philosopher repository provides an editorial
> voice through meta-layers.md: concrete examples before abstractions,
> feedback loops, visible tensions, and room for unresolved questions. It
> supplies no dates, milestones, authority, or proof.

## A parent learns how to be a parent

DomainSpec Core began by making a very understandable mistake: it tried to hold
too much.

On April 20, 2026, commit d96abdc3 created forty-five files and 8,739 lines
across research, experiments, and implementation mirrors. Later that day,
01f8ed53 connected the repositories that already owned the implementation and
its Poker Team validation. For one week, the new parent contained both the map
and copies of the territory.

Then the architecture became real. On April 27, 6158e841 removed 4,181 lines of
mirrored implementation documentation. The DomainSpec submodule remained; the
copies disappeared. The first important lesson in the parent history was
therefore expressed as a deletion: ownership was not merely something the
documents could describe. The filesystem had to obey it.

That movement—from a large idea toward explicit owners, and from explicit
owners toward evidence about their behavior—is the thread running through the
rest of the history. DomainSpec grew out of a broad specification-first
framework. Poker Team gave it a concrete project surface. Arcanum separated
reusable method from private intent. Formalization removed claims that could
not survive their assumptions. CyberAlchemy v2 made authority movement
explicit. DomainSpec v2 reconsidered which parts of its predecessor should be
carried, rewritten, or left behind. Saturn remained the name of a private loop
the architecture intends to close, not a shipped system that history may
pretend is already complete.

The result is not a clean march from version one to version two. It is a
sequence of corrections. Some arrived as theorems, some as failed runs, some as
deleted duplicates, and some as Git refusing to clone a topology the
documentation claimed was sound.

## Before there was a core

The parent repository is not the beginning of the work.

The oldest repository in the current topology is Poker Team, whose first
observed commit is dated January 8, 2026. DomainSpec-related activity appears
there by April 8. The repository contains typed feature specifications,
backend and UI work, observability, infrastructure, and governance changes.
That establishes pre-parent project activity. It does not establish
acceptance, production use, commercial success, or any other external outcome.

Legacy DomainSpec begins its own observed history on March 29. Release 1.0.0
assembled a typed specification kernel, relationships, document-to-test rules,
templates, examples, and an agent pack. April then widened the frame:
capability-driven specifications were followed by UI and end-to-end guidance,
richer meta-types, observability derivation, OpenTelemetry conventions,
infrastructure, verification, asynchronous signals, and governance baselines.

By April 25, the legacy changelog called the framework 2.0.0 and added
cross-feature composition through Saga and new relationship edges. The later
2.0.x and 2.1.0 entries added a unified startpoint, orchestration, strict
context selection, delegation policies, liveness controls, recovery,
interviews, feature architecture, glossaries, and implementation layering.
This was becoming a broad delivery framework, not merely a language for
describing domains.

The version number matters because the name later becomes overloaded. Legacy
DomainSpec 2.0.0 belongs to the implementation repository and its April release
history. It is not the separate program later created under
[projects/domainspec-v2](projects/domainspec-v2/).

Four related objects therefore travel through this story:

- **Legacy DomainSpec** is the framework under
  [implementation/domainspec](implementation/domainspec/).
- **DomainSpec Core** is the parent workspace whose root Git history begins on
  April 20.
- **The private DomainSpec pillar** is the current typed-intent owner, not a
  release label.
- **DomainSpec v2** is the separately governed program under
  [projects/domainspec-v2](projects/domainspec-v2/).

The names form a lineage. They do not make their evidence interchangeable.

## April 20–27 — the direction of learning reverses

The two April 20 commits gave the parent its first topology. The first created
the workspace; the second replaced informal linkage with Git submodules. The
parent could now coordinate research and orchestration while implementation
and validation retained their own histories.

What happened the following day makes the topology more interesting.

On April 21, legacy DomainSpec commit f0f6987 promoted twenty-seven files from
Poker Team after a file-by-file migration. Infrastructure, OpenTelemetry, user
story, UI, pipeline, reflection, and readiness material moved from the concrete
project back into the canonical agent and skill pack. Commit 8705f76 then
synchronized the pack documentation and added a drift guard.

The direction of travel was not one-way. Poker Team was not merely waiting at
the end of a pipeline to validate a finished framework. Concrete project work
was feeding material back upstream into the framework that was supposed to
guide it. Git witnesses the migration; it does not prove the resulting methods
were effective. But it does show that validation had already become a place
where the framework changed.

Six days later, the parent removed its implementation mirrors. Put together,
the sequence tells a compact story: create the workspace, connect the owners,
accept feedback from a concrete project, and remove the copies that blurred
ownership.

## Early May — failure begins writing the operating model

The first half of May reads less like a feature roadmap than a system
discovering the verbs it had forgotten.

On May 2, 82e6603d rolled planner-gate policy across DomainSpec skills. In the
legacy implementation history, planner-gated execution and routing changes
landed beside it. By May 6, c8c4175 was fixing knowledge-graph tag drift and
capturing retry outputs, while root commit bd673289 hardened delegation
watchdog telemetry and recorded a rerun. On May 7, 1ce5fe93 hardened ripgrep
timeout recovery; the legacy repository recorded remediation artifacts,
navigation regression, and stuck-stage guards. On May 11, 39d799ae hardened
the terminal guard and its wrapper workflow.

These subjects are not a universal incident report, and chronology alone does
not prove that one commit caused the next. They support a narrower and more
useful observation: retry behavior, drift, navigation regression, timeouts,
delegate liveness, and terminal failure had become visible enough to receive
named controls.

This is where the later lifecycle begins to take shape. Selecting a plan is not
the same as admitting a task. Admitting a task is not the same as executing it.
A successful command is not the same as a closed handoff. Validation is not an
external effect. The distinctions may look procedural when written as rules;
in the commit history, they look like answers to things that went wrong.

The project did not prove reliable autonomy in May. It began making failure
legible.

## May 14 — Arcanum steps out of the parent

Arcanum did not arrive as a finished public platform or through a single grand
declaration. Its emergence can be watched almost commit by commit on May 14.

The parent first installed Necronomicon for the Sonar Loop in cf0f9975. It
added a context bundle in a42bb126, regenerated the runtime in aa738c36,
updated the repository command bundle in 5f635e03, recorded command telemetry
in efa85f44, and then linked the Arcanum command bundle in 0e9d5e71. Runtime
bridges followed the next day in f075f8fc. The separate Arcanum repository
begins its own observed history on the same date with 4a5ede5.

The order matters without needing a heroic interpretation. Installation was
followed by context, regeneration, commands, observation, and ownership.
Arcanum entered the record as method already in motion, not as a polished
product appearing fully formed.

Its early history established tiers, lifecycle, registry, Necronomicon,
Invoke, observed-run hooks, experiments, telemetry, and centralized indexes.
From May 19, that history used the then-current CyberAlchemy name for reusable
method and capability vocabulary. This is a historical name inside Arcanum; it
is not the private CyberAlchemy v2 authority spine that appears in June.

From May 21 onward, the center of gravity moved toward execution: task-session
adapters, experiment profiles, context handoff, ontology lifecycle, runtime
adapters, Invoke refresh, and native skill surfaces. June and July added
deterministic tools, public research capabilities, capability-bound dispatch,
durable handoffs, typed status and event evidence, continuation routing, join
policies, blocker propagation, and stricter runtime ownership.

The public method layer therefore emerged through use, replacement,
observation, and separation. Its [README](arcanum/README.md),
[runtime model](arcanum/framework/runtime/README.md), and
[observability architecture](arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md)
describe the current public surface. They also preserve seams: parity is
uneven, observation is not assumed, and a receipt remains necessary precisely
because execution cannot certify itself.

## May 24 — the project learns how not to forget

Repositories are good at remembering bytes. They are less good at remembering
why one piece of work had to wait for another, which uncertainty was still
dangerous, or how a small result was supposed to return to the larger thing
being built. A conversation could reach that understanding and still leave the
next conversation with little more than a folder of plausible documents.

Craft began on May 24 inside that gap. Its
[initial definition](arcanum/development/craft/CRAFT-INITIAL-DEFINITION.md)
did not start from a command or a database. It started from a problem of
translation: intention becomes a schema; people, models, tools, and context
turn that schema into an artifact; the translation leaves residue. Craft was
the proposed method for deciding whether that residue belonged in the current
layer, required a smaller coherent layer of its own, or had to be carried back
into the larger work.

The first important restraint appeared beside the ambition. Craft was a
candidate, not a new name for the whole system. Its
[durable session context](arcanum/development/craft/DURABLE-SESSION-CONTEXT.md)
forbade it from absorbing Invoke, Refine, Distill, or Task Session. Those
capabilities would continue to author, reduce, or execute their own artifacts.
Craft would remember the contexts, blockers, decisions, gaps, evidence, and
recomposition paths between them. Even the development of Craft became its
first recursive test: the first smallest coherent unit was not “build Craft,”
but a bounded method-architecture package that could later rejoin the method.

Four days later, the idea acquired a ledger. The first Task Session created a
fixture with eight contexts, eighteen artifacts, thirteen relations, nine typed
items, and four decisions. The next sessions made blocker state explicit:
`raw`, `refined`, `resolved`, and `waived` were not interchangeable, and a raw
blocker could not leap directly to resolution. By May 29, the storage choice
was also becoming clear: structured ledger state would own the truth; readable
Markdown and a future machine index would be projections of it.

Then Craft produced a more revealing result by refusing to proceed. The
architecture work-pack was complete and its prose named a reasonable next
move: use the validation strategy on another sequence. Task Session returned
`BLOCK`. A useful sentence about what should happen next was not yet an
executable task: it had no selected work-pack item, write scope, done criteria,
or bounded validation surface. The refusal was small, but it captured what
Craft was becoming. Continuity was not a paragraph that sounded continuous.
It was a graph whose next edge had to exist.

The sharper test came on June 1. An early Refine run over Craft’s validation
document reported every stage as passing. The evidence repeated the same
reason: the stage command had produced output. That looked green until the
system asked what the output actually proved. A runtime handoff stub proved
that work had been prepared for an owner; it did not prove that Context
Builder, Invoke, Interrogation, or Distill had executed their owned stage and
returned a verdict.

The rerun changed the first such stage to `flag` and blocked everything that
depended on it. Later runs named the evidence kinds directly—observer envelope,
handoff prepared, receipt, blocked—and kept the aggregate Refine receipt at
`block` even after several early stages acquired real receipts. The dispatch
shape itself could validate while the work remained unexecuted. A file could
exist while its obligation remained open.

This was not Craft single-handedly inventing every receipt rule that Arcanum
would later use. It was a Craft validation sequence exposing the weakness and
forcing the shared runtime record to become more honest. The distinction that
survived was consequential: an emitted artifact is evidence of emission; a
handoff is evidence of preparation; a called capability’s receipt is evidence
of that capability’s result. None may impersonate the next.

### June 6–10 — AutoBayes puts Craft’s entropy on trial

Then an elegant piece of mathematics entered the story. AutoBayes, an arXiv
preprint about compositional generalized variational inference, seemed almost
uncannily close to Craft’s concerns. It separated a model from its inversion,
made local losses composable, exposed parameters explicitly, and kept the
optimization semantics accountable. Craft already spoke about translators,
residue, and the cost of breaking a difficult whole into smaller coherent
units. For a moment, the new theory looked capable of giving that language a
formal home.

The repository did not let resemblance become authority. On June 6 it opened
an [AutoBayes research tower](arcanum/research/autobayes/README.md) whose claim
kinds separated the paper’s results from derived readings and Arcanum
analogies. Two research fan-outs filled the tower with definition cards,
worked examples, boundary notes, and operator distills. Both also preserved an
awkward operational fact: the planned distill-steward could not start because
the agent thread cap had been reached. Parent synthesis closed the gap, but the
receipts kept the residue visible. By June 7, the
[learning pack](arcanum/research/autobayes/FINAL-LEARNING-PACK.md) could explain
the paper locally; it still authorized no vocabulary promotion, runtime, or
canonical Craft change.

On June 8, the investigation turned the new lens back on Craft. “Translation
entropy” had been doing too many jobs at once. The
[definition card](arcanum/research/autobayes/tracks/craft-entropy-definition-card.md)
separated a distributional-spread term from divergence or fit pressure, relational
recomposition cost, and degradation of the translator under attention load.
Calling the whole bundle entropy had made one word sound more explanatory than
the evidence allowed. AutoBayes supplied a disciplined analogy for local loss
composition; it did not license that bundle as a theorem.

The most attractive picture was a U-shaped curve: units too large would
overload the translator, units too small would lose meaning through excessive
fragmentation, and a smallest coherent unit would sit at the minimum. The
[experiment design](arcanum/research/autobayes/development/refinement-runs/refine-scu-entropy-experiment-20260608/RESULT.md)
made the claim falsifiable and immediately weakened it. Semantic-entropy
dispersion by itself should fall as the unit becomes more specific; it is not
U-shaped. A U appears only after combining a descending spread term with a
rising overload or recomposition term. The pilot was designed, not run. A
parallel [prior-art audit](arcanum/research/autobayes/tracks/craft-entropy-novelty-verdict.md)
reached a sharper candidate verdict: what had first looked like a narrow new
protocol collapsed, on a second pass, into a full restatement of familiar bias–variance,
rate–distortion, semantic-entropy, and compositional ideas applied to an
agentic-work setting.

Craft then tried a less lyrical route: measure the residue already present in
its own execution records. The proposed Design Coherence Index separated clean
records at 100 from residue-bearing records averaging 71.7 across a 398-record
[backtest](arcanum/research/autobayes/development/refinement-runs/refine-coherence-metric-20260608/RESULT.md),
with no overlap. That sounded decisive until the shape of the result was
examined. DCI was a bimodal anomaly flag, not a smooth gauge of intelligence,
entropy, or coherence. Its reopen term merely echoed an existing trigger, and
the data did not show residue rising with unit size. Residue tracked weak
validation more closely, while unit size was confounded with which capability
had run.

Instead of proving Craft, the AutoBayes episode made Craft easier to prosecute.
It left behind a narrower candidate: the smallest coherent unit was not simply
the smallest or the point of minimum “entropy,” but a unit of minimum residue
density subject to singular responsibility and explicit recomposition. Even
that [revision](arcanum/research/autobayes/development/refinement-runs/refine-coherence-metric-20260608/CRAFT-DEFINITION-REVISION.md)
remained unapplied. The historical definition kept its older U-curve language,
and the later canonical Craft surface contains none of the AutoBayes, DCI, or
translation-entropy terms.

The [formal-foundations map](arcanum/development/craft/CRAFT-FORMAL-FOUNDATIONS.md)
preserved what survived. It placed the Lean formalization beside Craft as a
discrete categorical cousin and AutoBayes beside it as a continuous
probabilistic cousin. That was useful, but it was not a mathematical
coronation. Lean supported constraints such as checking schema and instance
fidelity separately and recognizing finite residue plateaus. AutoBayes
supported the narrower idea that local probabilistic losses can compose inside
its own framework. Neither proved that an arbitrary Craft artifact was correct,
and the LLM-centered translator remained on the analogy side of the boundary.

By June 8, the method had also acquired explicit
[interface](arcanum/development/craft/CRAFT-INTERFACE.md) and
[interaction](arcanum/development/craft/CRAFT-INTERACTION-CONTRACT.md)
contracts. Craft could classify a route, prepare a handoff, receive a receipt,
open residue, and apply the receipt to its local state. It could not rewrite
the called capability’s verdict. A Task Session pass still needed
recomposition evidence before it could close a Craft context, and a Dispatch
Spec pass still proved route shape rather than execution.

Promotion did not happen at the first green architecture review. The May 29
[readiness assessment](arcanum/development/craft/CRAFT-PROMOTION-READINESS.md)
said `defer`: the examples were fresh and mostly manual, and repeated use was
missing. Further interface validation and project-ledger examples followed.
On June 12, Arcanum commit ed25dd2 promoted Craft into the canonical Arcana
surface. The historical material under `arcanum/development/craft/` became
promotion and failure evidence; the current contract moved to
[arcanum/arcana/craft/](arcanum/arcana/craft/README.md).

That distinction still matters. Canonical Craft remains intentionally small
and file-backed. Its [current architecture](arcanum/arcana/craft/ARCHITECTURE.md)
keeps `.craft/ledger.yml` as the source of truth. `CRAFT.md` is a human view,
and `.craft/index.json`, when present, is rebuildable machine data. The corpus contains designs for richer
schema stacks, row updates, projections, and runtime helpers, but the current
contract does not claim a public CLI, automated command runner, packaged
renderer, or canonical database service.

The retained Claude session history shows what happened after promotion more
clearly than it shows Craft’s birth. No retained May transcript for the origin
conversation was found. On June 29, however, a session began by opening a new
Craft context for DomainSpec v2 inside the CAV2 scope. By July 1, the operator
was asking that Invoke results be refreshed and recorded in Craft. On July 6,
another session used `craft state` to recover the DomainSpec v2 frontier, then
asked to apply refreshes, rebase the ledger, and show the next task. The
[DomainSpec v2 ledger](projects/domainspec-v2/.craft/ledger.yml) had become more
than an archive: it was the place from which interrupted work could be resumed
without pretending that every open context was ready.

As Craft spread into other project scopes, it also had to learn how to explain
itself. July’s
[storytelling research](arcanum/development/craft/research/craft-storytelling-essay-research-2026-07-09/findings.md)
replaced the abstract method lecture with three ordinary failures: the table
that is not yet a buildable table, the difficult step that becomes a build of
its own, and the dashboard that looks finished while answering the wrong
question. Later class material used a wobble and a shim to make the same point:
splitting work is useful only when the smaller layer can be validated and then
recomposed into the whole. Craft is not a ritual for making tasks tiny.

By August, a different pressure had appeared: could a database make the ledgers
faster to query without becoming their authority? The WaveDB research admitted
only a disposable, digest-bound projection experiment. When its first
execution unit found a package-provenance mismatch, the chain stopped before
installation, build, or native execution. No Craft runtime was proved. It is a
fitting current boundary for the chapter: the method born to preserve residue
did not let a convenient projection erase the uncertainty in its own source.

## Formalization teaches the project to be contradicted

While the operational history was learning from retries and regressions, the
formal history was learning from statements that did not survive.

The Lean program began with claims that sounded closely related. Formalization
separated them. Schema loss was not instance loss. Structural preservation was
not semantic adequacy. A count could constrain a translation without supplying
the readout, faithfulness, or empirical grounding required by a stronger
claim. A clean construction at one level did not silently become correctness at
another.

That correction changed the role of mathematics in the project. Lean was not a
seal placed over the architecture. It became an instrument for finding the
point where the architecture's language had outrun its assumptions.

The [Lean project history](domainspec-lean-formalization/PROJECT-HISTORY.md)
records this as a retrospective sequence of counterexamples, restricted
results, and reformulated questions. It also records why attractive slogans
were demoted: one witness is not yet a condition, one readout is not every
readout, and a theorem about a bounded model does not certify elicitation,
implementation, users, or production behavior.

What survived was less spectacular and more durable: claim ≤ proof.

## June 10 — Git refuses the architecture

By June, ownership had become a design principle. Then a fresh clone showed
that the repository topology did not yet honor it.

Commit ce1bb259 records the failure directly. The validation directory
contained an orphan sigil-spell-sandbox gitlink with no remote and no entry in
.gitmodules. It broke fresh clones and was surfaced by make doctor. The repair
removed the orphan and added
[SUBMODULE-DISCIPLINE.md](SUBMODULE-DISCIPLINE.md), branch tracking, and
Makefile commands for bootstrap, configuration, status, synchronization,
bump-check, and diagnosis.

The resulting rule—submodule first, parent last—was not born as decorative
governance. It was the repository's answer to a topology that could not be
reconstructed.

Two days later, b08d5085 removed a second kind of duplication: 711 lines of a
legacy sigils library whose packages had been superseded by native skills. The
installed skills became the single home. Once again, the architectural move
was subtraction. A declared owner became credible only after the stale
alternative stopped competing with it.

## June 14 — becoming public by publishing less

The public DomainSpec wedge is another story that reads differently in the
commits than it does in an architecture diagram.

Commit abf64284 moved a deliberately small DomainSpec vocabulary and spec
template into public Arcanum. The private moat cluster and ambiguous
definitions stayed private. The commit also recorded a green leak audit and a
deferred removal that was still referenced elsewhere. Later that day,
b224b138 replaced nine duplicated private definition bodies with pointers to
their public owner. On June 15, 1495bac7 made the wedge canonical in Arcanum
and removed roughly 120 more lines of duplicated private prose.

Public movement therefore meant selection, scrubbing, owner transfer, and
de-duplication. It did not mean opening the entire DomainSpec pillar. It did
not make Saturn public. Only Arcanum became the public reusable method surface.

The commits are useful here because they show that publication was not
addition alone. It was also the removal of private copies after a public owner
had been established.

## June 17 — an append-only rule meets a merge conflict

Governance soon encountered an ordinary version-control problem.

Commit 788ec733 extracted dispatch-record mechanics from the subagent strategy
router into a dedicated owner. The router had been carrying form-filling logic
that belonged somewhere narrower. The next commit, f197c9b2, marked the
append-only dispatch ledger with Git's union merge behavior.

The reason is almost comic in its precision: two branches could each append a
valid row, Git could produce a conflict, and the append-only guard would then
forbid the manual conflict resolution needed to keep both. The governance rule
and the merge mechanism were each sensible in isolation; together they
deadlocked.

The repair did not weaken the append-only rule. It changed the repository
mechanism so concurrent additions could coexist. This small episode captures a
larger pattern in DomainSpec Core: constraints become trustworthy when they
survive contact with the tools that must enforce them.

## June — a pass that keeps its failures

The deterministic test-derivation work contains one of the clearest bounded
learning loops in the repository.

Its [round-trip report](development/deterministic-test-derivation-engine/L0-ROUNDTRIP-REPORT.md)
preserves three moments. An original four-document financial-settlement input
missed obligations and failed. A repaired seven-document version passed its
recorded gate. A second access-control feature still failed.

The repaired pass did not erase the first miss, and the first pass did not
generalize over the second feature. Keeping all three beside one another made
the report more valuable than a clean success story. It showed a derivation
surface becoming more precise while preserving the boundary of what had
actually worked.

The checks were not rerun for this history. The sound claim is one
source-reported build–fail–repair episode and one remaining bounded failure,
not a universal intent compiler or a production test pipeline.

## June 19 — governance becomes something you can click

The [UI Prototyping Studio](projects/ui-prototyping-studio/README.md) made an
abstract governance idea visible in a browser.

Commit 46157a70 records a loop from preview to annotation, pending synthesis,
two-gate apply and accept, and revert. It added human and automatic modes,
treated reversibility as the main safety property, and kept export as the
irreversible gated edge. Its commit message reports sixty-one unit tests,
thirteen Playwright end-to-end tests, and a clean typecheck.

Those checks were not rerun for this history, so they remain source-reported.
What the commit supports is a bounded local interaction surface where
governance acquired buttons, state changes, and an undo path. It does not
support claims of accessibility, external human validation, publication, or
release.

## June 21–26 — CAV2 builds a language for what may count

Capability execution answers how work is done. It does not answer who may
change what counts as owned truth. CyberAlchemy v2 appeared to make that second
question explicit, and it did not begin with a finished authority model. The
model and its vocabulary grew into one another.

Root commit 7e776e65 added the private CyberAlchemy v2 project tree on June 21
under the label “stable repository.” The label records its design ambition,
not evidence that the project was already standalone, complete, or shipped.
Its canonical definitions file arrived with twenty-six cards. The count became
twenty-seven later that day, thirty-three on June 22, forty on June 23,
forty-nine on June 24, and fifty on June 26. That acceleration is evidence of
an intense definition-making period, not evidence that every definition was
correct.

These were not meant to be dictionary entries. The emerging
[definition towers](cyberAlchemy-v2/authority/definitions/DEFINITION-TOWERS.md)
asked a term to speak normatively, formally, operationally, and in plain
language, then to declare its boundaries and relations. An
[index](cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md), a
[schema registry](cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md),
and a [drift audit](cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md)
made the surrounding work inspectable. Behind the promoted cards sat 149
staged candidates waiting to be clustered, deduplicated, and localized. The
[primordial-basis handoff](cyberAlchemy-v2/TO-VLAD/SESSION-HANDOFF-cav2-primordial-basis.md)
is candid about that unfinished work: being found by inventory or arranged by
ontology did not promote a term by proximity.

That same boundary shaped the repository itself. A June 22
[definitions session](sessions/2026-06-22-1830-definitions-governance-cav2.md)
found that sigil, spell, and capability were not yet formally owned even in
Arcanum. CAV2 did not seize the names. The recorded decision was to define the
public terms upstream and let the private spine reference them. Vocabulary had
become an ownership problem, not merely a writing problem.

On June 24, 224331e4 introduced the authority-model path beside
authority-lifecycle schema, inventory, and governance-review work; the commit
itself called the checkpoint in progress. The resulting
[source map](cyberAlchemy-v2/SOURCE-MAP.md) and
[authority model](cyberAlchemy-v2/authority/AUTHORITY-MODEL.md) separated
source evidence, import candidates, inventory and ontology candidates,
owner-routed local authority, implementation or validation, and stable assets.
The core rule was short: authority moves by owner route, not by proximity,
usefulness, repetition, or a passing check. Evidence may support a decision.
Ontology may organize a candidate. Inventory may make it discoverable. None of
them may promote itself.

The new language was tested almost immediately by its own mistakes. Commit
a37dab67 repaired an alias collision in which “pattern authority lifecycle”
resolved to both CAV2-D48 and CAV2-D43. Two days later, 66c17bf8 added CAV2-D50
discipline and a handoff for a non-collapse validator while holding back a
ledger definition whose conditions were not met. Authority did not appear as
perfect vocabulary. It appeared as a surface that could notice when two terms
claimed one route, refuse an attractive term, and leave the refusal on record.

## July 8–14 — the definitions are allowed to fight back

By July, the question was no longer whether CAV2 could produce definitions. It
was whether those definitions could survive contact with one another. A
[contradiction-and-collapse review](sessions/2026-07-08-1333-definitions-contradiction-collapse-review.md)
put the fifty-card corpus under adversarial pressure. Attackers proposed nine
cuts and a reduction toward roughly forty-two terms. Three verifiers rejected
all nine. Then the final auditor overruled the unanimous verification and
reinstated one major contradiction: D29 allowed a loose owner decision to link
two axes while also demanding D16's full seven-field typed relation. The count
mostly survived; the claim of internal consistency did not. More importantly,
the review found that the linking rule still had no validator or typed-relations
runtime behind it.

The next definitions sharpened distinctions that ordinary prose had allowed to
blur. Commits 314f4700 and 14be682f added canonical artifact, durability,
axiom, invariant, and premise. The accompanying
[session](sessions/2026-07-08-1520-cav2-axiom-invariant-premise.md) separated a
canonical artifact from an authoritative one: a recognized kind does not grant
itself authority. Tests against two real axiom corpora also reclassified many
supposed axioms as system invariants and the explicitly uncertain entries as
premises. Yet the same session recorded that enforcement remained review-first,
with no act-time gate wired to make agents obey the distinctions.

The vocabulary then turned on one of its newest cards. CAV2-D51 said a
canonical artifact declared an authority kind, even though its own schema said
that authority kind was inherited. Commit 88a06b14 repaired the contradiction:
an artifact declares its canonical kind and origin, but it cannot choose its
own authority. The repair exposed a deeper hole. Its formal predicate called an
undefined `process` function, so the repository recorded the predicate as
undecidable instead of disguising the gap. A proposed CAV2-D56 definition of
process was promoted and retracted the same day after a counterexample showed
that it had been reverse-engineered from D51's needs. The identifier later
belonged to a different concept. This was definition-making with a memory: the
withdrawal followed the promotion in the drift record rather than rewriting it
away.

The concept that eventually received D56, schema, carried its own argument
with history. A June 22
[thirteen-agent review](sessions/2026-06-22-1945-cav2-definitions-schema-governance.md)
had rejected a generic objects–morphisms–laws definition and chosen a minimal
registry approach. In July, operator corrections and broader examples exposed
limits in the inherited wording, and the new card described schema through
kinds, occupant constraints, relations, and connection rules. Commit 16f1909e
records coverage against four different structures. But the
[D56 session](sessions/2026-07-13-1152-cav2-d56-schema-definition.md) also says
plainly that this overturned the earlier verdict without filing its requested
D25 witness or discharging its redundancy argument. The commit proves the card
landed. It does not prove the dispute ended.

Nor did the identifier system emerge clean. The canonical
[definitions](cyberAlchemy-v2/authority/definitions/DEFINITIONS.md) currently
assign D34–D37 to authority, provenance, traceability, and gate. The live schema
backlog assigns those same IDs to constitution, discipline, decision, and spec.
A July 13
[critical assessment](sessions/2026-07-13-1142-authority-definition-critical-assessment.md)
also found that D34's literal admissibility record was instantiated nowhere in
the inspected authority and ontology corpus. Those are unresolved defects in
the current tree, not colorful problems from a safely closed past.

By July 14, the file held fifty-six definition cards. The important number is
not fifty-six. It is the sequence around it: propose, distinguish, collide,
review, repair, retract, and sometimes reopen. CAV2's authority model became
credible not because its vocabulary stopped changing, but because the record
shows occasions when the vocabulary was permitted to say “this does not count
yet” about itself.

The dated [Saturn layer map](ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md)
belongs to the same June moment. It describes the intended private loop from
typed intent toward evidence and correction, and it records gaps in that
design. It does not establish a Saturn repository, a deployed convergence
loop, or a production capability.

## June 29–30 — v2 refuses a wholesale inheritance

Calling the movement from legacy DomainSpec to DomainSpec v2 a migration is
almost too gentle. The triage did not ask which directory should receive the
old files. It asked which responsibilities still had the right owner.

The June 29
[import triage](projects/domainspec-v2/research/2026-06-29-v1-import-triage/findings.md)
examined thirty-two de-duplicated capabilities. Its verdict was three genuine
imports, twenty-five reformulations, and four drops.

The three imports were the deterministic spec-to-test executor, its stable
obligation-key identity seam, and a concurrency/TOCTOU discrimination edge.
The first two were carried into the engine fork; the triage records the third
as unwitnessed and still absent. The reformulations covered the large middle:
rules, validators, drift tools, audit methods, taxonomy, edge law, telemetry,
and governance doctrine that already had owners but needed to be re-authored
for v2. The four drops removed a superseded LLM generator, the full
application-building pipeline, automatic promotion-status writing, and
application-runtime concerns below the new adapter line.

The same triage rejected “Lean is the moat” as a framing while retaining Lean
as evidence and an amplifier. That is not a fifth discarded capability. It is
a discarded explanation of where the project's defensible advantage lies.

The next day, b0f35d43 created the DomainSpec v2 implementation home and called
its L0–L2 build green. The commit reports 97 of 97 engine tests, 8 of 8 tag
tests, successful validation, and successful typechecking. It also records its
own weakness: the C10 lint check was vacuous until a real feature pack arrived.
C9 and C11 discriminated; C10 could not yet prove that it would.

That is one of the most revealing moments in the history. The milestone was
allowed to be green, but not allowed to pretend that green meant complete. Its
residue travelled inside the receipt. The same commit left v1 untouched and
read-only while stating that the formal freeze still depended on unfinished
reformulation.

The [import manifest](projects/domainspec-v2/IMPORT-MANIFEST.md) still describes
migration in progress. July added local definitions, relationship authority,
integrity receipts, conformance work, engine and generation work, and
architecture packages. August added architecture-realization work packs and
ontology-guided lifecycle canvases. These are committed materials and bounded
witnesses, not proof that every reformulation closed or that v2 became a
production release.

## July and August — evidence reaches more surfaces

By late July, the repository held more than architecture prose. It also held
local surfaces on which parts of the architecture could be exercised.

The ontology candidate graph
[task-session result](cyberAlchemy-v2/development/ontology-candidate-graph-prototype/planning/work-pack/session-evidence/SWU-OCGP-001/TASK-SESSION-RESULT.md)
records a candidate-local carrier and rejection tests. It does not establish a
complete ontology, grounding, admission, or promotion.

The [IDE Extension](projects/ide-extension/README.md) records a local
workbench, and later commits connect state projection and workbench behavior.
It does not establish an autonomous IDE, deployment, or adoption.

[Akashic Records](projects/akashic-records/README.md) records a bounded graph.
The admitted evidence does not establish its origin date, and the graph does
not become source truth by being searchable.

Private [Mint](cyberAlchemy-v2/development/mint/README.md) records bounded
implementation and synthetic validation inside an incomplete,
intended-not-shipped lifecycle. Mint promotes nothing, and its current evidence
does not prove that a repository was minted.

These artifacts matter because they let parts of the architecture meet bytes,
state, and behavior. They remain local witnesses. Multiplying witnesses is not
the same as integrating the entire system, and large generated commits are not
a maturity metric.

## What changed between the two DomainSpecs

Legacy DomainSpec tried to keep the path from specification to application
close together. Its framework included language, relationships, agents, test
derivation, UI, observability, infrastructure, orchestration, and governance.
That breadth gave projects a coherent starting point, but it also made
ownership harder to see.

The later architecture separated those responsibilities. Reusable ways of
working moved toward public Arcanum. Private CyberAlchemy v2 made authority and
promotion routes explicit. DomainSpec v2 narrowed its concern toward typed
intent, owned definitions, relationship laws, evidence obligations, and local
validation, layering, and drift governance. Application-runtime concerns were
placed across an adapter line rather than absorbed into the language owner.

This is why v2 could not be produced by copying v1. The old framework was both
precedent and evidence. Some of it could cross unchanged. Most of it needed a
new formulation because the owner or abstraction had changed. Some of it had
to stay behind because it would let the new language owner decide application
behavior or promote its own status.

Saturn remained separate from both. It names the private intent-to-reality loop
that would compare typed intent with evidence and return pressure for
correction. A name and a layer map are not evidence that this loop is already
operational.

## Where the story stops

The current architecture keeps four owners distinct. DomainSpec owns private
typed intent. Arcanum owns public reusable capabilities and their documented
runtime and observability surfaces. CyberAlchemy v2 owns the private authority
spine: vocabulary, source routing, owner routes, and promotion gates. Saturn
names the private convergence architecture rather than a repository or shipped
component.

The separation is not ceremony. Each owner answers a different question:
what is intended, how bounded work is done, who may change owned truth, and how
reality could return evidence to the intent.

Several frontiers remain open. Separate owners and local witnesses do not yet
prove one complete runtime. Candidate and inventory surfaces still need their
owner gates. Arcanum's native execution and observation surfaces retain seams.
Formal structure still cannot prove that elicited intent matches the lived
domain. Validation activity does not establish user, business, or production
outcomes. A plan, green gate, contract, or receipt does not by itself establish
publication, deployment, adoption, or production readiness.

The cited repository history therefore records a parent workspace forming
around separately owned implementation and validation repositories; Arcanum
acquiring separate ownership and developing public capability and runtime
surfaces; formal invalidations, operational incidents, deterministic-derivation
results, and bounded local prototypes informing documented corrections; and
private CyberAlchemy v2, DomainSpec v2, and Saturn-facing architecture being
specified without collapsing their owners.

This is evidence of repository formation, committed mechanisms, bounded
executions, and candidate architecture. It is not evidence that a complete
three-pillar system was integrated, publicly shipped, deployed, adopted,
production-ready, or operationally closed.

## Evidence note

A commit dates bytes entering one observed history; it does not date the birth
of an idea or prove operational success. An owned document records what its
owner says; it does not execute itself. The Lean history is retrospective
where an exact nested commit is not named. The deterministic derivation, UI
Studio, and Mint validations remain source-reported because this history did
not rerun them. A candidate or passing bounded receipt has no authority,
publication, deployment, or release effect by itself.

The Craft chapter uses retained local Claude transcripts only to corroborate
later use from June 29 onward. Those transcripts are not repository authority,
and no retained May transcript for Craft's origin conversation was found. The
May 24 initial definition remains the durable source for that origin. No direct
June AutoBayes conversation was found in the retained Claude transcripts;
repository-local research towers, Task Session receipts, refinement results,
and Git history are the evidence for that episode. The cited AutoBayes source
is an arXiv preprint, not evidence of peer review, and the chapter avoids exact
theorem selectors where local notes and the current paper version disagree.
The repository-wide Craft census also includes generated evidence, staged
copies, and nested specialist scopes, so file or ledger counts are footprint
evidence, not proof of independent adoption or successful execution.

These limits make the story less theatrical in one sense and more interesting
in another. The important moments are not the ones where the repository gives
itself a large name. They are the ones where it preserves the failure, deletes
the duplicate, narrows the claim, or admits that a green gate still contains
residue.

## Source map

### Repository formation and feedback

- Parent formation and topology: root commits d96abdc3 and 01f8ed53, plus
  .gitmodules history.
- Parent mirror removal: root commit 6158e841.
- Legacy DomainSpec:
  [README](implementation/domainspec/README.md),
  [CHANGELOG](implementation/domainspec/CHANGELOG.md), nested commits f0f6987
  and 8705f76, and its nested Git history.
- Validation activity: nested Git history under validation/poker-team.

### Execution, ownership, and public movement

- Early gates and failure controls: root commits 82e6603d, bd673289,
  1ce5fe93, and 39d799ae, with the cited legacy DomainSpec commits.
- Arcanum emergence: root commits cf0f9975, a42bb126, aa738c36, 5f635e03,
  efa85f44, 0e9d5e71, and f075f8fc; nested Arcanum Git beginning at 4a5ede5.
- Current public Arcanum:
  [README](arcanum/README.md),
  [runtime model](arcanum/framework/runtime/README.md), and
  [observability architecture](arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md).
- Craft origin and first ledger:
  [initial definition](arcanum/development/craft/CRAFT-INITIAL-DEFINITION.md),
  [durable session context](arcanum/development/craft/DURABLE-SESSION-CONTEXT.md),
  [first MVP result](arcanum/development/craft/task-sessions/20260528T200430Z-CRAFT-MVP-001/RESULT.md),
  and the [next-task block](arcanum/development/craft/task-sessions/20260529T163804Z-NEXT-TASK-BLOCK/RESULT.md).
- Craft's receipt correction:
  [initial false-green run](arcanum/development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/RESULT.md),
  [first corrected block](arcanum/development/craft/development/refinement-runs/20260601T010740Z-craft-validation-md/RESULT.md),
  [typed evidence run](arcanum/development/craft/development/refinement-runs/20260601T014741Z-craft-validation-md/RESULT.md),
  and [aggregate receipt run](arcanum/development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RESULT.md).
- Craft and AutoBayes:
  [research tower](arcanum/research/autobayes/README.md),
  [June 6 research receipt](arcanum/research/autobayes/sessions/task-session-autobayes-full-mode-result.md),
  [June 7 fan-out receipt](arcanum/research/autobayes/sessions/task-session-autobayes-all-possible-subagents-result.md),
  [learning pack](arcanum/research/autobayes/FINAL-LEARNING-PACK.md),
  [entropy definition card](arcanum/research/autobayes/tracks/craft-entropy-definition-card.md),
  [novelty verdict](arcanum/research/autobayes/tracks/craft-entropy-novelty-verdict.md),
  [coherence-metric result](arcanum/research/autobayes/development/refinement-runs/refine-coherence-metric-20260608/RESULT.md),
  [candidate definition revision](arcanum/research/autobayes/development/refinement-runs/refine-coherence-metric-20260608/CRAFT-DEFINITION-REVISION.md),
  and [formal-foundations map](arcanum/development/craft/CRAFT-FORMAL-FOUNDATIONS.md);
  nested Arcanum commits 2a44d30, 340faf7, 5722dde, and 159831c.
- Craft contracts, promotion, and current authority:
  [interface](arcanum/development/craft/CRAFT-INTERFACE.md),
  [interaction contract](arcanum/development/craft/CRAFT-INTERACTION-CONTRACT.md),
  [promotion readiness](arcanum/development/craft/CRAFT-PROMOTION-READINESS.md),
  [canonical README](arcanum/arcana/craft/README.md), and
  [current architecture](arcanum/arcana/craft/ARCHITECTURE.md); nested Arcanum
  commits 157d313, 7d304d6, ed25dd2, 8ce6e0f, 337d197, and 2ab6c82.
- Craft adoption and later pressure:
  [DomainSpec v2 ledger](projects/domainspec-v2/.craft/ledger.yml),
  [storytelling findings](arcanum/development/craft/research/craft-storytelling-essay-research-2026-07-09/findings.md),
  [WaveDB research closeout](ops/development/2026-08-04-wavedb-craft-runtime-research/CLOSEOUT.md),
  and the [provenance-block result](ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/execution/wp0-provenance/RESULT.md).
- Git-topology discipline: root commits ce1bb259 and b08d5085, plus
  [SUBMODULE-DISCIPLINE.md](SUBMODULE-DISCIPLINE.md).
- Selective public wedge: root commits abf64284, b224b138, and 1495bac7.
- Dispatch ownership and merge behavior: root commits 788ec733 and f197c9b2.

### Correction, authority, and v2

- Formal correction:
  [Lean project history](domainspec-lean-formalization/PROJECT-HISTORY.md) and
  its nested Git history.
- Deterministic derivation:
  [L0 round-trip report](development/deterministic-test-derivation-engine/L0-ROUNDTRIP-REPORT.md).
- CyberAlchemy v2:
  [README](cyberAlchemy-v2/README.md),
  [source map](cyberAlchemy-v2/SOURCE-MAP.md),
  [authority model](cyberAlchemy-v2/authority/AUTHORITY-MODEL.md),
  [canonical definitions](cyberAlchemy-v2/authority/definitions/DEFINITIONS.md),
  [definition towers](cyberAlchemy-v2/authority/definitions/DEFINITION-TOWERS.md),
  [schema registry](cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md),
  [drift audit](cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md),
  the cited June–July definition sessions, and root commits 7e776e65,
  91d63252, bdfa6d50, f3effa54, 224331e4, a37dab67, 66c17bf8, 314f4700,
  14be682f, 88a06b14, and 16f1909e.
- Saturn-facing June design:
  [layer map](ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md).
- DomainSpec v2:
  [README](projects/domainspec-v2/README.md),
  [v1 import triage](projects/domainspec-v2/research/2026-06-29-v1-import-triage/findings.md),
  [import manifest](projects/domainspec-v2/IMPORT-MANIFEST.md), root commit
  b0f35d43, and root path history under projects/domainspec-v2.
- Private framework synthesis:
  [concept map](projects/framework-unification/CONCEPT-MAP.md).

### Bounded local witnesses

- [UI Prototyping Studio](projects/ui-prototyping-studio/README.md) and root
  commit 46157a70.
- [Ontology candidate graph receipt](cyberAlchemy-v2/development/ontology-candidate-graph-prototype/planning/work-pack/session-evidence/SWU-OCGP-001/TASK-SESSION-RESULT.md).
- [IDE Extension](projects/ide-extension/README.md).
- [Akashic Records](projects/akashic-records/README.md).
- [Mint](cyberAlchemy-v2/development/mint/README.md) and its
  [runtime boundary](cyberAlchemy-v2/development/mint/runtime/README.md).

## Research receipt

The balanced expansion was produced through the confirmed dispatch
2026-08-07-project-history-balanced-expansion at digest
53543b40e0533a177fa851a240f7df7acabae86474aab08042a83507deb15a62.

Its accepted
[findings](research/2026-08-07-project-history-balanced-expansion/findings.md),
[evidence closure](research/2026-08-07-project-history-balanced-expansion/EVIDENCE-CLOSURE.json),
and [final audit](research/2026-08-07-project-history-balanced-expansion/AUDIT.md)
record the source census, exclusions, claim ceilings, and audit gate used for
the factual revision.

The August 8 voice revision used the approved
[meta-layers.md](business-philosopher/assuntos/meta-representations/meta-layers.md)
exemplar and additional root and nested commit history. The exemplar changed
the storytelling voice only. It provided no historical facts or authority.

The August 8 Craft chapter used Whisper for the narrative construction and
Distill to keep the smallest coherent historical spine: origin, ledger proof,
receipt correction, the AutoBayes challenge, promotion, adoption, and current
boundary. Its research pass inventoried the canonical and historical Craft
trees, read the formative Task Session and Refine results, inspected nested
Arcanum commits, and checked retained repository-scoped Claude transcripts.
The AutoBayes follow-on added its research tower, entropy and novelty audits,
coherence-metric backtest, unapplied definition candidate, and formal-foundation
boundary. Local transcript evidence was used only for the explicitly bounded
adoption observations in the chapter; all load-bearing method and status claims
remain anchored to repository artifacts.
