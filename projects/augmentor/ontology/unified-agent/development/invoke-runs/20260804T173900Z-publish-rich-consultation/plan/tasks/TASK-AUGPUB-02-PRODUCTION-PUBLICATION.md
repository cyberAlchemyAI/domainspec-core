# TASK-AUGPUB-02 — Production Publication

- Unit: `SWU-AUGPUB-004`
- Owner: production operator
- Goal: make the exact admitted candidate current or restore the exact prior
  generation.
- Prerequisites: passing candidate admission receipt and separate explicit
  authorization naming target, candidate, current, and rollback generation.
- External write scope: `/srv/augmentor-ontology` only through the owned script.
- Forbidden: source repositories, credentials, unrelated VPS paths, public root
  site.
- Acceptance: switch/start/check succeeds; otherwise rollback is healthy and
  the result is not called deployment completion.
- Closeout: deployment or rollback receipt routes to `TASK-AUGPUB-03` or
  incident handling.

