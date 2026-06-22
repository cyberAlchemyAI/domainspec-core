import { defineConfig } from "drizzle-kit";

const DEFAULT_E2E_DATABASE_URL =
  "postgres://auth_e2e:auth_e2e_password@127.0.0.1:55432/auth_user_management_e2e";

export default defineConfig({
  schema: "./src/infrastructure/drizzle-postgres/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url:
      process.env.AUTH_E2E_DATABASE_URL ??
      process.env.DATABASE_URL ??
      DEFAULT_E2E_DATABASE_URL,
  },
});
