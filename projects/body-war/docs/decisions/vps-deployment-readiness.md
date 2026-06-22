# Decision Gate - VPS Deployment Readiness

Status: `blocked-pending-operator`
Target scope: `TASK-BWO-005 - VPS Deployment Receipt`
Created: 2026-06-21

## Consequential Work Blocked

The next work-pack task would configure the production origin, deploy the
app/postgres/caddy stack to the VPS, configure the Strava production callback,
and produce the first deployment receipt. That work cannot proceed safely
without operator choices and private inputs.

## Decision 1 - Canonical App Origin

Question: Which public origin should the first online TROQAR deployment use?

### Option 1: Production TROQAR Domain

- Benefit: Creates the durable public origin immediately.
- Cost or risk: Requires real DNS control and Strava callback setup now.
- When to choose: You already own/control the domain and want the first VPS
  deployment to be the production-facing URL.
- Downstream impact: Caddy, `BODY_WAR_PUBLIC_BASE_URL`,
  `BODY_WAR_ALLOWED_ORIGINS`, and `STRAVA_REDIRECT_URI` all use this domain.

### Option 2: Temporary Stable Subdomain

- Benefit: Fastest safe online proof without committing to final branding.
- Cost or risk: Later migration requires updating Caddy, Strava callback, and
  public links.
- When to choose: You have any controlled subdomain ready before the final
  TROQAR domain is decided.
- Downstream impact: Deployment receipt can be produced now; later origin
  migration becomes a known task.

### Option 3: Stop Public Deploy, Continue Local/Infra Only

- Benefit: Avoids DNS/OAuth changes until product/domain decisions are ready.
- Cost or risk: No online app receipt yet.
- When to choose: Domain ownership or Strava app settings are not available.
- Downstream impact: Work can continue on local code and infra scripts, but
  `TASK-BWO-005` remains blocked.

Recommendation: Option 2 if a controlled subdomain is available; otherwise
Option 3.

## Decision 2 - VPS Deployment Access

Question: How should deployment access to the existing VPS be handled?

### Option 1: Manual SSH/Compose Deploy

- Benefit: Fastest path to the first online receipt.
- Cost or risk: Operator must provide SSH host/user/key path privately and
  accept manual operational steps.
- When to choose: Speed matters more than full CI automation for L0.
- Downstream impact: Use shell deploy checklist; GitHub Actions/Pulumi remain
  L1.

### Option 2: CI/Secret-Managed Deploy

- Benefit: More repeatable and auditable.
- Cost or risk: Requires repo secrets, CI permissions, and more setup before
  first receipt.
- When to choose: You want less manual VPS state from the beginning.
- Downstream impact: Adds GitHub Actions/secrets work before deployment.

### Option 3: Prepare Deploy Scripts Only

- Benefit: Keeps mutation local until access details are ready.
- Cost or risk: Still no online receipt.
- When to choose: SSH access exists but should not be used from this session.
- Downstream impact: Task can produce scripts/checklists, then block before
  actual deploy.

Recommendation: Option 1 for first L0 online proof, if you can provide access
privately; otherwise Option 3.

## Decision 3 - Strava Production Callback And Secrets

Question: When should real Strava app credentials and callback configuration be
introduced?

### Option 1: Configure Real Strava App For The Chosen Origin

- Benefit: Enables actual login/connect deployment receipt.
- Cost or risk: Requires private Strava app access and careful secret handling.
- When to choose: You are ready to validate the real online flow.
- Downstream impact: `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, and
  `STRAVA_REDIRECT_URI` must be provisioned on the VPS or CI secret store.

### Option 2: Deploy Health/Profile Shell Without Strava Callback

- Benefit: Proves HTTPS, app boot, Caddy, and profile unauthenticated behavior
  first.
- Cost or risk: Does not close login/connect receipt.
- When to choose: Domain/VPS are ready but Strava app settings are not.
- Downstream impact: Deployment receipt is partial and must stay flagged.

### Option 3: Stop Before Any Secret Handling

- Benefit: Avoids accidental secret exposure.
- Cost or risk: No production auth receipt.
- When to choose: Secrets cannot be provisioned safely in this session.
- Downstream impact: Continue only with local tests and docs.

Recommendation: Option 1 only if secrets can be provisioned through a private
channel; otherwise Option 2 for an HTTPS shell receipt or Option 3.

## Decision 4 - Activity Validation Identity

Question: Which identity should be used for the first activity import receipt?

### Option 1: Use The Operator's Own Strava Account

- Benefit: Avoids friend-consent dependency for first technical receipt.
- Cost or risk: The activity may not be the Taquaral fixture.
- When to choose: You want to prove import mechanics before friend validation.
- Downstream impact: Friend fixture remains later.

### Option 2: Use Friend Activity After Consent

- Benefit: Validates the intended Taquaral fixture path.
- Cost or risk: Requires explicit consent and careful private evidence
  handling.
- When to choose: Consent is already available or can be obtained now.
- Downstream impact: Store only a redacted receipt in tracked artifacts.

### Option 3: Skip Activity Import In First Deploy Receipt

- Benefit: Lets HTTPS/auth/profile deploy first.
- Cost or risk: Activity import remains unproven online.
- When to choose: Consent or Strava access is not ready.
- Downstream impact: Deployment receipt is partial and flagged.

Recommendation: Option 1 for first technical smoke if available; Option 2 only
after consent; Option 3 if Strava validation should wait.

## Current Result

Result: `BLOCK`

No option has been selected by the operator. Do not deploy, configure real
secrets, update Strava callback settings, or use friend activity evidence until
these decisions are resolved.
