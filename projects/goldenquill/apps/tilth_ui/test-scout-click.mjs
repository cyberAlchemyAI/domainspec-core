import { chromium } from "playwright";
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("http://127.0.0.1:4173/home");
  console.log("Navigated to Home");
  
  const buttons = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("li")).map(n => ({
      text: n.textContent.trim(),
      live: n.dataset.gqLive,
      route: n.dataset.gqRoute
    }));
  });
  console.log("Buttons:", buttons.filter(b => b.text.includes("Scout Profile")));

  await page.click("text=Scout Profile");
  console.log("Clicked Scout Profile");
  await page.waitForTimeout(1000);
  console.log("URL is now:", page.url());
  
  await browser.close();
})();
