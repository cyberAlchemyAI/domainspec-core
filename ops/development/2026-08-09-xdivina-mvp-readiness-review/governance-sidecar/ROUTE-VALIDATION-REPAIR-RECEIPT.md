# Route Validation Repair Receipt

- Status: governance-only repair proposal; no repair has been applied
- Authority effect: none
- Affected edge: Dispatch Spec validation before tension, confirmation, registration, or execution
- Frozen material strategy: `dispatch-sheet.json`
- Frozen sheet SHA-256: `45e8a24dfd22ba12bed09b66c0de8495fd51823bf7dea2a2a8f2298b647eecb2`

## Root cause

The route mixes artifact flow with the stricter capability-bound receipt flow required by the live validator:

1. `subagent_strategy.receipt_requirements` omits `capability_target`, `capability_mode`, `wave_id`, and `write_scope`.
2. Role `output_refs` are required to be step outputs of kind `receipt`. The attacker receipt directory is absent from step 1 outputs, and `findings.md` is typed only as an artifact in step 2.
3. Role dependencies must intersect through both a role `input_ref` and an applied-step input of kind `receipt`. The attacker-to-synthesizer, synthesizer-to-verifier, and verifier-to-auditor edges do not all do that.
4. Some role `input_refs` are not present on their applied steps: the synthesizer's Inventory packet, the verifier's corpus manifest, and the auditor's attacks and verifier receipts.
5. The corpus manifest's two closing rule lines are un-commented, so a line-oriented checker treats them as target paths.

The remaining diagnostics are flags rather than blocks: `ux-evidence-validator` is absent from the validator's hard-coded canonical capability set; waves 1 and 3 each contain one role even though their role has multiple agents; and the route cites no technique.

## Affected invariant

Capability-bound delegation requires every declared role receipt to be produced as a receipt by its applied step, every dependency receipt to be consumed as a receipt by the dependent step, and every declared role input to exist on that step. Acceptance-critical corpus checking must distinguish path records from explanatory prose. Validation failure must stop the route before tension, human confirmation, ledger registration, or spawning.

## Minimal repair proposal

Apply only these field-level changes to `DISPATCH-ROUTE.json`:

1. Add top-level `techniques: ["role_projection_boundary"]`. This names the already-present role projection boundary and removes the no-techniques flag without changing execution.
2. Append these four strings to `/subagent_strategy/receipt_requirements`: `capability_target`, `capability_mode`, `wave_id`, and `write_scope`.
3. At `/steps/s1-attack-current-mvp/outputs`, add:

   ~~~json
   {"kind":"receipt","ref":"ops/development/2026-08-09-xdivina-mvp-readiness-review/receipts/attackers/"}
   ~~~

4. At `/subagent_strategy/roles/change-request-synthesizer/input_refs`, add the same attacker receipt directory.
5. At `/steps/s2-synthesize-change-requests/inputs`, add:

   ~~~json
   {"kind":"receipt","ref":"ops/development/2026-08-09-xdivina-mvp-readiness-review/receipts/attackers/"}
   {"kind":"artifact","ref":"ops/development/2026-08-09-xdivina-mvp-readiness-review/strategy-inventory-packet.json"}
   ~~~

6. At `/steps/s2-synthesize-change-requests/outputs`, change the existing `findings.md` entry's `kind` from `artifact` to `receipt`. Do not change its path or the step's `evidence_artifact`; the existing receipt manifest already treats `findings.md` as `r-synthesizer`.
7. At `/steps/s3-verify-findings/inputs`, change the existing `findings.md` input's `kind` from `artifact` to `receipt`, and add:

   ~~~json
   {"kind":"artifact","ref":"ops/development/2026-08-09-xdivina-mvp-readiness-review/review-corpus.txt"}
   ~~~

8. At `/steps/s4-audit-coverage/inputs`, add:

   ~~~json
   {"kind":"artifact","ref":"ops/development/2026-08-09-xdivina-mvp-readiness-review/attacks.md"}
   {"kind":"receipt","ref":"ops/development/2026-08-09-xdivina-mvp-readiness-review/receipts/verifiers/"}
   ~~~

Apply only these two line edits to `review-corpus.txt`:

~~~text
# Resolve these paths only from the pinned commit. Every attacker reads the whole
# resolved corpus. Missing paths, target drift, or a dirty target block execution.
~~~

Do not alter the sheet, lanes, agents, prompts, corpus path list, gates, authorization, target commit, product bytes, or ledger. Leave the two single-role parallel-wave flags and the noncanonical-capability flag visible for this validation iteration; they are non-blocking and changing them without owner evidence would distort the admitted strategy. The expected immediate result is therefore `VALIDATION=flag` with no `BLOCK`. If `role_projection_boundary` is unexpectedly absent from the live technique catalog, treat that as validator iteration residue and select an already-catalogued receipt-boundary technique without changing route behavior.

## Changed-byte inventory

Actual bytes changed by this sidecar:

- Created only `ops/development/2026-08-09-xdivina-mvp-readiness-review/governance-sidecar/ROUTE-VALIDATION-REPAIR-RECEIPT.md`.
- `DISPATCH-ROUTE.json`, `review-corpus.txt`, and `dispatch-sheet.json` were not edited.

Proposed repair bytes:

- `DISPATCH-ROUTE.json`: one top-level technique entry; four receipt-requirement strings; one attacker receipt output; one synthesizer role input; two synthesizer step inputs; two `kind` substitutions for `findings.md`; one verifier corpus input; and two auditor inputs.
- `review-corpus.txt`: prefix exactly lines 72 and 73 with `# `; the target-path list remains byte-for-byte unchanged.
- No other file is in scope.

## Required revalidation

Run each command independently and preserve its exit status:

~~~sh
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py ops/development/2026-08-09-xdivina-mvp-readiness-review/DISPATCH-ROUTE.json
~~~

Expected: no `BLOCK`; `VALIDATION=flag` is acceptable only for the two single-role/multi-agent parallel-wave notices and the evidence-visible `ux-evidence-validator` canonicality notice.

~~~sh
sha256sum ops/development/2026-08-09-xdivina-mvp-readiness-review/dispatch-sheet.json
node implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs --validate-sheet ops/development/2026-08-09-xdivina-mvp-readiness-review/dispatch-sheet.json
~~~

Expected: `45e8a24dfd22ba12bed09b66c0de8495fd51823bf7dea2a2a8f2298b647eecb2`, `SHEET_VALIDATION=pass`, `SCHEMA_VERSION=0.8.0`, and `LEDGER_MUTATION=none`.

Rerun the existing corpus resolver/checker against the corrected manifest. It must skip blank lines, comments, and the three metadata records; every remaining line must resolve at the pinned commit, and any miss must preserve a nonzero exit.

After those checks pass, rerun both independent check-tension reviews against the unchanged admitted sheet digest. Do not register or spawn before the normal explicit human confirmation.

## Owner acceptance

No renewed acceptance is required solely for this repair because no prior dispatch confirmation has been bound and the acceptance-bound sheet bytes remain unchanged. The normal first explicit confirmation is still required after Dispatch Spec reaches pass/flag, both tension checks return PASS/PASS, and the parent presents the ready proposal. If evidence shows that an earlier human confirmation bound either route or corpus bytes, this conclusion is void: regenerate the candidate inventory/digests and request renewed exact-byte acceptance.

## Permanent workflow regression fix

Add a pre-confirmation fixture test that materializes a capability-bound route from the dispatch template and asserts all three edges: role `output_ref` to step receipt output, dependency `output_ref` to dependent role `input_ref`, and dependent role `input_ref` to step receipt input. The same test should require all capability-bound receipt fields and verify corpus prose is explicitly commented or structurally typed.

Separately, make the validator count agent instances, not only role IDs, before flagging a parallel wave, and source canonical capability IDs from the owned capability registry rather than a hard-coded subset. Those validator changes require their own owner-reviewed candidate and must not be folded into this route repair.
