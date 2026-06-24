import { chromium } from '@playwright/test';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 900, height: 800 }, deviceScaleFactor: 2 });
for (const [f,name] of [['file:///home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/production-login-variants/b.html','b-before'],['file:///tmp/ups-shots/candidate-b.html','b-after']]) {
  await p.goto(f, { waitUntil: 'load' });
  const hero = p.locator('[data-od-id="auth.login-first"]');
  await p.waitForTimeout(300);
  const box = await hero.boundingBox();
  await p.screenshot({ path: '/tmp/ups-shots/'+name+'.png', clip: { x: box.x, y: box.y, width: Math.min(box.width,820), height: Math.min(box.height,360) } });
}
await b.close(); console.log('done');
