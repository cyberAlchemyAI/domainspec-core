---
deployment_id: agent-orchestration-three-moment-20260821T142033Z
deployed_at: 2026-08-21T14:20:33Z
scope: agent-orchestration-guide
result: pass
authority_effect: bounded-public-route-update
---

# Agent Orchestration Three-Moment Deployment Receipt

## Outcome

The independently approved three-moment guide projection is deployed at:

- `https://cyberalchemize.com/agent-orchestration`
- `https://cyberalchemize.com/agent-orchestration-guide`

Both routes returned HTTP 200 and the exact promoted HTML bytes:

- SHA-256: `3f92a2ca13cbcaa4aad61daa9fd623dbc4f8cc40ff5e8efd77a4b539055be8a8`
- Size: 112467 bytes

## Authority And Inputs

- User authority: direct instruction to repair, implement, and deploy the guide.
- Approved Markdown candidate: `ce66cf05277339f6e475d7298c4241a3091cbfc87db2c1593782af00c7765df9`, 29290 bytes.
- Independent result: `671130a4c1f0a87cf7fa8d24350d263f80685c1d099233a126ba467991825633`, 954 bytes, verdict `pass`.
- Markdown Work Pack closeout: `803eb457c884a16a8fb1b06760d28c546b41685512d124e174d9d7a0cb004a5a`.
- L2 plan closeout: `d3743e7f14930acea9dbb1f2b9f7bf848620bcd8df74ed725d4bb9c3eb326521`, 7481 bytes.
- Pre-promotion source HTML: `59d38eff75024ea95028ed8b455e19a1cec9859e9735a035b58ea3f82db75446`, 101880 bytes.
- Validated sibling and promoted source HTML: `3f92a2ca13cbcaa4aad61daa9fd623dbc4f8cc40ff5e8efd77a4b539055be8a8`, 112467 bytes.

## Browser Evidence

Evidence root:
`output/playwright/ux-validator/20260821T135824Z-aog-three-moment-l2/`.

- Run metadata: `c7ce1c837a77f7ab22ee3f1339364c8d6ba256d25dbc082ecb7c8e4a369fb684`, 1040 bytes.
- Findings: `c5ccedb53278e88f6c4082775d9957a29366874e01d1f1202bac54abd23108bf`, 16650 bytes; 78 of 78 findings passed.
- Summary: `448fbc31a92f72fd2a7fbe5a94a8c534a34e0d766c4673cb8d210fc6f339a8fe`, 415 bytes.
- Residue ledger: `7ec318a8becb00a233ed4ee5c3cbb97dfaf8b57a10be9e50a4db61097f1dedec`, 511 bytes.
- Live verification: `8dc2765c2c2472da06caed57f929e691d0d6d122c05ac154e69c61fdf47023e7`, 2900 bytes; 16 of 16 checks passed.
- Runtime: Playwright 1.59.1, Chromium 147.0.7727.15, installed revision 1217.
- Chromium executable SHA-256: `696170a79640ec5b50c7518140ace06c69a49cfb295bf527d4a85e26a12b89a7`.
- Viewports: 1440 by 900 and 390 by 844.

The evidence proves the declared disclosure order, protected bindings, exact
Route 3 lifecycle sequence, retell-first Route 7 flow, keyboard focus,
labels/ARIA controls, target sizing, persistence/reset, request isolation,
absence of horizontal overflow, and absence of console/page errors.

The first browser attempt stopped before product checks because its title
assertion used unsupported title case. The failed outputs remain under
`failed-run-001/`; the governance-only sidecar is
`sidecars/validator-title-case-defect.json`, SHA-256
`f09332c753856ba294997a8b36eeaed3854075d858141484473977a5f660afbc`.
The validator-only one-byte repair received a full two-viewport rerun.

## Deployment Validation

Deployment controls:

- Script: `projects/co-op-engine/infra/deploy-static-vps.sh`, SHA-256 `64c924dfe8f76d48a47aa1ebfd34f04384514a185d134d9adc2623432232cb2b`.
- Nginx config: `projects/co-op-engine/infra/nginx.conf`, SHA-256 `62d842bf0052ad4020ea95ffa7cbce2a4da6ae8ebf7068969a673cc5360c6639`.
- Dry run: `DEPLOY_SCOPE=agent-orchestration-guide DRY_RUN=1 .../deploy-static-vps.sh` — pass.
- Live run: `DEPLOY_SCOPE=agent-orchestration-guide .../deploy-static-vps.sh` — pass.
- Candidate Nginx syntax and worker readability — pass.
- Exact public digest on both aliases — pass.
- Existing public route digest checks — pass.
- Root and `/craft` retained HTTP 200 — pass.
- Anonymous `/domainspec` remained HTTP 401 — pass.
- Mobile live route at 390 by 844 — HTTP 200, no overflow, no console/page error, no third-party request, Route 1 reveal pass.

The deploy script created exact remote rollback snapshots before switching:
`site.previous`, `docker-compose.yml.previous`, `nginx.conf.previous`,
`.env.previous`, and `.domainspec.htpasswd.previous` under the isolated
`/srv/co-op-engine` deployment directory.

## Claim Ceiling And Residue

This receipt establishes exact-byte deployment and the bounded browser claims
above. It does not establish human comprehension, intended-reader success,
operator voice approval, Human Gate A, semantic truth, authorization for agent
execution, canonical Arcanum documentation status, or production readiness.

No commit or push was performed. Unrelated dirty-worktree bytes were not
included in the scoped release.
