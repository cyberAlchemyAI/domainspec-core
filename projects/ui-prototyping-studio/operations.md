---
id: ui-prototyping-studio-operations
project: ui-prototyping-studio
title: "UI Prototyping Studio — Lean Operations (L0 loop)"
status: draft
node_type: operations
updatedAt: 2026-06-15
---

# UI Prototyping Studio — Lean Operations

> The L0 operations of the deterministic governance loop, at SPEC altitude. Each block gives the
> `studio` CLI command, inputs, preconditions/gates (citing `INV-x` from `SPEC.md §5`), rules,
> postconditions (state transition + side effects), and owner. Gates are enforced **server-side in
> the orchestration module behind the CLI** (`INV-8`), not bypassable by any flag.
> **Agent proposes** (`GenerateVariants`, `SynthesizeMutationBatch` execution); **human disposes**
> (`SelectOrCommitBaseline`, `ApproveMutationBatch`, `ApplyApprovedBatch`). Verbatim op rules and
> error codes: `provenance/legacy-domainspec-spec/operations.md`. Confirmed against backend
> `application/*.ts`.

## L0 loop

`InitializeSession → SubmitPrompt → GenerateVariants → SelectOrCommitBaseline →
CaptureCommentEvent → SynthesizeMutationBatch → ApproveMutationBatch → ApplyApprovedBatch
→ (append manifest) → ExportDesignHandoff`

---

## InitializeSession

- **CLI:** `studio session open [--variant-count N]`
- **Owner:** human
- **Inputs:** `requestedVariantCount?` (int), `requestedBy`.
- **Preconditions/gates:** none.
- **Rules:** default `variantCount = requestedVariantCount ?? 3` and bound to `{1,2,3}` (`INV-1`);
  open both gates as `pending` (`selectionGate`, `applyGate`).
- **Postconditions:** persists one `StudioSession` with `variantCount`, empty prompt, null baseline/
  revision head; state `[none] → SessionInitialized`. Reject `0`/`4` → `VARIANT_COUNT_OUT_OF_RANGE`.
- **Determinism:** pure given inputs (variant labels = `take(['A','B','C'], variantCount)`).

## SubmitPrompt

- **CLI:** (part of `session open`) — submit prompt to the open session.
- **Owner:** human.
- **Inputs:** `sessionId`, `prompt`, `submittedBy`.
- **Preconditions/gates:** session exists.
- **Rules:** prompt non-empty after trim; stored normalized (trimmed); notes/prompt sanitized before
  persist/render (`INV-7`).
- **Postconditions:** `StudioSession.prompt` set; state `SessionInitialized → PromptCaptured`.
  Reject: `SESSION_NOT_FOUND`, empty → `PROMPT_REQUIRED`.

## GenerateVariants

- **CLI:** `studio variants register` (Claude Code supplies the HTML; `--fake`/fixture for e2e).
- **Owner:** **agent proposes** (Claude Code generates the HTML-first variants and registers them).
- **Inputs:** `sessionId`, `requestedBy`; registered variants carry `htmlArtifactRef`,
  `componentsUsed`, `rationale`, `tradeoffs`, `risk`.
- **Preconditions/gates:** prompt set, else `PROMPT_NOT_SET`.
- **Rules:** emit **exactly** `variantCount` variants, else `VARIANT_GENERATION_COUNT_MISMATCH`;
  `variantCount = 1` ⇒ baseline `committed` and `selectionGate = satisfied` immediately;
  `variantCount > 1` ⇒ `selectionGate` stays `pending` (`INV-2`). Registering changes no gate
  beyond this `variantCount` semantic; swapping fake↔Claude Code changes no contract (AC-L0-9).
- **Postconditions:** `PrototypeVariant` rows persisted for the cycle; for count=1 the only variant
  is `committed`; state `PromptCaptured → VariantsReady`.
- **Determinism:** the studio fold is deterministic; HTML content itself is agent-generated and not a
  gate. (`explore`/`exploit` `GenerationMode` is an L0 name; `exploit` requires an existing baseline.)

## SelectOrCommitBaseline

- **CLI:** `studio baseline select <LABEL>` (multi) / `studio baseline commit` (single).
- **Owner:** **human disposes** (intentional baseline) — irreversible governance control (L2 target-size).
- **Inputs:** `sessionId`, `selectedLabel?` (required iff `variantCount > 1`), `requestedBy`.
- **Preconditions/gates:** variants generated (count matches `variantCount`).
- **Rules:** `variantCount > 1` ⇒ `selectedLabel ∈ variantLabels` (`INV-2`), provenance `mode=selected`;
  `variantCount = 1` ⇒ `mode=committed` (no input needed); selected variant marked `selected`/
  `committed`, the rest `candidate`.
- **Postconditions:** `BaselineProvenance` persisted; `revisionHeadId` anchored to `rev-0000` if unset
  (the `BaselineRevisionAnchor` / staleness oracle); `selectionGate → satisfied`, `applyGate → pending`;
  state `VariantsReady → BaselineReady`. (`BaselineGenealogyFamily` is an L0 name; rich genealogy is L4.)
  Reject: missing selection → `BASELINE_SELECTION_REQUIRED`; bad label → `BASELINE_LABEL_INVALID`.

## CaptureCommentEvent

- **CLI:** `studio comment add --target <sel> --severity <s> --intent <i> --note <n>`
- **Owner:** human (annotation).
- **Inputs:** `sessionId`, `revisionId`, `target {selector, elementLabel, odId?}`, `severity`,
  `intent`, `note`, `createdBy`.
- **Preconditions/gates:** `selectionGate = satisfied`, else `BASELINE_GATE_UNSATISFIED` (`INV-2`);
  `revisionId` must match `revisionHeadId` when set, else `SOURCE_REVISION_INVALID`.
- **Rules:** canonical schema mandatory — all of `{target.selector, target.elementLabel, severity,
  intent, note}` present, else `COMMENT_SCHEMA_INVALID`; `severity ∈ {blocker,high,medium,low}`;
  note/intent trimmed and sanitized (`INV-7`).
- **Postconditions:** one `CommentEvent` appended (append-only, the durable synthesis source); state
  `BaselineReady → CommentsCaptured` (self-loop on more comments).

## SynthesizeMutationBatch

- **CLI:** `studio synthesize`
- **Owner:** **agent / system executes** (deterministic fold — agent never reinterprets human intent).
- **Inputs:** `sessionId`, `sourceRevisionId`, `requestedBy`.
- **Preconditions/gates:** `sourceRevisionId` matches `revisionHeadId` when set, else
  `SOURCE_REVISION_INVALID`; ≥1 ordered comment for that revision, else `COMMENT_SET_EMPTY`.
- **Rules:** fold the **ordered** comments into `MutationTask`s; batch starts `status=draft` with
  `approval.required=true` (`INV-3`). `applyGate` stays `pending`.
- **Determinism (load-bearing, AC-L0-4):** identical ordered comments + same `sourceRevisionId` ⇒
  **identical task IDs and checksum**. `taskId = "task-" + sha1(sourceRevisionId:commentId:selector:index)[:10]`;
  `checksum = sha256({sourceRevisionId, generatedFromCommentIds, tasks})`. No randomness, no timestamps
  in the fold.
- **Postconditions:** one `draft` `MutationBatch` persisted with `generatedFromCommentIds` and `tasks`;
  state `CommentsCaptured → MutationDrafted`.

## ApproveMutationBatch

- **CLI:** `studio batch approve <batchId> --by <actor>`
- **Owner:** **human disposes** (explicit approval) — irreversible governance control (L2 target-size).
- **Inputs:** `sessionId`, `batchId`, `approvedBy`, `approvedAt` (ISO-8601).
- **Preconditions/gates (server-side, `INV-8`):** batch must be `draft`, else `BATCH_NOT_DRAFT`
  (re-approval rejected); `approvedBy` non-empty and `approvedAt` a parseable timestamp, else
  `APPROVAL_METADATA_REQUIRED`; batch `sourceRevisionId` must equal `revisionHeadId`, else
  `APPROVAL_STALE` (stale rejected, `INV-5`).
- **Rules:** approval is the **only** path `draft → approved` (`INV-3`); records approver identity +
  timestamp.
- **Postconditions:** `MutationBatch.status = approved`; `applyGate → satisfied`; state
  `MutationDrafted → MutationApproved`.

## ApplyApprovedBatch

- **CLI:** `studio batch apply <batchId> --by <actor>`
- **Owner:** **human disposes** (the irreversible durable change) — L2 target-size control.
- **Inputs:** `sessionId`, `batchId`, `applyRequestedBy`.
- **Preconditions/gates (server-side, `INV-8`, all rejected regardless of CLI flags):**
  - `applyRequestedBy != 'system:auto'` (case-insensitive), else `AUTO_APPLY_FORBIDDEN` (`INV-4`).
  - `selectionGate = satisfied` and baseline present, else `BASELINE_GATE_UNSATISFIED` (`INV-2`).
  - batch `status = approved`, else `BATCH_APPROVAL_REQUIRED` (non-approved rejected, `INV-3`).
  - batch `sourceRevisionId = revisionHeadId`, else `BATCH_STALE_FOR_HEAD` (stale rejected, `INV-5`).
- **Rules:** allocate next revision off `parentRevisionId = revisionHeadId ?? 'rev-0000'`; build
  `RevisionManifestEntry` carrying `variantCount`, baseline provenance (`selected`/`committed`),
  `parentRevisionId`, `appliedBatchId`, `appliedTaskIds`, `unresolvedCommentIds`, `diffSummary`
  (bare `{added,changed,removed}` from task `changeType`; L4 extends).
- **Postconditions:** batch `status = applied`; **exactly one** `RevisionManifestEntry` appended
  (`INV-6`, guarded post-write — count must be `prev+1` or the apply throws); `revisionHeadId`
  advances; `applyGate → pending`; state `MutationApproved → RevisionApplied → RevisionRecorded`.
  Then `RevisionRecorded → CommentsCaptured` (iterate) or `→ SessionCompleted` (finalize). Normal
  apply does **not** depend on any proof gate (`INV-9`).
- **Determinism:** revision-id allocation and diff are deterministic given the batch and head.

## ExportDesignHandoff

- **CLI:** `studio handoff export [--profile mvp]`
- **Owner:** human or system.
- **Inputs:** `sessionId`, `exportProfile?` (default `mvp`), `requestedBy`.
- **Preconditions/gates:** ≥1 `RevisionManifestEntry` and a `revisionHeadId`, else
  `HANDOFF_REVISION_REQUIRED`; baseline present and required downstream files exist
  (`SPEC.md`, `STORIES.md`, `UI-SPEC.md`, `TEST-SPEC.md`), else `HANDOFF_REFERENCE_INCOMPLETE`.
- **Rules:** bundle carries `revisionHeadId`, baseline, `variantCount`, and story/requirement/
  acceptance/UI-spec/test-spec refs; integration flags align with artifact presence.
- **Postconditions:** `HandoffBundle` persisted and queryable; `IntegrationReadiness` flags set true;
  state `RevisionRecorded → RevisionRecorded` (terminal-side projection).

---

## Optional / deferred operations

- **ConfirmUIDecisionEvidence** — *optional L0 branch* (`BaselineReady → IdentityEvidenceConfirmed`).
  Human confirms proposed identity/visual-DNA/decision evidence as durable; requires
  `confirmedBy != 'system:auto'`. Skippable: `BaselineReady → CommentsCaptured` is valid without it.
  Rich identity/DNA types are **L4** (not in code) — see `SPEC.md §3` DEFERRED.
- **RecordFitnessSignal** — **DEFERRED (L5)**. Not detailed; net-new fitness types, gated by OQ-3.
- **EvaluateProofGate** — **DEFERRED (L5+)**. Not detailed; normal MVP apply must not depend on it (`INV-9`).
- **PromoteEvolutionRule** — **DEFERRED (L3+/L5)**. Not detailed; runtime promotion rejected in MVP.
