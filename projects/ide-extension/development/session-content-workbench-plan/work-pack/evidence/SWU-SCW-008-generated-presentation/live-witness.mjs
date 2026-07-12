import { writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';

const evidenceDir = path.dirname(fileURLToPath(import.meta.url));
const base = process.env.SCW_WITNESS_URL || 'http://127.0.0.1:8798';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

try {
  await page.goto(`${base}/demo/l0`);
  await page.locator('#canvas-frame').waitFor({ state: 'visible' });
  const frame = page.frameLocator('#canvas-frame');
  await frame.locator('#revision-label').filter({ hasText: 'Revision One' }).waitFor();
  const initialRevisionId = await page.locator('#canvas-frame').getAttribute('data-revision-id');
  await page.screenshot({ path: path.join(evidenceDir, 'initial-workbench.png'), fullPage: true });
  process.stdout.write(`WITNESS_READY ${initialRevisionId}\n`);

  await page.waitForFunction((revisionId) => {
    const frameElement = document.querySelector('#canvas-frame');
    return frameElement?.dataset.revisionId && frameElement.dataset.revisionId !== revisionId;
  }, initialRevisionId, { timeout: 60_000 });
  await frame.locator('#revision-label').filter({ hasText: 'Revision Two' }).waitFor();
  const revisedRevisionId = await page.locator('#canvas-frame').getAttribute('data-revision-id');
  await page.screenshot({ path: path.join(evidenceDir, 'revised-workbench.png'), fullPage: true });
  await writeFile(path.join(evidenceDir, 'browser-witness.json'), `${JSON.stringify({
    base_url: base,
    initial_revision_id: initialRevisionId,
    revised_revision_id: revisedRevisionId,
    automatic_update_observed: true
  }, null, 2)}\n`, 'utf8');
  process.stdout.write(`WITNESS_PASS ${revisedRevisionId}\n`);
} finally {
  await browser.close();
}
