# Source Contracts

## Authority Classes

canonical_source: source file that governs behavior or law.

signed_contract: locked or signed spec, card, router, policy, or manifest.

runtime_index: query/index surface derived from source data.

derived_summary: human-readable synthesis that must point back to sources.

proposal_only: proposed design or patch queue with no mutation authority.

generated_state: runtime/session state that should not become canonical by accident.

absent_current_checkout: expected or documented surface that is not present in this checkout.

## Mutation Rules

- Canonical source changes need task-session scope and validation.
- Signed contracts need their own ceremony or supersession path.
- Runtime indexes are rebuilt from sources.
- Derived summaries can be edited, but must not silently outrank source files.
- Proposal-only files can guide work but cannot mutate runtime behavior alone.
- Generated state should not be committed unless an explicit policy says so.

