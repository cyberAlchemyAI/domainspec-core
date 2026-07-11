export function describeOpenRouterAdapter(env = process.env) {
  return {
    adapter_id: 'openrouter',
    role: 'provider-transport',
    ready: Boolean(env.OPENROUTER_API_KEY),
    key_location: 'server-env-only',
    forbidden: ['browser-key-storage', 'webview-key-storage', 'self-approval'],
    required_gate: 'human-approval-for-network-call'
  };
}

