# TASK-REGISTRY-SYNC: Registry and Glossary Sync

## Goal

Keep feature concepts, glossary definitions, and registry outputs synchronized as implementation and verification proceed.

## DomainSpec Coverage

All concept IDs listed in [../../SPEC.md](../../SPEC.md), plus source-linked feature terms in [../../glossary.md](../../glossary.md).

## Architecture References

- Registry sync is documentation governance; it must not change implementation behavior directly.
- Concept IDs remain authoritative from the feature SPEC.

## Implementation Directives

- Run `domainspec-sync-registry sonar-loop` after SPEC or concept table changes.
- Verify every concept/type/field link in changed markdown files with single-file link validation.
- Keep glossary updates source-linked to feature docs.

## Gaps and Questions

- Project-local registry destination must be confirmed if the sync tool supports multiple roots.

## Decision Lock

- No unresolved decision affects registry sync.
