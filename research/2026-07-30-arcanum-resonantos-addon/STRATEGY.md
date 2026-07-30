# Arcanum as a ResonantOS Add-on — Research Strategy

## Direct strategy

Research the integration as three deliberately separate layers:

1. **Repository installation:** public Arcanum Bootstrap already owns generated
   skills, runtime configuration, observability, optional harness state, and
   deterministic `tools/arcanum` surfaces at the resolved workspace root.
2. **Native product add-on:** ResonantOS must own the add-on manifest, capability
   grant, host adapter, browser projection, persistence, security, update,
   disable, rollback, and release behavior inside `2.0.0-alpha`.
3. **Conversational projection:** Augmentor lets a person discover, inspect,
   edit, decline, approve, follow, clarify, and separately consume Arcanum
   work from the conversation while every execution and state transition
   remains owned by Arcanum and existing ResonantOS runtime owners.

The result will recommend the smallest adapter between those retained owners or
kill or narrow the shape if current evidence cannot support it. It will not
install, sync, implement, deploy, promote, or release anything.

## Expected end state

The intended product outcome is a **ResonantOS-native Arcanum add-on with an
Augmentor conversational front door**, not Arcanum embedded as an independent
product runtime.

When implemented later:

1. Arcanum Bootstrap installs or updates selected public capabilities at the
   workspace or host and retains generated-byte provenance.
2. ResonantOS discovers that installed runtime through a versioned host profile,
   exposes only declared capabilities through its native add-on manifest and
   grants, and executes through its existing loopback host and runtime owners.
3. Explicit commands keep precedence. For an eligible ordinary-language
   request, Augmentor may classify the intent and show a side-effect-free,
   digest-bound `StrategyProposal`.
4. The person may edit, decline, or explicitly approve those exact proposal
   bytes. Preview, edit, and decline do not execute.
5. After approval, owner-backed Arcanum and ResonantOS services execute while
   Augmentor displays their states in the conversation and a compact run tray.
   The parent conversation remains usable, and a clarification is routed only
   to the addressed child.
6. Results and artifacts remain owner-backed and are presented separately.
   Opening, attaching, consuming, or admitting them to memory is another
   explicit user choice.

Augmentor is therefore a proposal and control projection. It is not a second
installer, add-on registry, router, scheduler, execution owner, workspace,
artifact store, session store, approval authority, or memory path.

The research is complete only when it selects, narrows, or kills this topology
from current source evidence and leaves an implementation-ready contract:

- selected initial public Arcanum capability catalog;
- current-versus-target ownership and lifecycle map;
- exact add-on manifest, grants, host adapter, runtime profile, proposal,
  approval, state/event, child-interaction, run-tray, artifact, and
  result-consumption contracts;
- the ordinary-language-to-consumption interaction sequence;
- ordered implementation slices, owner decisions, gaps, and kill criteria;
- deterministic checks and a reproducible two-child browser fixture using
  Subagent Strategy and Whisper precedent where current contracts support it,
  or a cited narrower witness if they do not.

## P1 trigger decision

This is a governed research dispatch. All four Principle-1 triggers hold:

- **Synthesis:** the canonical Arcanum installer, the already-installed
  workspace runtime, the nested ResonantOS add-on product, and security and
  validation obligations must be reconciled.
- **Context protection:** the source and generated runtime footprint, add-on
  SDK, browser bridge, ADR, test, version, and branch evidence is larger than
  the parent should carry.
- **Isolation:** installer ownership, product architecture, and operational
  safety need independent source reads and adversarial checks.
- **Parallelism:** the three explorer lanes are independent until synthesis.

The live dispatch type is `research`; the sheet uses schema `0.8.0`.

## Lanes, groups, and subagents

### Explorers — parallel

- `Hewitt, Carl` — **Arcanum installation lane**. Establishes what Bootstrap
  owns, what is already installed at `../workspace-resonant`, which surfaces
  are generated versus consumer-owned, and how update, provenance, runtime
  selection, observability, and drift work.
- `Simon, Herbert` — **ResonantOS product lane**. Traces the current
  `2.0.0-alpha` add-on SDK, manifests, capability review, registry, bridge,
  provider/delegation owners, Augmentor routing and conversation surfaces,
  module boundaries, browser surfaces, tests, and cached `origin/dev` delta.
- `Turing, Alan` — **security and executable-witness lane**. Attacks packaging,
  secrets, grants, Augmentor proposal and approval semantics, enable/disable,
  update, rollback, degraded modes, release gates, and the smallest
  proposal-to-two-child-to-consumption local fixture.

The explorer anti-bias axis is a composite of methodology and source corpus:
installer/runtime archaeology, empirical product tracing, and adversarial
operational validation. The exact sheet carries all three pairwise predicted
disagreements.

### Synthesis and adversarial review

- `Shannon, Claude` synthesizes one exact-binding current-state, options, and
  selected integration contract.
- Three reviewers run in parallel:
  - `Lakatos, Imre` attacks precedent and duplicated ownership.
  - `Gödel, Kurt` attacks non-vacuity and executable integration.
  - `Quine, Willard Van Orman` attacks definitional, public/private, secret,
    and execution-authority collapse.
- `van Lamsweerde, Axel` writes only `findings.md`, after evidence closure.
- `Brandenburg, Martin` audits the final findings; the parent remains the final
  approver.

## Dependency flow

```text
explorers
  -> synthesizer
  <-> reviewers
  -> exact-binding evidence closure
  -> writer
  -> auditor
  -> parent
```

- One bounded feedback edge lets the synthesizer request missing exact source
  evidence from explorers.
- The synthesizer/reviewer zig-zag has a loop cap of two.
- One bounded auditor-to-writer edge permits a final repair.
- Every spawned agent must be joined and closed.
- The strategist mechanically appends verbatim explorer returns to
  `research.md`; the writer never authors or rewrites that source record.
- No edge permits source-repository mutation.

## Inventory preflight

The owner machine index passed lookup readiness with zero failures and 115
inherited uncontrolled-tag warnings. Target lookup is degraded:

- the requested `../workspace-resonantos` path does not exist;
- the live sibling is `../workspace-resonant`;
- that workspace has no root machine Inventory;
- the only nested human-only Inventory belongs to the separate
  `agentsofthefree` project and is excluded.

Selected owner evidence:

- the verified Augmentor Subagent Strategy integration result, because it
  proves the retained-owner, adapter, degraded-mode, and browser-witness
  boundaries;
- the candidate ResonantOS Living Archive seam and owned-base synthesis,
  because it distinguishes runnable Bootstrap material from a missing
  host-owned provider body;
- its selector-level evidence cards for add-on capabilities, host-resident
  execution, runnable installers, and the public/private boundary.

Excluded:

- the broader unified-agent result, because memory, ontology, reasoning, and
  authority evolution would expand this add-on question;
- the retrieval-focused ResonantOS synthesis;
- the superseded unexecuted subagent strategy;
- the nested `agentsofthefree` Inventory;
- operational dispatch terms with no direct machine-index match, because live
  route owners and validators are stronger than a discovery read model.

The concrete Inventory consequences are the three-lane split, exact-binding
evidence, explicit workspace-root versus product-root separation, and reject
conditions against second installers, registries, schedulers, provider fabrics,
grant or approval owners, state stores, secret stores, and release owners.
Inventory remains discovery, not research proof or dispatch authority.

## Exact-binding research obligations

The findings must answer:

1. What Arcanum is already installed at the resolved workspace root, and is it
   current, selected, drifted, or intentionally separate from the product?
2. Which files and lifecycle stages remain owned by Arcanum Bootstrap?
3. Which exact ResonantOS manifest, capability, registry, bridge, provider,
   delegation, persistence, artifact, session, memory, browser, security, and
   release owners would carry a native Arcanum add-on?
4. Does current evidence support the intended three-layer topology: Bootstrap
   installation, ResonantOS-native add-on, and Augmentor conversational
   projection? If not, which exact part must be narrowed or killed?
5. Which initial public Arcanum capabilities should the add-on expose, what is
   the exact manifest and grant contract, and what stays in host-only runtime
   configuration?
6. How do install, update, validation, enable, disable, reload, rollback, and
   uninstall remain distinct and owner-backed?
7. What happens when Arcanum is absent, stale, partially installed, missing a
   selected capability, blocked by grants, unavailable at the host, or unable
   to run in parallel?
8. What exact sequence turns an eligible ordinary-language request into a
   side-effect-free digest-bound proposal, edit/decline/approval decision,
   owner-backed execution, targeted child clarification, parent-chat
   continuity, and a separate result-consumption choice?
9. What literal two-child local fixture and browser test proves that sequence
   with Subagent Strategy and Whisper where supported, without secrets,
   private authority, nested model-backed CLI, execution-by-preview, automatic
   artifact or memory intake, or duplicated product state?
10. Which cached `origin/dev` changes affect the answer, and what must be
   refreshed before any implementation?
11. What exact ordered slices, tests, issue and owner decisions would be needed
    later, without treating research as implementation authorization?

## Gate and ledger state

- Confirmation readiness: `PASS`
- Live schema: `0.8.0`
- Prior sheet SHA-256, now retired:
  `974e2dbd902f8fd1013a574892e8e19a856f05025b4bffb9c1a3919cda025bc2`
- Revised sheet SHA-256:
  `5f04fec36cd2962dbeea7138807d9c485177e69e5f3e4960ec32a3a7de313ac6`
- Ledger mutation during readiness validation: `none`
- Dispatch Spec: `PASS`
- Tension checker:
  `ct1-checker-5f04fec3-b91d7a2e = PASS`
- Tension reviewer:
  `reviewer-5f04fec3-a7c19e42 = PASS`
- Prior digest and tension receipts remain retired.
- Human confirmation:
  `chat-confirmed-20260730-5f04fec3 = CONFIRMED`
- Registration: exactly one dispatch row appended
- Execution: resolved after 13 role invocations and one bounded
  synthesizer-reviewer repair loop
- Reviewer closure: round two returned `PASS + PASS + PASS`
- Evidence closure: `ready`
- Writer: `findings.md` produced with a passing receipt
- Auditor: `RECOMMEND_ACCEPT`
- Parent approval: `PASS`
- Native orchestration evidence: 119 causal events, zero validation errors
- Ledger close: exactly one paired close row appended with
  `exit_reason: resolved`
- Product and public/private mutation boundary: preserved; the nested product
  checkout remained clean and no Arcanum install, sync, promotion, deployment,
  or release action occurred
- Close-row tooling residue: its optional `invoked_by` field was supplied as
  `victorboscaro@gmail.com`, while the registered dispatch row records
  `rondelli.vladimir@gmail.com`; the append-only ledger cannot be rewritten,
  and dispatch authority remains the digest-bound chat confirmation above

## Expected artifacts

If confirmed and run:

- `research.md` — verbatim explorer returns, mechanically assembled by the
  strategist;
- `findings.md` — exact-binding, auditor-checked integration contract;
- synthesis, reviewer, evidence-closure, writer, and audit receipts;
- paired append-only dispatch lifecycle evidence.

No target product code, public Arcanum package, private DomainSpec or Saturn
artifact, installation state, deployment, promotion, or release may be changed
by this research dispatch.

## Next owner action

Confirm `../workspace-resonant` as the corrected implementation target, refresh
the nested product checkout, and re-resolve every cited selector before
selecting an implementation plan. Research acceptance does not authorize that
refresh, Bootstrap mutation, product code, add-on installation, grants,
promotion, deployment, or release.
