# Arcanum Building System — Evidence-Bound Synthesis

Normalized from the native `Turing, Alan` return for `spawn-0004`. The native
return handle remains `native-agent-return:/root/synthesizer_spawn_0004`.
Parent repository identity is `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`;
Arcanum identity is `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295` with material
live-uncommitted changes. `OBSERVED`, `EXECUTED`, and `UNVERIFIED` retain the
meanings declared in `research.md`; generated provenance never implies parity.

## Plain-Language System Model

- `SYS-001`: Invoke authors the agreement—Define fixes intent, Design proves
  design evidence, and Plan authors layering, the Work Pack, SWUs, validation,
  execution, and closeout contracts. It does not execute product changes.
  Evidence: explorer-contract §§2,4; `arcanum/spells/invoke/define.md:45-68`,
  `design.md:104-182`, `plan.md:333-397`; mixed clean/live-uncommitted,
  `OBSERVED`.
- `SYS-002`: WPRA freezes/audits that agreement and Implementation Readiness
  coordinates a finite frontier. Plan-once WPRA retains `selected_unit:null`,
  `mutation_ready:false`, and `authority_effect:none`; neither readiness owner
  performs owner work. Evidence: explorer-contract §§2-3 and explorer-runtime
  timeline 1-3; current READMEs/scripts; live-uncommitted, partly `EXECUTED`.
- `SYS-003`: Task Session executes exactly one admitted SWU. It proves entry,
  context, preflight, mutation admission, bounded outputs, critical validation,
  terminal receipt, and separate closeout synchronization. It cannot impersonate
  a material producer, prerequisite owner, Refresh, or lifecycle owner.
  Evidence: explorer-contract §§2-5; `task-session/SKILL.md:148-420`;
  live-uncommitted, core paths `EXECUTED`, real-owner closeout `UNVERIFIED`.
- `SYS-004`: Continuation Router performs and joins one exact owner hop; it does
  not do owner work. Broad dependent graphs route to Goal; explicit SWU series
  route to Task Session Until Blocker. Evidence: explorer-closure dependency
  graph; `continuation-router/SKILL.md:45-54,98-171`; `OBSERVED`.
- `SYS-005`: Craft owns recursive local project state—contexts, blockers,
  decisions, gaps, receipts, children, and recomposition. It cannot select an
  SWU, admit mutation, establish native success, or promote a capability.
  Evidence: explorer-closure Craft section; `craft/SKILL.md:14-31,56-72,
  193-203,241-268,312-317,360-377`; `OBSERVED`.
- `SYS-006`: Synchronization is part of Task Session completion. Passing product
  execution plus failed/unjoined Refresh closeout preserves execution evidence
  but leaves the Task Session blocked. Evidence: explorer-contract §6G;
  `task-session/SKILL.md:351-420`; `OBSERVED`, end-to-end `UNVERIFIED`.

## Lifecycle Graph

```text
intent
  -> Invoke Define
  -> Invoke Design -> denominator + fixed-point validation
  -> Invoke Plan -> Implementation Layering -> Distill -> Work Pack/SWUs
  -> WPRA -> semantic manifest -> exact selected-unit receipt
  -> Implementation Readiness finite frontier
       -> fast-entry: task-ready | exact owner prerequisite | block
       -> fresh Task Session for one SWU
          -> Context Builder -> Decision Gate if needed
          -> closeout preflight -> mutation admission/consumption
          -> bounded mutation + critical validation -> terminal receipt
          -> distinct owner/Refresh closeout join
       -> next fresh session | FRONTIER_COMPLETE | real blocker

Craft records scoped state around the graph; it replaces no gate.
Dispatch Spec validates delegated routes; Orchestrate schedules/joins/closes.
Sigil Development or Spellcraft owns reusable capability lifecycle,
informed by Experiment Harness -> Signal Observer -> Workflow Reflect.
```

## Owner and Integration Matrix

| ID | Owner | Owned artifact/state | Ceiling and legal boundary |
|---|---|---|---|
| `OWN-001` | Invoke Define | spec, glossary, scope transport | definition completeness only; explorer-contract §2, `define.md:45-68` |
| `OWN-002` | Invoke Design | six views, denominator, selection result | design-validator pass, never Plan/execution proof; `design.md:104-182` |
| `OWN-003` | Invoke Plan | layering, Work Pack, SWUs, validation/closeout | mutation-handoff eligibility, not selection/admission/execution; `plan.md:333-397` |
| `OWN-004` | Distill | coherence/recomposition verdict | `pass|flag|block`, no mutation authority; `distill/SKILL.md:99-137,203-285` |
| `OWN-005` | WPRA | frozen audit, semantic manifest, selection receipt | readiness/current selection with `authority_effect:none`; WPRA README `198-342` |
| `OWN-006` | Implementation Readiness | frontier policy/entry/binding and joins | finite coordination, never inferred owner/SWU completion; README `52-130` |
| `OWN-007` | Context Builder | exact bounded context pack | coverage, not source truth or readiness; `context-builder/SKILL.md:27-86` |
| `OWN-008` | Decision Gate / typed owner | decision or one-use override | resolves one choice, cannot bypass lifecycle owner; `decision-gate/SKILL.md:52-206` |
| `OWN-009` | Task Session | one-SWU execution/validation/terminal/closeout state | one bounded unit; distinct producer and owner receipts; `task-session/SKILL.md:148-420` |
| `OWN-010` | Continuation Router | one owner-hop route/join receipt | route proof, never owner mutation; `continuation-router/SKILL.md:98-171` |
| `OWN-011` | Invoke Refresh | proposal/applied synchronization and material receipt | exact approval/binding; phase pass is not apply authority; `refresh.md:185-255,317-325` |
| `OWN-012` | Craft | `.craft/ledger.yml` scoped state | local state only; views derived; `craft/SKILL.md:56-72,312-317` |
| `OWN-013` | Dispatch Spec + Orchestrate | valid route and native receipts | delegated-work evidence, not semantic/lifecycle promotion; current SKILL contracts |
| `OWN-014` | Sigil Development / Spellcraft | reusable capability contract/lifecycle | experiment/observer/reflection informs but cannot promote |

## Gate Matrix

| ID | Gate | First stop and forbidden effect | Evidence/proof |
|---|---|---|---|
| `GATE-001` | Design activation/denominator/fixed point | missing/stale/self-issued evidence stops Plan | explorer-contract §3; `design.md:22-31,104-173`; `OBSERVED` |
| `GATE-002` | Plan admission | missing Design/layering/validation or Distill block stops mutation handoff | `plan.md:333-397`; live-uncommitted, `OBSERVED` |
| `GATE-003` | SWU uniqueness | unknown/duplicate/ambiguous/task-shaped unit stops guessed execution | `plan.md:344-370`, `task-session/SKILL.md:113-141` |
| `GATE-004` | Semantic manifest | bad pointers/routes/digests/overlapping decisions stop selection | `plan_semantics.py:25-280`; canonical `EXECUTED`, generated weaker/stale |
| `GATE-005` | Plan-once selection | semantic drift/non-unique membership stops entry/admission/mutation | `verify_plan_selection.py:141-251`; `EXECUTED` |
| `GATE-006` | Fast entry | stale binding/frontier/entry stops before Context Builder and effects | `fast_execution_entry_guard.py:63-207`; `EXECUTED` |
| `GATE-007` | Owner prerequisite | unauthorized/stale/repeated/non-pass owner tuple stops fresh session | Work-Pack route + `fresh_session_resume.py:420-592`; `EXECUTED` |
| `GATE-008` | Closeout preflight | stale/missing owner contracts/baselines/successor stop before product write | `task-session/SKILL.md:229-240`; E2E `UNVERIFIED` |
| `GATE-009` | Mutation admission | producer/package/target/write/digest/replay fault stops mutation | `verify-mutation-readiness.py:347-470`; `EXECUTED` |
| `GATE-010` | Completion | failed/unrun critical validation or missing output blocks terminal completion | `task-session/SKILL.md:321-350`; `OBSERVED` |
| `GATE-011` | Closeout join | owner failure/drift/cycle/ambiguity/missing join blocks synchronization | `task-session/SKILL.md:351-420`; real-owner E2E `UNVERIFIED` |
| `GATE-012` | Native wave join | missing/mismatched/timed-out receipt withholds dependent wave | `validate_run_evidence.py:128-258`; validator tests `EXECUTED` |

## Artifact and Receipt Lineage

- `LIN-001`: Define transport → Design scope/denominator/selection →
  Plan/layering/Work Pack/SWUs. Later authoring never erases prerequisite proof.
- `LIN-002`: frozen plan → semantic manifest → selection handoff → selected-unit
  receipt. Audit is not selection; selection is not mutation admission.
- `LIN-003`: selected unit + policy + binding + entry projection → fast-entry
  receipt. Consumer entry remains distinct from semantic selection.
- `LIN-004`: material package + producer receipt + schema + baselines → mutation
  admission → single-use ledger → execution ticket. Task Session consumes and
  binds; it does not copy the producer validator.
- `LIN-005`: execution ticket → bounded outputs and critical validation →
  terminal Task Session receipt. This proves one unit, not synchronization.
- `LIN-006`: terminal receipt + deltas/baselines → `CloseoutSync` → separate
  owner/Refresh receipt → continuity cursor.
- `LIN-007`: native action → attempt → spawn result → wait registration/attempt →
  terminal/close → normalized receipt → gate decision. Host evidence cannot
  establish semantic correctness or promotion.
- `LIN-008`: native result → optional Craft ledger reference → derived Craft
  views. Recording never transfers owner authority.

## Recent Change Chronology

1. `CHG-001`: July 30 immutable foundation at Arcanum `07b01c9`: commits
   `7ed9c113`, `8133179`, `952fa42`, `10d2e19`, `b0090ee`, `d2a7d0c`, and
   `07b01c9` establish deterministic governance, chain, audit, join,
   reconciliation, resume, and owner-hook behavior. `COMMITTED/OBSERVED`.
2. `CHG-002`: August 4–5 live changes add semantic manifest/selection,
   fast-entry, mutation-admission consumption, Work-Pack prerequisite routing,
   fresh-session resume, finite outer loop, and closeout/native-join contracts.
   `LIVE-UNCOMMITTED/OBSERVED`; scoped canonical suites `EXECUTED`.
3. `CHG-003`: generated WPRA is stale. Canonical/generated hashes differ for
   `plan_semantics.py`, `verify_plan_selection.py`, and `audit_work_pack.py`;
   generated semantics omit execution policy, allowed-route digest, and
   selection-intent binding. `GENERATED/OBSERVED`, parity `BLOCK`.
4. `CHG-004`: generated Task Session and Continuation Router docs also differ;
   package-wide parity remains `UNVERIFIED`.
5. `CHG-005`: canonical-live scoped suites passed: selection 6/6, plan-once
   E2E 1/1, fast guard, admission 3/3, governance 7/7, fresh resume 5/5,
   Work-Pack integration 14/14, native join 6/6, partial-wave recovery 3/3.
   This is not generated parity, product mutation, promotion, or production.
6. `CHG-006`: eight development SWU receipts and prototype closeout artifacts
   remain candidate evidence only.

## Exact Traces

- `TRACE-NORMAL-001`: Plan authors complete Work Pack → WPRA emits no-authority
  manifest → selection recomputes exact epoch/unit → Implementation Readiness
  emits policy/binding/entry → fast guard returns `task-ready` → Context Builder
  → closeout preflight → mutation admission revalidates producer/package,
  validation, writes, and baselines → single-use consumption → one fresh Task
  Session → terminal receipt → distinct owner/Refresh closeout → next fresh
  session or `FRONTIER_COMPLETE`. Core fixture/integration path `EXECUTED`; real
  owner closeout `UNVERIFIED`.
- `TRACE-FAIL-001`: change semantic value after manifest → selection detects
  `PLAN_EPOCH_STALE`/component change → Refresh/re-audit; no selection,
  Context Builder, admission, or mutation. `EXECUTED`.
- `TRACE-FAIL-002`: prerequisite owner receipt is non-pass, unchanged, or
  replayed → `OWNER_PREREQUISITE_BLOCKED`, `UNCHANGED_PREREQUISITE_FINGERPRINT`,
  or replay diagnostic; no fresh admission/session. `EXECUTED`.
- `TRACE-FAIL-003`: target bytes change or admission/package is reused → live
  rehash/identity check stops before governance writes. `EXECUTED`.
- `TRACE-FAIL-004`: product execution passes but closeout owner fails/drifts or
  is absent → preserve terminal receipt, block synchronized completion.
  `OBSERVED`; product-owner E2E `UNVERIFIED`.
- `TRACE-FAIL-005`: native action → spawn → wait registration/attempt → timeout
  → one interrupt → timed-out receipt → dependent gate closed. Validator suites
  `EXECUTED`; actual host timeout this run `UNVERIFIED`.

## Confusion and Bug Map

| ID | Defect/confusion | First owner/gate and correction |
|---|---|---|
| `BUG-001` | WPRA pass mistaken for mutation-ready | WPRA output must retain null selection/false mutation/no authority |
| `BUG-002` | Selection and fast-entry seem duplicate | preserve semantic-selection and consumer-entry bindings separately |
| `BUG-003` | Producer and consumer validation collapse | producer validates; Task Session binds/consumes without copying |
| `BUG-004` | Closeout checks seem triplicate | preserve Plan authoring, pre-mutation currentness, post-run sync |
| `BUG-005` | Distill `flag` lacks mechanical non-criticality proof | Plan handoff must bind criticality before mutation-capable route |
| `BUG-006` | Implementation Readiness treated as multi-unit executor | outer loop coordinates distinct one-SWU receipts |
| `BUG-007` | Refresh phase pass treated as apply authority | require inventory, approval, exact package/receipt, ready handoff |
| `BUG-008` | Generated runtime treated as canonical-live parity | block and regenerate/validate exact generated package |
| `BUG-009` | Canonical README contracts vs generated SKILL packages | bind canonical identity and derivation explicitly |
| `BUG-010` | Craft/Inventory treated as proof or authority | direct source and owner receipts remain decisive |
| `BUG-011` | Passing execution reported complete after closeout failure | preserve execution, return blocked synchronization |
| `BUG-012` | Native reducer consumed unrelated shared-directory JSON | filter by required action IDs or provide an exact action-only directory |
| `BUG-013` | Reducer failure blamed on explorers | `driver-correction.json` proves no retry/respawn and valid action receipts |
| `BUG-014` | Goal treated load-bearing without canonical package binding | bind the current Goal owner source first |

## Craft Role and Non-Role

- `CRAFT-001`: Craft can wrap the workflow for persistent state and residue;
  `.craft/ledger.yml` is authoritative only for that local scope and its views
  are derived.
- `CRAFT-002`: Craft is not a mandatory Invoke → WPRA → Task Session stage and
  cannot select, admit, execute, synchronize, or promote.
- `CRAFT-003`: deferred exchange/render/update schemas in
  `craft/templates/ledger.schema.yml:24-47` prevent claims of a complete
  automated Craft loop.

## Minimal Capability Closure

- `CAP-001`: Invoke + Implementation Layering—core for authoring.
- `CAP-002`: WPRA + Implementation Readiness—core readiness/frontier owners.
- `CAP-003`: Task Session + Context Builder + validation owner—core one-SWU path.
- `CAP-004`: Continuation Router—conditional typed owner prerequisite/closeout.
- `CAP-005`: Decision Gate—conditional consequential choice.
- `CAP-006`: Distill—required where Plan demands recomposition; retain flag gap.
- `CAP-007`: Task Session Until Blocker—only explicit ordered series.
- `CAP-008`: Goal—only broad dependent Craft graph after canonical binding.
- `CAP-009`: Dispatch Spec + Subagent Strategy + Orchestrate—delegated work only.
- `CAP-010`: Sigil Development/Spellcraft + Experiment Harness + Signal
  Observer + Workflow Reflect—reusable capability maintenance closure.
- `CAP-011`: Craft—optional recursive-state owner, never readiness/promotion.
- `CAP-012`: Inventory—optional discovery read model, never proof gate.
- `CAP-013`: Observability Setup—setup convenience when the package is absent;
  direct current package not independently validated here.

## Operating Playbooks

- `PLAY-001` ordinary feature: Define → validated Design → Plan/layering/Distill
  → WPRA/readiness → selected SWU → Task Session context/preflight/admission →
  mutation/critical validation → terminal receipt → owner/Refresh closeout →
  optional Craft recording.
- `PLAY-002` new sigil: Sigil Development → admitted Task Sessions → Experiment
  Harness → Signal Observer → Workflow Reflect → lifecycle-owner decision.
- `PLAY-003` new spell: Spellcraft → Dispatch Spec/Orchestrate only if multi-role
  → experiment/observer/reflection → Spellcraft owner decision.
- `PLAY-004` selected SWU/series: one selected unit follows fast-entry through
  closeout; explicit series uses Task Session Until Blocker and distinct fresh
  sessions/receipts, stopping at the first real blocker.

## Reviewer Attack Ledger

- `ATTACK-001`: generated WPRA parity is blocked.
- `ATTACK-002`: generated Task Session/Continuation Router parity is unproved.
- `ATTACK-003`: August 4–5 closure is live-uncommitted.
- `ATTACK-004`: no real product-through-owner-closeout E2E witness.
- `ATTACK-005`: Distill flag criticality binding is missing.
- `ATTACK-006`: Invoke producer/Task Session consumer compatibility not tested.
- `ATTACK-007`: Goal canonical source binding is missing.
- `ATTACK-008`: canonical README/generated SKILL source identity is ambiguous.
- `ATTACK-009`: deferred Craft schemas forbid automated-loop claims.
- `ATTACK-010`: timeout tests are event-contract evidence, not host timeout proof.
- `ATTACK-011`: reducer shared-directory scope bug remains; the corrected
  action-only reduction passed without retry or respawn.
- `ATTACK-012`: explorer-runtime verbatim receipt omitted `-route`, while the
  normalized parent receipt carries the correct orchestration dispatch ID.
- `ATTACK-013`: only runtime-explorer rows backed by tests may be `EXECUTED`;
  contract and closure rows remain `OBSERVED`.
- `ATTACK-014`: development receipts/fixtures are not promotion or production.
