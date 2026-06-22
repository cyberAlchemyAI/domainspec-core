import { defineConfig, devices } from "@playwright/test"

const host = "127.0.0.1"
const port = 5174
const baseURL = `http://${host}:${port}`

export default defineConfig({
  testDir: "./e2e/troqar-product-architecture",
  testMatch: "ui.spec.ts",
  timeout: 30_000,
  expect: {
    timeout: 5_000,
  },
  use: {
    baseURL,
    trace: "on-first-retry",
  },
  webServer: {
    command: [
      "BODY_WAR_STRAVA_FAKE=1",
      "BODY_WAR_AUTH_BACKEND=memory",
      `BODY_WAR_HOST=${host}`,
      `BODY_WAR_PORT=${port}`,
      `BODY_WAR_PUBLIC_BASE_URL=${baseURL}`,
      `BODY_WAR_ALLOWED_ORIGINS=${baseURL}`,
      "node dist/server.js",
    ].join(" "),
    reuseExistingServer: false,
    timeout: 15_000,
    url: baseURL,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
})
