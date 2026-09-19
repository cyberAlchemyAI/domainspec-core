# TROQAR pilot application

The preserved pilot UI and TypeScript HTTP/auth/storage adapters consume the
DomainSpec-generated consent predicate before activity evidence persistence.
Run the rebuild and validation commands from the [repository root](../README.md).
Migration authority remains the committed SQL under `drizzle/`; shared auth SQL
is imported with its source hashes under `../vendor/auth/drizzle/`.

## Open Questions

Owned by [repository README](../README.md#open-questions).
