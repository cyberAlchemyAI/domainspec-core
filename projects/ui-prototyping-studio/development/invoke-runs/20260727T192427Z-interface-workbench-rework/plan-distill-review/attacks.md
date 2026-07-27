# Plan Distill Attack Record

Dispatch:
`2026-07-27-ui-prototyping-studio-plan-distill-review`

This record preserves both attack roles' initial and final robot-talk
positions and the verifier return. Inventory references used by the agents
were discovery-only. No return selected or executed an SWU.

## Abramsky Initial Position

Verdict: **FLAG**.

No affirmative BLOCK finding. The 17-unit chain is semantically coherent,
`SWU-UPW-001` is a sound reversible first candidate, and recomposition is
explicit. One validation-transport gap prevents an unqualified PASS.

- PASS — semantic decomposition: each SWU has one operator-observable
  responsibility, dependency, bounded source/write surface, acceptance
  boundary, and successor.
- PASS — closeout coherence: every SWU has a declared execution receipt,
  synchronized planning targets, owner validation, and deterministic
  successor without auto-selection.
- FLAG — PD-VAL-01: SWU-UPW-008–013 have meaningful independent acceptance,
  but not an exact runnable per-SWU command or selector. Their task says each
  runs its "named focused Playwright slice," yet no such slice is named; only
  a task-closeout two-spec command is concrete.
- Repair proposed: bind each of 008–013 to an exact spec path and grep/test
  selector.
- BLOCK: none in affirmative closure/recomposition scope.

Initial per-SWU dispositions:

| SWU | Disposition |
| --- | --- |
| 001–007 | PASS |
| 008–013 | FLAG PD-VAL-01 |
| 014–017 | PASS |

First-unit verdict: SWU-UPW-001 PASS as recommended candidate, not selected.
It has no dependency, writes only a versioner and its test, proves digest
identity without changing `/state` or rendering, and keeps serializer and
hasher together because neither alone proves the behavior.

Initial recomposition proof:

`001 digest → 002 coherent read → 003 versioned transport → 004 inert shell →
005 action freshness → 006 atomic commit → 007 context continuity → 008–013
six regions → 014 responsive order → 015 copy → 016 interaction semantics →
017 content boundary → W5 full closure`.

Expected stable disagreements: splitting serializer from hasher in 001,
integration from HTTP exposure in 003, shell mount from inertness in 004, and
subdividing 016. Abramsky's initial position retained each cluster where one
externally meaningful acceptance invariant closed it.

## Rittel Initial Position

Verdict: **BLOCK** pending structural repairs.

1. Ambiguous mutation scopes: SWUs 004–017 use phrases such as "same
   shell/coordinator," "shell/projection," and "labels/copy," despite requiring
   baseline hashes and controlled overlapping writes. Repair proposed:
   exhaustive repo-relative path inventory, explicit create-if-absent markers,
   and forbidden paths.
2. Non-runnable/forward-dependent algorithms: 002 does not identify the
   authoritative epoch/token or retry constant; 003 promises invalid-route
   rejection while route validation is deferred to 017; 006 rolls back a
   context plan whose concrete bindings arrive only in 007. Repair proposed:
   name token/bound, place route validation before endpoint admission, and
   establish the context-plan contract before rollback integration.
3. Task-shaped bundling/duplicate ownership: 010 combines annotation, batch,
   and revision modes; 016 combines keyboard, focus, live regions, contrast,
   target size, and color; 017 combines server allowlisting and iframe
   sandboxing. Live-scope behavior is also claimed by 010/012/016. Repair:
   split by independently falsifiable boundary and give each UPW-FIX
   obligation one mutation owner.
4. Incomplete closeout: each row omits the promised
   `refresh-receipts/<SWU-ID>.json`, `EXECUTION-PACK.md`, and
   `PLAN-TRANSPORT.md`; W5's closure report has no exact path, schema, or
   synchronization inventory.
5. Coverage/dependency inflation: traceability does not give 008, 009, or 013
   an exact independent witness; the manifest turns serial write-conflict
   ordering into semantic dependencies. Repair: inverse
   SWU→Design→UPW acceptance matrix and distinct semantic/serialization
   treatment.

Initial per-SWU dispositions:

| SWU | Disposition |
| --- | --- |
| 001 | KEEP; declare absent paths as intentional creations |
| 002 | BLOCK; epoch/token and retry bound |
| 003 | SPLIT; projection/compatibility then HTTP exposure |
| 004–005 | KEEP; exact paths |
| 006 | BLOCK; context contract before transaction |
| 007–009 | KEEP |
| 010–012 | SPLIT |
| 013–015 | KEEP |
| 016–017 | SPLIT |

First-unit verdict: SWU-UPW-001 narrowness was not falsified. It remained only
a recommended candidate, not selection. Authority check passed:
`selected_swu` was null, witnesses were unexecuted, and Plan/Task Session gates
remained blocked.

## Abramsky Final Robot-Talk Position

Verdict: **BLOCK** pending structural repair. The initial PD-VAL-01 flag was
too narrow. The architecture still recomposes conceptually; the literal graph
does not prove safe execution.

1. Mutation scopes — CONCEDE. Replace shorthand scopes with exhaustive
   repo-relative paths; mark existing/create-if-absent; add forbidden paths;
   omitted paths are unauthorized; separate serial overlap from semantic
   dependency.
2. Forward dependencies — CONCEDE. For 002, name token owner, equality
   semantics, retry count, and terminal error. For 003/017, split route
   admission from sandbox and place admission before 003. For 006/007,
   establish the typed context-plan interface and bindings before
   transactional application.
3. Task shape — MIXED. REFUTE splits for 010, 011, and 012 because each closes
   one contextual-inspector, staged-review, or handler-plus-receipt behavior.
   CONCEDE duplicate assertion ownership, split 016 at interaction/live versus
   visual/target calibration, and split 017 at server admission versus iframe
   sandbox.
4. Closeout — CONCEDE. Every row must enumerate source targets, execution and
   refresh receipts, work-pack, manifest, task, wave, execution-pack, and
   transport targets; include schemas, baseline rules, permitted fields, and
   successor effect. W5 needs an exact report path/schema/synchronization
   inventory.
5. Coverage/dependency inflation — CONCEDE. Retain and expand PD-VAL-01:
   008–013 need selectors; 008/009/013 need direct witnesses; add inverse
   coverage and distinguish semantic prerequisites from serialization.

Final per-SWU dispositions:

| SWU | Disposition |
| --- | --- |
| 001 | PASS/KEEP after create/forbidden scope markers |
| 002 | BLOCK |
| 003 | BLOCK/dependency repair |
| 004–005 | PASS after exact path inventory |
| 006 | BLOCK |
| 007 | PASS subject to reordered context-plan ownership |
| 008–009 | FLAG |
| 010–012 | KEEP with assertion ownership and exact selectors |
| 013 | FLAG |
| 014–015 | PASS after exact path inventory |
| 016 | BLOCK/SPLIT |
| 017 | BLOCK/SPLIT and reorder |

SWU-UPW-001 remains the narrowest reversible recommended candidate;
`selected_swu` remains null. Recomposition is architecturally affirmative but
executably blocked.

## Rittel Final Robot-Talk Position

Verdict: **BLOCK**, repairable without losing the Design recomposition spine.

1. Semantic decomposition PASS — REFUTE for the current literal Plan, then
   STABILIZE most units with bounded exact-scope, token, route, and context
   repairs.
2. Closeout coherence PASS — REFUTE. Refresh receipt target inventories and
   the W5 closure-report contract are incomplete.
3. PD-VAL-01 — CONCEDE. Bind 008–013 to exact spec, selector/grep, positive
   assertion, negative mutant, and expected receipt field.
4. Per-SWU closure — REFUTE initial broad PASS. Withdraw earlier splits for
   003 and 010–012 after bounded repairs. Keep 002 and 006 blocked pending
   contracts; retain splits for 016 and 017.
5. First-unit PASS — CONCEDE. SWU-UPW-001 remains the narrowest reversible
   trust-building candidate and is not selected.
6. Recomposition PASS — STABILIZE WITH EXACT REPAIR. The spine survives after
   repairing 002/003/006, splitting 016/017, regenerating manifest/waves and
   closeout rows, and adding 008–013 selectors.

Final per-SWU dispositions:

| SWU | Disposition |
| --- | --- |
| 001 | KEEP |
| 002 | BLOCK until epoch/retry repair |
| 003 | KEEP after route-validity repair |
| 004–005 | KEEP |
| 006 | BLOCK until opaque-context repair |
| 007 | KEEP |
| 008–013 | KEEP after exact selectors |
| 014–015 | KEEP |
| 016–017 | SPLIT |

Authority remains intact: `selected_swu` is null, all units are not-started,
witnesses are unexecuted, and Task Session admission remains blocked.

## Schön Verifier Return

Verifier verdict: **BLOCK survives, but not PASS/no-objection.** Nine MAJOR
findings survive. PD-09 was severity-inflated and prescribed a mechanism not
required by Plan law. One bounded Noether revision was required.

| Finding | Verifier disposition |
| --- | --- |
| PD-01 | SUSTAIN, MAJOR: prose scopes conflict with exact hashed target inventories. |
| PD-02 | SUSTAIN, MAJOR: no authoritative store token or serialized-read primitive, equality rule, numeric retry, or exhaustion type. |
| PD-03 | SUSTAIN, MAJOR: invalid-route failure precedes route admission. KEEP 003 remains compatible with either accepted repair. |
| PD-04 | SUSTAIN, MAJOR: 006 consumes context planning before 007 defines it. |
| PD-05 | SUSTAIN, MAJOR: 016 contains independently passing boundaries. |
| PD-06 | SUSTAIN, MAJOR: route admission and iframe sandbox have separate mutation sites and witnesses. |
| PD-07 | SUSTAIN, MAJOR: 008–013 lack exact commands, polarity, and receipt binding. |
| PD-08 | SUSTAIN, MAJOR with correction: one primary acceptance owner per assertion; shared witness files are lawful. |
| PD-09 | REFUTE as framed: underlying ambiguity is real, but current serial order is safe. Reduce to MINOR and do not mandate field names. |
| PD-10 | SUSTAIN, MAJOR: refresh receipts and exact W5 closure contract are missing. |

Denominator checks passed: 17 unique mutation SWUs; five mutation tasks/waves
plus exempt VERIFY/W5; six tasks and waves; `selected_swu` null. SWU-UPW-001
remains the narrowest reversible recommendation. Recomposition architecture
survives all six Design views and UPW-FIX-001–024, but executable closure is
blocked. All witnesses remain unexecuted, L3/human/release claims remain
outside, and `authority_effect: none`.

The zig-zag correction was returned to Noether once. No further loop remains.

---

## Verbatim Return: Abramsky Initial

## Abramsky INITIAL — `FLAG`

No affirmative `BLOCK` finding. The 17-unit chain is semantically coherent, `SWU-UPW-001` is a sound reversible first candidate, and recomposition is explicit. One validation-transport gap prevents an unqualified `PASS`.

### Candidate findings

- **PASS — Semantic decomposition:** Each SWU has one operator-observable responsibility, dependency, bounded source/write surface, acceptance boundary, and successor. The manifest supplies the complete serial identity graph (`SWU-MANIFEST.json:8`); task files supply algorithms, edge cases, outputs, and acceptance.
- **PASS — Closeout coherence:** Every SWU has a declared execution receipt, synchronized planning targets, owner validation, and deterministic successor without auto-selection (`WORK-PACK.md:109`, `WORK-PACK.md:128`).
- **FLAG — PD-VAL-01:** SWU-UPW-008–013 have meaningful independent acceptance, but not an exact runnable per-SWU command or selector. Their task says each runs its “named focused Playwright slice,” yet no such slice is named; only a task-closeout two-spec command is concrete (`TASK-UPW-REGIONS.md:14`, `TASK-UPW-REGIONS.md:35`). Repair: bind each of 008–013 to an exact spec path and grep/test selector. This is a transport repair, not evidence that the region responsibilities fail semantic closure.
- **BLOCK:** none in affirmative closure/recomposition scope.

### Per-SWU closure matrix

| SWU | Closed semantic unit and I/O | Acceptance/validation | Dependency, closeout, recomposition | Disposition |
|---|---|---|---|---|
| 001 | Canonical whole/region JSON → stable lowercase SHA-256 or typed rejection | Golden vectors/mutants; exact `tsx` command | none → 002; isolated version module/test | PASS |
| 002 | store epoch + projection inputs → coherent snapshot or recoverable exhaustion | interleaving fixture; exact `tsx` command | 001 → 003 | PASS |
| 003 | accepted snapshot + digests → versioned `/state` with coherent compatibility fields | recomputation/coherence; exact unit+E2E command | 002 → 004 | PASS |
| 004 | versioned state → mounted shell with zero unchanged side effects | navigation/patch counters; exact Playwright grep | 003 → 005 | PASS |
| 005 | action receipt joining older flight → exactly one awaited trailing refresh | deferred-race fixture; exact grep | 004 → 006 | PASS |
| 006 | changed regions/context plan → atomic commit or restored mounts/context/versions | renderer-N failure; exact grep | 005 → 007 | PASS |
| 007 | old/new identities + local state → preserve-valid/reset-stale-with-reason | context matrix; exact grep | 006 → 008 | PASS |
| 008 | lifecycle projection → exact identity/progress/next-action spine | state matrix + governance fixture | 007 → 009 | FLAG PD-VAL-01 |
| 009 | current source identity → stable governed canvas/frame | frame navigation counters | 008 → 010 | FLAG PD-VAL-01 |
| 010 | lifecycle/selection identity → state-specific inspector or exact disabled reason | FIX-003/006/008 | 009 → 011 | FLAG PD-VAL-01 |
| 011 | staged/current evidence → named comparison/diff/ack context | FIX-007 + governance negatives | 010 → 012 | FLAG PD-VAL-01 |
| 012 | governed action intent → existing handler receipt in exact live scope | FIX-004/009/010/014 | 011 → 013 | FLAG PD-VAL-01 |
| 013 | revision lineage → collapsed non-current history preserving expansion | FIX-013 + continuity | 012 → 014 | FLAG PD-VAL-01 |
| 014 | six-region surface at 390×844 → task-first order/no overflow | FIX-013; exact mobile grep | 013 → 015 | PASS |
| 015 | lifecycle state → qualified browser copy + secondary CLI disclosure | FIX-020/governance; exact spec | 014 → 016 | PASS |
| 016 | keyboard/pointer/error interaction → bounded focus/live/color/size/contrast semantics | FIX-008–012/021–022; exact spec | 015 → 017 | PASS |
| 017 | projected routes/frames → admitted sandboxed local content or fail-closed rejection | FIX-023–024/injection negative; exact spec | 016 → W5 eligibility | PASS |

The detailed contracts supporting 001–007 are explicit at `TASK-UPW-PROJECTION.md:12` and `TASK-UPW-COORDINATOR.md:12`; 014–017 at `TASK-UPW-RESPONSIVE-COPY.md:12` and `TASK-UPW-HARDENING.md:11`.

### First-unit verdict

`SWU-UPW-001`: **PASS as recommended candidate, not selected**. It has no dependency, writes only a versioner and its test, proves digest identity without changing `/state` or rendering, and explicitly keeps serializer+hasher together because neither alone proves the behavior (`TASK-UPW-PROJECTION.md:12`). Its effect is reversible and prerequisite-shaped. Selection remains `null` (`SWU-MANIFEST.json:5`).

### Recomposition proof

The chain recomposes without an orphan:

`001 digest → 002 coherent read → 003 versioned transport → 004 inert shell → 005 action freshness → 006 atomic commit → 007 context continuity → 008–013 six regions → 014 responsive order → 015 copy → 016 interaction semantics → 017 content boundary → W5 full closure`.

Wave gates preserve that sequence (`EXECUTION-PACK.md:20`). Traceability covers DDR-01–05, Views 1–6, responsive behavior, bounded accessibility, and security (`traceability.md:3`); W5 then checks all 24 witness mappings, all views/extensions, governance regression, residue, and claim ceilings without mutating source (`TASK-UPW-VERIFY.md:12`).

Expected stable Rittel disagreements: splitting serializer from hasher in 001, integration from HTTP exposure in 003, shell mount from inertness in 004, and subdividing 016. My affirmative position is that each pairing/cluster has one externally meaningful acceptance invariant; the strongest conceded issue is only the missing exact validation bindings for 008–013.

## Verbatim Return: Rittel Initial

INITIAL position — `BLOCK` pending structural repairs. The Plan preserves authority correctly, but several SWUs are task-shaped or not independently runnable, and closeout cannot remain internally consistent.

Objections and one-line repairs:

1. **Ambiguous mutation scopes.** SWUs 004–017 use phrases such as “same shell/coordinator,” “shell/projection,” and “labels/copy,” despite requiring baseline hashes and controlled overlapping writes (`WORK-PACK.md:86`, `TASK-UPW-REGIONS.md:11`).  
   **Repair:** Replace every prose scope with an exhaustive repo-relative path inventory, explicit create-if-absent markers, and forbidden paths.

2. **Non-runnable/forward-dependent algorithms.** SWU-002 never identifies the authoritative epoch/token or bounded retry constant (`TASK-UPW-PROJECTION.md:47`); SWU-003 promises invalid-route rejection although route validation is deferred to 017 (`TASK-UPW-PROJECTION.md:82`, `TASK-UPW-HARDENING.md:38`); SWU-006 rolls back a context plan whose concrete bindings arrive only in 007 (`TASK-UPW-COORDINATOR.md:48`, `TASK-UPW-COORDINATOR.md:61`).  
   **Repair:** Name the real snapshot token/retry bound; move route validation before endpoint admission; establish context-plan contracts before rollback integration.

3. **Task-shaped bundling/duplicate ownership.** SWU-010 combines independently testable annotation, batch, and revision modes; 016 combines keyboard, focus, live regions, contrast, target size, and color; 017 combines server allowlisting and iframe sandboxing (`TASK-UPW-REGIONS.md:18`, `TASK-UPW-HARDENING.md:11`, `TASK-UPW-HARDENING.md:32`). Live-scope behavior is also claimed by 010/012 and again by 016.  
   **Repair:** Split by independently falsifiable boundary and give each UPW-FIX obligation one mutation owner.

4. **Incomplete closeout.** Each row omits the promised `refresh-receipts/<SWU-ID>.json`, `EXECUTION-PACK.md`, and `PLAN-TRANSPORT.md`, while claiming Refresh may update only listed targets (`WORK-PACK.md:113`, `WORK-PACK.md:128`). W5’s “one closure report” has no exact path/schema/synchronization inventory (`TASK-UPW-VERIFY.md:37`).  
   **Repair:** Add exact source/result/refresh/closure receipt paths and every gate-bearing synchronization target for each SWU and W5.

5. **Coverage/dependency inflation.** Traceability is many-to-many but does not give 008, 009, or 013 an exact independently falsifiable UPW witness; the manifest also turns serial write-conflict ordering into semantic dependencies, notably 016→017 (`traceability.md:3`, `SWU-MANIFEST.json:23`).  
   **Repair:** Add an inverse SWU→Design→UPW acceptance matrix and distinguish semantic dependency from serialization constraint.

Per-SWU disposition:

| SWU | Verdict | Required repair |
|---|---|---|
| 001 | KEEP | Declare both currently absent files as intentional creations. |
| 002 | BLOCK | Specify authoritative epoch/token and retry bound. |
| 003 | SPLIT | Projection assembly/compatibility contract; then HTTP exposure. |
| 004 | KEEP | Make shell/test paths exact. |
| 005 | KEEP | Make coordinator/test paths exact. |
| 006 | BLOCK | Establish context-plan contract first; then split transaction engine from DOM integration if independently testable. |
| 007 | KEEP | Bind all matrix rows to one generic reconciliation contract and exact paths. |
| 008 | KEEP | Add one exact state-spine witness. |
| 009 | KEEP | Add one exact current-canvas identity witness. |
| 010 | SPLIT | Inspector selection shell versus state-mode adapters/interactions. |
| 011 | SPLIT | Keep comparison evidence; move acknowledgment binding to governed actions. |
| 012 | SPLIT | Action gates/transport versus scoped status semantics. |
| 013 | KEEP | Add a direct collapsed-lineage/expansion witness. |
| 014 | KEEP | Exact layout/spec paths only. |
| 015 | KEEP | Exact projection/copy/spec paths only. |
| 016 | SPLIT | Keyboard/focus; live-status scope; visual perceivability/targets. |
| 017 | SPLIT | Server route allowlist versus iframe sandbox/safe-sink enforcement. |

First-unit verdict: **SWU-UPW-001 narrowness is not falsified.** It is two new, isolated files, has no dependency, changes neither `/state` nor rendering, and has a focused deterministic command (`TASK-UPW-PROJECTION.md:12`). It remains only a recommended candidate, not selection.

Authority check: all witnesses remain unexecuted, Plan/Task Session gates remain blocked, and `selected_swu` is null/none (`PLAN-CONTEXT.md:20`, `SWU-MANIFEST.json:5`, `PLAN-TRANSPORT.md:24`). No artifact selects or executes implementation.

## Verbatim Return: Abramsky Final

## Abramsky FINAL — `BLOCK` pending structural repair

My initial `PD-VAL-01` was too narrow. The six-region validation gap remains, but Rittel established additional defects that prevent affirmative executable closure. The target architecture still recomposes conceptually; the literal SWU graph does not yet prove safe execution.

### 1. Mutation scopes — CONCEDE; STABILIZE WITH EXACT REPAIR

The Plan requires preflight hashes of every declared target and permits Refresh to update only the closeout inventory (`WORK-PACK.md:116`, `WORK-PACK.md:148`), but 004–017 use shorthand such as “same shell,” “shell/projection,” and “labels/copy” (`WORK-PACK.md:91`).

Exact repair:

- Replace every shorthand write scope in `WORK-PACK.md` and task files with exhaustive repository-relative paths.
- Mark each path `existing` or `create-if-absent`.
- Add per-SWU forbidden paths.
- State that omitted paths are unauthorized.
- Preserve serial overlap separately from semantic dependency.

### 2. Forward/non-runnable dependencies — CONCEDE

- **002:** “stable input identity/epoch” and “bounded constant” have neither an authoritative token owner nor numeric retry bound (`TASK-UPW-PROJECTION.md:47`). Repair: name the authoritative token, its producer/read boundary, equality semantics, retry count, and terminal error shape.
- **003/017:** 003 promises invalid-route rejection (`TASK-UPW-PROJECTION.md:77`), while server-side route validation is owned by later 017 (`TASK-UPW-HARDENING.md:32`). Repair: split route-family validation from iframe sandbox rendering and place the server validator before versioned endpoint admission.
- **006/007:** 006 computes and rolls back a context plan (`TASK-UPW-COORDINATOR.md:48`), but the identity bindings and reconciliation rules arrive in 007 (`TASK-UPW-COORDINATOR.md:61`). Repair: establish the typed context-plan interface and binding rules before 006, then let 006 own transactional application/rollback.

### 3. Task shape and duplicate ownership — MIXED

- **010 split: REFUTE.** Annotation, batch, and revision are mutually exclusive state projections of one contextual-inspector region, not three independently useful surfaces. The task explicitly makes the region state-specific and independent of canvas/actions (`TASK-UPW-REGIONS.md:18`).
- **011 split: REFUTE.** Candidate identity, diff, named frames, and acknowledgment context jointly form one staged-review evidence surface; action transport is already separated into 012 (`WORK-PACK.md:73`).
- **012 split: REFUTE.** Existing handlers plus scoped receipt feedback form one governed action behavior (`TASK-UPW-REGIONS.md:20`).
- **Duplicate live-scope ownership: CONCEDE.** 010, 012, and 016 overlap UPW-FIX-008–010. Exact repair: assign FIX-008 and FIX-010 accessibility/live semantics to 016; FIX-009 action-event emission to 012; keep 010 on contextual presence, identity, and disabled-state behavior. Other SWUs may run these only as regression checks.
- **016 split: CONCEDE.** Keyboard/focus/live behavior and contrast/target/color calibration are independently falsifiable despite the task’s retained-boundary assertion (`TASK-UPW-HARDENING.md:11`). Split interaction/focus/live semantics from visual/target calibration.
- **017 split: CONCEDE.** Server route admission and iframe sandbox rendering require separate units, with route admission moved before 003.

### 4. Closeout — CONCEDE; STABILIZE WITH EXACT REPAIR

The common contract names `refresh-receipts/<SWU-ID>.json` (`WORK-PACK.md:123`), but the target rows omit it and omit gate-bearing `EXECUTION-PACK.md` and `PLAN-TRANSPORT.md`.

Exact repair:

- Every mutation row must list source targets, `execution-receipts/<ID>.json`, `refresh-receipts/<ID>.json`, `WORK-PACK.md`, `SWU-MANIFEST.json`, exact task/wave files, `EXECUTION-PACK.md`, and `PLAN-TRANSPORT.md`.
- Each must state schema, baseline rule, permitted fields, and successor effect.
- W5 must declare an exact closure-report path/schema and its synchronized target inventory; its current “one closure report” is insufficiently addressed (`TASK-UPW-VERIFY.md:37`).

### 5. Coverage and dependency inflation — CONCEDE

My `PD-VAL-01` is retained and expanded. 008–013 lack exact runnable selectors; 008, 009, and 013 additionally lack direct, independently falsifiable witness bindings. The current trace is Design→SWU only (`traceability.md:3`).

Exact repair:

- Add an inverse `SWU → responsibility → input/output → Design obligation → exact assertion/fixture → exact command/selector` matrix.
- Add direct plan acceptance cases for 008 state/next-action, 009 stable current-frame identity, and 013 collapsed/expanded lineage continuity.
- Separate `semantic_dependencies` from `serialization_after`. The Plan itself says overlap drives serialization (`PLAN-CONTEXT.md:55`); notably 016→017 is not a semantic dependency.

### Final per-SWU dispositions

| SWUs | Verdict |
|---|---|
| 001 | **PASS/KEEP after create-if-absent and forbidden-scope markers** |
| 002 | **BLOCK** — token and retry contract absent |
| 003 | **BLOCK/SPLIT-DEPENDENCY REPAIR** — consumes deferred route validation |
| 004–005 | **PASS after exact path inventory** |
| 006 | **BLOCK** — consumes undeclared future context-plan contract |
| 007 | **PASS**, subject to reordered context-plan ownership |
| 008–009 | **FLAG** — direct witness and exact selector required |
| 010–012 | **KEEP**, with exclusive witness ownership and exact selectors |
| 013 | **FLAG** — direct lineage witness/selector required |
| 014–015 | **PASS after exact path inventory** |
| 016 | **BLOCK/SPLIT** |
| 017 | **BLOCK/SPLIT AND REORDER** |

`SWU-UPW-001` remains the narrowest reversible first candidate: no dependency, two isolated paths, golden-vector acceptance, and no `/state` or rendering mutation (`TASK-UPW-PROJECTION.md:16`). This is still a recommendation only; `selected_swu` remains `null`.

Recomposition is **architecturally affirmative but executably BLOCKED**. The intended chain and W5 denominator remain coherent, but endpoint security, context transaction ordering, witness ownership, dependency kinds, mutation scopes, and closeout targets must be repaired before the literal units can safely recompose.

## Verbatim Return: Rittel Final

FINAL position — `BLOCK`, repairable without losing the Design’s recomposition spine.

1. **Abramsky: semantic decomposition PASS — REFUTE as a claim about the literal current Plan; STABILIZE most units with bounded repairs.**

   The responsibility labels are coherent, but “bounded write surface” is false: 004–017 use scopes such as “same shell/coordinator,” “shell/projection,” and a task-wide shared renderer/spec scope rather than exhaustive paths (`WORK-PACK.md:86`, `TASK-UPW-REGIONS.md:11`).  
   **Exact repair:** for every SWU, enumerate exact repo-relative source/test paths, mark each absent future path `create-if-absent`, and declare forbidden overlapping paths.

   SWU-002’s “stable input identity/epoch” and “bounded constant” are unnamed, so its algorithm cannot currently be preflighted or falsified deterministically (`TASK-UPW-PROJECTION.md:47`).  
   **Exact repair:** name the authoritative store token/identity construction and literal retry maximum.

   SWU-003 rejects invalid route data before SWU-017 introduces route validation (`TASK-UPW-PROJECTION.md:77`, `TASK-UPW-HARDENING.md:38`).  
   **Exact repair:** constrain 003 to existing route validity or move server allowlisting ahead of endpoint admission.

   SWU-006 computes and rolls back a context plan before 007 defines concrete context bindings (`TASK-UPW-COORDINATOR.md:48`, `TASK-UPW-COORDINATOR.md:61`).  
   **Exact repair:** make 006 journal/restore an opaque context snapshot only; leave identity-specific planning and feedback to 007.

2. **Abramsky: closeout coherence PASS — REFUTE.**

   The common contract requires `refresh-receipts/<SWU-ID>.json`, but every declared inventory lists only planning files and the incoming execution receipt, then says Refresh may update only those targets (`WORK-PACK.md:113`, `WORK-PACK.md:128`). W5 likewise promises “one closure report” without an exact path, schema, or synchronized targets (`TASK-UPW-VERIFY.md:37`).  
   **Exact repair:** add the refresh receipt to every target inventory and give W5 an exact report/receipt path, schema, owner validation, and plan-state synchronization list.

3. **Abramsky: PD-VAL-01 FLAG for 008–013 — CONCEDE.**

   The task promises a “named focused Playwright slice,” but supplies only one two-spec task-closeout command (`TASK-UPW-REGIONS.md:35`).  
   **Exact repair:** bind each of 008–013 to one exact spec path, selector/grep, positive assertion, negative mutant, and expected receipt field.

4. **Abramsky: per-SWU closure PASS except 008–013 — REFUTE.**

   Final disposition:

| SWU | Final disposition |
|---|---|
| 001 | KEEP |
| 002 | BLOCK until epoch/retry repair |
| 003 | KEEP after route-validity repair; withdraw prior split |
| 004 | KEEP |
| 005 | KEEP |
| 006 | BLOCK until opaque-context repair; no split then required |
| 007 | KEEP |
| 008–013 | KEEP after PD-VAL-01 selectors; withdraw prior 010–012 splits |
| 014–015 | KEEP |
| 016 | SPLIT |
| 017 | SPLIT |

   SWU-016 remains task-shaped: keyboard/focus, live-region ownership, contrast, target size, and color/error signaling have distinct fixtures and can fail independently (`TASK-UPW-HARDENING.md:11`, `WITNESS-CONTRACTS.md:21`).  
   **Exact repair:** split into keyboard/focus, scoped status semantics, and visual perceivability/target-size SWUs.

   SWU-017 combines independently enforceable server route admission and browser sandbox/safe-sink defenses (`TASK-UPW-HARDENING.md:32`, `WITNESS-CONTRACTS.md:35`).  
   **Exact repair:** split route-family validation from iframe sandbox/safe-sink enforcement.

5. **Abramsky: first-unit PASS — CONCEDE.**

   Serializer and hasher jointly establish one digest-identity behavior; the unit has exact isolated files, no dependency, a focused command, and does not change `/state` or rendering (`TASK-UPW-PROJECTION.md:12`). SWU-001 remains the narrowest reversible trust-building candidate. It is not selected.

6. **Abramsky: recomposition proof PASS — STABILIZE WITH EXACT REPAIR.**

   The semantic spine survives: digest → coherent snapshot → transport → inert shell → freshness → recoverable commit → context → regions → responsive/copy → bounded semantics/security → W5 (`EXECUTION-PACK.md:18`). After repairing 002/003/006, splitting 016/017, regenerating manifest/waves/closeout rows, and adding 008–013 selectors, recomposition is credible without reopening Design. Until then, false dependency readiness and incomplete closeout justify `BLOCK`, not merely `FLAG`.

Authority remains intact: `selected_swu` is null, all SWUs are `not-started`, witnesses are unexecuted, and Task Session admission remains blocked (`SWU-MANIFEST.json:5`, `PLAN-TRANSPORT.md:24`). No SWU is selected or executed.

## Verbatim Return: Schön Verifier

Verifier verdict: **BLOCK survives, but not PASS/no-objection.** Nine MAJOR findings survive; PD-09 is severity-inflated and prescribes a schema mechanism not required by Plan law. One bounded Noether revision should correct PD-08’s ownership wording and PD-09’s severity/repair. The zig-zag does not terminate yet.

- **PD-01 — SUSTAIN, MAJOR.** `WORK-PACK.md:86-104` uses abbreviations/prose such as “projection source/test,” “same shell,” and “route validation/shell”; several task scopes name future files/specs without exact create-if-absent or forbidden boundaries. Yet every target is baseline-hashed and Refresh may mutate only the inventory (`WORK-PACK.md:109-150`). Plan law requires explicit write scope and complete pre-mutation synchronization inventory (`invoke/plan.md:199-202,314-320`). Repair as proposed. Dispositions remain valid; all retained SWUs are conditional on this repair.

- **PD-02 — SUSTAIN, MAJOR.** The algorithm says only “stable input identity/epoch,” “bounded constant,” and “typed recoverable failure” (`TASK-UPW-PROJECTION.md:40-65`). Current `StudioSessionStorePort` exposes no epoch/transaction token (`ports.ts:17-38`), while file-store methods independently `readFresh()` (`file-studio-session-store.ts:58-67,100-126`). Name the authoritative producer or serialized-read primitive, equality rule, numeric retry bound, and exhaustion type. KEEP 002 after repair.

- **PD-03 — SUSTAIN, MAJOR.** SWU-003 promises invalid-route failure (`TASK-UPW-PROJECTION.md:67-93`) but route admission is deferred to 017 (`TASK-UPW-HARDENING.md:32-48`; manifest lines 10,24). KEEP 003 is compatible with repair: “KEEP” concerns its atomic boundary, not immutable ordering. Either constrain 003 to already-valid existing route families, or split 017 and move its admission child before 003. SPLIT/BLOCK 017 remains valid.

- **PD-04 — SUSTAIN, MAJOR.** 006 computes and rolls back a context plan (`TASK-UPW-COORDINATOR.md:48-59`) before 007 defines binding/reconciliation (`:61-72`), although Design requires calculation before journaled commit (`ARCHITECTURE.md:180-205`). Introduce the typed planner interface before 006, or make 006 journal/restore context opaquely and defer planning to 007. KEEP 006–007 after repair.

- **PD-05 — SUSTAIN, MAJOR.** 016 combines keyboard/pointer, focus, live scopes, color, contrast, and target size under one acceptance (`TASK-UPW-HARDENING.md:11-30`; `WITNESS-CONTRACTS.md:19-35`). These contain independently passing boundaries, violating `invoke/plan.md:195-197`. Split at least interaction/focus/live from calibrated visual/target semantics; test scoped-status/error urgency as a possible third. SPLIT/BLOCK 016 valid.

- **PD-06 — SUSTAIN, MAJOR.** Server route admission and iframe sandbox rendering have separate mutation sites and negative witnesses (`TASK-UPW-HARDENING.md:32-48`; UPW-FIX-023/024 at `WITNESS-CONTRACTS.md:35-36`). Split; place route admission consistently with PD-03. SPLIT/BLOCK 017 valid.

- **PD-07 — SUSTAIN, MAJOR.** 008–013 provide outcome prose and generic “focused” checks, not exact spec/grep commands, polarity, or receipt binding (`TASK-UPW-REGIONS.md:14-40`). Plan law requires each SWU’s acceptance evidence and verification command/reviewable check (`invoke/plan.md:199,212-229`). Repair per SWU. KEEP 008–013 after repair.

- **PD-08 — SUSTAIN, MAJOR, repair wording corrected.** The trace maps 010/012/016 to overlapping fixtures and gives no direct acceptance witness for 008, 009, or 013 (`traceability.md:9-17`; `TASK-UPW-REGIONS.md:16-21`). Require an inverse SWU→Design→assertion matrix with one **primary acceptance owner per assertion**. Do not require absolute uniqueness of witness files: shared recomposition/regression witnesses are lawful when their owned assertions are explicit. Candidate SWU dispositions remain valid.

- **PD-09 — REFUTE as framed.** The manifest is a single 001→017 chain (`SWU-MANIFEST.json:8-24`), while waves explain shared-file serialization (`W1.md:6-8`, `W2.md:6-9`). The underlying semantic-vs-write-order ambiguity is real, but current order is safe and executable; Plan law requires accurate dependencies and parallelization boundaries, not fields named `semantic_dependencies` and `serialization_after` (`invoke/plan.md:258-267`). Correct severity: **MINOR**, not MAJOR. Repair by distinguishing semantic prerequisites from serialization in the existing manifest/waves; new fields are optional only if the local schema is intentionally revised and validated. No SWU disposition changes.

- **PD-10 — SUSTAIN, MAJOR.** Closeout rows include execution receipts but omit the declared Refresh receipt and omit synchronization of current-state `EXECUTION-PACK.md`/`PLAN-TRANSPORT.md` (`WORK-PACK.md:109-150`). W5 promises only “one closure report,” with no exact path/schema/required synchronization (`TASK-UPW-VERIFY.md:37-41`). This violates the exact preflightable closeout contract (`invoke/plan.md:25-30,314-317`). Repair exact inventories and W5 report contract. Artifact FIX dispositions remain valid.

Denominator checks pass literally: 17 unique mutation SWUs, five mutation tasks/waves plus the exempt VERIFY task/W5 = six tasks and six waves; `selected_swu` is null (`SWU-MANIFEST.json:5-24`). SWU-001 remains the narrowest reversible recommendation, not a selection (`WORK-PACK.md:63,88`; `PLAN-TRANSPORT.md:38-48`). Recomposition architecture survives through all six Design views and UPW-FIX-001–024 (`traceability.md:3-18`), but executable closure remains blocked.

The passing Design admits authoring only (`DESIGN-DISTILL.md:78-84`); all witnesses remain unexecuted, L3/human/release claims remain outside, and `authority_effect: none` is correct. This verification frame expires on material Plan or Design byte changes.
