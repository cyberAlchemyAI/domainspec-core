import { defineConfig } from "drizzle-kit";

const DEFAULT_DATABASE_URL =
  "postgres://body_war_e2e:body_war_e2e_password@127.0.0.1:55433/body_war_e2e";

export default defineConfig({
  schema: "./src/infrastructure/postgres/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url:
      process.env.BODY_WAR_DATABASE_URL ??
      process.env.DATABASE_URL ??
      DEFAULT_DATABASE_URL,
  },
});
