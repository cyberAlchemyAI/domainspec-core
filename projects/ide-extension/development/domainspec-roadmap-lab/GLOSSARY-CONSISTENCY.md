---
id: ide-extension-domainspec-roadmap-lab-glossary-consistency
status: pass
updatedAt: 2026-07-14
---

# Roadmap Lab Glossary Consistency

These are package-local explanatory terms. They are not promoted canonical
DomainSpec or Arcanum definitions.

| Term | Meaning in this package | Must not mean |
| --- | --- | --- |
| Roadmap Lab | The dedicated trusted-local learning and proposal surface rendered through ide-extension Canvas. | A DomainSpec authority editor or production control plane. |
| learning packet | The node explanation, why-now, dependency, evidence/source references, and guided questions displayed for one roadmap node. | A canonical replacement for source artifacts. |
| presentation copy | Human-facing labels/explanations used to render the roadmap, keyed by stable field IDs. | Graph identity, claim authority, or Craft continuation state. |
| roadmap input fingerprint | Deterministic digest of the authoritative/projection inputs used to build the displayed roadmap. | A Canvas revision ID or proof that the inputs are correct. |
| Canvas revision | The ide-extension hash-bound complete HTML publication currently displayed. | A DomainSpec release, roadmap version, or source commit. |
| restatement | The participant's own explanation of a node before proposing a change. | Acceptance evidence that the roadmap is objectively correct. |
| improvement proposal | An append-only, revision-bound request for owner review. | An accepted, applied, or promoted change. |
| proposal disposition | Review status such as submitted, stale-review-required, under-review, accepted, rejected, or applied-with-evidence. | Browser-owned lifecycle truth without an owner receipt. |
| stale-review-required | The displayed revision, roadmap fingerprint, or observed original value no longer matches the current review context. | Automatic rejection or automatic rebasing. |
| source request | A named event asking the active session to inspect an identified repository-relative source. | Direct browser filesystem access. |
| continuation proposal | A proposal that concerns work state, gaps, decisions, or next moves and must route to Craft ownership. | A direct Craft ledger mutation. |
| applied-with-evidence | The owning lifecycle accepted the change, the relevant source/projection was regenerated, and concrete before/after evidence was retained. | A proposal submission acknowledgment. |

## Consistency Check

| Check | Result | Note |
| --- | --- | --- |
| Proposal versus mutation | pass | All design artifacts reserve mutation for the target owner. |
| Canvas revision versus roadmap fingerprint | pass | Both bindings are required and kept distinct. |
| Presentation copy versus graph authority | pass | Stable copy fields are separate from node identity/claims. |
| Local participant label versus identity | pass | The label is expressly unauthenticated. |
| Submitted versus accepted/applied | pass | State transitions require separate owner evidence. |
| Canonical vocabulary claim | pass | No package-local term is presented as promoted vocabulary. |

