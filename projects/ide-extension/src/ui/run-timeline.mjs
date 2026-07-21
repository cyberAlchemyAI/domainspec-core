export const RUN_TIMELINE_STAGES = Object.freeze([
  { key: 'prepared', label: 'Prepared' },
  { key: 'approved', label: 'Approved' },
  { key: 'available', label: 'Available' },
  { key: 'running', label: 'Running' },
  { key: 'result', label: 'Result' },
  { key: 'receipt', label: 'Receipt' }
]);

const STAGE_INDEX = new Map(RUN_TIMELINE_STAGES.map(({ key }, index) => [key, index]));
const STATUS_LABELS = Object.freeze({
  active: 'Current',
  done: 'Completed',
  pending: 'Pending'
});

function currentStageFor(runView) {
  if (runView?.stage === 'interrupted') return 'running';
  return STAGE_INDEX.has(runView?.stage) ? runView.stage : null;
}

function statusFor(stageKey, runView) {
  const currentStage = currentStageFor(runView);
  if (!currentStage) return 'pending';
  const currentIndex = STAGE_INDEX.get(currentStage);
  const stageIndex = STAGE_INDEX.get(stageKey);
  if (stageIndex < currentIndex) return 'done';
  if (stageIndex === currentIndex) return 'active';
  return 'pending';
}

function detailLabelFor(stageKey, runView) {
  if (stageKey === 'running' && runView?.stage === 'interrupted') return runView.label;
  if (stageKey === 'result' && ['blocked', 'failed', 'flagged'].includes(runView?.typestate)) {
    return runView.label;
  }
  return null;
}

export function renderRunTimeline(container, runView = {}) {
  if (!container || !container.ownerDocument) {
    throw new TypeError('run timeline requires a document container');
  }

  const documentRef = container.ownerDocument;
  while (container.firstChild) container.removeChild(container.firstChild);

  for (const stage of RUN_TIMELINE_STAGES) {
    const status = statusFor(stage.key, runView);
    const item = documentRef.createElement('li');
    item.className = `bridge-step ${status}`;
    item.dataset.stage = stage.key;
    item.dataset.status = status;
    item.dataset.runState = runView?.typestate || 'unknown';
    item.setAttribute('aria-label', `${stage.label} - ${STATUS_LABELS[status]}`);
    if (status === 'active') item.setAttribute('aria-current', 'step');

    const label = documentRef.createElement('span');
    label.className = 'bridge-stage-label';
    label.textContent = stage.label;
    item.append(label);

    const detailLabel = detailLabelFor(stage.key, runView);
    const statusLabel = documentRef.createElement('span');
    statusLabel.className = 'bridge-stage-status';
    statusLabel.textContent = detailLabel || STATUS_LABELS[status];
    item.append(statusLabel);

    container.append(item);
  }
}
