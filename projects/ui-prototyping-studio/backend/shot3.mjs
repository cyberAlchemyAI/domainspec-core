import { chromium } from '@playwright/test';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 1700 } });
await p.goto('http://127.0.0.1:7334/preview/ups-session-0001', { waitUntil: 'networkidle' });
await p.waitForTimeout(1000);
await p.screenshot({ path: '/tmp/ups-shots/staged-diff2.png', fullPage: true });
await b.close(); console.log('done');
