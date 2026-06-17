# Closure Gates

The tower may be marked **closed** only when every gate below passes. Until then it is
`OPEN` / `PARTIAL`. (From the research-tower sigil's quality bar + subagent closeout rule.)

## Gates

| # | Gate | Pass condition | Status |
|---|---|---|---|
| G1 | Source record | `levels/L0-corpus.md` has version, URL, date, source boundary | ✅ pass (2026-06-16) |
| G2 | Existing artifacts checked | confirmed no prior tower for this source before creating | ✅ pass |
| G3 | Required artifacts | README, TOWER, L0, L1, L2, gates, residue all exist; claim-ledger, glossary, definitions, distill, bridge-decisions, LEARNING-PACK filled | ✅ pass — all filled at reconciliation |
| G4 | Source-kind discipline | every upstream claim carries a source-kind label; no `analogy`/`operator-reading` masquerading as `primary-source` | ✅ pass — reviewer S1 confirmed the seam holds; P6 + paintbrush-handles label fixes applied |
| G5 | Notation bridge | not applicable — corpus is prose, not formal notation (Bayes math is `related-source`, light) | ✅ not-needed |
| G6 | Borrow/block decisions | bridge-decisions.md gives every Arcanum mapping a status | ✅ pass — 10 candidates, all with a status + S2 verdict |
| G7 | Residue closed-or-deferred | every named residue item is closed or moved to explicit future-work | ✅ pass — itemized R-01…R-08; open items owned, out-of-corpus deferred (none falsely closed) |
| G8 | **Subagent closeout** | every dispatched lane has an integration decision; no implicit/unreviewed lane (ledger below) | ✅ pass — 6 lanes, all terminal (ledger below) |
| G9 | Promotion boundary | LOCAL-ONLY preserved; promotion-candidates listed but not promoted; no write into `arcanum` | ✅ pass |
| G10 | Links/structure valid | all internal links resolve; layer spine intact | ✅ pass — validated 2026-06-16 (see validation note) |

## Subagent closeout ledger (G8)

No lane may be hidden, unreviewed, or missing an integration decision at closure.

| Lane | Assigned question | Evidence returned | Integration decision | Rejected/blocked | Final status | Residue owner |
|---|---|---|---|---|---|---|
| lens-readers/E1 charitable (source-internal) | strongest version of each book's thesis + vocabulary | `_dispatch/lens-E1.md` (~15–16 essay bodies; ~60% URLs 404'd) | spine + per-book theses + glossary/definitions | nothing rejected; title-level items → residue | `integrated` | R-01,02,04,05 |
| lens-readers/E2 adversarial (external literature) | overclaims/divergences vs Kahneman/Jaynes/cog-sci | `_dispatch/lens-E2.md` | claim-ledger R1–R11 + counter-spine + L2–L5 | none | `integrated` | R-06,07 |
| lens-readers/E3 historical (lineage) | concept origins, recurrence, mis-attribution | `_dispatch/lens-E3.md` (terminal/instr. origin 404'd) | recurrence matrix + Korzybski/attribution flags | none | `integrated` | R-03 |
| synthesizer/01 | triangulate 3 lenses → per-book maps + spine + bridge candidates | `_dispatch/findings-draft.md` | basis for findings.md + all tower content | superseded by corrected findings.md | `integrated` | — |
| reviewers/S1 faithfulness/definitional gate | misrepresentation / seam leaks / label errors | return (0 blockers, 2 major, 2 minor) | all 4 corrections applied (P6, paintbrush-handles, P1, P5) | none | `integrated` | — |
| reviewers/S2 bridge precedent/non-vacuity gate | are bridges real mechanisms or vacuous? | return (per-candidate verdict table) | re-statuses applied (B1/B5 already-owned, B3 analogy-only, B4 scoped) | B7,B8 block · B9,B10 future-work | `integrated` | R-08 |

Final status vocabulary: `closed` · `integrated` · `rejected` · `blocked`. **All 6 lanes
terminal; no hidden/implicit/unreviewed lane.** Plus 4 check-tension gate agents (2 reproved v1,
2 passed v2) — *infrastructure, not registered* (per `check-tension` skill); reported here for
completeness, not as dispatch lanes.
