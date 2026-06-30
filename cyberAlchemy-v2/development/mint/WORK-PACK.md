---
node_type: work-pack
is_session: false
status: candidate
boundary: INTERNAL — intended-not-shipped; non-executed
created: 2026-06-29
authored_by: invoke (mode=plan)
output_mode: single-file
next_owner: sigil-development
note: Paths repo-root-relative from domainspec-core/. Execution belongs to sigil-development → task-session, not invoke.
---

# Mint — WORK PACK

The buildable-now slice (L0 + L1). L2+ are listed but gated (signer capability + public/private blocker).

## Shared SWU manifest
| SWU | layer | one parent task | write scope | acceptance evidence | verify |
|---|---|---|---|---|---|
| **SWU-1** compose-scaffold wrapper | L0 | wrap `domainspec-new-repo` as Mint stage 1 | the Mint skill's stage-1 step (no edits to `domainspec-new-repo`) | a minted tree is produced + Step-7 clone-safe verify passes | run on a throwaway target path; inspect tree |
| **SWU-2** emit-template set | L1 | reverse-engineer 6 templates from the external resonantos sibling | `cyberAlchemy-v2/development/mint/templates/` (new) | 6 parameterized skeletons (AUTHORITY-MODEL, source-spine, promotion-policy, constitution, DEFINITIONS, crosswalk), domain content stripped | diff each skeleton vs its resonantos source; no domain leakage |
| **SWU-3** authority-spine emit step | L1 | emit the domain spine via authority-triage (review-mode) | the Mint skill's stage-2 step | emitted authority-model parses; every proposed kind carries a default-deny row | run on the resonantos domain as golden fixture; reproduce its spine shape |
| **SWU-4** signed decision-gate step | L2 (gated) | emit signed `authority/decisions/<date>-mint.md` + owner ratify | the Mint skill's stage-3 step | a committed signed record names the ratified kinds | **BLOCKED on the signer-capability gap (review C7)** |

## Task-local notes
- **No edits to `domainspec-new-repo`** — Mint composes it (review C6: cav2 owns the orchestrator; the scaffolder stays unchanged).
- **authority-triage** consumed in review-mode (internal); do not block SWU-3 on its public promotion (review C5).
- **Templates are external-sourced** (review C4): SWU-2 reads `<repo-root>/../resonantos-economy-research/...`, writes only into the Mint package.

## Out of this work-pack (next routes)
- The **signer/ratifier capability** for SWU-4 (owner: sigil-development design).
- **`BLK-CAV2-PUBLIC-PRIVATE-001`** resolution before any public-attached mint (owner: decision-gate).
- L3 adopt-back (deferred).
