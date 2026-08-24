# DomainSpec private guide deployment receipt

- Date: `2026-08-13T20:28:45Z`
- Operator: Codex, under direct user commit-and-deploy instruction
- Route: `https://cyberalchemize.com/domainspec/`
- Access: HTTPS Basic Auth; username `domainspec-guide`
- Guide source commit: `6db728283dc51c4f0fe37840f71cea91ee60f45e`
- Protected-route commit: `351611fced2013127cb2b221a9413ef4d37a8db4`
- Readability repair commit: `aaf832d27bbb61ae2225343ec6b0791fa5589523`
- Remote directory: `/srv/co-op-engine`
- Container: `coop-engine-site`
- Image: `nginx:1.27-alpine`
- Deployment scope: `domainspec`
- Result: `pass`

## Deployed guide hashes

| Artifact | Source, live, and remote SHA-256 |
| --- | --- |
| `COMPLETE-GUIDE.html` and route index | `754b753635f603e3d89f72ac5ecbcdb1351a4a6d386f299ad99365bb83e15e9d` |
| `COMPLETE-GUIDE.md` | `d3dda05f4fe9aa6615e05145d6de643eeb81cc0eef418e0abe8aabb835643f36` |
| `COMPLETE-GUIDE.lanes.json` | `58f815337c0e9591f0be9dd8c08482d329d6359b0c0bf7199e6b544214c393a0` |
| `COMPLETE-GUIDE.schema.json` | `9da00722c99ebab03ca8005b828f03d8575c3d3e3f06c6031eb0f5c550cbc4d6` |

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Candidate validation | pass | The extracted candidate passed its eight-file inventory, exact hashes, directory mode `0755`, file mode `0644`, Compose configuration, and Nginx syntax checks before the release switch |
| Canonical route | pass | `/domainspec` returns `308` to `/domainspec/` |
| Anonymous access | pass | The route index, named HTML, Markdown, lanes manifest, schema, and an absent deep path all return `401` without credentials |
| Wrong credentials | pass | The same six paths all return `401` with an invalid username and password |
| Authentication challenge | pass | Anonymous responses include `WWW-Authenticate: Basic realm="DomainSpec guide"` |
| Authenticated guide | pass | The route index and four named artifacts return `200` and match the source hashes above |
| Private source boundary | pass | `/domainspec/impl/not-deployed` returns `401` before authentication and `404` afterward; no private repository tree was packaged |
| Protected response headers | pass | Private no-store caching, CSP, no-referrer, nosniff, frame denial, restrictive permissions, `Vary: Authorization`, and noindex/noarchive headers are present |
| Password verifier | pass | The remote verifier is owned by UID/GID `101:101`, mode `0600`, and mounted read-only; plaintext is absent from the site bundle and public-routing environment |
| Worker readability | pass | A container process running as UID/GID `101:101` read all eight deployed page files and the verifier |
| Direct container health | pass | Container `/healthz` returned `ok`; Nginx syntax passed in the running container |
| Portfolio continuity | pass | `/` remained byte-identical at `477f2ca9a1c1787054e5e0d75b15417e59d7af113a5fdd403a69702e24cc6196` |
| Craft continuity | pass | `/craft` remained byte-identical at `a2fc1c35490fb1da00145602b427298fb8e17f25bb5d348be97a233dcecac3bc` |
| Bella continuity | pass | `/bella` remained byte-identical at `e0dc32910abe18c63194dbdbce672d34c0ff95de7d7543dd5b5268141f2dfb48` |
| Candidate cleanup | pass | No `.next` bundle, configuration, environment, or verifier remained after the successful release |
| Live browser | pass | Authenticated Chromium returned HTTP `200`, loaded the expected title, completed all six Key-and-Door decisions, persisted all six across reload, and displayed the completion panel |
| Mobile browser | pass | The live guide had zero horizontal document overflow at a `320 x 800` viewport |
| Browser errors | pass | The live interaction produced zero console errors and zero page errors under the deployed CSP |

## Browser runtime

- Playwright: `1.59.1`
- Chromium revision: `1217`
- Executable: `/home/vrondelli/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`
- Executable SHA-256: `696170a79640ec5b50c7518140ace06c69a49cfb295bf527d4a85e26a12b89a7`

The newest `playwright-cli` wrapper could not launch because it expected an
uninstalled Chrome/Chromium revision. No browser was downloaded and no project
dependency was added. Live acceptance therefore used the repository-approved
shared Playwright runtime directly.

## Failed attempt and rollback evidence

The first deployment attempt passed pre-switch hash and syntax checks but the
new fail-closed process `umask` caused the archived site directories and files
to be unreadable by the Nginx worker. Public and authenticated requests returned
`404`, and the running Nginx log recorded permission-denied file access.

The scripted failure path restored the previous site, Compose file, Nginx file,
environment, and absence of a verifier. After rollback, `/`, `/craft`, and
`/bella` returned `200` with their exact pre-attempt hashes, `/domainspec`
returned `404`, and container health returned `ok`.

Commit `aaf832d27bbb61ae2225343ec6b0791fa5589523` permanently closes this
regression by normalizing site directories to `0755`, page files to `0644`,
checking those modes before switching, and checking UID `101` readability after
startup. The second deployment attempt passed.

## Rollback

The immediately previous complete generation remains in
`/srv/co-op-engine/site.previous`, with the previous Compose, Nginx, and
environment files retained beside the active release as `.previous` files. The
deployment script restores and restarts that generation if startup, direct
health, worker readability, or live HTTPS validation fails.

## Boundaries

- This is an authenticated private documentation preview. It is not a public
  DomainSpec release and does not prove the described system is shipped,
  production-ready, or available as a stable external product.
- Basic Auth protects content over HTTPS but does not hide the route name,
  provide MFA, per-user audit, or granular revocation. This preview also shares
  an origin with the public pages, which is weaker isolation than a dedicated
  protected host.
- Only the four committed guide artifacts were packaged. Repository-relative
  links into `impl/`, `authority/`, `definitions/`, `development/`, and other
  private trees intentionally return authenticated `404` responses.
- No plaintext password, password verifier value, private source file, or local
  credential content is recorded in this receipt.
