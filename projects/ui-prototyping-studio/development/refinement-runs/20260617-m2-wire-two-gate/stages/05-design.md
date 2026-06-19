---
id: design-m2-wire-two-gate
run_id: 20260617-m2-wire-two-gate
step_id: s5-s8 (x-ray + tournament + dialectic + toy-game, consolidated)
capability_ref: distill+invoke+interrogation (inline)
updatedAt: 2026-06-17
---

# Design — M2-wire (live two-gate apply over real HTML)

## §1 X-ray: the state + HTML data-flow (and the HTML-free gap)

```
TODAY (single-gate, HTML-FREE):
  batch approve -> applyApprovedBatch
     -> append RevisionManifestEntry{ diffSummary = INFERRED from task.changeType }   ← no real diff
     -> revisionHeadId = new ; state = RevisionRecorded   ← ONE call, head advances immediately
  No currentHtml, no candidateHtml, no scope check at apply. The variant HTML (real post-MR1) is
  never read. diffSummary is a count of intents, not a measured before/after. (Review honest-diff finding.)

TARGET (two-gate, HTML-REAL):
  apply --candidate-from <file>   (agent supplies the FULL mutated document)
     -> currentHtml = readHtml(head revision's committed ref) OR, for rev-0000, the baseline variant's
        htmlArtifactRef (resolvable post-MR1)
     -> scopeOdIds = approved batch.tasks[].odId
     -> validateAndStage(currentHtml, candidateHtml, scopeOdIds, port)
            REJECT  -> no write; stay MutationApproved
            NOT_REJECT -> stageHtml -> stagedRef + candidateHtmlHash
     -> persist staged candidate {stagedRef, candidateHtmlHash, batchId}; state = RevisionApplied (head NOT advanced)
     -> compute + return DiffSummaryHonest (real od-id before/after) for the human to SEE
  accept <sid>
     -> acceptStaged(stagedRef, candidateHtmlHash, port) -> commit -> committedRef
     -> append RevisionManifestEntry{ candidateHtmlHash, diffSummaryHonest, htmlArtifactRef=committedRef }
     -> head++ ; state = RevisionRecorded ; clear staged
  discard <sid>
     -> discardStaged(stagedRef) ; clear staged ; state = MutationApproved
```

**Finding:** M2-wire is not "call the engine" — it must introduce the **HTML data-flow the apply path
never had** (current-HTML resolution + candidate ingestion), a place to **hold the staged candidate**
between `apply` and `accept`, and an **honest diff**. The engine + `RevisionApplied` state + the M0a
`candidateHtmlHash`/`diffSummaryHonest` fields already exist (added for exactly this). **Chain
dependency:** the live path requires **MR1-registered** variants (real HTML); stub `generate` variants
have dangling refs → current-HTML unresolvable. So MR1 → MW1.

## §2 Tournament

### 2a Staged-candidate persistence
| Option | Shape | domain purity | migration | atomicity | verdict |
|--------|-------|---------------|-----------|-----------|---------|
| **A** store methods `saveStagedCandidate/getStagedCandidate/clearStagedCandidate` | transient infra state under a separate store key | high (StudioSession entity untouched) | none (no entity schema change) | per-session record | **WINNER** |
| B field `StudioSession.stagedCandidate?` | persisted with the session | low (pollutes the entity + its INVs with transient state) | entity schema change | one save | runner-up (simpler but dirties the entity) |

**Pareto: A.** The staged candidate is admission-boundary *infra*, not part of the session's conceptual
identity; keep the entity clean (consistent with "core owns determinism; staging is infra"). B's only win
is one fewer call.

### 2b Candidate ingestion
`apply --candidate-from <file>` carrying the **FULL mutated document** (vs a fragment). Full doc wins:
`admitScope` is whole-tree, the agent rewrites the document with the in-scope change, and the scope fence
rejects anything out-of-scope — no merge logic needed. (Mirrors MR1's `--from` ingestion.) Fragment
rejected (needs a merge step the scope fence is designed to make unnecessary).

## §3 Dialectic — inferred vs honest diff
- **P1:** keep the inferred `diffSummary` (cheap, exists).
- **P2:** compute `DiffSummaryHonest` from a real before/after (the review flagged inferred-diff as
  dishonest; the M0a fields exist for this).
**Resolution — honest, because we now HAVE both sides.** The two-gate apply holds `currentHtml` and
`candidateHtml`, so it MUST compute the honest per-od-id fragment diff (reuse the `admission.ts`/
`canonicalize.ts` od-id attribution) and populate `diffSummaryHonest` + `candidateHtmlHash` on the
recorded revision; the human's accept-diff shows the honest fragments. Keep the legacy `diffSummary`
during migration (optional). **Convergence:** the accepted revision carries `diffSummaryHonest`; this
discharges the review's honest-diff finding. **Idempotency-at-verdict:** commit exactly the previewed
`candidateHtmlHash` (seen == recorded) — already enforced by `acceptStaged`.

## §4 Toy-game (falsification before planning)
| Case | Input | Expected |
|------|-------|----------|
| ADMIT | in-scope candidate (only scope od-ids changed) | staged; head unchanged; state RevisionApplied; honest diff returned |
| REJECT | out-of-scope candidate (a non-scope od-id changed) | REJECT; nothing staged; stays MutationApproved |
| ACCEPT | acceptStaged(correct hash) | committed; head+1; state RevisionRecorded; revision carries diffSummaryHonest+candidateHtmlHash |
| MISMATCH | accept wrong hash | CANDIDATE_HASH_MISMATCH (fail-closed) |
| DISCARD | discard staged | staged dropped; state MutationApproved |
Mirrors the C-1 GOOD/BAD fixture discipline; falsifies "the gates fire" and "head advances only on accept".
