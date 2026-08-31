# OWNER-BWSL-001 Decision Gate

## Outcome Brief

The corrected privacy-policy graph passed independent review, but the gate is
`BLOCK` until the activity-evidence privacy owner selects the six decisions.
No OAuth, provider call, private-data access, or SWU-BWSL-002 effect is
authorized.

## Recommended aggregate selection

1. The confirmer is the sole consenting owner-operator runner; later OAuth uses
   exactly `read,activity:read`, with no public provider identity.
2. The non-private receipt contains typed proof only—no runner/activity values,
   payload digest, activity count, provider IDs, tokens, raw payload, maps,
   polylines, coordinates, notes, or secrets.
3. Normal cleanup targets the same attempt within 15 minutes. This is not a
   crash-safe retention guarantee; an independent cleanup supervisor is a
   mandatory pre-effect requirement.
4. Delete the exact witness evidence row and provider tokens, reset the
   SuggestedTrack only when its final candidate is removed, and prohibit
   app-controlled backup/cache/private-log/temp copies.
5. Actually run and repeat evidence disposition plus provider revocation.
   Runner profile, disconnected provider-account metadata, auth lifecycle
   records, SuggestedTrack, unrelated evidence, provider-side records, and the
   minimal receipt persist or remain outside the proved deletion boundary.
6. Propose one later 15-minute attempt with no retry: one token exchange, a
   page-1 / 12 activity listing, a page-1 / 50 POST revalidation listing, one
   evidence submission, and supervised cleanup. Token refresh is excluded.

The full per-decision alternatives and trade-offs are in
`OWNER-BWSL-001-DECISION-GRAPH.json`. `defer`, `stop`, and `Explain / more
context` remain available.

## Exact owner response

- Select the recommended aggregate:
  `confirmed 0dd43a28120e6ffa5ba182238c0810c7b3c88da9301c8c7186201c945b323c18`
- Reject it:
  `rejected 0dd43a28120e6ffa5ba182238c0810c7b3c88da9301c8c7186201c945b323c18`
- Ask for aligned examples and deeper trade-offs without selecting:
  `explain 0dd43a28120e6ffa5ba182238c0810c7b3c88da9301c8c7186201c945b323c18`

Exact confirmation selects policy only. SWU-BWSL-002 still requires a separate
independently reviewed, exact external-effect authorization.
