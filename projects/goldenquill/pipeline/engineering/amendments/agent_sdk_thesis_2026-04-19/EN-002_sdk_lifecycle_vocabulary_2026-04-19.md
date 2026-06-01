# EN-002 — SDK Lifecycle Vocabulary Reference Table

**Amendment ID:** EN-002
**Date:** 2026-04-19
**Type:** Documentation hygiene — immediate, zero-code
**Status:** `LOCKED-internal-simulated` pending operator sign-off
**Authority:** Thesis debate at `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/00_debate_and_consensus.md`

---

## Scope

Add one reference file: `pipeline/engineering/references/sdk_lifecycle_map.md`.

The file is a table mapping the Claude Agent SDK's ten lifecycle event names (PreToolUse, PostToolUse, PostToolUseFailure, PreCompact, SubagentStart, SubagentStop, Stop, UserPromptSubmit, PermissionRequest, Notification) to the Tilth lifecycle moments they structurally correspond to.

## Purpose

If Tilth ever needs to interoperate with the SDK, another generic agent runtime, or a third-party tool that uses SDK vocabulary, a translation table exists. Without the table, every such interop requires re-deriving the mapping from scratch.

## What this amendment is not

- **Not a semantic change.** Tilth's F-codes, P-surfaces, and M-mechanisms are unchanged.
- **Not a binding change.** No model bindings in `router.yaml` change.
- **Not a Cedar change.** No policy rules change.
- **Not a substitution.** SDK event names do not replace Tilth event names anywhere in active use — the mapping table is a reference, not a rename.

## Version pin

The mapping is pinned to the SDK's state at the write date (2026-04-19). The 2025 "Claude Code SDK → Claude Agent SDK" rename shows this vocabulary drifts. Refresh policy:

- Refresh on SDK **minor** version bump (x.Y.z changes).
- Refresh on any lifecycle-event rename, addition, or removal in the SDK CHANGELOG.
- Snapshot older versions at `pipeline/engineering/references/sdk_lifecycle_map.archive/` when superseded.

## Placement

Reference file lives at `pipeline/engineering/references/sdk_lifecycle_map.md`. Not in `pipeline/blueprint/`, not in `pipeline/architecture/`, not in an orgs folder. It is engineering documentation, not a blueprint section or an architectural primitive.

## Sign-off

- Cycle 1 verdict: REQUIRES_MINOR_FIXES (jargon glosses, version pin, refresh policy).
- Cycle 2 verdict: READY across all seats.
- Judge score Cycle 2: subsumed in EN-001 aggregate 96/100.
- Logician Cycle 2: zero-code, zero F-code additions, zero Cedar changes.
- Red Team Cycle 2: RT-B-01 MED CLOSED (version pin + refresh policy).

Operator signature required for promotion from `LOCKED-internal-simulated` to `LOCKED-sealed`.

---

## Cycle 2 Fix — Applied 2026-04-20 (addresses RT-NEW-04 MED from live cross-family audit)

**Vocabulary drift enforcement:** the mapping table in `pipeline/engineering/references/sdk_lifecycle_map.md` is a **reference-only** artifact. To prevent silent vocabulary drift where future Tilth code starts using SDK lifecycle event names as native Tilth primitives:

1. **Lint rule.** Adds a pre-commit check (`scripts/lint_sdk_vocabulary_drift.sh`) that greps production code under `pipeline/`, `tilth/bin/`, `scripts/` for references to SDK lifecycle event identifiers (PreToolUse, PostToolUse, PostToolUseFailure, PreCompact, SubagentStart, SubagentStop, Stop-as-SDK-event, UserPromptSubmit, PermissionRequest, Notification-as-SDK-event). Matches outside the reference file itself or inside `# SDK interop:` comments raise a warning. Adoption into production code without the comment annotation blocks the commit.
2. **Exception path.** Code that genuinely needs to interoperate with an external SDK-using tool MUST carry a `# SDK interop: <reason>` comment. Comment + reason reviewed at PR time.
3. **Refresh acknowledgment.** Any refresh of the mapping table (per the existing refresh policy) re-runs the lint on full tree to catch any drift that slipped in since the last refresh.

**EN-002 Cycle 2 status: READY for re-audit.** RT-NEW-04 MED CLOSED. Live cross-family re-audit would verify closure.

---

## Operator Sign-off — LOCKED-sealed 2026-04-20

**Status:** `LOCKED-sealed`
**Interpretation adopted:** policy-lock.
**Cycle 2 re-audit outcomes:** consolidated with EN-001 re-audit (EN-002 is the documentation-hygiene companion amendment; Cycle 2 pass covers both).
**Audit trail:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/cross_family_audit_cycle2/synthesis.md`
**Operator authorization token:** Josh Inklovich, session authorization 2026-04-20.
**Cryptographic seal (Ed25519):** pending v2.2 gates #5/#10 infrastructure; hash-bound record at `pipeline/engineering/operator_authorization_ledger.v1.jsonl`. `LOCKED-sealed` reflects policy-lock, not cryptographic seal.
**Effective:** LOCKED-sealed 2026-04-20.
