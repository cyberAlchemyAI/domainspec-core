# Creative Economy Academy Deployment Receipt

- Deployed: `2026-07-28T17:51:36Z`
- Public URL: <https://resonant-alchemy.com/>
- Source: `creative-economy-session.html`
- Source SHA-256: `ce6a161949a2339a2ad5a3b25344f1397e548b79401ab5b0b052cfd08b3681d7`
- Remote directory: `/srv/creative-economy-academy`
- Container: `creative-economy-academy-site`
- Edge network: `troqar_edge`
- Router: `creative-economy-academy` for `Host(resonant-alchemy.com)`

## Verified

- The isolated Nginx container is healthy and its `/healthz` endpoint returns `ok`.
- The public HTTPS URL returns HTTP 200.
- The live HTML SHA-256 matches the deployed local source exactly.
- The response includes CSP, no-referrer, `nosniff`, frame denial, permissions,
  and no-cache headers.
- Firefox loaded the public page with title `The Creative Exchange`; navigation
  reached the complete Whisper example after its transition settled.

## Known Provider-Side Warning

Cloudflare injects `static.cloudflareinsights.com/beacon.min.js` at the edge.
The deployed CSP deliberately blocks that external analytics script, which
creates one Firefox console error and one warning. The presentation itself has
no page-origin console errors; preserve this strict CSP unless the owner elects
to enable Cloudflare analytics or disables the Cloudflare injection.
