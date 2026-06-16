# Context Pack: Mutation Execution Mechanics

Artifact written to: `/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/01-context-pack.md`

## Open Question (crisp)
When an approved MutationBatch is applied, HOW does the prototype HTML actually change? Today apply only appends one RevisionManifestEntry and flips state — nothing edits the HTML. Choose an execution model (A deterministic patch / B agentic regeneration / C hybrid propose-then-validate) that turns a MutationTask description into new prototype HTML, Claude Code-native, without breaking determinism/audit governance or losing the data-od-id anchor.

## Grounded baseline (key facts)
- **Apply today = bookkeeping.** `apply-approved-batch.ts` runs gates (AUTO_APPLY_FORBIDDEN, SESSION_NOT_FOUND, BASELINE_GATE_UNSATISFIED, BATCH_NOT_FOUND, BATCH_APPROVAL_REQUIRED, BATCH_STALE_FOR_HEAD), allocates a revision off `revisionHeadId ?? "rev-0000"`, marks batch applied, computes unresolvedCommentIds, appends one RevisionManifestEntry, sets session → RevisionRecorded / applyGate pending, and post-checks the manifest grew by exactly one (VARIANT_GENERATION_COUNT_MISMATCH). No HTML is ever read/written. `MutationTask` semantics are consumed only by `buildDiffSummary` (counts) and `appliedTaskIds`.
- **Schemas (models.ts).** `MutationTask {taskId, target(selector string), intent, changeType(string), acceptanceText, priority}` — no machine-applicable change params, no odId field, changeType is bare string not a union. `DiffSummary {added, changed, removed}` counts-only. `RevisionManifestEntry` has NO pointer to produced HTML. State enum includes both RevisionApplied and RevisionRecorded; apply sets RevisionRecorded.
- **Determinism (synthesize-mutation-batch.ts).** taskId = `task-` + sha1(`${sourceRevisionId}:${commentId}:${selector}:${index}`)[:10], no timestamps. changeType inferred from intent substrings (add/create→add, remove/delete→remove, else change). priority maps severity (blocker→p0…low→p3). acceptanceText templated `Apply <intent> at <selector>: <note>`. intent copied verbatim. Batch checksum = sha256 over {sourceRevisionId, generatedFromCommentIds, tasks}. Synthesis is fully reproducible; execution is the only place non-determinism can enter.
- **Runtime/seam [governance context].** Generation engine = Claude Code-native (DEC-RUNTIME-CLAUDE-CODE-011, DEC-CLI-NOT-MCP-012); `studio` CLI is the only seam; this module (orchestration core) owns gates + determinism and is pure/framework-free TS over StudioSessionStorePort — it never calls an LLM. Any agentic step must live outside the core, behind the CLI seam. Prototype HTML is a file artifact: `htmlArtifactRef = /artifacts/ui-prototyping-studio/<sessionId>/<label>.html` (generate-variants.ts:56).
- **data-od-id.** AnnotationTarget carries `odId: string | null`; capture-comment-event.ts normalizes/persists it onto the comment target. BUT toMutationTask copies only `target.selector` — odId is DROPPED; MutationTask has no odId field. So the engine would receive only a fragile CSS selector. [governance: DEC-ATOMIC-IDS-014]

## Two load-bearing gaps (regardless of A/B/C)
1. od-id must be threaded into MutationTask (schema change) for criterion 4 to be satisfiable.
2. RevisionManifestEntry needs a pointer/hash to produced HTML for replay and the "saw-the-diff" ergonomic (OQ-2) — currently impossible since DiffSummary is counts-only and no real HTML diff exists.

## Governance invariants the execution model must honor
Auto-apply forbidden (code-enforced), approval-before-apply (code), baseline gate (code), staleness guard (code), append-only manifest exactly-one-per-apply (code post-check), determinism/reproducibility (checksum), intent is sacred (realize not reinterpret), ergonomics-first incl. saw-the-diff. INV-3/4/5/6/8 are governance context, not committed docs.

## Three approaches framed against the baseline
- A deterministic patch: max audit/reproducibility but synthesis only infers add/remove/change today — full edit-spec burden is large; expressiveness limited; requires typed param-bearing changeType union.
- B agentic regeneration: native + handles fuzzy intent but non-deterministic, breaks checksum-grade audit, drift risk, core can't vouch.
- C hybrid: Claude Code proposes HTML; deterministic validators in the core (post-seam) check target changed, acceptanceText met, od-id preserved, no out-of-scope edits, text escaped before it becomes a revision. Matches existing topology (core owns gates+determinism, CLI is seam).

## Five Pareto criteria
(1) auditability/determinism, (2) change expressiveness, (3) Claude Code-native fit, (4) data-od-id stability [needs odId in MutationTask], (5) apply-gate saw-the-diff ergonomics OQ-2 [needs real HTML output].

## Central tension
Determinism/audit/reproducibility vs expressiveness vs "generation is free" native runtime vs od-id stability vs apply-gate ergonomics. A favors 1/4 at cost of 2/3; B favors 2/3/5 at cost of 1; C separates propose (native, expressive) from validate/record (deterministic core), at the cost of a validator suite + od-id propagation.