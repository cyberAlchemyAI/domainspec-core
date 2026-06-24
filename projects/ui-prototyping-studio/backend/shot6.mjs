import { chromium } from '@playwright/test';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 900, height: 900 }, deviceScaleFactor: 2 });
for (const [f,name] of [['file:///home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/production-login-variants/b.html','tag-before'],['file:///tmp/ups-shots/candidate-b.html','tag-after']]) {
  await p.goto(f, { waitUntil: 'load' });
  const el = p.locator('.line');           // the "Corra. Conecte. Conquiste." tagline
  await el.scrollIntoViewIfNeeded();
  await p.waitForTimeout(300);
  const box = await el.boundingBox();
  await p.screenshot({ path: '/tmp/ups-shots/'+name+'.png', clip: { x: Math.max(0,box.x-10), y: Math.max(0,box.y-12), width: 560, height: box.height+24 } });
}
await b.close(); console.log('done');
