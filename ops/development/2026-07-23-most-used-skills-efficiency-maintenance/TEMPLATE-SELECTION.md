# Template And Evidence Selection

## Inventory lookup

The repository-local `.arcanum/inventory/index.json` was read first. It is
parseable but its current kind validator fails on 15 pre-existing records, so
Inventory is usable as a non-authoritative discovery index with `flag` status,
not as conformance proof.

Selected entries:

| Entry | Why selected | Obligation |
| --- | --- | --- |
| `most-used-skills-efficiency-review-strategy-result` | points to the accepted ten findings and the one-change-at-a-time queue | source boundary and accepted scope |
| `sigil-maintenance-loop-inventory-first-hardening` | preserves machine-index-first lookup and non-authority rules | Inventory integration boundary |
| `domainspec-subagents-research-review-inventory-preflight` | preserves pre-sheet evidence lookup without adding another human gate | Subagents design context |
| `invoke-distill-enforcement-review-strategy-result-synthesis` | supports automatic Distill and atomic SWU handoff | plan validation |
| `whisper-concision-reading-flow-maintenance-review-strategy-result` | supplies prior Whisper runtime/readability maintenance context | runtime overlay boundary |

Excluded nearby entries: DomainSpec v2 product, UI, BTE, investor, and research
packages. They do not close a workflow-maintenance obligation in this package.

## Selected templates

| Stage | Template/profile | Eligibility | Decision |
| --- | --- | --- | --- |
| Define | `domainspec-spec/SPEC.md` | governed behavioral baseline with explicit aspects | selected; no tie |
| Design | DomainSpec architecture profile and `architecture-bundle.md` | six required design views and owner/interface decisions | selected; no tie |
| Plan | standalone `implementation-layering.md` | required for Plan | selected |
| Plan | standalone `work-pack.md` | canonical executable planning surface | selected |
| Plan | `domainspec-spec/execution-pack.md` | required by high-complexity split plan | selected |

Dedicated `spell` and `sigil` candidate families were not selected as the
package root because the target crosses both lifecycle kinds. Individual task
contracts route to those owners instead.

## Complexity

High: more than five tasks, more than two artifacts, multiple lifecycle owners,
public/private boundaries, generated-runtime synchronization, and unresolved
implementation evidence. Output mode is `split`.
