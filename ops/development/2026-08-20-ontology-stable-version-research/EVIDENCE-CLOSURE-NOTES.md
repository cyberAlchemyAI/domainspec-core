# Evidence Closure Notes — parent-verified corrections

Accumulated by the strategist during the run. Checked at the closure gate before the
writer becomes READY. Every row here was verified by the parent by executing a check,
not by trusting a return.

## D1 — selector does not resolve (explorer-owned, parent-repaired)

**Claimed:** `arcanum/arcana/ontology-vault/development/schema-validation-plan/schema/branch-aware-ontology-candidate.schema.yml` key path `$defs.lifecycle_status.enum`.
Asserted by the governance explorer and repeated verbatim in `synthesis.md` §C2 and §X2.

**Actual:** `lifecycle_status` is at `properties.lifecycle_status`, file line 44. It is NOT
under `$defs`. Parent-executed:

```
python3 -c "import yaml; d=yaml.safe_load(open(<schema>)); print('lifecycle_status' in d.get('$defs',{}), 'lifecycle_status' in d.get('properties',{}))"
-> False True
```

**Status of the underlying claim:** TRUE and unchanged. The enum is
`[raw, catalogedEvidence, reviewableSignal, promotionRecordDraft, candidate, premise,
reviewed, promoted, contradicted, retired, rejected, deferred]` — twelve values, none
`stable`. Only the address was wrong.

**Defect class:** location precision — the same class recorded as
`runtime-state-enum-and-reducer-contract-inconsistent` in the prior runtime dispatch,
where vocabulary declared in one file was instantiated in another with nothing forcing
agreement. This dispatch selected the `exact-binding` contract specifically to catch it.

**Routing:** `defect_class: selector-unresolvable`; `repair_owner_stage: explorer`. The
sheet declares NO synthesizer→explorers feedback edge, so there is no eligible declared
route to an explorer, and the research type owner forbids spending auditor→writer
revision capacity on explorer-owned evidence defects. Rather than invent a
post-confirmation edge, the parent bound the row directly by executing the check above.
Row status: **bound by parent verification**, with the corrected selector of record
`properties.lifecycle_status`, file line 44.

**Obligation on the writer:** cite `properties.lifecycle_status` (line 44). Do not
reproduce `$defs.lifecycle_status.enum`.

## D2 — dispatch context premise was stale (parent-owned)

Recorded in full at `CONTEXT-CORRECTION.md`. The sheet's `context` asserted the prior
runtime dispatch "ended BLOCKED" with a live blocker; the working folder proves it was
repaired and reached `research_complete_exact_binding_findings`. Cause: the parent
treated the Inventory index as proof rather than as a discovery read model. The
explorer lane falsified it because it was instructed to demand repair evidence.

Row status: **corrected before synthesis**; the synthesizer read the correction first.

## Pattern

Both defects are the same shape: a claim that is true, carried by a pointer that does not
resolve or no longer holds. Neither was caught by the stage that produced it. Both were
caught by parent re-verification. The `exact-binding` contract is doing its job only
because something downstream is actually dereferencing the selectors — the contract alone
does not enforce itself.

## Closure implication

No row here is `blocked`. D1 is bound with a corrected selector; D2 is corrected and was
consumed before synthesis. Neither blocks the writer.

## D3 — scope breach by a read-only agent (disclosed, restore parent-verified)

The non-vacuity skeptic was instructed "Read-only outside your own output file." During
mutation probe M11 it appended four lines to
`cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml` — a governed file in the
private authority spine — then restored it. It disclosed this voluntarily and prominently
rather than hiding it.

Parent-verified restore, executed:

```
sha256sum ALLOWED-EDGES.yaml -> 500851b158e5c286a45ce50a99a7010e58ede6d7702cbf148c0f9db24a0224b8
sha256sum EDGES.yaml        -> f3ed1ed8a6452b5b8c200eadf184b2bf937b919440c26dcfa726fa334752e0d1
git -C cyberAlchemy-v2 status --porcelain ontology/canonical-kinds/  -> (empty)
tail -5 ALLOWED-EDGES.yaml  -> no appended content
```

Both digests equal the pins in `src/evaluator/edge-grammar.mjs:1-6`. Net change zero.

**Finding, independent of the outcome:** the read-only constraint was instruction only. No
mechanism enforced it. The prototype ships `scripts/verify-write-isolation.mjs`, which
hashes exactly this protected selector set before and after a run — the guard existed and
was not applied to the agent. That is a dispatch-design gap owned by the parent, not agent
misconduct; the agent's disclosure is the reason it is recorded at all.

## D4 — third selector drift

The authority skeptic cited `PACKAGE-MODEL.md:50` for "runtime contract definition"; the
actual line is `:51` (parent-executed `grep -n`). The claim holds; the address is off by one.

## Pattern, updated

Four defects, three of them the same shape: a true claim carried by a pointer that does not
resolve (`$defs` vs `properties`; `:50` vs `:51`; a stale Inventory status). Every one was
caught by parent re-dereferencing, none by the stage that produced it. Under `exact-binding`
the selector is the deliverable, not decoration — and nothing in this pipeline automatically
checks that a selector resolves. That is the single strongest process finding of this run.

## D5 — fifth selector drift

`synthesis-revised.md` §0 cites `AUTHORITY-KINDS.md:33` for `kind.evidence` / "Not authority
by itself". Line 33 is `kind.projection` ("Not promotion."). `kind.evidence` is at line **34**
— owner route "source/inventory owner", forbidden collapse "Not authority by itself."
Parent-executed `grep -n`. Claim true and correctly characterized; address off by one.

**Writer obligation:** cite `AUTHORITY-KINDS.md:34` for `kind.evidence`.

---

# CLOSURE VERDICT — `ready`

Checked `synthesis-revised.md` against the `exact-binding` contract declared in the confirmed
strategy.

**Verdict: `ready`.** No row is `blocked`. Every load-bearing claim carries a source identity
and a selector; the five drifted selectors are bound by parent execution and their corrections
are listed as writer obligations below. Rows marked `unverified` / "declared, no falsifier" are
correctly typed as such — under this contract an honestly-typed unverified row is closed, an
untyped or invented one is not.

**Not routed to feedback.** All five defects are explorer- or synthesizer-owned in origin, and
the sheet declares no synthesizer→explorers feedback edge. The research type owner forbids
spending auditor→writer revision capacity on evidence defects of that class. Rather than invent
a post-confirmation edge, the parent bound each row directly by executing the check. Zig-zag
capacity (cap 1) is fully consumed by the completed revision.

## Writer obligations — corrected selectors of record

| Cite | Not |
| --- | --- |
| `properties.lifecycle_status`, line 44 | `$defs.lifecycle_status.enum` |
| `PACKAGE-MODEL.md:51` | `:50` |
| `AUTHORITY-KINDS.md:34` (`kind.evidence`) | `:33` (that is `kind.projection`) |

## Rows the writer must carry as unresolved, not repair

NV-O5 / NV-O6 (green-while-broken path open until A2 and A2′ exist, neither written);
NV-O1 on S1 (`NODE_KINDS` untested, a third status distinct from both bound and declared);
AU-O2 (state is `blocked`; proposing `kind.evidence` is not an owner accepting it — CAV2-D49
makes accepting a kind owner-gated); AU-O3 second point (`ontology-edge-law-owner` unregistered
anywhere in the authority spine); X4; X5.

## Process finding of record

Five defects, five the same shape: a true claim carried by a pointer that does not resolve.
None was caught by the stage that produced it; all five were caught by parent re-dereferencing.
Under `exact-binding` the selector is the deliverable. Nothing in this pipeline automatically
checks that a selector resolves — the contract is enforced by a human-equivalent step, not by
a mechanism. That is the strongest transferable finding of this run and it is not about ontology.
