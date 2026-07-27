# Co-Op Engine Deployment Receipt

- Date:
- Operator:
- Source SHA-256:
- Domain: `https://cyberalchemize.com/`
- Remote directory: `/srv/co-op-engine`
- Container: `coop-engine-site`
- Compose file: `projects/co-op-engine/infra/docker-compose.yml`
- Environment: public routing values only

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Co-Op page |  | HTTPS returns the expected title |
| Co-Op health |  | container `/healthz` returns `ok` |
| Security headers |  | CSP, frame, referrer, content-type, and permissions headers present |
| External requests |  | no runtime dependency outside the page origin |
| Time Capsule isolation |  | subdomain still returns its expected title |
| TROQAR isolation |  | `/api/status` returns HTTP 200 |
| Container isolation |  | existing app containers remain running |

## Boundaries

- This is a public review prototype, not proof of comprehension, recruitment,
  project-owner welcome, or production product readiness.
- No secrets, credentials, participant data, or private source paths belong in
  this receipt.
