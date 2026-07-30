async page => {
  const evidence = {};
  const node = page.getByText('SuggestedTrack Needs Evidence', { exact: true });
  evidence.nodeTextCount = await node.count();
  if (evidence.nodeTextCount) {
    await node.first().click();
    await page.waitForTimeout(250);
    await page.screenshot({ path: '/tmp/bw-ui-color/selected-node-default.png' });
    evidence.nodeSideText = (await page.getByRole('complementary').innerText()).slice(0, 5000);
    evidence.nodePresentation = await node.first().evaluate(e => {
      const values = [];
      for (let x = e, i = 0; x && i < 5; x = x.parentElement, i++) {
        const c = getComputedStyle(x);
        const r = x.getBoundingClientRect();
        values.push({
          tag: x.tagName,
          role: x.getAttribute('role'),
          color: c.color,
          background: c.backgroundColor,
          border: c.borderColor,
          outline: c.outline,
          boxShadow: c.boxShadow,
          bounds: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]
        });
      }
      return values;
    });
  }
  const edgeName = 'Edge from presentation:body-war.business.operation.attach-activity-evidence-candidate to presentation:body-war.business.entity.suggested-track';
  const edge = page.locator('[role="group"]').filter({ has: page.locator('title') });
  const exactEdge = page.locator(`[role="group"][aria-label="${edgeName}"]`);
  evidence.edgeCount = await exactEdge.count();
  if (evidence.edgeCount) {
    await exactEdge.first().click();
    await page.waitForTimeout(250);
    await page.screenshot({ path: '/tmp/bw-ui-color/active-relation-default.png' });
    evidence.edgeSideText = (await page.getByRole('complementary').innerText()).slice(0, 5000);
    evidence.edgePresentation = await exactEdge.first().evaluate(e => {
      const c = getComputedStyle(e);
      return { color: c.color, background: c.backgroundColor, outline: c.outline, filter: c.filter, aria: e.getAttribute('aria-label') };
    });
  }
  const style = await page.addStyleTag({ content: 'html { filter: grayscale(1) !important; }' });
  await page.waitForTimeout(100);
  evidence.grayscale = { sideText: (await page.getByRole('complementary').innerText()).slice(0, 3000) };
  await page.screenshot({ path: '/tmp/bw-ui-color/active-relation-grayscale.png' });
  await style.evaluate(e => e.remove());
  await page.emulateMedia({ forcedColors: 'active', reducedMotion: 'no-preference' });
  await page.waitForTimeout(100);
  evidence.forcedColors = {
    active: await page.evaluate(() => matchMedia('(forced-colors: active)').matches),
    sideText: (await page.getByRole('complementary').innerText()).slice(0, 3000),
    body: await page.locator('body').evaluate(e => {
      const c = getComputedStyle(e);
      return { color: c.color, background: c.backgroundColor };
    })
  };
  await page.screenshot({ path: '/tmp/bw-ui-color/active-relation-forced-colors.png' });
  await page.emulateMedia({ forcedColors: 'none', reducedMotion: 'reduce' });
  evidence.reducedMotion = {
    active: await page.evaluate(() => matchMedia('(prefers-reduced-motion: reduce)').matches),
    animations: await page.evaluate(() => document.getAnimations().map(a => ({
      state: a.playState,
      duration: a.effect?.getTiming().duration,
      iterations: a.effect?.getTiming().iterations
    })).slice(0, 30))
  };
  await page.screenshot({ path: '/tmp/bw-ui-color/active-relation-reduced-motion.png' });
  return evidence;
}
