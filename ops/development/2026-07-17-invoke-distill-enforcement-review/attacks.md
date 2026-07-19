# Invoke Distill Enforcement Review - Attack Transcript


## Verifier Returns

### Rittel, Horst

**Definitional Verification**

1. **UPHELD — Runtime role policy.** Distill says: “Use true subagents whenever the active runtime supports them” and, only if unavailable, “run labeled Proposer and Balancer passes in one agent” ([Distill](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:83)). Both paths owe the same trace at lines 86–92.<br>
Required correction: none. Historical Workbench execution path remains unknown; the later review dispatch’s runtime claim does not prove the earlier run.

2. **UPHELD — Semantic execution obligations.** A successful execution must preserve role trace, classify objections, run techniques, and return navigation ([Distill](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:172)); finite rounds are mandatory at line 80.<br>
Required correction: none.

3. **UPHELD — Plan records verdict without execution proof.** Plan requires running Distill over named artifacts ([plan.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/plan.md:116)) but outputs only verdict, recomposition status, and gap count at line 373.<br>
Required correction: require evidence covering Distill’s literal output contract before mutation routing.

4. **UPHELD — Root contract has the same proof gap.** Root permits `pass` routing at lines 134–142 but preserves only “verdict, gap summary, and recomposition proof status” ([README](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:218)).<br>
Required correction: gate routing on validated contract-complete evidence.

5. **UPHELD — Fixtures admit label-only passes.** The runner checks only `Distill validation:` at lines 347–359 and 513–557 ([runner](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:337)); the passing fixture contains only “pass; recomposition proof pass; gap count 0” ([fixture](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/fixtures/INV-PLAN-PASS-001.expected.md:15)).<br>
Required correction: add executable positive and negative validation cases.

6. **UPHELD — No runtime-backed evidence contract exists.** Distill’s required result includes role conversation, rounds, techniques, tensions, and navigation ([Distill](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:220)); Invoke does not project them.<br>
Required correction: define an enforceable evidence projection.

7. **UPHELD — `handoff` omits root Dispatch/conditional-Distill projection.** Its required sections and output contain neither ([handoff](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/handoff.md:96)), while root says “Every invoke mode” must record Dispatch and handoff “should run Distill” when broad ([README](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:117)).<br>
Required correction: add mode-local trace, trigger/skip rationale, and gates.

8. **UPHELD — `refresh` has the same omission.** Its report, gates, observability, and output omit both fields ([refresh](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/refresh.md:115)).<br>
Required correction: same as handoff, including bounded no-op behavior.

9. **UPHELD — Deferred-mode incoherence.** Root says `full` and `validate` “must run” Distill, while each literal mode says `Status: deferred` and “When implemented” ([full](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/full.md:7), [validate](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/validate.md:7)).<br>
Required correction: fail closed as deferred; do not implement them in this remediation.

10. **UPHELD — `define`/`design` preserve status, not proof.** Define requires a conditional sanity check ([define](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/define.md:67)); design requires a unit check ([design](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/design.md:128)), but their projections stop at status/rationale.<br>
Required correction: add common execution-evidence fields when Distill runs.

11. **UPHELD — Anti-bias is bounded.** It applies only to `n >= 2` investigate/evaluate subject groups and explicitly excludes single synthesizers/auditors ([anti-bias](/home/vrondelli/projects/domainspec-core/.claude/skills/anti-bias-vector-composition/SKILL.md:27)).<br>
Required correction: reject blanket application to Distill role simulation.

12. **UPHELD — Workbench pass is unverified.** It declares pass without the required role, round, objection, or technique traces ([validation](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/DISTILL-VALIDATION.md:3)) and routes to Task Session ([result](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/INVOKE-RESULT.md:20)).<br>
Required correction: replay; do not invalidate the eleven-SWU decomposition itself.

13. **UPHELD — Observability is stale.** It records five SWUs ([run](/home/vrondelli/projects/domainspec-core/.arcanum/observability/runs/invoke-20260717T080501Z-workbench-ui-v1.json:36)); the manifest has eleven ([work-pack](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/WORK-PACK.md:47)).<br>
Required correction: append a superseding assessment.

14. **UPHELD — Mirrors are not the cause.** The generated package declares canonical generation and regeneration-only mutation ([generated skill](/home/vrondelli/projects/domainspec-core/.agents/skills/invoke/SKILL.md:2)).<br>
Required correction: regenerate only after canonical changes.

**Ordered Change Requests**

- **CR1 REFUTED as mandatory architecture.** No literal contract requires a versioned JSON receipt or runtime-owned index. Drop that necessity claim. Require contract-complete, validator-checkable evidence; select schema architecture explicitly.
- **CR2 UPHELD**, but source-digest failures must remain conditional.
- **CR3 UPHELD**, with “immutable receipt” contingent on the accepted evidence design.
- **CR4 UPHELD.**
- **CR5 UPHELD.**
- **CR6 REFUTED as written.** Distill does not require recorded proof of runtime unavailability. Drop that added obligation; retain true-subagents-when-supported, labeled fallback, and bounded anti-bias.
- **CR7 UPHELD.**

No files were modified.

### Schön, Donald

## Schön Verification

Focused check: all seven runner predicates passed against `INV-PLAN-PASS-001.expected.md`, although it contains only `Distill validation: pass; recomposition proof pass; gap count 0` and no execution trace.

1. **Role boundary: UPHELD.**<br>
Evidence: `distill/SKILL.md:83-92` requires true subagents when supported, labeled simulation otherwise, with the same trace.<br>
Correction: preserve policy; separately attest capability and selected path.

2. **Successful Distill has semantic obligations: UPHELD.**<br>
Evidence: `SKILL.md:95-128,134-142,172-185,220-245` requires finite rounds, role trace, categorized objections, techniques, reconciliation, and navigation.<br>
Correction: enforce these through executable evidence, not verdict text.

3. **Plan contract permits unsupported verdicts: UPHELD.**<br>
Evidence: `plan.md:118-126,297-298` requires Distill, but `:360-373` records only verdict/recomposition/gap count.<br>
Correction: require validator-issued execution evidence before pass/flag routing.

4. **Invoke root trusts authored outcomes: UPHELD.**<br>
Evidence: `README.md:134-144,217-218,223-231` defines routing from reported verdict without provenance validation.<br>
Correction: mutation routing must consume validator output.

5. **Fixtures admit Markdown-only false passes: UPHELD.**<br>
Evidence: runner `:347-359,513-557,640-648` uses regex presence checks. The focused predicate replay passed every relevant check against the receipt-free fixture.<br>
Correction: add valid, missing-receipt, and fabricated-receipt cases.

6. **Proposed receipt architecture kills fabricated receipts: REFUTED.**<br>
Evidence: `findings.md:67-86` requires runtime resolution only for `true-subagents`; a fabricated `role-simulation` receipt can assert unavailability, pass boundaries, rounds, objections, and techniques. Schema and semantic consistency cannot prove those events occurred.<br>
Required correction: require runtime-owned append-only execution events for both paths, including capability probe, ordered role-pass boundaries, transcript/output digests, parent run linkage, and validator recomputation. Drop any claim that labeled fallback fields alone prove execution.

7. **Conditional source digests are sufficient for mutation routing: REFUTED.**<br>
Evidence: the Workbench receipt names mutable paths without revision or digest; the same path now resolves to eleven SWUs while the receipt says five.<br>
Required correction: require recomputed content digests for every mutable reviewed artifact whenever readiness can unlock mutation. Revision/state references are acceptable only when they identify immutable content exactly.

8. **Mode-contract findings: UPHELD.**<br>
Evidence: `handoff.md:96-170` and `refresh.md:117-204` omit root-required Dispatch/conditional-Distill fields; `define.md:66-78` and `design.md:127-142,183-184` retain authored status/rationale; `full.md:7-27` and `validate.md:7-27` are deferred.<br>
Correction: compose fields/gates into active modes and fail closed as `unsupported/deferred` for deferred modes.

9. **Anti-bias bounded placement: UPHELD.**<br>
Required correction: none beyond retaining qualifying-group scope.

10. **Workbench is an enforcement false-pass: UPHELD.**<br>
Evidence: `DISTILL-VALIDATION.md:3-20` and `INVOKE-RESULT.md:11-20` assert pass and route to Task Session; focused search found no Proposer/Balancer, rounds, objections, reconciliation, or execution receipt.<br>
Correction: status becomes governance-unverified pending replay; do not invalidate the decomposition itself.

11. **Stale five-versus-eleven identity: UPHELD, with narrower wording.**<br>
Evidence: observability JSON `:33-41` records five and routes onward; `WORK-PACK.md:51-61` contains eleven. Because the receipt lacks immutable binding, it cannot identify the current package.<br>
Correction: preserve it as historical evidence, not necessarily historically false; append a digest-bound superseding receipt and recompute counts.

12. **Mirror fidelity: UPHELD.**<br>
Evidence: SHA-256 pairs match for all seven canonical/generated mode files.<br>
Correction: regenerate mirrors only after canonical fixes.



Dispatch: `2026-07-17-invoke-distill-enforcement-review`

The following attacker returns preserve each agent's initial and post-robot-talks final position.

## Abramsky, Samson

# INITIAL POSITION: Abramsky, Samson

**Verdict:** The Workbench artifacts prove that a Distill-shaped review influenced the repaired plan. They do **not** prove a contract-complete Distill execution. No preserved evidence identifies true-subagent execution or labeled role simulation.

## Findings

### F1. Distill `pass` lacks the mandatory role trace

**Severity:** High

**Evidence**

- Distill requires true Proposer/Balancer subagents when supported, otherwise labeled single-agent passes; both paths must preserve claims, evidence, categorized objections, reconciliation, and stable disagreement: [arcanum/arcana/distill/SKILL.md](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:83).
- Preserving that trace and classifying Balancer objections are explicit success requirements: [arcanum/arcana/distill/SKILL.md](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:172).
- Workbench’s validation records checks and verdicts, but no Proposer claim, Balancer objection, reconciliation, mode budget, rounds, execution path, or skipped-technique rationale: [DISTILL-VALIDATION.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/DISTILL-VALIDATION.md:3).
- The Invoke result reduces this to one label: [INVOKE-RESULT.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/INVOKE-RESULT.md:9).

**Position:** Distill may have been reasoned through informally, but “Distill executed successfully” is unproven.

**Proposed fix:** Require a Distill execution receipt before Invoke can emit `pass`, containing:

```text
mode, budget, role_execution_path,
proposer_claims, balancer_objections,
objection_categories, reconciliation,
rounds_completed, techniques_run/skipped,
verdict, source-artifact digests
```

For true subagents, also record agent handles and governed dispatch/helper lineage. For simulation, record `role_execution_path: local-role-simulation`.

---

### F2. The fixture runner validates labels and result shape, not execution

**Severity:** High

**Evidence**

- The runner accepts expected output containing `Distill validation:`: [run-validation-fixtures.sh](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:347).
- Plan checks require headings and phrases such as atomicity and narrowness, but no role trace or receipt: [run-validation-fixtures.sh](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:513).
- Integration fixtures likewise check the heading and status fields: [run-validation-fixtures.sh](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:640).
- Yet the plan contract says to “run Distill in validate mode”: [plan.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/plan.md:116).

**Proposed fix:** Add a machine-readable receipt fixture and reject `pass` when role execution path, categorized objections, reconciliation, finite rounds, or source bindings are absent. Include a negative fixture containing the current Workbench-style table to prove labels alone cannot pass.

---

### F3. Observability is a result label, not an execution trace

**Severity:** High

**Evidence**

- The initial run records `distill_validation: "pass"` but no Distill invocation, role path, rounds, or receipt: [.arcanum run receipt](/home/vrondelli/projects/domainspec-core/.arcanum/observability/runs/invoke-20260717T080501Z-workbench-ui-v1.json:24).
- It simultaneously records five SWUs: [.arcanum run receipt](/home/vrondelli/projects/domainspec-core/.arcanum/observability/runs/invoke-20260717T080501Z-workbench-ui-v1.json:33).
- Operator review later found those five units task-shaped and replaced them with eleven: [PLAN-REFRESH.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/PLAN-REFRESH.md:3).
- Distill itself recommends recording role execution path, rounds, and techniques: [.agents Distill mirror](/home/vrondelli/projects/domainspec-core/.agents/skills/distill/SKILL.md:208).

**Proposed fix:** Make Invoke observability reference a separate immutable Distill receipt by run ID and digest. Later corrections should append a superseding assessment rather than leave the original pass operationally ambiguous.

---

### F4. Callable subagents were declared, but their use is unproven

**Severity:** Medium

**Evidence**

- The installed Codex Distill package declares `Task` among allowed tools: [.agents/skills/distill/SKILL.md](/home/vrondelli/projects/domainspec-core/.agents/skills/distill/SKILL.md:1).
- The registered review context states that the runtime supported subagents: [subagents-dispatch.yaml](/home/vrondelli/projects/domainspec-core/telemetry/agents/subagents-dispatch.yaml:3461).
- Neither proves a Workbench Proposer/Balancer call occurred. No corresponding agent identity, return, dispatch/helper lineage, or execution receipt appears in the Workbench package.

**Proposed fix:** Runtime capability detection and actual invocation must be separate receipt fields: `subagents_available`, `role_execution_path`, and `agent_receipts`.

## Surviving Targets

- **Canonical/generated fidelity: zero findings.** The generated plan mirror is byte-identical to canonical; the root mirror differs only by generated-runtime frontmatter. Its ownership metadata is explicit: [.agents/skills/invoke/SKILL.md](/home/vrondelli/projects/domainspec-core/.agents/skills/invoke/SKILL.md:1).
- **Workbench repaired SWU structure: zero findings under this lens.** The eleven units have independent acceptance and retained-boundary rationale: [WORK-PACK.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/WORK-PACK.md:47). This supports the repaired decomposition, not the missing Distill execution proof.
- **Anti-bias contract: zero findings.** It applies to `n >= 2` investigate/evaluate subject groups, not universally to every Proposer/Balancer pass: [anti-bias-vector-composition/SKILL.md](/home/vrondelli/projects/domainspec-core/.claude/skills/anti-bias-vector-composition/SKILL.md:27). A true multi-agent Distill fan-out may trigger dispatch governance, but local role simulation does not become an anti-bias subject group merely by using two labels.
- **Subagent strategy/check-tension/register contracts: zero internal findings.** Their lifecycle and applicability are explicit: [domainspec-subagents-strategy/SKILL.md](/home/vrondelli/projects/domainspec-core/.claude/skills/domainspec-subagents-strategy/SKILL.md:10), [check-tension/SKILL.md](/home/vrondelli/projects/domainspec-core/.claude/skills/check-tension/SKILL.md:14). The defect is absent Workbench evidence selecting and completing either permitted Distill execution path.

# FINAL POSITION: Abramsky, Samson

## Changed View

I now separate two defects that my initial position treated too closely:

1. **Execution-proof defect:** Invoke can claim Distill pass without proving either permitted execution path.
2. **Mode-contract defect:** a receipt cannot repair missing or contradictory obligations in `handoff`, `refresh`, deferred `full`, or deferred `validate`.

I also narrow the proposed receipt. Source digests and agent receipts should be conditional, not universal.

## Highest-Severity Findings

**HIGH: Distill pass is not execution-backed.**<br>
Workbench preserves a useful repaired decomposition, but no role execution path, Proposer/Balancer trace, objection categories, reconciliation, rounds, or Distill invocation receipt. This violates Distill’s common trace contract regardless of whether execution used subagents or role simulation.

**HIGH: Fixtures admit Markdown-only false passes.**<br>
The runner checks headings, labels, and selected phrases. Workbench demonstrates that structurally complete Markdown can pass while the supposedly smallest units remain task-shaped. Positive and negative receipt fixtures are required.

**HIGH: Root/mode contract incoherence cannot be solved by receipts.**<br>
The root says every mode records Dispatch technique trace and conditionally runs Distill, while `handoff` and `refresh` do not fully expose those fields. `full` and `validate` are presented as mandatory-mode participants while remaining deferred. A receipt validator cannot infer obligations that mode contracts do not encode.

## Minimal Enforcement Architecture

1. **Mode capability table**

   Make each mode explicitly declare:

   ```text
   implementation_status
   dispatch_trace: required | conditional | unavailable
   distill: required | conditional | unavailable
   mutation_handoff_allowed
   ```

   Deferred modes must return `unavailable`, not advertise a runnable mandatory path.

2. **Small Distill receipt**

   Required whenever Distill actually runs:

   ```text
   schema_version
   invoke_run_id
   mode
   role_execution_path: true-subagents | role-simulation
   target_evidence_refs
   distill_mode
   rounds_budget / rounds_completed
   role_trace
   techniques_run / skipped_with_reason
   verdict
   ```

   `role_trace` must contain Balancer objections, categories, and reconciliation. Proposer entries may be absent in Validate mode when no repair is attempted.

3. **Conditional provenance**

   - True-subagent path: require agent handles and dispatch/helper lineage.
   - Role simulation: require labeled pass boundaries, not fake agent identities.
   - Source digests: require only where immutable source binding is needed or available; otherwise paths plus revision/state references suffice.

4. **Executable validator**

   Invoke pass requires:

   - mode contract says Distill is runnable and required/triggered;
   - receipt schema passes;
   - receipt verdict agrees with the Invoke result;
   - referenced artifacts exist;
   - a flag has owned repair routes;
   - a block cannot route to mutation.

5. **Fixture pair**

   - Positive: valid receipt plus matching Markdown projection.
   - Negative: current Workbench-style `Distill validation: pass` and table, but no receipt. It must fail.

## Rejected Claims

- **Receipt alone repairs Invoke:** rejected. It proves execution only after mode contracts consistently define when execution is required and possible.
- **One heavyweight receipt for every mode:** rejected as over-specified.
- **True subagents are universally mandatory:** rejected. Distill explicitly permits role simulation when unavailable.
- **`allowed-tools: Task` proves subagents were callable during Workbench:** rejected. It proves package declaration, not runtime availability or invocation.
- **Blanket anti-bias/check-tension enforcement:** rejected. Those rules remain bounded to governed subject groups; simulated Proposer/Balancer labels do not automatically create such a group.
- **Canonical/generated drift caused the failure:** rejected. The reviewed mirrors are synchronized; the weakness is shared contract and validator behavior.

## Stable Disagreement

No substantive disagreement remains among the three attackers. The only unresolved evidentiary point is historical runtime availability: the repository and review row declare subagent support, but Workbench left no runtime receipt proving availability or use. The defensible conclusion is therefore **execution path unknown**, not “subagents definitely ran” or “subagents were unavailable.”

## Ashby, W. Ross

## INITIAL POSITION

Invoke’s prose contract requires Distill, but its evidence contract does not prove Distill executed. A verdict label can currently substitute for the Proposer/Balancer process, role trace, rounds, and runtime receipt.

### Mode Matrix

| Mode | Dispatch | Distill | Enforcement position |
|---|---|---|---|
| `define` | Required | Conditional; may record `not required` | Contract present; no execution proof |
| `design` | Required | Required after draft exists | Contract present; no execution proof |
| `plan` | Required | Automatic Validate pass | Strong content gates; role execution unproved |
| `handoff` | Root-required | Conditional | Mode contract omits both fields/gates |
| `refresh` | Root-required | Conditional | Mode contract omits both fields/gates |
| `full` | Required | Automatic | Deferred; no executable contract |
| `validate` | Required | Automatic | Deferred; no executable contract |

### Findings

1. **High: Distill pass is not evidence of a valid Distill execution.**<br>
   Distill requires true Proposer/Balancer subagents when available and the same role trace under fallback ([Distill](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:83)); its quality bar requires preserved role trace and classified objections ([Distill](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:172)). Invoke only requires verdict, gap summary, and recomposition status ([Invoke root](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:217)). Plan likewise says “run Distill” and lists inspected properties, but requires no role or runtime receipt ([plan.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/plan.md:116)).<br>
   **Proposed fix:** Define a Distill execution receipt containing mode/budget, runtime path (`subagent` or labeled fallback), Proposer and Balancer identities, role trace, rounds, technique trace, reconciliation, and verdict. Block Invoke readiness when required receipt fields are absent.

2. **High: The fixture runner admits label-only false passes.**<br>
   Generic fixtures only search expected Markdown for `Dispatch techniques:` and `Distill validation:` ([runner](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:337)). Plan validation similarly checks headings and asserted strings such as atomicity/pass, not a Distill receipt or role trace ([runner](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:505)).<br>
   **Proposed fix:** Add positive and negative receipt fixtures. Reject `Distill validation: pass` without role trace, runtime path, budget/round accounting, always-on technique evidence, and reconciliation.

3. **High: Workbench UI’s repaired pass remains structurally asserted, not process-proven.**<br>
   `DISTILL-VALIDATION.md` records checks and verdict but no Proposer/Balancer trace or receipt ([DISTILL-VALIDATION.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/DISTILL-VALIDATION.md:3)). `INVOKE-RESULT.md` repeats the pass and routes directly to Task Session ([INVOKE-RESULT.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/INVOKE-RESULT.md:9)). No matching Workbench UI invocation was found in the inspected Invoke observability index.<br>
   **Proposed fix:** Downgrade this pass to `unverified` until replayed through Distill with a receipt. Do not infer that the eleven SWUs are wrong; the evidence only fails to prove the required review process.

4. **Medium: `handoff` and `refresh` contradict root governance.**<br>
   Root says every mode must carry a Dispatch trace and conditionally Distill broad `handoff`/`refresh` outputs ([Invoke root](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:117), [Invoke root](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:144)). Their mode gates and output shapes omit both obligations ([handoff.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/handoff.md:111), [refresh.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/refresh.md:133)).<br>
   **Proposed fix:** Add mode-local trace fields, conditional Distill trigger/skip rationale, and pass-blocking gates.

5. **Medium: `full` and `validate` are named as mandatory Distill modes while remaining non-executable.**<br>
   Root imposes artifacts and automatic Distill on both ([Invoke root](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:223)), but their files contain only deferred drafts ([full.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/full.md:7), [validate.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/validate.md:7)).<br>
   **Proposed fix:** Fail closed at routing: deferred modes must return `unsupported/deferred`, never a lifecycle verdict.

6. **Low: Anti-bias enforcement must remain bounded.**<br>
   Anti-bias applies only to `n >= 2` investigate/evaluate subject groups, not single writers or auditors ([anti-bias](/home/vrondelli/projects/domainspec-core/.claude/skills/anti-bias-vector-composition/SKILL.md:27)); `check-tension` is initialization-only and explicitly has no post-dispatch realization check ([check-tension](/home/vrondelli/projects/domainspec-core/.claude/skills/check-tension/SKILL.md:8)).<br>
   **Proposed fix:** Require anti-bias only when Invoke creates a qualifying multi-agent dispatch. Do not make it a universal Distill-pass requirement; Proposer/Balancer role separation is the broader obligation.

### Defended Zero-Findings

- **Canonical/generated mode mirrors:** all seven per-mode files are byte-identical by SHA-256; no mirror drift found.
- **Dispatch registration:** the review row is present with the correct review goal, three tensioned attackers, synthesis, verification, and audit stages ([ledger](/home/vrondelli/projects/domainspec-core/telemetry/agents/subagents-dispatch.yaml:3456)).
- **Public/private authority:** no recommendation requires private DomainSpec or Saturn prose to enter public `arcanum/`; enforcement belongs in public Invoke/Distill contracts and generated mirrors.
- **Anti-bias contract:** internally coherent within its declared subject-group scope; the defect is overextension risk, not a defect in that scope.

## FINAL POSITION

The confrontation strengthens the root-cause finding: this is not primarily a prose defect. Invoke can describe the correct Distill behavior while its validation and observability surfaces accept an unsupported verdict.

### Changed Position

I now make the machine-readable execution receipt the primary fix, not merely one proposed fix. Prose changes are necessary to define the obligation, but prose cannot prove execution. Proof requires a runtime-produced receipt tied to the exact reviewed inputs.

I also strengthen the Workbench finding: it is the concrete false-pass witness. Its repair may be substantively good, but the preserved evidence proves only a Distill-shaped analysis, not contract-complete Distill execution ([DISTILL-VALIDATION.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/DISTILL-VALIDATION.md:3), [INVOKE-RESULT.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/INVOKE-RESULT.md:9)).

### Rejected Claims

- **Reject blanket anti-bias enforcement.** Anti-bias applies to qualifying multi-agent investigate/evaluate groups, not every Invoke or Distill run ([anti-bias](/home/vrondelli/projects/domainspec-core/.claude/skills/anti-bias-vector-composition/SKILL.md:27)). Distill’s Proposer/Balancer separation is the relevant universal role obligation; dispatch anti-bias is conditional.
- **Reject “mirrors caused the failure.”** The per-mode canonical and generated files are byte-identical. Synchronized prose can still share the same enforcement hole.
- **Reject treating Workbench’s SWUs as substantively disproven.** The missing execution proof invalidates the claimed Distill pass, not necessarily the repaired decomposition.
- **Reject implementing `full` and `validate` in this remediation.** Their lifecycle implementation is larger work and lacks mature activation evidence. Only fail-closed routing belongs in this change.

### Surviving Findings

1. **Critical: Invoke accepts a Distill verdict without execution proof.**<br>
   Distill requires true subagents when available, labeled fallback otherwise, and preserved Proposer/Balancer trace ([Distill](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:83)). Invoke records only verdict, gaps, and recomposition status ([Invoke](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:217)).

2. **Critical: Fixture validation is structurally gameable.**<br>
   The runner checks Markdown patterns such as `Distill validation:` and expected headings; it does not validate execution evidence ([runner](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:337), [runner](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:505)).

3. **High: Workbench is a concrete admitted false-pass.**<br>
   It routes to mutation-capable Task Session after asserting Distill pass, while preserving no role path, role trace, rounds, techniques, or agent receipts.

4. **High: `handoff` and `refresh` fail to project root gates.**<br>
   Root requires a Dispatch trace for every mode and conditional Distill for broad outputs ([Invoke](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:117), [Invoke](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/README.md:144)); the mode-local output contracts omit those fields.

5. **Medium: Deferred modes are exposed ambiguously.**<br>
   `full` and `validate` are deferred ([full.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/full.md:7), [validate.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/validate.md:7)), while root governance describes their eventual mandatory artifacts and Distill behavior.

### Minimal Enforcement Architecture

1. Define one versioned `DistillExecutionReceipt` schema containing:
   - Distill mode and budget;
   - reviewed artifact paths plus content digests;
   - runtime path: true subagents or labeled fallback;
   - Proposer/Balancer identities and receipts;
   - role trace and objection categories;
   - rounds performed and termination reason;
   - activated/skipped techniques;
   - reconciliation and stable disagreements;
   - verdict, gaps, recomposition result, and next route.

2. Make Invoke require and schema-validate that receipt whenever Distill is required. A verdict without a valid receipt blocks mutation-capable handoff.

3. Add positive and negative fixtures. At minimum, reject missing role trace, missing input digests, fabricated pass labels, insufficient rounds for the selected budget, and unavailable agent receipts when the runtime path claims subagents.

4. Add Dispatch and conditional-Distill fields to `handoff` and `refresh`.

5. Make `full` and `validate` return an explicit deferred/unsupported result before lifecycle processing. Their actual implementation remains separate work.

6. Replay Workbench through the new enforcement path; do not grandfather its current pass.

### Stable Disagreement

Source digests are not literal obligations in the current Distill prose, so they cannot be cited as an already-violated Distill rule. I nevertheless retain them as a new receipt requirement: without artifact identity, a valid role trace still cannot prove which plan was reviewed.

Likewise, native agent-specific receipts may vary by runtime. The invariant should be evidence of distinct role execution; the schema should allow either native subagent receipt references or an explicit labeled-fallback trace, never an unqualified verdict.

## Shannon, Claude

**INITIAL POSITION**

**Finding 1: Distill fixture validation is label-presence validation, not execution validation**

- **Severity:** Critical
- **Exploit:** An expected Markdown file containing `Distill validation: pass` satisfies the runner without any Proposer pass, Balancer pass, recursive round, objection category, technique trace, or receipt. The runner only applies `rg` predicates for the labels at [run-validation-fixtures.sh](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/run-validation-fixtures.sh:337), especially lines 347-359. Its stronger plan fixture still checks authored headings and prose at lines 513-557.
- **Proof mismatch:** Distill mandates true subagents when available and a preserved role trace at [SKILL.md](/home/vrondelli/projects/domainspec-core/arcanum/arcana/distill/SKILL.md:83), recursive rounds and named techniques at lines 95-128, a technique activation trace at lines 131-143, and those fields in its output contract at lines 220-245. Current passing fixtures provide only a verdict sentence, for example [INV-PLAN-PASS-001.expected.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/development/fixtures/INV-PLAN-PASS-001.expected.md:14).
- **Smallest executable fix:** Require a referenced JSON Distill receipt for every applicable pass/flag. Validate nonempty `mode`, `round_budget`, `rounds_completed`, `role_execution_path`, `proposer_receipt`, `balancer_receipt`, `role_trace`, `technique_trace`, `recomposition`, and `verdict`. When `role_execution_path=true_subagents`, require distinct nonempty invocation IDs for Proposer and Balancer. Reject Markdown-only assertions.

**Finding 2: Workbench UI V1 demonstrates the false-pass path**

- **Severity:** Critical
- **Exploit:** [DISTILL-VALIDATION.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/DISTILL-VALIDATION.md:3) declares pass through a self-authored check table at lines 9-20. It has no role trace, rounds, objection categories, technique activation trace, skipped-technique reasons, or execution receipt. Nevertheless, [INVOKE-RESULT.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/INVOKE-RESULT.md:11) declares Distill pass and routes to Task Session at line 20; [WORK-PACK.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/WORK-PACK.md:8) repeats pass statuses.
- **Corroborating inconsistency:** The observability record merely repeats `"distill_validation": "pass"` and routes onward at [invoke-20260717T080501Z-workbench-ui-v1.json](/home/vrondelli/projects/domainspec-core/.arcanum/observability/runs/invoke-20260717T080501Z-workbench-ui-v1.json:33). It reports `swu_count: 5` at line 36 while the repaired work-pack contains eleven SWUs at [WORK-PACK.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/workbench-ui-v1/WORK-PACK.md:47). Observability therefore neither proves Distill execution nor accurately receipts the repaired result.
- **Smallest executable fix:** Treat this package’s Distill status as unproven and block mutation handoff until a new receipt validates against the proposed schema and hashes/references the eleven-SWU artifact.

**Finding 3: Invoke contracts require verdicts but do not require proof**

- **Severity:** High
- **Exploit:** Plan says automatic Distill validation is mandatory at [plan.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/plan.md:297), but its output contract asks only for verdict, recomposition status, and gap count at line 373. Design requires a check and rationale at [design.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/design.md:127), while define similarly records only status/rationale at [define.md](/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/define.md:67). Thus Invoke can satisfy its literal local contract while violating Distill’s execution contract.
- **Smallest executable fix:** Add `Distill receipt: <path>` and `Distill execution path: true-subagents | role-simulation | not-applicable` to each applicable mode output. A pass/flag must fail closed when the receipt is absent or structurally invalid. `not-applicable` should remain allowed only for the bounded define applicability case, with a recorded reason.

**Defended Zero Findings**

- **Generated Invoke mirrors:** No canonical/generated drift found for the inspected `README`, `define`, `design`, and `plan` files. Mirror fidelity does not cause this failure; both surfaces preserve the same under-enforced contract.
- **Anti-bias vector composition:** No finding. Its scope is explicitly limited to `n >= 2` investigate/evaluate dispatch groups at [SKILL.md](/home/vrondelli/projects/domainspec-core/.claude/skills/anti-bias-vector-composition/SKILL.md:27). Extending its pairwise anti-bias rules universally to Distill’s Proposer/Balancer pair would overshoot the proof. Distill needs role opposition and receipts, not necessarily dispatch-group anti-bias vectors.
- **Dispatch governance:** No finding against registration/tension contracts for this exploit. The registered review row correctly records this investigation at [subagents-dispatch.yaml](/home/vrondelli/projects/domainspec-core/telemetry/agents/subagents-dispatch.yaml:3456). It proves the present review dispatch exists; it cannot retroactively prove the earlier Distill execution.

**FINAL POSITION**

**Changed From Initial View**

I strengthen my initial receipt proposal: a schema-valid JSON receipt is insufficient. Invoke can fabricate the same claims in JSON that it currently fabricates in Markdown. Receipt validation must establish provenance and cross-artifact consistency, not merely field presence.

I also adopt the governance finding that `handoff` and `refresh` omit the root Invoke result fields for Dispatch and conditional Distill status. That is a contract-composition defect, separate from the Workbench false-pass.

**Rejected**

- **Blanket anti-bias enforcement:** Rejected. Dispatch pairwise-tension rules apply to multi-agent investigate/evaluate groups, not automatically to Distill’s Proposer/Balancer roles. Distill needs genuine role separation and categorized opposition, but not the dispatch anti-bias vocabulary.
- **“Workbench proves Distill did not run”:** Too strong. It proves no contract-complete execution was preserved. A Distill-shaped reasoning process may have occurred, but the artifacts cannot substantiate it.
- **Schema-only receipt enforcement:** Rejected as gameable. A model can emit plausible role names, round counts, techniques, and invented receipt IDs.

**Surviving Findings**

1. **Critical: Invoke can claim Distill pass without executable proof.**<br>
   The fixture runner checks labels and headings, while Workbench supplies exactly those labels without role, round, technique, or agent evidence. Mutation-capable handoff follows from an unproven verdict.

2. **Critical: Observability repeats claims instead of attesting execution.**<br>
   The Workbench record says Distill passed but contains no role path or runtime receipt references. Its stale five-SWU count against the repaired eleven-SWU package further shows that it is not a reliable execution receipt.

3. **High: Mode contracts under-specify Distill evidence.**<br>
   Define, design, and plan request status/rationale rather than a validated execution reference. Handoff and refresh do not consistently preserve even those root fields. Full and validate remain deferred, so root documentation must not imply that they currently provide enforceable end-to-end guarantees.

**Minimal Enforcement Architecture**

1. **Runtime stage envelope**<br>
   Record `run_id`, mode, runtime capability availability, role path, source artifact paths and recomputed digests, round budget/completion, verdict, and receipt references.

2. **Independent role receipts**<br>
   Proposer and Balancer receipts must be runtime-emitted or indexed by a runtime-owned invocation ledger. For true-subagent execution, require distinct invocation IDs, role outputs, timestamps, and parent `run_id`. A self-authored path or arbitrary UUID is not evidence.

3. **Semantic validator**<br>
   Validate more than schema:
   - `pass` requires completed finite rounds.
   - Proposer and Balancer IDs differ.
   - Every Balancer objection has a named category and reconciliation.
   - Required techniques have traces; skipped techniques have reasons.
   - Referenced artifacts exist and their digests are recomputed.
   - Receipt verdict, Invoke result, observability row, and work-pack counts agree.
   - `true_subagents` must resolve against runtime evidence.
   - `role_simulation` is allowed only with recorded runtime unavailability.

4. **Handoff gate**<br>
   Mutation-capable routing consumes the validator result, not the authored `Distill validation: pass` label. Missing, stale, inconsistent, or unverifiable receipts block.

**Minimum Executable Negative Proof**

The minimum meaningful negative fixture is not “missing receipt”; that only proves required-field checking. Use an adversarial fixture that looks complete:

- Markdown declares Distill pass.
- JSON contains every required field.
- Proposer and Balancer use the same invocation ID or IDs absent from the runtime ledger.
- It claims two rounds and all techniques.
- One source digest is fabricated or stale.
- Expected result: `block`, with provenance, role-separation, and digest failures.

Pair it with one valid positive fixture using two resolvable role receipts. If the adversarial receipt passes, the enforcement remains cosmetic.

**Stable Disagreement**

None among the three lenses on root cause or scope. The remaining epistemic boundary is wording: current evidence supports “contract-complete Distill execution is unproven,” not “Distill definitely never ran.”
## Final Verifier Convergence

### Schon

NO OBJECTION

- Both execution paths now require runtime-owned events; labeled fallback fields alone are explicitly insufficient.
- Mutation-capable inputs now require exact immutable-content identity, closing the mutable-path and stale-count gap.
- Historical five-SWU evidence is correctly preserved without claiming its original count was false.

### Rittel

OBJECTION

**Remaining claim:** “Mutation-capable readiness nevertheless requires exact immutable-content identity for every mutable reviewed artifact.”

**Evidence:** `attacks.md` states source digests are not literal Distill obligations and that paths plus revision/state references may suffice. The revised claim turns one proposed provenance mechanism into mandatory law.

**Required narrowing:** Treat exact immutable-content identity as a lifecycle-approved strengthening, not current contract-derived evidence. Require reviewed-input provenance sufficient for the accepted validator design.
