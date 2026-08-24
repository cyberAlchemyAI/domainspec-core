# audit.md — final approval (parent fallback)

**Auditor stage did not run.** Agent "Brandenburg, Martin" terminated on an API session
limit before producing a verdict. Per the research type owner, `parent` is the declared
`final_approver` and the fallback when the auditor group never runs, so this approval is
mine.

**Stated weakness, not a caveat to skip:** a parent audit is structurally weaker than the
independent one the sheet designed for. I wrote the agent prompts, shaped the revision
instructions, and supplied several of the parent-verified corrections the record now
carries. I am checking work I influenced. The independent audit is owed and unpaid.

## Check 1 — closure obligations applied: PASS

| Required | In `findings.md` |
| --- | --- |
| `properties.lifecycle_status` line 44, not `$defs...` | present 1×; `$defs.lifecycle_status` 0× |
| `PACKAGE-MODEL.md:51`, not `:50` | `:51` present; `:50` absent |
| `AUTHORITY-KINDS.md:34` for `kind.evidence`, not `:33` | `:34` present; `:32` used correctly for `kind.runtime_contract` |

## Check 2 — dereference sample: 7 of 8 PASS, 1 FAIL

| Selector | Resolves | Found |
| --- | --- | --- |
| `AUTHORITY-KINDS.md:32` | yes | `kind.runtime_contract` \| task-session after owner gates |
| `AUTHORITY-KINDS.md:34` | yes | `kind.evidence` \| source/inventory owner |
| `LIFECYCLE-MODEL.md:31` | yes | `active` \| Owner route promoted the artifact |
| `NODE-MODEL.md:18` | yes | `concept_id` \| Local stable identifier |
| `grounding.mjs:13` | yes | `export function evaluateGrounding(graph)` |
| `candidate-v1.mjs:109` | yes | `function validateAuthorityEffect(...)` |
| `candidate-v1.mjs:80` | yes | `function exactFields(...)` |
| **`AUTHORITY-KINDS.md:28`** (cited for decision-gate eligibility) | **no** | line 28 is `kind.constitution`; `kind.decision` \| decision-gate is at **line 30** |

**D6 — sixth selector defect.** Claim true (decision-gate owns `kind.decision`), address wrong
by two lines. Corrected selector of record: `AUTHORITY-KINDS.md:30`. Not routed to a writer
revision: the claim is unaffected and the correction is recorded here as parent-verified.

## Check 3 — no claim exceeds its evidence: PASS

Every `executed` row in §2 and §3 names a mutation (M1, M9, M10, M13, M15, M3, M4, M5, M7,
M11, M12, M14) and an observed failure count. D4 correctly reports "no mutation needed — the
property is absent" rather than inventing one. `unverified` rows are typed as such and none is
upgraded.

## Check 4 — objections preserved unrepaired: PASS

NV-O5/O6, NV-O1 on S1, AU-O2, AU-O3 second point all appear in §8 under "unrepaired", with
AU-O2 explicitly qualified as "repaired only in direction". S1 is carried as a third status,
`untested`, rather than collapsed into either existing bucket. Wording does not soften them.

## Check 5 — headline survived: PASS

"There is no first version" appears as the §1 heading and is restated in the direct answer.
No hedge, no "partially ready", no "foundation exists". The writer additionally recorded a
discrepancy in its own input — the synthesis said four declared properties, its table listed
five — and adopted five, the worse reading.

## Check 6 — ceiling stated and unlifted: PASS

§9 states the ceiling and names what is *not* an owner act: the `kind.evidence` proposal, the
label, the A-steps. `ontology-authority-not-granted` and `runtime-implementation-not-authorized`
carried through. No gate lifted, nothing promoted.

## Verdict

```text
VERDICT: FLAG
```

One row to repair: `AUTHORITY-KINDS.md:28` → `:30`. Corrected here rather than spent on a
revision. The record is otherwise sound and I found nothing else wrong across six checks —
stating that plainly, since an audit reporting only problems is as untrustworthy as one
reporting none.

**Owed:** an independent audit of this record by an agent that did not participate in producing it.
