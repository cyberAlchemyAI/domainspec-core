const TERMINAL_STATES = new Set(['passed', 'flagged', 'blocked', 'failed', 'completed']);
const SECONDARY_COMMANDS = new Set(['reject', 'unready', 'release']);

const PRIMARY_AFFORDANCES = Object.freeze({
  awaiting_approval: Object.freeze({ id: 'approve', label: 'Approve request', kind: 'command' }),
  approved: Object.freeze({ id: 'ready', label: 'Make available', kind: 'command' }),
  ready_for_poll: Object.freeze({ id: 'available', label: 'Available to poll', kind: 'status' }),
  claimed: Object.freeze({ id: 'running', label: 'Running', kind: 'status' }),
  interrupted: Object.freeze({ id: 'review-interruption', label: 'Review interruption', kind: 'status' }),
  passed: Object.freeze({ id: 'inspect', label: 'Inspect result', kind: 'navigation' }),
  flagged: Object.freeze({ id: 'inspect', label: 'Inspect result', kind: 'navigation' }),
  blocked: Object.freeze({ id: 'inspect', label: 'Inspect result', kind: 'navigation' }),
  failed: Object.freeze({ id: 'inspect', label: 'Inspect result', kind: 'navigation' }),
  completed: Object.freeze({ id: 'inspect', label: 'Inspect result', kind: 'navigation' }),
  unknown: Object.freeze({ id: 'none', label: 'No action', kind: 'status' })
});

function uniqueStrings(values) {
  return [...new Set(Array.isArray(values)
    ? values.filter((value) => typeof value === 'string')
    : [])];
}

export function resolveRunActions(runView = {}) {
  const typestate = typeof runView.typestate === 'string' && PRIMARY_AFFORDANCES[runView.typestate]
    ? runView.typestate
    : 'unknown';
  const legalActions = uniqueStrings(runView.legal_actions);
  const primaryAction = PRIMARY_AFFORDANCES[typestate];
  const secondaryActions = legalActions.filter((action) => SECONDARY_COMMANDS.has(action));
  const browserCommands = legalActions.filter((action) => (
    action === primaryAction.id || secondaryActions.includes(action)
  ));
  const delegatedActions = legalActions.filter((action) => !browserCommands.includes(action));

  return {
    schema_version: '1',
    typestate,
    primary_action: { ...primaryAction },
    legal_actions: legalActions,
    browser_commands: browserCommands,
    secondary_actions: secondaryActions,
    delegated_actions: delegatedActions,
    terminal: TERMINAL_STATES.has(typestate)
  };
}
