import { chromium } from '@playwright/test';
const base = 'http://127.0.0.1:7333';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto(base + '/preview/ups-session-0001', { waitUntil: 'networkidle' });
await p.waitForTimeout(800);
await p.screenshot({ path: '/tmp/ups-shots/preview-full.png', fullPage: true });
for (const v of ['A','B','C']) {
  await p.goto(base + '/raw/variant/' + v, { waitUntil: 'networkidle' });
  await p.waitForTimeout(500);
  await p.screenshot({ path: `/tmp/ups-shots/variant-${v}.png`, fullPage: true });
}
await b.close();
console.log('done');
