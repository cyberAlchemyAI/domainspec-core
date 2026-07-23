# Collected Attacker And Verifier Returns

This file mechanically preserves the final post-confrontation attacker returns and both verifier dispositions. Findings and final parent disposition are in `findings.md`.

## Goldratt, Eliyahu — computational/empirical attacker — final post-confrontation return

Final confrontation: Ashby changes my position materially on Subagents, Inventory, and Whisper. My lean combined package is below.

1. Task Session — **AGREE**

- Evidence: `--auto` says non-blocking “or where a recommendation is clearly safe” ([SKILL](arcanum/arcana/task-session/SKILL.md:106)); that subjective escape hatch conflicts with its own “ask user for each blocker” rule (line 105). Validation failure may return `FLAG` ([line 148]) without distinguishing acceptance-critical criteria. There are no Task Session behavioral/red-receipt fixtures under `arcanum/arcana/task-session/`.
- Lean change: delete “or where a recommendation is clearly safe”; `--auto` is non-blocking only. Add typed done-criterion criticality and require `BLOCK` for an unmet acceptance-critical criterion; add fixtures proving auto cannot select a blocker and critical validation cannot yield a completion-capable flag.
- Preserve: bounded recovery and `FLAG` for non-critical/deferred validation; this avoids turning harmless uncertainty into extra waits.

2. Invoke — **NARROW**

- Evidence: Ashby is right about registry promotion: `development/VALIDATION.md:77` blocks registry release for `plan`, `full`, and `validate` pending controls/live regimes. But the claimed runtime exposure is partly already contained: `mode-capabilities.json` marks `full`/`validate` deferred with `mutation_handoff_allowed: never`, and the root says they return `unsupported` before Dispatch/Distill ([README](arcanum/spells/invoke/README.md:48)). `plan` is active and has live evidence; it should not be silently downgraded to read-only.
- Lean change: add a machine-enforced **promotion/status ceiling** to the capability resolver: active authoring vs registry-release-ready are separate states; `full`/`validate` remain `unsupported`, and no active mode can claim registry/promotion readiness without its deterministic and live-regime receipts. Keep the earlier patch-verdict/readiness preflight and behavioral negative fixtures.
- Reject: a blanket read-only-by-default validator for `plan`; it would contradict the active mode contract and add cost without evidence of unsafe plan mutation.

3. DomainSpec Subagents Strategy — **AGREE**

- Evidence: canonical appender explicitly accepts reserved `code/plan/suggestion` rows and only logs a note (`append-dispatch.cjs:392`); it permits orphan closes (`:372`); `final_approver` is only checked non-empty (`:161`), not against working-agent identities; `working_folder` only strips leading `./` and rejects `vault/` text (`:176`), not normalized containment. Installed `.claude` appender remains schema v0.6.0 while canonical is v0.6.1; telemetry already observed this projection failure.
- Lean change: enforce LIVE type at registration; reject orphan/duplicate closes; resolve working-folder realpath beneath an approved non-vault root; enforce approver ≠ any working agent; regenerate installed skill/appender and add parity test. Persist tension proof as part of the same registration receipt, not a separate human gate.
- Preserve: one human entry confirmation and inline-review option.

4. Decision Gate — **AGREE**

- Evidence: the only override rule is generic—consequential work may proceed if “the user explicitly overrides the gate” ([SKILL](arcanum/arcana/decision-gate/SKILL.md:103)); observability records only “user override, if any” (line 117). It carries no target scope, hazard, evidence, or expiry.
- Lean change: add a typed override receipt: exact target/write scope, blocked decision IDs, hazard class, rationale, issuer, timestamp/expiry, and one-use semantics. Callers still must reject malformed structural packages before invoking Decision Gate.
- This supersedes my initial “only narrow callers” conclusion: caller narrowing prevents theater; typed override prevents ambient assent.

5. Inventory — **AGREE**

- Evidence: live `.arcanum/inventory/index.json` currently fails `validate-index-json.sh`: 15 entries use kinds outside the hardcoded enum—`query-file` (2), `research-findings` (4), `research-transcript` (4), `strategy-result` (5). It nevertheless advertises parseability; parseability is weaker than conformance. The validator’s listed enum is at [validate-index-json.sh](arcanum/arcana/inventory/scripts/validate-index-json.sh:50).
- Lean change: first reconcile schema enum with the accepted live kinds (or migrate the records), then make index validation required before an inventory “completed/pass” signal. Add the bidirectional derived-index checks I proposed earlier. Keep historical uncontrolled-tag warnings warn-only unless changed entries violate the catalog.
- Preserve: `index.json`-first, read-only/non-authoritative lookup.

6. Whisper — **NARROW**

- Evidence: my “regenerate Claude from canonical” recommendation was too broad. `.agents/skills/whisper/` is a repository-local overlay with `product_research_blueprint` and `intent_state`/fan-out gating; these are absent from public canonical but are substantive local behavior. Canonical independently has current transport-audition/volatile-intent controls ([README](arcanum/spells/whisper/README.md:105), [139]), while the older `.claude` runtime lacks them. The receipt validator has proven status-ceiling controls for candidate/unproven transports and human approval (`validate-whisper-run-receipt.py:131`).
- Lean change: split runtime assembly into **canonical generated base + declared repo-local overlay manifest**, with allowed extension points, provenance/digests, and parity tests that ensure overlays neither silently disappear nor overwrite canonical guarantees. Regenerate `.claude` from this composition, not from canonical alone.
- Preserve: negative fixtures for duplicate prose, transport proof/status ceiling, human editorial approval, and local product-research/intent-state controls.

## Ashby, W. Ross — formal/adversarial attacker — final post-confrontation return

## Final confrontation position

Goldratt is right that late invalid-package discovery and generated-surface drift are major bottlenecks. Those proposals combine with stronger machine controls; they do not displace controls that contain concrete authority, mutation, or false-readiness hazards.

### 1. Task Session — NARROW

Goldratt’s digest-bound readiness receipt is a good fast path, but “rebuild only when absent/stale” is too weak unless staleness includes every controlling input.

Evidence:

- `arcanum/arcana/task-session/SKILL.md:85-90` requires bounded context and blocks stale, contradictory, unsafe, validation-less, or write-scope-less context.
- Lines `111-114` independently check dependencies, approvals, destructive action, write scope, and validation.
- Lines `142-148` retain live done-criterion validation and closeout.
- Current telemetry `.arcanum/observability/tmp/task-session-20260723T000729Z-bte-l0-context-route-conflict.json` is the failure witness: a prior continuation pointed to the wrong path and the live pass found a circular SWU after a decision had resolved.

Lean combined change:

- Invoke/Implementation Readiness emits a receipt binding target, task/SWU identity, exact controlling paths and digests, dependency frontier, write scope, validation commands, authority/publication class, generated-surface parity result, and expiry.
- Task Session verifies those bindings cheaply. It rebuilds full context on absence, mismatch, unresolved residue, changed dependency state, or missing authority/publication classification.
- Keep live validation and subagent closeout.
- Also tighten two independent hazards: `--auto` never resolves blocker/destructive/authority-changing decisions (`task-session:105-107`), and acceptance-critical unavailable/failed validation cannot degrade to `FLAG` (`140-148`).

This reduces repeated context work without allowing a digest receipt to become stale authority.

### 2. Invoke — AGREE

Goldratt identifies the correct earliest containment point.

Evidence:

- `arcanum/spells/invoke/README.md:78-83` separates authoring from execution authority.
- Lines `144-150` make Distill block mutation handoff.
- Lines `231-254` require layering, work-pack, validation strategy, Distill, SWUs, approval, and proposal-only refresh.
- `arcanum/spells/invoke/development/VALIDATION.md:77` nevertheless says `plan`, `full`, and `validate` remain release-blocked pending matching deterministic controls/live regimes.
- Current fixtures cover many abstract positive/negative outputs, but the wrapper reported `EXAMPLE-OUTPUTS (0 checked)`: materialized package validation is the missing control.

Lean combined change:

- Add one pre-handoff validator over the actual candidate patch/package, not only narrative receipts.
- It checks allowed paths, public/private classification, target-owner boundaries, source and output digests, dependencies, generated mirrors, approval class (`proposal-only`, `apply-approved`, lifecycle approval), validation commands, and mutation status.
- Add negative fixtures for private evidence in public output, stale/missing digest, path escape, missing dependency, proposal-only mutation, and blocked mode claiming mutation readiness.
- Materialize the Task Session readiness receipt only after this validator passes.
- Preserve proposal-only default and phase-status/handoff-status separation.

This displaces redundant late Task Session package reconstruction, but not Task Session’s live verification of actual execution.

### 3. DomainSpec Subagents Strategy — NARROW

Persisting check-tension and parity testing is useful, but insufficient by itself. Check-tension is semantic review; it does not contain schema-enforceable authority hazards.

Evidence:

- Canonical `implementation/.../domainspec-subagents-strategy/SKILL.md:82-86` requires double tension PASS, explicit confirmation, and sheet freeze.
- Lines `157-166` forbid RESERVED dispatch types.
- Lines `190-196` prohibit self-approval and protect public/private boundaries.
- Appender comments `append-dispatch.cjs:30-37` explicitly decline to enforce self-approval.
- `append-dispatch.cjs:362-363` records RESERVED types anyway.
- `tests/test-append-dispatch.cjs:270-272` positively tests RESERVED `code` append.
- Lines `341-342`, with test `292-293`, permit orphan close rows.
- `.claude/skills/domainspec-subagents-strategy/SKILL.md` is materially stale versus the canonical 204-line adapter.

Lean combined change:

- Persist the two check-tension receipts, their sheet digest, and confirmation against that same digest.
- Add canonical/generated appender and skill parity tests.
- Do not add a second human gate.
- At the existing registration boundary, reject RESERVED types, self-approving final approvers, orphan normal close rows, path traversal/repo escape, and public destinations carrying private evidence.
- Keep the single explicit human delegation confirmation because it grants real delegation authority.

Goldratt’s proposal improves auditability; the machine checks provide containment.

### 4. Decision Gate — NARROW, mostly KEEP

I accept Goldratt’s core claim: Decision Gate should not adjudicate structurally invalid packages. Callers must reject those before it, and Decision Gate should run only when two or more valid repairs remain.

Evidence:

- `arcanum/arcana/decision-gate/SKILL.md:52-64` already frames the gate around viable options.
- Lines `65-81` require actual selection and durable provenance.
- Lines `84-101` correctly make explanation and uncertainty non-consent.
- Structural invalidity has no meaningful choice and belongs in Invoke/Implementation Readiness/Task Session validation.

One contained defect remains:

- `decision-gate:103-105` permits proceeding after an “explicit override” without defining target, scope, hazard class, or provenance.

Lean combined change:

- KEEP Decision Gate’s workflow.
- Add a caller precondition: structural invalidity returns `BLOCK` directly; invoke Decision Gate only for at least two validator-admissible repairs.
- Narrow override to a typed, scoped decision receipt. Generic override cannot authorize destructive/irreversible action, authority promotion, public/private publication, or spend.
- Add only small negative fixtures for no-valid-option invocation, explanation-as-consent, ambiguous override, stale approval, and scope mismatch.

Thus stronger validation mostly displaces misuse of Decision Gate, not Decision Gate itself.

### 5. Inventory — AGREE, with an immediate schema reconciliation

Bidirectional projection and freshness validation are the right lean mechanism, but the current live failure must be resolved first.

Evidence:

- `arcanum/arcana/inventory/SKILL.md:112-121` makes `index.json` machine-first and requires gaps/exclusions.
- Lines `159-218` define human/machine projections and Inventory-only authority.
- Lines `294-298` separate Inventory from Ontology and Definitions authority.
- The current `validate-index-json.sh .arcanum/inventory/index.json` fails `entries have required fields`.
- Fifteen live rows use kinds outside `validate-index-json.sh:50-64`, including `research-transcript`, `research-findings`, `query-file`, and `strategy-result`.

Lean combined change:

- Reconcile the kind enum and updater output first.
- Validate both directions:
  - every governed inventory entry appears in `index.json` and `index.md`;
  - every projection row resolves to an existing source file;
  - source digest/update time agrees with projection freshness;
  - derived indexes contain only current IDs;
  - human and machine projections agree on identity/status.
- Historical tag lint is conditional: enforce current taxonomy on active/candidate entries; report legacy tags as migration residue unless they affect lookup or authority.
- Lookup packets carry the current validator result, not merely JSON parseability.

This turns the current false-ready machine view into a verifiable read model without over-governing history.

### 6. Whisper — NARROW

Goldratt is right about regeneration and parity, but drift is not limited to `.claude`: `.agents` is also materially different from canonical.

Evidence:

- Canonical `arcanum/spells/whisper/README.md:99-109` preserves audition and editorial status ceilings.
- Lines `225-227` prohibit schema/layout/Playwright evidence from satisfying operator voice approval.
- `.agents/skills/whisper/SKILL.md` adds `product_research_blueprint` and an extra intent-state gate absent from canonical while claiming generated canonical provenance.
- `.claude/skills/whisper/SKILL.md` also needs parity verification.
- By contrast, Task Session, Decision Gate, and Inventory mirror differences are generated metadata/newline only.
- Whisper’s editorial schema suite passed 16/16, including 13 negative cases for ambient approval, cross-axis substitution, missing comprehension, malformed digests, and approval-surface mismatch.

Lean combined change:

- Regenerate both `.agents` and `.claude` from canonical.
- Move `product_research_blueprint` to an explicitly local overlay, or promote it canonically through lifecycle evidence.
- Add semantic parity tests that permit runtime metadata but reject undeclared transports, gates, statuses, or authority changes.
- Bind each Whisper receipt to canonical schema/preset digest.
- Preserve the existing editorial status ceiling and negative suite; add one case where structural/browser PASS attempts to promote editorial proof.

Parity controls displace accidental runtime divergence. They do not displace Whisper’s human/editorial gate because cross-axis validation cannot prove voice approval.

## Combined minimum package

The lean cross-skill solution is one evidence chain:

`Invoke materialized package validator` → `digest-bound readiness receipt` → `Task Session cheap binding check + live execution validation` → `typed Decision Gate only for multiple valid repairs`.

Alongside it:

- canonical/generated semantic parity for all installed skills and appender copies;
- Subagents’ single human confirmation bound to a persisted sheet/check-tension digest;
- Inventory bidirectional source/projection/freshness validation;
- Whisper’s existing editorial status ceiling.

That attacks Goldratt’s bottleneck while retaining only gates with concrete authority, mutation, publication, destructive-action, or false-readiness containment.

## Popper, Karl — verifier — round 1 return

## Verdict: REVISE

Most candidates survive, but several need scope/severity correction and two contain overbroad prescriptions.

## Surviving findings

- **TS-1 — HIGH, corrected.** `task-session` permits `--auto` for decisions “non-blocking **or** where a recommendation is clearly safe” (`arcanum/arcana/task-session/SKILL.md:106`), despite separately warning against guessing consequential choices. It also validates every done criterion/obligation (`:142`) but turns unrecovered validation failure into generic `FLAG` (`:148`). Fix: auto-selection only for explicitly non-consequential/reversible decisions; acceptance-critical validation failure or inability to validate must `BLOCK`; reserve `FLAG` for named noncritical residue. Add negative fixtures. The gate is useful, but these escape clauses weaken it.

- **TS-2 — HIGH for routed/reusable execution only.** Existing controls are substantial: Context Builder runs before mutation, stale/unsafe/weak/missing coverage blocks (`:85-90`), runtime handoff uses strict Markdown plus JSON/index, and live execution must revalidate. Therefore this is not a “no readiness mechanism” finding. The narrower gap is that no durable execution admission receipt binds the selected task/SWU and strict pack to controlling identities/digests, dependency frontier, allowed writes, validation surface, and authority/publication class. Add that receipt at runtime/routed handoff, verify it immediately before mutation, rebuild on mismatch, and retain live validation. Do not impose arbitrary expiry/runtime-parity fields on every local Task Session without a demonstrated consumer.

- **INV-1 — HIGH, not SEVERE.** Refresh’s JSON contract ends in an unconstrained `validation: []`; the mode gates ensure evidence-to-delta mapping, scope, approval, and status separation, but no deterministic check proves that a material apply package covers exact target paths/identities, dependencies, mirrors, ownership/publication boundary, and mutation scope. Add a material-package validator for `apply-approved`/mutation-capable handoff plus negative fixtures. Proposal-only completion must remain possible without apply authorization. A readiness receipt should be downstream of validator pass.

- **INV-2 — MEDIUM, wording already appropriately narrow.** Literal status is: Plan is an implemented L2 authoring/governance contract and is expressly nonexecuting; `full` and `validate` are deferred/unsupported and must not grant mutation handoff. Registry release/runtime execution remain separately gated. Add or standardize the three ceilings: artifact authored, registry-released, mutation/runtime-ready. Do not call all Plan output blanket “read-only”: it writes planning artifacts while forbidding target/source execution mutation.

- **DSS-1 — HIGH.** Appender comments explicitly say no-self-approval is not enforced; tests demonstrate RESERVED rows are accepted; orphan closes are warned then appended; duplicate close is safely idempotent; working-folder protection is lexical and vault-specific. Correct fix: reject new RESERVED dispatch rows, orphan closes, and final approvers present among working agents; canonicalize/resolve paths before boundary checks; add explicit authority/publication classification if private-to-public enforcement is expected. Grandfather existing ledger history. Do not describe duplicate close as currently unsafe—it is already a no-op.

- **DSS-2 — HIGH.** Strategy prose requires two tension passes and frozen human confirmation, but the persisted row lacks tension evidence and confirmed-sheet identity/digest. Persist both tension verdicts and exact confirmed-sheet digest, and reject registration if the current sheet differs. This strengthens the existing single gate rather than adding another.

  The reported `diff` is real and partly substantive, not mere metadata. The canonical/tooling copy adds the public-Arcanum-core/private-DomainSpec-adapter boundary and a research transcript/findings ownership rule absent from installed Codex. The installed copy also has extensive formatting drift and some locally newer wording. Therefore “byte-identical” is false, and parity must be resolved by classified canonical-base plus declared local overlay—not a blind byte-copy assertion.

- **DG-1 — HIGH, corrected.** Decision Gate says it enumerates “more than one viable option,” but provides no explicit admissibility preflight and allows a generic explicit override after `BLOCK` with no target, hazard, scope, lifetime, or consumption semantics. Require callers/Gate to reject structurally invalid choices before presenting option cards; if fewer than two admissible choices remain, return direct structural `BLOCK` or the single safe repair route, rather than fabricate a decision. Replace generic override with typed, target-bound, one-use authorization, excluding destructive, authority/publication, spend, and other irreversible commitments unless their owning gate separately authorizes them.

- **INT-1 — HIGH, count confirmed exactly.** Current validator exits 1 at “entries have required fields.” There are exactly **15** out-of-enum kinds: 2 `query-file`, 4 `research-findings`, 4 `research-transcript`, 5 `strategy-result`. Reconcile producer/updater vocabulary, live rows, and validator enum; Inventory cannot claim ready while its canonical machine index fails its own validator.

- **INT-2 — MEDIUM.** Current validator checks required derived indexes exist, `by_id` references known IDs, and projections declare themselves secondary. That does not prove bidirectional identity/completeness/freshness among source entries, `index.json`, `index.md`, and projections. Add those checks and make lookup report validator status. Historical free-form tags should remain warning-only until a closed vocabulary is actually governed.

- **WH-1 — HIGH, corrected.** `.agents` contains the current canonical controls (`surface_map`, `language_audition`, `intent_state`) and several local preset extensions, including `product_research_blueprint`, `business_plan`, and `live_presentation`; `.claude` lacks the three current controls. Thus `.agents` is not merely one undeclared product overlay, and `.claude` is materially stale. Generate a canonical base plus explicit overlay manifest with extension points/digests; permit declared presets, reject undeclared removal/addition of gates/status/authority semantics, and regenerate stale runtimes. Preserve editorial negatives and legitimate local presets.

## Refuted portions

- “Duplicate close is unsafe” is refuted: existing behavior is idempotent/no-op.
- “Canonical/tooling and installed DSS are byte-identical” is refuted by substantive diff.
- Universal TS receipt expiry/runtime-parity is unsupported; scope it to routed/reusable mutation admission.
- Decision Gate must always present “two repairs” is too rigid; invalidity may leave one safe repair or none.
- `.agents` has only `product_research_blueprint` as overlay is false; it has multiple declared-looking local preset extensions.
- Gap-item totals are not failure counts and should not support severity or incidence claims.

## Missing coverage

- Run the existing DSS appender test suite and add counterexample fixtures for symlink/`..` escape, approver/member collision, RESERVED insertion, orphan close, and confirmed-sheet mutation.
- Inspect telemetry rows individually before using the supplied use/gap counts; six legacy Invoke rows missing `sigil` are schema-era residue, not automatically six execution failures.
- Add fixture-level evidence that acceptance-critical Task Session failures cannot finish `FLAG`.
- Add end-to-end parity validation across canonical Whisper base, generated runtimes, and declared overlays.
- Verify Inventory regeneration/updater behavior after enum reconciliation, not only the static validator.

## Popper, Karl — verifier — final return

ACCEPT, with two bounded wording corrections:

- **DSS-1:** Say “canonicalized path containment, including existing-parent realpath/symlink checks” rather than simply “realpath escape.” A new working folder may not yet exist, so literal `realpath` of the leaf cannot always be required.
- **DG-1:** Replace “2+ valid repairs gate” with “2+ admissible options invoke the choice gate.” Options may include defer/stop and need not all be repairs.

No remaining blocking defect is unsupported. The order is a prioritization of independent change requests; it does not imply one combined mutation or authorize implementation.
