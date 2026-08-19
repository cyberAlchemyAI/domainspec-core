# Pre-Acceptance Consumer Closure

Run this gate after the final WPRA v2 report, semantic manifest, and selection
handoff exist, but before constructing an owner acceptance inventory or asking
for an epoch approval.

The gate validates the exact staged bytes through the canonical Implementation
Readiness initializer and Task Session Until Blocker WPRA binder. Route counts
are derived from the frozen frontier. A pass also proves separate Task Session
terminal and Invoke closeout routes for every unit, closed terminal receipt
shape, and nonterminal/terminal successor semantics.

The receipt is no-authority evidence. Validation does not select a unit, admit
mutation, execute a configured unit command, or approve an epoch.

## Mandatory choreography

1. Produce the final WPRA v2 outputs.
2. Run `consumer_closure.py validate` on those exact outputs.
3. Construct the acceptance request only as an unpublished draft.
   The draft must bind the live work-pack ID, plan-epoch ID, manifest ID,
   audit ID, audit verdict, terminal code, and exact closure-receipt reference.
4. Run `consumer_closure.py guard` as the exclusive writer of the acceptance
   artifact.
5. Ask the owner only after the guarded write succeeds.

The guard revalidates the receipt schema and digest, all no-authority flags,
the exact live input references, and hashes of every canonical consumer. It
fails closed if a receipt is merely present, blocked, stale, or bound to a
different consumer version. Its output uses exclusive creation.
It also rejects a draft whose identity tuple or closure-receipt binding is
missing or stale, even when the supplied closure receipt itself passes.

Do not carry an older approval over changed acceptance-bound bytes. Semantic
equivalence and approval carry-forward would be a separate authority policy
requiring an explicit owner decision.
