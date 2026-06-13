# Research Validation Ledger - Boundary and canon

- Dispatch ID: `gq-research-strategy-boundary-and-canon-2026-06-12`
- Gate: `rg05-claim-evidence` — each claim maps to a source class, concrete path/handle, and validation question.
- Org isolation (`rg04`): Golden Quill PROJECT evidence only. No `orgs/` PROJECT_CONTEXT read. PASS.
- Owner boundary (`rg06`): planning evidence only; no canonical/lifecycle mutation; only the two RUN_DIR outputs written. PASS.

## Claim -> Source -> Validation Table

| # | Claim | Source class | Path / handle | Validation question | Verdict |
| --- | --- | --- | --- | --- | --- |
| F1 | Workbook posture row uses "Unrestricted / Hybrid / Sanitized / Sovereign" (four items, deprecated terms) | source-contract (workbook) | `docs/golden-quill-task-role-breakdown-handoff.md:50` | Does the workbook string differ from canon's three-value set? | CONFIRMED conflict |
| F1c | Canon posture set is exactly three: Frontier-Eligible / Split-Context Hybrid / Local-Only / Sovereign; "Sanitized" deprecated | canon | `AGENTS.md:45-47`; reinforced `CLAUDE.md:254` | Is three-posture vocabulary locked and "Sanitized" retired? | CONFIRMED canon |
| F2 | Workbook lists "Sanitization pipeline" as a build task | source-contract | `docs/golden-quill-task-role-breakdown-handoff.md:51` | Is "Sanitization pipeline" a live canon mechanism? | CONFIRMED conflict (deprecated mechanism) |
| F2c | Sanitized/opaque-slot round-trip is deprecated; only split-context survives | canon / boundary-register | `AGENTS.md:45-47`; `CLAUDE.md:254` | Does canon retire the sanitization mechanism? | CONFIRMED canon |
| F3 | Workbook includes an interactive operator console UI build row | source-contract | `docs/golden-quill-task-role-breakdown-handoff.md:53, :108` | Is interactive UI in v0.1 scope? | CONFIRMED conflict |
| F3c | v0.1 is headless only; no UI layer | boundary-register | `CLAUDE.md:252` | Is the no-UI boundary locked for v0.1? | CONFIRMED canon |
| F4 | Workbook uses "Municipal" as a segment/expert label | source-contract | `docs/golden-quill-task-role-breakdown-handoff.md:91, :95, :113, :117` | Is "Municipal" the current CIC label? | CONFIRMED conflict (stale label) |
| F4c | Canon CIC is "Public Agency", clearer alternative to "Municipal Steward" | boundary-register | `CLAUDE.md:48` | Does canon prefer "Public Agency"? | CONFIRMED canon |
| F5 | Workbook says "Sovereign-mode build" and "Sovereign-mode pilots" | source-contract | `docs/golden-quill-task-role-breakdown-handoff.md:92, :95` | Is "Sovereign-mode" an unambiguous canon term? | PARTIAL — needs disambiguation to "Local-Only / Sovereign" posture |
| F5c | "Sovereign" is a posture label half; "Sovereign Node" is Stage-5 commons, not a per-node mode | canon / boundary-register | `AGENTS.md:45-47`; `CLAUDE.md:30, :34` | Does canon separate posture-Sovereign from Stage-5 Sovereign Node? | CONFIRMED canon |
| F6 | No conflict on GB floor, Managed Edition, metered billing, MaatAI, Sovereign Node LLC | boundary-register / canon | `CLAUDE.md:24, :30, :34, :251`; `AGENTS.md:112` | Does the workbook revive any of these stale terms? | CONFIRMED clean (negative) |
| EXT | Public terminology-risk comparison would need external evidence | external (DEFERRED) | not run — needs `rg03` approval | Approved by Josh? | DEFERRED — no approval present |

## Gate Check

- `rg02-local-first`: all answer-bearing claims sourced from local workspace before any external class considered. PASS.
- `rg03-external-approval`: one external request (EXT-BC-01) named and held; no external lookup executed. PASS (correctly blocked).
- `rg04-org-isolation`: no client org material read. PASS.
- `rg05-claim-evidence`: every claim above carries source class + concrete path + validation question. PASS.
- `rg06-owner-boundary`: outputs are RESEARCH-RESULT.md and this ledger only; ledger.yml and canon untouched. PASS.

## Overall Verdict

**PASS.** The core question is fully answered from local Golden Quill canon. Five conflicts (F1-F5) and one negative confirmation (F6) are evidence-backed with concrete paths. F1/F2/F5 close under the existing `DEC-BC-POSTURE-VOCAB` correction; F3 feeds `DEC-BC-UI-BOUNDARY`; F4 is a folded vocabulary correction. One external request (EXT-BC-01) is correctly DEFERRED pending operator approval. No org-isolation or owner-boundary violation. No claim lacks a source.
