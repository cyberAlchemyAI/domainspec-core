# Context Pack: OEWSN Dedicated Build Binding Refresh

## Identity

- Task: `invoke:refresh:apply-approved:SWU-OEWSN-004-build-binding`
- Run: `oewsn-binding-20260802T021403Z`
- Mode: standard, strict
- Repository revision: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`
- Authority effect: none

## Obligation coverage

| Obligation | Status | Selected evidence | Resolution |
| --- | --- | --- | --- |
| O-01 persist option 2 | covered | selection receipt `selected_option` | dedicated semantic-navigation binding is the only admitted repair |
| O-02 preserve blocker history | covered | blocked receipt plus Work Pack G-04 | blocker is retained as resolved, not erased |
| O-03 protect historical build identity | covered | L1 lock, base overlay and first-working hashes | all remain read-only and byte-exact |
| O-04 repair SWU-004 material scope | covered | manifest SWU-004 material/output fields | five materials plus three execution outputs form the exact write union |
| O-05 keep mutation closed | covered | admission contract | only fresh Task Session can authorize product mutation |

Strict coverage: pass.

## Selected sources

- `planning/decisions/admissibility/SWU-OEWSN-004-build-binding-repair-selection.json`
  - Selector: `selected_option`, `authorization`
  - Obligations: O-01, O-05
- `planning/work-pack/session-evidence/SWU-OEWSN-004/20260802T014636Z/receipt.json`
  - Selector: terminal blocker and zero-product-mutation result
  - Obligations: O-02
- `planning/SWU-MANIFEST.json`
  - Selector: `SWU-OEWSN-004`
  - Obligations: O-03, O-04
- `planning/MUTATION-ADMISSION-CONTRACT.json`
  - Selector: required, satisfied and forbidden lists
  - Obligations: O-03, O-05
- `planning/WORK-PACK.md`
  - Selector: control fields, G-04 and gate checks
  - Obligations: O-01 through O-05

## Constraints and non-goals

- No product, ontology, authority, publication, release or deployment mutation.
- Historical L1 lock, first-working manifest, base overlay manifest and patches
  0001–0002 remain immutable.
- No UI implementation is added by this refresh.

## Write scope

- The five Invoke-owned planning targets listed in `material-package.json`.

## Validation surface

- Invoke material-package schema and byte binding.
- Refresh handoff `pass/ready`.
- JSON parsing, all-SWU write algebra, Markdown links, protected historical
  hashes, patch inventory, scoped whitespace and staged/live byte equality.

## Gaps and blockers

- None within Invoke Refresh. Product mutation is intentionally pending fresh
  Task Session admission and is not a refresh blocker.

## Authority precedence

1. Explicit option-2 Decision Gate selection.
2. Existing approved Body War profile and SWU manifest ownership.
3. Historical build artifacts as protected implementation evidence.

## Fallback exploration rule

No broad exploration is admitted. Task Session may inspect only the selected
SWU's named build, source, test and fixture surfaces when it starts.

## Provenance

- Selection digest: `54c41a4f4a17cf164dcefed429c50a9e4d8e3aa42b6cee0ace877cabf6747249`
- Prior blocked receipt: `ae26c2350223856452f9cf91fc28abc9e2605cc000a35920cf9b0a2b161e597b`
- Material package digest: `121be1afaf2d4ba534e2a77b48a769aa290412819343cde1f33d0ee763294ccd`
