export interface IdentityContext {
  user_id: string;
  applied_as: string;
  token_validity: boolean;
  is_human: boolean;
}

export interface CommandRequest {
  identity_context?: IdentityContext;
  command_type: string;
  payload: Record<string, any>;
}

export interface ActionRequest {
  identity_context?: IdentityContext;
  action: string;
  label: string;
}

export class SubstrateClient {
  private identityContext: IdentityContext;

  constructor(identityContext: IdentityContext) {
    this.identityContext = identityContext;
  }

  async getProjection() {
    const response = await fetch('/api/projections/current');
    if (!response.ok) {
      throw new Error(`Failed to fetch projection: ${response.statusText}`);
    }
    return response.json();
  }

  async sendCommand(command_type: string, payload: Record<string, any>) {
    const request: CommandRequest = {
      identity_context: this.identityContext,
      command_type,
      payload
    };

    const response = await fetch('/api/commands', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`Logician Gate Failed: ${response.status} - ${errorData.detail || response.statusText}`);
    }

    return response.json();
  }

  async runAction(action: string, label: string) {
    const request: ActionRequest = {
      identity_context: this.identityContext,
      action,
      label
    };

    const response = await fetch('/api/actions/run', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`Logician Gate Failed: ${response.status} - ${errorData.detail || response.statusText}`);
    }

    return response.json();
  }
}
