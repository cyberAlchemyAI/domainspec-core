import { expect, test } from "@playwright/test"

const rawAuthTerms = /access_token|refresh_token|client_secret|oauth code/i
const nonStravaProviders = /google|email|password|guest|facebook|apple/i

async function connectFakeStrava(page: import("@playwright/test").Page) {
  await page.goto("/")
  await page.locator('[data-od-id="auth.connect.cta"]').click()
  await expect(page.locator('[data-od-id="auth.callback-status"]')).toContainText("Strava conectado")
  await expect(page.locator('[data-od-id="profile.safe-athlete-card"]')).toBeVisible()
}

async function expectBoxFitsViewport(page: import("@playwright/test").Page, selector: string, width: number) {
  const box = await page.locator(selector).first().boundingBox()
  expect(box, `${selector} should be visible and measurable`).not.toBeNull()
  expect(box?.x ?? 0, `${selector} should not overflow left`).toBeGreaterThanOrEqual(0)
  expect((box?.x ?? 0) + (box?.width ?? 0), `${selector} should fit viewport`).toBeLessThanOrEqual(width)
}

test.describe("TROQAR production login and runner profile", () => {
  test("renders a Strava-only anonymous login-first page", async ({ page }) => {
    await page.goto("/")

    await expect(page.locator('[data-od-id="troqar.shell"]')).toBeVisible()
    await expect(page.locator('[data-od-id="auth.login-first"]')).toBeVisible()
    await expect(page.locator('[data-od-id="login.hero"]')).toContainText("Bora correr")
    await expect(page.locator('[data-od-id="login.trust-copy"]')).toContainText("credenciais ficam no servidor")
    await expect(page.locator('[data-od-id="login.preview-card"]')).toBeVisible()

    const visibleStravaCtas = page.getByRole("link", { name: "Entrar com Strava" }).filter({ visible: true })
    await expect(visibleStravaCtas).toHaveCount(1)
    await expect(page.locator('[data-od-id="auth.connect.cta"]')).toBeVisible()

    await expect(page.locator('[data-od-id="profile.safe-athlete-card"]')).toBeHidden()
    await expect(page.locator('[data-od-id="activity.recent-summary"]')).toBeHidden()
    await expect(page.locator('[data-od-id="evidence.submission-list"]')).toBeHidden()
    await expect(page.locator('[data-od-id="evidence.submit.cta"]')).toHaveCount(0)
    await expect(page.getByRole("button", { name: "Sair" })).toBeHidden()
    await expect(page.getByRole("link", { name: "Perfil" })).toBeHidden()

    await expect(page.locator("body")).not.toContainText(rawAuthTerms)
    await expect(page.locator('[data-od-id="auth.login-first"]')).not.toContainText(nonStravaProviders)
    await page.screenshot({ path: "test-results/troqar-anonymous-login.png", fullPage: true })
  })

  test("shows safe callback and provider error states", async ({ page }) => {
    await page.goto("/?connected=1")
    await expect(page.locator('[data-od-id="auth.callback-status"]')).toContainText("resumos seguros")

    await page.goto("/?auth_error=access_denied")
    await expect(page.locator('[data-od-id="auth.error.banner"]')).toContainText("Nao foi possivel conectar com Strava")
    await expect(page.locator('[data-od-id="auth.reconnect.cta"]')).toHaveText("Tentar Strava de novo")
    await expect(page.locator("body")).not.toContainText(rawAuthTerms)
  })

  test("connects fake Strava and renders safe profile, activity, and evidence UI", async ({ page }) => {
    await connectFakeStrava(page)

    await expect(page.getByText(/Conectado com escopo:/)).toBeVisible()
    await expect(page.locator('[data-od-id="profile.safe-athlete-card"]')).toContainText(
      "Credenciais ficam no servidor",
    )
    await expect(page.locator('[data-od-id="profile.strava-link"]').first()).toHaveText("Open public Strava profile")
    await expect(page.locator('[data-od-id="profile.strava-link"]').first()).toHaveAttribute(
      "href",
      /https:\/\/www\.strava\.com\/athletes\/\d+/,
    )
    await expect(page.locator('[data-od-id="activity.recent-summary"]')).toContainText(
      "Geometria da rota e pontuacao",
    )
    await expect(page.locator('[data-od-id="track.geometry-status"]').first()).toBeVisible()
    await expect(page.locator("body")).not.toContainText(rawAuthTerms)
    await expect(page.locator("body")).not.toContainText(/verified scoring|verified control|ranked evidence/i)
    await page.screenshot({ path: "test-results/troqar-connected-runner.png", fullPage: true })
  })

  test("submits one activity as preview evidence through visible controls", async ({ page }) => {
    await connectFakeStrava(page)

    const firstActivity = page.locator(".activity").first()
    await expect(firstActivity).toBeVisible()
    await firstActivity.locator("select").selectOption({ index: 0 })
    await firstActivity.locator('[data-od-id="evidence.submit.cta"]').click()

    await expect(page.locator(".submission").first()).toBeVisible()
    await expect(page.locator('[data-od-id="evidence.status-chip"]').first()).toContainText(/enviado/i)
    await expect(page.locator(".submission").first()).not.toContainText("verified")
  })

  test("logout returns the shell to anonymous account actions", async ({ page }) => {
    await connectFakeStrava(page)
    await expect(page.getByRole("button", { name: "Sair" })).toBeVisible()

    await page.getByRole("button", { name: "Sair" }).click()
    await expect(page.locator('[data-od-id="auth.login-first"]')).toBeVisible()
    await expect(page.getByRole("link", { name: "Entrar com Strava" }).filter({ visible: true })).toHaveCount(1)
  })

  for (const width of [390, 320]) {
    test(`keeps critical controls reachable at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 844 })
      await page.goto("/")

      await expect(page.locator('[data-od-id="login.hero"]')).toBeVisible()
      await expect(page.locator('[data-od-id="auth.connect.cta"]')).toBeVisible()
      await expectBoxFitsViewport(page, '[data-od-id="topbar.account.actions"]', width)
      await expectBoxFitsViewport(page, '[data-od-id="auth.connect.cta"]', width)

      await page.locator('[data-od-id="auth.connect.cta"]').click()
      const criticalSelectors = [
        '[data-od-id="topbar.account.actions"]',
        '[data-od-id="profile.safe-athlete-card"]',
        '[data-od-id="activity.recent-summary"]',
        '[data-od-id="evidence.submit.cta"]',
      ]

      for (const selector of criticalSelectors) {
        await expectBoxFitsViewport(page, selector, width)
      }
    })
  }
})
