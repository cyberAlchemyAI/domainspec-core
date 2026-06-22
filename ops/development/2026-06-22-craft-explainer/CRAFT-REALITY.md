# Craft: Reality Ledger (BUILT vs DESIGNED)

Skeptic stance: claim ≤ proof. Every line below cites the file that backs it.
Scope: the Craft sigil as it exists in this repo on 2026-06-22.

## What Craft actually is

Craft is an **agent-operated, file-backed ledger method**, not a program.
There is no Craft binary, daemon, or CLI. The "methods" (`start`, `state`,
`add_blocker`, `decide`, `recompose`, `validate`, `export_ledger`, etc.) are a
*contract an agent follows by hand* when editing YAML — they are specified as
prose in `arcanum/arcana/craft/SKILL.md` (<core-methods>, lines 152-269), with
`allowed-tools: Read, Write, Bash, Glob, Grep` (SKILL.md line 9). The agent reads
the SKILL, edits `.craft/ledger.yml`, and writes a `CRAFT.md` view. That is the
whole mechanism.

---

## 1. BUILT and operating today

| Built thing | Proof |
| --- | --- |
| Promoted canonical sigil (`tier: arcana`, `version: 0.2.1`) with full operating contract. | `arcanum/arcana/craft/SKILL.md` lines 1-10 |
| File-backed ledger method: storage contract `.craft/ledger.yml` (truth) + `CRAFT.md` (view) + `.craft/artifacts/`. | `SKILL.md` <storage-contract> lines 56-72 |
| Method surface operable by an agent (all 14 methods specified as inputs/writes/invariants). | `SKILL.md` <core-methods> lines 152-269 |
| Canonical YAML schema stack, versioned (`schema_version: 0.3.0`). | `arcanum/arcana/craft/templates/ledger.schema.yml` (25K), `templates/schemas/ledger-core.schema.yml` (21K), `templates/schemas/index.schema.yml` (5K) |
| Worked examples (ledger + matching CRAFT.md export pair, x2). | `arcanum/arcana/craft/examples/product-launch-ledger.yml` + `-CRAFT.md`; `platform-governance-ledger.yml` + `-CRAFT.md` |
| **Real `.craft/` instances in active use across the repo — 21 ledgers, 15 CRAFT.md exports.** Several are large and genuinely populated (cyberAlchemy 804 lines, poker-agent-arena 534, test-derivation-engine 512, auth-user-management 402). | `find . -path '*/.craft/ledger.yml'` → 21 hits; e.g. `cyberAlchemy-v2/.craft/ledger.yml` (`ledger_id: craft.cyberalchemy_v2`, `schema_version: 0.3.0`, populated `contexts/decisions/gaps/typed_items`) |
| Real ledgers are git-tracked (not scratch). | `git ls-files cyberAlchemy-v2/.craft/ledger.yml` returns the path |
| Schema validation done by hand against the schema and recorded as pass. | `arcanum/development/craft/LEDGER-VALIDATION.md` (VAL-001..010 all `pass`) |
| Validation/recomposition review guide. | `arcanum/development/craft/CRAFT-VALIDATION.md` |
| CRAFT.md export view exists alongside real ledgers. | `cyberAlchemy-v2/CRAFT.md`, `projects/auth-user-management/CRAFT.md` |

**Net:** the ledger method, the schema, the export view, and real working
instances are BUILT. They work because an agent operates them — that is the
intended and proven mode.

---

## 2. DESIGNED / NOT YET BUILT (no runtime, no automation)

The SKILL itself states the limit. Verbatim from `SKILL.md` <status> (lines 14-19):

> "Craft is a first canonical Arcana sigil... It is intentionally small...
> **It does not yet provide an automated command runner or full ledger renderer.**"

Promotion verdict, verbatim from `arcanum/development/craft/CRAFT-PROMOTION-READINESS.md`:

> Recommendation: **`defer`** — "Craft is ready for continued local use and more
> task-session execution, **but not ready for canonical promotion**... automation
> is explicitly deferred, and runtime/interface work remains side-threaded."
> (lines 9-13)

| Designed / deferred (NOT built) | Proof |
| --- | --- |
| Automated command runner (methods stay agent-operated by hand). | `SKILL.md` line 18; `CRAFT-PROMOTION-READINESS.md` line 13 |
| Full ledger renderer (CRAFT.md is hand/agent-exported, not auto-generated). | `SKILL.md` line 18 |
| Generated machine `index.json` — optional, rebuildable, no automated generator. | `SKILL.md` lines 67-71; `LEDGER-VALIDATION.md` line 65 ("`ledger-index.json` — deferred") |
| Priority scoring across validated states. | `CRAFT-PROMOTION-READINESS.md` line 43 (`deferred`); `LEDGER-VALIDATION.md` line 73 |
| Automatic role/lane delegation (role fields are hints only, no authority assignment). | `SKILL.md` lines 190-192; `CRAFT-PROMOTION-READINESS.md` line 45 (`deferred`) |
| Runtime / Refine interface integration; `dispatch-spec` + `runtime-handoff` not exposed as bare command routes. | `arcanum/development/craft/CRAFT-MISSING-ARTIFACTS.md` lines 9-29 (verdict: a runtime/command-surface **work-pack**, i.e. still planned work) |
| Repeated independent-use evidence for promotion. | `CRAFT-PROMOTION-READINESS.md` lines 20, 42 (examples "candidate/manual", "not yet exercised across multiple real Craft runs") |
| External registry/ontology conflict review of glossary terms. | `CRAFT-PROMOTION-READINESS.md` lines 22, 47 |

Note on the `development/craft/` tree (~425 files): it is **historical
promotion/MVP/define/design/refine/missing-work evidence, not the runtime
contract** (`SKILL.md` lines 48-49). Its volume reflects design iteration, not
shipped automation. The blocker docs (`CRAFT-MISSING-BLOCKERS-AND-GAPS.md`,
`CRAFT-MISSING-ARTIFACTS.md`) describe receipt-continuity and runtime-surface
work that is *planned*, not done.

---

## 3. The single "do not overclaim" line for a public page

> **Craft is a file-backed ledger method an agent operates by hand; it is not a
> runtime. There is no automated command runner, no auto-renderer, and no runtime
> automation — those are explicitly deferred, and promotion to canonical is still
> `defer`.**

(Backed verbatim by `SKILL.md` line 18 and `CRAFT-PROMOTION-READINESS.md`
lines 11-13.)

A public page may truthfully say: "Craft is a canonical Arcanum sigil with a
versioned schema, real in-repo ledgers, and an export view." It may **not** say:
"Craft runs commands / generates ledgers / automates roles / has a runtime."
