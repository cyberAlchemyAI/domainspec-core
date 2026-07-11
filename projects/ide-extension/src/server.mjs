import http from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { appendEvent, readEvents } from './kernel/audit.mjs';
import { writeArtifactRef } from './kernel/artifacts.mjs';
import { blockedBeforeApproval } from './kernel/grants.mjs';
import { loadModuleManifests } from './kernel/registry.mjs';
import { describeOpenRouterAdapter } from './adapters/openrouter.mjs';
import { approveDryRunEnvelope, prepareDryRunEnvelope } from './envelopes/dry-run-envelope.mjs';

const PROJECT_ROOT = path.resolve(fileURLToPath(new URL('..', import.meta.url)));

function defaultState() {
  return {
    project: 'ide-extension',
    boundary: 'l0-witness',
    selected_work_item: {
      work_item_id: 'work-l0-001',
      title: 'Prove approval-gated dry-run receipt loop',
      owner_route: 'task-session',
      source_ref: 'projects/ide-extension/SPEC.md'
    },
    approval_queue: [],
    receipts: [],
    current_envelope: null,
    evidence_refs: ['projects/ide-extension/development/founding-research/findings.md']
  };
}

async function readJson(file, fallback) {
  try {
    return JSON.parse(await readFile(file, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') return fallback;
    throw error;
  }
}

async function writeJson(file, value) {
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

async function readBody(request) {
  const chunks = [];
  for await (const chunk of request) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw.trim() ? JSON.parse(raw) : {};
}

function sendJson(response, status, value) {
  response.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store'
  });
  response.end(`${JSON.stringify(value, null, 2)}\n`);
}

function sendText(response, status, value, contentType = 'text/plain; charset=utf-8') {
  response.writeHead(status, {
    'content-type': contentType,
    'cache-control': 'no-store'
  });
  response.end(value);
}

async function serveFile(response, file, contentType) {
  try {
    sendText(response, 200, await readFile(file, 'utf8'), contentType);
  } catch (error) {
    if (error.code === 'ENOENT') {
      sendText(response, 404, 'not found');
      return;
    }
    throw error;
  }
}

export function createServer(options = {}) {
  const rootDir = options.rootDir || PROJECT_ROOT;
  const stateDir = options.stateDir || path.join(rootDir, '.ide-extension/state');
  const modulesDir = options.modulesDir || path.join(rootDir, 'src/modules');
  const publicDir = options.publicDir || path.join(rootDir, 'public');
  const workbenchFile = path.join(stateDir, 'workbench.json');
  const eventsFile = path.join(stateDir, 'events.jsonl');
  const artifactDir = path.join(stateDir, 'artifacts');

  async function readWorkbench() {
    return readJson(workbenchFile, defaultState());
  }

  async function writeWorkbench(state) {
    await writeJson(workbenchFile, state);
  }

  return http.createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://127.0.0.1');

      if (request.method === 'GET' && url.pathname === '/') {
        response.writeHead(302, { location: '/demo/l0' });
        response.end();
        return;
      }

      if (request.method === 'GET' && url.pathname === '/demo/l0') {
        await serveFile(response, path.join(publicDir, 'demo/l0.html'), 'text/html; charset=utf-8');
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/state') {
        const state = await readWorkbench();
        const [modules, events] = await Promise.all([
          loadModuleManifests(modulesDir),
          readEvents(eventsFile)
        ]);
        sendJson(response, 200, {
          ...state,
          modules,
          provider_adapters: [describeOpenRouterAdapter()],
          event_count: events.length
        });
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/envelopes/prepare') {
        const input = await readBody(request);
        const state = await readWorkbench();
        const envelope = prepareDryRunEnvelope(input);
        const approvalItem = {
          approval_id: envelope.approval.approval_id,
          run_id: envelope.run_id,
          state: 'pending',
          title: envelope.task,
          required_for: envelope.requested_grants,
          created_at: envelope.created_at
        };

        const nextState = {
          ...state,
          current_envelope: envelope,
          approval_queue: [...state.approval_queue.filter((item) => item.state === 'pending'), approvalItem]
        };
        await writeWorkbench(nextState);
        await appendEvent(eventsFile, {
          event_type: 'envelope.prepared',
          envelope_id: envelope.envelope_id,
          run_id: envelope.run_id,
          approval_id: envelope.approval.approval_id,
          created_at: envelope.created_at
        });
        sendJson(response, 201, { envelope, approval: approvalItem });
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/envelopes/run') {
        const state = await readWorkbench();
        if (blockedBeforeApproval(state.current_envelope)) {
          sendJson(response, 409, {
            error: 'approval_required',
            approval_id: state.current_envelope.approval.approval_id
          });
          return;
        }
        sendJson(response, 200, { state: state.current_envelope?.state || 'blocked' });
        return;
      }

      const approvalMatch = url.pathname.match(/^\/api\/approvals\/([^/]+)\/approve$/);
      if (request.method === 'POST' && approvalMatch) {
        const approvalId = approvalMatch[1];
        const body = await readBody(request);
        const state = await readWorkbench();
        const envelope = state.current_envelope;

        if (!envelope || envelope.approval.approval_id !== approvalId) {
          sendJson(response, 404, { error: 'approval_not_found' });
          return;
        }

        const beforeRef = await writeArtifactRef(artifactDir, `${envelope.run_id}-before`, {
          state: envelope.state,
          approval_id: approvalId
        });
        const { envelope: approvedEnvelope, receipt } = approveDryRunEnvelope(envelope, {
          approved_by: body.approved_by || 'human',
          before_ref: beforeRef,
          after_ref: `state:${envelope.run_id}:passed`
        });
        const receiptRef = await writeArtifactRef(artifactDir, receipt.receipt_id, receipt);
        const nextState = {
          ...state,
          current_envelope: approvedEnvelope,
          approval_queue: state.approval_queue.map((item) => (
            item.approval_id === approvalId ? { ...item, state: 'approved', approved_at: receipt.created_at } : item
          )),
          receipts: [...state.receipts, receipt]
        };

        await writeWorkbench(nextState);
        await appendEvent(eventsFile, {
          event_type: 'receipt.appended',
          receipt_id: receipt.receipt_id,
          run_id: receipt.run_id,
          approval_id: approvalId,
          artifact_ref: receiptRef,
          created_at: receipt.created_at
        });
        sendJson(response, 201, { receipt, artifact_ref: receiptRef });
        return;
      }

      sendText(response, 404, 'not found');
    } catch (error) {
      sendJson(response, 500, { error: error.message });
    }
  });
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const port = Number(process.env.PORT || 8765);
  const server = createServer();
  server.listen(port, '127.0.0.1', () => {
    const address = server.address();
    console.log(`ide-extension local workbench: http://127.0.0.1:${address.port}/demo/l0`);
  });
}

