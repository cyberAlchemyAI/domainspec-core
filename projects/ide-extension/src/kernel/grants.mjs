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

export function requiresApproval(grants) {
  return grants.some((grant) => EFFECTFUL_GRANTS.has(grant) || grant.endsWith('-after-approval'));
}

export function blockedBeforeApproval(envelope) {
  return Boolean(envelope?.approval?.required && !envelope.approval.approved_at);
}

export function defaultGrants() {
  return ['preview.read', 'dry-run.noop'];
}

