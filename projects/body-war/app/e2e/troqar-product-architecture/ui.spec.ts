import { expect, test } from "@playwright/test"

test.describe("TROQAR online runner profile", () => {
  test("connects fake Strava and renders safe profile and activity UI", async ({ page }) => {
    await page.goto("/")

    await expect(page.locator('[data-od-id="troqar.shell"]')).toBeVisible()
    await expect(page.locator('[data-od-id="topbar.account.actions"]')).toBeVisible()
    await expect(page.getByRole("heading", { name: "Online Runner Profile" })).toBeVisible()
    await expect(page.locator('[data-od-id="auth.connect.cta"]')).toBeVisible()

    await page.locator('[data-od-id="auth.connect.cta"]').click()
    await expect(page.getByText(/Connected with scope:/)).toBeVisible()
    await expect(page.locator('[data-od-id="profile.safe-athlete-card"]')).toContainText(
      "Tokens stay server-side and never render in this page",
    )
    await expect(page.locator('[data-od-id="profile.strava-link"]').first()).toHaveText("Open public Strava profile")
    await expect(page.locator('[data-od-id="profile.strava-link"]').first()).toHaveAttribute(
      "href",
      /https:\/\/www\.strava\.com\/athletes\/\d+/,
    )

    await expect(page.locator("body")).not.toContainText(/access_token|refresh_token|client_secret|oauth code/i)
    await expect(page.locator('[data-od-id="activity.recent-summary"]')).toContainText(
      "Route geometry and scoring are explicitly separate from this preview",
    )
  })

  test("submits one activity as preview evidence through visible controls", async ({ page }) => {
    await page.goto("/")
    await page.getByRole("link", { name: "Connect Strava" }).click()

    const firstActivity = page.locator(".activity").first()
    await expect(firstActivity).toBeVisible()
    await firstActivity.locator("select").selectOption({ index: 0 })
    await firstActivity.locator('[data-od-id="evidence.submit.cta"]').click()

    await expect(page.locator(".submission").first()).toBeVisible()
    await expect(page.locator(".submission").first()).not.toContainText("verified")
  })

  test("logout returns the shell to anonymous account actions", async ({ page }) => {
    await page.goto("/")
    await page.getByRole("link", { name: "Connect Strava" }).click()
    await expect(page.getByRole("button", { name: "Logout" })).toBeVisible()

    await page.getByRole("button", { name: "Logout" }).click()
    await expect(page.getByRole("link", { name: "Connect Strava" })).toBeVisible()
  })

  test("mobile layout keeps critical controls reachable", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 })
    await page.goto("/")

    await expect(page.getByRole("heading", { name: "Online Runner Profile" })).toBeVisible()
    await expect(page.locator('[data-od-id="auth.connect.cta"]')).toBeVisible()
    await page.locator('[data-od-id="auth.connect.cta"]').click()

    const criticalSelectors = [
      '[data-od-id="topbar.account.actions"]',
      '[data-od-id="profile.safe-athlete-card"]',
      '[data-od-id="activity.recent-summary"]',
      '[data-od-id="evidence.submit.cta"]',
    ]

    for (const selector of criticalSelectors) {
      const box = await page.locator(selector).first().boundingBox()
      expect(box, `${selector} should be visible and measurable`).not.toBeNull()
      expect(box?.x ?? 0, `${selector} should not overflow left`).toBeGreaterThanOrEqual(0)
      expect((box?.x ?? 0) + (box?.width ?? 0), `${selector} should fit viewport`).toBeLessThanOrEqual(390)
    }
  })
})
