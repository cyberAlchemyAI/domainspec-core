---
id: ide-extension-operations-v1-glossary
project: ide-extension
title: "Operations V1 Glossary Consistency"
status: pass
node_type: glossary-consistency
updatedAt: 2026-07-12
---

# Operations V1 Glossary Consistency

## Existing Terms Reused

| Term | Preserved meaning |
| --- | --- |
| V0 surface | Logical surface whose canonical body remains a workspace HTML file. |
| Surface id | Stable identity for one logical work surface. |
| Revision id | Identity for one complete committed HTML body. |
| Canvas publish | Existing complete-file V0 registration operation. |
| Automatic update | Notice followed by complete-revision fetch/reload. |
| Interaction event | User-originated named JSON payload returned to the session. |

## Local Candidate Terms

| Term | Working definition |
| --- | --- |
| Operations surface | A new surface derived from an exact V0 revision and governed by operation CAS. |
| Content operation | Retry-safe transformation from one committed complete revision to another. |
| Operation record | Durable binding between normalized request, source revision, and result revision/blob. |
| Blob store | Kernel-owned content-addressed storage for immutable complete revision bodies. |
| Whole-document target | Initial operation target whose result is always one complete HTML document. |
| Declared region | Future exactly-one element target identified by an author-stable id. |
| Rebuild | Explicit replacement from an exact-hash workspace source with lineage. |
| Navigation command | Redirect or refresh instruction that changes display without changing content. |

## Required Distinctions

- Derivation is not in-place V0 promotion.
- Operation record is not a protected-effect execution receipt.
- Append is parser-based body extension, not byte concatenation.
- Refresh reloads display; rebuild creates a content revision.
- A runtime DOM mutation is not a persisted content operation.
- Region targeting is additive future behavior, not current V1 readiness.

## Result

- Canonical conflicts: none.
- Local candidate terms: eight.
- Status: `pass` for design use; no Arcanum-wide definition promotion.
