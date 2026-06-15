---
module: keystone-closeout
version: current
status: draft
updatedAt: 2026-06-14
docType: work-pack
---

# WORK-PACK: Keystone Closeout

Closes the three deferred follow-ups from the keystone lift ([../keystone-lift/WORK-PACK.md](../keystone-lift/WORK-PACK.md)). Define + design are compact-inline (no new domain; terms already in [../keystone-lift/GLOSSARY.md](../keystone-lift/GLOSSARY.md)).

## Control Fields
| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Planning complete; execution-ready. |
| complexity | medium | TASK-MF-REMOVE-2 is cross-cutting (80+ refs + validation suite); the other two are low. |
| outputMode | single-file | Compact; tasks are self-contained. |
| layeringArtifactRef | inline (below) | Low/medium — compact layer mapping. |
| readinessProfile | pilot | |

## Objective
Finish the keystone: retire Module Formulae physically (with fixture/mogt migration), prove the `define` cutover end-to-end, and de-duplicate the wedge definition bodies now that arcanum is canonical.

## Compact Layer Mapping
- **L0** — prove the cutover actually works (live `define` dry-run). Decision unlocked: is the DomainSpec template usable end-to-end? Must pass before MF removal.
- **L1** — retire Module Formulae safely (migrate fixtures/contracts/mogt refs, then delete). Decision unlocked: can the spell validation suite pass on the DomainSpec template?
- **L2** — clean up duplication (prose de-dup in private DEFINITIONS.md).

## Task Status Board
| Task ID | Goal | Layer | Complexity | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| TASK-DRYRUN | Run `invoke define` against a real feature on the DomainSpec template; capture output as evidence | L0 | low | ready | not-started |
| TASK-MF-REMOVE-2 | Migrate fixtures/contracts/mogt refs off Module Formulae, then delete the family | L1 | medium | ready-after TASK-DRYRUN | not-started |
| TASK-PROSE-DEDUP | Replace the 9 wedge bodies in private `DEFINITIONS.md` with reference stubs | L2 | low | ready (independent) | not-started |
| TASK-VERIFY | Confirm: dry-run passes, MF gone + suite green, no wedge body duplicated | L2 | low | ready-after-impl | not-started |

## Task Detail + SWUs

### TASK-DRYRUN (L0)
- **Detail:** pick one existing feature spec (or the `domainspec-spec/SPEC.md` example), run `invoke define` so it routes to the `domainspec-spec/` baseline, and confirm it emits a SPEC + aspect docs referencing canonical DS-D1/D2 IDs and a Concept Registry. Capture the output under `evidence/`.
- **SWU-KCO-001** — execute the dry-run, save `evidence/define-dryrun-output.md`. Verify: output uses DomainSpec format + links resolve. Owner: local-fallback.
- **Acceptance:** a real `define` run produces a DomainSpec-format spec; discovery soft gate fires (or waiver writeback works).

### TASK-MF-REMOVE-2 (L1) — the substantial one
- **Detail:** the inventory under-scoped this — 80+ live refs. Order: (1) classify each ref as *active contract* (plan.md/design.md/work-pack.md template/SKILL/READMEs → repoint to `domainspec-spec/`), *validation fixture* (invoke `development/fixtures` + `experiment-loops` + `live-evidence` → regenerate against the DomainSpec template OR retire as historical), or *foreign project* (`mogt-agentic-conversation/module-formulae/` → leave; it's that project's own artifact dir, rename out of scope). (2) Migrate active contracts + fixtures. (3) Delete `templates/module-formulae/`. (4) Re-run `spells/invoke/development/run-validation-fixtures.sh` green.
- **Edge case:** historical run records (experiment-loops, refinement-runs) are immutable evidence — do NOT rewrite; only the *live* validation fixtures need migration.
- **SWU-KCO-002** — repoint active contract refs (plan.md/design.md/work-pack.md/SKILL/READMEs). Verify: `grep -rl 'Module Formulae' spells/invoke/{*.md,templates,README.md}` → 0.
- **SWU-KCO-003** — migrate/regenerate invoke validation fixtures against `domainspec-spec/`; re-run the fixture suite green.
- **SWU-KCO-004** — delete `templates/module-formulae/`; final grep shows only historical/log + foreign-project hits.
- **Acceptance:** family deleted; invoke validation suite passes; no live contract references Module Formulae.

### TASK-PROSE-DEDUP (L2)
- **Detail:** in `research/projects/domainspec/definitions/DEFINITIONS.md`, replace each of the 9 wedge bodies (DS-D1/D2/D3/D7/D8/D10/P1-3) with a one-line reference stub → `arcanum/definitions/DEFINITIONS.md#<anchor>`, keeping the heading + ID so internal DS links resolve. Moat cluster + D4/D5/D6 untouched.
- **SWU-KCO-005** — stub the 9 wedge sections (surgical edits, preserve LaTeX-free stub). Verify: DS link check green; moat bodies intact; arcanum refs resolve.
- **Acceptance:** no wedge definition body duplicated; private file is references-only for the wedge.

### TASK-VERIFY (L2) — SWU exemption (VERIFY)
- Confirm all three: dry-run evidence exists; MF family gone + suite green; zero duplicated wedge bodies. Produce `VERIFY-REPORT.md`.

## Validation Strategy
- TASK-DRYRUN: real `invoke define` output inspected.
- TASK-MF-REMOVE-2: `run-validation-fixtures.sh` green + grep clean of live refs.
- TASK-PROSE-DEDUP: DS link check + moat-grep (moat bodies still present).

## Blockers
- **B-KCO-1:** TASK-MF-REMOVE-2 must not run before TASK-DRYRUN proves the cutover (don't delete the fallback before the replacement is verified working).

## Next Route
`task-session` per SWU; `spellcraft` for the invoke contract/fixture migration (spell lifecycle). Submodule-first for any arcanum push.
