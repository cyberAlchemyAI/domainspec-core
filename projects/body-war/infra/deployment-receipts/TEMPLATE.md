# TROQAR Deployment Receipt

- Date:
- Operator:
- Image:
- Domain:
- Compose file: `docker-compose.traefik.yml`
- Env file: server-owned, not printed

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Traefik route |  | `https://<domain>/` returns page |
| Status endpoint |  | `https://<domain>/api/status` returns 200 |
| Strava callback configured |  | Strava settings contain `https://<domain>/api/auth/strava/callback` |
| Login start |  | `https://<domain>/api/auth/strava/start` redirects to Strava |
| Connected profile |  | profile renders public Strava link after login |
| CSRF |  | unsafe POST without CSRF fails |
| Secret scan |  | receipt/logs contain no tokens, secrets, OAuth codes, or raw private payloads |

## Redaction Rules

- Do not paste `.env`.
- Do not paste Strava client secret.
- Do not paste access tokens, refresh tokens, OAuth codes, or cookie values.
- Do not paste raw private athlete payloads.
- Redact personal activity IDs if the runner asks for privacy.
