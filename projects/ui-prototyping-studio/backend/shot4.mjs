import { chromium } from '@playwright/test';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 760, height: 1200 } });
for (const [f,name] of [['file:///home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/production-login-variants/a.html','before'],['file:///tmp/ups-session-1009208/artifacts/staged/37db32cea07509f4061fe85cf39434f03584e3df07db53ad0886a828959a1b8e.html','after']]) {
  await p.goto(f, { waitUntil: 'load' });
  const cta = p.locator('[data-od-id="auth.connect.cta"]');
  await cta.scrollIntoViewIfNeeded();
  await p.waitForTimeout(300);
  const box = await cta.boundingBox();
  await p.screenshot({ path: '/tmp/ups-shots/cta-'+name+'.png', clip: { x: Math.max(0,box.x-20), y: Math.max(0,box.y-25), width: 440, height: 100 } });
}
await b.close(); console.log('done');
