import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from '../../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-e2e-'));
const server = createServer({ rootDir: projectRoot, stateDir });
await server.ready;

await new Promise((resolve, reject) => {
  server.once('error', reject);
  server.listen(4177, '127.0.0.1', resolve);
});

console.log(`Approval Desk E2E server: http://127.0.0.1:4177/demo/l0 (${stateDir})`);

let stopping = false;
async function stop() {
  if (stopping) return;
  stopping = true;
  await new Promise((resolve) => server.close(() => resolve()));
  await rm(stateDir, { recursive: true, force: true });
  process.exit(0);
}

process.on('SIGINT', stop);
process.on('SIGTERM', stop);
