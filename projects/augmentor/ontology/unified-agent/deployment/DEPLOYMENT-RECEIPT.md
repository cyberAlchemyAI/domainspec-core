# Augmentor Ontology Deployment Receipt

- Deployed: `2026-08-03T18:00:41Z`
- Protected URL: <https://resonant-alchemy.com/augmentor/>
- Source: `../ontology-visualization.html`
- Source SHA-256: `79397e106f4f5d5894262c63b6e96d704c7bd025fa7331f1b97750b975256b9f`
- Remote directory: `/srv/augmentor-ontology`
- Current release: `releases/79397e106f4f5d58-20260803175858`
- Previous release: `releases/79397e106f4f5d58-20260803175745`
- Container: `augmentor-ontology-site`
- Authentication: HTTP Basic Auth; username `augmentor`; password delivered directly and not stored in this repository

## Verified

- Anonymous and wrong-password requests return HTTP `401` with `WWW-Authenticate`.
- Authenticated requests return HTTP `200` and the live HTML digest matches the source exactly.
- The existing homepage remains available with its previous digest.
- `/augmentoration` and `/augmentor/healthz` return HTTP `404` rather than reaching protected content or the internal health endpoint.
- CSP, no-referrer, `nosniff`, frame denial, permissions, and private no-store headers are present.
- The container is healthy; after a restart, three consecutive authenticated responses matched the source digest.
- Chromium loaded the protected page with no page errors and rendered the ontology graph.

## Deployment Note

The first release exposed a password-file ownership mismatch: anonymous denial worked,
but authenticated requests returned HTTP `500`. The release script now assigns the
hash file to the Nginx worker while retaining mode `0600`; the corrected complete
release replaced that generation before acceptance.

## Consultation API deployment — 2026-08-04

- Deployed: `2026-08-04T13:06:33Z`
- API URL: <https://resonant-alchemy.com/augmentor/consultation>
- Current release: `releases/79397e106f4f5d58-20260804130441`
- Rollback release: `releases/79397e106f4f5d58-20260803175858`
- API container: `augmentor-ontology-api` (`node:22.13.0-alpine`)
- Proxy container: `augmentor-ontology-site` (`nginx:1.27-alpine`)
- Authentication: the same fixed HTTP Basic Auth password as the ontology page;
  the existing APR1 password hash was preserved byte-for-byte and no password was
  read, printed, copied into source, or replaced.

### Deployed byte evidence

| Artifact | SHA-256 |
| --- | --- |
| Static ontology | `79397e106f4f5d5894262c63b6e96d704c7bd025fa7331f1b97750b975256b9f` |
| Compose definition | `51f54e9e39a1b93100298d5b6cb9167375d1471e02fc50faff4366b799bc8366` |
| Nginx proxy configuration | `18e63e530317346910c022e05d558d15d3b7496fadc16f96194f407dd0f494ad` |
| Consultation deployment adapter | `bd19150d79214dbf2102633edc31a8aa83f66e216343a21837c7d1d7ba9af6a3` |
| Neutral projection | `2544b0ac676c2914382f9cbca705489a848784032a24450181d88da399078428` |
| Projection manifest | `d9b25dcb76a5fd16f541dd58b566244df093f5003b9c8c120c8b0a5e6a69a96c` |

Local and deployed hashes matched for every listed artifact.

### Verified

- Local deployment-adapter and consultation suites passed under Node `v22.13.0`.
- Module ownership, documentation, production build, security pipeline, and
  `verify:alpha` passed before deployment.
- The API has no published host port and joins only the private Compose backend;
  Nginx alone joins the Traefik edge network.
- Both containers became healthy, were restarted, and became healthy again.
- Direct requests without the trusted proxy principal returned `401`.
- Three post-restart consultations returned HTTP `200`, bounded `partial`
  evidence, the `qualify` answer action, and 15 source-bound statements each.
- Public anonymous and deliberately wrong-password API requests returned `401`.
- The protected static page continued to return `401` anonymously.
- The existing public homepage still returned `The Creative Exchange`.

The public authenticated API response was not replayed by the deployment agent
because the raw existing password was intentionally unavailable. The internal
Nginx-to-API path, fixed-hash preservation, public authentication denial, TLS
route, deployed bytes, restart behavior, and consultation result were tested.

### Failed candidate and rollback proof

Candidate `releases/79397e106f4f5d58-20260804130258` started healthy but its
smoke assertion incorrectly required `ok/answer`; the real bounded result was
valid `partial/qualify`. The script restored the previous release. The assertion
was corrected to accept both evidence-bearing outcomes, rollback was strengthened
to remove new-service orphans, and the successful release was then deployed.

## Agent API page deployment — 2026-08-04

- Deployed: `2026-08-04T13:46:29Z`
- Protected UI: <https://resonant-alchemy.com/augmentor/#agent-api>
- Consultation route: <https://resonant-alchemy.com/augmentor/consultation>
- Current release: `releases/6bba2f8ed49bfd44-20260804134409`
- Rollback release: `releases/79397e106f4f5d58-20260804130441`
- Authentication: the existing HTTP Basic Auth username and password remain in
  use. The password hash was preserved byte-for-byte; no plaintext password was
  read, printed, replaced, or written into the page.

### Deployed byte evidence

| Artifact | SHA-256 |
| --- | --- |
| Agent API and ontology page | `6bba2f8ed49bfd443386413b5cd7f1f52e67a9d183efb9c014397362fbf2ac55` |
| Nginx proxy configuration | `f2c0b74abb22ff302534db71582cb61381b4b529ee2e57e1a90998b9007e0d3f` |
| Compose definition | `51f54e9e39a1b93100298d5b6cb9167375d1471e02fc50faff4366b799bc8366` |
| Consultation deployment adapter | `bd19150d79214dbf2102633edc31a8aa83f66e216343a21837c7d1d7ba9af6a3` |
| Neutral projection | `2544b0ac676c2914382f9cbca705489a848784032a24450181d88da399078428` |
| Projection manifest | `d9b25dcb76a5fd16f541dd58b566244df093f5003b9c8c120c8b0a5e6a69a96c` |

Local and deployed hashes matched for the page, Nginx configuration, and Compose
definition.

### Verified

- The generated visualization was current; seven focused Node tests passed.
- The existing ontology browser suite passed, and the new Agent API browser
  scenario passed eight mocked requests covering all answer actions, cancellation,
  malformed and unauthorized responses, safe text rendering, automation events,
  and 320 px reflow.
- The deployed page contains the `#agent-api` view, the frozen
  `window.augmentorConsultationPage` controller, and stable automation selectors.
- The public CSP now permits only same-origin API connections through
  `connect-src 'self'`; every other prior CSP restriction remains.
- The API container has no published host ports and remains attached only to the
  private Compose backend. Nginx alone also joins the public edge network.
- Both containers became healthy, were restarted, and became healthy again.
- Three post-restart reasoning-engine consultations returned `partial/qualify`
  with 14 source-bound statements each, `followRetrievedInstructions: false`,
  and `authorityEffect: none`.
- Public anonymous page and API requests returned `401`; a deliberately wrong
  page password returned `401`; the existing public homepage still returned
  `The Creative Exchange`.
- The first public probe during the atomic Traefik/container transition returned
  `404`; the deployment acceptance loop retried and reached the expected `401`
  without rollback.

The authenticated browser form was not replayed against the public hostname
because the existing plaintext password remains intentionally unavailable to the
deployment agent. The same page bytes and consultation flow passed together in a
loopback browser test; production separately proved the exact deployed page bytes,
the fixed-hash Basic Auth boundary, public same-origin CSP, private API health,
restart recovery, and live reasoning consultation results.
