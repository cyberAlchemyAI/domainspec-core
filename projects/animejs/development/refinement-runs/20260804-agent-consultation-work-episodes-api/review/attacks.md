# Design Review Attacks

Both confirmed read-only critics completed and returned `BLOCK` against the draft. This means the requested attacks completed; it does not mean the direction failed or the repaired design passed.

## API and authority lane

The critic defended the basic capability split, host-injected context, digest preconditions, handle-only evidence intake, append/reducer separation, and separate Lesson owner. It found nine missing closures, led by four critical defects:

- no closed neutral-projection allowlist/manifest;
- no immutable episode owner/delegation binding;
- derived episode material could become a second canonical graph writer;
- close/materialize operations lacked a closed effect and output-kind allowlist.

Structured capture: `api-authority-critic.review.json`.

## Episode-integrity lane

The critic constructed 20 bounded transition counter-examples. It found the append-only direction sound but blocked the draft on:

- two conflicting supersession spellings and no vocabulary-valid WorkEpisode supersession edge;
- mutable Task/VersionContext meaning when references are resolved after open;
- incomplete outer status and committed-receipt recovery contracts;
- undefined episode graph-digest policy;
- incomplete evidence attachment/revocation state machine;
- reducer/snapshot/projection versioning gaps.

Structured capture: `episode-integrity-critic.review.json`.

All fixtures are `planned_not_executed`.
