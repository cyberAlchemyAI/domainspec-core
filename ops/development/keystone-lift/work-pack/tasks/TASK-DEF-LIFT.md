---
module: keystone-lift
task: TASK-DEF-LIFT
version: current
status: draft
updatedAt: 2026-06-14
docType: work-pack-task
---

# TASK-DEF-LIFT — Split DEFINITIONS.md and lift the wedge subset to arcanum canonical

Layer: L0 · Wave: W0 · Complexity: high · Gate: ready

## Objective
Make the DomainSpec wedge vocabulary canonical in **public arcanum** by splitting the normative `DEFINITIONS.md` at the wedge/moat seam and lifting only the wedge subset — without touching the moat cluster or cutting over invoke. Per decisions C1 (formal IDs canonical) and C2 (arcanum canonical, DS references it).

## Dependencies
- None (W0 entry). Source of truth: `research/projects/domainspec/definitions/DEFINITIONS.md`.
- Parity baseline: `arcanum/definitions/DEFINITIONS.md` currently holds only `DEF-ARC-CONTRACT`, `DEF-ARC-SCHEMA`.

## Implementation Detail Spec (domain-logic task)

**Purpose / decision owned:** which definition IDs become public-canonical, and how collisions are resolved — this is the seam that protects the moat.

**Inputs:**
- Normative `DEFINITIONS.md` (DS-D1…, DS-C…, DS-F…, DS-P…, DS-M…, DS-COR-1).
- The wedge/moat partition from the build-decisions record (C2).

**Outputs:**
- `arcanum/definitions/DEFINITIONS.md` — canonical wedge IDs (formal form).
- Updated `arcanum/definitions/DEFINITIONS-INDEX.md` and `DEFINITION-DRIFT-AUDIT.md` to absorb new IDs.

**Data model touched:** definition records (id, term, statement, type/edge semantics). No code.

**Ordered rules:**
1. **Include (wedge → canonical):** `DS-D1` (25 meta-types), `DS-D2` (29 edges, adopted profile only), `DS-D3` (concept graph), `DS-D7`/`DS-D8` (edge partition + signature), `DS-D10` (coverage-status), `DS-P1..3`.
2. **Exclude (moat → stays private, do NOT lift):** `DS-C3`, `DS-D9`, `DS-COR-1`, `DS-F1`, `DS-F5`, `DS-F6`, `DS-M13`.
3. **Exclude (not adopted):** the proposed ~38-edge / 7-category extension flagged in `DS-D2`'s canon-boundary note.
4. **Hold private (ambiguous, default per C3):** `DS-D4`, `DS-D5`, `DS-D6` — do not lift; leave in private DS.
5. **Collision guard:** before writing any ID, check against arcanum `DEF-ARC-CONTRACT`/`DEF-ARC-SCHEMA` and the Lean/Spivak `schema` usage. If a term collides (`schema`, `contract`), mint a namespaced ID (e.g. `DEF-DS-SCHEMA`) and add a one-line boundary note distinguishing it from the arcanum-native term. Do not overwrite the arcanum-native terms.
6. **Preserve provenance:** each lifted ID keeps its DS-D* identifier as the canonical key (C1: formal IDs are canonical); prose is added later as the example layer (TASK-PROSE-RECOMPOSE), not here.
7. **No reference back to private DS** in the public file (public can't depend on private). Canonical text lives in arcanum.

**Edge cases / failure modes:**
- A wedge definition *transitively references* a moat ID (e.g. a DS-D2 edge whose semantics cite DS-F1). → keep the wedge ID but strip/abstract the moat reference; record in the audit. If it can't be cleanly severed, demote that single ID to needs-decision and leave private (do not leak).
- `DS-D2` mixing adopted + proposed edges in one table. → lift only the 29 adopted edges; drop the proposed rows entirely.
- Stale project strings (`ZefraHub`) or PT terms inside a lifted definition. → sanitize before write (also covered by TASK-AUDIT).

**Acceptance checks / validation evidence:**
- arcanum link-checker + definitions-index + markdown-linking constitution green on the new file.
- `grep -E 'DS-C3|DS-D9|DS-COR-1|DS-F1|DS-F5|DS-F6|DS-M13' arcanum/definitions/` → **zero** (moat-protection).
- All 25 types + 29 edges present; proposed-extension rows absent.
- Collision terms carry a boundary note; arcanum-native `DEF-ARC-*` unchanged.

## Smallest Working Units
- **SWU-KSL-001** — extract + write the wedge subset canonical (write scope: `arcanum/definitions/`).
- **SWU-KSL-002** — verify exclusions (moat cluster + proposed extension + D4/D5/D6 absent).

(Both defined in the WORK-PACK SWU manifest with verify commands and owner = subagent.)

## Subagent Handoff Note
Work entirely in the `arcanum` submodule (public). Read the normative DEFINITIONS.md from the parent path; write only under `arcanum/definitions/`. Do NOT modify `implementation/domainspec` in this task (that's TASK-DEFS-REF-PRIVATE). Return the SWU result shape (pass/flag/block + files_touched + validation results). Submodule-first: do not bump the parent gitlink.

## Expected Result Shape
```yaml
swu_id: SWU-KSL-001 | SWU-KSL-002
result: pass | flag | block
files_touched: [arcanum/definitions/DEFINITIONS.md, ...]
validation:
  - "link-checker: <result>"
  - "moat-grep: 0 hits"
blockers: [<or none>]
reroute: <or none>
```
