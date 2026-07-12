const EFFECTFUL_GRANTS = new Set([
  'fs.write',
  'shell.exec',
  'network.call',
  'browser.act',
  'export',
  'handoff',
  'commit',
  'push',
  'publish',
  'provider.key.change'
]);

export const L0_GRANT_POLICY_VERSION = '1';
export const L0_BRIDGE_GRANT_POLICY_VERSION = '2';

const LEGACY_L0_GRANTS = new Set([
  'preview.read',
  'dry-run.noop'
]);

const BRIDGE_L0_GRANTS = new Set([
  'preview.read',
  'skill.invoke'
]);

const L0_GRANTS = new Set([...LEGACY_L0_GRANTS, ...BRIDGE_L0_GRANTS]);

function invalidGrants(message) {
  const error = new Error(message);
  error.code = 'invalid_grants';
  error.policy_version = L0_GRANT_POLICY_VERSION;
  return error;
}

export function requiresApproval(grants) {
  return grants.some((grant) => EFFECTFUL_GRANTS.has(grant) || grant.endsWith('-after-approval'));
}

export function blockedBeforeApproval(envelope) {
  return Boolean(
    envelope?.approval?.required
    && !envelope.approval.approved_at
    && !envelope.approval.rejected_at
  );
}

export function defaultGrants() {
  return [...LEGACY_L0_GRANTS].sort();
}

export function bridgeGrants() {
  return [...BRIDGE_L0_GRANTS].sort();
}

export function normalizeL0Grants(grants) {
  const values = grants === undefined ? defaultGrants() : grants;

  if (!Array.isArray(values) || values.length === 0) {
    throw invalidGrants('requested_grants must be a non-empty array');
  }

  if (!values.every((grant) => typeof grant === 'string' && grant !== '')) {
    throw invalidGrants('requested_grants must contain only non-empty strings');
  }

  if (new Set(values).size !== values.length) {
    throw invalidGrants('requested_grants must not contain duplicates');
  }

  const unknown = values.filter((grant) => !L0_GRANTS.has(grant));
  if (unknown.length > 0) {
    throw invalidGrants(`unknown L0 grants: ${unknown.sort().join(', ')}`);
  }

  if (values.includes('skill.invoke')) {
    const normalized = [...values].sort();
    const expected = bridgeGrants();
    if (JSON.stringify(normalized) !== JSON.stringify(expected)) {
      throw invalidGrants('skill.invoke requires the exact preview.read bridge profile');
    }
  }

  return [...values].sort();
}
